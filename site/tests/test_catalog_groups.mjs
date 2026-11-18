import fs from 'node:fs/promises';
import path from 'node:path';
import assert from 'node:assert/strict';
const dist=path.resolve(import.meta.dirname,'../dist');
globalThis.fetch=async raw=>({ok:true,json:async()=>JSON.parse(await fs.readFile(path.join(dist,decodeURIComponent(String(raw).split('?')[0])),'utf8'))});
globalThis.window={};
const store=await import('../dist/modules/store.mjs');await store.initialize();
const {catalogPage}=await import('../dist/modules/catalog.mjs');
function check(params){
 const p=new URLSearchParams(params),items=store.select(p),html=catalogPage(p);
 const codes=[...html.matchAll(/data-standard="([^"]+)"/g)].map(m=>m[1]);
 assert.deepEqual(codes,[...store.levels].flatMap(level=>[...new Set(items.filter(s=>s.level===level).map(store.band))].flatMap(b=>[...new Set(items.filter(s=>s.level===level&&store.band(s)===b).map(s=>s.domain))].flatMap(d=>items.filter(s=>s.level===level&&store.band(s)===b&&s.domain===d).map(s=>s.code)))));
 assert.equal(new Set(codes).size,items.length);
 assert(!html.includes('undefined'));assert(!html.includes('60개 더 보기'));
 return html;
}
let states=0;
for(const scope of Object.keys(store.scopes)){
 check({scope});states++;
 for(const band of new Set(store.catalog.standards.filter(s=>store.inScope(s,scope)).map(store.band))){
  const html=check({scope,band,expand:'all'});assert(html.includes(`data-catalog-band="${band}"`));states++;
  for(const domain of new Set(store.catalog.standards.filter(s=>store.inScope(s,scope)&&store.band(s)===band).map(s=>s.domain))){check({scope,band,domain,display:'compact'});states++;}
 }
}
for(const s of store.catalog.standards){check({q:s.code});states++;}
const all=check({});assert.equal((all.match(/data-standard=/g)||[]).length,435);
assert(all.includes('학년군과 과목 바로 선택'));
check({q:'<script>not-a-standard</script>'});
console.log(JSON.stringify({status:'pass',standards:435,states,checks:'all standards without pagination loss, school/band/domain grouping, unique codes, all subjects, filters, code search, expanded and compact views'}));
