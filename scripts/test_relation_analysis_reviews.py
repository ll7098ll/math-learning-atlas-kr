"""Guard evidence changes and verify that scoped mathematics reaches the actual corpus."""
import copy,json,tempfile,unittest
from pathlib import Path
from relation_analysis_review import ROOT,FILE,digest,source_value,load_reviews,apply_review
from relation_literature_review import FILE as LITERATURE_FILE, apply_literature_context, claim_snapshot, relation_snapshot

class FixtureGuards(unittest.TestCase):
 def fixture(self,root,revision_link=False):
  (root/'data/teaching_examples').mkdir(parents=True)
  a,b='2수01-01','9수01-04'
  raw=dict(id='R',from_='standard:'+a,to='standard:'+b,type='generalizes',rationale='Original claim');raw['from']=raw.pop('from_')
  standards=[dict(code=c,statement_display='Official scope '+c,school_level='school',subject='math',domain='numbers') for c in [a,b]]
  revisions={c:dict(mathematicalMeaning='meaning',taskSolution='solution',conditions=['defined']) for c in [a,b]}
  if revision_link:
   raw['id']='REV-'+a+'-1'
   revisions[a]['internalRelations']=[dict(target=b,kind='meaning_connection',reviewState='candidate',rationale='Authored candidate',conditions=['defined'])]
  corpus=dict(entries=[dict(code=c,goals=[dict(id=c+':goal',case_ids=[c+':task'])]) for c in [a,b]],cases=[dict(id=c+':task',task='case '+c,resources=[dict(path='examples/fixture.csv')]) for c in [a,b]])
  for path,value in [('data/relations.json',dict(relations=[] if revision_link else [raw])),('data/standards.json',dict(standards=standards)),('data/revisions_fixture.json',revisions),('data/goal_hierarchy_fixture.json',corpus),('data/initial_case_studies.json',{a:'Original detailed case'})]:
   (root/path).write_text(json.dumps(value),encoding='utf-8')
  (root/'data/teaching_examples/fixture.csv').write_text('value\n1\n',encoding='utf-8')
  review=dict(relation_id=raw['id'],state='self_checked_scope_math',reviewer='Author',date='2026-11-05',from_=raw['from'],to=raw['to'],type='meaning_connection',scope='Representative tasks only',rationale='Analogy has a boundary',conditions=['same quantity'],diagnostic='Compare a pair',expected_response='Explain the boundary',limit='Not an empirical prerequisite',additional_learning=['new representation'],mathematical_check='An exact counterexample',type_decision_reason='Analogy is not a directed extension',source_snapshot=digest(source_value(raw['id'],root)),independent_review=False,student_validated=False);review['from']=review.pop('from_')
  registry=dict(schema_version=1,records={raw['id']:review});(root/FILE).write_text(json.dumps(registry),encoding='utf-8')
  load_reviews(root);return registry,raw

 def test_generated_candidate_binds_authored_link_not_previous_output(self):
  for mutation in ['rationale','conditions','reorder','delete']:
   with self.subTest(mutation=mutation),tempfile.TemporaryDirectory() as directory:
    root=Path(directory);registry,raw=self.fixture(root,revision_link=True)
    value=source_value(raw['id'],root)['original_relation']
    self.assertEqual(value['authored_from'],'data/revisions_fixture.json')
    self.assertEqual(value['authored_link_index'],0);self.assertEqual(value['type'],'meaning_connection')
    p=root/'data/revisions_fixture.json';data=json.loads(p.read_text(encoding='utf-8'));links=data['2수01-01']['internalRelations']
    if mutation=='rationale':links[0]['rationale']='Different claim'
    elif mutation=='conditions':links[0]['conditions']=['Different scope']
    elif mutation=='reorder':links.insert(0,{**links[0],'rationale':'Different first identity'})
    else:links.clear()
    p.write_text(json.dumps(data),encoding='utf-8')
    with self.assertRaises(AssertionError):load_reviews(root)

 def test_source_relation_change_requires_explicit_re_review(self):
  with tempfile.TemporaryDirectory() as directory:
   root=Path(directory);_,raw=self.fixture(root);raw['rationale']='Changed source'
   (root/'data/relations.json').write_text(json.dumps(dict(relations=[raw])),encoding='utf-8')
   with self.assertRaisesRegex(AssertionError,'explicit re-review'):load_reviews(root)

 def test_endpoint_revision_task_goal_and_resource_changes_require_re_review(self):
  for mutation in ['official','revision','task','goal','resource']:
   with self.subTest(mutation=mutation),tempfile.TemporaryDirectory() as directory:
    root=Path(directory);self.fixture(root)
    if mutation=='resource':(root/'data/teaching_examples/fixture.csv').write_text('value\n2\n',encoding='utf-8')
    else:
     path=root/({'official':'data/standards.json','revision':'data/revisions_fixture.json'}.get(mutation,'data/goal_hierarchy_fixture.json'))
     data=json.loads(path.read_text(encoding='utf-8'))
     if mutation=='official':data['standards'][0]['statement_display']='Different range'
     elif mutation=='revision':data['2수01-01']['conditions']=['Changed domain']
     elif mutation=='task':data['cases'][0]['task']='Changed quantities'
     else:data['entries'][0]['goals'][0]['success']='Changed success'
     path.write_text(json.dumps(data),encoding='utf-8')
    with self.assertRaisesRegex(AssertionError,'explicit re-review'):load_reviews(root)

 def test_self_check_cannot_become_external_or_student_evidence(self):
  for key in ['independent_review','student_validated']:
   with self.subTest(key=key),tempfile.TemporaryDirectory() as directory:
    root=Path(directory);registry,_=self.fixture(root);registry['records']['R'][key]=True
    (root/FILE).write_text(json.dumps(registry),encoding='utf-8')
    with self.assertRaises(AssertionError):load_reviews(root)

 def test_initial_detailed_case_change_requires_explicit_re_review(self):
  with tempfile.TemporaryDirectory() as directory:
   root=Path(directory);self.fixture(root)
   (root/'data/initial_case_studies.json').write_text(json.dumps({'2수01-01':'Changed original quantities and units'}),encoding='utf-8')
   with self.assertRaisesRegex(AssertionError,'explicit re-review'):load_reviews(root)

 def test_type_decision_and_mathematical_witness_are_required(self):
  for key in ['type_decision_reason','mathematical_check','conditions','expected_response']:
   with self.subTest(key=key),tempfile.TemporaryDirectory() as directory:
    root=Path(directory);registry,_=self.fixture(root);registry['records']['R'][key]=''
    (root/FILE).write_text(json.dumps(registry),encoding='utf-8')
    with self.assertRaises(AssertionError):load_reviews(root)

 def test_apply_preserves_identity_original_evidence_and_separate_hierarchy_state(self):
  with tempfile.TemporaryDirectory() as directory:
   root=Path(directory);registry,raw=self.fixture(root)
   original=copy.deepcopy(raw);original.update(review_state='legacy_draft',hierarchy_review='independently_reviewed',independent_review=True,student_validated=True,review_history=[dict(reviewer='External',scope='Earlier task',date='2026-11-04')])
   before=copy.deepcopy(original);result=apply_review(original,registry['records']['R'])
   self.assertEqual(original,before);self.assertEqual(result['id'],original['id'])
   self.assertEqual(result['type'],'meaning_connection');self.assertEqual(result['review_state'],'self_checked')
   self.assertEqual(result['hierarchy_review'],'independently_reviewed');self.assertTrue(result['independent_review']);self.assertTrue(result['student_validated'])
   self.assertFalse(result['analysis_review_evidence']['independent_review'])
   self.assertEqual(result['review_history'],original['review_history'])
   self.assertEqual(result['analysis_review_history'][-1]['previous_derived_fields']['type'],'generalizes')

 def test_literature_context_preserves_relation_and_rejects_stale_evidence(self):
  with tempfile.TemporaryDirectory() as directory:
   root=Path(directory);_,original=self.fixture(root)
   claim=dict(id='L',source_id='S',standard_codes=[original['from'][9:],original['to'][9:]],locations=['https://example.test/article#page=4'])
   source=dict(snapshot_sha256='source-hash',bibliography_snapshot='bibliography-hash',display=dict(title='Article',url='https://example.test/article'))
   literature=dict(claims=[claim],sources={'S':source})
   row=dict(relation_id='R',claim_id='L',role='inference_limit',finding='Limited comparison',limit='Specific task only',
            relation_snapshot=relation_snapshot(original),claim_snapshot=claim_snapshot(claim,source))
   (root/LITERATURE_FILE).write_text(json.dumps(dict(schema_version=1,reviewer='Author',date='2026-11-09',records=[row])),encoding='utf-8')
   enriched=copy.deepcopy(original)
   apply_literature_context([enriched],literature,root)
   self.assertEqual(enriched.pop('literature_context')[0]['url'],claim['locations'][0])
   self.assertEqual(enriched,original)
   with self.assertRaisesRegex(AssertionError,'Relation changed'):apply_literature_context([{**original,'rationale':'New relation'}],literature,root)
   source['snapshot_sha256']='new source'
   with self.assertRaisesRegex(AssertionError,'Literature changed'):apply_literature_context([original],literature,root)

class DeliveredReviews(unittest.TestCase):
 def test_basic_reciprocal_does_not_import_common_course_translation(self):
  read=lambda p:json.loads(p.read_text(encoding='utf-8'))
  e=read(ROOT/'data/basic_reciprocal_scope_correction.json');code=e['code']
  self.assertEqual(read(ROOT/'data/revisions_high.json')[code]['mathematicalMeaning'],e['corrected_meaning'])
  entries={v['code']:v for v in read(ROOT/'data/secondary_analysis_details.json')['analyses']}
  entry=entries[code]
  self.assertEqual(entry['prior'][0][1],e['corrected_prior'])
  for key,value in e['secondary_copy_followup']['current'].items():self.assertEqual(entry[key],value)
  self.assertEqual(entries['10공수2-03-04']['prior'][0][1],e['original_prior'])
  site=ROOT.parent if ROOT.name=='research' else ROOT/'tmp/pathways-release'
  document=(ROOT/f'analyses/{code}.md').read_text(encoding='utf-8')
  detail=read(site/f'dist/content/standards/{code}.json');payload='\n'.join(s['body'] for s in detail['analysis']['sections'])
  for content in [document,payload]:
   self.assertIn(e['corrected_meaning'],content)
   self.assertNotIn(e['original_meaning'],content)
   self.assertNotIn(e['original_prior'],content)
  for path in [ROOT/'data/revised_relations.json',site/'dist/content/connections.json']:
   row=next(r for r in read(path)['relations'] if r['id']=='SEC_10기수2-03-04_C03')
   self.assertNotIn(e['original_prior'],row['rationale']);self.assertNotIn(e['original_prior'],row.get('expected_response',''))

 def test_product_integral_does_not_force_integration_by_parts(self):
  read=lambda p:json.loads(p.read_text(encoding='utf-8'))
  e=read(ROOT/'data/integration_product_strategy_source_correction.json');old=e['original_rationale'];new=e['corrected_rationale']
  self.assertEqual(read(ROOT/'data/revisions_high.json')['12미적Ⅰ-03-02']['internalRelations'][1]['rationale'],new)
  entry=next(v for v in read(ROOT/'data/secondary_analysis_details.json')['analyses'] if v['code']=='12미적Ⅰ-03-02')
  self.assertEqual(entry['onward'][0][1],new)
  site=ROOT.parent if ROOT.name=='research' else ROOT/'tmp/pathways-release'
  for path in [ROOT/'data/revised_relations.json',site/'dist/content/connections.json']:
   for r in read(path)['relations']:
    if {r['from'],r['to']}=={'standard:12미적Ⅰ-03-02','standard:12미적Ⅱ-03-03'}:
     self.assertNotIn(old,r['rationale']);self.assertNotIn(old,r.get('expected_response',''))
  for code in ['12미적Ⅰ-03-02','12미적Ⅱ-03-03']:
   self.assertNotIn(old,(ROOT/f'analyses/{code}.md').read_text(encoding='utf-8'))
   detail=read(site/f'dist/content/standards/{code}.json')
   self.assertNotIn(old,'\n'.join(s['body'] for s in detail['analysis']['sections']))

 def test_parabola_center_error_cannot_survive_in_active_copies(self):
  read=lambda p:json.loads(p.read_text(encoding='utf-8'))
  evidence=read(ROOT/'data/parabola_translation_source_correction.json')
  old=evidence['original_rationale'];new=evidence['corrected_rationale']
  self.assertEqual(read(ROOT/'data/revisions_high.json')['10공수2-01-06']['internalRelations'][0]['rationale'],new)
  entry=next(e for e in read(ROOT/'data/secondary_analysis_details.json')['analyses'] if e['code']=='10공수2-01-06')
  self.assertEqual(entry['onward'][0][1],new)
  site=ROOT.parent if ROOT.name=='research' else ROOT/'tmp/pathways-release'
  for path in [ROOT/'data/revised_relations.json',site/'dist/content/connections.json']:
   for r in read(path)['relations']:
    if {r['from'],r['to']}=={'standard:10공수2-01-06','standard:12기하01-01'}:
     self.assertNotIn(old,r['rationale']);self.assertNotIn(old,r.get('expected_response',''))
  for code in ['10공수2-01-06','12기하01-01']:
   self.assertNotIn(old,(ROOT/f'analyses/{code}.md').read_text(encoding='utf-8'))
   detail=read(site/f'dist/content/standards/{code}.json')
   self.assertNotIn(old,'\n'.join(s['body'] for s in detail['analysis']['sections']))

 def test_every_review_reaches_both_documents_current_portal_and_queue(self):
  records=load_reviews()['records'];self.assertTrue(records)
  site=ROOT.parent if ROOT.name=='research' else ROOT/'tmp/pathways-release'
  read=lambda p:json.loads(p.read_text(encoding='utf-8'))
  derived={r['id']:r for r in read(ROOT/'data/revised_relations.json')['relations']}
  catalog=read(site/'dist/content/catalog.json');bundle=read(site/'dist/content/connections.json')
  self.assertEqual(catalog['version'],bundle['version'])
  portal={r['id']:r for r in bundle['relations']};queued={r['relation_id'] for r in read(ROOT/'data/relation_analysis_scope_queue.json')['records']}
  for rid,review in records.items():
   self.assertNotIn(rid,queued);self.assertEqual(portal[rid],derived[rid]);self.assertEqual(derived[rid]['type'],review['type'])
   self.assertEqual(derived[rid]['review_state'],'self_checked')
   self.assertEqual(derived[rid]['analysis_review_evidence']['mathematical_check'],review['mathematical_check'])
   for code in [review['from'][9:],review['to'][9:]]:
    # Table cells escape the bar in P(A|B); compare the visible notation.
    document=(ROOT/f'analyses/{code}.md').read_text(encoding='utf-8').replace('\\|','|')
    detail=read(site/f'dist/content/standards/{code}.json');self.assertEqual(detail['version'],catalog['version'])
    payload='\n'.join(s['body'] for s in detail['analysis']['sections']).replace('\\|','|')
    for value in [review['rationale'],review['diagnostic'],review['expected_response'],review['limit'],*review['conditions']]:
     self.assertIn(value,document);self.assertIn(value,payload)

if __name__=='__main__':unittest.main()
