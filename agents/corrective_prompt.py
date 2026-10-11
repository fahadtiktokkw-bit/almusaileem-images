"""Almusaileem V1.4: convert a reviewed video audit report into a corrective prompt.
Works offline with V1.3 JSON reports. No claim of automatic video editing.
"""
import argparse
import json
from pathlib import Path

PROTECTED = ("text", "logo", "typography", "background", "geometry", "camera", "dust", "audio", "duration")
def corrective_prompt(report, allowed_motion="clouds and camel", duration=10):
    if not isinstance(report,dict):
        raise ValueError("report must be an object")
    review=report.get("semantic_review")
    if not isinstance(review,dict):
        raise ValueError("semantic_review must be a JSON object from an actual vision review")
    findings=review.get("findings",[])
    if not isinstance(findings,list):
        raise ValueError("findings must be a list")
    details=[]
    for finding in findings:
        if isinstance(finding,dict):
            desc=str(finding.get("description") or finding.get("issue") or "").strip()
        elif isinstance(finding,str):
            desc=finding.strip()
        else:
            continue
        if desc:
            details.append(desc[:500])
    problems="; ".join(details[:12]) or "No specific visual deviations reported"
    d=report.get("video",{}).get("duration_seconds")
    has_audio=report.get("video",{}).get("has_audio")
    if d is not None and abs(float(d)-duration)>0.25:
        problems+=f"; previous duration {float(d):.2f}s differs from requested {duration}s"
    if has_audio:
        problems+="; previous output contains an audio stream"
    return (
        f"Generate exactly {duration} seconds of silent image-to-video animation using the ORIGINAL source image. "
        f"ALLOW MOTION ONLY: {allowed_motion}. "
        "Lock the camera and preserve framing, typography, logos, ornaments, architecture, background, "
        "colors, geometry and original subject identity. No zoom, cuts, morphing, dust, particles, "
        "extra objects, voice, ambient sound or music. "
        "Fix these observed issues without changing anything else: "+problems+". "
        "Keep all protected regions visually unchanged. Do not redesign the source."
    )
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--report",required=True)
    p.add_argument("--allowed-motion",default="clouds and camel")
    p.add_argument("--duration",type=float,default=10)
    p.add_argument("--output")
    a=p.parse_args()
    if a.duration<=0: p.error("duration must be positive")
    data=json.loads(Path(a.report).read_text(encoding="utf-8"))
    prompt=corrective_prompt(data,a.allowed_motion,a.duration)
    print(prompt)
    if a.output: Path(a.output).write_text(prompt+"\n",encoding="utf-8")
if __name__=="__main__": main()
