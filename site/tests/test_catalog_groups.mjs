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
const {resolveView}=await import('../dist/modules/route-views.mjs');
const modern=resolveView('#view=standard&code=6수01-10','reader');
assert.equal(modern.entry,'reader');
assert.equal(modern.params.get('code'),'6수01-10');
const manuscript=resolveView('#view=standard&code=6수01-10&section=paths','reader');
assert.equal(manuscript.entry,'legacy');
assert.equal(manuscript.params.get('section'),'paths');
const oldCatalog=resolveView('#view=map&scope=e&q=분수&display=compact','legacy');
assert.equal(oldCatalog.entry,'reader');
assert.deepEqual(Object.fromEntries(oldCatalog.params),
 {view:'catalog',scope:'e',q:'분수',display:'compact',list:'1'});
const overview=resolveView('#view=overview','legacy');
assert.equal(overview.params.get('mode'),'structure');
assert.equal(overview.menu,'network');
assert.equal(resolveView('#view=overview&mode=flow','legacy').params.get('mode'),'flow');
assert.equal(resolveView('#view=explore&relation=L014','legacy').params.get('relation'),'L014');
assert.equal(resolveView('#view=unknown','legacy').menu,'network');
const sources=await store.sources();
assert.deepEqual(sources,(await store.connections()).sources);
assert.equal(new Set(sources.map(s=>s.id)).size,sources.length);
console.log(JSON.stringify({status:'pass',standards:435,states,sources:sources.length,checks:'all standards without pagination loss, school/band/domain grouping, unique codes, all subjects, filters, code search, expanded and compact views, legacy routes, sources index parity'}));
