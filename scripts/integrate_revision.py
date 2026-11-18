from pathlib import Path
R=Path(__file__).resolve().parents[1];S=R/'tmp/pathways-release/dist'
def edit(p,old,new):
 t=p.read_text(encoding='utf-8');assert old in t,(str(p),old[:50]);p.write_text(t.replace(old,new),encoding='utf-8')
edit(R/'scripts/build_portal_data.py',"OUT = ROOT / 'portal' / 'math-atlas' / 'dist'", "import os\nOUT = Path(os.environ.get('MATH_ATLAS_DIST', ROOT / 'tmp' / 'pathways-release' / 'dist'))")
edit(R/'scripts/build_portal_data.py',"family = (details['families'].get(entry['family']) or secondary['profiles'].get(entry['family'])) if entry else None", "family = (details['families'][entry['family']] if code in entries else secondary['profiles'][entry['family']]) if entry else None")
edit(R/'scripts/build_portal_data.py',"relations = load('relations')['relations']", "relations = load('relations')['relations']\n    from detailed_revision import apply as apply_revisions\n    relations = apply_revisions(analyses, inventory, relations)")
edit(R/'scripts/build_portal_data.py',"detail = {**analyses[code]", "detail = {**analyses[code]")
# The original renderers remain available for unmigrated content, but never
# recreate unconditional AND claims even during an intermediate regeneration.
for name in ['expand_analyses.py','expand_secondary.py']:
 p=R/'scripts'/name;t=p.read_text(encoding='utf-8')
 lines=t.splitlines()
 for i,line in enumerate(lines):
  if ('첫 두 요소인' in line or '첫 번째 경로에서 **' in line) and 'AND' in line:
   indent=line[:len(line)-len(line.lstrip())]
   if 'out += [' in line:lines[i]=indent+"out += ['조건 묶음은 개별 과제와 경로에서 검토한 경우에만 함께 필요한 조건으로 기록한다.', '',"
   else:lines[i]=indent+"'조건 묶음은 개별 과제와 경로에서 검토한 경우에만 함께 필요한 조건으로 기록한다.','',"
 p.write_text('\n'.join(lines)+'\n',encoding='utf-8')
edit(S/'modules/concept-pathways.mjs',"s.code,s])),c=data.concept;", "s.code,s])),c={...data.concept};")
edit(S/'modules/concept-pathways.mjs',"r.order_role==='meaning_expansion'&&r.type==='generalizes'", "r.order_role==='meaning_expansion'&&(r.type==='generalizes'||r.type==='requires_for_task')")
edit(S/'modules/concept-pathways.mjs',"r=>r.type==='generalizes'", "r=>r.type==='generalizes'||r.type==='requires_for_task'")
edit(S/'modules/concept-pathways.mjs',"위계 미검토</span></a>","관계 분석 초안</span></a>")
edit(S/'modules/concept-pathways.mjs',"${r.type==='generalizes'?'의미 확장 초안':'연결 초안'} · 위계 미검토", "${r.type==='requires_for_task'?'과제별 조건':r.type==='generalizes'?'의미 확장 초안':'연결 초안'} · ${r.review_state==='self_checked'?'자체 분석':'추가 검토 필요'}")
edit(S/'modules/detail.mjs',"const groups=relationGroups", "if(a.schemaVersion===2)return revisedStandardPage(s,a,p);\n const groups=relationGroups")
with (S/'modules/detail.mjs').open('a',encoding='utf-8') as f:f.write('''
function revisedStandardPage(s,a,p){
 const scope=p.get('scope')||'all';
 const toc=a.sections.map(sec=>`<a href="${url('standard',{code:s.code,section:sec.id,scope})}" data-section="${sec.id}">${esc(sec.title)}</a>`).join('');
 return `<header class="standard-header"><p>${esc(s.level)} · ${esc(s.subject)} · ${esc(s.code)}</p><h1 tabindex="-1">${esc(a.title)}</h1><div class="official-statement"><span class="label">공식 성취기준</span><p>${esc(s.statement)}</p><a href="curriculum.pdf#page=${s.pdfPages[0]}" target="_blank" rel="noopener">교육과정 PDF ${s.pdfPages.join(', ')}쪽 ↗</a></div><p>개별 수학적 분석과 교수 설계 초안 · 독립 검토와 학생 반응 검증 전</p><div class="cp-actions"><a class="button" href="${url('network',{node:s.code,scope})}">연결망에서 보기</a><a class="button" href="${url('hierarchy',{q:s.code,scope})}">내부 관계와 위계 찾기</a><a class="button" href="${url('connections',{code:s.code,scope})}">관계 근거</a><button class="button" data-print>인쇄</button></div></header><div class="reading-layout"><article class="reading-body">${a.sections.map((sec,i)=>`<section id="${sec.id}" class="reading-section"><p class="section-index">${String(i+1).padStart(2,'0')}</p><h2>${esc(sec.title)}</h2><div class="prose">${sec.id==='connections'&&scope!=='all'?`<details><summary>다른 학교급으로 이어지는 관계 펼치기</summary>${markdown(sec.body)}</details>`:markdown(sec.body)}</div></section>`).join('')}</article><aside class="reading-toc"><nav aria-label="상세 분석 목차">${toc}</nav></aside></div>`;
}
''')
# Scope summaries are generated from the same relation slice as the diagram.
edit(R/'scripts/build_concept_pathways.py',"'order_role': 'meaning_expansion' if r['type'] == 'generalizes' else 'unordered_connection'", "'order_role': 'meaning_expansion' if r['type'] in ('generalizes','requires_for_task') and r.get('review_state') != 'candidate' else 'unordered_connection'")
edit(R/'scripts/build_concept_pathways.py',"groups.append(summary)", "summary['by_scope'] = {}\n        for scope, level in [('e','초등학교'),('m','중학교'),('h','고등학교')]:\n            local = [r for r in edges if standards[r['from'][9:]]['level'] == level and standards[r['to'][9:]]['level'] == level]\n            n = sum(standards[c]['level'] == level for c in members)\n            count = sum(r['order_role'] == 'meaning_expansion' for r in local)\n            summary['by_scope'][scope] = {'members': n, 'relations': len(local), 'expansions': count, 'hierarchy_status': 'expansion_draft' if count else 'order_unreviewed'}\n        groups.append(summary)")
edit(S/'modules/pathways.mjs',"new Map((index?.groups||[]).map(g=>[g.id,g]))", "new Map((index?.groups||[]).map(g=>[g.id,{...g,...g.by_scope?.[scope]}]))")
edit(S/'modules/pathways.mjs',"index?.groups.filter(g=>g.expansions)", "[...byConcept.values()].filter(g=>g.expansions)")
edit(S/'modules/pathways.mjs',"index?.groups.filter(g=>!g.expansions)", "[...byConcept.values()].filter(g=>!g.expansions)")
edit(S/'modules/pathways.mjs',"학교급 범위를 바꿔도 위계의 목표와 필요한 기초는 유지됩니다.", "선택한 학교급의 기준과 내부 관계를 살펴보세요. 필요한 다른 학교급 연결은 목표 화면에서 펼칠 수 있습니다.")
print('revision integration applied')
