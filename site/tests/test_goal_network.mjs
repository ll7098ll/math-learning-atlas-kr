import fs from 'node:fs/promises';
import path from 'node:path';
import crypto from 'node:crypto';
import assert from 'node:assert/strict';
const root=path.resolve(import.meta.dirname,'..'),dist=path.join(root,'dist');
const read=async p=>JSON.parse(await fs.readFile(path.join(dist,p),'utf8'));
const index=await read('content/task-pathways-index.json'),requests=[];
globalThis.fetch=async(raw,options)=>{const name=decodeURIComponent(String(raw).split('?')[0]);requests.push({name,cache:options?.cache});return {ok:true,json:()=>read(name)};};
globalThis.window={};
const store=await import('../dist/modules/store.mjs');await store.initialize();
assert.equal(requests.length,1,'Initial catalog must not eagerly load the goal graph');
const data=await store.goalNetwork();assert.strictEqual(await store.goalNetwork(),data);
assert.equal(requests.filter(r=>r.name.includes(index.goalGraph.hash)).length,1);
assert.equal(requests.find(r=>r.name.includes(index.goalGraph.hash)).cache,'default');
const bytes=await fs.readFile(path.join(dist,'content/task-pathways/items',index.goalGraph.hash+'.json'));
assert.equal(crypto.createHash('sha256').update(bytes).digest('hex'),index.goalGraph.hash);
assert.equal(data.version,index.version);assert.equal(data.kind,'scoped_goal_network');
assert.deepEqual(data.coverage,{standards:435,goals:870,cases:565,routes:626,directed_pairs:1481});
const authored=[];
for(const name of await fs.readdir(path.join(root,'../data'))){
 if(/^goal_hierarchy_.*\.json$/.test(name))authored.push(JSON.parse(await fs.readFile(path.join(root,'../data',name),'utf8')));
}
const goals=new Map(authored.flatMap(d=>d.entries.flatMap(e=>e.goals.map(g=>[g.id,{...g,code:e.code}]))));
assert.deepEqual(new Map(data.goals.map(g=>[g.id,g])),goals);
const cases=authored.flatMap(d=>d.cases).filter(c=>!c.superseded_by_case_ids?.length),routes=new Map(data.routes.map(r=>[r.id,r]));
for(const c of cases)for(const r of c.routes){
 const g=routes.get(c.id+'::'+r.id);assert(g);
 assert.deepEqual(g.shared_conditions,c.shared_conditions);assert.deepEqual(g.goal_ids,c.goal_ids);
 assert.equal(g.operator,r.operator);assert.equal(g.alternative_review,c.alternative_review);
 assert.deepEqual(g.conditions.map(v=>v.text),r.conditions);
 assert.deepEqual(g.conditions.map(({text,...source})=>source),r.condition_sources);
}
const {buildGoalNetwork,renderGoalNetwork,goalTrace}=await import('../dist/modules/goal-network.mjs');
const {esc}=await import('../dist/modules/ui.mjs');
const model=buildGoalNetwork(data),pairs=new Set();let rendered=0;
for(const r of data.routes)for(const c of r.conditions)if(c.kind==='goal')for(const target of c.applies_to_goal_ids||r.goal_ids)pairs.add(c.goal_id+'|'+target);
assert.equal(pairs.size,1481);
for(const g of data.goals){
 const expectedIncoming=data.routes.filter(r=>r.goal_ids.includes(g.id));
 const expectedOutgoing=data.routes.filter(r=>r.conditions.some(c=>c.kind==='goal'&&c.goal_id===g.id));
 assert.deepEqual(model.incoming.get(g.id),expectedIncoming);assert.deepEqual(model.outgoing.get(g.id),expectedOutgoing);
 for(const scope of ['all','e','m','h']){
  const html=renderGoalNetwork(new URLSearchParams({target:g.code,goal:g.id,scope}),model);
  assert(html.includes(esc(g.title))&&html.includes(esc(g.success))&&!html.includes('undefined'));
  for(const [,id,href] of html.matchAll(/data-network-goal="([^"]+)" href="([^"]+)"/g)){
   const query=new URLSearchParams(href.replace(/^#/, '').replaceAll('&amp;','&'));
   assert.deepEqual(goalTrace(model,query.get('trace'),id),query.get('trace').split('|'),'Links must not imply an edge to another goal\'s companion condition');
  }
  for(const r of [...expectedIncoming,...expectedOutgoing]){
   assert(html.includes('data-network-route="'+esc(r.id)+'"'));
   for(const c of r.conditions)assert(html.includes(esc(c.text))&&html.includes(esc(c.rationale)));
   for(const text of r.shared_conditions)assert(html.includes(esc(text)));
  }
  for(const r of expectedOutgoing)for(const c of r.conditions.filter(c=>c.kind==='goal'&&c.goal_id===g.id)){
   for(const id of c.applies_to_goal_ids||r.goal_ids)assert(html.includes('data-network-goal="'+esc(id)+'"'));
  }
  if(!store.inScope(store.standard(g.code),scope))assert(html.includes('선택 학교급 밖'));
  rendered++;
 }
}
for(const [source,targets] of model.next)for(const target of targets){
 assert.deepEqual(goalTrace(model,source+'|'+target,target),[source,target]);
 assert.deepEqual(goalTrace(model,target+'|'+source,source),[target,source]);
}
const route=(source,target)=>model.next.get(source)?.has(target);
const chain=['6수03-13:rectangle','12수과02-03:method','12수과03-01:plan','12수과03-02:perform'];
assert(chain.slice(1).every((g,i)=>route(chain[i],g)));
assert.deepEqual(goalTrace(model,chain.join('|'),chain.at(-1)),chain);
const trailHtml=renderGoalNetwork(new URLSearchParams({target:'12수과03-02',goal:chain.at(-1),scope:'h',trace:chain.join('|')}),model);
assert(trailHtml.includes('지금까지 살펴본 목표')&&trailHtml.includes('함께 필요한 다른 조건의 충족'));
assert(trailHtml.includes('6수03-13'));
for(const bad of ['unknown|'+chain.at(-1),chain[0]+'|'+chain.at(-1),[...chain,chain[0],chain.at(-1)].join('|')])assert.deepEqual(goalTrace(model,bad,chain.at(-1)),[chain.at(-1)]);
assert(renderGoalNetwork(new URLSearchParams({target:'not-a-standard'}),model).includes('등록된 성취기준'));
// One route may contain conditions applying to different goals. Keep AND and targets separate.
const fixture={goals:['A','B','C','D'].map(id=>({id,code:'A',title:id})),routes:[{id:'r',case_id:'case',goal_ids:['C','D'],conditions:[{kind:'goal',goal_id:'A',applies_to_goal_ids:['C']},{kind:'goal',goal_id:'B',applies_to_goal_ids:['D']}]}]};
const scoped=buildGoalNetwork(fixture);
assert.deepEqual([...scoped.next.get('A')],['C']);assert.deepEqual([...scoped.next.get('B')],['D']);
assert.deepEqual(scoped.incoming.get('C'),scoped.incoming.get('D'));
const {hierarchyHome}=await import('../dist/modules/pathways.mjs');
const home=hierarchyHome(new URLSearchParams(),await store.hierarchy(),await store.conceptFlows(),await store.conceptPathwaysIndex(),index);
assert(home.includes('870개 하위 목표')&&!home.includes('과제별 위계 미검토'));
for(const s of store.catalog.standards)assert(home.includes('mode=goals&amp;target='+encodeURIComponent(s.code))||home.includes('mode=goals&target='+encodeURIComponent(s.code)));
assert(!requests.some(r=>r.name.includes('/standards/')||r.name==='content/connections.json'),'Goal navigation must not fetch all standard analyses or relations');
console.log(JSON.stringify({status:'pass',goals:870,routes:626,pairs:pairs.size,renderedStates:rendered,bytes:bytes.length,checks:'exact authored source and AND preservation; scoped per-condition targets; full reverse neighborhoods; all goals and school scopes; valid multistep and reverse traces; invalid trace rejection; lazy immutable graph; full hub entry points'}));
