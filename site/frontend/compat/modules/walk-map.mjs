import {standard, standardConnections} from './store.mjs';
import {esc,url} from './ui.mjs';

// The URL holds a discovery tree and any additional edges the visitor traversed.
// Each step names a previously visited source by index and its destination by code.
function pair(a,b) { return [a,b].sort().join('|'); }
export function extendWalk(walk, from, to) {
  return walk.encoded+','+walk.codes.indexOf(from)+':'+to;
}
export async function readWalk(params,current) {
  const saved=params.get('walk');
  const legacy=(params.get('trail')||'').split(',').filter(Boolean);
  const steps=saved?saved.split(','):[...legacy,current].map((c,i)=>i?(i-1)+':'+c:c);
  const root=steps.shift();
  const empty=()=>({codes:[current],edges:[],pairs:new Set(),encoded:current});
  if(!standard(root)||!steps.length)return empty();
  const codes=[root],edges=[],pairs=new Set(),tokens=[root];
  const sources=new Map();
  for(const step of steps){
    const [index,to]=step.split(':');
    const from=codes[index];
    if(!/^\d+$/.test(index)||!from||!standard(to)||from===to)break;
    const key=pair(from,to);
    if(pairs.has(key))continue;
    if(!sources.has(from))sources.set(from,(await standardConnections(from)).relations);
    const records=sources.get(from).filter(r=>
      (r.from==='standard:'+from&&r.to==='standard:'+to)||(r.from==='standard:'+to&&r.to==='standard:'+from));
    if(!records.length)break;
    if(!codes.includes(to))codes.push(to);
    pairs.add(key);
    edges.push({from,to,records});tokens.push(step);
  }
  return codes.includes(current)?{codes,edges,pairs,encoded:tokens.join(',')}:empty();
}
export const traversed=(walk,from,to)=>walk.pairs.has(pair(from,to));

export function drawWalk(walk,current,neighbors,values,reasonPanel) {
  const edges=[...walk.edges,...neighbors.map(n=>({from:current.code,to:n.target.code,records:n.records,fresh:true}))];
  const nodes=new Map();
  function add(code,depth) {
    const n={code,children:[],depth};
    nodes.set(code,n);return n;
  }
  const origin=add(walk.codes[0],0);
  const links=edges.map(edge=>{
    const parent=nodes.get(edge.from);
    const cross=nodes.has(edge.to);
    if(!cross)parent.children.push(add(edge.to,parent.depth+1));
    return {...edge,cross};
  });
  let leaves=0;
  function place(node){
    node.children.forEach(place);
    node.x=node.children.length?(node.children[0].x+node.children.at(-1).x)/2:50+100*leaves++;
    node.y=23+node.depth*134;
  }
  place(origin);
  const crossCount=links.filter(e=>e.cross).length;
  const width=leaves*100+crossCount*38;
  const height=Math.max(...[...nodes.values()].map(n=>n.y))+82;
  let lane=0;
  const panels=[];
  const lines=links.map(({from,to,records,fresh,cross},i)=>{
    const a=nodes.get(from),b=nodes.get(to);
    let path,mx,my;
    if(cross){
      mx=leaves*100+18+38*lane++;
      my=(a.y+b.y)/2+(a.y===b.y?60:0);
      path=`M${a.x} ${a.y} Q${mx} ${a.y} ${mx} ${my} Q${mx} ${b.y} ${b.x} ${b.y}`;
    }else{
      const first=a.y+64,last=b.y-22;
      mx=(a.x+b.x)/2;my=(first+last)/2;
      path=`M${a.x} ${a.y} L${a.x} ${first} L${b.x} ${last} L${b.x} ${b.y}`;
    }
    const title=standard(from).title+' · '+standard(to).title;
    panels.push(reasonPanel(i,title,records));
    return `<g class="local-edge ${fresh?'walk-option':'walk-used'}" role="button" tabindex="0" data-from="${esc(from)}" data-to="${esc(to)}" aria-expanded="false" aria-controls="local-reason-${i}" aria-label="${esc(title)} 연결 이유">
      <path class="edge-hit" d="${path}"/><path class="edge-ink" d="${path}"/>
      <circle class="edge-hit-disc" cx="${mx}" cy="${my}" r="20"/><circle class="edge-mark" cx="${mx}" cy="${my}" r="10"/>
      <text x="${mx}" y="${my}" dy=".35em" text-anchor="middle" aria-hidden="true">?</text></g>`;
  });
  const candidates=new Set(neighbors.map(n=>n.target.code));
  const dots=[...nodes.values()].map(({code,x,y})=>{
    const s=standard(code),active=code===current.code,first=code===origin.code,visited=walk.codes.includes(code);
    const label=active?(first?'출발 · 지금 보는 기준':'지금 보는 기준'):first?'출발점':visited?'지나온 기준':'새 연결';
    const encoded=candidates.has(code)?extendWalk(walk,current.code,code):walk.encoded;
    const attrs=active?'type="button" aria-current="step" aria-controls="local-standard"':`href="${esc(url('network',{...values,node:code,walk:encoded}))}"`;
    const tag=active?'button':'a';
    return `<${tag} ${attrs} class="walk-dot ${active?'walk-active':visited?'walk-visited':'walk-new'}" data-code="${esc(code)}" ${first?'data-origin':''} style="left:${x/width*100}%;top:${y}px" title="${esc(s.title)} · ${esc(code)}">
      <i aria-hidden="true"></i><span><small>${label}</small><strong>${esc(s.title)}</strong></span></${tag}>`;
  });
  return {panels:panels.join(''),board:`<div class="walk-board" tabindex="0" role="region" aria-label="따라온 길과 새 연결 지도">
    <div class="walk-canvas" style="--lanes:${width/100};height:${height}px"><svg class="local-lines" viewBox="0 0 ${width} ${height}" width="100%" height="100%" preserveAspectRatio="none" aria-label="연결 이유를 여는 선">${lines.join('')}</svg>${dots.join('')}</div></div>
    <div class="walk-tools"><button type="button" data-locate="origin">출발점 찾기 · ${esc(standard(origin.code).title)}</button><button type="button" data-locate="active">지금 보는 점 찾기</button></div>`};
}
