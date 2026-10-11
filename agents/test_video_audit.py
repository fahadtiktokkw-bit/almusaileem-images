import unittest
from unittest.mock import patch
import video_audit
class Tests(unittest.TestCase):
 def test_probe(self):
  with patch.object(video_audit,"command",return_value='{"format":{"duration":"10.0"},"streams":[{"codec_type":"video"}]}'):
   self.assertFalse(video_audit.probe("x.mp4")["has_audio"])
 def test_metadata(self):
  with patch.object(video_audit,"probe",return_value={"duration_seconds":10.0,"has_audio":False,"video_streams":[{}]}):
   r=video_audit.audit("x.mp4");self.assertTrue(r["silent_pass"]);self.assertTrue(r["duration_10s_tolerance_pass"])
 def test_audio(self):
  with patch.object(video_audit,"probe",return_value={"duration_seconds":9.0,"has_audio":True,"video_streams":[{}]}):
   r=video_audit.audit("x.mp4");self.assertFalse(r["silent_pass"]);self.assertFalse(r["duration_10s_tolerance_pass"])
 def test_reference_required(self):
  with patch.object(video_audit,"probe",return_value={"duration_seconds":10.0,"has_audio":False,"video_streams":[{}]}):
   with self.assertRaises(ValueError):video_audit.audit("x.mp4",vision=True)
if __name__=="__main__":unittest.main()
