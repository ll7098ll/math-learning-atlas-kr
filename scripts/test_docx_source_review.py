import unittest,tempfile,json,copy,hashlib
from pathlib import Path
from zipfile import ZipFile
from io import BytesIO
from PIL import Image
from docx_source_review import inspect_docx_source,validate_docx_review,W,R,C,A
from literature_review import load_registry,digest

class DocxSourceEvidence(unittest.TestCase):
 def fixture(self,root):
  image=BytesIO();Image.new('RGB',(8,6),'white').save(image,format='PNG')
  path=root/'source.docx'
  with ZipFile(path,'w') as z:
   z.writestr('word/document.xml',f'<w:document xmlns:w="{W}" xmlns:r="{R}" xmlns:c="{C}" xmlns:a="{A}"><w:body><w:p><w:r><w:t>Own fixture</w:t><w:instrText>Hidden field instructions</w:instrText></w:r><c:chart r:id="chart"/><a:blip r:embed="image"/></w:p><w:sectPr/></w:body></w:document>')
   z.writestr('word/_rels/document.xml.rels','<Relationships><Relationship Id="chart" Target="charts/chart1.xml"/><Relationship Id="image" Target="media/image1.png"/></Relationships>')
   z.writestr('word/charts/chart1.xml',f'<c:chartSpace xmlns:c="{C}"><c:chart/></c:chartSpace>');z.writestr('word/media/image1.png',image.getvalue())
  return dict(file='source.docx',sha256=hashlib.sha256(path.read_bytes()).hexdigest(),docx_url='https://example.org/source.docx',repository_record_url='https://example.org/record',block_ids=[1,2],chart_parts=['word/charts/chart1.xml'],image_parts=['word/media/image1.png'],other_text_parts=[])
 def reviews(self,root):
  spec=self.fixture(root);manifest=inspect_docx_source(spec,root);source=dict(id='S',title='Own fixture',url=spec['repository_record_url'])
  fields=dict(source_asset_kind='repository_docx',source_asset_sha256=spec['sha256'],repository_docx_review=manifest)
  notes=dict(source_id='S',source_url=source['url'],read_scope='Native blocks, chart cache and image; no PDF reading',pdf_read=False,original_page_layout_review=False,source_asset_redistributed=False,source_pdf_redistributed=False,contains_source_full_text=False,reading_log=['Read fixture'],source_corrections=[],**fields)
  review=dict(source_id='S',reviewer='Fixture',date='2026-11-17',read_scope=notes['read_scope'],limits='No outcomes or rendered page fidelity',independent_review=False,student_validated=False,snapshot_kind='authored_review_notes',snapshot_file='data/literature_evidence/notes.json',bibliography_snapshot=digest(source),redistribution_license='workspace_authored_notes',display=dict(url=source['url']),**fields)
  return spec,source,notes,review
 def test_native_content_and_embedded_references_bind_without_hidden_field_text(self):
  with tempfile.TemporaryDirectory() as d:
   r=Path(d);s=self.fixture(r);m=inspect_docx_source(s,r);self.assertEqual(m['embedded_images'][0]['dimensions'],[8,6]);self.assertTrue(m['all_body_blocks_read']);self.assertFalse(m['document_page_layout_verified']);self.assertEqual(m['selected_body_blocks'][0]['text_sha256'],hashlib.sha256(b'Own fixture').hexdigest())
 def test_changed_binary_rejected(self):
  with tempfile.TemporaryDirectory() as d:
   r=Path(d);s=self.fixture(r);(r/s['file']).write_bytes(b'changed')
   with self.assertRaises(AssertionError):inspect_docx_source(s,r)
 def test_unlinked_chart_or_image_rejected(self):
  for key in ['chart_parts','image_parts']:
   with self.subTest(key=key),tempfile.TemporaryDirectory() as d:
    r=Path(d);s=self.fixture(r);s[key]=['word/unlinked.xml']
    with self.assertRaisesRegex(AssertionError,'Unlinked'):inspect_docx_source(s,r)
 def test_complete_reading_cannot_drop_a_body_block(self):
  with tempfile.TemporaryDirectory() as d:
   _,_,n,v=self.reviews(Path(d));n=copy.deepcopy(n);v=copy.deepcopy(v);n['repository_docx_review']['selected_body_blocks'].pop();v['repository_docx_review']=copy.deepcopy(n['repository_docx_review'])
   with self.assertRaises(AssertionError):validate_docx_review(v,n)
 def test_pdf_or_page_layout_promotion_rejected(self):
  for mutation in ['pdf_hash','pdf_read','page_layout','chart_layout']:
   with self.subTest(mutation=mutation),tempfile.TemporaryDirectory() as d:
    _,_,n,v=self.reviews(Path(d));n=copy.deepcopy(n);v=copy.deepcopy(v)
    if mutation=='pdf_hash':v['source_pdf_sha256']='a'*64
    elif mutation=='pdf_read':n['pdf_read']=True
    elif mutation=='page_layout':n['original_page_layout_review']=True
    else:n['repository_docx_review']['chart_parts'][0]['visual_layout_verified']=True;v['repository_docx_review']=copy.deepcopy(n['repository_docx_review'])
    with self.assertRaises(AssertionError):validate_docx_review(v,n)
 def test_changed_part_hash_rejected(self):
  with tempfile.TemporaryDirectory() as d:
   _,_,n,v=self.reviews(Path(d));n=copy.deepcopy(n);v=copy.deepcopy(v);n['repository_docx_review']['chart_parts'][0]['sha256']='b'*64;v['repository_docx_review']=copy.deepcopy(n['repository_docx_review'])
   with self.assertRaisesRegex(AssertionError,'part hash'):validate_docx_review(v,n)
 def test_portable_registry_validation_needs_no_private_docx(self):
  with tempfile.TemporaryDirectory() as d:
   r=Path(d);_,source,n,v=self.reviews(r);p=r/v['snapshot_file'];p.parent.mkdir(parents=True);p.write_text(json.dumps(n),encoding='utf-8');v['snapshot_sha256']=hashlib.sha256(p.read_bytes()).hexdigest();(r/'data/sources.json').write_text(json.dumps([source]));(r/'data/literature_claim_reviews.json').write_text(json.dumps(dict(sources={'S':v},claims=[])));(r/'source.docx').unlink();self.assertEqual(load_registry(r)['sources']['S']['source_asset_kind'],'repository_docx')
if __name__=='__main__':unittest.main()
