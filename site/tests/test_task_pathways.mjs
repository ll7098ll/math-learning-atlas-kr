import fs from 'node:fs/promises';
import path from 'node:path';
import assert from 'node:assert/strict';
const dist=path.resolve(import.meta.dirname,'../dist');
const read=async p=>JSON.parse(await fs.readFile(path.join(dist,p),'utf8'));
const requests=[];
globalThis.fetch=async raw=>{const name=decodeURIComponent(String(raw).split('?')[0]);requests.push(name);return {ok:true,json:()=>read(name)};};
globalThis.window={};
const store=await import('../dist/modules/store.mjs');await store.initialize();
const {renderTaskPathway}=await import('../dist/modules/task-pathways.mjs');
const {esc}=await import('../dist/modules/ui.mjs');
const source=new Map();
for(const name of (await fs.readdir(path.resolve(dist,'../../data'))).filter(n=>/^revisions_.*\.json$/.test(n))){
 const entries=JSON.parse(await fs.readFile(path.resolve(dist,'../../data',name),'utf8'));for(const [code,value] of Object.entries(entries))source.set(code,value);
}
const authoredCases=JSON.parse(await fs.readFile(path.resolve(dist,'../../data/task_route_cases.json'),'utf8')).cases;
const goalEntries=new Map(),goalSources=new Map();
for(const name of (await fs.readdir(path.resolve(dist,'../../data'))).filter(n=>/^goal_hierarchy_.*\.json$/.test(n))){
 const corpus=JSON.parse(await fs.readFile(path.resolve(dist,'../../data',name),'utf8'));
 authoredCases.push(...corpus.cases);
 for(const entry of corpus.entries){goalEntries.set(entry.code,{...entry,authored_from:'data/'+name});for(const goal of entry.goals)goalSources.set(goal.id,{...goal,code:entry.code});}
}
let cases=0,states=0,pilots=0;
for(const standard of store.catalog.standards){
 const data=await store.taskPathway(standard.code),original=source.get(standard.code);
 assert.equal(data.code,standard.code);assert.equal(data.official_goal,standard.statement);
 assert.deepEqual(data.goal_analysis,goalEntries.get(standard.code)||null);
 for(const [id,goal] of Object.entries(data.goal_references))assert.deepEqual(goal,goalSources.get(id));
 for(const [a,b] of [['task_solution','taskSolution'],['thinking','thinking'],['recorded_conditions','conditions'],['source_routes','paths'],['diagnostics','diagnostics'],['goal_branches','goalBranches']])assert.deepEqual(data[a],original[b]||[],standard.code+'.'+a);
 cases+=data.cases.length;pilots+=!!data.pilots.length;
 if(data.pilots.some(m=>m.id==='ratio'))assert(data.pilots.find(m=>m.id==='ratio').route_relationship==='different_goals');
 for(const scope of ['all','e','m','h'])for(const selected of ['',...data.cases.flatMap(c=>c.routes.map(r=>r.id))]){
  const html=renderTaskPathway(new URLSearchParams({scope,taskRoute:selected}),data);
  assert(!html.includes('undefined'));assert(html.includes(esc(standard.statement)));
  for(const c of data.cases){assert.deepEqual(c,authoredCases.find(x=>x.id===c.id));
   for(const condition of c.shared_conditions)assert(html.includes(esc(condition)));
   for(const r of c.routes){assert.equal(r.operator,'AND');for(const condition of r.conditions)assert(html.includes(esc(condition)));assert(html.includes(esc(r.diagnostic.expected)));}
   assert.equal(c.route_relationship,'alternative_explanations');
  }
  if(!data.cases.length)assert(html.includes('추가 판정이 필요합니다.'));
  states++;
 }
 for(const g of data.goal_analysis?.goals||[]){
  for(const scope of ['all','e','m','h']){
   const html=renderTaskPathway(new URLSearchParams({scope,goal:g.id,taskCase:g.case_ids[0]}),data);
   assert(html.includes('data-goal-id="'+esc(g.id)+'"'));assert(html.includes(esc(g.success)));
   assert(html.includes('선택한 하위 목표'));
   for(const c of data.cases)for(const r of c.routes)for(const condition of r.conditions)assert(html.includes(esc(condition)));
   states++;
  }
 }
}
assert.equal(source.size,435);assert.equal(cases,authoredCases.length);assert.equal(pilots,12);
assert.equal(goalEntries.size,435);assert.equal(goalSources.size,870);
assert.equal(cases,571);
const {renderExtraVisual,renderTaskResources}=await import('../dist/modules/task-visuals.mjs');
for(const code of ['12직수02-05','12수과02-03']){
 const data=await store.taskPathway(code),c=data.cases.find(c=>c.visual);
 assert(c);const html=renderExtraVisual(c.visual);
 assert(html.includes('role="img"')&&!/NaN|undefined/.test(html));
 if(code==='12직수02-05')assert(html.includes('7000원')&&html.includes('교점'));
 else assert(html.includes('넓이 9cm²')&&html.includes('넓이 16cm²')&&html.includes('넓이 25cm²'));
}
for(const code of ['12직수04-03','12수문03-03','12수문04-01','12수문04-04','12수과03-02']){
 const data=await store.taskPathway(code);
 for(const c of data.cases)for(const resource of c.resources||[]){
  assert.deepEqual(await fs.readFile(path.resolve(dist,resource.path)),await fs.readFile(path.resolve(dist,'../../data/teaching_examples/'+path.basename(resource.path))));
 }
}
const inquiryPlan=await store.taskPathway('12수과03-01');
const methodRefs=inquiryPlan.cases.flatMap(c=>c.routes.flatMap(r=>r.condition_sources.filter(s=>s.goal_id?.startsWith('12수과02-')).map(s=>s.goal_id)));
assert.deepEqual(methodRefs,['12수과02-03:method']);
assert((await store.taskPathway('12수과03-03')).goal_analysis.goals.some(g=>g.id==='12수과03-03:present'));
for(const code of ['12경수03-01','12인수03-02','12인수04-04']){
 const data=await store.taskPathway(code),c=data.cases.find(c=>c.visual);
 assert(c);const html=renderExtraVisual(c.visual);
 assert(html.includes('role="img"')||html.includes('<table>'));assert(!/NaN|undefined/.test(html));
 if(code==='12인수03-02')assert(html.includes('밝기 +30')&&html.includes('좌우 반사')&&html.includes('255'));
 if(code==='12인수04-04')assert(html.includes('최소 a=23/14')&&html.includes('L=3/14'));
}
for(const code of ['12인수04-02','12인수04-03','12인수04-04','12인수05-02']){
 const data=await store.taskPathway(code);
 for(const c of data.cases)for(const resource of c.resources||[]){
  const source=resource.path.endsWith('.py')?'../../scripts/economy_ai_models.py':'../../data/teaching_examples/model-ai-regression.csv';
  assert.deepEqual(await fs.readFile(path.resolve(dist,resource.path)),await fs.readFile(path.resolve(dist,source)));
 }
}
for(const code of ['12실통02-03','12실통03-01','12확통03-04']){
 const data=await store.taskPathway(code),c=data.cases.find(c=>c.visual);
 assert(c);const html=renderExtraVisual(c.visual);assert(html.includes('role="img"')&&!html.includes('NaN'));
 if(code==='12실통02-03')assert(html.includes('재사용 응답 · 200개')&&html.includes('보충 시간 · 9개'));
 else if(code==='12실통03-01')assert(html.includes('1.960')&&html.includes('2.571')&&html.includes('2.042'));
 else assert(html.includes('n=10')&&html.includes('n=30')&&html.includes('n=100'));
}
for(const code of ['12실통01-01','12실통03-01','12실통03-02','12실통03-04','12확통03-07','12확통03-04']){
 const data=await store.taskPathway(code);
 for(const c of data.cases){
  const html=renderTaskResources(c.resources,c.references);
  for(const resource of c.resources||[]){
   const name=path.basename(resource.path),original=name==='stats-inference.py'?'../../scripts/statistical_tools.py':'../../data/teaching_examples/'+name;
   assert.deepEqual(await fs.readFile(path.resolve(dist,resource.path)),await fs.readFile(path.resolve(dist,original)));
   assert(html.includes(esc(resource.path))&&html.includes('download'));
  }
  for(const reference of c.references||[])assert(html.includes(esc(reference.url))&&html.includes(esc(reference.title))&&html.includes('noopener noreferrer'));
 }
}
assert(!renderTaskResources([],[{url:'javascript:alert(1)',title:'bad'}]).includes('javascript:'));
const rectangles=await store.taskPathway('12미적Ⅱ-03-04');
const rectangleCase=rectangles.cases.find(c=>c.visual?.kind==='riemann_rectangles');
assert(rectangleCase);const rectangleHtml=renderExtraVisual(rectangleCase.visual);
assert(rectangleHtml.includes('n=4')&&rectangleHtml.includes('n=8'));
assert(rectangleHtml.includes('0.46875')&&rectangleHtml.includes('0.39844'));
assert(rectangleHtml.includes('두 합은 모두 정적분 1/3으로 접근한다.'));
const conic=await store.taskPathway('12기하01-04');
const conicCase=conic.cases.find(c=>c.id==='early-12기하01-04-point-tangent');
assert.deepEqual(conicCase.routes.map(r=>r.id),['discriminant','implicit']);
assert(conicCase.routes.every(r=>r.result==='접선은 y=x−√3이다.'));
assert(!conicCase.routes[0].condition_sources.some(s=>s.goal_id?.startsWith('12미적')));
assert(conicCase.routes[1].condition_sources.some(s=>s.goal_id==='12미적Ⅱ-02-07:implicit'));
for(const code of ['12미적Ⅰ-03-03','12미적Ⅰ-03-06']){
 const data=await store.taskPathway(code),c=data.cases.find(c=>c.visual?.kind==='signed_linear_integral');
 assert(c);const html=renderExtraVisual(c.visual);
 assert(html.includes('음의 기여 −0.5')&&html.includes('양의 기여 +0.5'));
 assert(html.includes('정적분 0 · 넓이 합 1')&&html.includes('role="img"'));
}
await assert.rejects(store.taskPathway('../bad'),/등록되지/);
assert(!requests.some(p=>p.includes('connections.json')));
const substitution=await store.taskPathway('12미적Ⅱ-03-02');
assert.deepEqual(substitution.cases[0].routes.map(r=>r.id),['substitute','expand']);
assert(substitution.cases[0].routes.every(r=>r.result.includes('15/4')));
const mvt=await store.taskPathway('12미적Ⅰ-02-06');assert.equal(mvt.cases[0].routes.length,1);
const estimation=await store.taskPathway('2수03-12');
const estimationRoute=estimation.cases[0].routes[0];
const measureSource=estimationRoute.condition_sources.find(s=>s.goal_id==='2수03-10:measure');
const {conditionList}=await import('../dist/modules/task-goals.mjs');
const measureOnly=conditionList({conditions:[estimationRoute.conditions[measureSource.condition_index]],condition_sources:[{...measureSource,condition_index:0}]},estimation,'h');
const calibrationGoal=estimation.goal_analysis.goals.find(g=>g.id==='2수03-12:calibrate');
const initialEstimate=estimation.goal_analysis.goals.find(g=>g.id==='2수03-12:estimate');
assert(measureOnly.includes(esc(calibrationGoal.title)));
assert(!measureOnly.includes(esc(initialEstimate.title)),'Measuring after estimating must not become a prerequisite for initial estimation');
assert(measureOnly.includes('scope=h'));
const circle=await store.taskPathway('4수03-06');
const circleRoute=circle.cases[0].routes[0];
const radiusSource=circleRoute.condition_sources.find(s=>s.goal_id==='4수03-06:radius');
assert.deepEqual(radiusSource.applies_to_goal_ids,['4수03-06:diameter']);
const radiusHtml=conditionList({conditions:[circleRoute.conditions[radiusSource.condition_index]],condition_sources:[{...radiusSource,condition_index:0}]},circle,'e');
assert(radiusHtml.includes('target=4%EC%88%9803-06'));
assert(radiusHtml.includes('goal=4%EC%88%9803-06%3Aradius'));
assert(radiusHtml.includes('이 조건이 적용되는 목표: 지름과 반지름의 관계'));
const ratio=await store.taskPathway('6수02-03');
const ratioRoute=ratio.cases[0].routes[0];
const decimalSource=ratioRoute.condition_sources.find(s=>s.goal_id==='4수01-13:hundredths');
const decimalHtml=conditionList({conditions:[ratioRoute.conditions[decimalSource.condition_index]],condition_sources:[{...decimalSource,condition_index:0}]},ratio,'h');
assert(decimalHtml.includes('이 조건이 적용되는 목표: 비율의 소수 표현'));
assert(!decimalHtml.includes('비율의 백분율 표현'));
assert(decimalHtml.includes('scope=h'));
assert(ratio.pilots.some(m=>m.id==='ratio'&&m.route_relationship==='different_goals'));
const fractionDivision=await store.taskPathway('6수01-11');
assert.equal(fractionDivision.goal_analysis.goals.length,3);
assert.equal(fractionDivision.cases.length,3);
const fractionQuotient=await store.taskPathway('6수01-10');
assert(fractionQuotient.pilots.some(m=>m.id==='fraction'));
const triangleArea=await store.taskPathway('6수03-14');
assert.equal(triangleArea.goal_analysis.goals.length,4);
assert.equal(triangleArea.cases.length,4);
assert(triangleArea.cases.every(c=>c.routes.length===2));
assert(triangleArea.pilots.some(m=>m.id==='area'&&m.route_relationship==='alternative_explanations'));
const areaHtml=renderTaskPathway(new URLSearchParams({scope:'h',goal:'6수03-14:triangle',taskCase:'early-6수03-14-triangle'}),triangleArea);
assert(areaHtml.includes('현재 목표: 초등학교 · 5~6학년군'));
assert(areaHtml.includes('높이의 발은 밑변 선분 밖'));
assert(areaHtml.includes('같은 목표의 대안 경로 · OR'));
const chance=await store.taskPathway('6수04-06');
assert.equal(chance.goal_analysis.goals.length,2);
assert(chance.cases[0].shared_conditions.some(s=>s.includes('가상 실험 자료')));
const blockTasks=await store.taskPathway('6수03-10');
const blockHtml=renderTaskPathway(new URLSearchParams({scope:'h',goal:'6수03-10:infer',taskCase:'early-6수03-10-ambiguous'}),blockTasks);
assert(blockHtml.includes('같은 세 모습, 서로 다른 블록 수'));
assert(blockHtml.includes('합계 6개')&&blockHtml.includes('합계 8개'));
assert(blockHtml.includes('위 모습: 2행 2열 중 4칸이 차 있습니다.'));
assert(blockHtml.includes('앞 모습: 2행 2열 중 4칸이 차 있습니다.'));
assert(blockHtml.includes('오른쪽 모습: 2행 2열 중 4칸이 차 있습니다.'));
const quadratic=await store.taskPathway('9수02-20');
assert.equal(quadratic.goal_analysis.goals.length,2);
assert.equal(quadratic.cases.length,3);
const quadraticHtml=renderTaskPathway(new URLSearchParams({scope:'e',taskCase:'early-9수02-20-irrational-roots'}),quadratic);
assert(quadraticHtml.includes('현재 목표: 중학교 · 1~3학년군'));
assert(quadraticHtml.includes('같은 두 근의 완전제곱과 근의 공식'));
assert(quadraticHtml.includes('0인 해와 중근을 빠뜨리지 않기'));
assert(quadraticHtml.includes('2±√5'));
const intersection=await store.taskPathway('9수02-18');
const intersectionHtml=renderTaskPathway(new URLSearchParams({scope:'e'}),intersection);
assert(intersectionHtml.includes('교점 (2,3)'));
assert(intersectionHtml.includes('같은 점이 두 식을 모두 만족합니다'));
assert(intersectionHtml.includes('현재 목표: 중학교 · 1~3학년군'));
const boxplot=await store.taskPathway('9수04-08');
const boxHtml=renderTaskPathway(new URLSearchParams({scope:'m'}),boxplot);
assert(boxHtml.includes('같은 중앙값, 서로 다른 퍼짐'));
assert(boxHtml.includes('사분위수'));
assert(boxHtml.includes('href="examples/middle-boxplots.csv" download'));
assert(boxHtml.includes('1, 2.5, 5, 7.5, 9'));
for(const data of [boxplot,await store.taskPathway('9수04-04')])for(const c of data.cases)for(const resource of c.resources||[]){
 const name=path.basename(resource.path);
 assert.deepEqual(await fs.readFile(path.resolve(dist,resource.path)),await fs.readFile(path.resolve(dist,'../../data/teaching_examples',name)));
}
const pythagoras=await store.taskPathway('9수03-15');
assert.deepEqual(pythagoras.cases.find(c=>c.id==='early-9수03-15-proof').routes.map(r=>r.id),['area','similar']);
const pythagorasHtml=renderTaskPathway(new URLSearchParams({scope:'e',taskRoute:'area'}),pythagoras);
assert(pythagorasHtml.includes('넓이 6인 직각삼각형 네 개'));
assert(pythagorasHtml.includes('가운데 정사각형'));
assert(pythagorasHtml.includes('현재 목표: 중학교 · 1~3학년군'));
assert(pythagorasHtml.includes('data-previous-case="task-9수03-15" >'));
assert(!pythagorasHtml.includes('data-previous-case="task-9수03-15" open'));
const previousPythagorasHtml=renderTaskPathway(new URLSearchParams({taskCase:'task-9수03-15',taskRoute:'similarity'}),pythagoras);
assert(previousPythagorasHtml.includes('data-previous-case="task-9수03-15" open'));
assert(previousPythagorasHtml.includes('여기의 p는 a에 대응하는 빗변 부분'));
for(const s of store.catalog.standards.filter(s=>s.level==='중학교'))assert(goalEntries.has(s.code));
for(const [code,amounts] of [['10공수1-04-02',[1300,800]],['10기수1-04-02',[1200,1000]]]){
 const matrix=await store.taskPathway(code),html=renderTaskPathway(new URLSearchParams({scope:'e'}),matrix);
 assert(html.includes('품목의 순서를 맞춰 수량과 단가를 곱합니다'));
 assert(html.includes('<caption>단가 p · 원/개</caption>'));
 assert(html.includes('<caption>매출 Qp · 원</caption>'));
 assert(html.includes('현재 목표: 고등학교'));
 for(const amount of amounts)assert(html.includes('<td>'+amount+'</td>'));
}
for(const [code,result] of [['10공수2-02-03','{1, 2, 3, 4}'],['10기수2-02-03','{2, 3, 4, 6}']]){
 const data=await store.taskPathway(code),html=renderTaskPathway(new URLSearchParams({scope:'m'}),data);
 assert(html.includes('같은 원소를 네 벤 영역과 연산 결과에 대응합니다'));
 assert(html.includes('<small>'+result+'</small>'));
 assert.equal((html.match(/class="tp-set-panel"/g)||[]).length,4);
 assert(html.includes('현재 목표: 고등학교'));
}
console.log(JSON.stringify({status:'pass',standards:435,cases,goalDecomposedStandards:goalEntries.size,constituentGoals:goalSources.size,pilotReferencedStandards:pilots,states,checks:'authored goals and route preservation, complete AND clauses under school scope and route selection, scoped source-goal links, same-goal alternatives vs different goals, honest pending states, per-target loading'}));
