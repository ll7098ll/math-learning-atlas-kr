"""Validate and merge durable hierarchy review records without inventing reviews."""
import copy
import json


def analysis_review_record(record):
    """Make an absent analysis label explicit without inferring a review."""
    result = copy.deepcopy(record)
    if not result.get('review_state'):
        result['review_state'] = 'legacy_draft'
        result.setdefault('analysis_review_note', '이전 분석 초안의 개별 수학적 분석 범위가 이 필드에 기록되지 않았다. 별도 위계 검토 원장의 상태·이력과 구별하며 자체 분석 완료·독립 검토·학생 검증으로 자동 승격하지 않는다.')
    result.setdefault('independent_review', False)
    result.setdefault('student_validated', False)
    return result


def load_registry(root, standard_ids, relation_ids):
    path = root / 'data/hierarchy_review_registry.json'
    registry = json.loads(path.read_text(encoding='utf-8')) if path.exists() else {}
    assert set(registry.get('standards', {})) <= set(standard_ids), 'Unknown reviewed standard'
    assert set(registry.get('relations', {})) <= set(relation_ids), 'Unknown reviewed relation'
    for group in ('standards', 'relations'):
        for key, entry in registry.get(group, {}).items():
            if entry.get('order_decision'):
                decision=entry['order_decision']
                assert group=='standards' and decision.get('kind')=='unordered_for_analyzed_scope', key
                assert all(decision.get(k) for k in ('scope','rationale','relation_ids','reviewer','date')), key
                assert set(decision['relation_ids'])<=set(relation_ids), key
            assert entry.get('state', 'unreviewed') in ('unreviewed', 'in_progress', 'self_checked', 'independently_reviewed', 'student_validated', 'deferred'), key
            if entry.get('state') in ('self_checked', 'independently_reviewed', 'student_validated'):
                assert entry.get('rationale') and entry.get('history'), f'Missing review evidence: {key}'
            if entry.get('independent_review') or entry.get('student_validated'):
                assert any(h.get('reviewer') and h.get('date') and h.get('scope') for h in entry.get('history', [])), f'Missing reviewer: {key}'
    return registry


def reviewed_record(record, registry):
    result = copy.deepcopy(record)
    entry = registry.get('relations', {}).get(record['id'], {})
    result.update({
        'hierarchy_review': entry.get('state', record.get('hierarchy_review', 'unreviewed')),
        'independent_review': entry.get('independent_review', record.get('independent_review', False)),
        'student_validated': entry.get('student_validated', record.get('student_validated', False)),
        'review_history': copy.deepcopy(entry.get('history', record.get('review_history', []))),
    })
    if entry.get('rationale'):
        result['hierarchy_review_rationale'] = entry['rationale']
    return result
