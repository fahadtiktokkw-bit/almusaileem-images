import tempfile
import unittest
from pathlib import Path
from PIL import Image
from visual_audit import compare

class VisualAuditTests(unittest.TestCase):
    def test_identical(self):
        with tempfile.TemporaryDirectory() as t:
            a=Path(t)/"a.png"; Image.new("RGB",(10,10),"white").save(a)
            self.assertEqual(compare(a,a)["changed_pixels"],0)
    def test_changed_outside_region(self):
        with tempfile.TemporaryDirectory() as t:
            a=Path(t)/"a.png"; b=Path(t)/"b.png"
            Image.new("RGB",(10,10),"white").save(a)
            im=Image.new("RGB",(10,10),"white"); im.putpixel((9,9),(0,0,0)); im.save(b)
            self.assertEqual(compare(a,b,[[0,0,0.5,0.5]])["changed_outside_allowed_pixels"],1)
    def test_changed_inside_region(self):
        with tempfile.TemporaryDirectory() as t:
            a=Path(t)/"a.png"; b=Path(t)/"b.png"
            Image.new("RGB",(10,10),"white").save(a)
            im=Image.new("RGB",(10,10),"white"); im.putpixel((1,1),(0,0,0)); im.save(b)
            self.assertEqual(compare(a,b,[[0,0,0.5,0.5]])["changed_outside_allowed_pixels"],0)
    def test_dimension_mismatch(self):
        with tempfile.TemporaryDirectory() as t:
            a=Path(t)/"a.png"; b=Path(t)/"b.png"
            Image.new("RGB",(10,10)).save(a); Image.new("RGB",(11,10)).save(b)
            self.assertEqual(compare(a,b)["reason"],"image_dimensions_differ")
    def test_invalid_region(self):
        with tempfile.TemporaryDirectory() as t:
            a=Path(t)/"a.png"; Image.new("RGB",(10,10)).save(a)
            with self.assertRaises(ValueError): compare(a,a,[[0.5,0.5,0.2,0.2]])
if __name__=="__main__": unittest.main()
