"""Almusaileem V1.7 offline protected-region audit. Requires cv2 and numpy."""
import argparse, json
from pathlib import Path
import cv2
import numpy as np
def inspect(video, reference, output, protected_top=0.31, sample_step=1):
    if not 0 <= protected_top < 1 or sample_step < 1: raise ValueError("Invalid parameters")
    cap=cv2.VideoCapture(str(video))
    if not cap.isOpened(): raise ValueError("Cannot open video")
    fps=cap.get(cv2.CAP_PROP_FPS)
    if fps<=0: raise ValueError("Invalid FPS")
    original=cv2.imread(str(reference))
    if original is None: raise ValueError("Cannot open reference")
    n=0; first=None; samples=[]
    while True:
        ok,frame=cap.read()
        if not ok: break
        if first is None: first=frame.copy()
        if n%sample_step==0:
            y=int(frame.shape[0]*protected_top)
            a=cv2.cvtColor(first[y:],cv2.COLOR_BGR2GRAY)
            b=cv2.cvtColor(frame[y:],cv2.COLOR_BGR2GRAY)
            edges_a=cv2.Canny(a,70,150);edges_b=cv2.Canny(b,70,150)
            samples.append({"frame":n,"time_s":round(n/fps,3),"changed_pixels_pct":round(float(np.mean(cv2.absdiff(a,b)>25)*100),3),"edge_disagreement_pct":round(float(np.mean(edges_a!=edges_b)*100),3)})
        n+=1
    cap.release()
    if n==0: raise ValueError("Empty video")
    h,w=first.shape[:2];y=int(h*protected_top)
    resized=cv2.resize(original,(w,h),interpolation=cv2.INTER_AREA)
    src=cv2.Canny(cv2.cvtColor(resized[y:],cv2.COLOR_BGR2GRAY),70,150)
    dst=cv2.Canny(cv2.cvtColor(first[y:],cv2.COLOR_BGR2GRAY),70,150)
    report={"status":"REVIEW","version":"1.7","decoded_frames":n,"fps":fps,"duration_estimate_s":round(n/fps,3),"video_size":[w,h],"reference_size":[original.shape[1],original.shape[0]],"protected_top_fraction":protected_top,"reference_to_first_edge_disagreement_pct":round(float(np.mean(src!=dst)*100),3),"max_temporal_edge_disagreement_pct":max(x["edge_disagreement_pct"] for x in samples),"max_temporal_pixel_change_pct":max(x["changed_pixels_pct"] for x in samples),"samples":samples[::max(1,len(samples)//12)],"limitations":"Not OCR or Quranic text verification; human review required."}
    Path(output).parent.mkdir(parents=True,exist_ok=True)
    Path(output).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
    return report
if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--video",required=True);p.add_argument("--reference",required=True);p.add_argument("--output",required=True);p.add_argument("--protected-top",type=float,default=.31);p.add_argument("--sample-step",type=int,default=1)
    a=p.parse_args()
    print(json.dumps(inspect(a.video,a.reference,a.output,a.protected_top,a.sample_step),ensure_ascii=False,indent=2))
