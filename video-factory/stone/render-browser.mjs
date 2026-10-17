import puppeteer from 'puppeteer-core';
import fs from 'node:fs';import path from 'node:path';import {pathToFileURL} from 'node:url';
import {spawn} from 'node:child_process';import {once} from 'node:events';
const out=path.resolve(process.argv[2]||'output');fs.mkdirSync(out,{recursive:true});
const executablePath=process.env.HYPERFRAMES_BROWSER_PATH || process.env.CHROME_PATH;
if(!executablePath)throw new Error('Set HYPERFRAMES_BROWSER_PATH to installed Chrome');
let browser,encoder;
try{
 browser=await puppeteer.launch({executablePath,headless:true,pipe:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 const page=await browser.newPage();await page.setViewport({width:1080,height:1920});
 const errors=[];page.on('pageerror',e=>errors.push(e.message));
 await page.goto(pathToFileURL(path.resolve('index.html')).href,{waitUntil:'load'});
 await page.evaluate(()=>document.fonts.ready);await page.waitForFunction(()=>!!window.__timelines?.main);
 const assets=await page.evaluate(()=>[...document.images].every(i=>i.complete&&i.naturalWidth>0));if(!assets)throw new Error('An image did not load');
 const final=path.join(out,'catalogue.mp4'),temporary=path.join(out,'catalogue.partial.mp4');
 encoder=spawn('ffmpeg',['-y','-loglevel','error','-f','image2pipe','-vcodec','png','-framerate','30','-i','pipe:0','-an','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',temporary],{stdio:['pipe','inherit','inherit']});
 const closed=once(encoder,'close');let streamError;encoder.stdin.on('error',e=>streamError=e);
 for(let frame=0;frame<450;frame++){
  await page.evaluate(t=>{window.__timelines.main.pause().seek(t);document.querySelectorAll('[data-start]:not(#root)').forEach(e=>{const start=Number(e.dataset.start),duration=Number(e.dataset.duration);e.style.visibility=t>=start&&t<start+duration?'visible':'hidden';});window.gsap.ticker.tick();},frame/30);
  if(frame===30)await page.screenshot({path:path.join(out,'preview.jpg'),type:'jpeg',quality:92});
  const bytes=await page.screenshot({type:'png'});if(streamError)throw streamError;if(!encoder.stdin.write(bytes))await once(encoder.stdin,'drain');
  if(frame%90===0)console.log(`frame ${frame}/450`);
 }
 encoder.stdin.end();const [code]=await closed;if(code!==0)throw new Error(`FFmpeg exited ${code}`);
 if(errors.length)throw new Error(errors.join('\n'));fs.renameSync(temporary,final);
}finally{if(encoder&&encoder.exitCode===null)encoder.kill('SIGTERM');if(browser)await browser.close();}
