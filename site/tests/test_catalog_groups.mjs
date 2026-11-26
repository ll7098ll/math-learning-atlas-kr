import fs from 'node:fs/promises';
import path from 'node:path';
import assert from 'node:assert/strict';
const dist=path.resolve(import.meta.dirname,'../dist');
globalThis.fetch=async raw=>({ok:true,json:async()=>JSON.parse(await fs.readFile(path.join(dist,decodeURIComponent(String(raw).split('?')[0])),'utf8'))});
globalThis.window={};
const store=await import('../dist/modules/store.mjs');await store.initialize();
const model=await import('../dist/modules/catalog-model.mjs');
function check(values) {
  const params = new URLSearchParams(values);
  const selected = model.selection(store.catalog.standards, values.scope, values.band, values.domain, values.category);
  const matches = model.search(selected, values.q || '');
  const expected = store.select(params);
  assert.deepEqual(new Set(matches.map(s=>s.code)), new Set(expected.map(s=>s.code)));
  const groups = model.groupStandards(matches);
  const grouped = groups.flatMap(group=>group.domains.flatMap(domain=>domain.rows.map(row=>row.code)));
  const expectedOrder = store.levels.flatMap(level=>{
    const school = expected.filter(row=>row.level===level);
    return [...new Set(school.map(store.band))].flatMap(band=>{
      const bandRows = school.filter(row=>store.band(row)===band);
      return [...new Set(bandRows.map(row=>row.domain))].flatMap(domain=>
        bandRows.filter(row=>row.domain===domain).map(row=>row.code));
    });
  });
  assert.deepEqual(grouped,expectedOrder);
  assert.equal(new Set(grouped).size,matches.length);
  const expanded = model.catalogPageRows(matches,new URLSearchParams({...values,expand:'all'}));
  assert.equal(expanded.pageCount,1);
  assert.deepEqual(expanded.shown,matches);
  const pages = [];
  for(let page=1;page<=Math.max(1,Math.ceil(matches.length/24));page++){
    const result=model.catalogPageRows(matches,new URLSearchParams({...values,page}));
    assert.equal(result.page,page);
    assert(result.shown.length<=24);
    pages.push(...result.shown);
  }
  assert.deepEqual(pages,matches);
  return matches;
}
let states=0;
for(const scope of Object.keys(store.scopes)){
 check({scope});states++;
 for(const band of new Set(store.catalog.standards.filter(s=>store.inScope(s,scope)).map(store.band))){
  check({scope,band});states++;
  for(const domain of new Set(store.catalog.standards.filter(s=>store.inScope(s,scope)&&store.band(s)===band).map(s=>s.domain))){check({scope,band,domain});states++;}
 }
}
for(const s of store.catalog.standards){assert.equal(check({q:s.code})[0].code,s.code);states++;}
const all=check({});
assert.equal(all.length,435);
for(const row of all){
  const focused=model.catalogPageRows(all,new URLSearchParams({focus:row.code}));
  assert(focused.shown.some(s=>s.code===row.code),row.code);
}
assert.equal(check({q:'<script>not-a-standard</script>'}).length,0);
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
for(const entry of ['reader','legacy']){
 const overview=resolveView('#view=overview',entry);
 assert.equal(overview.entry,'reader');
 assert.equal(overview.menu,'catalog');
 assert.deepEqual(Object.fromEntries(overview.params),{view:'catalog',list:'1'});
 const focus = new URLSearchParams({view:'overview',mode:'structure',density:'expanded',scope:'h',
   subject:'공통수학1',domain:'다항식',focus:'10공수1-01-01',q:'다항식'});
 const expanded=resolveView('#'+focus,entry);
 assert.equal(expanded.entry,'reader');
 assert.deepEqual(Object.fromEntries(expanded.params),
   {view:'catalog',scope:'h',band:'공통수학1',domain:'다항식',focus:'10공수1-01-01',q:'다항식',list:'1',expand:'all'});
 const flow=resolveView('#view=overview&mode=flow&strand=ratio&scope=em',entry);
 assert.equal(flow.entry,'legacy');
 assert.equal(flow.menu,'network');
 assert.equal(flow.params.get('strand'),'ratio');
 assert.equal(flow.params.get('scope'),'em');
}
assert.equal(resolveView('#view=explore&relation=L014','legacy').params.get('relation'),'L014');
assert.equal(resolveView('#view=unknown','legacy').menu,'network');
const sources=await store.sources();
assert.deepEqual(sources,(await store.connections()).sources);
assert.equal(new Set(sources.map(s=>s.id)).size,sources.length);
console.log(JSON.stringify({status:'pass',standards:435,states,sources:sources.length,checks:'all standards without pagination loss, school/band/domain grouping, unique codes, all subjects, filters, code search, expanded and paginated lists, row focus, legacy routes, sources index parity'}));
