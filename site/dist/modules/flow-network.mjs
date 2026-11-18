import {standard,levels} from './store.mjs';
import {esc,url,standardURL} from './ui.mjs';

// The graph uses recorded standard relations only. A path is undirected
// exploration of those records, never a claim about a required learning order.
export function buildConceptNetwork(concept,data,selectedCode='',reach='direct',subject=''){
 const allowed=c=>{const s=standard(c);return !!s&&(!subject||s.level!==levels[2]||s.subject===subject);};
 const own=new Set(concept.stages.flatMap(s=>s.codes).filter(allowed));
 const ids=new Set([...concept.relation_ids,...concept.external_relation_ids]);
 const records=data.relations.filter(r=>ids.has(r.id)&&r.from.startsWith('standard:')&&r.to.startsWith('standard:')&&allowed(r.from.slice(9))&&allowed(r.to.slice(9)));
 const universe=new Set([...own,...records.flatMap(r=>[r.from.slice(9),r.to.slice(9)])]);
 const selected=universe.has(selectedCode)?selectedCode:'';
 const distance=new Map(selected?[[selected,0]]:[]),adjacency=new Map();
 for(const r of records){
  const a=r.from.slice(9),b=r.to.slice(9);
  if(selected&&a!==b&&(a===selected||b===selected))distance.set(a===selected?b:a,1);
  if(own.has(a)&&own.has(b)||a===selected||b===selected){
   if(!adjacency.has(a))adjacency.set(a,new Set());if(!adjacency.has(b))adjacency.set(b,new Set());
   adjacency.get(a).add(b);adjacency.get(b).add(a);
  }
 }
 if(selected&&reach==='path'){
  distance.clear();distance.set(selected,0);const queue=[selected];
  for(let i=0;i<queue.length;i++)for(const next of adjacency.get(queue[i])||[])if(!distance.has(next)){distance.set(next,distance.get(queue[i])+1);queue.push(next);}
 }
 const visible=new Set([...own,...distance.keys()]);
 const nodes=[...visible].map(code=>({code,standard:standard(code),external:!own.has(code),distance:distance.get(code),selected:code===selected}));
 const rank=n=>!selected?0:n.selected?0:n.distance===1?1:n.distance>1?2:3;
 const lanes=levels.map(level=>nodes.filter(n=>n.standard.level===level).sort((a,b)=>rank(a)-rank(b)||Number(a.external)-Number(b.external)||a.code.localeCompare(b.code,'ko',{numeric:true})));
 lanes.forEach((lane,i)=>lane.forEach((n,j)=>Object.assign(n,{x:20+i*320,y:24+j*104,width:280,height:84})));
 const grouped=new Map();
 for(const r of records){
  const a=r.from.slice(9),b=r.to.slice(9);if(!visible.has(a)||!visible.has(b)||a===b)continue;
  const key=[a,b].sort().join('|');if(!grouped.has(key))grouped.set(key,{a,b,records:[]});grouped.get(key).records.push(r);
 }
 const edges=[...grouped.values()].map(e=>({...e,direct:!!selected&&(e.a===selected||e.b===selected),traced:!!selected&&reach==='path'&&distance.has(e.a)&&distance.has(e.b),directional:e.records.every(r=>r.type==='generalizes'&&r.from==='standard:'+e.a&&r.to==='standard:'+e.b)}));
 return {selected,reach,own,nodes,lanes,edges,distance,width:960,height:Math.max(260,...lanes.map(l=>l.length*104+28)),records};
}

function curve(a,b){
 const ay=a.y+a.height/2,by=b.y+b.height/2;
 if(a.x===b.x){const x=a.x+a.width;return `M${x},${ay} C${x+16},${ay} ${x+16},${by} ${x},${by}`;}
 // A link that skips a school lane runs through the row and column gutters,
 // so it cannot look like it terminates at an unrelated middle-school card.
 if(Math.abs(a.x-b.x)>320){
  const left=a.x<b.x?a:b,right=a.x<b.x?b:a,x1=left.x+left.width,x2=right.x,y1=left.y+left.height/2,y2=right.y+right.height/2,track=Math.min(left.y,right.y)-10;
  return a.x<b.x?`M${x1},${y1} C${x1+10},${y1} ${x1+10},${track} ${x1+20},${track} H${x2-20} C${x2-10},${track} ${x2-10},${y2} ${x2},${y2}`:`M${x2},${y2} C${x2-10},${y2} ${x2-10},${track} ${x2-20},${track} H${x1+20} C${x1+10},${track} ${x1+10},${y1} ${x1},${y1}`;
 }
 const ax=a.x<b.x?a.x+a.width:a.x,bx=a.x<b.x?b.x:b.x+b.width,mid=(ax+bx)/2;
 return `M${ax},${ay} C${mid},${ay} ${mid},${by} ${bx},${by}`;
}

export function conceptNetwork(t,data,p,params){
 const reach=p.get('flowReach')==='path'?'path':'direct';
 const g=buildConceptNetwork(t,data,p.get('flowNode'),reach,params.subject),selected=g.selected&&standard(g.selected);
 const graphURL=(node,mode=reach)=>url('overview',{...params,strand:t.id,flowNode:node,flowReach:mode==='path'?'path':'',edgeCode:'',edgeScope:node?'all':''});
 const byCode=new Map(g.nodes.map(n=>[n.code,n]));
 const direct=[...g.distance.values()].filter(d=>d===1).length,indirect=[...g.distance.values()].filter(d=>d>1).length;
 return `<section class="flow-network ${selected?'has-selection':''}" aria-labelledby="network-title-${t.id}" data-network="${t.id}" data-selected-code="${esc(g.selected)}">
 <header class="network-heading"><div><p class="eyebrow">STANDARD CONNECTIONS</p><h4 id="network-title-${t.id}">성취기준 연결 지도</h4><p>기준을 누르면 연결된 초·중·고 기준이 강조됩니다. 여러 기록이 있는 두 기준은 한 선으로 묶었습니다.</p></div><a href="${graphURL('')}" class="button quiet" data-keep-scroll>선택 해제 · 전체 연결</a></header>
 <div class="network-toolbar"><nav aria-label="강조할 연결 범위"><a href="${graphURL(g.selected,'direct')}" ${reach==='direct'?'aria-current="true"':''} data-keep-scroll>직접 연결</a><a href="${graphURL(g.selected,'path')}" ${reach==='path'?'aria-current="true"':''} data-keep-scroll>개념 안에서 연결 따라가기</a></nav><span>● 선택 기준 <b>━</b> 직접 연결 <i>┄</i> 여러 연결을 거침</span></div>
 <div class="network-selection" role="status" aria-live="polite">${selected?`<div><span>선택한 성취기준</span><strong>${esc(selected.code)} · ${esc(selected.title)}</strong><p>직접 연결 <b>${direct}</b>개${reach==='path'?` · 여러 연결을 거쳐 <b>${indirect}</b>개`:''} · 연결되지 않은 기준은 흐리게 표시합니다.</p></div><a class="text-link" href="${standardURL(selected.code)}" data-standard="${esc(selected.code)}" data-focus-key="network-detail:${t.id}:${esc(selected.code)}">선택 기준 상세 읽기 ↗</a>`:`<div><strong>이 개념의 성취기준 ${g.own.size}개 · 기준 사이 연결 ${g.edges.length}쌍</strong><p>기준 하나를 선택해 보세요. 다른 개념에 속한 직접 연결 기준도 함께 나타납니다.</p></div>`}</div>
 <p class="network-scroll-hint" id="network-help-${t.id}">지도를 가로·세로로 이동할 수 있습니다. 선택하면 연결된 기준을 각 학교급의 위쪽에 모아 보여줍니다.</p>
 <div class="network-scroll" tabindex="0" role="region" aria-label="${esc(t.title)} 성취기준 연결 지도" aria-describedby="network-help-${t.id}" data-scroll-key="network:${t.id}">
 <div class="network-board" style="width:${g.width}px"><div class="network-schools">${levels.map((level,i)=>{const active=g.lanes[i].filter(n=>n.distance>0).length;return `<div class="network-school school-${i}"><strong>${level}</strong><span>${selected?`연결된 기준 ${active}개`:`이 개념의 기준 ${g.lanes[i].length}개`}</span></div>`;}).join('')}</div>
 <div class="network-canvas" style="height:${g.height}px">
 <svg class="network-lines" width="${g.width}" height="${g.height}" viewBox="0 0 ${g.width} ${g.height}" aria-hidden="true" focusable="false"><defs><marker id="network-arrow-${t.id}" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 0 L8 4 L0 8z" fill="context-stroke"/></marker></defs>${[...g.edges].sort((a,b)=>Number(a.direct||a.traced)-Number(b.direct||b.traced)).map(e=>`<path data-network-edge="${esc(e.records.map(r=>r.id).join(' '))}" data-edge-from="${esc(e.a)}" data-edge-to="${esc(e.b)}" class="network-edge ${selected?(e.direct?'is-direct':e.traced?'is-traced':'is-muted'):''}" d="${curve(byCode.get(e.a),byCode.get(e.b))}" ${e.directional?`marker-end="url(#network-arrow-${t.id})"`:''}/>`).join('')}</svg>
 ${g.lanes.map((lane,i)=>lane.length?lane.map(n=>`<a class="network-node ${n.selected?'is-current':selected?(n.distance===1?'is-direct':n.distance>1?'is-traced':'is-muted'):''} ${n.external?'is-external':''}" style="left:${n.x}px;top:${n.y}px;width:${n.width}px;height:${n.height}px" href="${graphURL(n.code)}" data-flow-select data-node-code="${esc(n.code)}" data-focus-key="network:${t.id}:${esc(n.code)}" data-keep-scroll ${n.selected?'aria-current="true"':''} aria-label="${esc(n.code+' '+n.standard.title+' · '+(n.selected?'선택됨':n.distance===1?'직접 연결 · ':n.distance>1?'여러 연결을 거침 · ':'')+'연결 강조하기')}"><span class="network-code">${esc(n.code)}<em>${n.selected?'선택':n.distance===1?'직접 연결':n.distance>1?`${n.distance}개 연결 거침`:''}</em></span><strong>${esc(n.standard.title)}</strong><small>${esc(n.standard.level===levels[2]?n.standard.subject:n.standard.band)}${n.external?' · 다른 개념':''}</small></a>`).join(''):`<p class="network-empty" style="left:${20+i*320}px">${selected?'선택 기준과 연결된 기록이 없습니다.':'이 개념에 직접 분류된 기준이 없습니다. 다른 학교급의 기준을 선택해 연결을 확인하세요.'}</p>`).join('')}
 </div></div></div>
 <p class="network-note">선은 기록된 관계를 나타내며 필수 학습 순서를 뜻하지 않습니다. 직접 연결은 두 기준 사이의 기록을 뜻하며, 해당 기록에 중간 학습이 포함될 수 있습니다. 화살표는 ‘의미 확장’입니다. 다른 개념의 기준은 점선 테두리로 표시합니다. 아래 연결 근거에서 조건과 출처를 확인하세요.${reach==='path'?' ‘연결 따라가기’는 같은 개념 안의 관계를 방향과 무관하게 탐색하며, 다른 개념의 기준은 선택 기준의 직접 연결만 포함합니다.':''}</p>
 </section>`;
}
