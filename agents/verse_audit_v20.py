"""Almusaileem V2.0 offline verse comparison. Requires opencv-python, numpy."""
import cv2,numpy as np,json,argparse
from pathlib import Path
def audit(reference,video,outdir):
 out=Path(outdir);out.mkdir(parents=True,exist_ok=True)
 ref=cv2.imread(str(reference))
 if ref is None:raise ValueError("Reference unreadable")
 cap=cv2.VideoCapture(str(video));frames=[]
 while True:
  ok,f=cap.read()
  if not ok:break
  frames.append(f)
 cap.release()
 if not frames:raise ValueError("Video unreadable")
 h,w=frames[0].shape[:2];ref=cv2.resize(ref,(w,h),interpolation=cv2.INTER_AREA)
 x1,y1,x2,y2=int(w*.16),int(h*.302),int(w*.85),int(h*.38)
 def gray(im):return cv2.cvtColor(im[y1:y2,x1:x2],cv2.COLOR_BGR2GRAY)
 def compare(a,b):
  a,b=gray(a),gray(b);d=cv2.absdiff(a,b)
  ea,eb=cv2.Canny(a,70,150),cv2.Canny(b,70,150)
  return {"changed_pixels_over_25_pct":round(float(np.mean(d>25)*100),3),"edge_disagreement_pct":round(float(np.mean(ea!=eb)*100),3),"mean_absolute_difference":round(float(d.mean()),3)}
 first,last=frames[0],frames[-1]
 comparisons={"reference_vs_first":compare(ref,first),"reference_vs_last":compare(ref,last),"first_vs_last":compare(first,last)}
 cv2.imwrite(str(out/"verse_reference_first_last.jpg"),np.concatenate([ref[y1:y2,x1:x2],first[y1:y2,x1:x2],last[y1:y2,x1:x2]],axis=0))
 report={"version":"2.0","frames_decoded":len(frames),"video_resolution":[w,h],"roi":[x1,y1,x2,y2],"comparisons":comparisons,"status":"HUMAN_REVIEW_REQUIRED","limitations":"Pixel/edge comparison only, not verification of Quranic wording or diacritics. Resampling and compression affect scores."}
 (out/"verse_audit_v20.json").write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
 return report
if __name__=="__main__":
 p=argparse.ArgumentParser();p.add_argument("--reference",required=True);p.add_argument("--video",required=True);p.add_argument("--output-dir",required=True)
 a=p.parse_args();print(json.dumps(audit(a.reference,a.video,a.output_dir),ensure_ascii=False,indent=2))
