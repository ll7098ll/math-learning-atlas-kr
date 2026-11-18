"""Guard authored route conditions against later generic-profile corrections."""
import json
from pathlib import Path

root=Path(__file__).resolve().parents[1]
relations=json.loads((root/'data/revised_relations.json').read_text(encoding='utf-8'))['relations']
by_id={r['id']:r for r in relations}
count=0
for file in (root/'data').glob('hierarchy_*_claims.json'):
    for claim in json.loads(file.read_text(encoding='utf-8'))['relations']:
        derived=by_id[claim['id']]
        for key,value in claim.items():
            assert derived[key]==value, f'Authored field changed: {claim["id"]}.{key}'
        assert 'original_conditions' not in derived, claim['id']
        count+=1
print(f'Preserved all authored fields for {count} task-route claims')
