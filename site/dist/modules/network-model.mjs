// Educational position and recorded relations are separate: subcolumns inside
// a stage are only packing, and only generalizes edges carry expansion order.
export const NETWORK_DOMAINS=['수와 연산','변화와 관계','도형과 측정','자료와 가능성','활용과 탐구'];
const stageDefinitions=[
 {id:'elementary-12',title:'초등 1–2',label:'초등 1–2학년군',width:210,columns:3},
 {id:'elementary-34',title:'초등 3–4',label:'초등 3–4학년군',width:210,columns:3},
 {id:'elementary-56',title:'초등 5–6',label:'초등 5–6학년군',width:210,columns:3},
 {id:'middle',title:'중학교',label:'중학교 1–3학년군',width:220,columns:3},
 {id:'high-common',title:'고교 공통',label:'고등학교 공통 과목',width:290,columns:4},
 {id:'high-elective',title:'고교 선택',label:'고등학교 선택 과목 · 병렬 분기',width:440,columns:5}
];
const compare=(a,b)=>String(a).localeCompare(String(b),'ko',{numeric:true});
const normalize=value=>String(value||'').trim().normalize('NFKC').toLocaleLowerCase('ko');

function stageOf(s){
 if(s.level==='초등학교'){
  const index={'1~2학년군':0,'3~4학년군':1,'5~6학년군':2}[s.band];
  if(index!==undefined)return index;
 }
 if(s.level==='중학교')return 3;
 if(s.level==='고등학교')return s.category==='공통'?4:5;
 throw new Error(`교육과정 위치를 확인할 수 없습니다: ${s.code}`);
}

export function buildNetwork(catalog,flows,connections){
 const primary=new Map(),memberships=new Map(),strandOrder=new Map();
 flows.strands.forEach((strand,index)=>{
  strandOrder.set(strand.id,index);
  for(const stage of strand.stages){
   for(const code of stage.codes){
    if(!memberships.has(code))memberships.set(code,new Set());
    memberships.get(code).add(strand.id);
   }
   for(const code of stage.primary_codes){
    if(primary.has(code)&&primary.get(code).id!==strand.id)throw new Error(`주 개념이 중복되었습니다: ${code}`);
    primary.set(code,strand);
   }
  }
 });
 const nodes=catalog.standards.map(standard=>{
  const strand=primary.get(standard.code);
  if(!strand||!NETWORK_DOMAINS.includes(strand.domain))throw new Error(`주 개념 분류를 확인할 수 없습니다: ${standard.code}`);
  return {id:standard.code,code:standard.code,title:standard.title,standard,stage:stageOf(standard),domain:strand.domain,strandId:strand.id,strandTitle:strand.title,strandIds:[...(memberships.get(standard.code)||new Set([strand.id]))],x:0,y:0};
 }).sort((a,b)=>NETWORK_DOMAINS.indexOf(a.domain)-NETWORK_DOMAINS.indexOf(b.domain)||a.stage-b.stage||strandOrder.get(a.strandId)-strandOrder.get(b.strandId)||compare(a.standard.subject,b.standard.subject)||compare(a.code,b.code));
 const byCode=new Map(nodes.map(n=>[n.code,n]));
 if(byCode.size!==nodes.length)throw new Error('성취기준 코드가 중복되었습니다.');
 let left=160;
 const stages=stageDefinitions.map((definition,index)=>{
  const stage={...definition,index,x:left,center:left+definition.width/2,count:nodes.filter(n=>n.stage===index).length};
  left+=definition.width;return stage;
 });
 let top=90;
 const bands=NETWORK_DOMAINS.map(domain=>{
  const cells=stages.map(stage=>nodes.filter(n=>n.domain===domain&&n.stage===stage.index));
  const rows=Math.max(3,...cells.map((cell,i)=>Math.ceil(cell.length/stages[i].columns)));
  const band={domain,y:top,height:40+rows*22,count:cells.reduce((sum,cell)=>sum+cell.length,0)};
  cells.forEach((cell,i)=>{
   const stage=stages[i],columns=Math.min(stage.columns,cell.length);
   cell.forEach((node,index)=>{
    const column=index%columns,row=Math.floor(index/columns);
    node.x=columns===1?stage.center:stage.x+38+column*(stage.width-76)/(columns-1);
    node.y=top+30+row*22;
   });
  });
  top+=band.height;return band;
 });
 const grouped=new Map();
 for(const record of connections.relations){
  if(!record.from.startsWith('standard:')||!record.to.startsWith('standard:'))continue;
  const from=record.from.slice(9),to=record.to.slice(9);
  if(!byCode.has(from)||!byCode.has(to))continue;
  const id=`${record.type}:${from}>${to}`;
  if(!grouped.has(id))grouped.set(id,{id,from,to,type:record.type,records:[]});
  grouped.get(id).records.push(record);
 }
 const edges=[...grouped.values()].sort((a,b)=>compare(a.id,b.id));
 for(const edge of edges)edge.records.sort((a,b)=>compare(a.id,b.id));
 return {nodes,edges,stages,bands,width:1800,height:top+40,byCode,byEdge:new Map(edges.map(e=>[e.id,e]))};
}

export function selectNetwork(model,{domain='',strand='',query='',relation='all',selected=''}={}){
 const terms=normalize(query).split(/\s+/u).filter(Boolean);
 const matchedNodes=new Set(model.nodes.filter(node=>{
  if(domain&&node.domain!==domain||strand&&!node.strandIds.includes(strand))return false;
  const s=node.standard,text=normalize([node.code,node.title,s.statement,s.subject,s.band,node.domain,node.strandTitle,s.searchTerms].join(' '));
  return terms.every(term=>text.includes(term));
 }).map(n=>n.code));
 // Keep matching isolated nodes: a relation filter changes the lines, not the
 // set of criteria. A selected node never silently overrides user filters.
 const activeNodes=new Set(matchedNodes);
 const activeEdges=new Set(model.edges.filter(edge=>activeNodes.has(edge.from)&&activeNodes.has(edge.to)&&(!relation||relation==='all'||edge.type===relation)).map(e=>e.id));
 return {activeNodes,activeEdges,matchedNodes,selected:model.byCode.has(selected)?selected:''};
}

export function traceExpansion(model,code){
 const ancestors=new Set(),descendants=new Set(),edges=new Set();
 if(!model.byCode.has(code))return {ancestors,descendants,edges};
 const outgoing=new Map(),incoming=new Map();
 for(const edge of model.edges){
  if(!['generalizes','requires_for_task'].includes(edge.type))continue;
  if(!outgoing.has(edge.from))outgoing.set(edge.from,[]);
  if(!incoming.has(edge.to))incoming.set(edge.to,[]);
  outgoing.get(edge.from).push(edge);incoming.get(edge.to).push(edge);
 }
 const walk=(adjacency,target,endpoint)=>{
  const visited=new Set([code]),queue=[code];
  for(let index=0;index<queue.length;index++){
   for(const edge of adjacency.get(queue[index])||[]){
    edges.add(edge.id);
    const next=edge[endpoint];
    if(visited.has(next))continue;
    visited.add(next);target.add(next);queue.push(next);
   }
  }
 };
 walk(incoming,ancestors,'from');walk(outgoing,descendants,'to');
 return {ancestors,descendants,edges};
}
