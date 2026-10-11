# Almusaileem Visual Audit V1.2
Pixel-level comparison for still images, **not** a semantic vision model.

Install: `pip install Pillow`

Run:
```bash
python agents/visual_audit.py --reference before.png --result after.png --allowed-regions "[[0.1,0.2,0.7,0.8]]" --output audit.json
```

Allowed regions are normalized rectangles [left,top,right,bottom], 0..1. Pixels changed outside allowed areas are reported separately. No mask means every pixel is protected. The result is always REVIEW, never an automatic approval.

Test:
```bash
cd agents
python -m unittest test_visual_audit.py -v
```

Limitations: requires equal-sized aligned images. Camera shifts, lighting changes and compression can trigger differences. Does not understand text, logos, architecture, sound, video duration, or whether an edit is desirable. No Grok or Google Drive API integration.