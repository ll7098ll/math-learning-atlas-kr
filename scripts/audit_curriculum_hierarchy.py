"""Read-only hierarchy audit; output is a report, not prerequisite assertions."""
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def components(edges):
    graph = defaultdict(set)
    for a, b in edges:
        graph[a].add(b)
        graph[b]
    index, low, stack, active, groups = {}, {}, [], set(), []

    def visit(v):
        index[v] = low[v] = len(index)
        stack.append(v)
        active.add(v)
        for w in graph[v]:
            if w not in index:
                visit(w)
                low[v] = min(low[v], low[w])
            elif w in active:
                low[v] = min(low[v], index[w])
        if low[v] == index[v]:
            group = []
            while True:
                w = stack.pop()
                active.remove(w)
                group.append(w)
                if w == v:
                    break
            groups.append(group)

    for v in list(graph):
        if v not in index:
            visit(v)
    cyclic = [sorted(g) for g in groups if len(g) > 1]
    return {'cyclic_components': len(cyclic),
            'nodes_in_cyclic_components': sum(map(len, cyclic)),
            'largest_component': max(map(len, cyclic), default=0),
            'sample': sorted(cyclic, key=len, reverse=True)[:2]}


def main():
    def read(name):
        return json.loads((ROOT / 'data' / (name + '.json')).read_text(encoding='utf-8'))
    relations = read('relations')['relations']
    standard_edges = [r for r in relations if r['from'].startswith('standard:') and r['to'].startswith('standard:')]
    secondary = read('secondary_analysis_details')['analyses']
    result = {
        'scope': 'Structure audit only. Cycles in semantic links are not errors or evidence of learning order.',
        'source_sha256': hashlib.sha256((ROOT / 'data/relations.json').read_bytes()).hexdigest(),
        'standards': len(read('standards')['standards']),
        'elements': len(read('elements')['elements']),
        'relation_records': len(relations),
        'relation_types': dict(Counter(r['type'] for r in relations)),
        'standard_relation_records': len(standard_edges),
        'standard_relation_types': dict(Counter(r['type'] for r in standard_edges)),
        'task_requirement_target_count': len({r['to'] for r in relations if r['type'] == 'requires_for_task'}),
        'explicit_instructional_sequences': sum(r['type'] == 'instructional_sequence' for r in relations),
        'secondary_prior_mentions': sum(len(a.get('prior', [])) for a in secondary),
        'secondary_onward_mentions': sum(len(a.get('onward', [])) for a in secondary),
        'all_standard_edges_as_directed': components([(r['from'], r['to']) for r in standard_edges]),
        'generalizes_only': components([(r['from'], r['to']) for r in standard_edges if r['type'] == 'generalizes']),
    }
    target = ROOT / 'data' / 'hierarchy_audit.json'
    target.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k: v for k, v in result.items() if not isinstance(v, dict)}, ensure_ascii=False))
    for k in ('all_standard_edges_as_directed', 'generalizes_only'):
        print(k, {a: b for a, b in result[k].items() if a != 'sample'})


if __name__ == '__main__':
    main()
