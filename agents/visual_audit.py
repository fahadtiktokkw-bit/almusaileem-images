#!/usr/bin/env python3
"""Almusaileem V1.2: pixel-level reference comparison, NOT semantic visual AI.
Requires: pip install Pillow
"""
import argparse
import json
from pathlib import Path
from PIL import Image, ImageChops, ImageStat

def compare(reference, result, allowed=None, threshold=20):
    with Image.open(reference) as src, Image.open(result) as dst:
        if src.size != dst.size:
            return {"status": "REVIEW", "reason": "image_dimensions_differ", "reference_size": list(src.size), "result_size": list(dst.size)}
        src, dst = src.convert("RGB"), dst.convert("RGB")
        w, h = src.size
        allowed = allowed or []
        rectangles = []
        for rect in allowed:
            if len(rect) != 4 or any(not isinstance(v, (float,int)) or not 0 <= v <= 1 for v in rect):
                raise ValueError("Allowed regions must be normalized [x1,y1,x2,y2] coordinates in [0,1]")
            x1,y1,x2,y2 = rect
            if x1 >= x2 or y1 >= y2:
                raise ValueError("Allowed region must have positive area")
            rectangles.append((int(x1*w),int(y1*h),int(x2*w),int(y2*h)))
        diff = ImageChops.difference(src,dst)
        pixels = diff.load()
        changed = outside = protected = 0
        total_difference = 0
        for y in range(h):
            for x in range(w):
                d = max(pixels[x,y])
                if d > threshold:
                    changed += 1
                    if not any(x1 <= x < x2 and y1 <= y < y2 for x1,y1,x2,y2 in rectangles):
                        outside += 1
                total_difference += sum(pixels[x,y])/3
                if not any(x1 <= x < x2 and y1 <= y < y2 for x1,y1,x2,y2 in rectangles):
                    protected += 1
        # REVIEW is deliberately conservative; pixel differences cannot establish visual correctness.
        return {
            "status": "REVIEW",
            "reference_size": [w,h],
            "changed_pixels": changed,
            "changed_percent": round(100*changed/(w*h),3),
            "changed_outside_allowed_pixels": outside,
            "changed_outside_allowed_percent_of_full_image": round(100*outside/(w*h),3),
            "mean_absolute_channel_difference": round(total_difference/(w*h),3),
            "allowed_regions": allowed,
            "note": "Pixel-only check. Does not recognize text, logos, objects, geometry, lighting quality, video duration or audio. Align images first. A human or vision model must review."
        }

def main():
    p=argparse.ArgumentParser(description="Pixel comparison for two equally sized images")
    p.add_argument("--reference",required=True)
    p.add_argument("--result",required=True)
    p.add_argument("--allowed-regions",default="[]",help='JSON normalized rectangles, e.g. [[0.1,0.2,0.5,0.6]]')
    p.add_argument("--threshold",type=int,default=20)
    p.add_argument("--output")
    a=p.parse_args()
    if not 0 <= a.threshold <= 255: p.error("threshold must be 0..255")
    report=compare(a.reference,a.result,json.loads(a.allowed_regions),a.threshold)
    rendered=json.dumps(report,ensure_ascii=False,indent=2)
    print(rendered)
    if a.output: Path(a.output).write_text(rendered+"\n",encoding="utf-8")
if __name__=="__main__": main()
