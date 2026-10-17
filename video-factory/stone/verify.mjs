import {spawnSync} from 'node:child_process';import fs from 'node:fs';import path from 'node:path';
const out=path.resolve(process.argv[2]||process.env.STONE_OUTPUT_DIR||'output'),file=path.join(out,'catalogue.mp4');
const probe=spawnSync('ffprobe',['-v','error','-show_streams','-show_format','-of','json',file],{encoding:'utf8'});if(probe.status!==0)throw new Error(probe.stderr);
const info=JSON.parse(probe.stdout),video=info.streams.find(s=>s.codec_type==='video');
if(!video||video.width!==1080||video.height!==1920||video.r_frame_rate!=='30/1'||Number(video.nb_frames)!==450||Math.abs(Number(info.format.duration)-15)>0.05)throw new Error('Unexpected video dimensions, duration or frame count');
const decode=spawnSync('ffmpeg',['-v','error','-i',file,'-f','null','-'],{encoding:'utf8'});if(decode.status!==0||decode.stderr.trim())throw new Error(decode.stderr||'Video decode failed');
fs.writeFileSync(path.join(out,'verification.json'),JSON.stringify({ok:true,width:1080,height:1920,fps:30,frames:450,duration:Number(info.format.duration),bytes:fs.statSync(file).size},null,2));console.log('Verification passed: 1080x1920, 30fps, 450 frames, 15s');
