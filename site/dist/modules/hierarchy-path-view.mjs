import {catalog, inScope} from './store.mjs';
import {directionGraph} from './hierarchy-graph.mjs';
import {esc, url, heading, standardURL, sourcesHTML, list,relationLiteratureHTML} from './ui.mjs';

export function renderHierarchyPaths(p, data, index, graph) {
 const byCode = new Map(catalog.standards.map(s => [s.code, s]));
 const target = byCode.has(p.get('target')) ? p.get('target') : data.concept.member_codes[0];
 const depth = ['1','2','3','all'].includes(p.get('depth')) ? p.get('depth') : '3';
 const scope = p.get('scope') || 'all', model = directionGraph(graph, target, depth);
 const decision=graph.standard_decisions?.[target];
 const decisionNote=decision?`<aside class="cp-evidence" data-order-decision><h2>검토한 범위에서는 순서를 두지 않았습니다</h2><p>${esc(decision.scope)}</p><p>${esc(decision.rationale)}</p><a class="button" href="${esc(url('hierarchy',{concept:data.concept.id,target,mode:'meaning',scope}))}">방향 없는 의미 연결 보기</a><p>이 판정은 기록한 활동 범위에 한정됩니다. 다른 과제의 선수 조건은 별도 검토합니다.</p></aside>`:'';
 const route = changes => url('hierarchy', {concept:data.concept.id, target, mode:'path', depth, scope, ...changes});
 const title = code => byCode.get(code)?.title || code;
 const context=(graph.context_relations||[]).filter(r=>decision?.relation_ids.includes(r.id));
 const displayEdges=[...model.edges,...context];
 const ordered=r=>['generalizes','requires_for_task'].includes(r.type);
 const recordLink = r => `<a class="hp-record" href="${esc(route({relation:r.id}))}"><span>${esc(r.type === 'requires_for_task' ? '과제별 필요 조건' : r.type==='generalizes'?'의미 확장':'의미 연결 · 순서 없음')}</span><strong>${esc(title(r.from.slice(9)))} ${ordered(r)?'→':'↔'} ${esc(title(r.to.slice(9)))}</strong><small>${esc(r.id)}</small></a>`;
 const card = (code, distance, path) => {
  const s = byCode.get(code), boundary = !inScope(s, scope);
  return `<article class="hp-card ${code === target ? 'hp-goal' : ''} ${boundary ? 'hp-boundary' : ''}" data-path-node="${esc(code)}"><small>${esc(code)} · ${esc(s.level)}${boundary ? ' · 선택 학교급 밖' : ''}</small><a class="hp-node-title" href="${esc(route({target:code,relation:''}))}">${esc(s.title)}</a><p>${esc(s.statement)}</p>${distance ? `<span class="hp-distance">목표에서 ${distance}개 연결</span><details><summary>이 기준까지의 연결 경로</summary>${path.map(recordLink).join('')}</details>` : `<span class="hp-distance">${code===target?'선택 목표':'순서 없는 의미 연결'}</span>`}<a class="hp-detail" href="${esc(standardURL(code))}">상세 분석 ↗</a></article>`;
 };
 const column = (label, codes, distances, paths) => `<section class="hp-column"><h3>${esc(label)} <small>${codes.length}</small></h3>${codes.map(c => card(c, distances?.get(c), paths?.get(c) || [])).join('')}</section>`;
 const levels = side => [...new Set(side.distances.values())].sort((a,b)=>a-b);
 const beforeLevels = levels(model.before).reverse(), afterLevels = levels(model.after);
 const codesAt = (side, level) => [...side.distances].filter(([,d])=>d===level).map(([c])=>c);
 const columns = [
  ...beforeLevels.map(d => column(`앞선 의미 · ${d}개 연결`, codesAt(model.before,d), model.before.distances,model.before.paths)),
  column('선택 목표', [target]),
  ...afterLevels.map(d => column(`이후 확장 · ${d}개 연결`, codesAt(model.after,d), model.after.distances,model.after.paths)),
 ].join('');
 const active = displayEdges.find(r => r.id === p.get('relation'));
 const related=[...new Set(context.flatMap(r=>[r.from.slice(9),r.to.slice(9)]))].filter(c=>c!==target);
 const relatedCards=related.length?`<section><h2>순서 없이 함께 살펴볼 기준</h2><div class="cp-node-grid">${related.map(c=>card(c,0,[])).join('')}</div></section>`:'';
 const evidence = active ? `<article class="cp-evidence" id="path-evidence"><h2>${esc(title(active.from.slice(9)))} ${ordered(active)?'→':'↔'} ${esc(title(active.to.slice(9)))}</h2><p>${esc(active.type==='requires_for_task'?'이 과제·경로의 필요 조건':active.type==='generalizes'?'기존 의미의 확장':'순서를 두지 않은 의미 연결')} · ${esc(active.id)}</p><h3>연결의 이유</h3><p>${esc(active.rationale)}</p><h3>적용 범위</h3><p>${esc(active.scope)}</p><h3>성립 조건</h3>${list(active.conditions)}${active.additional_learning?.length?'<h3>새로 필요한 사고</h3>'+list(active.additional_learning):''}${active.diagnostic?'<h3>확인 질문</h3><p>'+esc(active.diagnostic)+'</p>':''}${active.expected_response?'<h3>기대하는 설명</h3><p>'+esc(active.expected_response)+'</p>':''}${active.alternative_route?'<h3>다른 설명 경로</h3><p>'+esc(active.alternative_route)+'</p>':''}<h3>해석의 한계</h3><p>${esc(active.limit)}</p><h3>근거</h3>${sourcesHTML(graph.sources.filter(s=>(active.source_ids||[]).includes(s.id)))}${relationLiteratureHTML(active)}<p>위계 검토: ${esc(({unreviewed:'미검토',in_progress:'작성 중',self_checked:'자체 점검',independently_reviewed:'독립 검토',student_validated:'학생 반응 검증',deferred:'보류'})[active.hierarchy_review] || '미검토')} · 독립 검토 ${active.independent_review?'기록 있음':'전'} · 학생 반응 검증 ${active.student_validated?'기록 있음':'전'}</p></article>` : '<div class="cp-evidence"><h2>연결의 근거를 읽으세요</h2><p>카드의 연결 경로를 펼치거나 아래 관계를 선택하면 이유·조건·확인 질문을 볼 수 있습니다.</p></div>';
 return heading('LEARNING CONNECTIONS', title(target), '여러 단계의 앞선 의미와 이후 확장을 따라가며 각 연결의 조건을 확인하세요.')+
 `<div class="cp-actions"><a class="button" href="${esc(url('hierarchy',{mode:'tasks',target,scope}))}">과제·조건·대안 경로</a><a class="button" href="${esc(url('hierarchy',{scope}))}">← 전체 개념군</a><a class="button" href="${esc(route({mode:'expansion'}))}">직접 연결 보기</a></div><nav class="hp-depth" aria-label="연결 탐색 깊이">${[['1','직접 연결'],['2','2개 연결까지'],['3','3개 연결까지'],['all','끝까지 탐색']].map(([d,t])=>`<a class="button ${depth===d?'primary':''}" ${depth===d?'aria-current="page"':''} href="${esc(route({depth:d,relation:''}))}">${t}</a>`).join('')}</nav><p class="hp-guide">왼쪽에서 오른쪽으로 의미가 이어집니다. 거리는 관계 수이며 난이도나 필수 숙달 단계가 아닙니다. 다른 학교급의 조건도 경계 카드로 함께 보존합니다.</p><div class="hp-scroll" data-scroll-key="hierarchy-path" tabindex="0" role="region" aria-label="여러 단계의 성취기준 연결"><div class="hp-columns">${columns}</div></div>${decisionNote}${relatedCards}${!model.before.distances.size&&!decision?'<p class="cp-unknown">이 목표로 들어오는 방향 관계는 미기록 또는 미검토입니다. 직접 의미 연결에서도 관련 기준을 확인할 수 있습니다.</p>':''}${!model.after.distances.size&&!decision?'<p class="cp-unknown">이 목표 이후의 확장 방향은 미기록 또는 미검토입니다.</p>':''}${model.cycles.length?`<details><summary>순환 검토 대상 ${model.cycles.length}개 묶음</summary><p>순환에 속하는 기준에는 선후 단계를 부여하지 않았습니다.</p>${model.cycles.map(c=>'<p>'+c.map(code=>esc(code+' '+title(code))).join(' ↔ ')+'</p>').join('')}</details>`:''}<div class="cp-details"><section><h2>${decision?'선택 목표의 관련 기록':'이 경로에 기록된 관계'} ${displayEdges.length}개</h2>${displayEdges.map(recordLink).join('')}</section><aside>${evidence}</aside></div><p class="hp-guide">여러 화살표로 이어진 경로는 각 기록의 합성입니다. 과제별 조건의 필수성은 해당 과제에 한정되며, 경로 전체의 필수 선수성을 뜻하지 않습니다.</p>`;
}
