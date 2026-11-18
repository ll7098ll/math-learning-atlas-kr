import json,unittest
import copy
import hashlib
import tempfile,io,contextlib
from unittest.mock import patch
from pathlib import Path
R=Path(__file__).resolve().parents[1]
class OfficialTableExtraction(unittest.TestCase):
 def setUp(self):self.data=json.loads((R/'data/curriculum_structure.json').read_text(encoding='utf-8'))
 def test_middle_columns_and_category_labels(self):
  items=self.data['items'];texts={i['text'] for i in items}
  for text in ['소인수분해','정수와 유리수','유리수와 순환소수','제곱근과 실수','다항식의 연산','수학과제 탐구의 의미와 필요성']:
   self.assertIn(text,texts)
  for text in ['유리수와','제곱근과','이해','기능','태도']:
   self.assertNotIn(text,texts)
  self.assertTrue(all('핵심 아이디어' not in i['text'] for i in items))
 def test_degree_symbol_has_traceable_image_correction(self):
  item=next(i for i in self.data['items'] if i['id']=='CT-015-2-111')
  self.assertEqual(item['text'],'각도(°)')
  self.assertNotEqual(item['source_text_raw'],item['text'])
  self.assertEqual(item['display_correction']['pdf_page'],15)
  self.assertTrue((R/item['display_correction']['evidence_file']).is_file())
 def test_inline_middle_dot_is_not_a_new_bullet(self):
  from build_curriculum_structure import split_bullets
  self.assertEqual(split_bullets('과정\n⋅토의⋅토론을 통해\n 설명하기\n⋅자료 정리하기'),['토의⋅토론을 통해 설명하기','자료 정리하기'])
  page=[i['text'] for i in self.data['items'] if i['pdf_page']==252]
  self.assertIn('토의⋅토론을 통해 수학과제 탐구, 올바른 연구 윤리의 의미와 필요성 설명하기',page)
  self.assertNotIn('토의',page)
 def test_table_image_review_matches_current_source_and_items(self):
  registry=json.loads((R/'data/curriculum_table_image_reviews.json').read_text(encoding='utf-8'))
  self.assertEqual(registry['source_sha256'],self.data['source_sha256'])
  for review in registry['reviews']:
   evidence=R/review['evidence_file']
   self.assertEqual(hashlib.sha256(evidence.read_bytes()).hexdigest(),review['evidence_sha256'])
   items=[i for i in self.data['items'] if i['pdf_page']==review['pdf_page']]
   self.assertEqual(len(items),review['item_count'])
   self.assertEqual({i['source_fingerprint'] for i in items},set(review['item_fingerprints']))
 def test_review_identity_and_snapshot(self):
  items=self.data['items'];self.assertEqual(len({i['source_fingerprint'] for i in items}),len(items))
  reviewed=[i for i in items if i.get('mapping_review')]
  registry=json.loads((R/'data/curriculum_mapping_reviews.json').read_text(encoding='utf-8'))['reviews']
  self.assertEqual({i['source_fingerprint'] for i in reviewed},set(registry))
  self.assertTrue(all(not i['changed_cases_since_review'] for i in reviewed))
  self.assertTrue(all(set(i['mapping_review']['standard_codes'])<=set(i['scope_codes']) for i in reviewed))
 def test_entry_or_task_edit_requires_new_review(self):
  from mapping_review_author import changed_targets
  entries={};cases={}
  for path in (R/'data').glob('goal_hierarchy_*.json'):
   d=json.loads(path.read_text(encoding='utf-8'));entries.update({e['code']:e for e in d['entries']});cases.update({c['id']:c for c in d['cases']})
  review=next(i['mapping_review'] for i in self.data['items'] if i.get('mapping_review'))
  self.assertEqual(changed_targets(review,entries,cases),[])
  changed_entries=copy.deepcopy(entries);code=next(iter(review['entry_snapshots']))
  changed_entries[code]['scope']+=' changed'
  self.assertIn('entry:'+code,changed_targets(review,changed_entries,cases))
  changed_cases=copy.deepcopy(cases);cid=review['case_ids'][0]
  changed_cases[cid]['task']+=' changed'
  self.assertIn('case:'+cid,changed_targets(review,entries,changed_cases))
 def test_resource_edit_requires_new_review(self):
  import mapping_review_author as author
  with tempfile.TemporaryDirectory() as directory:
   root=Path(directory);resource=root/'model.csv';resource.write_text('x,y\n1,2\n',encoding='utf-8')
   review=dict(resource_snapshots={'model.csv':hashlib.sha256(resource.read_bytes()).hexdigest()})
   with patch.object(author,'R',root):
    self.assertEqual(author.changed_targets(review,{},{}),[])
    resource.write_text('x,y\n1,99\n',encoding='utf-8')
    self.assertEqual(author.changed_targets(review,{},{}),['resource:model.csv'])
 def test_reauthoring_does_not_silently_accept_a_changed_goal(self):
  import mapping_review_author as author
  source=next(i for i in self.data['items'] if i['pdf_page']==13)
  code='2수01-01';entry={'code':code,'scope':'original scope','goals':[{'id':code+':count','case_ids':['C']} ]}
  case={'id':'C','task':'original task'}
  with tempfile.TemporaryDirectory() as directory:
   root=Path(directory);(root/'data').mkdir()
   (root/'data/curriculum_structure.json').write_text(json.dumps({'items':[source]}),encoding='utf-8')
   corpus=root/'data/goal_hierarchy_fixture.json'
   write=lambda:corpus.write_text(json.dumps({'entries':[entry],'cases':[case]}),encoding='utf-8')
   write();decision={1:([code],'Fixture scope review')}
   with patch.object(author,'R',root),contextlib.redirect_stdout(io.StringIO()):
    author.write_decisions(13,decision,{})
    entry['scope']='changed scope';write()
    with self.assertRaisesRegex(AssertionError,'explicit re-review rationale'):author.write_decisions(13,decision,{})
    author.write_decisions(13,decision,{},reviewed_changes={1:'Fixture explicitly reviewed after scope change'})
if __name__=='__main__':unittest.main()
