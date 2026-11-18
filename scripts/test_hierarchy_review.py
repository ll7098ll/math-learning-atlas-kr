import json
import tempfile
import unittest
from pathlib import Path
from hierarchy_review import load_registry, reviewed_record, analysis_review_record


class DurableReviewTests(unittest.TestCase):
    def test_missing_analysis_scope_is_explicit_without_becoming_a_review(self):
        record={'id':'R','conditions':['task A'],'review_history':[{'scope':'previous scope'}]}
        result=analysis_review_record(record)
        self.assertEqual(result['review_state'],'legacy_draft')
        self.assertFalse(result['independent_review']);self.assertFalse(result['student_validated'])
        self.assertIn('별도 위계 검토',result['analysis_review_note'])
        self.assertNotIn('review_state',record)
        result['conditions'].append('changed');self.assertEqual(record['conditions'],['task A'])

    def test_recording_scope_keeps_existing_evidence_and_is_idempotent(self):
        record={'id':'R','review_state':'candidate','independent_review':True,'student_validated':True,'review_history':[{'reviewer':'Teacher','date':'2026-10-30','scope':'task A'}]}
        result=analysis_review_record(record)
        self.assertEqual(result,record);self.assertEqual(analysis_review_record(result),result)

    def test_hierarchy_self_check_does_not_promote_the_analysis_label(self):
        record=analysis_review_record({'id':'R'})
        registry={'relations':{'R':{'state':'self_checked','rationale':'scoped prerequisite decision','history':[{'scope':'task A'}]}}}
        merged=reviewed_record(record,registry)
        self.assertEqual(merged['hierarchy_review'],'self_checked')
        self.assertEqual(merged['review_state'],'legacy_draft')
        self.assertFalse(merged['independent_review']);self.assertFalse(merged['student_validated'])

    def test_regeneration_keeps_existing_review(self):
        record = {'id': 'R', 'independent_review': True, 'review_history': [{'reviewer': 'Teacher', 'scope': 'task A', 'date': '2026-10-30'}]}
        self.assertEqual(reviewed_record(record, {})['review_history'], record['review_history'])
        self.assertTrue(reviewed_record(record, {})['independent_review'])

    def test_registry_survives_repeat_merge(self):
        entry = {'state': 'self_checked', 'rationale': 'Checked task A', 'history': [{'kind': 'self_check'}]}
        registry = {'relations': {'R': entry}}
        once = reviewed_record({'id': 'R'}, registry)
        twice = reviewed_record(once, registry)
        self.assertEqual(once, twice)
        once['review_history'].append({'kind': 'mutation'})
        self.assertEqual(len(entry['history']), 1)

    def test_unsubstantiated_review_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'data').mkdir()
            file = root / 'data/hierarchy_review_registry.json'
            file.write_text(json.dumps({'relations': {'R': {'state': 'independently_reviewed', 'independent_review': True}}}), encoding='utf-8')
            with self.assertRaises(AssertionError):
                load_registry(root, ['S'], ['R'])
            file.write_text(json.dumps({'standards': {'missing': {'state': 'unreviewed'}}}), encoding='utf-8')
            with self.assertRaises(AssertionError):
                load_registry(root, ['S'], ['R'])


if __name__ == '__main__':
    unittest.main()
