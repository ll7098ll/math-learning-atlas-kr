import fs from 'node:fs/promises';
import path from 'node:path';
import assert from 'node:assert/strict';
import {directionGraph} from '../dist/modules/hierarchy-graph.mjs';
const dist=path.resolve(import.meta.dirname,'../dist');
const read=async file=>JSON.parse(await fs.readFile(path.join(dist,file),'utf8'));
globalThis.fetch=async raw=>({ok:true,json:()=>read(decodeURIComponent(String(raw).split('?')[0]))});
globalThis.window={};
const store=await import('../dist/modules/store.mjs');await store.initialize();
const {renderHierarchyPaths}=await import('../dist/modules/hierarchy-path-view.mjs');
const index=await store.conceptPathwaysIndex(),graph=await store.hierarchyGraph();
assert.equal(graph.nodes.length,435);assert.equal(graph.version,index.version);
const edge=(a,b,type='generalizes')=>({id:a+b,from:'standard:'+a,to:'standard:'+b,type});
const fake=relations=>({nodes:['A','B','C','D','E'],relations});
const chain=fake([edge('A','B'),edge('B','C'),edge('C','D'),edge('E','C','meaning_connection')]);
assert.deepEqual([...directionGraph(chain,'D',2).before.distances],[['C',1],['B',2]]);
assert.deepEqual(directionGraph(chain,'D','all').before.paths.get('A').map(r=>r.id),['AB','BC','CD']);
assert.deepEqual(directionGraph(chain,'A','all').after.paths.get('D').map(r=>r.id),['AB','BC','CD']);
assert(!directionGraph(chain,'C').before.distances.has('E'));
assert.equal(directionGraph(fake([edge('A','B'),edge('B','C'),edge('C','A')]),'A').cyclic.size,3);
assert.equal(directionGraph(fake([edge('A','A')]),'A').cycles.length,1);
assert.equal(directionGraph(fake([{...edge('A','B'),review_state:'candidate'}]),'B').before.distances.size,0);
assert.throws(()=>directionGraph(chain,'missing'),/등록되지/);
const diamond=directionGraph(fake([edge('A','B'),edge('A','C'),edge('B','D'),edge('C','D')]),'D','all');
assert.equal(diamond.before.distances.size,3);assert.equal(diamond.edges.length,4);
let renders=0;
for(const g of index.groups){
 const data=await store.conceptPathway(g.id);
 for(const target of g.member_codes){
  const model=directionGraph(graph,target,'all');assert.equal(model.cycles.length,0);
  for(const [side,backwards] of [[model.before,true],[model.after,false]])for(const [code,records] of side.paths){
   assert.equal(records.length,side.distances.get(code));
   assert.equal(records[0].from.slice(9),backwards?code:target);
   assert.equal(records.at(-1).to.slice(9),backwards?target:code);
   for(let i=1;i<records.length;i++)assert.equal(records[i-1].to,records[i].from);
  }
  for(const scope of ['all','e','m','h']){
   const html=renderHierarchyPaths(new URLSearchParams({target,scope,depth:'all'}),data,index,graph);
   assert(html.includes(`data-path-node="${target}"`));assert(!html.includes('undefined'));
   for(const code of [...model.before.distances.keys(),...model.after.distances.keys()])assert(html.includes(`data-path-node="${code}"`));
   renders++;
  }
 }
}
for(const target of Object.keys(graph.standard_decisions||{})){
 const group=index.groups.find(g=>g.member_codes.includes(target)),data=await store.conceptPathway(group.id);
 const html=renderHierarchyPaths(new URLSearchParams({target,scope:'all'}),data,index,graph);
 assert(html.includes('data-order-decision'));assert(html.includes('순서 없이 함께 살펴볼 기준'));assert(html.includes(graph.standard_decisions[target].relation_ids[0]));
 assert(!html.includes('이 목표로 들어오는 방향 관계는 미기록 또는 미검토입니다.'));
}
const {connectionsPage}=await import('../dist/modules/explore.mjs');
const {esc}=await import('../dist/modules/ui.mjs');
const authored=(await read('content/connections.json')).relations.filter(r=>r.authored_from?.startsWith('data/hierarchy_'));
for(const r of authored){
 const html=await connectionsPage(new URLSearchParams({code:r.to.slice(9),scope:'all',type:r.type,relation:r.id}));
 assert(html.includes(['generalizes','requires_for_task'].includes(r.type)?'<span>↓</span>':'<span>↔</span>'),r.id);assert(html.includes('type=requires_for_task'));
 assert(html.includes(esc(r.diagnostic))&&html.includes(esc(r.expected_response))&&html.includes(esc(r.alternative_route)),r.id);
}
console.log(JSON.stringify({status:'pass',standards:435,relations:graph.relations.length,renders,checks:'transitive witnesses, arbitrary cycles, diamond sharing, depth bounds, candidates, semantic separation, all targets and school scopes'}));
