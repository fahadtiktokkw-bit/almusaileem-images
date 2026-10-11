import unittest
from corrective_prompt import corrective_prompt
class TestCorrectivePrompt(unittest.TestCase):
 def test_issue_in_prompt(self):
  r={"semantic_review":{"findings":[{"description":"Arabic text moved"}]},"video":{"duration_seconds":7.04,"has_audio":True}}
  p=corrective_prompt(r,"clouds and camel")
  self.assertIn("Arabic text moved",p)
  self.assertIn("7.04s",p)
  self.assertIn("audio stream",p)
 def test_missing_vision_report_rejected(self):
  with self.assertRaises(ValueError):corrective_prompt({"semantic_review":"NOT_RUN"})
 def test_empty_findings(self):
  self.assertIn("No specific visual deviations",corrective_prompt({"semantic_review":{"findings":[]}}))
 def test_bad_findings(self):
  with self.assertRaises(ValueError):corrective_prompt({"semantic_review":{"findings":{}}})
if __name__=="__main__":unittest.main()
