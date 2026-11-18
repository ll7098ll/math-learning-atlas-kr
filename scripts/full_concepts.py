"""Compile the complete, explicit concept taxonomy and recorded connections."""
from collections import Counter

LEVELS = ['초등학교', '중학교', '고등학교']

def compile_flows(taxonomy, standards, relations):
    by_code = {s['code']: s for s in standards}
    order = {s['code']: i for i, s in enumerate(standards)}
    primary = {}
    for g in taxonomy['groups']:
        assert len(g['stage_labels']) == 3, g['id']
        assert g['primary_codes'], g['id']
        for code in g['primary_codes']:
            assert code in by_code, (g['id'], code)
            assert code not in primary, ('duplicate primary', code)
            primary[code] = g['id']
        for code in g['additional_codes']:
            assert code in by_code and code not in g['primary_codes'], (g['id'], code)
    assert set(primary) == set(by_code), ('unassigned', set(by_code) - set(primary))
    edges = [r for r in relations if r['from'].startswith('standard:') and r['to'].startswith('standard:')]
    strands = []
    for g in taxonomy['groups']:
        members = set(g['primary_codes'] + g['additional_codes'])
        inside, outside = [], []
        related = {l: {} for l in LEVELS}
        neighbors = Counter()
        for r in edges:
            a, b = r['from'][9:], r['to'][9:]
            if a in members and b in members:
                inside.append(r['id'])
            elif a in members or b in members:
                outside.append(r['id'])
                other, own = (b, a) if a in members else (a, b)
                neighbors[primary[other]] += 1
                if by_code[other]['level'] != by_code[own]['level']:
                    related[by_code[other]['level']].setdefault(other, []).append(r['id'])
        stages = []
        for i, level in enumerate(LEVELS):
            codes = sorted((c for c in members if by_code[c]['level'] == level), key=order.get)
            stages.append(dict(headline=g['stage_labels'][i], codes=codes,
                primary_codes=[c for c in codes if primary[c] == g['id']],
                additional_codes=[c for c in codes if primary[c] != g['id']],
                related=[dict(code=c, concept=primary[c], relation_ids=related[level][c])
                         for c in sorted(related[level], key=order.get)]))
        strands.append(dict(id=g['id'], title=g['title'], domain=g['domain'], question=g['question'],
                            stages=stages, relation_ids=inside, external_relation_ids=outside,
                            related_concepts=[dict(id=id, records=n) for id,n in neighbors.items() if id != g['id']]))
    return dict(schema_version='3.0', title=taxonomy['title'], classification=taxonomy['classification'],
                interpretation=taxonomy['interpretation'], assignment_basis=taxonomy['assignment_basis'],
                coverage=dict(total=len(by_code), primary_assigned=len(primary), unassigned=[],
                              by_level=dict(Counter(s['level'] for s in standards)), concepts=len(strands),
                              memberships=sum(len(s['codes']) for g in strands for s in g['stages']),
                              standard_relations=len(edges)), strands=strands)
