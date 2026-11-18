"""Bind a repository DOCX reading without claiming rendered PDF page fidelity."""
from pathlib import PurePosixPath
from zipfile import ZipFile
from xml.etree import ElementTree as ET
from io import BytesIO
from PIL import Image
import hashlib,re,posixpath

W='http://schemas.openxmlformats.org/wordprocessingml/2006/main'
R='http://schemas.openxmlformats.org/officeDocument/2006/relationships'
C='http://schemas.openxmlformats.org/drawingml/2006/chart'
A='http://schemas.openxmlformats.org/drawingml/2006/main'
sha=lambda b:hashlib.sha256(b).hexdigest()

def body_blocks(raw):
 root=ET.fromstring(raw);body=root.find(f'{{{W}}}body');assert body is not None
 return [dict(index=i,kind=e.tag.rsplit('}',1)[-1],text=' '.join(t.text or '' for t in e.iter() if t.tag.rsplit('}',1)[-1]=='t')) for i,e in enumerate(body,1)]

def inspect_docx_source(spec,cache):
 p=(cache/spec['file']).resolve();assert p.is_relative_to(cache.resolve())
 raw=p.read_bytes();assert sha(raw)==spec['sha256']
 with ZipFile(BytesIO(raw)) as z:
  names=z.namelist();assert len(set(names))==len(names)
  assert all(not PurePosixPath(n).is_absolute() and '..' not in PurePosixPath(n).parts for n in names)
  assert sum(i.file_size for i in z.infolist())<64*1024*1024
  document=z.read('word/document.xml');root=ET.fromstring(document);blocks=body_blocks(document)
  rels=ET.fromstring(z.read('word/_rels/document.xml.rels'))
  targets={e.attrib['Id']:posixpath.normpath(posixpath.join('word',e.attrib['Target'])) for e in rels if e.attrib.get('TargetMode')!='External'}
  used_charts={targets[e.attrib[f'{{{R}}}id']] for e in root.findall(f'.//{{{C}}}chart')}
  used_images={targets[e.attrib[f'{{{R}}}embed']] for e in root.findall(f'.//{{{A}}}blip') if f'{{{R}}}embed' in e.attrib}
  assert set(spec['chart_parts'])<=used_charts and set(spec['image_parts'])<=used_images,'Unlinked DOCX chart or image'
  selected=[]
  for i in spec['block_ids']:
   b=blocks[i-1];assert b['index']==i
   selected.append(dict(index=i,kind=b['kind'],text_sha256=sha(b['text'].encode('utf-8'))))
  charts=[]
  for part in spec['chart_parts']:
   chart=ET.fromstring(z.read(part));assert chart.tag==f'{{{C}}}chartSpace'
   charts.append(dict(part=part,sha256=sha(z.read(part)),read_kind='native_chart_xml_and_cached_values',visual_layout_verified=False))
  images=[]
  for part in spec['image_parts']:
   data=z.read(part)
   with Image.open(BytesIO(data)) as im:dimensions=list(im.size)
   images.append(dict(part=part,sha256=sha(data),dimensions=dimensions,read_kind='embedded_image_visual_review',redistributed=False))
  other=[dict(part=n,sha256=sha(z.read(n))) for n in spec['other_text_parts']]
  all_parts=[dict(part=n,sha256=sha(z.read(n))) for n in sorted(names)]
 return dict(url=spec['docx_url'],record_url=spec['repository_record_url'],binary_obtained=True,content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document',package_sha256=spec['sha256'],package_parts=all_parts,body_block_count=len(blocks),selected_body_blocks=selected,all_body_blocks_read=spec['block_ids']==list(range(1,len(blocks)+1)),other_text_parts=other,chart_parts=charts,embedded_images=images,document_page_layout_verified=False,published_pdf_obtained=False,field_instructions_not_body_text=True)

def validate_docx_review(review,notes):
 assert notes['source_asset_kind']==review['source_asset_kind']=='repository_docx'
 assert notes['read_scope']==review['read_scope']
 assert notes['source_asset_sha256']==review['source_asset_sha256'] and re.fullmatch('[0-9a-f]{64}',review['source_asset_sha256'])
 assert all('source_pdf_sha256' not in x for x in [review,notes]),'A DOCX reading is not a PDF reading'
 assert notes['pdf_read'] is False and notes['original_page_layout_review'] is False and notes['source_asset_redistributed'] is False
 m=notes['repository_docx_review'];assert m==review['repository_docx_review'],'Changed DOCX reading scope requires review'
 assert m['url'].startswith('https://') and m['record_url'].startswith('https://') and m['binary_obtained'] is True
 assert m['content_type']=='application/vnd.openxmlformats-officedocument.wordprocessingml.document' and m['package_sha256']==review['source_asset_sha256']
 assert m['document_page_layout_verified'] is False and m['published_pdf_obtained'] is False
 parts=m['package_parts'];assert parts and len({p['part'] for p in parts})==len(parts)
 assert all(p['part'] and '..' not in PurePosixPath(p['part']).parts and not PurePosixPath(p['part']).is_absolute() and re.fullmatch('[0-9a-f]{64}',p['sha256']) for p in parts)
 hashes={p['part']:p['sha256'] for p in parts};assert 'word/document.xml' in hashes and 'word/_rels/document.xml.rels' in hashes
 blocks=m['selected_body_blocks'];indices=[p['index'] for p in blocks];assert blocks and indices==sorted(set(indices)) and all(type(i) is int and 1<=i<=m['body_block_count'] for i in indices)
 assert all(p['kind'] and re.fullmatch('[0-9a-f]{64}',p['text_sha256']) for p in blocks)
 if m['all_body_blocks_read']:assert indices==list(range(1,m['body_block_count']+1))
 for key in ['chart_parts','embedded_images','other_text_parts']:
  assert len({p['part'] for p in m[key]})==len(m[key])
  assert all(hashes.get(p['part'])==p['sha256'] for p in m[key]),'DOCX part hash mismatch'
 for p in m['chart_parts']:assert p['read_kind']=='native_chart_xml_and_cached_values' and p['visual_layout_verified'] is False
 for p in m['embedded_images']:assert p['read_kind']=='embedded_image_visual_review' and len(p['dimensions'])==2 and all(type(d) is int and d>0 for d in p['dimensions']) and p['redistributed'] is False
