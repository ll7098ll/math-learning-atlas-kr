import {catalog,conceptPathway,conceptPathwaysIndex,inScope,hierarchyGraph} from './store.mjs';
import {esc,url,heading,scopeSelect,standardURL,sourcesHTML,list,relationLiteratureHTML} from './ui.mjs';

export const reviewLabels={expansion_draft:'의미 확장·조건 기록',order_unreviewed:'직접 방향 미기록'};
export const reviewStateLabels={unreviewed:'미검토',in_progress:'작성 중',self_checked:'자체 점검',independently_reviewed:'독립 검토',student_validated:'학생 반응 검증',deferred:'보류'};
export function relationReviewHTML(r){
 const state=r.hierarchy_review||'unreviewed',label=reviewStateLabels[state]||reviewStateLabels.unreviewed;
 const history=r.review_history||[];
 return `<section class="cp-review-record" data-relation-review="${esc(state)}"><h3>이 관계의 위계 검토</h3><p>관계 자체 분석: ${esc(r.review_state==='self_checked'?'자체 분석 기록 있음':r.review_state==='candidate'?'후보':'이전 분석 초안')} · 아래 상태는 학습 선수성 검토 기록입니다.</p><p><strong>${esc(label)}</strong> · 독립 검토 ${r.independent_review?'기록 있음':'기록 없음'} · 학생 반응 검증 ${r.student_validated?'기록 있음':'기록 없음'}</p>${r.hierarchy_review_rationale?`<p>${esc(r.hierarchy_review_rationale)}</p>`:''}${history.length?`<details><summary>검토 범위와 이력 ${history.length}건</summary>${history.map(h=>`<p>${esc(h.date||'날짜 미기록')} · ${esc(h.reviewer||'검토자 미기록')}<br>${esc(h.scope||'범위 미기록')}${h.method?`<br>${esc(h.method)}`:''}</p>`).join('')}</details>`:''}<p class="cp-note">${state==='unreviewed'?'이 관계의 학습 선수성은 미검토입니다. ':state==='self_checked'?'기록한 과제와 적용 범위의 자체 점검입니다. ':''}교육과정 출처나 화살표만으로 모든 학생의 필수 학습 순서가 검증되는 것은 아닙니다.</p></section>`;
}
export function conceptNeighborhood(data,target){
 const ids=new Set(data.nodes.map(n=>n.id));
 const selected=ids.has(target)?target:data.concept.member_codes[0];
 const edges=data.relations.filter(r=>[r.from.slice(9),r.to.slice(9)].includes(selected));
 const before=new Set(),after=new Set(),related=new Set();
 for(const r of edges){const from=r.from.slice(9),to=r.to.slice(9),other=from===selected?to:from;
  if(r.order_role==='meaning_expansion'&&(r.type==='generalizes'||r.type==='requires_for_task')){
   if(to===selected)before.add(from);if(from===selected)after.add(to);
  }else related.add(other);
 }
 const conflicts=new Set([...before].filter(c=>after.has(c)||c===selected));
 for(const c of conflicts){before.delete(c);after.delete(c);related.add(c);}
 return {target:selected,edges,before,after,related,conflicts,reset:!!target&&target!==selected};
}

export function renderConceptPathway(p,data,index){
 const byCode=new Map(catalog.standards.map(s=>[s.code,s])),c={...data.concept};
 const scope=p.get('scope')||'all',mode=['expansion','meaning','position'].includes(p.get('mode'))?p.get('mode'):'expansion';
 const showExternal=p.get('external')==='1';
 const members=c.member_codes.filter(id=>inScope(byCode.get(id),scope));
 const allowed=new Set(showExternal?data.nodes.map(n=>n.id):data.nodes.filter(n=>inScope(byCode.get(n.id),scope)).map(n=>n.id));
 data={...data,nodes:data.nodes.filter(n=>allowed.has(n.id)),relations:data.relations.filter(r=>allowed.has(r.from.slice(9))&&allowed.has(r.to.slice(9)))};
 const expansions=data.relations.filter(r=>r.type==='generalizes'||r.type==='requires_for_task').length;
 Object.assign(c,{member_codes:members,members:members.length,relations:data.relations.length,expansions,hierarchy_status:expansions?'expansion_draft':'order_unreviewed'});
 if(!members.length)return heading('SCHOOL SCOPE',c.title,'선택 학교급에 직접 분류된 기준이 없습니다.')+`<a class="button" href="${url('hierarchy',{scope})}">개념군 목록으로</a>`;
 const wanted=p.get('target');
 if(wanted&&!allowed.has(wanted))return heading('SCHOOL SCOPE',c.title,'이전 목표가 선택한 학교급 범위 밖입니다. 목표를 다시 선택하세요.')+members.map(id=>`<a class="button" href="${url('hierarchy',{concept:c.id,target:id,scope})}">${esc(id+' '+byCode.get(id).title)}</a>`).join('');
 const n=conceptNeighborhood({...data,concept:{...c,member_codes:members}},wanted),goal=byCode.get(n.target);
 const route=changes=>url('hierarchy',{concept:c.id,target:n.target,scope,mode,external:showExternal?'1':'',...changes});
 const node=id=>{const s=byCode.get(id),boundary=!inScope(s,scope),member=c.member_codes.includes(id);return `<a class="cp-node ${id===n.target?'is-target':''} ${boundary?'is-boundary':''}" data-keep-scroll data-cp-node="${esc(id)}" href="${route({target:id,relation:''})}"><small>${esc(id)} · ${esc(s.level)}${boundary?' · 범위 밖':''}${member?'':' · 다른 개념군'}</small><strong>${esc(s.title)}</strong><span class="cp-status pending">목표·과제 ${esc(reviewStateLabels[data.nodes.find(n=>n.id===id)?.goal_analysis_review]||'미검토')} · 기존 연결 ${esc(reviewStateLabels[data.nodes.find(n=>n.id===id)?.hierarchy_review]||'미검토')}</span></a>`;};
 const lane=(title,ids,emptyText)=>`<section class="cp-lane"><h3>${title} <small>${ids.size}</small></h3>${ids.size?[...ids].map(node).join(''):`<p class="cp-unknown">${emptyText}</p>`}</section>`;
 const active=data.relations.find(r=>r.id===p.get('relation'));
 const edgeLink=r=>`<a class="cp-edge ${active?.id===r.id?'selected':''}" data-keep-scroll data-cp-relation="${esc(r.id)}" href="${route({relation:r.id})}"><span class="cp-status pending">${r.type==='requires_for_task'?'과제별 조건':r.type==='generalizes'?'의미 확장 초안':'연결 초안'} · ${esc(reviewStateLabels[r.hierarchy_review]||'미검토')}</span><strong>${esc(byCode.get(r.from.slice(9)).title)} ${['generalizes','requires_for_task'].includes(r.type)?'→':'↔'} ${esc(byCode.get(r.to.slice(9)).title)}</strong><small>${esc(r.id)} · ${esc(r.scope)}</small></a>`;
 let diagram;
 if(mode==='position')diagram=`<div class="cp-columns">${['초등학교','중학교','고등학교'].map(level=>lane(level,new Set(data.nodes.filter(x=>x.member&&byCode.get(x.id).level===level).map(x=>x.id)),'이 개념군에 직접 분류된 기준이 없습니다.')).join('')}</div><p class="cp-note">이 배치는 공식 학교급 위치입니다. 같은 열 안의 순서는 학습 선후를 뜻하지 않습니다.</p>`;
 else if(mode==='meaning')diagram=lane('선택 목표에 직접 연결된 기준',new Set(n.edges.map(r=>r.from.slice(9)===n.target?r.to.slice(9):r.from.slice(9))),'이 자료 범위에 직접 연결이 기록되지 않았습니다. 기초 개념이 없다는 뜻은 아닙니다.');
 else diagram=`<div class="cp-columns">${lane('앞에서 이어지는 의미',n.before,'이 목표로 들어오는 의미 확장은 미검토 또는 미기록 상태입니다. 선수 개념이 없다는 뜻은 아닙니다.')}<section class="cp-lane cp-goal ${n.before.size?'has-before':''} ${n.after.size?'has-after':''}"><h3>선택 목표</h3>${node(n.target)}<p>선택한 기준과 실제로 기록된 직접 확장을 보여줍니다. 다른 기준을 누르면 그 목표에서 다시 탐색합니다.</p></section>${lane('이후 의미 확장',n.after,'이 목표 이후의 확장 방향은 미검토 또는 미기록 상태입니다.')}</div>${n.related.size?`<details class="cp-related" open><summary>순서가 정해지지 않은 의미 연결 ${n.related.size}개</summary><div class="cp-node-grid">${[...n.related].map(node).join('')}</div></details>`:''}${n.conflicts.size?'<p class="cp-note">양방향 확장 기록이 있어 선후 관계를 정하지 않았습니다. 해당 관계는 검토 대상입니다.</p>':''}`;
 const decision=data.nodes.find(x=>x.id===n.target)?.order_decision;
 if(decision){diagram=diagram.replaceAll('이 목표로 들어오는 의미 확장은 미검토 또는 미기록 상태입니다. 선수 개념이 없다는 뜻은 아닙니다.','기록한 활동 범위에서는 고정된 선후를 두지 않았습니다.').replaceAll('이 목표 이후의 확장 방향은 미검토 또는 미기록 상태입니다.','다른 과제의 확장 방향은 별도로 검토합니다.');diagram=`<aside class="cp-evidence" data-order-decision><h2>검토한 범위에서는 순서를 두지 않았습니다</h2><p>${esc(decision.scope)}</p><p>${esc(decision.rationale)}</p></aside>`+diagram;}
 const explanation=active?`<article class="cp-evidence" id="concept-evidence" aria-live="polite"><span class="cp-status pending">${active.type==='generalizes'?'의미 확장':active.type==='requires_for_task'?'과제별 조건':'의미 연결'} · ${esc(reviewStateLabels[active.hierarchy_review]||'미검토')}</span><h2>${esc(byCode.get(active.from.slice(9)).title)} ${['generalizes','requires_for_task'].includes(active.type)?'→':'↔'} ${esc(byCode.get(active.to.slice(9)).title)}</h2><p class="meta">${esc(active.id)} · 원래 기록 상태: ${esc(active.status)}</p><div class="cp-actions"><a class="button" href="${route({target:active.from.slice(9),relation:active.id})}">출발 기준을 목표로</a><a class="button" href="${route({target:active.to.slice(9),relation:active.id})}">도착 기준을 목표로</a></div><h3>연결의 이유</h3><p>${esc(active.rationale)}</p><h3>적용 범위</h3><p>${esc(active.scope)}</p><h3>성립 조건</h3>${active.condition_scope_note?`<p>${esc(active.condition_scope_note)}</p>`:''}${list(active.conditions||[])}${active.additional_learning?.length?'<h3>새로 필요한 사고</h3>'+list(active.additional_learning):''}${active.diagnostic?'<h3>확인 질문</h3><p>'+esc(active.diagnostic)+'</p>':''}${active.expected_response?'<h3>기대하는 설명</h3><p>'+esc(active.expected_response)+'</p>':''}${active.alternative_route?'<h3>다른 설명 경로</h3><p>'+esc(active.alternative_route)+'</p>':''}<h3>해석의 한계</h3><p>${esc(active.limit)}</p><h3>근거와 실제 검토 범위</h3>${sourcesHTML(data.sources.filter(s=>(active.source_ids||[]).includes(s.id)))}${relationReviewHTML(active)}${relationLiteratureHTML(active)}</article>`:'<div class="cp-evidence"><h2>왜 연결되는지 확인하세요</h2><p>관계를 선택하면 기존 분석의 이유·조건·한계·출처를 읽을 수 있습니다. 모든 관계에 위계 검토 상태를 함께 표시합니다.</p></div>';
 const visibleEdges=mode==='expansion'?n.edges.filter(r=>r.type==='generalizes'||r.type==='requires_for_task'):n.edges;
 return heading('ALL CONCEPT PATHWAYS',c.title,'교육과정 전체에서 의미가 어떻게 이어지는지 살펴보고, 검토가 필요한 구간을 확인하세요.')+
 `<a class="button" href="${url('hierarchy',{scope})}">← 46개 전체 개념군</a><section class="cp-review"><span class="cp-status ${c.expansions?'draft':'pending'}">${reviewLabels[c.hierarchy_status]}</span><p>${esc(c.question)}</p><p><strong>${c.members}개 소속 기준 · ${c.relations}개 연결 기록 · ${c.expansions}개 방향 관계</strong></p><p>현재 표시 범위의 연결 기록: 자체 점검 ${data.relations.filter(r=>r.hierarchy_review==='self_checked').length}건 · 독립 검토 ${data.relations.filter(r=>r.independent_review).length}건 · 학생 반응 검증 ${data.relations.filter(r=>r.student_validated).length}건. 관계를 선택하면 개별 판정과 검토 범위를 확인할 수 있습니다. 하위 목표의 출발 조건과 후속 활용은 목표별 위계에서 살펴보세요.</p></section>
 <form class="cp-controls" data-filter="hierarchy"><label>개념군<select name="concept">${index.groups.map(g=>`<option value="${g.id}" ${g.id===c.id?'selected':''}>${esc(g.title)}</option>`).join('')}</select></label><label>목표 기준<select name="target">${data.nodes.map(x=>{const s=byCode.get(x.id);return `<option value="${x.id}" ${x.id===n.target?'selected':''}>${esc(x.id+' · '+s.title)}${x.member?'':' · 다른 개념군'}</option>`;}).join('')}</select></label><label><input type="checkbox" name="external" value="1" ${showExternal?'checked':''}>다른 학교급 연결 함께 보기</label><input type="hidden" name="mode" value="${mode}"><button class="button primary">적용</button></form>
 ${n.reset?'<p class="cp-note">이 개념군에 이전 목표가 없어 첫 소속 기준을 표시했습니다. 목표 기준에서 다른 대상을 선택할 수 있습니다.</p>':''}<nav class="cp-tabs" aria-label="개념군 보기">${[['goals','목표별 위계'],['tasks','과제·조건·대안 경로'],['path','여러 단계 연결'],['expansion','확장 위계 초안'],['meaning','직접 의미 연결'],['position','교육과정 위치']].map(([id,label])=>`<a href="${route({mode:id,relation:''})}" ${id===mode?'aria-current="page"':''}>${label}</a>`).join('')}</nav>
 <section class="cp-map" aria-label="${esc(c.title)} 연결과 위계">${diagram}</section>
 <div class="cp-actions"><a class="button" href="${standardURL(n.target)}">${esc(n.target)} 상세 분석 ↗</a><a class="button" href="${url('network',{node:n.target})}">전체 연결망에서 보기 ↗</a>${c.pilot_maps.map(id=>`<a class="button" href="${url('hierarchy',{map:id,scope})}">관련 과제별 시범 위계 ↗</a>`).join('')}</div>
 <div class="cp-details"><section><h2>선택 목표의 ${mode==='expansion'?'직접 확장':'직접 연결'} 근거 <small>${visibleEdges.length}</small></h2>${visibleEdges.map(edgeLink).join('')||(decision?'<p class="cp-unknown">기록한 활동 범위의 판정 이유와 직접 의미 연결을 함께 확인하세요.</p>':'<p class="cp-unknown">이 보기의 방향 관계는 미검토입니다. 직접 의미 연결 보기에서 다른 기록을 확인하세요.</p>')}</section><aside>${explanation}</aside></div>
 <details class="cp-all-expansions" data-open="expansions-${c.id}" ${c.expansions<=8?'open':''}><summary>이 개념군에 닿는 전체 방향 관계 기록 ${c.expansions}개</summary><div class="cp-node-grid">${data.relations.filter(r=>r.type==='generalizes'||r.type==='requires_for_task').map(edgeLink).join('')||'<p class="cp-unknown">확장 방향은 미검토입니다. 교육과정 위치와 직접 의미 연결은 탐색할 수 있습니다.</p>'}</div></details><details class="cp-members" data-open="members-${c.id}"><summary>이 개념군의 ${c.members}개 기준과 검토 상태 모두 보기</summary><div class="cp-node-grid">${c.member_codes.map(node).join('')}</div></details>
 <p class="cp-note">이 지도는 이 개념군에 직접 닿는 기록 범위입니다. 선택 학교급 내부 관계를 표시합니다. 다른 학교급의 연결은 별도 선택으로 펼칠 수 있습니다. 선이 없는 구간은 위계가 확정된 기초 단계가 아닙니다.</p>`;
}

export async function conceptPathwayPage(p){const [data,index]=await Promise.all([conceptPathway(p.get('concept')),conceptPathwaysIndex()]);if(p.get('mode')==='path'){const [{renderHierarchyPaths},graph]=await Promise.all([import('./hierarchy-path-view.mjs'),hierarchyGraph()]);return renderHierarchyPaths(p,data,index,graph);}return renderConceptPathway(p,data,index);}
