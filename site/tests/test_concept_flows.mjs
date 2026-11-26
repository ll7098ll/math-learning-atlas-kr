import fs from 'node:fs/promises';
import path from 'node:path';
import assert from 'node:assert/strict';
import {fileURLToPath} from 'node:url';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..'),dist=path.join(root,'dist');
const read=async p=>JSON.parse(await fs.readFile(path.join(dist,p),'utf8'));
const requests=[];
globalThis.fetch=async raw=>{const p=decodeURIComponent(String(raw).split('?')[0]);requests.push(p);return {ok:true,json:()=>read(p)};};
globalThis.window={};
const store=await import('../dist/modules/store.mjs');
const {overview}=await import('../dist/modules/catalog.mjs');
await store.initialize();
const flows=await store.conceptFlows(),all=store.catalog.standards;
const initial=await overview(new URLSearchParams());
assert.equal(store.catalog.standards.length,435);
assert.equal((initial.match(/class="flow-row tone-/g)||[]).length,flows.coverage.concepts);
assert.equal((initial.match(/role="group"/g)||[]).length,flows.strands.length*3);
assert.equal((initial.match(/data-classification="primary"/g)||[]).length,435);
assert.equal((initial.match(/data-classification="additional"/g)||[]).length,47);
assert(!requests.some(p=>p.endsWith('connections.json')),'Default map must not download all evidence');
assert.equal(flows.coverage.total,435);assert.deepEqual(flows.coverage.unassigned,[]);
assert.equal(flows.coverage.primary_assigned,435);assert.deepEqual(flows.coverage.by_level,{'초등학교':121,'중학교':60,'고등학교':254});
assert.equal(flows.version,store.catalog.version);
assert.equal(new Set(flows.strands.map(t=>t.id)).size,flows.strands.length);
const primary=new Map(),allEvidence=new Set(),relations=(await store.connections()).relations;
for(const t of flows.strands){
 assert.equal(t.stages.length,3);
 const ids=new Set(t.stages.flatMap(s=>s.codes));
 for(const [i,s] of t.stages.entries()){
  assert.equal(new Set(s.codes).size,s.codes.length);
  assert.deepEqual(new Set([...s.primary_codes,...s.additional_codes]),new Set(s.codes));
  for(const c of s.codes)assert.equal(store.standard(c).level,store.levels[i],c);
  for(const c of s.primary_codes){assert(!primary.has(c),'duplicate primary '+c);primary.set(c,t.id);}
  for(const ref of s.related){assert(!ids.has(ref.code),ref.code);assert.equal(store.standard(ref.code).level,store.levels[i]);for(const id of ref.relation_ids){const r=relations.find(r=>r.id===id);assert(r,id);const a=r.from.slice(9),b=r.to.slice(9);assert([a,b].includes(ref.code));assert(ids.has(a)||ids.has(b));assert.notEqual(store.standard(a).level,store.standard(b).level);}}
 }
 for(const id of t.relation_ids){const r=relations.find(r=>r.id===id);assert(r,id);assert(ids.has(r.from.slice(9))&&ids.has(r.to.slice(9)));allEvidence.add(id);}
 for(const id of t.external_relation_ids){const r=relations.find(r=>r.id===id);assert(r,id);assert.notEqual(ids.has(r.from.slice(9)),ids.has(r.to.slice(9)));allEvidence.add(id);}
 const html=await overview(new URLSearchParams({mode:'flow',strand:t.id}));
 assert(html.includes(t.question));assert(!html.includes('undefined')&&!html.includes('[object Object]'));
}
assert.deepEqual(new Set(primary.keys()),new Set(all.map(s=>s.code)));
assert.equal(allEvidence.size,store.catalog.meta.standardConnections,'Every recorded standard relation must be reachable from a concept');
for(const s of all){const html=await overview(new URLSearchParams({mode:'flow',q:s.code}));assert(html.includes(`id="flow-${primary.get(s.code)}"`),s.code);assert(html.includes(`data-standard="${s.code}"`),s.code);assert(html.includes('is-match'),s.code);}
for(const subject of new Set(all.filter(s=>s.level==='고등학교').map(s=>s.subject))){
 const html=await overview(new URLSearchParams({mode:'flow',subject}));
 const shown=[...html.matchAll(/<a class="flow-member[^\"]*" href="[^\"]*" data-standard="([^\"]+)"[^>]*data-classification="primary"/g)].map(m=>m[1]).filter(c=>store.standard(c).level==='고등학교');
 assert.deepEqual(new Set(shown),new Set(all.filter(s=>s.subject===subject).map(s=>s.code)),subject);
}
const matrix=flows.strands.find(g=>g.id==='matrix');assert.equal(matrix.stages[0].codes.length,0);assert.equal(matrix.stages[1].codes.length,0);assert(matrix.stages.some(s=>s.related.length));
const expanded=await overview(new URLSearchParams({mode:'flow',expanded:'all'}));
assert.equal((expanded.match(/<details class="flow-members"[^>]* open/g)||[]).length,flows.strands.flatMap(t=>t.stages).filter(s=>s.codes.length).length);
const ratio=await overview(new URLSearchParams({mode:'flow',strand:'ratio',edgeCode:'6수02-03',edgeScope:'all',edgeLimit:'9999'}));
const ratioIds=[...ratio.matchAll(/data-evidence="([^\"]+)"/g)].map(m=>m[1]);
assert(ratioIds.length>12);for(const id of ratioIds){const r=relations.find(r=>r.id===id);assert([r.from,r.to].includes('standard:6수02-03'));}
assert((await overview(new URLSearchParams({mode:'flow',q:'zz-unknown'}))).includes('일치하는 개념 또는'));
const {resolveView}=await import('../dist/modules/route-views.mjs');
const structure=resolveView('#view=overview&mode=structure&density=expanded','legacy');
assert.equal(structure.entry,'reader');
assert.equal(structure.params.get('expand'),'all');
console.log(JSON.stringify({status:'pass',concepts:flows.strands.length,primaryStandards:primary.size,additionalMemberships:47,searchableCodes:435,highSchoolCourses:15,reachableRelations:allEvidence.size,checks:'all standards assigned exactly once, real cross-school evidence, direct vs related roles, all-code search, all-course filters, full expansion, code-level evidence, lazy loading, school structure link opens the expanded reader list'}));



