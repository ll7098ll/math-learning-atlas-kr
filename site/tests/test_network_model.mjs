import fs from 'node:fs/promises';
import path from 'node:path';
import assert from 'node:assert/strict';
import {fileURLToPath} from 'node:url';
import {buildNetwork,selectNetwork,traceExpansion,NETWORK_DOMAINS} from '../dist/modules/network-model.mjs';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const read=async name=>JSON.parse(await fs.readFile(path.join(root,'dist/content',name+'.json'),'utf8'));
const [catalog,flows,connections]=await Promise.all(['catalog','flows','connections'].map(read));
const originalCorpus=JSON.parse(await fs.readFile(path.join(root,'../data/relations.json'),'utf8'));
const originalIds=new Set(originalCorpus.relations.filter(r=>r.from.startsWith('standard:')&&r.to.startsWith('standard:')).map(r=>r.id));
const model=buildNetwork(catalog,flows,connections);
assert.equal(model.nodes.length,435);assert.equal(model.byCode.size,435);
assert.deepEqual(new Set(model.nodes.map(n=>n.code)),new Set(catalog.standards.map(s=>s.code)));
assert.equal(model.stages.length,6);assert.deepEqual(model.bands.map(b=>b.domain),NETWORK_DOMAINS);
assert.equal(model.width,1800);assert(model.height>=1100&&model.height<=1500);
assert.equal(new Set(model.nodes.map(n=>`${n.x},${n.y}`)).size,435,'Node centers never overlap');
for(const node of model.nodes){
 const stage=model.stages[node.stage],band=model.bands.find(b=>b.domain===node.domain);
 assert(node.x>stage.x&&node.x<stage.x+stage.width);assert(node.y>band.y&&node.y<band.y+band.height);
 const strand=flows.strands.find(t=>t.id===node.strandId);
 assert(strand.stages.some(s=>s.primary_codes.includes(node.code)));
 assert.equal(node.domain,strand.domain);
}
assert.deepEqual(model.stages.map(s=>s.count),[29,47,45,60,73,181]);
const expectedRecords=connections.relations.filter(r=>r.from.startsWith('standard:')&&r.to.startsWith('standard:'));
assert.equal(originalIds.size,1518);assert.deepEqual(new Set(expectedRecords.filter(r=>originalIds.has(r.id)).map(r=>r.id)),originalIds);
assert.equal(model.edges.reduce((count,edge)=>count+edge.records.length,0),expectedRecords.length);
assert.deepEqual(new Set(model.edges.flatMap(e=>e.records.map(r=>r.id))),new Set(expectedRecords.map(r=>r.id)));
for(const edge of model.edges){
 for(const record of edge.records){assert.equal(record.from,'standard:'+edge.from);assert.equal(record.to,'standard:'+edge.to);assert.equal(record.type,edge.type);}
 if(edge.type==='generalizes'&&edge.records.every(r=>originalIds.has(r.id)))assert(model.byCode.get(edge.from).stage<model.byCode.get(edge.to).stage,'Every recorded expansion follows educational stages');
}
const reversed=buildNetwork({...catalog,standards:[...catalog.standards].reverse()},flows,{...connections,relations:[...connections.relations].reverse()});
assert.deepEqual(reversed.nodes,model.nodes);assert.deepEqual(reversed.edges,model.edges);
const all=selectNetwork(model);assert.equal(all.activeNodes.size,435);assert.equal(all.activeEdges.size,model.edges.length);
const onlyExpansion=selectNetwork(model,{relation:'generalizes',selected:'6수02-03'});
assert.equal(onlyExpansion.activeNodes.size,435,'Relation choice preserves isolated nodes');
assert([...onlyExpansion.activeEdges].every(id=>model.byEdge.get(id).type==='generalizes'));
for(const domain of NETWORK_DOMAINS){
 const filtered=selectNetwork(model,{domain});assert.equal(filtered.activeNodes.size,model.nodes.filter(n=>n.domain===domain).length);
 for(const id of filtered.activeEdges){const e=model.byEdge.get(id);assert(filtered.activeNodes.has(e.from)&&filtered.activeNodes.has(e.to));}
 assert.deepEqual(selectNetwork(model,{domain,selected:'6수02-03'}).activeNodes,filtered.activeNodes,'Selection must not change the map filter');
}
for(const strand of flows.strands){
 const filtered=selectNetwork(model,{strand:strand.id});
 assert.deepEqual(filtered.activeNodes,new Set(strand.stages.flatMap(s=>s.codes)),'Concept selection includes additional memberships without duplicating nodes');
}
for(const standard of catalog.standards){
 const found=selectNetwork(model,{query:standard.code});assert(found.activeNodes.has(standard.code));
}
assert.equal(selectNetwork(model,{query:'not-a-real-criterion-code'}).activeNodes.size,0);
assert.equal(selectNetwork(model,{domain:'수와 연산',query:'6수02-03'}).activeNodes.size,0);
assert.equal(selectNetwork(model,{selected:'invalid'}).selected,'');
const trace=traceExpansion(model,'6수02-03');
assert(trace.descendants.has('9수02-07'));assert(!trace.descendants.has('6수02-03'));assert(!trace.ancestors.has('6수02-03'));
for(const id of trace.edges)assert(['generalizes','requires_for_task'].includes(model.byEdge.get(id).type));
const a='2수01-01',b='4수01-01',c='6수01-01',d='9수01-01';
const synthetic={relations:[
 {id:'ab1',from:'standard:'+a,to:'standard:'+b,type:'generalizes'},
 {id:'ab2',from:'standard:'+a,to:'standard:'+b,type:'generalizes'},
 {id:'bc',from:'standard:'+b,to:'standard:'+c,type:'generalizes'},
 {id:'ca',from:'standard:'+c,to:'standard:'+a,type:'generalizes'},
 {id:'ad',from:'standard:'+a,to:'standard:'+d,type:'meaning_connection'},
 {id:'ba',from:'standard:'+b,to:'standard:'+a,type:'meaning_connection'},
 {id:'ab3',from:'standard:'+a,to:'standard:'+b,type:'meaning_connection'}
]};
const cycle=buildNetwork(catalog,flows,synthetic);assert.equal(cycle.edges.length,6,'Only identical type and direction are merged');
const cycled=traceExpansion(cycle,a);assert.deepEqual(cycled.ancestors,new Set([c,b]));assert.deepEqual(cycled.descendants,new Set([b,c]));assert.equal(cycled.edges.size,3);assert(!cycled.descendants.has(d));
const absent=traceExpansion(model,'invalid');assert.equal(absent.ancestors.size+absent.descendants.size+absent.edges.size,0);
console.log(JSON.stringify({status:'pass',nodes:model.nodes.length,relations:expectedRecords.length,edges:model.edges.length,width:model.width,height:model.height,checks:'coverage, unique positions, stage direction, primary domains, stable layout, record preservation, additional memberships, filters, isolated nodes, cycle-safe directed expansion'}));
