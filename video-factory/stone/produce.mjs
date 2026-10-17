import {spawnSync} from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
const out=path.resolve(process.env.STONE_OUTPUT_DIR || 'output');fs.mkdirSync(out,{recursive:true});
const cli=path.resolve('node_modules/.bin/hyperframes');
function run(args,timeout){const r=spawnSync(cli,args,{encoding:'utf8',timeout,maxBuffer:16*1024*1024,env:process.env});return {ok:r.status===0,output:(r.stdout||'')+(r.stderr||''),error:r.error?.message};}
const build=spawnSync(process.execPath,['build.mjs'],{stdio:'inherit'});if(build.status!==0)process.exit(1);
const lint=run(['lint','--json'],60000);fs.writeFileSync(path.join(out,'lint.json'),lint.output);if(!lint.ok)throw new Error('Template lint failed; see lint.json');
const check=run(['check','--at','1,6,10,14','--json'],120000);fs.writeFileSync(path.join(out,'hyperframes-check.json'),check.output);
let mode='hyperframes';
if(check.ok){const render=run(['render','--fps','30','--quality','delivery','--workers','1','--output',path.join(out,'catalogue.mp4')],240000);fs.writeFileSync(path.join(out,'hyperframes-render.log'),render.output);if(!render.ok)mode='browser-fallback';}else mode='browser-fallback';
if(mode==='browser-fallback'){
 console.log('HyperFrames browser path unavailable; rendering the same HTML timeline using the documented local fallback.');
 const r=spawnSync(process.execPath,['render-browser.mjs',out],{stdio:'inherit',timeout:600000,env:process.env});if(r.status!==0)throw new Error('Fallback rendering failed');
}else{
 const r=spawnSync('ffmpeg',['-y','-v','error','-ss','1','-i',path.join(out,'catalogue.mp4'),'-frames:v','1',path.join(out,'preview.jpg')],{stdio:'inherit'});if(r.status!==0)throw new Error('Preview extraction failed');
}
const v=spawnSync(process.execPath,['verify.mjs',out],{stdio:'inherit'});if(v.status!==0)throw new Error('Video verification failed');
fs.writeFileSync(path.join(out,'run.json'),JSON.stringify({renderer:mode,hyperframesRuntimeCheckPassed:check.ok,commit:process.env.GITHUB_SHA||null,runId:process.env.GITHUB_RUN_ID||null},null,2));
console.log('Verified video output: '+path.join(out,'catalogue.mp4'));
