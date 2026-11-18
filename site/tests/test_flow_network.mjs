import fs from 'node:fs/promises';
import path from 'node:path';
import assert from 'node:assert/strict';
import {fileURLToPath} from 'node:url';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..'),dist=path.join(root,'dist');
globalThis.fetch=async raw=>({ok:true,json:async()=>JSON.parse(await fs.readFile(path.join(dist,decodeURIComponent(String(raw).split('?')[0])),'utf8'))});
globalThis.window={};
const store=await import('../dist/modules/store.mjs');await store.initialize();
const {buildConceptNetwork,conceptNetwork}=await import('../dist/modules/flow-network.mjs');
const flows=await store.conceptFlows(),data=await store.connections();
let nodesChecked=0,edgesChecked=0;
for(const t of flows.strands){
 const own=new Set(t.stages.flatMap(s=>s.codes));
 const g=buildConceptNetwork(t,data);
 assert.deepEqual(new Set(g.nodes.map(n=>n.code)),own,'Unselected map contains every concept criterion');
 const ids=new Set([...t.relation_ids,...t.external_relation_ids]);
 for(const edge of g.edges)for(const r of edge.records){assert(ids.has(r.id));assert(own.has(r.from.slice(9))&&own.has(r.to.slice(9)));edgesChecked++;}
 for(const code of own){
  const g=buildConceptNetwork(t,data,code),expected=new Set(data.relations.filter(r=>ids.has(r.id)&&[r.from,r.to].includes('standard:'+code)).flatMap(r=>[r.from.slice(9),r.to.slice(9)]));expected.add(code);
  assert.deepEqual(new Set(g.distance.keys()),expected,`${t.id}/${code} direct neighbors`);
  for(const node of g.nodes){assert.equal(node.selected,node.code===code);assert.equal(node.distance===1,expected.has(node.code)&&node.code!==code);assert(own.has(node.code)||expected.has(node.code),'Only actual external neighbors are added');nodesChecked++;}
  for(const level of g.lanes){const highlighted=level.filter(n=>n.distance!==undefined);assert.deepEqual(level.slice(0,highlighted.length),highlighted,'Highlight is visible at top of every school lane');}
  const walked=buildConceptNetwork(t,data,code,'path');
  for(const [target,d] of walked.distance){
   if(d===0){assert.equal(target,code);continue;}
   assert(data.relations.some(r=>ids.has(r.id)&&[r.from,r.to].includes('standard:'+target)&&walked.distance.get((r.from==='standard:'+target?r.to:r.from).slice(9))===d-1),'Every highlighted path step has a real recorded relation');
  }
 }
 const html=conceptNetwork(t,data,new URLSearchParams(),{});
 assert(html.includes('data-network="'+t.id+'"'));assert(!html.includes('undefined')&&!html.includes('NaN'));
 assert.equal((html.match(/data-node-code=/g)||[]).length,own.size);
 assert.equal(buildConceptNetwork(t,data,'invalid-code').selected,'');
}
const ratio=flows.strands.find(t=>t.id==='ratio');
const direct=buildConceptNetwork(ratio,data,'6수02-03');
assert.deepEqual(new Set(direct.nodes.filter(n=>n.distance!==undefined).map(n=>n.standard.level)),new Set(store.levels));
assert(direct.nodes.some(n=>n.external),'Cross-concept neighbors must be shown');
const matrix=flows.strands.find(t=>t.id==='matrix');
assert(matrix.stages[0].codes.length===0);
const matrixSeed=matrix.stages[2].codes.find(c=>buildConceptNetwork(matrix,data,c).lanes[0].length);
assert(matrixSeed,'A high-only concept still reveals its recorded elementary connections');
const subject='공통수학2',filtered=buildConceptNetwork(ratio,data,'6수02-03','path',subject);
assert(filtered.nodes.filter(n=>n.standard.level==='고등학교').every(n=>n.standard.subject===subject));
// A cycle and two records for the same pair must not invent nodes or distances.
const sample={stages:[{codes:['6수02-02','6수02-03']},{codes:['9수02-07']},{codes:[]}],relation_ids:['a','b','c','d'],external_relation_ids:[]};
const sampleData={relations:[['a','6수02-02','6수02-03'],['b','6수02-03','9수02-07'],['c','6수02-02','6수02-03'],['d','9수02-07','6수02-02']].map(([id,a,b])=>({id,from:'standard:'+a,to:'standard:'+b,type:'meaning_connection'}))};
const cycle=buildConceptNetwork(sample,sampleData,'6수02-02','path');assert.equal(cycle.edges.length,3);assert.equal(cycle.distance.size,3);assert.equal(cycle.distance.get('9수02-07'),1);
console.log(JSON.stringify({status:'pass',concepts:46,selectableMemberships:482,nodeStatesChecked:nodesChecked,recordedEdgesChecked:edgesChecked,checks:'complete concept nodes, exact direct neighbors, real indirect paths, cross-school highlight, external concepts, course scope, cycle handling, pair grouping, empty and invalid selections'}));
