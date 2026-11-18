import fs from 'node:fs/promises';
import path from 'node:path';
import assert from 'node:assert/strict';
import {buildNetwork} from '../dist/modules/network-model.mjs';
import {layoutInternalNetwork} from '../dist/modules/internal-layout.mjs';
const dist=path.resolve(import.meta.dirname,'../dist');
const read=async p=>JSON.parse(await fs.readFile(path.join(dist,p),'utf8'));
globalThis.fetch=async raw=>({ok:true,json:()=>read(decodeURIComponent(String(raw).split('?')[0]))});
globalThis.window={};
const store=await import('../dist/modules/store.mjs');await store.initialize();
const catalog=store.catalog,flows=await store.conceptFlows(),connections=await store.connections();
const {renderConceptPathway}=await import('../dist/modules/concept-pathways.mjs');
const {flowOverview}=await import('../dist/modules/flows.mjs');
const {standardPage}=await import('../dist/modules/detail.mjs');
const {markdown}=await import('../dist/modules/ui.mjs');
const probabilityTable=markdown('| 질문 | 설명 |\n|---|---|\n| P(A\\|B) | P(B\\|A)와 구별 |');
assert(probabilityTable.includes('P(A|B)')&&probabilityTable.includes('P(B|A)'));
assert.equal((probabilityTable.match(/<td>/g)||[]).length,2,'conditional bars stay inside their table cells');
assert(!probabilityTable.includes('\\|'),'Markdown escape is not visible to the reader');
assert((await standardPage(new URLSearchParams({code:'6수04-04'}))).includes('P(A|B)'));
const index=await store.conceptPathwaysIndex();
let states=0;
for(const [scope,level,count] of [['e','초등학교',121],['m','중학교',60],['h','고등학교',254]]){
 const standards=catalog.standards.filter(s=>s.level===level);
 assert.equal(standards.length,count);
 const model=layoutInternalNetwork(buildNetwork({...catalog,standards},flows,connections));
 assert.equal(model.nodes.length,count);
 assert(model.edges.every(e=>model.byCode.has(e.from)&&model.byCode.has(e.to)));
 assert.equal(new Set(model.nodes.map(n=>n.x+','+n.y)).size,count,'school nodes do not overlap');
 for(const e of model.edges.filter(e=>['generalizes','requires_for_task'].includes(e.type)&&e.records.some(r=>r.review_state==='self_checked'))){
  const a=model.byCode.get(e.from),b=model.byCode.get(e.to);
  if(a.stage!==model.stages.length-1&&b.stage!==model.stages.length-1)assert(a.x<b.x,'authored direction controls rank');
 }
 globalThis.atlasSchoolScope=scope;const overview=await flowOverview(new URLSearchParams({scope,expanded:'all'}));for(const m of overview.matchAll(/data-standard="([^"]+)"/g))assert.equal(catalog.standards.find(s=>s.code===m[1]).level,level);
 for(const g of index.groups){
  const data=await store.conceptPathway(g.id),original=JSON.stringify(data);
  const html=renderConceptPathway(new URLSearchParams({concept:g.id,scope}),data,index);
  assert.equal(JSON.stringify(data),original,'render cannot mutate cached scope data');
  assert(!html.includes('undefined'));
  for(const match of html.matchAll(/data-cp-node="([^"]+)"/g))assert.equal(catalog.standards.find(s=>s.code===match[1]).level,level);
  states++;
 }
}
globalThis.atlasSchoolScope='all';
const coverage=[];
for(const s of catalog.standards){
 const a=await store.detail(s.code);assert.equal(a.schemaVersion,2,s.code+' must be individually migrated');
 assert.equal(a.sections.length,12,s.code);assert.equal(new Set(a.sections.map(x=>x.id)).size,12);
 assert(a.sections.every(x=>x.body.trim()),s.code);
 const html=await standardPage(new URLSearchParams({code:s.code}));assert(!html.includes('undefined'));
 assert.equal((html.match(/class="reading-section"/g)||[]).length,12);
 assert(html.includes(s.statement.replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;').replaceAll('"','&quot;').replaceAll("'",'&#39;')));
 coverage.push(s.code);
}
const factor=await store.detail('9수01-01');
assert(factor.markdown.includes('2²×3×5'));assert(!factor.markdown.includes('근호 안의 수'));
for(const code of ['9수03-06','9수03-08']){const a=await store.detail(code);assert(!JSON.stringify(a.paths).includes('옮겨 담기'));}
const originalCorpus=JSON.parse(await fs.readFile(path.resolve(dist,'../../data/relations.json'),'utf8'));
const originalIds=new Set(originalCorpus.relations.filter(r=>r.from.startsWith('standard:')&&r.to.startsWith('standard:')).map(r=>r.id));
const originalRelations=connections.relations.filter(r=>originalIds.has(r.id)&&r.from.startsWith('standard:')&&r.to.startsWith('standard:'));
assert.equal(originalRelations.length,1518,'all original records retained');assert.deepEqual(new Set(originalRelations.map(r=>r.id)),originalIds);
console.log(JSON.stringify({status:'pass',standards:coverage.length,scopeConceptStates:states,sourceRelations:originalRelations.length,relations:connections.relations.length,checks:'school isolation, stable cache, unique placement, authored directions, full 12-section corpus, original statements, specific regression cases'}));
