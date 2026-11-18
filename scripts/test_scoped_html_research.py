import hashlib,json,tempfile,unittest
from pathlib import Path
from PIL import Image
from record_scoped_pdf_research import inspect_html_assets
from literature_review import load_registry,digest
class HtmlAssets(unittest.TestCase):
 def fixture(self,root):
  base='https://example.org/book/';raw=b'<html><body>Own fixture<img src="figure.png"></body></html>'
  (root/'page.html').write_bytes(raw);Image.new('RGB',(8,6),'white').save(root/'figure.png')
  digest=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
  return dict(url=base+'page.html',asset_base_url=base,sha256=digest(root/'page.html'),html_assets=[dict(file='page.html',key='page',url=base+'page.html',title='Fixture',sha256=digest(root/'page.html'),status=200,content_type='text/html')],image_assets=[dict(file='figure.png',url=base+'figure.png',page_url=base+'page.html',sha256=digest(root/'figure.png'),status=200,content_type='image/png',dimensions=[8,6])])
 def test_actual_bytes_and_embedded_reference(self):
  with tempfile.TemporaryDirectory() as d:
   r=Path(d);s=self.fixture(r);pages,images=inspect_html_assets(s,r)
   self.assertEqual(len(pages),1);self.assertEqual(images[0]['dimensions'],[8,6]);self.assertFalse(images[0]['redistributed'])
 def test_changed_html_or_image_rejected(self):
  for name in ['page.html','figure.png']:
   with self.subTest(name=name),tempfile.TemporaryDirectory() as d:
    r=Path(d);s=self.fixture(r);(r/name).write_bytes(b'changed')
    with self.assertRaises(AssertionError):inspect_html_assets(s,r)
 def test_unlinked_image_rejected(self):
  with tempfile.TemporaryDirectory() as d:
   r=Path(d);s=self.fixture(r);s['image_assets'][0]['url']=s['asset_base_url']+'unlinked.png'
   with self.assertRaises(AssertionError):inspect_html_assets(s,r)
 def test_wrong_dimensions_rejected(self):
  with tempfile.TemporaryDirectory() as d:
   r=Path(d);s=self.fixture(r);s['image_assets'][0]['dimensions']=[6,8]
   with self.assertRaises(AssertionError):inspect_html_assets(s,r)
 def test_failed_response_or_foreign_origin_rejected(self):
  for changes in [dict(status=404),dict(url='https://other.org/figure.png')]:
   with self.subTest(changes=changes),tempfile.TemporaryDirectory() as d:
    r=Path(d);s=self.fixture(r);s['image_assets'][0].update(changes)
    with self.assertRaises(AssertionError):inspect_html_assets(s,r)
 def registry_fixture(self,root):
  spec=self.fixture(root);pages,images=inspect_html_assets(spec,root)
  source=dict(id='S',title='Fixture',url=spec['url'])
  fields=dict(source_asset_kind='publisher_html',source_asset_sha256=spec['sha256'],asset_base_url=spec['asset_base_url'],html_read_manifest=pages,image_read_manifest=images)
  notes=dict(source_id='S',source_url=spec['url'],read_scope='One page and embedded image',source_asset_redistributed=False,original_page_layout_review=False,pdf_read=False,contains_source_full_text=False,source_pdf_redistributed=False,reading_log=['read'],source_corrections=[],**fields)
  path=root/'data/literature_evidence/notes.json';path.parent.mkdir(parents=True);path.write_text(json.dumps(notes),encoding='utf-8')
  review=dict(source_id='S',reviewer='Fixture',date='2026-11-16',read_scope=notes['read_scope'],limits='No outcomes',independent_review=False,student_validated=False,snapshot_kind='authored_review_notes',snapshot_file='data/literature_evidence/notes.json',snapshot_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),bibliography_snapshot=digest(source),redistribution_license='workspace_authored_notes',display=dict(url=spec['url']),**fields)
  registry=dict(sources={'S':review},claims=[])
  (root/'data/sources.json').write_text(json.dumps([source]));(root/'data/literature_claim_reviews.json').write_text(json.dumps(registry))
  return registry
 def test_registry_keeps_canonical_url_and_separate_asset_base(self):
  with tempfile.TemporaryDirectory() as d:
   r=Path(d);self.registry_fixture(r);v=load_registry(r)['sources']['S']
   self.assertEqual(v['display']['url'],'https://example.org/book/page.html')
   self.assertEqual(v['asset_base_url'],'https://example.org/book/')
 def test_changed_asset_base_requires_review(self):
  with tempfile.TemporaryDirectory() as d:
   r=Path(d);v=self.registry_fixture(r);v['sources']['S']['asset_base_url']='https://other.org/'
   (r/'data/literature_claim_reviews.json').write_text(json.dumps(v))
   with self.assertRaisesRegex(AssertionError,'asset base'):load_registry(r)
if __name__=='__main__':unittest.main()
