import {catalog,levels,categories,band,select,inScope} from './store.mjs';
import {esc,url,heading,uniq,standardRow,scopeSelect,options,domainBadge,empty,overviewModes} from './ui.mjs';
import {flowOverview} from './flows.mjs';
import {catalogGroups} from './catalog-groups.mjs';
export function overview(p){
 if(p.get('mode')==='flow'||(!p.has('mode')&&!p.has('density')&&!p.has('scope')&&!p.has('q')&&!p.has('focus')))return flowOverview(p);
 const items=select(p),expanded=p.get('density')==='expanded',q=p.get('q')||'';
 return heading('CURRICULUM ATLAS','초등에서 고등까지, 수학의 전체 모습','학년군과 과목을 펼쳐 성취기준의 위치와 내용을 함께 살펴보세요.',`<a class="text-link" href="${url('catalog')}">성취기준 찾기로 →</a>`)+
 overviewModes(expanded?'expanded':'structure')+`<form class="overview-toolbar" data-filter="overview"><div class="search-input"><span aria-hidden="true">⌕</span><input name="q" type="search" value="${esc(q)}" placeholder="개념, 원문 또는 코드 검색" aria-label="전체 조망 검색"></div>${scopeSelect(p.get('scope')||'all')}<button class="button primary">검색</button><input type="hidden" name="mode" value="structure"><input type="hidden" name="density" value="${expanded?'expanded':''}"></form>`+
 `<div class="overview-caption"><span>전체 <b>435</b>개${items.length!==435?` · 현재 <b>${items.length}</b>개`:' 성취기준'} · 고등학교 15과목</span><span>2022 개정 · 제공 판본 기준 <a href="${url('about')}">자료 범위 ↗</a></span>${p.get('scope')&&p.get('scope')!=='all'||q?`<a href="${url('overview',{mode:'structure'})}">전체로 돌아가기</a>`:''}</div>`+
 (items.length?`<div class="overview-grid ${expanded?'is-expanded':''} ${levels.filter(l=>inScope({level:l},p.get('scope'))).length===1?'single-school':levels.filter(l=>inScope({level:l},p.get('scope'))).length===2?'two-schools':''}">${levels.filter(l=>inScope({level:l},p.get('scope'))).map(level=>{const i=levels.indexOf(level);
 const all=catalog.standards.filter(s=>s.level===level),ss=items.filter(s=>s.level===level),isHigh=i===2;
 return `<section class="school-column school-${i}"><header class="school-heading"><div class="school-icon">${['01','02','03'][i]}</div><div><h2>${level}</h2><p>${all.length}개 기준${ss.length!==all.length?` · 검색 ${ss.length}개`:''}</p></div></header>${isHigh?
 categories.map(cat=>`<section class="course-category"><h3>${cat}<small>${all.filter(s=>s.category===cat).length}개</small></h3>${uniq(all.filter(s=>s.category===cat).map(s=>s.subject)).map(subject=>{const matches=ss.filter(s=>s.subject===subject);return `<details class="course-block" data-open="${esc(subject)}" ${expanded?'open':''}><summary><strong>${esc(subject)}</strong><span>${matches.length}개 <b>＋</b></span></summary>${subject.startsWith('기본')?'<p class="course-note">같은 번호의 공통수학 대체 이수 과목</p>':''}${groupRows(matches,expanded,subject)}</details>`;}).join('')}</section>`).join(''):
 uniq(all.map(band)).map(b=>`<section class="band-block"><header><h3>${esc(b)}</h3><a href="${url('catalog',{scope:i===0?'e':'m',band:b})}">${all.filter(s=>band(s)===b).length}개 기준 →</a></header>${groupRows(ss.filter(s=>band(s)===b),expanded,b)}</section>`).join('')}
 </section>`;
 }).join('')}</div>`:empty('일치하는 성취기준이 없습니다.'))+
 `<section class="concept-entry"><div><p class="eyebrow">한 개념을 더 깊이 읽기</p><h2>개념은 어떻게 이어질까요?</h2><p>서로 다른 풀이 경로와 그 경로에서 필요한 사고를 살펴보세요.</p></div><div class="concept-links">${[['fraction','나눗셈과 분수','등분과 단위의 구성'],['ratio','비율과 함수','불변량과 공변 관계'],['area','넓이와 도형','분해·이동·복제']].map(([id,t,desc])=>`<a href="${url('hierarchy',{map:id})}"><strong>${t} <span>↗</span></strong><small>${desc}</small></a>`).join('')}</div></section>`;
}
function groupRows(items,expanded,key){
 if(!items.length)return '<p class="no-match">검색 결과 없음</p>';
 return uniq(items.map(s=>s.domain)).map(d=>{const ss=items.filter(s=>s.domain===d);return `<details class="domain-group" data-open="${esc(key+'|'+d)}" ${expanded?'open':''}><summary>${domainBadge(d)}<span>${ss.length} <b>⌄</b></span></summary>${expanded?'':`<p class="group-preview">${ss.slice(0,3).map(s=>esc(s.title)).join(' · ')}${ss.length>3?' 외':''}</p>`}<div class="compact-standards">${ss.map(s=>standardRow(s)).join('')}</div></details>${!expanded?`<p class="domain-preview">${ss.slice(0,2).map(s=>esc(s.title)).join(' · ')}${ss.length>2?' …':''}</p>`:''}`;}).join('');
}
export function catalogPage(p){
 const items=select(p),scope=p.get('scope')||'all',scoped=catalog.standards.filter(s=>inScope(s,scope));
 const full=p.get('display')!=='compact';
 return heading('FIND A STANDARD','성취기준 찾기','학년군과 과목 안에서 영역별 성취기준을 살펴보고, 코드·원문·개념으로 검색하세요.')+
 `<form class="catalog-filters" data-filter="catalog"><div class="search-input"><span aria-hidden="true">⌕</span><input type="search" name="q" value="${esc(p.get('q')||'')}" placeholder="예: 분수, 변화율, 6수02-03" aria-label="성취기준 검색"></div><button class="button primary">검색</button><div class="filter-row">${scopeSelect(scope)}<label>학년군 · 과목<select name="band">${options(uniq(scoped.map(band)),p.get('band'),'전체 학년군·과목')}</select></label><label>내용 영역<select name="domain">${options(uniq(scoped.filter(s=>!p.get('band')||band(s)===p.get('band')).map(s=>s.domain)),p.get('domain'),'모든 영역')}</select></label><a class="text-link" href="${url('catalog')}">초기화</a></div><input type="hidden" name="display" value="${full?'full':'compact'}"></form>`+
 `<div class="results-heading"><h2>${p.get('q')?`“${esc(p.get('q'))}” 검색 결과`:'선택한 범위의 성취기준'} <span>${items.length}개</span></h2><a class="text-link" href="${url('catalog',{...Object.fromEntries(p),display:full?'compact':'full'})}">${full?'간단히 보기':'원문 함께 보기'}</a></div>`+
 (items.length?catalogGroups(p,items,full):empty('조건에 맞는 성취기준이 없습니다.'));
}
