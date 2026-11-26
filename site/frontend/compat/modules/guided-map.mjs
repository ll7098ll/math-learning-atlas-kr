import {catalog, band, conceptPathwaysIndex, standard, standardRelations, inScope, types} from './store.mjs';
import {esc, url} from './ui.mjs';
import {drawWalk,extendWalk,readWalk,traversed} from './walk-map.mjs';

const pageSize = 3;
let nextFocus;
function link(values) {
  return esc(url('network', values));
}
function options(rows, selected) {
  return rows.map(([key, label]) => `<option value="${esc(key)}" ${key === selected ? 'selected' : ''}>${esc(label)}</option>`).join('');
}
function listLimit(params, total) {
  const count = Number(params.get('show'));
  return Number.isSafeInteger(count) ? Math.min(total, Math.max(pageSize, count)) : Math.min(total, pageSize);
}
function where(s) {
  return s.level + ' · ' + band(s);
}
function more(values, visible, total) {
  if (visible >= total) return '';
  const next = Math.min(pageSize, total - visible);
  return `<a class="guide-more" href="${link({...values, show: visible + next})}">다음 ${next}개 더 보기 <small>(${visible}/${total})</small></a>`;
}
function startingList(rows, params, values) {
  const shown = listLimit(params, rows.length);
  return `<h2>어느 기준에서 시작할까요?</h2>${rows.length ? `<ul class="guide-starts">${rows.slice(0, shown).map(s => `<li><a href="${link({...values, node:s.code})}"><small>${esc(where(s))} · ${esc(s.code)}</small><strong>${esc(s.title)}</strong><span>연결 보기 →</span></a></li>`).join('')}</ul>${more(values, shown, rows.length)}` : '<p>두 조건에 모두 맞는 기준이 없습니다. 학년군이나 개념을 바꿔 보세요.</p>'}`;
}
function groupNeighbors(data, current) {
  const groups = new Map();
  const id = 'standard:' + current.code;
  for (const record of data.relations) {
    const other = record.from === id ? record.to : record.to === id ? record.from : '';
    if (!other.startsWith('standard:') || other === id) continue;
    const target = standard(other.slice(9));
    if (!target) continue;
    if (!groups.has(target.code)) groups.set(target.code, {target, records:[]});
    groups.get(target.code).records.push(record);
  }
  return [...groups.values()];
}
function evidence(record) {
  const from = standard(record.from.slice(9)), to = standard(record.to.slice(9));
  return `<p class="guide-direction">${esc(from.title)} · ${esc(to.title)} <b>${esc(types[record.type] || record.type)}</b></p>
    <p>${esc(record.rationale)}</p><details><summary>어디에 적용되는 연결인가요?</summary>
    <p>${esc(from.code)}에서 ${esc(to.code)}로 기록한 연결 · ${esc(record.id)}</p>
    ${record.scope ? `<p>${esc(record.scope)}</p>` : ''}
    ${record.conditions?.length ? `<ul>${record.conditions.map(c=>`<li>${esc(c)}</li>`).join('')}</ul>` : ''}
    ${record.limit ? `<p>${esc(record.limit)}</p>` : ''}</details>`;
}
const layouts = [
  [],
  [[50,18]],
  [[50,18],[24,74]],
  [[50,18],[24,74],[76,74]],
];

function reasonPanel(i,title,records) {
  return `<section class="local-reason" id="local-reason-${i}" hidden><small>연결 이유 · 이 사이트의 해설</small>
    <h3 tabindex="-1">${esc(title)}</h3>${evidence(records[0])}
    ${records.length>1?`<details><summary>다른 연결 이유 ${records.length-1}개</summary>${records.slice(1).map(evidence).join('')}</details>`:''}
    <button type="button" class="local-back">지도로 돌아가기</button></section>`;
}
function localDiagram(current, neighbors, walk, values) {
  const positions = layouts[neighbors.length];
  const edges = [], nodes = [], reasons = [];
  for (const [i, {target, records}] of neighbors.entries()) {
    const [x,y] = positions[i];
    const midX = (50+x)/2+'%', midY = (50+y)/2+'%';
    const ends = `x1="50%" y1="50%" x2="${x}%" y2="${y}%"`;
    edges.push(`<g class="local-edge" data-edge-index="${i}" role="button" tabindex="0" aria-label="${esc(target.title)}와 연결되는 이유" aria-expanded="false" aria-controls="local-reason-${i}">
      <line class="edge-hit" ${ends}/><line class="edge-ink" ${ends}/>
      <circle class="edge-hit-disc" cx="${midX}" cy="${midY}" r="22"/></g>`);
    nodes.push(`<a class="guide-next" href="${link({...values,node:target.code,walk:extendWalk(walk,current.code,target.code)})}" style="--x:${x}%;--y:${y}%" data-slot="${i}" title="${esc(target.title)} · ${esc(target.code)}" aria-label="${esc(target.title)}, ${esc(band(target))}. 여기서 연결 펼치기">
      <i class="local-dot" aria-hidden="true"></i><span><small>${esc(band(target))}</small><strong>${esc(target.title)}</strong></span></a>`);
    reasons.push(reasonPanel(i,target.title,records));
  }
  return {panels:reasons.join(''),choices:neighbors.map(({target},index)=>({index,title:target.title})),board:`<div class="local-board" role="group" aria-label="${esc(current.title)} 주변 연결 지도">
    <svg class="local-lines" width="100%" height="100%" aria-label="연결 이유를 여는 선">${edges.join('')}</svg>
    <button type="button" class="local-center" aria-controls="local-standard" aria-label="${esc(current.title)} 기준 설명">
      <i class="local-dot" aria-hidden="true"></i><span><small>중심 기준</small><strong>${esc(current.title)}</strong></span></button>
    ${nodes.join('')}</div>`};
}

async function neighborhood(current, params, values, members, example) {
  const [records,walk] = await Promise.all([standardRelations(current.code),readWalk(params,current.code)]);
  const groups=groupNeighbors(records,current).filter(g=>inScope(g.target,values.scope)&&!traversed(walk,current.code,g.target.code));
  const following=walk.edges.length>0;
  // Prefer unexplored neighbors matching the chosen starting concept or band.
  const score = s => (walk.codes.includes(s.code) ? 0 : 8) + (members?.has(s.code) ? 4 : 0)
    + (band(s) === values.band ? 2 : 0) + Number(s.domain === current.domain);
  groups.sort((a,b)=>score(b.target)-score(a.target) || a.target.code.localeCompare(b.target.code,'ko',{numeric:true}));
  const base = {...values, node:current.code, walk:following?walk.encoded:undefined};
  const lastPage = Math.max(0, Math.ceil(groups.length / pageSize)-1);
  const requested = Number(params.get('page') || Math.ceil(listLimit(params,groups.length)/pageSize)-1);
  const page = Number.isSafeInteger(requested) ? Math.min(lastPage, Math.max(0,requested)) : 0;
  const start = page*pageSize;
  const neighbors = groups.slice(start,start+pageSize);
  const diagram=following?drawWalk(walk,current,neighbors,values,reasonPanel):localDiagram(current,neighbors,walk,values);
  const paging = groups.length ? `<nav class="local-paging" aria-label="주변 기준 바꾸기">
      ${page>0?`<a href="${link({...base,page:page-1})}">← 이전 연결</a>`:''}
      <span>주변 기준 ${start+1}–${start+neighbors.length} / ${groups.length}개</span>
      ${page<lastPage?`<a href="${link({...base,page:page+1})}">다른 연결 보기 →</a>`:''}</nav>` : '<p>이 점에서 더 펼칠 연결이 없습니다.</p>';
  return `<h2 class="local-title" tabindex="-1">${following?'내가 따라온 길':example?'분수로 지도 둘러보기':esc(current.title)+' 주변 지도'}</h2>
    ${diagram.location||''}
    <p class="local-instructions">점을 누르면 그 기준에서 길이 이어집니다. 선을 누르면 연결 이유가 열립니다.</p>
    <div class="walk-actions">${following?`<div class="walk-key">${diagram.routeLength>1?'<span class="key-path">현재 위치까지 온 길</span>':''}${walk.edges.length>=diagram.routeLength?'<span class="key-other">살펴본 다른 길</span>':''}${neighbors.length?'<span class="key-next">더 가볼 길</span>':''}</div>`:''}
    ${diagram.choices.length?`<details class="reason-picker"><summary>연결 이유 보기</summary><p>지금 보는 기준과 어떤 기준의 연결을 살펴볼까요?</p>
      ${diagram.choices.map(c=>`<button type="button" data-explain="local-reason-${c.index}" aria-controls="local-reason-${c.index}">${esc(c.title)}</button>`).join('')}</details>`:''}</div>
    <div class="local-layout"><div>${diagram.board}${paging}</div><aside class="local-inspector" aria-label="선택한 기준과 연결 설명">
    <section id="local-standard"><small>지금 보는 기준 · ${esc(where(current))}</small><h3 tabindex="-1">${esc(current.title)}</h3>
    <p>${esc(current.statement)}</p><small>${esc(current.code)} · 교육과정 원문</small>
    <a href="./${esc(url('standard',{scope:'all',code:current.code}))}">기준 상세 읽기 →</a></section>${diagram.panels}</aside></div>`;
}
export async function guidedMap(params) {
  const scope = params.get('scope') || 'all';
  const rows = catalog.standards.filter(s=>inScope(s,scope));
  const {groups} = await conceptPathwaysIndex();
  const grades = [...new Set(rows.map(band))];
  const grade = grades.includes(params.get('band')) ? params.get('band') : '';
  const available = new Set(rows.map(s=>s.code));
  const concepts = groups.filter(g=>g.member_codes.some(c=>available.has(c)));
  const concept = concepts.find(g=>g.id===params.get('concept'));
  const members = concept && new Set(concept.member_codes);
  const values = {scope,band:grade,concept:concept?.id};
  const requested = standard(params.get('node'));
  const current = inScope(requested,scope) ? requested : null;
  const results = rows.filter(s=>(!grade||grade===band(s))&&(!members||members.has(s.code)));
  const example = !current && !grade && !concept && scope === 'all';
  const content = current || example
    ? await neighborhood(current || standard('6수01-10'),params,values,members,example)
    : startingList(results,params,values);
  const selected = current || (example ? standard('6수01-10') : null);
  const resume = current ? new URLSearchParams({...Object.fromEntries(params), scope, node:current.code}).toString() : undefined;
  const fullLink = targetScope => link({mapMode:'full',scope:targetScope,node:selected?.code,resume});
  return `<section class="guided-map"><header class="page-heading"><h1 tabindex="-1">연결 지도</h1><p>학년이나 개념을 고르고, 기준이 서로 이어지는 이유를 한 단계씩 살펴보세요.</p>
    <a class="guide-mode-link" href="${fullLink(scope)}">${scope==='all'?'435개 기준 전체 지도 보기':'선택한 학교급의 전체 연결망 보기'} ↗</a>
    ${scope==='all'?'':`<a class="guide-mode-link" href="${fullLink('all')}">435개 기준 전체 지도 보기 ↗</a>`}</header>
    ${current?'<details class="local-picker-fold"><summary>학년이나 개념 다시 고르기</summary>':''}
    <div class="guide-pickers"><label>학년군·과목<select name="guide-band">${options([['','모든 학년군·과목'],...grades.map(g=>[g,g])],grade)}</select></label>
    <label>수학 개념<select name="guide-concept">${options([['','모든 개념'],...concepts.map(g=>[g.id,g.title])],concept?.id || '')}</select></label>
    ${(current||grade||concept)?`<a href="${link({scope:'all'})}">처음부터 보기</a>`:''}</div>
    ${current?'</details>':''}<div class="guide-results">${content}</div></section>`;
}
export function mountGuidedMap(root) {
  const guide = root.querySelector('.guided-map');
  const form = root.querySelector('.guide-pickers');
  const abort = new AbortController();
  const board=guide.querySelector('.walk-board');
  function locate(selector,focus=false){
    const dot=board?.querySelector(selector);
    if(!dot)return;
    const rect=dot.getBoundingClientRect(), frame=board.getBoundingClientRect();
    board.scrollLeft+=rect.left+rect.width/2-frame.left-frame.width/2;
    board.scrollTop+=rect.top-frame.top-frame.height*.42;
    if(focus)dot.focus({preventScroll:true});
  }
  if(board)requestAnimationFrame(()=>{if(board.isConnected)locate('.walk-active');});
  if (nextFocus?.hash === location.hash) {
    const target = guide.querySelector(nextFocus.selector);
    requestAnimationFrame(()=>requestAnimationFrame(()=>{
      if (!target?.isConnected) return;
      if (target.tabIndex < 0) target.tabIndex = -1;
      target.focus({preventScroll:true});
      target.scrollIntoView({block:target.matches('.local-title')?'start':'nearest'});
    }));
  }
  nextFocus = undefined;
  form.addEventListener('change', event=>{
    const hash = url('network',{scope:new URLSearchParams(location.hash.slice(1)).get('scope'),band:form.querySelector('[name=guide-band]').value,concept:form.querySelector('[name=guide-concept]').value});
    nextFocus = {hash,selector:'[name="'+event.target.name+'"]'};
    location.hash = hash;
  }, {signal:abort.signal});
  let reasonTrigger;
  function openPanel(edge,trigger=edge) {
    reasonTrigger=trigger;
    const id = edge?.getAttribute('aria-controls') || 'local-standard';
    for (const panel of guide.querySelectorAll('.local-inspector > section')) panel.hidden = panel.id !== id;
    for (const item of guide.querySelectorAll('.local-edge')) item.setAttribute('aria-expanded',String(item === edge));
    const heading = guide.querySelector('#'+id+' h3');
    heading.focus({preventScroll:true});
    heading.scrollIntoView({block:matchMedia('(max-width:760px)').matches?'start':'nearest'});
  }
  guide.addEventListener('keydown',event=>{
    if (event.target.matches('.local-edge') && ['Enter',' '].includes(event.key)) {
      event.preventDefault();
      openPanel(event.target);
    }
  },{signal:abort.signal});
  guide.addEventListener('click',event=>{
    if (event.button || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
    const option=event.target.closest('[data-explain]');
    if(option){
      openPanel(guide.querySelector('.local-edge[aria-controls="'+option.dataset.explain+'"]'),option);
      return;
    }
    const edge = event.target.closest('.local-edge');
    const jump=event.target.closest('[data-locate]');
    if(jump){
      locate(jump.dataset.locate==='origin'?'[data-origin]':'.walk-active',true);
      return;
    }
    if (edge || event.target.closest('.local-center,.walk-active')) {
      openPanel(edge);
      return;
    }
    if (event.target.closest('.local-back')) {
      const active = reasonTrigger;
      openPanel(null);
      active?.focus();
      return;
    }
    const anchor = event.target.closest('a');
    if (!anchor) return;
    if (anchor.matches('.guide-next, .walk-dot, .walk-location a, .guide-starts a, .local-paging a')) {
      nextFocus = {hash:anchor.hash, selector:'.local-title'};
    } else if (anchor.matches('.guide-more')) {
      const starts = guide.querySelector('.guide-starts');
      const index = starts.children.length + 1;
      const selector = '.guide-starts li:nth-child('+index+') a';
      nextFocus = {hash:anchor.hash, selector};
    }
  }, {signal:abort.signal});
  return ()=>abort.abort();
}
