import tempfile,unittest,re
from pathlib import Path
from html.parser import HTMLParser
from build_inquiry_workbook import build
class WorkbookModels(unittest.TestCase):
 def output(self):
  with tempfile.TemporaryDirectory() as d:
   text=build(Path(d));self.assertEqual(text,(Path(d)/'inquiry-workbook.html').read_text(encoding='utf-8'));return text
 def test_integer_model_rows_match_independent_expected_areas(self):
  text=self.output();rows=re.findall(r'<tr data-x="(\d+)">(.*?)</tr>',text)
  self.assertEqual(len(rows),9)
  areas=[9,16,21,24,25,24,21,16,9]
  for i,(x,body) in enumerate(rows,1):
   cells=[int(n) for n in re.findall(r'<td>(\d+)</td>',body)]
   self.assertEqual(cells,[i,10-i,20,areas[i-1]])
  self.assertNotIn('data-x="0"',text);self.assertNotIn('data-x="10"',text)
 def test_drawings_use_one_shared_scale_and_match_dimensions(self):
  text=self.output()
  class Rectangles(HTMLParser):
   def __init__(self):super().__init__();self.rects=[]
   def handle_starttag(self,tag,attrs):
    a=dict(attrs)
    if tag=='rect' and 'data-model-x' in a:self.rects.append(a)
  parser=Rectangles();parser.feed(text)
  self.assertEqual(len(parser.rects),3)
  sizes=[(float(a['width']),float(a['height'])) for a in parser.rects]
  self.assertEqual(sizes,[(12,108),(60,60),(108,12)])
  self.assertEqual([2*(w+h) for w,h in sizes],[240,240,240])
  self.assertEqual([w*h for w,h in sizes],[1296,3600,1296])
if __name__=='__main__':unittest.main()
