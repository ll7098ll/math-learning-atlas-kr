/* Curated partial orders. Layout never derives pedagogical rank from grades. */
(function(root){
  'use strict';
  const orderedKinds=new Set(['task_condition','generalizes','instructional_sequence']);
  const names={task_condition:'이 과제의 필요 조건',generalizes:'의미 확장',instructional_sequence:'수업 순서 제안'};
  const escape=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  function selectRoute(map,route){
    const claims=map.claims.filter(c=>c.routes.includes(route));
    const used=new Set([map.focus,...claims.flatMap(c=>[c.source,c.target])]);
    return {nodes:map.nodes.filter(n=>used.has(n.id)),claims};
  }
  function context(map,route,byCode,includes){
    const data=selectRoute(map,route);
    return {...data,nodes:data.nodes.map(n=>({...n,boundary:!n.standards.some(c=>includes(byCode.get(c)))})),hiddenNodes:0,hiddenClaims:0,boundaryCount:data.nodes.filter(n=>!n.standards.some(c=>includes(byCode.get(c)))).length};
  }
  function rank(nodes,claims){
    const levels=new Map(nodes.map(n=>[n.id,0])), indegree=new Map(nodes.map(n=>[n.id,0]));
    const edges=claims.filter(c=>orderedKinds.has(c.kind));
    for(const c of edges){if(!levels.has(c.source)||!levels.has(c.target))throw new Error('위계 대상이 없습니다: '+c.id);indegree.set(c.target,indegree.get(c.target)+1);}
    const outgoing=new Map(nodes.map(n=>[n.id,[]]));for(const c of edges)outgoing.get(c.source).push(c);
    const queue=nodes.filter(n=>indegree.get(n.id)===0).map(n=>n.id);let seen=0;
    for(let i=0;i<queue.length;i++){
      const id=queue[i];seen++;
      for(const c of outgoing.get(id)){
        levels.set(c.target,Math.max(levels.get(c.target),levels.get(id)+1));
        indegree.set(c.target,indegree.get(c.target)-1);
        if(indegree.get(c.target)===0)queue.push(c.target);
      }
    }
    if(seen!==nodes.length)throw new Error('선후 관계에 순환이 있습니다. 위계 검토가 필요합니다.');
    return levels;
  }
  function init(container,query,D){
    const maps=D.hierarchy.maps,Scope=root.CurriculumScope,standardByCode=new Map(D.standards.map(s=>[s.code,s]));
    const available=m=>m.nodes.some(n=>n.standards.some(c=>!Scope||Scope.includes(standardByCode.get(c))));
    const mapIcon=m=>root.DomainIcons?root.DomainIcons.icon(m.id==='fraction'?'수와 연산':m.id==='ratio'?'변화와 관계':'도형과 측정'):'';
    const map=maps.find(m=>m.id===query.get('map'))||maps.find(available)||maps[0];
    const route=map.routes.find(r=>r.id===query.get('route'))||map.routes.find(r=>!Scope||Scope.visibleHierarchy(map,r.id,standardByCode,Scope.current().id).nodes.length)||map.routes[0];
    const fullData=selectRoute(map,route.id),data=Scope?Scope.visibleHierarchy(map,route.id,standardByCode,Scope.current().id):fullData;
    if(!data.nodes.length){container.innerHTML=`<div class="hierarchy-map-tabs">${maps.map(m=>`<a class="button" href="#view=hierarchy&map=${m.id}&scope=${Scope?.current().id||'all'}">${mapIcon(m)}${escape(m.title)}</a>`).join('')}</div><section class="empty"><h2>선택한 범위에서 이 경로의 사고를 찾을 수 없습니다.</h2><p>현재 ${escape(Scope?.current().title||'전체')}를 살펴보고 있습니다. 다른 개념군을 고르거나 범위를 넓혀 주세요.</p><button class="button primary" data-scope="all">초·중·고 전체에서 보기</button></section>`;return ()=>{};}
    const requested=query.get('target')||map.focus;
    if(!data.nodes.some(n=>n.id===requested)){
      const base={view:'hierarchy',map:map.id,route:route.id,scope:Scope?.current().id||'all'};
      container.innerHTML=`<section class="empty"><h2>목표가 선택 학교급 범위 밖입니다.</h2><p>현재 범위에서 목표를 선택하거나 전체 조건을 펼쳐 보세요.</p>${data.nodes.map(n=>`<a class="button" href="#${new URLSearchParams({...base,target:n.id})}">${escape(n.title)}</a>`).join('')}<a class="button" href="#${new URLSearchParams({...base,target:requested,external:'1'})}">다른 학교급의 전체 조건 보기</a></section>`;return ()=>{};
    }
    const levels=rank(data.nodes,data.claims),fullLevels=rank(fullData.nodes,fullData.claims);
    const focusId=data.nodes.some(n=>n.id===query.get('target'))?query.get('target'):map.focus;
    const initialClaim=data.claims.find(c=>c.id===query.get('claim'));
    const nodeId=data.nodes.some(n=>n.id===query.get('node'))?query.get('node'):focusId;
    const nodeById=new Map(map.nodes.map(n=>[n.id,n]));
    const esc=escape,link=(params={})=>'#'+new URLSearchParams({view:'hierarchy',map:map.id,route:route.id,target:focusId,...(query.get('external')?{external:'1'}:{}),...(query.get('kind')?{kind:query.get('kind')}:{}),...(query.get('compare')?{compare:'1'}:{}),...(Scope?{scope:Scope.current().id}:{}),...params});
    const standardLink=code=>'#view=standard&code='+encodeURIComponent(code);
    const nodeTitle=id=>nodeById.get(id)?.title||id;
    const list=values=>'<ul>'+values.map(v=>'<li>'+esc(v)+'</li>').join('')+'</ul>';
    const sources=new Map(D.sources.map(s=>[s.id,s]));
    const kind=query.get('kind')||'',shownClaims=data.claims.filter(c=>!kind||c.kind===kind);
    const max=Math.max(...levels.values()),focusLevel=levels.get(focusId);
    container.innerHTML=`<div class="hierarchy-map-tabs" aria-label="시범 개념군">${maps.map(m=>`<a class="button ${m.id===map.id?'primary':''}" href="#view=hierarchy&map=${m.id}&scope=${Scope?.current().id||'all'}" ${m.id===map.id?'aria-current="page"':''}>${mapIcon(m)}${esc(m.title)}</a>`).join('')}</div>
      <section class="hierarchy-summary panel"><div><span class="pill">경로별 위계 탐색</span><h2>${esc(map.title)}</h2><p>${esc(map.task)}</p><p class="meta">${esc(D.hierarchy.status)}</p></div><label>설명 경로<select id="hierarchy-route" aria-label="설명 경로">${map.routes.map(r=>`<option value="${r.id}" ${r.id===route.id?'selected':''}>${esc(r.title)}</option>`).join('')}</select></label></section>
      <p class="note hierarchy-note">${query.get('target')&&query.get('target')!==focusId?'선택했던 사고가 이 경로에 없어 원래 목표를 보여줍니다. ':''}${data.boundaryCount?`현재 ${escape(Scope.current().title)} 범위 밖 사고 ${data.boundaryCount}개를 맥락으로 남겼습니다. 목표와 전체 조건은 유지됩니다. `:''}${data.hiddenNodes?`현재 ${escape(Scope.current().title)} 범위입니다. 범위 밖 ${data.hiddenNodes}개 사고·${data.hiddenClaims}개 관계를 숨겼으며, 숨겨진 단계를 건너뛰는 화살표는 만들지 않습니다. `:''}기초에서 목표를 거쳐 확장으로 읽습니다. 화살표의 종류를 선택해 이유와 한계를 확인하세요. 단계는 선택한 경로의 상대 위치이며 학년·난이도·모든 학생의 발달 순서를 뜻하지 않습니다.</p>
      <div class="hierarchy-layout"><div class="panel"><div class="panel-heading"><h2>기초 → 선택 목표 → 이후 확장</h2><small>${data.nodes.length}개 사고 · ${data.claims.length}개 관계</small></div><div class="hierarchy-scroll"><div class="hierarchy-canvas" style="--stages:${max+1}"><svg aria-hidden="true"></svg>${Array.from({length:max+1},(_,i)=>`<section class="hierarchy-stage" aria-label="${i+1}단계"><header><small>STEP ${String(i+1).padStart(2,'0')}</small><strong>${i<focusLevel?'이전 설명 단계':i===focusLevel?'목표가 있는 단계':'이후 설명·확장'}</strong></header><div class="hierarchy-stage-nodes">${data.nodes.filter(n=>levels.get(n.id)===i).map(n=>`<button type="button" class="hierarchy-node ${n.id===focusId?'target':''} ${n.boundary?'boundary':''}" data-hnode="${n.id}" aria-pressed="false"><span>${esc(n.id===focusId?'선택 목표':n.standards[0])}${n.boundary?' · 범위 밖':''}</span><strong>${esc(n.title)}</strong></button>`).join('')}</div></section>`).join('')}</div></div>
      <div class="map-footer hierarchy-legend"><span>실선 → 과제의 조건</span><span>파란 점선 → 의미 확장</span><span>회색 점선 → 수업 제안</span></div><div class="hierarchy-claims"><h3>이 경로의 연결 근거</h3><p class="meta">같은 합류 묶음의 조건은 함께(AND) 필요합니다. 분수와 넓이는 같은 목표의 대안 풀이입니다. 정비례와 반비례는 서로 다른 관계를 다루는 분기입니다. 과제의 조건은 과제 안에서 함께 구성할 수도 있습니다.</p>${shownClaims.map(c=>`<button type="button" class="hierarchy-claim" data-hclaim="${c.id}"><span class="pill">${names[c.kind]}</span><strong>${esc(nodeTitle(c.source))} → ${esc(nodeTitle(c.target))}</strong><small>${c.condition_group?fullData.claims.filter(x=>x.condition_group===c.condition_group).length+'개 전체 조건 함께 · AND'+(fullData.claims.filter(x=>x.condition_group===c.condition_group&&!data.nodes.some(n=>n.id===x.source)).length?' · 범위 밖 조건 포함':''):'관계 '+esc(c.id)}</small></button>`).join('')}</div></div>
      <aside class="panel hierarchy-inspector" aria-label="위계 분석 근거"><div id="hierarchy-detail" aria-live="polite"></div></aside></div>`;
    const kindPanel=document.createElement('div');kindPanel.className='hierarchy-kind';kindPanel.innerHTML=`<label>관계 종류 <select id="hierarchy-kind"><option value="">모든 설명 관계</option>${Object.entries(names).map(([k,v])=>`<option value="${k}" ${kind===k?'selected':''}>${v}</option>`).join('')}</select></label><p class="meta">단계는 설명의 흐름입니다. 선 종류를 골라 과제의 조건과 의미 확장을 구별하세요. 조건 묶음은 항상 전체를 유지합니다.</p>`;container.querySelector('.hierarchy-note').after(kindPanel);kindPanel.querySelector('select').addEventListener('change',e=>{location.hash=link({kind:e.target.value});});
    const routePanel=document.createElement('section');routePanel.className='panel pathway-comparison';
    const sets=map.routes.map(r=>({route:r,...selectRoute(map,r.id)}));
    const common=map.nodes.filter(n=>sets.every(r=>r.nodes.some(x=>x.id===n.id)));
    routePanel.innerHTML=`<details ${query.get('compare')?'open':''} data-open="compare-${map.id}"><summary>두 경로의 공통점과 차이 비교</summary><p>${map.id==='ratio'?'정비례와 반비례는 불변량이 다른 목표 분기입니다. 서로 대체하는 풀이로 취급하지 않습니다.':'같은 목표를 설명하는 두 경로입니다. 한 경로의 전용 사고를 다른 경로에 강제하지 않습니다.'}</p><h3>공통 사고</h3>${list(common.map(n=>n.title))}<div class="pathway-cards">${sets.map(r=>`<article><h3>${esc(r.route.title)}</h3>${list(r.nodes.filter(n=>!common.some(c=>c.id===n.id)).map(n=>n.title))}<a class="button" href="${link({route:r.route.id,target:r.nodes.some(n=>n.id===focusId)?focusId:map.focus,compare:'1'})}">이 경로로 보기 →</a></article>`).join('')}</div></details>`;
    container.querySelector('.hierarchy-note').after(routePanel);
    function highlight(node,claim){
      for(const n of container.querySelectorAll('[data-hnode]'))n.setAttribute('aria-pressed',String(n.dataset.hnode===node));
      for(const n of container.querySelectorAll('[data-hclaim]'))n.classList.toggle('selected',n.dataset.hclaim===claim);
      for(const path of container.querySelectorAll('[data-hpath]'))path.classList.toggle('selected',path.dataset.hpath===claim);
    }
    function showNode(id){
      const n=nodeById.get(id);if(!n)return;
      history.replaceState(null,'',link({node:id}));
      highlight(id,null);
      const incoming=data.claims.filter(c=>c.target===id),outgoing=data.claims.filter(c=>c.source===id);
      const buttons=cs=>cs.map(c=>`<button class="hierarchy-claim" data-hclaim="${c.id}"><small>${names[c.kind]}</small><strong>${esc(nodeTitle(c.source))} → ${esc(nodeTitle(c.target))}</strong></button>`).join('');
      container.querySelector('#hierarchy-detail').innerHTML=`<div class="inspector-header"><span class="pill">${id===focusId?'선택 목표':'사고 요소'}</span><h2>${esc(n.title)}</h2><small>현재 경로의 ${levels.get(id)+1}단계</small></div><div class="inspector-body"><a class="button primary" href="${link({target:id,node:id})}">이 사고를 목표로 보기 →</a><h3>이해를 확인할 질문</h3><p>${esc(n.question)}</p><h3>기대하는 설명</h3><p>${esc(n.expected)}</p><h3>대응하는 공식 성취기준</h3>${n.standards.map(c=>`<a class="button" href="${standardLink(c)}">${esc(c)} · 원문과 분석 ↗</a>`).join('')}<h3>이 사고로 들어오는 관계</h3>${buttons(incoming)||'<p>이 시범 경로에 선행 관계가 기록되지 않았습니다. 더 기초적인 개념이 없다는 뜻은 아닙니다.</p>'}<h3>이후 이어지는 관계</h3>${buttons(outgoing)||'<p>이 시범 분석의 끝입니다. 후속 학습 전체를 뜻하지 않습니다.</p>'}<p class="note">학생 반응 검증 전인 진단 설계안입니다.</p></div>`;
    }
    function showClaim(id){
      const c=data.claims.find(c=>c.id===id);if(!c)return;
      history.replaceState(null,'',link({claim:id}));
      highlight(null,id);
      const siblings=c.condition_group?fullData.claims.filter(x=>x.condition_group===c.condition_group):[];
      container.querySelector('#hierarchy-detail').innerHTML=`<div class="inspector-header"><span class="pill">${names[c.kind]}</span><h2>${esc(nodeTitle(c.source))}<br>↓<br>${esc(nodeTitle(c.target))}</h2><small>${esc(c.id)} · ${esc(c.status)}</small></div><div class="inspector-body"><h3>왜 이 방향인가</h3><p>${esc(c.rationale)}</p><h3>성립하는 과제와 조건</h3>${list(c.conditions)}${siblings.length?'<h3>함께 필요한 조건 · AND</h3>'+list(siblings.map(s=>nodeTitle(s.source)))+'<p class="meta">각 조건은 현재 선택한 경로에서 함께 필요합니다. 전체 묶음을 유지하며 일부 조건이 선택 학교급 밖일 수 있습니다.</p>':''}<h3>수학적 자체 점검</h3><p>${esc(c.mathematical_check)}</p><h3>확인 질문</h3><p>${esc(c.probe.question)}</p><h3>기대하는 설명</h3><p>${esc(c.probe.expected)}</p><h3>다른 경로와 적용 한계</h3><p>${esc(c.alternative)}</p><h3>분석 근거 문서</h3>${map.documents.map(p=>{const code=p.split('/').pop().replace('.md','');return `<a class="button" href="${standardLink(code)}">${esc(code)} 분석 ↗</a>`;}).join('')}${c.original_relation_ids.length?'<h3>기존 관계 기록과 대조</h3>'+c.original_relation_ids.map(id=>{const r=D.relations.find(r=>r.id===id);return r?`<details class="source"><summary>${esc(id)} · ${esc(r.status)}</summary><p>${esc(r.scope)}</p><p>${esc(r.rationale)}</p><p>${esc(r.limit)}</p></details>`:'';}).join(''):''}${c.research_context.length?'<h3>관련 연구 관점</h3>'+c.research_context.map(id=>{const s=sources.get(id);return s?`<div class="source"><a href="${esc(s.url)}" target="_blank" rel="noopener noreferrer">${esc(s.title)} ↗</a><p>분할·반복·단위 조정에 관한 관점을 참고했습니다. 이 화살표와 한국 과제의 효과를 직접 검증한 연구라는 뜻은 아닙니다.</p></div>`:'';}).join(''):''}<p class="note">근거: ${esc(c.evidence_kind)}<br>독립 검토 전 · 학생 반응 검증 전</p><div class="inspector-actions"><button class="button" data-hnode="${c.source}">출발 사고</button><button class="button" data-hnode="${c.target}">도착 사고</button></div></div>`;
    }
    const canvas=container.querySelector('.hierarchy-canvas');
    function draw(){
      if(!canvas.isConnected)return;
      const rect=canvas.getBoundingClientRect(),svg=canvas.querySelector('svg'),positions=new Map([...canvas.querySelectorAll('[data-hnode]')].map(n=>[n.dataset.hnode,n.getBoundingClientRect()]));
      svg.setAttribute('viewBox',`0 0 ${canvas.scrollWidth} ${canvas.scrollHeight}`);
      svg.innerHTML=`<defs>${['task_condition','generalizes','instructional_sequence'].map(k=>`<marker id="arrow-${map.id}-${k}" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 Z" class="arrow-${k}"/></marker>`).join('')}</defs>`+shownClaims.map(c=>{
        const from=positions.get(c.source),to=positions.get(c.target);
        let x=from.right-rect.left,y=from.top-rect.top+from.height/2,tx=to.left-rect.left,ty=to.top-rect.top+to.height/2;
        const mobile=window.innerWidth<=520;
        if(mobile){x=from.left-rect.left+from.width/2;y=from.bottom-rect.top;tx=to.left-rect.left+to.width/2;ty=to.top-rect.top;}
        const d=mobile?`M${x},${y} L${x},${y+6} L4,${y+6} L4,${ty-10} L${tx},${ty-10} L${tx},${ty}`:`M${x},${y} C${(x+tx)/2},${y} ${(x+tx)/2},${ty} ${tx},${ty}`;
        return `<path class="hierarchy-line ${c.kind}" d="${d}" marker-end="url(#arrow-${map.id}-${c.kind})"/><path class="hierarchy-hit" d="${d}" data-hpath="${c.id}"/>`;
      }).join('');
      const joins=[...new Set(shownClaims.map(c=>c.condition_group).filter(Boolean))].map(id=>data.claims.filter(c=>c.condition_group===id));
      svg.insertAdjacentHTML('beforeend',joins.map(group=>{const target=positions.get(group[0].target),mobile=window.innerWidth<=520,x=mobile?target.left-rect.left+target.width/2:target.left-rect.left-19,y=mobile?target.top-rect.top-17:target.top-rect.top+target.height/2;return `<g class="hierarchy-join" transform="translate(${x},${y})"><rect x="-16" y="-9" width="32" height="18" rx="5"/><text text-anchor="middle" y="4">AND</text></g>`;}).join(''));
      const selected=container.querySelector('.hierarchy-claim.selected');if(selected)highlight(null,selected.dataset.hclaim);
    }
    container.querySelector('#hierarchy-route').addEventListener('change',e=>{location.hash=link({route:e.target.value});});
    container.addEventListener('click',handler);
    function handler(event){
      const button=event.target.closest('[data-hnode],[data-hclaim],[data-hpath]');if(!button)return;
      if(button.dataset.hnode)showNode(button.dataset.hnode);else showClaim(button.dataset.hclaim||button.dataset.hpath);
      if(window.innerWidth<=800&&button.closest('.hierarchy-canvas'))container.querySelector('.hierarchy-inspector').scrollIntoView({block:'start',behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'instant':'smooth'});
    }
    try{const key='atlas-recent-pathways',old=JSON.parse(localStorage.getItem(key)||'[]');localStorage.setItem(key,JSON.stringify([{map:map.id,route:route.id,target:focusId},...old.filter(x=>x.map!==map.id||x.route!==route.id||x.target!==focusId)].slice(0,5)));}catch{}
    if(initialClaim)showClaim(initialClaim.id);else showNode(nodeId);
    let frame=0;const schedule=()=>{if(!frame)frame=requestAnimationFrame(()=>{frame=0;draw();});};const observer=new ResizeObserver(schedule);observer.observe(canvas);schedule();
    return ()=>{observer.disconnect();cancelAnimationFrame(frame);container.removeEventListener('click',handler);};
  }
  const api={selectRoute,context,rank,init};
  if(typeof module!=='undefined'&&module.exports)module.exports=api;else root.CurriculumHierarchy=api;
})(typeof window!=='undefined'?window:globalThis);
