import {catalog, band, conceptPathwaysIndex, standard, standardConnections, inScope, types} from './store.mjs';
import {esc, url} from './ui.mjs';

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
async function neighborhood(current, params, values, members) {
  const groups = groupNeighbors(await standardConnections(current.code), current);
  const trail = [...new Set((params.get('trail') || '').split(',').filter(c=>c!==current.code && standard(c)))];
  const visited = [...trail, current.code];
  // Prefer unexplored neighbors matching the chosen starting concept or band.
  const score = s => (trail.includes(s.code) ? 0 : 8) + (members?.has(s.code) ? 4 : 0)
    + (band(s) === values.band ? 2 : 0) + Number(s.domain === current.domain);
  groups.sort((a,b)=>score(b.target)-score(a.target) || a.target.code.localeCompare(b.target.code,'ko',{numeric:true}));
  const base = {...values, node:current.code, trail:trail.join(',')};
  const shown = listLimit(params, groups.length);
  const crumbs = visited.map((code,i)=>i===visited.length-1 ? `<span aria-current="step">${esc(current.title)}</span>`
    : `<a href="${link({...values,node:code,trail:trail.slice(0,i).join(',')})}">${esc(standard(code).title)}</a>`).join('<i aria-hidden="true">›</i>');
  return `<nav class="guide-trail" aria-label="살펴본 기준">${crumbs}</nav>
    <section class="guide-center"><small>지금 보는 기준 · ${esc(where(current))} · ${esc(current.code)}</small><h2>${esc(current.title)}</h2><p>${esc(current.statement)}</p>
    <a href="./${esc(url('standard',{scope:'all',code:current.code}))}">기준 상세 읽기 →</a></section>
    <h2>어떤 기준으로 이어질까요?</h2>
    ${groups.length ? `<p>직접 연결된 기준 ${groups.length}개 중 ${shown}개 · 이 사이트의 해설</p>
    <ol class="guide-branches">${groups.slice(0,shown).map(({target,records})=>{
      const seen = trail.indexOf(target.code);
      const next = seen<0 ? visited : trail.slice(0,seen);
      return `<li><small>${esc(where(target))} · ${esc(target.code)}</small><h3>${esc(target.title)}</h3>
        ${evidence(records[0])}${records.length>1 ? `<details><summary>다른 연결 이유 ${records.length-1}개</summary>${records.slice(1).map(evidence).join('')}</details>` : ''}
        <a class="guide-next" href="${link({...values,node:target.code,trail:next.join(',')})}">${seen<0?'여기서 한 단계 더 보기':'이전에 본 이 기준으로'} →</a></li>`;
    }).join('')}</ol>${more(base,shown,groups.length)}` : '<p>이 기준과 직접 이어진 성취기준이 아직 기록되지 않았습니다.</p>'}`;
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
  const current = standard(params.get('node'));
  const results = rows.filter(s=>(!grade||grade===band(s))&&(!members||members.has(s.code)));
  const content = current ? await neighborhood(current,params,values,members)
    : grade || concept || scope!=='all' ? startingList(results,params,values)
    : `<div class="guide-example"><span>바로 시작해 보기</span><a href="${link({scope:'all',concept:'fraction',node:'6수01-10'})}">초등 분수에서 이어지는 기준 →</a></div>`;
  return `<section class="guided-map"><header class="page-heading"><h1 tabindex="-1">연결 지도</h1><p>학년이나 개념을 고르고, 기준이 서로 이어지는 이유를 한 단계씩 살펴보세요.</p>
    <a class="guide-mode-link" href="${link({mapMode:'full',scope:'all'})}">435개 기준 전체 지도 보기 ↗</a></header>
    <div class="guide-pickers"><label>학년군·과목<select name="guide-band">${options([['','모든 학년군·과목'],...grades.map(g=>[g,g])],grade)}</select></label>
    <label>수학 개념<select name="guide-concept">${options([['','모든 개념'],...concepts.map(g=>[g.id,g.title])],concept?.id || '')}</select></label>
    ${(current||grade||concept)?`<a href="${link({scope:'all'})}">처음부터 보기</a>`:''}</div>
    <div class="guide-results">${content}</div></section>`;
}
export function mountGuidedMap(root) {
  const guide = root.querySelector('.guided-map');
  const form = root.querySelector('.guide-pickers');
  const abort = new AbortController();
  if (nextFocus?.hash === location.hash) {
    const target = guide.querySelector(nextFocus.selector);
    requestAnimationFrame(()=>requestAnimationFrame(()=>{
      if (!target?.isConnected) return;
      if (target.tabIndex < 0) target.tabIndex = -1;
      target.focus({preventScroll:true});
      target.scrollIntoView({block:'nearest'});
    }));
  }
  nextFocus = undefined;
  form.addEventListener('change', event=>{
    const hash = url('network',{scope:new URLSearchParams(location.hash.slice(1)).get('scope'),band:form.querySelector('[name=guide-band]').value,concept:form.querySelector('[name=guide-concept]').value});
    nextFocus = {hash,selector:'[name="'+event.target.name+'"]'};
    location.hash = hash;
  }, {signal:abort.signal});
  guide.addEventListener('click',event=>{
    if (event.button || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
    const anchor = event.target.closest('a');
    if (!anchor) return;
    if (anchor.matches('.guide-next, .guide-trail a, .guide-example a, .guide-starts a')) {
      nextFocus = {hash:anchor.hash, selector:'.guide-center h2'};
    } else if (anchor.matches('.guide-more')) {
      const starts = guide.querySelector('.guide-starts');
      const list = starts || guide.querySelector('.guide-branches');
      const index = list.children.length + 1;
      const selector = starts ? '.guide-starts li:nth-child('+index+') a' : '.guide-branches li:nth-child('+index+') > h3';
      nextFocus = {hash:anchor.hash, selector};
    }
  }, {signal:abort.signal});
  return ()=>abort.abort();
}
