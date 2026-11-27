import {pathForStandard} from './pathways.mjs';
import {catalog,standard,detail,standardConnections,hierarchy,conceptPathwaysIndex,relationGroups,types,band,inScope} from './store.mjs';
import {esc,url,heading,standardURL,standardRow,domainBadge,pill,list,markdown,empty,sourcesHTML} from './ui.mjs';
import {analysisSections} from './analysis-sections.mjs';
export async function standardPage(p){
 const code=p.get('code'),s=standard(code);if(!s)return empty('등록되지 않은 성취기준입니다.','주소의 성취기준 코드를 확인하거나 교육과정 탐색에서 찾아보세요.');
 const [a,data,pilotData,conceptIndex]=await Promise.all([detail(code),standardConnections(code),hierarchy(),conceptPathwaysIndex()]);
 if(a.schemaVersion===2)return revisedStandardPage(s,a,p,data,conceptIndex);
 const groups=relationGroups(data.relations,code),pilot=pilotData.hierarchy.maps.filter(m=>m.standards.includes(code));
 let returnTo='#view=overview';try{returnTo=sessionStorage.getItem('atlas-return')||returnTo;}catch{}
 const sections=[['meaning','핵심 의미'],['thinking','사고와 수행'],['task','과제와 경로'],['diagnosis','진단 질문'],['connections','관련 성취기준'],['references','출처와 검토']];
 const referenced=new Set([s.sourceId,...groups.flatMap(g=>g.records.flatMap(r=>r.source_ids||[]))]);
 const conditions=data.relations.filter(r=>r.type==='requires_for_task'&&r.to==='standard:'+code);
 const supplement=a.sections.filter(x=>!/교육과정과 목표|수학적 의미|하위요소|진단|경로|수행 과정|연결|다음 조사|검토 상태/.test(x.title));
 return `<nav class="breadcrumbs" aria-label="교육과정 위치"><a href="${url('catalog')}">교육과정 탐색</a><span>/</span><a href="${url('catalog',{scope:{초등학교:'e',중학교:'m',고등학교:'h'}[s.level]})}">${esc(s.level)}</a><span>/</span><a href="${url('catalog',{band:band(s)})}">${esc(band(s))}</a><span>/</span><span>${esc(s.domain)}</span></nav>`+
 `<header class="standard-header"><div class="standard-topline">${domainBadge(s.domain)}${pill(s.code,'code-tag')}${pill('분석 '+a.status)}</div><h1 tabindex="-1">${esc(s.title)}</h1><p class="title-note">성취기준을 설명하는 분석 제목</p><div class="official-statement"><span class="label">공식 성취기준</span><p>${esc(s.statement)}</p><a href="curriculum.pdf#page=${s.pdfPages[0]}" target="_blank" rel="noopener">교육과정 PDF ${s.pdfPages.join(', ')}쪽 ↗</a></div><button class="button screen-only" type="button" data-print>인쇄</button></header>`+
 `<nav class="reading-jumps screen-only" aria-label="상세 분석 목차">${sections.map(([id,t])=>`<a href="${url('standard',{code,section:id})}" data-section="${id}">${t}</a>`).join('')}</nav>
 <div class="reading-layout"><article class="reading-body">
 <section id="meaning" class="reading-section"><p class="section-index">01 · UNDERSTANDING</p><h2>핵심 의미</h2><p class="key-meaning">${esc(a.idea)}</p><p class="muted">${esc(a.limit)}</p>${s.level==='고등학교'&&s.subject.startsWith('기본')?'<aside class="notice">같은 번호의 공통수학을 대체하여 이수하는 과목입니다.</aside>':''}${a.sourceNotes.length?`<aside class="source-note"><strong>교육과정의 적용 범위 메모</strong>${a.sourceNotes.map(n=>`<p>${esc(n.scope_note)} <a href="curriculum.pdf#page=${n.pdf_page}" target="_blank" rel="noopener">PDF ${n.pdf_page}쪽 ↗</a></p>`).join('')}</aside>`:''}</section>
 <section id="thinking" class="reading-section"><p class="section-index">02 · THINKING</p><h2>사고 요소와 관찰할 수행</h2><p class="muted">목표를 구성하는 사고입니다. 아래 순서가 필수 학습 순서를 뜻하지는 않습니다.</p><div class="thinking-list">${a.stepObjects.map((step,i)=>`<div class="thinking-step"><span>${String(i+1).padStart(2,'0')}</span><div><h3>${esc(step.label)}</h3><p>${esc(step.meaning)}</p>${step.observable?`<p><b>관찰할 수행</b> ${esc(step.observable)}</p>`:''}${step.conditions?`<p class="muted">경로의 조건 · ${esc(step.conditions)}</p>`:''}</div></div>`).join('')}</div>${a.elements.length?`<details class="further"><summary>연결된 사고 요소 ${a.elements.length}개 더 읽기</summary>${a.elements.map(e=>`<div class="source-block"><h3>${esc(e.label)}</h3><p>${esc(e.observable)}</p></div>`).join('')}</details>`:''}</section>
 <section id="task" class="reading-section"><p class="section-index">03 · TASK & PATHWAYS</p><h2>대표 과제와 풀이 경로</h2>${a.task?`<div class="task-box"><span class="label">대표 과제</span>${esc(a.task).split('\n\n').map(t=>`<p>${t}</p>`).join('')}</div>`:'<p>구체적인 과제는 아래 경로에서 함께 읽습니다.</p>'}${a.paths.map((path,i)=>`<div class="path-block"><span class="path-number">경로 ${i+1}</span><div class="prose">${markdown(Array.isArray(path)?path.join(' · '):path)}</div></div>`).join('')}${conditions.length?`<details class="further"><summary>과제별 선수 조건과 함께 필요한 사고</summary>${conditions.map(r=>`<div class="source-block"><h3>${esc(a.elements.find(e=>'element:'+e.id===r.from)?.label||r.scope)}</h3><p>${esc(r.rationale)}</p>${list(r.conditions)}${r.prerequisite_group?`<p><b>${esc(r.prerequisite_group.operator)} · 함께 필요한 조건 묶음</b></p>${list(r.prerequisite_group.members.map(id=>a.elements.find(e=>'element:'+e.id===id)?.label||id))}`:''}<p class="muted">${esc(r.limit)} · ${esc(r.status)}</p></div>`).join('')}</details>`:''}${a.profile.representations?.length?`<details class="further"><summary>공통 관점의 표현 연결</summary>${list(a.profile.representations)}</details>`:''}</section>
 <section id="diagnosis" class="reading-section"><p class="section-index">04 · QUESTIONS</p><h2>진단 질문과 예상 반응</h2><p class="muted">정답과 설명을 함께 살펴보는 질문입니다. 다른 반응의 해석은 후속 발문으로 확인합니다.</p><div class="probe-list">${a.probeObjects.map((probe,i)=>`<article class="probe"><header><span>Q${String(i+1).padStart(2,'0')}</span><h3>${esc(probe.question)}</h3></header><dl><div><dt>기대하는 설명</dt><dd>${esc(probe.expected)}</dd></div>${probe.interpretation?`<div><dt>반응의 가능한 해석</dt><dd>${esc(probe.interpretation)}</dd></div>`:''}${probe.followup?`<div class="followup"><dt>후속 질문과 발문</dt><dd>${esc(probe.followup)}</dd></div>`:''}</dl></article>`).join('')}</div>${a.commonProbe.length?`<details class="further"><summary>공통 관점의 선택 진단</summary>${list(a.commonProbe)}</details>`:''}</section>
 ${supplement.length?`<section class="reading-section"><h2>활동과 추가 해설</h2>${supplement.map(x=>`<div class="prose"><h3>${esc(x.title)}</h3>${markdown(x.body)}</div>`).join('')}</section>`:''}
 <section id="connections" class="reading-section"><p class="section-index">05 · CONNECTIONS</p><h2>관련 성취기준</h2><div class="cp-actions">${conceptIndex.groups.filter(g=>g.member_codes.includes(code)).map(g=>`<a class="button primary" href="${url('hierarchy',{concept:g.id,target:code})}">${esc(g.title)} 확장 위계 초안 ↗</a>`).join('')}</div><p>다른 내용과 이어지는 이유와 적용 조건을 함께 확인하세요.</p><div class="related-standards">${groups.slice(0,6).map(g=>`<div>${pill(types[g.type])}${standardRow(g.other)}</div>`).join('')}</div><a class="button primary" href="${url('connections',{code})}">연결 ${groups.length}개 묶음과 근거 살펴보기 →</a>${pilot.length?`<div class="pilot-links"><h3>이 기준을 포함하는 위계와 경로</h3>${pilot.map(m=>`<a class="button" href="${url('hierarchy',pathForStandard(m,code))}">${esc(m.title)} ↗</a>`).join('')}</div>`:''}</section>
 <section id="references" class="reading-section"><p class="section-index">06 · SOURCES</p><h2>출처와 검토 범위</h2><dl class="review-list"><div><dt>기준 판본</dt><dd>${esc(catalog.meta.curriculum)} · 별책8</dd></div><div><dt>원문 위치와 대조</dt><dd>PDF ${s.pdfPages.join(', ')}쪽 · 인쇄 ${s.printedPages.join(', ')}쪽 · ${esc(s.sourceReview)}</dd></div><div><dt>분석 검토</dt><dd>${esc(a.status)}</dd></div><div><dt>학생 반응</dt><dd>${a.validated?'검증 기록 있음':'검증 전'}</dd></div></dl>${a.correction?`<details class="further"><summary>원문 추출과 보정 기록</summary><p>${esc(a.correction.method)}</p><p><b>추출문</b> ${esc(s.extracted)}</p><p><b>표시문</b> ${esc(s.statement)}</p></details>`:''}${sourcesHTML(data.sources.filter(x=>referenced.has(x.id)))}<details class="further"><summary>전체 분석 원고 확인</summary><div class="prose">${markdown(a.markdown)}</div></details></section>
 <div class="reading-return"><a class="button" href="${esc(returnTo)}">← 찾아보던 화면으로</a><a href="${url('overview',{density:'expanded',focus:code})}">교육과정 목록에서 위치 보기 ↗</a></div></article>
 </div>`;
}

function revisedStandardPage(s,a,p,data,conceptIndex){
 const scope=p.get('scope')||'all';
 const sections = new Map(a.sections.map(section => [section.id, section]));
 const toc = analysisSections.flatMap(([, ids]) => ids.filter(id => sections.has(id)).map(id =>
   `<a href="${url('standard',{code:s.code,section:id,scope})}" data-section="${id}">${esc(sections.get(id).title)}</a>`
 )).join('');
 const renderSection = section => {
  const body = section.id === 'references' ? renderReferences(section.body) : markdown(section.body, {reading: true});
  return `<section id="${esc(section.id)}" class="reading-section">
   <h2>${esc(section.title)}</h2>
   <div class="prose">${body}${section.id==='references'?sourcesHTML(data.sources.filter(x=>x.id===s.sourceId)):''}</div>
  </section>`;
 };
 return `${!inScope(s,scope)?`<aside class="notice">현재 학교급 보기 범위 밖의 상세 문서를 열었습니다. 성취기준은 ${esc(s.level)}에 속합니다.</aside>`:''}
 <header class="standard-header">
   <p>${esc(s.level)} · ${esc(band(s))} · ${esc(s.code)}</p><h1 tabindex="-1">${esc(a.title)}</h1>
   <div class="official-statement"><span class="label">공식 성취기준</span><p>${esc(s.statement)}</p><a href="curriculum.pdf#page=${s.pdfPages[0]}" target="_blank" rel="noopener">교육과정 PDF ${s.pdfPages.join(', ')}쪽 ↗</a></div>
   ${a.sourceNotes?.length?`<aside class="notice">${a.sourceNotes.map(n=>`<p>${esc(n.scope_note)}</p>`).join('')}</aside>`:''}
   <div class="cp-actions">
     <a class="button primary" href="${url('hierarchy',{mode:'goals',target:s.code,scope})}">목표별 연결</a>
     <a class="button" href="${url('hierarchy',{mode:'tasks',target:s.code,scope})}">과제와 풀이 조건</a>
     ${conceptIndex.groups.filter(g=>g.member_codes.includes(s.code)).map(g=>`<a class="button" href="${url('hierarchy',{concept:g.id,target:s.code,scope})}">${esc(g.title)} 내부 위계</a>`).join('')}
     <a class="button" href="${url('network',{node:s.code,scope})}">연결 지도</a>
     <a class="button" href="${url('hierarchy',{q:s.code,scope})}">개념별 관계 찾기</a>
     <a class="button" href="${url('connections',{code:s.code,scope})}">관계 근거</a>
     <button class="button" data-print>인쇄</button>
   </div>
 </header>
 <nav class="reading-jumps screen-only" aria-label="상세 분석 목차">${toc}</nav>
 <div class="reading-layout"><article class="reading-body">
   ${a.sections.map(renderSection).join('')}
   <p><a class="button" href="${url('catalog',{scope,focus:s.code})}">성취기준 목록으로</a></p>
 </article></div>`;
}

function renderReferences(text) {
 return text.split(/(?=^#{3,4} )/m).map(block => {
  const claim = /^#### (근거 .+)\n\s*([\s\S]*)/.exec(block);
  if (!claim) return markdown(block, {reading: true});
  return `<details class="analysis-claim"><summary>${esc(claim[1])}</summary>${markdown(claim[2], {reading: true})}</details>`;
 }).join('');
}
