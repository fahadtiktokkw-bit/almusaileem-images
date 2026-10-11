"""Almusaileem V1.8: offline multi-region visual stability audit, no OCR."""
import argparse,json
from pathlib import Path
import cv2,numpy as np
REGIONS={"verse":[.285,.425],"explanation":[.44,.715],"glossary":[.715,.89],"source_footer":[.89,.985]}
def analyze(video,reference,output):
 cap=cv2.VideoCapture(str(video))
 if not cap.isOpened():raise ValueError("Video unavailable")
 fps=cap.get(cv2.CAP_PROP_FPS)
 original=cv2.imread(str(reference))
 if original is None:raise ValueError("Reference unavailable")
 ok,first=cap.read()
 if not ok:raise ValueError("Empty video")
 h,w=first.shape[:2]
 reference_resized=cv2.resize(original,(w,h),interpolation=cv2.INTER_AREA)
 accum={name:{"max_temporal_edge_disagreement_pct":0,"max_temporal_pixel_change_pct":0,"reference_to_first_edge_disagreement_pct":0} for name in REGIONS}
 masks={}
 for name,(a,b) in REGIONS.items():
  y1,y2=round(a*h),round(b*h)
  gray_first=cv2.cvtColor(first[y1:y2],cv2.COLOR_BGR2GRAY)
  gray_ref=cv2.cvtColor(reference_resized[y1:y2],cv2.COLOR_BGR2GRAY)
  edges_first=cv2.Canny(gray_first,70,150)
  edges_ref=cv2.Canny(gray_ref,70,150)
  accum[name]["reference_to_first_edge_disagreement_pct"]=round(float(np.mean(edges_first!=edges_ref)*100),3)
  masks[name]=(y1,y2,gray_first,edges_first)
 n=1
 while True:
  ok,frame=cap.read()
  if not ok:break
  for name,(y1,y2,gray_first,edges_first) in masks.items():
   gray=cv2.cvtColor(frame[y1:y2],cv2.COLOR_BGR2GRAY)
   edge=cv2.Canny(gray,70,150)
   e=float(np.mean(edge!=edges_first)*100)
   p=float(np.mean(cv2.absdiff(gray,gray_first)>25)*100)
   accum[name]["max_temporal_edge_disagreement_pct"]=round(max(accum[name]["max_temporal_edge_disagreement_pct"],e),3)
   accum[name]["max_temporal_pixel_change_pct"]=round(max(accum[name]["max_temporal_pixel_change_pct"],p),3)
  n+=1
 cap.release()
 report={"version":"1.8","status":"REVIEW","decoded_frames":n,"fps":fps,"duration_s":round(n/fps,3),"regions":{name:{"normalized_y":REGIONS[name],**stats} for name,stats in accum.items()},"limitations":"Compares pixel edges only, not Arabic text accuracy. Resizing/compression affect scores. Must review Quranic text manually."}
 Path(output).parent.mkdir(parents=True,exist_ok=True)
 Path(output).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
 return report
if __name__=="__main__":
 p=argparse.ArgumentParser()
 p.add_argument("--video",required=True);p.add_argument("--reference",required=True);p.add_argument("--output",required=True)
 a=p.parse_args()
 print(json.dumps(analyze(a.video,a.reference,a.output),ensure_ascii=False,indent=2))
