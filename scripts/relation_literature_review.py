"""Attach explicitly reviewed literature context without changing relation claims."""
from urllib.parse import urlsplit

from literature_review import ROOT, digest, read


FILE = 'data/relation_literature_reviews.json'
LABELS = {'activity_context': '과제 설계 참고', 'inference_limit': '연결 해석의 한계'}


def relation_snapshot(relation):
    return digest({key: value for key, value in relation.items() if key != 'literature_context'})


def claim_snapshot(claim, source):
    return digest([claim, source['snapshot_sha256'], source['bibliography_snapshot']])


def apply_literature_context(relations, literature, root=ROOT, *, registry=None):
    if registry is None:
        if not (root / FILE).exists():
            return
        registry = read(root, FILE)
    assert registry['schema_version'] == 1 and registry['reviewer'] and registry['date']
    by_relation = {r['id']: r for r in relations}
    claims = {c['id']: c for c in literature['claims']}
    contexts = {}
    seen = set()
    for row in registry['records']:
        pair = row['relation_id'], row['claim_id']
        assert pair not in seen, pair
        seen.add(pair)
        relation, claim = by_relation[pair[0]], claims[pair[1]]
        endpoints = [relation[key] for key in ('from', 'to')]
        assert all(s.startswith('standard:') for s in endpoints), pair
        assert {s.removeprefix('standard:') for s in endpoints} <= set(claim['standard_codes']), pair
        source = literature['sources'][claim['source_id']]
        assert relation_snapshot(relation) == row['relation_snapshot'], ('Relation changed; review again', pair)
        assert claim_snapshot(claim, source) == row['claim_snapshot'], ('Literature changed; review again', pair)
        assert row['finding'].strip() and row['limit'].strip(), pair
        link = next((loc.split()[0] for loc in claim['locations'] if loc.startswith(('https://', 'http://'))), source['display']['url'])
        assert urlsplit(link).scheme in ('https', 'http') and urlsplit(link).netloc, pair
        contexts.setdefault(pair[0], []).append(dict(
            claim_id=pair[1], source_id=claim['source_id'], title=source['display']['title'], url=link,
            role=LABELS[row['role']], finding=row['finding'], limit=row['limit'],
        ))
    for relation_id, rows in contexts.items():
        by_relation[relation_id]['literature_context'] = rows
