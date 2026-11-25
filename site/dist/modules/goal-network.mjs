import {catalog,standard,inScope,goalNetwork} from './store.mjs';
import {esc,url,heading,list} from './ui.mjs';

export function buildGoalNetwork(data){
 const goals=new Map(data.goals.map(g=>[g.id,g])),incoming=new Map(),outgoing=new Map(),next=new Map(),byCode=new Map(),caseRoutes=new Map();
 for(const g of goals.values()){
  incoming.set(g.id,[]);outgoing.set(g.id,[]);next.set(g.id,new Set());
  if(!byCode.has(g.code))byCode.set(g.code,[]);byCode.get(g.code).push(g);
 }
 for(const route of data.routes){
  if(!caseRoutes.has(route.case_id))caseRoutes.set(route.case_id,[]);caseRoutes.get(route.case_id).push(route);
  for(const id of route.goal_ids)incoming.get(id).push(route);
  const sources=new Set();
  for(const c of route.conditions){
   if(c.kind!=='goal')continue;
   if(!goals.has(c.goal_id))throw new Error('출발 목표의 자료를 확인할 수 없습니다.');
   sources.add(c.goal_id);
   for(const target of c.applies_to_goal_ids||route.goal_ids){
    if(!goals.has(target)||target===c.goal_id)throw new Error('목표 연결의 범위를 확인할 수 없습니다.');
    next.get(c.goal_id).add(target);
   }
  }
  for(const id of sources)outgoing.get(id).push(route);
 }
 return {data,goals,incoming,outgoing,next,byCode,caseRoutes};
}

const targetsOf=(route,source)=>[...new Set(route.conditions.filter(c=>c.kind==='goal'&&c.goal_id===source).flatMap(c=>c.applies_to_goal_ids||route.goal_ids))];
const adjacent=(model,a,b)=>model.next.get(a)?.has(b)||model.next.get(b)?.has(a);
export function goalTrace(model,raw,focus){
 const ids=String(raw||'').split('|').filter(Boolean);
 if(!ids.length)return [focus];
 if(ids.length>16||ids.at(-1)!==focus||new Set(ids).size!==ids.length||ids.some(id=>!model.goals.has(id)))return [focus];
 if(ids.some((id,i)=>i&&!adjacent(model,ids[i-1],id)))return [focus];
 return ids;
}
function nextTrace(trace,id){const i=trace.indexOf(id);return (i>=0?trace.slice(0,i+1):[...trace,id].slice(-16)).join('|');}

export function renderGoalNetwork(p,model){
 const scope=p.get('scope')||'all',code=p.get('target');
 const siblings=model.byCode.get(code)||[];
 const goal=siblings.find(g=>g.id===p.get('goal'))||siblings[0];
 if(!goal)return heading('GOAL PATHWAYS','목표별 위계','등록된 성취기준에서 목표를 다시 선택해 주세요.')+`<a class="button" href="${esc(url('hierarchy',{scope}))}">전체 목표에서 찾기</a>`;
 const item=standard(goal.code),trace=goalTrace(model,p.get('trace'),goal.id);
 const link=(id,extra={})=>url('hierarchy',{mode:'goals',target:model.goals.get(id).code,goal:id,scope,trace:adjacent(model,goal.id,id)?nextTrace(trace,id):id,...extra});
 const goalLink=id=>{
  const g=model.goals.get(id),s=standard(g.code),boundary=!inScope(s,scope);
  return `<a class="gn-goal-link${boundary?' is-boundary':''}" data-network-goal="${esc(id)}" href="${esc(link(id))}"><strong>${esc(g.title)}</strong><small>${esc(g.code)} · ${esc(s.level)} · ${esc(s.level==='고등학교'?s.subject:s.band)}${boundary?' · 선택 학교급 밖':''}</small></a>`;
 };
 const conditionLabels={within_task:'과제 안에서 구성·확인',task_assumption:'주어진 가정',entry_capability:'기초 출발 능력',goal:'다른 목표의 부분 수행'};
 const routeCard=(route,direction)=>{
  const affected=direction==='out'?targetsOf(route,goal.id):[goal.id],alternatives=model.caseRoutes.get(route.case_id).length;
  const taskLink=url('hierarchy',{mode:'tasks',target:route.standard,scope,taskCase:route.case_id,taskRoute:route.route_id,goal:affected[0]});
  return `<article class="gn-route" data-network-route="${esc(route.id)}"><header><small>${esc(route.standard)} · 과제 경로</small><h4>${esc(route.case_title)}</h4><p>${esc(route.title)}${alternatives>1?` · 대안 ${alternatives}개 중 하나`:''}</p></header>${direction==='out'?`<p class="gn-direction">이 수행을 사용하는 목표 ↓</p>${affected.map(goalLink).join('')}`:''}<details class="gn-conditions" ${direction==='in'?'open':''}><summary>이 경로의 전체 조건 · AND ${route.conditions.length}개</summary><h5>모든 대안에 공통인 조건</h5>${list(route.shared_conditions)}<h5>이 경로에서 함께 확인할 조건</h5><ul>${route.conditions.map(c=>{
   const applies=c.applies_to_goal_ids||route.goal_ids,matches=applies.includes(goal.id),uses=c.kind==='goal'&&c.goal_id===goal.id;
   return `<li class="${uses?'is-used-source':matches?'is-target-condition':'is-companion-condition'}"><p>${esc(c.text)}</p>${direction==='in'&&!matches?'<p class="gn-applies">이 조건은 이 과제의 다른 목표에 적용합니다.</p>':''}${c.kind==='goal'?goalLink(c.goal_id):`<small class="gn-kind">${esc(conditionLabels[c.kind])}</small>`}<p class="gn-reason">${esc(c.rationale)}</p>${applies.length!==1||applies[0]!==goal.id?`<p class="gn-applies">적용 목표: ${applies.map(id=>esc(model.goals.get(id).title)).join(' · ')}</p>`:''}</li>`;
  }).join('')}</ul></details><details class="gn-review"><summary>이 풀이를 다른 방법과 구분한 이유</summary><p>${esc(route.alternative_review)}</p></details><a class="text-link" href="${esc(taskLink)}">문제·풀이·학생에게 할 질문 보기 ↗</a></article>`;
 };
 const incoming=model.incoming.get(goal.id),outgoing=model.outgoing.get(goal.id);
 const cards=(routes,direction)=>routes.slice(0,3).map(r=>routeCard(r,direction)).join('')+(routes.length>3?`<details class="gn-more"><summary>나머지 ${routes.length-3}개 경로 펼치기</summary>${routes.slice(3).map(r=>routeCard(r,direction)).join('')}</details>`:'');
 const traceHTML=trace.length>1?`<nav class="gn-trace" aria-label="살펴본 목표 연결"><h2>지금까지 살펴본 목표</h2><ol>${trace.map((id,i)=>{const g=model.goals.get(id);return `<li>${i?`<span class="gn-trace-arrow" aria-label="${model.next.get(trace[i-1]).has(id)?'앞 목표에서 활용되는 방향':'출발 목표로 돌아가는 방향'}">${model.next.get(trace[i-1]).has(id)?'→':'←'}</span>`:''}<a href="${esc(link(id,{trace:trace.slice(0,i+1).join('|')}))}" ${id===goal.id?'aria-current="step"':''}><strong>${esc(g.title)}</strong><small>${esc(g.code)}</small></a></li>`;}).join('')}</ol><p>살펴본 연결의 기록입니다. 연결 하나를 따라왔다는 사실이 함께 필요한 다른 조건의 충족이나 학습 완료를 뜻하지 않습니다.</p></nav>`:'';
 return heading('GOAL PATHWAYS','목표별 위계','앞에서 사용하는 수행과 다음에 활용되는 과제를,선택한 목표를 중심으로 살펴보세요.')+
 `<div class="cp-actions"><a class="button" href="${esc(url('hierarchy',{scope}))}">전체 목표에서 찾기</a><a class="button" href="${esc(url('hierarchy',{mode:'tasks',target:goal.code,goal:goal.id,scope}))}">이 기준의 모든 과제</a><a class="button" href="${esc(url('hierarchy',{q:goal.code,scope}))}">개념별 연결 찾기</a><a class="button" href="${esc(url('standard',{code:goal.code,scope}))}">성취기준 상세</a></div>`+
 `<section class="gn-intro"><p><strong>${esc(model.data.coverage.standards)}개 성취기준 · ${esc(model.data.coverage.goals)}개 하위 목표</strong></p><p>${esc(model.data.interpretation)}</p><p>학교급을 바꾸어도 선택한 목표와 전체 경로 조건을 유지합니다. 학교급 밖의 출발 목표와 함께 필요한 조건도 표시합니다. 독립 검토·학생 반응 검증 전의 자체 설계입니다.</p></section>`+
 `<nav class="gn-siblings" aria-label="이 기준의 하위 목표">${siblings.map(g=>`<a href="${esc(url('hierarchy',{mode:'goals',target:goal.code,goal:g.id,scope}))}" ${g.id===goal.id?'aria-current="page"':''}>${esc(g.title)}</a>`).join('')}</nav>${traceHTML}`+
 `<div class="gn-lanes"><section class="gn-before"><h2>이 목표를 다룰 때 필요한 것 <span>${incoming.length}개 경로</span></h2>${cards(incoming,'in')}</section><section class="gn-focus"><p class="eyebrow">선택한 목표</p><p>${esc(item.level)} · ${esc(item.level==='고등학교'?item.subject:item.band)}${!inScope(item,scope)?' · 선택 학교급 밖':''}</p><h2>${esc(goal.title)}</h2><p class="meta">${esc(goal.code)}</p><blockquote>${esc(goal.official_span)}</blockquote><h3>확인할 수행</h3><p>${esc(goal.success)}</p><p>기초나 다음 목표를 누르면 그 목표를 중심으로 연결이 이어집니다.</p></section><section class="gn-after"><h2>이 수행을 활용하는 과제 <span>${outgoing.length}개 경로</span></h2>${outgoing.length?cards(outgoing,'out'):'<p class="gn-empty">이 원장에서 이 수행을 출발 조건으로 직접 참조한 후속 과제는 없습니다. 앞으로 활용되지 않거나 연결이 없다는 뜻은 아닙니다.</p>'}</section></div>`;
}

let lastData,lastModel;
export async function goalNetworkPage(p){
 const data=await goalNetwork();
 if(data!==lastData){lastData=data;lastModel=buildGoalNetwork(data);}
 return renderGoalNetwork(p,lastModel);
}
