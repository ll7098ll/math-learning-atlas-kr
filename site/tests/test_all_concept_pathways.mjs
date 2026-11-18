import fs from 'node:fs/promises';
import path from 'node:path';
import assert from 'node:assert/strict';
const dist=path.resolve(import.meta.dirname,'../dist');
const read=async name=>JSON.parse(await fs.readFile(path.join(dist,name),'utf8'));
const requests=[];
globalThis.fetch=async raw=>{const name=decodeURIComponent(String(raw).split('?')[0]);requests.push(name);return {ok:true,json:()=>read(name)};};
globalThis.window={};
const store=await import('../dist/modules/store.mjs');await store.initialize();
const {conceptNeighborhood,renderConceptPathway,relationReviewHTML,reviewStateLabels}=await import('../dist/modules/concept-pathways.mjs');
const {hierarchyHome}=await import('../dist/modules/pathways.mjs');
const index=await store.conceptPathwaysIndex(),flows=await store.conceptFlows(),pilot=await store.hierarchy();
assert.equal(index.groups.length,46);assert.equal(index.coverage.independently_reviewed_hierarchies,0);
const registry=JSON.parse(await fs.readFile(path.resolve(dist,'../../data/hierarchy_review_registry.json'),'utf8'));
const originals=new Map((await read('content/connections.json')).relations.map(r=>[r.id,r]));
const standards=new Set(),records=new Set();let rendered=0,withExpansion=0,withoutExpansion=0;
for(const g of index.groups){
 const [data,again]=await Promise.all([store.conceptPathway(g.id),store.conceptPathway(g.id)]);assert.strictEqual(data,again);
 assert.equal(data.version,index.version);assert.equal(data.concept.id,g.id);assert.equal(g.reviewed,0);
 if(g.expansions)withExpansion++;else withoutExpansion++;
 const ids=new Set(data.nodes.map(n=>n.id));
 for(const node of data.nodes){assert.equal(node.hierarchy_review,registry.standards[node.id]?.state||'unreviewed');assert.equal(node.goal_analysis_review,registry.standards[node.id]?.goal_analysis?.review_state||'unreviewed');assert.equal(node.goal_analysis_scope,registry.standards[node.id]?.goal_analysis?.scope||'');}
 for(const code of g.member_codes){assert(ids.has(code));standards.add(code);const n=conceptNeighborhood(data,code);assert.equal(n.target,code);for(const c of n.before)assert(n.edges.some(r=>['generalizes','requires_for_task'].includes(r.type)&&r.from==='standard:'+c&&r.to==='standard:'+code));for(const c of n.after)assert(n.edges.some(r=>['generalizes','requires_for_task'].includes(r.type)&&r.to==='standard:'+c&&r.from==='standard:'+code));}
 const expected=[...originals.values()].filter(r=>r.from.startsWith('standard:')&&r.to.startsWith('standard:')&&(g.member_codes.includes(r.from.slice(9))||g.member_codes.includes(r.to.slice(9))));
 assert.deepEqual(data.relations.map(r=>r.id),expected.map(r=>r.id));
 for(const r of data.relations){const original=originals.get(r.id);assert(original);const review=registry.relations[r.id]||{};const expected={...original,hierarchy_review:review.state??original.hierarchy_review??'unreviewed',independent_review:review.independent_review??original.independent_review??false,student_validated:review.student_validated??original.student_validated??false,review_history:review.history??original.review_history??[]};for(const k of Object.keys(original))assert.deepEqual(r[k],expected[k]);assert.deepEqual(r.review_history,expected.review_history);assert(ids.has(r.from.slice(9))&&ids.has(r.to.slice(9)));assert.equal(r.hierarchy_review,registry.relations[r.id]?.state||'unreviewed');assert.equal(r.independent_review,false);assert.equal(r.student_validated,false);if(!['generalizes','requires_for_task'].includes(r.type))assert.equal(r.order_role,'unordered_connection');records.add(r.id);}
 for(const scope of Object.keys(store.scopes))for(const mode of ['expansion','meaning','position']){
  const html=renderConceptPathway(new URLSearchParams({concept:g.id,target:g.member_codes[0],scope,mode}),data,index);
  assert(!html.includes('undefined'));if(store.inScope(store.standard(g.member_codes[0]),scope)){assert(html.includes(g.member_codes[0]));assert(html.includes('전체 연결망에서 보기'));}else assert(html.includes('다시 선택')||html.includes('직접 분류된 기준이 없습니다'));rendered++;
 }
 if(!g.expansions){const html=renderConceptPathway(new URLSearchParams({concept:g.id}),data,index);assert(html.includes('직접 방향 미기록'));assert(!data.relations.some(r=>r.order_role==='meaning_expansion'));}
 if(data.relations.length){const r=data.relations[0];const html=renderConceptPathway(new URLSearchParams({concept:g.id,relation:r.id}),data,index);assert(html.includes(r.id));assert(html.includes(`data-relation-review="${r.hierarchy_review}"`));assert(html.includes(reviewStateLabels[r.hierarchy_review]));if(r.hierarchy_review==='unreviewed')assert(html.includes('학습 선수성은 미검토'));else assert(!html.includes('선수 위계 미검토'));}
}
// A review belongs to this relation and its recorded scope; original draft
// labels must not override the durable ledger or invent external validation.
for(const state of Object.keys(reviewStateLabels)){
 const html=relationReviewHTML({hierarchy_review:state,hierarchy_review_rationale:'범위 <A>',review_history:[{date:'2026-11-04',reviewer:'검토자',scope:'과제 A만'}],independent_review:state==='independently_reviewed',student_validated:state==='student_validated'});
 assert(html.includes(`data-relation-review="${state}"`));assert(html.includes(reviewStateLabels[state]));assert(html.includes('범위 &lt;A&gt;'));assert(html.includes('과제 A만'));
 assert(html.includes(`독립 검토 ${state==='independently_reviewed'?'기록 있음':'기록 없음'}`));
 assert(html.includes(`학생 반응 검증 ${state==='student_validated'?'기록 있음':'기록 없음'}`));
 assert.equal(html.includes('학습 선수성은 미검토'),state==='unreviewed');
}
assert.equal(standards.size,435);assert.equal(records.size,index.coverage.relations);assert.equal(withExpansion+withoutExpansion,46);
for(const [filter,count] of [['',46],['expansion_draft',withExpansion],['order_unreviewed',withoutExpansion],['reviewed',0]]){const html=hierarchyHome(new URLSearchParams({review:filter}),pilot,flows,index);assert.equal((html.match(/data-concept-pathway=/g)||[]).length,count);}
const fake={concept:{member_codes:['A']},nodes:[{id:'A'},{id:'B'},{id:'C'}],relations:[{from:'standard:A',to:'standard:B',type:'meaning_connection',order_role:'unordered_connection'},{from:'standard:A',to:'standard:C',type:'generalizes',order_role:'meaning_expansion'},{from:'standard:C',to:'standard:A',type:'generalizes',order_role:'meaning_expansion'}]};
const n=conceptNeighborhood(fake,'A');assert(!n.before.size&&!n.after.size);assert(n.conflicts.has('C'));assert(n.related.has('B'));assert(conceptNeighborhood(fake,'missing').reset);
await assert.rejects(store.conceptPathway('../bad'),/등록되지/);
const {standardPage}=await import('../dist/modules/detail.mjs');for(const s of store.catalog.standards){const html=await standardPage(new URLSearchParams({code:s.code}));assert(html.includes('concept=')&&html.includes('target='),s.code);assert(!html.includes('undefined'));}
assert(!requests.some(p=>p.includes('connections.json')));
console.log(JSON.stringify({status:'pass',concepts:46,standards:standards.size,sourceRelations:records.size,withExpansion,withoutExpansion,renderedStates:rendered,checks:'complete corpus, original evidence preserved, per-concept loading, honest review states, semantic direction only, boundary goal retention, filters, cycles, invalid IDs'}));
