"""Reject stale citations and unsupported promotion of literature evidence."""
import copy,hashlib,json,tempfile,unittest
from pathlib import Path
from literature_review import ROOT,digest,load_registry,empirical_note,target_value

class ScopedLiteratureEvidence(unittest.TestCase):
 def fixture(self,root):
  import hashlib
  (root/'data/literature_evidence').mkdir(parents=True)
  (root/'data/literature_evidence/paper.pdf').write_bytes(b'%PDF-test-source')
  source=dict(id='S',title='Test source');target=dict(id='R',rationale='Task-specific claim')
  registry=dict(sources={'S':dict(source_id='S',bibliography_snapshot=digest(source),reviewer='R',date='2026-11-04',read_scope='p1',limits='Scope-specific',snapshot_file='data/literature_evidence/paper.pdf',snapshot_sha256=hashlib.sha256(b'%PDF-test-source').hexdigest(),independent_review=False,student_validated=False)},claims=[dict(id='C',source_id='S',role='related_theoretical_context',locations=['p1'],support='Context',does_not_establish='Student validation',standard_codes=['6수01-10'],target_snapshots={'relation:R':digest(target)},independent_review=False,student_validated=False)])
  for name,value in [('sources',[source]),('relations',dict(relations=[target])),('literature_claim_reviews',registry)]:
   (root/f'data/{name}.json').write_text(json.dumps(value),encoding='utf-8')
  return registry,target,source
 def test_current_evidence_and_every_scoped_note_reaches_its_document(self):
  data=load_registry()
  for source in data['sources'].values():
   for probe in source.get('observations',[]):
    self.assertFalse(probe['student_validated'])
    for code in probe['standard_codes']:
     text=(ROOT/f'analyses/{code}.md').read_text(encoding='utf-8')
     self.assertIn(probe['question'],text);self.assertIn(probe['expected'],text);self.assertIn(probe['interpretation'],text)
  for claim in data['claims']:
   for code in claim['standard_codes']:
    text=(ROOT/f'analyses/{code}.md').read_text(encoding='utf-8')
    self.assertIn(claim['id'],text);self.assertIn(claim['support'],text);self.assertIn(claim['does_not_establish'],text)
 def test_changed_claim_requires_re_review(self):
  with tempfile.TemporaryDirectory() as directory:
   root=Path(directory);_,target,_=self.fixture(root);load_registry(root)
   target['rationale']='Changed claim';(root/'data/relations.json').write_text(json.dumps(dict(relations=[target])),encoding='utf-8')
   with self.assertRaisesRegex(AssertionError,'target'):load_registry(root)
 def test_authored_revision_changes_require_re_review_and_ambiguous_targets_fail(self):
  with tempfile.TemporaryDirectory() as directory:
   root=Path(directory);registry,_,_=self.fixture(root)
   revision={'12미적Ⅰ-02-01':dict(conditions=['h≠0'],taskSolution='finite limit')}
   file=root/'data/revisions_high.json';file.write_text(json.dumps(revision),encoding='utf-8')
   target='revision:12미적Ⅰ-02-01'
   registry['claims'][0]['target_snapshots']={target:digest(target_value(target,root))}
   (root/'data/literature_claim_reviews.json').write_text(json.dumps(registry),encoding='utf-8');load_registry(root)
   revision['12미적Ⅰ-02-01']['conditions']=['h=0'];file.write_text(json.dumps(revision),encoding='utf-8')
   with self.assertRaisesRegex(AssertionError,'target'):load_registry(root)
   (root/'data/revisions_duplicate.json').write_text(json.dumps(revision),encoding='utf-8')
   with self.assertRaisesRegex(AssertionError,'one authored source'):target_value(target,root)
 def test_portal_payload_contains_every_claim_and_observation(self):
  data=load_registry();site=ROOT.parent if ROOT.name=='research' else ROOT/'tmp/pathways-release'
  catalog=json.loads((site/'dist/content/catalog.json').read_text(encoding='utf-8'))
  def text_for(code):
   record=json.loads((site/f'dist/content/standards/{code}.json').read_text(encoding='utf-8'))
   self.assertEqual(record['version'],catalog['version'])
   self.assertFalse(record['analysis']['validated'])
   return '\n'.join(section['body'] for section in record['analysis']['sections'])
  for claim in data['claims']:
   for code in claim['standard_codes']:
    text=text_for(code)
    for value in [claim['id'],claim['support'],claim['does_not_establish']]:self.assertIn(value,text)
  for source in data['sources'].values():
   for observation in source.get('observations',[]):
    for code in observation['standard_codes']:
     text=text_for(code)
     for field in ['question','expected','interpretation']:self.assertIn(observation[field],text)
 def test_changed_initial_case_body_requires_re_review(self):
  with tempfile.TemporaryDirectory() as directory:
   root=Path(directory);registry,_,_=self.fixture(root)
   initial={'6수02-03':'The reference quantity is nonzero.'}
   file=root/'data/initial_case_studies.json';file.write_text(json.dumps(initial),encoding='utf-8')
   target='initial:6수02-03'
   registry['claims'][0]['target_snapshots'][target]=digest(target_value(target,root))
   path=root/'data/literature_claim_reviews.json';path.write_text(json.dumps(registry),encoding='utf-8');load_registry(root)
   initial['6수02-03']='Changed reference quantity.';file.write_text(json.dumps(initial),encoding='utf-8')
   with self.assertRaisesRegex(AssertionError,'target'):load_registry(root)
 def test_changed_snapshot_is_rejected(self):
  with tempfile.TemporaryDirectory() as directory:
   root=Path(directory);self.fixture(root);(root/'data/literature_evidence/paper.pdf').write_bytes(b'changed')
   with self.assertRaisesRegex(AssertionError,'snapshot'):load_registry(root)
 def test_prior_scoped_notes_remain_bound_after_extension(self):
  import hashlib
  with tempfile.TemporaryDirectory() as directory:
   root=Path(directory);registry,_,_=self.fixture(root)
   prior=root/'data/literature_evidence/previous.json';prior.write_bytes(b'{"scope":"previous"}')
   registry['sources']['S']['snapshot_history']=[dict(snapshot_file='data/literature_evidence/previous.json',snapshot_sha256=hashlib.sha256(prior.read_bytes()).hexdigest(),date='2026-11-04',read_scope='Prior bounded reading')]
   (root/'data/literature_claim_reviews.json').write_text(json.dumps(registry),encoding='utf-8');load_registry(root)
   prior.write_bytes(b'changed')
   with self.assertRaisesRegex(AssertionError,'historical literature snapshot'):load_registry(root)
 def test_changed_bibliography_is_rejected(self):
  with tempfile.TemporaryDirectory() as directory:
   root=Path(directory);_,_,source=self.fixture(root);source['title']='Different paper';(root/'data/sources.json').write_text(json.dumps([source]),encoding='utf-8')
   with self.assertRaisesRegex(AssertionError,'bibliography'):load_registry(root)
 def test_licensed_pdf_extension_rejects_changed_notes_and_scope(self):
  import hashlib
  with tempfile.TemporaryDirectory() as directory:
   root=Path(directory);registry,_,_=self.fixture(root);source=registry['sources']['S']
   source.update(text_pdf_pages=[1],visual_pdf_pages=[1])
   notes=dict(source_id='S',source_pdf_sha256=source['snapshot_sha256'],cumulative_read_scope='p1',cumulative_text_pdf_pages=[1],cumulative_visual_pdf_pages=[1],contains_source_full_text=False,reading_log=['Observed page 1'])
   file=root/'data/literature_evidence/extension.json';file.write_text(json.dumps(notes),encoding='utf-8')
   source['reading_extension']=dict(file='data/literature_evidence/extension.json',sha256=hashlib.sha256(file.read_bytes()).hexdigest())
   path=root/'data/literature_claim_reviews.json';path.write_text(json.dumps(registry),encoding='utf-8');load_registry(root)
   notes['cumulative_read_scope']='all pages';file.write_text(json.dumps(notes),encoding='utf-8')
   with self.assertRaisesRegex(AssertionError,'reading extension'):load_registry(root)
   source['reading_extension']['sha256']=hashlib.sha256(file.read_bytes()).hexdigest();path.write_text(json.dumps(registry),encoding='utf-8')
   with self.assertRaisesRegex(AssertionError,'cumulative reading scope'):load_registry(root)
 def test_incomplete_source_cannot_gain_whole_book_status_or_unreviewed_scope(self):
  import hashlib
  for mutation in ['whole_book','scope','audit']:
   with self.subTest(mutation=mutation),tempfile.TemporaryDirectory() as directory:
    root=Path(directory);registry,_,_=self.fixture(root);source=registry['sources']['S']
    audit=root/'data/literature_evidence/audit.json';audit.write_bytes(b'{"incomplete":true}')
    integrity=dict(status='incomplete_repeated_segments',whole_book_obtained=False)
    notes=dict(source_id='S',source_url='https://example.org/book',source_pdf_sha256='a'*64,reading_log=['Selected p1'],source_corrections=[],contains_source_full_text=False,source_pdf_redistributed=False,source_integrity=copy.deepcopy(integrity),read_scope='p1',text_pdf_pages=[1],visual_pdf_pages=[1],asset_audit_file='data/literature_evidence/audit.json',asset_audit_sha256=hashlib.sha256(audit.read_bytes()).hexdigest())
    file=root/'data/literature_evidence/notes.json';file.write_text(json.dumps(notes),encoding='utf-8')
    source.update(snapshot_kind='authored_review_notes',snapshot_file='data/literature_evidence/notes.json',snapshot_sha256=hashlib.sha256(file.read_bytes()).hexdigest(),source_pdf_sha256='a'*64,redistribution_license='workspace_authored_notes',display=dict(url=notes['source_url']),source_integrity=copy.deepcopy(integrity),text_pdf_pages=[1],visual_pdf_pages=[1])
    path=root/'data/literature_claim_reviews.json';path.write_text(json.dumps(registry),encoding='utf-8');load_registry(root)
    if mutation=='whole_book':
     source['source_integrity']['whole_book_obtained']=True;notes['source_integrity']['whole_book_obtained']=True
     file.write_text(json.dumps(notes),encoding='utf-8');source['snapshot_sha256']=hashlib.sha256(file.read_bytes()).hexdigest()
    elif mutation=='scope':source['text_pdf_pages']=[1,2,3]
    else:audit.write_bytes(b'{"incomplete":false}')
    path.write_text(json.dumps(registry),encoding='utf-8')
    with self.assertRaises(AssertionError):load_registry(root)
 def test_literature_reading_cannot_be_student_or_independent_validation(self):
  for field in ['student_validated','independent_review']:
   with self.subTest(field=field),tempfile.TemporaryDirectory() as directory:
    root=Path(directory);registry,_,_=self.fixture(root);registry['claims'][0][field]=True;(root/'data/literature_claim_reviews.json').write_text(json.dumps(registry),encoding='utf-8')
    with self.assertRaises(AssertionError):load_registry(root)
 def test_authored_notes_bind_the_observed_source_without_redistributing_pdf(self):
  import hashlib
  with tempfile.TemporaryDirectory() as directory:
   root=Path(directory);registry,_,_=self.fixture(root)
   notes=dict(source_id='S',source_url='https://example.org/source.pdf',source_pdf_sha256='a'*64,reading_log=['p1 text and diagram checked'],source_corrections=[],contains_source_full_text=False,source_pdf_redistributed=False)
   file=root/'data/literature_evidence/notes.json';file.write_text(json.dumps(notes),encoding='utf-8')
   source=registry['sources']['S'];source.update(snapshot_kind='authored_review_notes',snapshot_file='data/literature_evidence/notes.json',snapshot_sha256=hashlib.sha256(file.read_bytes()).hexdigest(),source_pdf_sha256='a'*64,redistribution_license='workspace_authored_notes',display=dict(url=notes['source_url']))
   (root/'data/literature_claim_reviews.json').write_text(json.dumps(registry),encoding='utf-8');load_registry(root)
   source['source_pdf_sha256']='b'*64
   (root/'data/literature_claim_reviews.json').write_text(json.dumps(registry),encoding='utf-8')
   with self.assertRaises(AssertionError):load_registry(root)
 def test_empirical_claim_requires_a_study_scope(self):
  with tempfile.TemporaryDirectory() as directory:
   root=Path(directory);registry,_,_=self.fixture(root);registry['claims'][0]['role']='empirical_result_with_scope'
   (root/'data/literature_claim_reviews.json').write_text(json.dumps(registry),encoding='utf-8')
   with self.assertRaises(KeyError):load_registry(root)
 def test_cross_sectional_comparison_cannot_be_promoted_to_causal_longitudinal_or_local(self):
  for field in ['causal_effect_established','longitudinal_cohort','local_effect_tested']:
   with self.subTest(field=field),tempfile.TemporaryDirectory() as directory:
    root=Path(directory);registry,_,_=self.fixture(root)
    scope=dict(design='cross_sectional_with_selected_interviews',sample_description='Different groups at three grades',inference_limit='Not a treatment or longitudinal comparison',local_effect_tested=False,causal_effect_established=False,longitudinal_cohort=False)
    registry['claims'][0].update(role='empirical_result_with_scope',empirical_scope=scope)
    file=root/'data/literature_claim_reviews.json';file.write_text(json.dumps(registry),encoding='utf-8');load_registry(root)
    scope[field]=True;file.write_text(json.dumps(registry),encoding='utf-8')
    with self.assertRaises(AssertionError):load_registry(root)
 def test_actual_empirical_comparison_scope_reaches_docs_and_portal(self):
  registry=load_registry();claims=[c for c in registry['claims'] if c['role']=='empirical_result_with_scope']
  self.assertTrue({'KB02','KB03','KB04','KB05','PL01','PL02','PL03'}<={c['id'] for c in claims})
  site=ROOT.parent if ROOT.name=='research' else ROOT/'tmp/pathways-release'
  for claim in claims:
   note=empirical_note(claim);self.assertTrue(note)
   for code in claim['standard_codes']:
    self.assertIn(note,(ROOT/f'analyses/{code}.md').read_text(encoding='utf-8'))
    record=json.loads((site/f'dist/content/standards/{code}.json').read_text(encoding='utf-8'))
    self.assertIn(note,'\n'.join(s['body'] for s in record['analysis']['sections']))
 def test_textbook_analysis_cannot_be_a_student_outcome_or_causal_study(self):
  for field in ['student_outcome_study','causal_effect_established']:
   with self.subTest(field=field),tempfile.TemporaryDirectory() as directory:
    root=Path(directory);registry,_,_=self.fixture(root)
    scope=dict(design='comparative_textbook_content_analysis',sample_description='Selected historical textbook series',inference_limit='Not a pupil sample or current national census',student_outcome_study=False,causal_effect_established=False,local_effect_tested=False)
    registry['claims'][0].update(role='empirical_result_with_scope',empirical_scope=scope)
    file=root/'data/literature_claim_reviews.json';file.write_text(json.dumps(registry),encoding='utf-8');load_registry(root)
    scope[field]=True;file.write_text(json.dumps(registry),encoding='utf-8')
    with self.assertRaises(AssertionError):load_registry(root)
 def test_publisher_html_reading_is_bound_without_claiming_a_pdf_reading(self):
  import hashlib
  for mutation in ['html_hash','fake_pdf','format','pdf_read']:
   with self.subTest(mutation=mutation),tempfile.TemporaryDirectory() as directory:
    root=Path(directory);registry,_,_=self.fixture(root)
    notes=dict(source_id='S',source_url='https://example.org/chapter',source_asset_kind='publisher_html',source_asset_sha256='a'*64,source_asset_redistributed=False,reading_log=['Official chapter and embedded figures read'],source_corrections=[],contains_source_full_text=False,source_pdf_redistributed=False,pdf_read=False,original_page_layout_review=False)
    file=root/'data/literature_evidence/notes.json';file.write_text(json.dumps(notes),encoding='utf-8')
    source=registry['sources']['S'];source.update(snapshot_kind='authored_review_notes',snapshot_file='data/literature_evidence/notes.json',snapshot_sha256=hashlib.sha256(file.read_bytes()).hexdigest(),source_asset_kind='publisher_html',source_asset_sha256='a'*64,redistribution_license='workspace_authored_notes',display=dict(url=notes['source_url']))
    path=root/'data/literature_claim_reviews.json';path.write_text(json.dumps(registry),encoding='utf-8');load_registry(root)
    if mutation=='html_hash':source['source_asset_sha256']='b'*64
    elif mutation=='fake_pdf':source['source_pdf_sha256']='a'*64
    elif mutation=='format':source['source_asset_kind']='not_a_supported_format'
    else:
     notes['pdf_read']=True;file.write_text(json.dumps(notes),encoding='utf-8');source['snapshot_sha256']=hashlib.sha256(file.read_bytes()).hexdigest()
    path.write_text(json.dumps(registry),encoding='utf-8')
    with self.assertRaises(AssertionError):load_registry(root)
 def test_repository_xml_binds_selected_elements_without_pdf_claims(self):
  for mutation in ['asset_hash','selection','duplicate','element_hash','provenance','fake_pdf','layout']:
   with self.subTest(mutation=mutation),tempfile.TemporaryDirectory() as directory:
    root=Path(directory);registry,_,_=self.fixture(root)
    scope=dict(url='https://example.org/repository/article.xml',repository='Public repository',article_identifier='A1',
               publication_doi='10.1234/test',binary_obtained=True,content_type='application/xml',
               selected_elements=[dict(id='methods',sha256='b'*64)])
    notes=dict(source_id='S',source_url='https://example.org/article',source_asset_kind='repository_xml',
               source_asset_sha256='a'*64,source_asset_redistributed=False,read_scope='p1',
               repository_xml_review=copy.deepcopy(scope),pdf_read=False,original_page_layout_review=False,
               contains_source_full_text=False,source_pdf_redistributed=False,reading_log=['Methods section'],source_corrections=[])
    file=root/'data/literature_evidence/notes.json'
    file.write_text(json.dumps(notes),encoding='utf-8')
    source=registry['sources']['S']
    source.update(snapshot_kind='authored_review_notes',snapshot_file='data/literature_evidence/notes.json',
       snapshot_sha256=hashlib.sha256(file.read_bytes()).hexdigest(),source_asset_kind='repository_xml',
       source_asset_sha256='a'*64,repository_xml_review=copy.deepcopy(scope),redistribution_license='workspace_authored_notes',
       display=dict(url=notes['source_url']))
    path=root/'data/literature_claim_reviews.json'
    path.write_text(json.dumps(registry),encoding='utf-8');load_registry(root)
    if mutation=='asset_hash':source['source_asset_sha256']='c'*64
    elif mutation=='selection':source['repository_xml_review']['selected_elements'][0]['id']='unread-section'
    elif mutation=='fake_pdf':source['source_pdf_sha256']='a'*64
    elif mutation=='layout':notes['original_page_layout_review']=True
    else:
     for record in [notes,source]:
      selected=record['repository_xml_review']['selected_elements']
      if mutation=='duplicate':selected.append(copy.deepcopy(selected[0]))
      elif mutation=='element_hash':selected[0]['sha256']='not-a-hash'
      else:record['repository_xml_review']['url']=''
    file.write_text(json.dumps(notes),encoding='utf-8');source['snapshot_sha256']=hashlib.sha256(file.read_bytes()).hexdigest()
    path.write_text(json.dumps(registry),encoding='utf-8')
    with self.assertRaises(AssertionError):load_registry(root)

 def test_author_web_text_does_not_claim_article_pdf_access(self):
  with tempfile.TemporaryDirectory() as directory:
   root=Path(directory);registry,_,_=self.fixture(root)
   scope=dict(url='https://example.org/author-copy',uploaded_by='Author',article_pdf_obtained=False,
              article_printed_pages=[10,20],selected_sections=[dict(section='Method',printed_pages=[11,12])])
   notes=dict(source_id='S',source_url='https://example.org/article',source_asset_kind='author_web_text',
              author_text_review=scope,read_scope='Method excerpt',original_page_layout_review=False,
              contains_source_full_text=False,source_pdf_redistributed=False,reading_log=['Author transcript'],source_corrections=[])
   file=root/'data/literature_evidence/notes.json';path=root/'data/literature_claim_reviews.json'
   source=registry['sources']['S'];source.update(snapshot_kind='authored_review_notes',snapshot_file='data/literature_evidence/notes.json',
       source_asset_kind='author_web_text',author_text_review=scope,read_scope=notes['read_scope'],
       redistribution_license='workspace_authored_notes',display=dict(url=notes['source_url']))
   def save():
    file.write_text(json.dumps(notes),encoding='utf-8');source['snapshot_sha256']=hashlib.sha256(file.read_bytes()).hexdigest()
    path.write_text(json.dumps(registry),encoding='utf-8')
   save();load_registry(root)
   scope['article_pdf_obtained']=True;save()
   with self.assertRaises(AssertionError):load_registry(root)
   scope['article_pdf_obtained']=False;scope['selected_sections'][0]['printed_pages']=[11,21];save()
   with self.assertRaises(AssertionError):load_registry(root)
 def test_extended_html_manifest_rejects_changed_scope_assets_and_duplicate_urls(self):
  import hashlib
  for mutation in ['asset','scope','duplicate_url']:
   with self.subTest(mutation=mutation),tempfile.TemporaryDirectory() as directory:
    root=Path(directory);registry,_,_=self.fixture(root)
    manifest=[dict(key='page1',url='https://example.org/chapter1',status=200,sha256='b'*64)]
    notes=dict(source_id='S',source_url='https://example.org/',source_asset_kind='publisher_html',source_asset_sha256='a'*64,source_asset_redistributed=False,reading_log=['Selected public English chapter'],source_corrections=[],contains_source_full_text=False,source_pdf_redistributed=False,pdf_read=False,original_page_layout_review=False,read_scope='One selected chapter',html_read_manifest=copy.deepcopy(manifest))
    file=root/'data/literature_evidence/notes.json';file.write_text(json.dumps(notes),encoding='utf-8')
    source=registry['sources']['S'];source.update(snapshot_kind='authored_review_notes',snapshot_file='data/literature_evidence/notes.json',snapshot_sha256=hashlib.sha256(file.read_bytes()).hexdigest(),source_asset_kind='publisher_html',source_asset_sha256='a'*64,redistribution_license='workspace_authored_notes',display=dict(url=notes['source_url']),read_scope=notes['read_scope'],html_read_manifest=copy.deepcopy(manifest))
    path=root/'data/literature_claim_reviews.json';path.write_text(json.dumps(registry),encoding='utf-8');load_registry(root)
    if mutation=='asset':source['html_read_manifest'][0]['sha256']='c'*64
    elif mutation=='scope':source['read_scope']='All chapters read'
    else:
     extra={**manifest[0],'key':'page2'};source['html_read_manifest'].append(extra);notes['html_read_manifest'].append(extra)
     file.write_text(json.dumps(notes),encoding='utf-8');source['snapshot_sha256']=hashlib.sha256(file.read_bytes()).hexdigest()
    path.write_text(json.dumps(registry),encoding='utf-8')
    with self.assertRaises(AssertionError):load_registry(root)
 def test_inline_image_review_rejects_changed_hash_duplicate_and_unread_page(self):
  import hashlib
  for mutation in ['hash','duplicate','unread_page','redistributed','dimension']:
   with self.subTest(mutation=mutation),tempfile.TemporaryDirectory() as directory:
    root=Path(directory);registry,_,_=self.fixture(root)
    html=[dict(key='page',url='https://example.org/chapter',status=200,sha256='b'*64)]
    images=[dict(page_url=html[0]['url'],url='https://example.org/figure.png',status=200,sha256='c'*64,dimensions=[220,95],content_type='image/png',read_kind='inline_image_visual_review',redistributed=False)]
    notes=dict(source_id='S',source_url='https://example.org/',source_asset_kind='publisher_html',source_asset_sha256='a'*64,source_asset_redistributed=False,reading_log=['Selected chapter and inline figure'],source_corrections=[],contains_source_full_text=False,source_pdf_redistributed=False,pdf_read=False,original_page_layout_review=False,read_scope='One chapter and one inline image',html_read_manifest=copy.deepcopy(html),image_read_manifest=copy.deepcopy(images))
    file=root/'data/literature_evidence/notes.json';file.write_text(json.dumps(notes),encoding='utf-8')
    source=registry['sources']['S'];source.update(snapshot_kind='authored_review_notes',snapshot_file='data/literature_evidence/notes.json',snapshot_sha256=hashlib.sha256(file.read_bytes()).hexdigest(),source_asset_kind='publisher_html',source_asset_sha256='a'*64,redistribution_license='workspace_authored_notes',display=dict(url=notes['source_url']),read_scope=notes['read_scope'],html_read_manifest=html,image_read_manifest=images)
    path=root/'data/literature_claim_reviews.json';path.write_text(json.dumps(registry),encoding='utf-8');load_registry(root)
    if mutation=='hash':images[0]['sha256']='d'*64
    else:
     if mutation=='duplicate':images.append(copy.deepcopy(images[0]))
     elif mutation=='unread_page':images[0]['page_url']='https://example.org/unread'
     elif mutation=='redistributed':images[0]['redistributed']=True
     else:images[0]['dimensions'][0]=0
     notes['image_read_manifest']=copy.deepcopy(images);file.write_text(json.dumps(notes),encoding='utf-8');source['snapshot_sha256']=hashlib.sha256(file.read_bytes()).hexdigest()
    path.write_text(json.dumps(registry),encoding='utf-8')
    with self.assertRaises(AssertionError):load_registry(root)
 def test_linked_pdf_review_cannot_expand_pages_links_or_redistribution_without_evidence(self):
  import hashlib
  for mutation in ['manifest','missing_manifest','unread_link','duplicate_url','duplicate_page','outside_page','unread_visual','render','hash','redistributed','primary_pdf']:
   with self.subTest(mutation=mutation),tempfile.TemporaryDirectory() as directory:
    root=Path(directory);registry,_,_=self.fixture(root)
    html=[dict(key='page',url='https://example.org/activity',status=200,sha256='b'*64)]
    pdf=[dict(url='https://example.org/worksheet.pdf',linked_page_urls=[html[0]['url']],status=200,content_type='application/pdf',sha256='c'*64,read_kind='linked_pdf_content_and_visual_review',redistributed=False,pdf_pages=2,content_pdf_pages=[1],visual_pdf_pages=[1],rendered_pages=[dict(pdf_page=1,sha256='d'*64)])]
    notes=dict(source_id='S',source_url='https://example.org/',source_asset_kind='publisher_html',source_asset_sha256='a'*64,source_asset_redistributed=False,reading_log=['Activity and first worksheet page read'],source_corrections=[],contains_source_full_text=False,source_pdf_redistributed=False,pdf_read=True,primary_asset_is_pdf=False,original_page_layout_review=False,read_scope='HTML and linked PDF page 1 only',html_read_manifest=copy.deepcopy(html),supplementary_pdf_read_manifest=copy.deepcopy(pdf))
    file=root/'data/literature_evidence/notes.json';source=registry['sources']['S']
    source.update(snapshot_kind='authored_review_notes',snapshot_file='data/literature_evidence/notes.json',source_asset_kind='publisher_html',source_asset_sha256='a'*64,redistribution_license='workspace_authored_notes',display=dict(url=notes['source_url']),read_scope=notes['read_scope'],html_read_manifest=html,supplementary_pdf_read_manifest=pdf)
    path=root/'data/literature_claim_reviews.json'
    def save():
     file.write_text(json.dumps(notes),encoding='utf-8');source['snapshot_sha256']=hashlib.sha256(file.read_bytes()).hexdigest();path.write_text(json.dumps(registry),encoding='utf-8')
    save();load_registry(root)
    if mutation=='manifest':pdf[0]['sha256']='e'*64
    elif mutation=='missing_manifest':source.pop('supplementary_pdf_read_manifest');notes.pop('supplementary_pdf_read_manifest')
    else:
     if mutation=='unread_link':pdf[0]['linked_page_urls']=['https://example.org/unread']
     elif mutation=='duplicate_url':pdf.append(copy.deepcopy(pdf[0]))
     elif mutation=='duplicate_page':pdf[0]['content_pdf_pages']=[1,1]
     elif mutation=='outside_page':pdf[0]['content_pdf_pages']=[1,3]
     elif mutation=='unread_visual':pdf[0]['visual_pdf_pages']=[2]
     elif mutation=='render':pdf[0]['rendered_pages'][0]['pdf_page']=2
     elif mutation=='hash':pdf[0]['sha256']='not-a-hash'
     elif mutation=='redistributed':pdf[0]['redistributed']=True
     elif mutation=='primary_pdf':notes['primary_asset_is_pdf']=True
     notes['supplementary_pdf_read_manifest']=copy.deepcopy(pdf)
    save()
    with self.assertRaises(AssertionError):load_registry(root)
 def test_web_pdf_text_scope_cannot_claim_binary_visual_or_unlocated_pages(self):
  with tempfile.TemporaryDirectory() as directory:
   root=Path(directory);registry,_,_=self.fixture(root)
   scope=dict(reported_pdf_pages=2,text_pdf_pages=[1],visual_pdf_pages=[],binary_obtained=False,
              page_text_line_ranges=[[0,2]],text_line_count=3)
   notes=dict(source_id='S',source_url='https://example.org/paper.pdf',source_asset_kind='web_pdf_text',
              read_scope='p1',pdf_text_review=scope,original_page_layout_review=False,
              reading_log=['Text p1'],source_corrections=[],contains_source_full_text=False,source_pdf_redistributed=False)
   file=root/'data/literature_evidence/notes.json';source=registry['sources']['S']
   source.update(snapshot_kind='authored_review_notes',snapshot_file='data/literature_evidence/notes.json',
                 source_asset_kind='web_pdf_text',pdf_text_review=scope,
                 redistribution_license='workspace_authored_notes',display=dict(url=notes['source_url']))
   def save():
    file.write_text(json.dumps(notes),encoding='utf-8')
    source['snapshot_sha256']=hashlib.sha256(file.read_bytes()).hexdigest()
    (root/'data/literature_claim_reviews.json').write_text(json.dumps(registry),encoding='utf-8')
   save();load_registry(root)
   for key,value in [('binary_obtained',True),('visual_pdf_pages',[1]),('text_pdf_pages',[1,2])]:
    with self.subTest(key=key):
     original=scope[key];scope[key]=value;save()
     with self.assertRaises(AssertionError):load_registry(root)
     scope[key]=original
if __name__=='__main__':unittest.main()
