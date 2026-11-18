const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path');
const Scope=require('../portal/math-atlas/dist/scope.js');
const Icons=require('../portal/math-atlas/dist/domain-icons.js');
const Hierarchy=require('../portal/math-atlas/dist/hierarchy.js');
const read=n=>JSON.parse(fs.readFileSync(path.join(__dirname,'../data',n+'.json'),'utf8'));
const standards=read('standards').standards,map=new Map(standards.map(s=>[s.code,s]));
const expected={e:121,em:181,m:60,mh:314,h:254,all:435};
for(const p of Scope.presets)assert.equal(standards.filter(s=>Scope.allows(p.id,s)).length,expected[p.id],p.id);
const pilot=read('hierarchy_pilot');let checked=0;
for(const preset of Scope.presets)for(const m of pilot.maps)for(const r of m.routes){
 const selected=Scope.visibleHierarchy(m,r.id,map,preset.id),ids=new Set(selected.nodes.map(n=>n.id));
 for(const n of selected.nodes)assert.equal(n.boundary,!n.standards.some(code=>Scope.allows(preset.id,map.get(code))));
 assert(ids.has(m.focus),'Scope must retain original target');
 for(const c of selected.claims){assert(ids.has(c.source)&&ids.has(c.target));assert(m.claims.includes(c));}
 assert.equal(selected.claims.length+selected.hiddenClaims,m.claims.filter(c=>c.routes.includes(r.id)).length);
 const levels=Hierarchy.rank(selected.nodes,selected.claims);
 for(const c of selected.claims)assert(levels.get(c.source)<levels.get(c.target));
 checked++;
}
const ratio=pilot.maps.find(m=>m.id==='ratio');
const highOnly=Scope.visibleHierarchy(ratio,'inverse',map,'h');
assert(highOnly.nodes.some(n=>n.id==='R5'&&n.boundary));assert(highOnly.nodes.some(n=>n.id==='R9'&&!n.boundary));assert.equal(highOnly.claims.length,ratio.claims.filter(c=>c.routes.includes('inverse')).length);
assert(Scope.visibleHierarchy(pilot.maps[0],'unit',map,'mh').nodes.every(n=>n.boundary));
assert.equal(Scope.get('invalid').id,'all');assert.equal(Scope.allows('e',undefined),false);
assert.equal(new Set(['수와 연산','변화와 관계','도형과 측정','자료와 가능성'].map(d=>Icons.kind(d))).size,4);
assert.equal(Icons.kind('도형의 방정식'),'geometry');assert.equal(Icons.kind('행렬'),'matrix');
for(const d of new Set(standards.map(s=>s.domain))){assert(Icons.icon(d).includes('aria-hidden="true"'));assert(Icons.tone(d));}
console.log(JSON.stringify({status:'pass',presets:6,scopedRoutes:checked,counts:expected,checks:'scope counts, node/edge isolation, no invented shortcuts, boundary targets, domain icons'}));
