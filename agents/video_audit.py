"""Almusaileem video audit V1.3. Requires ffmpeg/ffprobe; optional OpenAI API."""
import argparse, base64, json, os, subprocess, tempfile, urllib.request
from pathlib import Path
def command(args):
 p=subprocess.run(args,capture_output=True,text=True,check=True)
 return p.stdout
def probe(path):
 data=json.loads(command(["ffprobe","-v","error","-show_entries","format=duration:stream=codec_type,width,height","-of","json",str(path)]))
 return {"duration_seconds":float(data["format"]["duration"]),"has_audio":any(s.get("codec_type")=="audio" for s in data.get("streams",[])),"video_streams":[s for s in data.get("streams",[]) if s.get("codec_type")=="video"]}
def extract(video, folder, times):
 output=[]
 for i,t in enumerate(times):
  path=Path(folder)/f"frame_{i}.png"
  command(["ffmpeg","-hide_banner","-loglevel","error","-ss",str(t),"-i",str(video),"-frames:v","1","-y",str(path)])
  output.append(path)
 return output
def semantic(reference, images, motion, key, model):
 def part(path):
  data=base64.b64encode(Path(path).read_bytes()).decode()
  return {"type":"image_url","image_url":{"url":"data:image/png;base64,"+data,"detail":"low"}}
 items=[{"type":"text","text":"Compare original (first) to sampled video frames. Allowed motion: "+motion+". Identify any visible text/logo changes, geometry changes and forbidden motion. Return JSON with findings array, critical boolean and suggested_prompt string. Be cautious: these are sampled frames only."},part(reference)]+[part(x) for x in images]
 payload=json.dumps({"model":model,"messages":[{"role":"user","content":items}],"response_format":{"type":"json_object"},"max_tokens":900}).encode()
 req=urllib.request.Request("https://api.openai.com/v1/chat/completions",data=payload,headers={"Authorization":"Bearer "+key,"Content-Type":"application/json"})
 with urllib.request.urlopen(req,timeout=90) as r: answer=json.load(r)
 return json.loads(answer["choices"][0]["message"]["content"])
def audit(video, reference=None, allowed_motion="", vision=False, model="gpt-4.1-mini"):
 info=probe(video)
 if not info["video_streams"]: raise ValueError("No video stream")
 d=info["duration_seconds"]
 times=[min(d*f,max(0,d-0.05)) for f in (0.1,0.5,0.9)]
 result={"status":"REVIEW","video":info,"sample_times":times,"duration_10s_tolerance_pass":abs(d-10)<=0.25,"silent_pass":not info["has_audio"],"allowed_motion":allowed_motion,"semantic_review":"NOT_RUN"}
 if vision:
  if not reference: raise ValueError("--reference required for --vision")
  key=os.environ.get("OPENAI_API_KEY")
  if not key: raise ValueError("OPENAI_API_KEY required for --vision")
  with tempfile.TemporaryDirectory() as tmp: result["semantic_review"]=semantic(reference,extract(video,tmp,times),allowed_motion,key,model)
 return result
def main():
 p=argparse.ArgumentParser()
 p.add_argument("--video",required=True);p.add_argument("--reference");p.add_argument("--allowed-motion",default="")
 p.add_argument("--vision",action="store_true");p.add_argument("--model",default="gpt-4.1-mini");p.add_argument("--output")
 a=p.parse_args();r=json.dumps(audit(a.video,a.reference,a.allowed_motion,a.vision,a.model),ensure_ascii=False,indent=2)
 print(r)
 if a.output: Path(a.output).write_text(r+"\n",encoding="utf-8")
if __name__=="__main__":main()
