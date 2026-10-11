# Almusaileem Video Audit V1.3
Requirements: Python 3.10+, ffmpeg and ffprobe on PATH. Standard Python library only.

Metadata mode (offline):
```bash
python agents/video_audit.py --video clip.mp4 --allowed-motion "clouds and camel" --output report.json
```

Optional AI visual review (requires OPENAI_API_KEY and API billing):
```bash
python agents/video_audit.py --video clip.mp4 --reference original.png --allowed-motion "clouds and camel only; text static" --vision --output report.json
```

With --vision the reference and three extracted video frames are sent to OpenAI API. Without --vision no images are uploaded. The API model defaults to gpt-4.1-mini and must be accessible to the API account. Review output manually. Audio stream absence does not prove audible silence. This tool does not control Grok, detect all intermediate-frame changes, or automatically edit videos.

Tests: `cd agents && python -m unittest -v test_video_audit.py`
