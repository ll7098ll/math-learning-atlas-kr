import fs from 'node:fs/promises';
import path from 'node:path';
import crypto from 'node:crypto';
import assert from 'node:assert/strict';
const dist=path.resolve(import.meta.dirname,'../dist');
const read=async name=>JSON.parse(await fs.readFile(path.join(dist,name),'utf8'));
const task=await read('content/task-pathways-index.json'),concept=await read('content/concept-pathways-index.json');
assert.deepEqual(Object.keys(task.files).sort(),[...task.codes].sort());
assert.deepEqual(Object.keys(concept.files).sort(),[...concept.groups.map(g=>g.id),'graph'].sort());
let bytes=0,objects=0;
for(const [namespace,index] of [['task-pathways',task],['concept-pathways',concept]]){
 for(const [key,hash] of Object.entries(index.files)){
  assert.match(hash,/^[a-f0-9]{64}$/);
  const data=await fs.readFile(path.join(dist,'content',namespace,'items',hash+'.json'));
  assert.equal(crypto.createHash('sha256').update(data).digest('hex'),hash);
  const parsed=JSON.parse(data);assert.equal(parsed.version,index.version);
  if(namespace==='task-pathways')assert.equal(parsed.code,key);
  else if(key!=='graph')assert.equal(parsed.concept.id,key);
  bytes+=data.length;objects++;
 }
}
let mode='current',badVersionOnce=false;
const requests=[];
globalThis.window={};
globalThis.fetch=async(raw,options)=>{
 const name=decodeURIComponent(String(raw).split('?')[0]);requests.push({name,cache:options?.cache});
 let data;
 if(name==='content/task-pathways-index.json'||name==='content/concept-pathways-index.json'){
  data=structuredClone(name.includes('task-pathways')?task:concept);
  if(mode==='legacy')delete data.files;
  if(mode==='malformed')data.files[task.codes[0]]='../bad';
 }else{
  let file=name;
  if(mode==='legacy')for(const [namespace,index] of [['task-pathways',task],['concept-pathways',concept]]){
   const prefix='content/'+namespace+'/'+index.datasetVersion+'/';
   if(name.startsWith(prefix)){const key=name.slice(prefix.length,-5);file='content/'+namespace+'/items/'+index.files[key]+'.json';}
  }
  data=await read(file);
  if(badVersionOnce&&name.includes('/items/')){data={...data,version:'stale'};badVersionOnce=false;}
 }
 return {ok:true,json:async()=>data};
};
const current=await import('../dist/modules/store.mjs?object-check');await current.initialize();
const [one,two]=await Promise.all([current.taskPathway(task.codes[0]),current.taskPathway(task.codes[0])]);
assert.strictEqual(one,two);
assert.equal(requests.filter(r=>r.name.includes('/task-pathways/items/')).length,1);
assert(requests.some(r=>r.name==='content/task-pathways-index.json'&&r.cache==='no-cache'));
assert(requests.some(r=>r.name.includes('/items/')&&r.cache==='default'));
mode='legacy';
const legacy=await import('../dist/modules/store.mjs?legacy-check');await legacy.initialize();
assert.deepEqual(await legacy.taskPathway(task.codes[0]),one);
assert.equal((await legacy.conceptPathway(concept.groups[0].id)).concept.id,concept.groups[0].id);
assert.equal((await legacy.hierarchyGraph()).version,concept.version);
assert(requests.some(r=>r.name.startsWith('content/task-pathways/'+task.datasetVersion+'/')));
mode='current';badVersionOnce=true;
const retry=await import('../dist/modules/store.mjs?object-retry');await retry.initialize();
await assert.rejects(retry.taskPathway(task.codes[0]),/갱신/);
assert.equal((await retry.taskPathway(task.codes[0])).code,task.codes[0]);
mode='malformed';
const malformed=await import('../dist/modules/store.mjs?bad-object');await malformed.initialize();
await assert.rejects(malformed.taskPathway(task.codes[0]),/자료 목록/);
const normalFetch=globalThis.fetch;mode='current';
const retired=await import('../dist/modules/store.mjs?retired-object');await retired.initialize();
globalThis.fetch=async(raw,options)=>String(raw).includes('/items/')?{ok:false,status:404}:normalFetch(raw,options);
await assert.rejects(retired.taskPathway(task.codes[0]),error=>error.needsReload===true&&/새로고침/.test(error.message));
globalThis.fetch=normalFetch;
assert.equal((await retired.taskPathway(task.codes[0])).code,task.codes[0],'404 must clear rejected cache entries');
console.log(JSON.stringify({status:'pass',objects,bytes,checks:'per-record content hashes and identifiers; immutable request policy; deduplication; legacy index compatibility; stale version retry; malformed path rejection'}));
