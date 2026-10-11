# Almusaileem Video Audit | 2026-10-11 | V1.5
Reference: 1000097522.jpg
Video: 1000097526.mp4

## Measured
- Duration: 7.041667 s (target 10 s)
- Resolution: 720 x 1280; 24 fps
- Decoded frames: 168
- AAC audio present; mean volume -13.9 dB, maximum -2.6 dB (audible signal, not silent)
- Against first frame at frame 156, average absolute pixel difference (0-255): top 370 rows 43.63; lower rows 3.41
- In lower region, 2.15% of pixels differ by over 25 intensity units from first frame at frame 156.

## Assessment
REVISE. Missing target duration and silence. Lower text region is relatively stable but not identical pixel-for-pixel. This comparison does not establish whether Quranic typography is preserved exactly, nor attribute top-region movement specifically to clouds or camel.

## Correction
Create an exactly 10-second silent vertical video from the original image. Animate ONLY slow cloud drift and subtle camel breathing/head movement. Completely lock all Quranic text, explanations, decorative frames, ground, dust, plants, mountains, sun, and camera. No zoom, cuts, morphing, additional objects or audio track.

## Method and limitations
Decoded all 168 frames with OpenCV and sampled pixel differences every 12 frames relative to the first video frame. ffprobe for metadata; ffmpeg volumedetect for audio levels. Compression and color changes can produce differences; semantic visual review and frame-by-frame text recognition have not been performed. No Grok automation or regeneration was run.
