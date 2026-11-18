"""Recommendation evidence grades cannot become claims of local effectiveness."""
import json,tempfile,unittest
from pathlib import Path
from literature_review import ROOT,load_registry,rating_note
from test_literature_review import ScopedLiteratureEvidence

class RecommendationScope(unittest.TestCase):
 def fixture(self,root):
  registry,_,_=ScopedLiteratureEvidence.fixture(self,root)
  registry['sources']['S']['evidence_ratings']={'2':'Moderate'}
  registry['claims'][0].update(role='instructional_recommendation_with_evidence_scope',local_effect_tested=False,recommendations=[dict(number=2,evidence_rating='Moderate',application_limit='A recommendation is not a test of our task')])
  return registry
 def save(self,root,registry):
  (root/'data/literature_claim_reviews.json').write_text(json.dumps(registry),encoding='utf-8')
 def test_scoped_recommendation_is_accepted(self):
  with tempfile.TemporaryDirectory() as directory:
   root=Path(directory);registry=self.fixture(root);self.save(root,registry)
   self.assertEqual(load_registry(root)['claims'][0]['recommendations'][0]['evidence_rating'],'Moderate')
 def test_changed_evidence_grade_is_rejected(self):
  with tempfile.TemporaryDirectory() as directory:
   root=Path(directory);registry=self.fixture(root);registry['claims'][0]['recommendations'][0]['evidence_rating']='Strong';self.save(root,registry)
   with self.assertRaisesRegex(AssertionError,'rating'):load_registry(root)
 def test_recommendation_cannot_be_promoted_to_local_effect(self):
  with tempfile.TemporaryDirectory() as directory:
   root=Path(directory);registry=self.fixture(root);registry['claims'][0]['local_effect_tested']=True;self.save(root,registry)
   with self.assertRaises(AssertionError):load_registry(root)
 def test_recommendation_needs_its_own_application_limit(self):
  with tempfile.TemporaryDirectory() as directory:
   root=Path(directory);registry=self.fixture(root);registry['claims'][0]['recommendations'][0]['application_limit']='';self.save(root,registry)
   with self.assertRaises(AssertionError):load_registry(root)
 def test_actual_grades_reach_detailed_documents_and_portal(self):
  registry=load_registry();source=registry['sources']['IES_FRACTIONS_2010']
  self.assertEqual(source['evidence_ratings'],{'1':'Minimal','2':'Moderate','3':'Moderate','4':'Minimal','5':'Minimal'})
  self.assertEqual(source['text_pdf_pages'],list(range(1,91)))
  self.assertEqual(source['visual_pdf_pages'],list(range(1,91)))
  extension=json.loads((ROOT/source['reading_extension']['file']).read_text(encoding='utf-8'))
  self.assertEqual(extension['new_text_pdf_pages'],[])
  self.assertEqual(extension['new_visual_pdf_pages'],sorted(set(range(1,91))-set(extension['previous_review']['visual_pdf_pages'])))
  self.assertEqual(len(extension['new_visual_pdf_pages']),67)
  self.assertEqual(extension['protocol']['visual_pdf_pages'],list(range(1,9)))
  self.assertEqual(extension['protocol']['new_visual_pdf_pages'],[1,2,3,5,6,7,8])
  self.assertFalse(extension['protocol']['redistributed'])
  self.assertEqual(extension['source_discrepancies'],source['source_discrepancies'])
  self.assertFalse(extension['exact_condition_checks']['student_data'])
  site=ROOT.parent if ROOT.name=='research' else ROOT/'tmp/pathways-release'
  for claim in registry['claims']:
   if claim['source_id']!='IES_FRACTIONS_2010':continue
   note=rating_note(claim);self.assertTrue(note)
   for code in claim['standard_codes']:
    self.assertIn(note,(ROOT/f'analyses/{code}.md').read_text(encoding='utf-8'))
    payload=json.loads((site/f'dist/content/standards/{code}.json').read_text(encoding='utf-8'))
    self.assertIn(note,'\n'.join(s['body'] for s in payload['analysis']['sections']))
 def test_algebra_revision_and_recommendation_limits_reach_delivery(self):
  registry=load_registry();source=registry['sources']['IES_ALGEBRA_2015']
  self.assertEqual(source['reviewed_revision'],'2019-01')
  self.assertEqual(source['evidence_ratings'],{'1':'Minimal','2':'Minimal','3':'Moderate'})
  self.assertEqual(source['text_pdf_pages'],list(range(1,source['pdf_pages_total']+1)))
  self.assertEqual(source['visual_pdf_pages'],list(range(1,72)))
  extension=json.loads((ROOT/source['reading_extension']['file']).read_text(encoding='utf-8'))
  self.assertEqual(extension['new_text_pdf_pages'],
                   sorted(set(source['text_pdf_pages'])-set(extension['previous_review']['text_pdf_pages'])))
  self.assertEqual(extension['new_text_pdf_pages'],[])
  self.assertEqual(extension['new_visual_pdf_pages'],
                   sorted(set(source['visual_pdf_pages'])-set(extension['previous_review']['visual_pdf_pages'])))
  self.assertEqual(len(extension['new_visual_pdf_pages']),54)
  historical=json.loads((ROOT/extension['previous_reading_extension']['file']).read_text(encoding='utf-8'))
  self.assertEqual(len(historical['new_text_pdf_pages']),39)
  self.assertEqual(historical['cumulative_visual_pdf_pages'],[9,13,16,17,27,28,29,37,38,48,55,57,58,61,62,63,70])
  self.assertEqual(extension['previous_review']['text_pdf_pages'],historical['cumulative_text_pdf_pages'])
  self.assertFalse(extension['official_erratum_or_cause_verified'])
  self.assertEqual(extension['protocol']['text_pdf_pages'],list(range(1,9)))
  self.assertEqual(extension['protocol']['visual_pdf_pages'],[])
  self.assertFalse(extension['protocol']['redistributed'])
  self.assertEqual(source['snapshot_sha256'],'83f6f973eb79caa2170f2818034d533322258708d38a777620862b95a9cbc730')
  originals={row['source_id']:row for row in source['primary_source_crosschecks']}
  self.assertEqual(len(originals),len(source['primary_source_crosschecks']))
  for source_id,comparison in originals.items():
   original=registry['sources'][source_id]
   self.assertEqual(comparison['snapshot_file'],original['snapshot_file'])
   self.assertEqual(comparison['snapshot_sha256'],original['snapshot_sha256'])
   self.assertEqual(set(comparison['claim_ids']),
                    {c['id'] for c in registry['claims'] if c['source_id']==source_id})
  crosscheck=originals['RITTLE_JOHNSON_STAR_2009_EQUATION_COMPARISONS']
  self.assertEqual(sum(crosscheck['author_conditions'].values()),162)
  self.assertTrue(crosscheck['shared_comparison'])
  self.assertFalse(crosscheck['same_analysis'])
  prior=originals['RITTLE_JOHNSON_STAR_DURKIN_2009_PRIOR_ALGEBRA']
  self.assertEqual(prior['participated_n']-sum(prior['excluded'].values()),236)
  self.assertEqual(sum(prior['author_condition_n'].values()),236)
  self.assertEqual(prior['guide_n'],{'attempted':101,'not_observed':55})
  self.assertTrue(prior['attempt_could_be_incorrect'])
  self.assertFalse(prior['same_analysis'])
  prior_notes=json.loads((ROOT/prior['snapshot_file']).read_text(encoding='utf-8'))
  self.assertFalse(prior_notes['retention']['strategy_use_scored'])
  self.assertEqual(prior_notes['retention']['conceptual_missing_pct'],37)
  crosscheck=originals['RITTLE_JOHNSON_STAR_2007_EQUATION_METHODS']
  self.assertEqual(crosscheck['assigned_n']-crosscheck['missing_posttest_n'],crosscheck['wwc_n'])
  self.assertEqual(crosscheck['assigned_pairs'],[18,17])
  self.assertTrue(crosscheck['comparison_description_conflict'])
  self.assertFalse(crosscheck['same_analysis'])
  official=next(row for row in source['official_review_crosschecks']
                if row['source_id']=='WWC_79864_EQUATION_COMPARISON_2012')
  review=registry['sources'][official['source_id']]
  self.assertEqual(official['snapshot_sha256'],review['snapshot_sha256'])
  self.assertEqual(official['snapshot_file'],review['snapshot_file'])
  self.assertFalse(official['article_full_text_obtained'])
  self.assertEqual(official['article_total_assigned_n'],198)
  self.assertEqual(official['immediate_comparison_n'],{'1 Day':124,'1 Month':118})
  self.assertEqual(official['delayed_comparison_n'],{'2 Days':115})
  rows=json.loads((ROOT/review['snapshot_file']).read_text(encoding='utf-8'))['outcomes']
  self.assertEqual(len(rows),10)
  self.assertEqual({(r['comparison'],r['measure'],r['timing']) for r in rows if r['significant']},
                   {('immediate','flexibility_use','1 Day'),('immediate','flexibility_use','1 Month')})
  claims=[c for c in registry['claims'] if c['source_id']=='IES_ALGEBRA_2015']
  self.assertEqual({c['id'] for c in claims},{f'IA{i:02}' for i in range(1,12)})
  site=ROOT.parent if ROOT.name=='research' else ROOT/'tmp/pathways-release'
  for claim in claims:
   self.assertFalse(claim['local_effect_tested']);note=rating_note(claim)
   for code in claim['standard_codes']:
    self.assertIn(note,(ROOT/f'analyses/{code}.md').read_text(encoding='utf-8'))
    payload=json.loads((site/f'dist/content/standards/{code}.json').read_text(encoding='utf-8'))
    self.assertIn(note,'\n'.join(s['body'] for s in payload['analysis']['sections']))
  for probe in source['observations']:
   self.assertFalse(probe['student_validated'])
   for code in probe['standard_codes']:
    payload=json.loads((site/f'dist/content/standards/{code}.json').read_text(encoding='utf-8'))
    self.assertIn(probe['id'],'\n'.join(s['body'] for s in payload['analysis']['sections']))
 def test_early_math_age_progression_and_unresolved_count_limits_reach_delivery(self):
  registry=load_registry();source=registry['sources']['IES_EARLY_2013']
  self.assertEqual(source['evidence_ratings'],{'1':'Moderate','2':'Minimal','3':'Minimal','4':'Minimal','5':'Minimal'})
  self.assertEqual(source['intended_learner_scope']['ages'],[3,6])
  self.assertFalse(source['intended_learner_scope']['korean_elementary_full_scope_established'])
  self.assertFalse(source['direct_particular_progression_comparison_established'])
  self.assertEqual(source['text_pdf_pages'],list(range(1,source['pdf_pages_total']+1)))
  self.assertEqual(source['pdf_pages_total'],165)
  self.assertEqual(len(source['visual_pdf_pages']),116)
  self.assertEqual(source['source_discrepancies'][0]['status'],'epic_inclusion_resolved_study_count_open')
  final=json.loads((ROOT/source['reading_extension']['file']).read_text(encoding='utf-8'))
  self.assertEqual(source['source_discrepancies'],final['source_corrections'])
  instruction=json.loads((ROOT/final['previous_reading_extension']['file']).read_text(encoding='utf-8'))
  extension=json.loads((ROOT/instruction['previous_reading_extension']['file']).read_text(encoding='utf-8'))
  appendix=json.loads((ROOT/extension['previous_reading_extension']['file']).read_text(encoding='utf-8'))
  self.assertEqual(appendix['table_d1']['counts_by_recommendation'],[23,13,12,16,20])
  prior=json.loads((ROOT/appendix['previous_reading_extension']['file']).read_text(encoding='utf-8'))
  self.assertFalse(prior['measurement_table_audit']['author_counting_intent_confirmed'])
  self.assertEqual(prior['previous_review']['text_pdf_pages'],[2,4,10,13,17,18,19,20,22,23,24,25,26,29,31,32,33,34,36,37,38,39,40,42,43,44,45,46,71,72,75,76,96,97,107,108])
  self.assertEqual(set(appendix['cumulative_text_pdf_pages'])-set(prior['cumulative_text_pdf_pages']),set(appendix['new_text_pdf_pages']))
  self.assertEqual(set(extension['cumulative_text_pdf_pages'])-set(appendix['cumulative_text_pdf_pages']),set(range(82,96)))
  self.assertEqual(set(extension['cumulative_visual_pdf_pages'])-set(appendix['cumulative_visual_pdf_pages']),set(range(82,96)))
  self.assertEqual(set(instruction['cumulative_text_pdf_pages'])-set(extension['cumulative_text_pdf_pages']),set(range(109,138)))
  self.assertEqual(set(instruction['cumulative_visual_pdf_pages'])-set(extension['cumulative_visual_pdf_pages']),set(range(109,138)))
  for table,contrasts,outcomes in [('table_d3',6,22),('table_d4',18,65)]:
   comparisons=extension[table]['comparisons']
   self.assertEqual(len(comparisons),contrasts)
   self.assertEqual(sum(row['printed_outcome_rows'] for row in comparisons),outcomes)
   self.assertTrue(extension[table]['participants_are_not_summed'])
  curtis=next(row for row in extension['table_d4']['comparisons'] if row['contrast']=='experiment 1 count support')
  self.assertEqual((curtis['printed_total'],curtis['checked_total']),(25,35))
  self.assertEqual(curtis['intervention']+curtis['comparison'],curtis['checked_total'])
  self.assertTrue(extension['review_protocol']['separate_from_guide'])
  self.assertEqual(extension['review_protocol']['text_pdf_pages'],list(range(1,10)))
  for table,citations,contrasts,outcomes in [('table_d6',12,14,35),('table_d7',16,20,42),('table_d8',20,26,74)]:
   summary=instruction[table]
   self.assertEqual((summary['citation_or_chapter_units'],summary['comparison_blocks'],summary['printed_outcome_rows']),(citations,contrasts,outcomes))
   self.assertTrue(summary['repeated_comparisons_across_tables_are_not_independent'])
  self.assertTrue(instruction['selected_d7_conditions']['child_explains_examiner_reasoning_after_feedback'])
  self.assertEqual(instruction['unread_full_pdf_pages'],[*range(138,142),*range(143,151),*range(152,166)])
  self.assertEqual(final['unread_full_pdf_pages'],[])
  self.assertEqual(set(source['text_pdf_pages'])-set(instruction['cumulative_text_pdf_pages']),set(instruction['unread_full_pdf_pages']))
  self.assertEqual(set(source['visual_pdf_pages'])-set(instruction['cumulative_visual_pdf_pages']),set(instruction['unread_full_pdf_pages']))
  measure=final['measurement']
  self.assertEqual((measure['d5_printed_comparison_rows'],len(measure['appendix_note_284_citation_units']),len(measure['result_summary_notes_79_and_287_citation_units'])),(11,10,9))
  self.assertFalse(measure['original_editorial_intent_confirmed'])
  self.assertEqual(final['data_analysis']['main_total_notes_81_82'],8)
  self.assertEqual(final['bibliography']['bold_reference_entries'],30)
  self.assertEqual(final['bibliography']['d1_citation_rows'],29)
  self.assertFalse(final['bibliography']['cited_study_reading_implied'])
  claims=[c for c in registry['claims'] if c['source_id']=='IES_EARLY_2013']
  self.assertEqual({c['id'] for c in claims},{f'IE{i:02}' for i in range(1,21)})
  self.assertIn('실험자가',next(c['support'] for c in claims if c['id']=='IE17'))
  site=ROOT.parent if ROOT.name=='research' else ROOT/'tmp/pathways-release'
  for claim in claims:
   self.assertFalse(claim['local_effect_tested']);note=rating_note(claim);self.assertTrue(note)
   for code in claim['standard_codes']:
    self.assertIn(note,(ROOT/f'analyses/{code}.md').read_text(encoding='utf-8'))
    payload=json.loads((site/f'dist/content/standards/{code}.json').read_text(encoding='utf-8'))
    self.assertIn(note,'\n'.join(s['body'] for s in payload['analysis']['sections']))
if __name__=='__main__':unittest.main(defaultTest='RecommendationScope')
