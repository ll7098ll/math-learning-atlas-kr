import fs from 'node:fs/promises';
import path from 'node:path';
import assert from 'node:assert/strict';
import {createRequire} from 'node:module';
const root=path.resolve(import.meta.dirname,'..'),dist=process.env.MATH_ATLAS_DIST||path.join(root,'portal/math-atlas/dist');
const read=async p=>JSON.parse(await fs.readFile(path.join(dist,p),'utf8'));
const requests=[];
globalThis.fetch=async raw=>{const p=decodeURIComponent(String(raw).split('?')[0]);requests.push(p);return {ok:true,json:()=>read(p)};};
const store=await import('../portal/math-atlas/dist/modules/store.mjs');await store.initialize();
const [a,b,flows]=await Promise.all([store.hierarchy(),store.hierarchy(),store.conceptFlows()]);
assert.strictEqual(a,b);assert.equal(requests.filter(x=>x.endsWith('/hierarchy.json')).length,1);
assert(!requests.some(x=>x.includes('connections.json')));
assert((await fs.stat(path.join(dist,'content/hierarchy.json'))).size<60000);
const {hierarchyHome,pathForStandard}=await import('../portal/math-atlas/dist/modules/pathways.mjs');
const home=hierarchyHome(new URLSearchParams(),a,flows);
assert.equal((home.match(/data-open="path-/g)||[]).length,46);
for(const s of store.catalog.standards)assert(home.includes(encodeURIComponent(s.code)),s.code+' missing from hub');
assert(hierarchyHome(new URLSearchParams({q:'6수02-03'}),a,flows).includes('6수02-03'));
const require=createRequire(import.meta.url),H=require(path.join(dist,'hierarchy.js'));
const byCode=new Map(store.catalog.standards.map(s=>[s.code,s]));let combinations=0;
for(const m of a.hierarchy.maps){
 for(const code of new Set(m.nodes.flatMap(n=>n.standards))){const p=pathForStandard(m,code);assert(m.nodes.find(n=>n.id===p.target).standards.includes(code));assert(H.selectRoute(m,p.route).nodes.some(n=>n.id===p.target));}
 for(const group of m.condition_groups){assert.equal(group.operator,'AND');assert(group.members.length>=2);for(const id of group.claim_ids){const c=m.claims.find(c=>c.id===id);assert.equal(c.kind,'task_condition');assert.equal(c.target,group.target);}}
 for(const r of m.routes)for(const scope of Object.keys(store.scopes)){
  const full=H.selectRoute(m,r.id),filtered=H.context(m,r.id,byCode,s=>store.inScope(s,scope));
  assert(filtered.nodes.some(n=>n.id===m.focus));assert.deepEqual(filtered.claims,full.claims);
  assert.deepEqual(filtered.nodes.map(n=>n.id),full.nodes.map(n=>n.id));
  for(const n of filtered.nodes)assert.equal(n.boundary,!n.standards.some(c=>store.inScope(byCode.get(c),scope)));
  for(const c of filtered.claims.filter(c=>c.condition_group))assert.equal(filtered.claims.filter(x=>x.condition_group===c.condition_group).length,full.claims.filter(x=>x.condition_group===c.condition_group).length);
  H.rank(filtered.nodes,filtered.claims);combinations++;
 }
}
const original=JSON.parse(await fs.readFile(path.join(root,'data/relations.json'),'utf8')).relations;
const union=new Set();
for(const s of store.catalog.standards){const data=await store.standardConnections(s.code);assert.equal(data.version,a.version);assert.deepEqual(data.relations,original.filter(r=>[r.from,r.to].includes('standard:'+s.code)));for(const r of data.relations)if(r.from.startsWith('standard:')&&r.to.startsWith('standard:'))union.add(r.id);}
assert.equal(union.size,1518);assert(!requests.some(x=>x.includes('connections.json')));
const count=requests.length;await store.hierarchy();await store.standardConnections('6수02-03');assert.equal(requests.length,count);
// A rejected version must leave the shared cache so retry can recover.
const retryStore=await import('../portal/math-atlas/dist/modules/store.mjs?retry');await retryStore.initialize();let attempts=0;
globalThis.fetch=async raw=>({ok:true,json:async()=>{const d=await read(decodeURIComponent(String(raw).split('?')[0]));return ++attempts===1?{...d,version:'stale'}:d;}});
await assert.rejects(retryStore.hierarchy(),/갱신/);await retryStore.hierarchy();assert.equal(attempts,2);
console.log(JSON.stringify({status:'pass',concepts:46,standards:435,scopeRoutes:combinations,reachableStandardRelations:union.size,hierarchyBytes:(await fs.stat(path.join(dist,'content/hierarchy.json'))).size,checks:'small versioned bundle, request deduplication, all-code entry, complete AND groups, fixed targets, retry after stale version'}));
