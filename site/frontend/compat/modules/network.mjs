import {catalog,conceptFlows,connections,types,inScope} from './store.mjs';
import {esc,url,overviewModes} from './ui.mjs';
import {buildNetwork,selectNetwork,traceExpansion} from './network-model.mjs';

import {layoutInternalNetwork} from './internal-layout.mjs';
import {guidedMap, mountGuidedMap} from './guided-map.mjs';
const palette=['#6ce1cc','#8cafff','#f3bd72','#d59cf5','#f490ab'];
let model,flows;
const cameras=new Map();
export async function networkPage(p=new URLSearchParams()){
 if(p.get('mapMode')!=='full' && !['q','domain','strand','relation'].some(key=>p.get(key))) return guidedMap(p);
 const [f,c]=await Promise.all([conceptFlows(),connections()]);flows=f;
 const scope=p.get('scope')||'all';
 model=buildNetwork({...catalog,standards:catalog.standards.filter(s=>inScope(s,scope))},f,c);
 if(['e','m','h'].includes(scope))layoutInternalNetwork(model);
 return `<section class="atlas-network"><div class="network-intro"><div><p class="eyebrow">THE MATHEMATICS NETWORK</p><h1 tabindex="-1">${p.get("node")&&model.byCode.has(p.get("node"))?"이 기준의 연결 지도":"수학 연결 지도"}</h1><p>선택한 학교급의 성취기준과 내부 연결을 하나의 연결망으로. 왼쪽에서 오른쪽으로 교육과정의 단계와 개념의 확장을 따라가세요.</p></div><a class="text-link" href="#view=hierarchy">전체 개념군 연결과 위계 ↗</a></div>${overviewModes('network')}<a class="guide-mode-link" href="${url('network',{scope,node:p.get('node')})}">학년·개념으로 연결 따라가기</a>
 <form class="atlas-controls" aria-label="연결망 탐색"><label class="atlas-search">노드 찾기<input name="query" type="search" placeholder="분수, 비율 또는 성취기준 코드" autocomplete="off"></label><label>내용 영역<select name="domain"><option value="">모든 영역</option>${model.bands.map(b=>`<option>${esc(b.domain)}</option>`).join('')}</select></label><label>개념<select name="strand"><option value="">46개 개념 전체</option>${f.strands.map(s=>`<option value="${esc(s.id)}">${esc(s.title)}</option>`).join('')}</select></label><label>연결선<select name="relation"><option value="all">전체 연결</option><option value="generalizes">의미 확장</option><option value="requires_for_task">과제별 필요 조건</option><option value="meaning_connection">의미 연결</option><option value="contrasts">대조</option></select></label><button type="button" class="button" data-action="reset">초기화</button></form>
 <div class="atlas-summary" role="status" aria-live="polite"></div>
 <div class="atlas-workspace"><div class="atlas-stage"><div class="atlas-axis" role="group" aria-label="${model.internal?'관계 단계':'교육과정 단계'}">${model.stages.map((s,i)=>`<span>${esc(s.title)}${i<model.stages.length-1?' <b aria-hidden="true">→</b>':''}</span>`).join('')}</div><svg class="atlas-svg" role="group" tabindex="0" aria-label="전체 수학 연결망. 방향키로 이동, 더하기와 빼기로 확대 축소, 0으로 전체 보기. 노드를 선택하면 연결을 강조합니다."><defs><marker id="atlas-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="context-stroke"/></marker></defs><g class="atlas-world"></g></svg><div class="atlas-tooltip" hidden></div><div class="atlas-tools"><button type="button" data-action="in" aria-label="연결망 확대">＋</button><button type="button" data-action="out" aria-label="연결망 축소">−</button><button type="button" data-action="fit">전체 맞춤</button><button type="button" data-action="focus">선택 연결 맞춤</button><button type="button" data-action="expand" aria-pressed="false">크게 보기</button><output class="atlas-zoom" aria-label="확대 비율">100%</output></div><p class="atlas-help">드래그로 이동 · 휠 / 두 손가락으로 확대 · 노드를 눌러 연결 탐색</p></div><aside class="atlas-inspector" aria-label="선택한 노드 정보"></aside></div>
 <div class="atlas-legend"><span><i class="legend-expansion"></i>화살표: 의미 확장·과제 조건</span><span><i class="legend-task"></i>황갈색 점선: 과제별 필요 조건</span><span><i class="legend-connection"></i>선: 의미 연결</span><span><i class="legend-contrast"></i>점선: 대조</span><span>선택 후 <b style="color:#2477ac">파랑: 이전 확장</b> · <b style="color:#a86a16">금색: 이후 확장</b></span></div><p class="atlas-note">${model.internal?'가로 위치는 자체 분석한 의미 확장·과제 조건의 상대 단계입니다. 순서 미정에는 방향 미기록과 순환 검토 대상을 둡니다.':'가로 위치는 교육과정의 학년군·과목 단계입니다.'} 같은 단계 안의 위치는 개념별 배치이며 학습 선후를 뜻하지 않습니다. 화살표는 기록된 의미 확장으로, 모든 학생의 필수 선수 순서를 뜻하지 않습니다.</p></section>`;
}

function curve(a,b,index){
 const dx=b.x-a.x,dy=b.y-a.y,d=Math.hypot(dx,dy)||1;
 const start={x:a.x+dx/d*7,y:a.y+dy/d*7},end={x:b.x-dx/d*9,y:b.y-dy/d*9};
 if(Math.abs(dx)<30){const bend=44+(index%4)*12;return `M${start.x},${start.y} C${start.x+bend},${start.y} ${end.x+bend},${end.y} ${end.x},${end.y}`;}
 const bend=Math.max(50,Math.abs(dx)*.46)*Math.sign(dx);return `M${start.x},${start.y} C${start.x+bend},${start.y} ${end.x-bend},${end.y} ${end.x},${end.y}`;
}

export function mountNetwork(p,root,onRouteChange=()=>{}){
 if(root.querySelector('.guided-map')) return mountGuidedMap(root);
 const host=root.querySelector('.atlas-network'),form=host.querySelector('form'),svg=host.querySelector('svg.atlas-svg'),world=svg.querySelector('.atlas-world'),inspector=host.querySelector('.atlas-inspector'),workspace=host.querySelector('.atlas-workspace'),tooltip=host.querySelector('.atlas-tooltip');
 const state={query:p.get('q')||'',domain:p.get('domain')||'',strand:p.get('strand')||'',relation:p.get('relation')||'all',selected:p.get('node')||''};
 for(const name of ['query','domain','strand','relation']){form.elements[name].value=state[name];if(form.elements[name].value!==state[name])state[name]=form.elements[name].value;}
 const outsideSelection=!!state.selected&&!model.byCode.has(state.selected);if(outsideSelection)state.selected='';
 let active,trace,neighbors=new Set(),directEdges=new Set(),camera={x:0,y:0,w:model.width,h:model.height},timer,frame,moved=false,drag=null,pinch=null;
 const pointers=new Map(),abort=new AbortController(),signal=abort.signal;
 const colors=new Map(model.bands.map((b,i)=>[b.domain,palette[i%palette.length]]));
 world.innerHTML=model.bands.map((b,i)=>`<rect class="atlas-band" x="0" y="${b.y}" width="${model.width}" height="${b.height}" fill="${i%2?'#122936':'#10232f'}"/><text class="atlas-band-label" x="20" y="${b.y+28}" fill="${colors.get(b.domain)}">${esc(b.domain)}</text>`).join('')+
 model.stages.map(s=>`<line class="atlas-column-line" x1="${s.x}" x2="${s.x}" y1="50" y2="${model.height-20}"/><text class="atlas-stage-label" x="${s.center}" y="45" text-anchor="middle">${esc(s.title)}</text>`).join('')+
 `<g class="atlas-edges" aria-hidden="true">${model.edges.map((e,i)=>`<path data-edge="${esc(e.id)}" class="atlas-edge ${e.type==='requires_for_task'?'is-task':''} ${['generalizes','requires_for_task'].includes(e.type)?'is-expansion':e.type==='contrasts'?'is-contrast':''}" d="${curve(model.byCode.get(e.from),model.byCode.get(e.to),i)}" ${['generalizes','requires_for_task'].includes(e.type)?'marker-end="url(#atlas-arrow)"':''} vector-effect="non-scaling-stroke"><title>${esc(model.byCode.get(e.from).title)} ${['generalizes','requires_for_task'].includes(e.type)?'→':'—'} ${esc(model.byCode.get(e.to).title)} · ${esc(types[e.type])}</title></path>`).join('')}</g>`+
 `<g class="atlas-nodes">${model.nodes.map(n=>`<g class="atlas-dot" data-node="${esc(n.code)}" transform="translate(${n.x} ${n.y})" style="--node-color:${colors.get(n.domain)}" tabindex="-1" role="button" aria-label="${esc(n.code+' '+n.title)}" aria-pressed="false"><circle class="hit" r="13" fill="transparent"/><circle class="ring" r="10"/><circle class="core" r="5.5"/><text class="atlas-label" x="12" y="5" pointer-events="none">${esc(n.title.length>15?n.title.slice(0,15)+'…':n.title)}</text><title>${esc(n.code+' · '+n.title)}</title></g>`).join('')}</g>`;
 const nodeEls=new Map([...world.querySelectorAll('[data-node]')].map(el=>[el.dataset.node,el]));
 const edgeEls=new Map([...world.querySelectorAll('[data-edge]')].map(el=>[el.dataset.edge,el]));

 function save(){
  const params={mapMode:'full',scope:globalThis.atlasSchoolScope||'all',node:state.selected,q:state.query,domain:state.domain,strand:state.strand,relation:state.relation==='all'?'':state.relation};
  if(p.has('resume'))params.resume=p.get('resume');
  const hash=url('network',params);history.replaceState(history.state,'',hash);onRouteChange(hash);cameras.set(hash,{...camera});
  const guide=host.querySelector('.guide-mode-link');
  const resume=new URLSearchParams(p.get('resume')||'');
  const sameCenter=state.selected && resume.get('node')===state.selected;
  const back={scope:sameCenter?resume.get('scope')||params.scope:params.scope,node:state.selected};
  if(sameCenter)for(const key of ['band','concept','walk','trail','page'])back[key]=resume.get(key);
  guide.href=url('network',back);
  const label=back.walk||back.trail?'내가 따라온 길로 돌아가기':'학년·개념으로 연결 따라가기';
  if(guide.textContent!==label)guide.textContent=label;
  const heading=host.querySelector('h1');
  const title=state.selected?'이 기준의 연결 지도':'수학 연결 지도';
  if(heading.textContent!==title){
   heading.textContent=title;
   document.title=title+' · 수학의 연결 지도';
  }
  try{sessionStorage.setItem('atlas-return',hash);sessionStorage.setItem('atlas-network-camera',JSON.stringify({hash,camera}));}catch{}
 }
 const axis=host.querySelector('.atlas-axis');
 const stageLabels=[...axis.children];

 function drawStageLabels(){
  const axisWidth=axis.clientWidth;
  const widths=stageLabels.map(label=>Math.ceil(label.getBoundingClientRect().width));
  const labelGap=8;
  let previousRight=-labelGap;

  stageLabels.forEach((label,index)=>{
   const position=(model.stages[index].center-camera.x)/camera.w;
   const halfWidth=widths[index]/2;
   const left=position*axisWidth-halfWidth;
   const right=left+widths[index];
   const visible=left>=0 && right<=axisWidth && left>=previousRight+labelGap;
   label.style.left=position*100+'%';
   label.toggleAttribute('data-axis-hidden',!visible);
   if(visible)previousRight=right;
  });
 }

 function drawCamera(){
  svg.setAttribute('viewBox',`${camera.x} ${camera.y} ${camera.w} ${camera.h}`);
  drawStageLabels();
  const labelSize=Math.min(38,Math.max(14,11*camera.w/Math.max(svg.getBoundingClientRect().width,1)));world.querySelectorAll('.atlas-label').forEach(el=>el.style.fontSize=labelSize+'px');
  const zoom=model.width/camera.w;svg.classList.toggle('show-labels',zoom>3.2);
  host.querySelector('.atlas-zoom').textContent=Math.round(zoom*100)+'%';save();
 }
 function fit(codes){
  const ns=codes?.size?model.nodes.filter(n=>codes.has(n.code)):model.nodes;if(!ns.length)return;
  const bounds=codes?.size?{x:Math.min(...ns.map(n=>n.x))-90,y:Math.min(...ns.map(n=>n.y))-80,w:Math.max(...ns.map(n=>n.x))-Math.min(...ns.map(n=>n.x))+180,h:Math.max(...ns.map(n=>n.y))-Math.min(...ns.map(n=>n.y))+160}:{x:0,y:0,w:model.width,h:model.height};
  const rect=svg.getBoundingClientRect(),aspect=rect.width/Math.max(rect.height,1);bounds.w=Math.max(bounds.w,360);bounds.h=Math.max(bounds.h,240);
  if(bounds.w/bounds.h>aspect){const h=bounds.w/aspect;bounds.y-=(h-bounds.h)/2;bounds.h=h;}else{const w=bounds.h*aspect;bounds.x-=(w-bounds.w)/2;bounds.w=w;}
  camera=bounds;drawCamera();
 }
 function zoom(factor,cx=.5,cy=.5){
  const w=Math.max(170,Math.min(model.width*2.5,camera.w*factor)),ratio=w/camera.w,h=camera.h*ratio;
  camera={x:camera.x+(camera.w-w)*cx,y:camera.y+(camera.h-h)*cy,w,h};drawCamera();
 }
 function relationshipButton(code,label=''){
  const n=model.byCode.get(code);return `<button type="button" data-select="${esc(code)}"><small>${esc(label||model.stages[n.stage].label||model.stages[n.stage].title)} · ${esc(code)}</small><strong>${esc(n.title)}</strong></button>`;
 }
 function relationList(title,codes){
  const sorted=[...codes].sort((a,b)=>model.byCode.get(a).stage-model.byCode.get(b).stage||a.localeCompare(b,'ko'));
  return `<section><h3>${title} <small>${sorted.length}</small></h3>${sorted.length?`<div class="atlas-relations">${sorted.slice(0,5).map(c=>relationshipButton(c)).join('')}${sorted.length>5?`<details><summary>나머지 ${sorted.length-5}개 보기</summary>${sorted.slice(5).map(c=>relationshipButton(c)).join('')}</details>`:''}</div>`:'<p class="muted">기록된 연결이 없습니다.</p>'}</section>`;
 }
 function renderInspector(){
  const n=model.byCode.get(state.selected);
  if(n){
   const before=new Set([...trace.ancestors].filter(id=>active.activeNodes.has(id))),after=new Set([...trace.descendants].filter(id=>active.activeNodes.has(id))),other=new Set([...neighbors].filter(id=>!before.has(id)&&!after.has(id)));
   inspector.innerHTML=`<p class="eyebrow">선택한 성취기준</p><p class="atlas-selected-code">${esc(n.code)} · ${esc(model.stages[n.stage].label||model.stages[n.stage].title)}</p><h2 class="atlas-selected-title">${esc(n.title)}</h2><p>${esc(n.standard.statement)}</p><p class="muted">${esc(n.domain)} · ${esc(n.standard.level)} · ${esc(n.standard.subject||n.standard.band)} · ${esc(n.strandTitle)}</p><div class="atlas-inspector-actions"><a class="button" href="${url('hierarchy',{concept:n.strandId,target:n.code})}">이 목표의 확장 위계 초안 ↗</a><a class="button primary" href="${url('standard',{code:n.code})}" data-standard="${esc(n.code)}">상세 분석 ↗</a><a class="text-link" href="${url('connections',{code:n.code})}">연결 근거 ↗</a><button type="button" data-action="clear">선택 해제</button></div><p class="atlas-selection-note">${active.activeNodes.has(n.code)?'현재 필터 안의 연결을 표시합니다.':'선택 노드가 필터 범위 밖입니다. 초기화하면 전체 연결을 볼 수 있습니다.'}</p>${relationList('← 앞선 의미·과제 조건',before)}${relationList('이후 의미·과제 조건 →',after)}${relationList('함께 연결된 기준',other)}`;
  }else if(state.query||state.domain||state.strand){
   const nodes=model.nodes.filter(n=>active.activeNodes.has(n.code));inspector.innerHTML=`<p class="eyebrow">연결망 안에서 찾기</p><h2>선택 범위 ${nodes.length}개</h2><p>선택 범위의 기준과 연결만 표시했습니다. 기준을 눌러 앞뒤 연결을 살펴보세요.</p><div class="atlas-relations">${nodes.slice(0,50).map(n=>relationshipButton(n.code)).join('')}</div>${nodes.length>50?`<p>50개 표시 중 · 개념이나 코드로 더 좁힐 수 있습니다.</p>`:''}${nodes.length?'':'<p class="atlas-empty">일치하는 기준이 없습니다.</p>'}`;
  }else{
   inspector.innerHTML=`<p class="eyebrow">수학 전체를 한눈에</p><h2>하나의 점에서<br>연결을 따라가세요.</h2><p>각 점은 하나의 성취기준입니다. 점을 선택하면 직접 연결과 앞뒤로 이어지는 확장이 드러납니다.</p><div class="atlas-stats"><strong>${model.nodes.length} <small>성취기준</small></strong><strong>46 <small>개념</small></strong></div><ul class="atlas-domain-key">${model.bands.map(b=>`<li><i style="background:${colors.get(b.domain)}"></i>${esc(b.domain)} <small>${b.count}</small></li>`).join('')}</ul><h3>여기서 시작해 보세요</h3><div class="atlas-relations">${['6수01-10','6수02-03','9수02-07'].filter(c=>model.byCode.has(c)).map(c=>relationshipButton(c)).join('')}</div><a class="text-link" href="#view=hierarchy">필요한 사고와 과제별 위계 ↗</a>`;
  }
 }
 function update({autoFit=false}={}){
  active=selectNetwork(model,state);trace=traceExpansion({...model,edges:model.edges.filter(e=>active.activeEdges.has(e.id))},state.selected);neighbors=new Set();directEdges=new Set();
  for(const e of model.edges)if(active.activeEdges.has(e.id)&&(e.from===state.selected||e.to===state.selected)){neighbors.add(e.from===state.selected?e.to:e.from);directEdges.add(e.id);}
  const emphasize=new Set([state.selected,...neighbors,...trace.ancestors,...trace.descendants]);
  for(const n of model.nodes){const el=nodeEls.get(n.code),visible=active.activeNodes.has(n.code),selected=n.code===state.selected;el.style.display=visible?'':'none';el.setAttribute('aria-hidden',String(!visible));el.classList.toggle('is-muted',!selected&&(!visible||(!!state.selected&&!emphasize.has(n.code))));el.classList.toggle('is-selected',selected);el.classList.toggle('is-neighbor',neighbors.has(n.code));el.classList.toggle('is-before',trace.ancestors.has(n.code));el.classList.toggle('is-after',trace.descendants.has(n.code));el.classList.toggle('is-match',!!state.query&&visible);el.setAttribute('aria-pressed',String(selected));el.setAttribute('tabindex',selected||(!state.selected&&n===model.nodes.find(x=>active.activeNodes.has(x.code)))?'0':'-1');}
  for(const e of model.edges){const el=edgeEls.get(e.id),visible=active.activeEdges.has(e.id),highlight=directEdges.has(e.id)||trace.edges.has(e.id);el.style.display=visible?'':'none';el.classList.toggle('is-muted',!visible||(!!state.selected&&!highlight));el.classList.toggle('is-active',!!state.selected&&highlight);el.classList.toggle('is-before',trace.edges.has(e.id)&&trace.ancestors.has(e.from));el.classList.toggle('is-after',trace.edges.has(e.id)&&trace.descendants.has(e.to));}
  const count=model.edges.filter(e=>active.activeEdges.has(e.id)).reduce((sum,e)=>sum+e.records.length,0);host.querySelector('.atlas-summary').textContent=`전체 ${model.nodes.length}개 노드 · 현재 범위 ${active.activeNodes.size}개 · 연결 기록 ${count.toLocaleString()}개${state.selected?` · 직접 연결 ${neighbors.size}개`:''}${outsideSelection?' · 이전 목표가 학교급 범위 밖이어서 선택을 해제했습니다.':''}`;
  renderInspector();save();if(autoFit&&active.activeNodes.size)fit(active.activeNodes);
 }
 function choose(code){const fromSearch=!!state.query;state.selected=code;state.query='';form.elements.query.value='';tooltip.hidden=true;update();inspector.scrollTop=0;if(fromSearch)focusSelection();}
 function focusSelection(){const codes=state.selected?new Set([state.selected,...neighbors,...trace.ancestors,...trace.descendants]):active.activeNodes;fit(codes);}
 function showTip(event){const el=event.target.closest('[data-node]');if(!el){tooltip.hidden=true;return;}const n=model.byCode.get(el.dataset.node),rect=svg.getBoundingClientRect();tooltip.textContent=n.code+' · '+n.title;tooltip.hidden=false;tooltip.style.left=Math.max(8,Math.min(event.clientX-rect.left+12,rect.width-270))+'px';tooltip.style.top=Math.max(50,event.clientY-rect.top-38)+'px';}
 host.addEventListener('click',event=>{
  const select=event.target.closest('[data-select]');if(select){choose(select.dataset.select);return;}
  const node=event.target.closest('[data-node]');if(node){if(!moved)choose(node.dataset.node);return;}
  const action=event.target.closest('[data-action]')?.dataset.action;
  if(action==='in')zoom(.75);if(action==='out')zoom(1.33);if(action==='fit')fit();if(action==='focus')focusSelection();
  if(action==='clear'){state.selected='';update();}
  if(action==='reset'){Object.assign(state,{query:'',domain:'',strand:'',relation:'all',selected:''});for(const key of ['query','domain','strand','relation'])form.elements[key].value=state[key];update();fit();}
  if(action==='expand'){const expanded=workspace.classList.toggle('is-expanded');event.target.setAttribute('aria-pressed',String(expanded));event.target.textContent=expanded?'크게 보기 닫기':'크게 보기';requestAnimationFrame(()=>fit());}
 },{signal});
 form.addEventListener('submit',event=>{event.preventDefault();clearTimeout(timer);state.query=form.elements.query.value.trim();state.selected='';update({autoFit:true});},{signal});
 form.addEventListener('input',event=>{if(event.target.name!=='query')return;clearTimeout(timer);timer=setTimeout(()=>{state.query=event.target.value.trim();state.selected='';update({autoFit:true});},180);},{signal});
 form.addEventListener('change',event=>{if(event.target.tagName!=='SELECT')return;state[event.target.name]=event.target.value;state.selected='';update({autoFit:event.target.name!=='relation'});},{signal});
 svg.addEventListener('wheel',event=>{event.preventDefault();const rect=svg.getBoundingClientRect();zoom(Math.exp(Math.max(-.3,Math.min(.3,event.deltaY*.0015))),(event.clientX-rect.left)/rect.width,(event.clientY-rect.top)/rect.height);},{signal,passive:false});
 svg.addEventListener('pointerdown',event=>{if(event.button!==0)return;moved=false;svg.setPointerCapture(event.pointerId);pointers.set(event.pointerId,{x:event.clientX,y:event.clientY});drag={x:event.clientX,y:event.clientY,camera:{...camera},code:event.target.closest('[data-node]')?.dataset.node};if(pointers.size===2){const [a,b]=[...pointers.values()];pinch={distance:Math.hypot(a.x-b.x,a.y-b.y),camera:{...camera},center:{x:(a.x+b.x)/2,y:(a.y+b.y)/2}};}},{signal});
 svg.addEventListener('pointermove',event=>{if(!pointers.has(event.pointerId)){showTip(event);return;}pointers.set(event.pointerId,{x:event.clientX,y:event.clientY});const rect=svg.getBoundingClientRect();if(pointers.size===2&&pinch){const [a,b]=[...pointers.values()],distance=Math.hypot(a.x-b.x,a.y-b.y);camera={...pinch.camera};zoom(pinch.distance/Math.max(distance,1),(pinch.center.x-rect.left)/rect.width,(pinch.center.y-rect.top)/rect.height);moved=true;}else if(drag){const dx=event.clientX-drag.x,dy=event.clientY-drag.y;if(Math.hypot(dx,dy)>3)moved=true;camera={...drag.camera,x:drag.camera.x-dx/rect.width*drag.camera.w,y:drag.camera.y-dy/rect.height*drag.camera.h};cancelAnimationFrame(frame);frame=requestAnimationFrame(drawCamera);}tooltip.hidden=true;},{signal});
 function release(event){if(event.type==='pointerup'&&!moved&&drag?.code)choose(drag.code);pointers.delete(event.pointerId);pinch=null;if(pointers.size){const a=[...pointers.values()][0];drag={...a,camera:{...camera}};}else drag=null;}
 svg.addEventListener('pointerup',release,{signal});svg.addEventListener('pointercancel',release,{signal});svg.addEventListener('pointerleave',()=>{tooltip.hidden=true;},{signal});
 svg.addEventListener('keydown',event=>{
  const node=event.target.closest('[data-node]');
  if(node&&['Enter',' '].includes(event.key)){event.preventDefault();choose(node.dataset.node);return;}
  if(node&&['ArrowDown','ArrowUp','ArrowLeft','ArrowRight'].includes(event.key)){event.preventDefault();const available=model.nodes.filter(n=>active.activeNodes.has(n.code)),index=available.findIndex(n=>n.code===node.dataset.node),direction=['ArrowLeft','ArrowUp'].includes(event.key)?-1:1,next=available[(index+direction+available.length)%available.length];if(next){choose(next.code);nodeEls.get(next.code).focus();}return;}
  if(['+','=','-','0','ArrowLeft','ArrowRight','ArrowUp','ArrowDown','Escape'].includes(event.key))event.preventDefault();
  if(event.key==='+'||event.key==='=')zoom(.8);if(event.key==='-')zoom(1.25);if(event.key==='0')fit();
  if(event.key.startsWith('Arrow')){camera.x+=event.key==='ArrowLeft'?-camera.w*.1:event.key==='ArrowRight'?camera.w*.1:0;camera.y+=event.key==='ArrowUp'?-camera.h*.1:event.key==='ArrowDown'?camera.h*.1:0;drawCamera();}
  if(event.key==='Escape'){state.selected='';update();}
 },{signal});
 let restored=cameras.get(location.hash);if(!restored){try{const saved=JSON.parse(sessionStorage.getItem('atlas-network-camera'));if(saved?.hash===location.hash)restored=saved.camera;}catch{}}
 update();if(restored&&['x','y','w','h'].every(key=>Number.isFinite(restored[key]))&&restored.w>0&&restored.h>0){camera=restored;drawCamera();}else fit();
 let lastSize=svg.getBoundingClientRect();const resize=new ResizeObserver(()=>{const size=svg.getBoundingClientRect();if(Math.abs(size.width-lastSize.width)>2||Math.abs(size.height-lastSize.height)>2){lastSize=size;fit();}});resize.observe(svg);
 document.fonts.ready.then(()=>{if(!signal.aborted)drawStageLabels();});
 return ()=>{abort.abort();resize.disconnect();clearTimeout(timer);cancelAnimationFrame(frame);};
}

