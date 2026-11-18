"""Read manually authored cross-standard claims with stable IDs and evidence."""
import json
from pathlib import Path


def load_claims(root, standards, existing_ids):
    result = []
    known = set(existing_ids)
    for file in sorted((root/'data').glob('hierarchy_*_claims.json')):
        for record in json.loads(file.read_text(encoding='utf-8'))['relations']:
            rid = record['id']
            assert rid not in known, f'Duplicate authored relation: {rid}'
            known.add(rid)
            assert record['from'].startswith('standard:') and record['to'].startswith('standard:'), rid
            assert record['from'][9:] in standards and record['to'][9:] in standards, rid
            assert record['from'] != record['to'], rid
            assert record['type'] in ('requires_for_task', 'generalizes', 'meaning_connection', 'contrasts'), rid
            assert all(record.get(k) for k in ('scope', 'rationale', 'conditions', 'diagnostic', 'expected_response', 'alternative_route', 'limit', 'review_history')), rid
            assert record['source_ids'] == ['CURRICULUM_2022_33'], rid
            # Authored mathematical reasoning must never masquerade as an external review.
            assert not record.get('independent_review') and not record.get('student_validated'), rid
            result.append(record)
    return result
