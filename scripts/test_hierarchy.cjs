// Regression checks for route-dependent partial orders and real corpus references.
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict'),vm=require('node:vm');
const root=path.resolve(__dirname,'..'),read=name=>JSON.parse(fs.readFileSync(path.join(root,'data',name+'.json'),'utf8'));
const {selectRoute,rank}=require('../portal/math-atlas/dist/hierarchy.js');
const pilot=read('hierarchy_pilot'),standards=new Set(read('standards').standards.map(s=>s.code));
const relationIds=new Set(read('relations').relations.map(r=>r.id)),sourceIds=new Set(read('sources').map(s=>s.id));
let routes=0;
for(const map of pilot.maps){
  assert(map.nodes.some(n=>n.id===map.focus));
  assert.equal(new Set(map.nodes.map(n=>n.id)).size,map.nodes.length);
  const routeIds=new Set(map.routes.map(r=>r.id)),nodeIds=new Set(map.nodes.map(n=>n.id));
  for(const node of map.nodes)for(const code of node.standards)assert(standards.has(code),code);
  for(const claim of map.claims){
    assert(nodeIds.has(claim.source)&&nodeIds.has(claim.target),claim.id);
    for(const route of claim.routes)assert(routeIds.has(route));
    for(const id of claim.original_relation_ids)assert(relationIds.has(id),id);
    for(const id of claim.research_context)assert(sourceIds.has(id),id);
    for(const key of ['rationale','conditions','mathematical_check','alternative','status'])assert(claim[key]?.length,claim.id+':'+key);
    assert(claim.probe.question&&claim.probe.expected);
    assert.equal(typeof claim.student_validated,'boolean');if(claim.student_validated)assert(claim.review_history?.some(r=>r.kind==='student'&&r.evidence));
    assert.equal(typeof claim.independent_review,'boolean');if(claim.independent_review)assert(claim.review_history?.some(r=>r.kind==='independent'&&r.reviewer&&r.evidence));
  }
  for(const route of map.routes){
    const selected=selectRoute(map,route.id),levels=rank(selected.nodes,selected.claims);
    for(const claim of selected.claims)assert(levels.get(claim.source)<levels.get(claim.target),claim.id);
    const groupMap=new Map();
    for(const c of selected.claims)if(c.condition_group){const group=groupMap.get(c.condition_group)||[];group.push(c);groupMap.set(c.condition_group,group);}
    for(const group of groupMap.values()){assert(group.length>=2);assert.equal(new Set(group.map(c=>c.target)).size,1);}
    routes++;
  }
}
const map=id=>pilot.maps.find(m=>m.id===id),ids=(id,route)=>new Set(selectRoute(map(id),route).nodes.map(n=>n.id));
assert(ids('fraction','unit').has('F4'));assert(!ids('fraction','unit').has('F5'));
assert(ids('fraction','whole').has('F5'));assert(!ids('fraction','whole').has('F4'));
assert(ids('ratio','inverse').has('R9'));assert(!ids('ratio','direct').has('R9'));
assert(ids('area','copy').has('A6'));assert(!ids('area','move').has('A6'));
const selected=selectRoute(map('fraction'),'unit');
assert.throws(()=>rank(selected.nodes,[...selected.claims,{source:'F7',target:'F1',kind:'task_condition'}]),/순환/);
const dir=path.join(root,'portal/math-atlas/dist/content');
const exported={...JSON.parse(fs.readFileSync(path.join(dir,'catalog.json'),'utf8')),...JSON.parse(fs.readFileSync(path.join(dir,'connections.json'),'utf8'))};
exported.analyses=Object.fromEntries(exported.standards.map(s=>[s.code,JSON.parse(fs.readFileSync(path.join(dir,'standards',s.code+'.json'),'utf8')).analysis]));
assert.equal(exported.hierarchy.maps.length,3);
assert.equal(Object.keys(exported.analyses).length,exported.standards.length);
assert.equal(exported.relations.length,read('relations').relations.length);
console.log(JSON.stringify({status:'pass',maps:pilot.maps.length,routes,nodes:pilot.maps.reduce((n,m)=>n+m.nodes.length,0),claims:pilot.maps.reduce((n,m)=>n+m.claims.length,0),exportedStandards:exported.standards.length,checks:'references, evidence fields, route isolation, AND groups, monotone ranks, cycle rejection, export preservation'}));
