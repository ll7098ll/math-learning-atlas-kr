import {initialize,scopes,hierarchy,conceptFlows,conceptPathway,conceptPathwaysIndex,taskPathway} from './modules/store.mjs';
import {esc,url} from './modules/ui.mjs';
import {overview} from './modules/catalog.mjs';
import {focusOutlineTarget} from './modules/section-outline.mjs';
import {standardPage} from './modules/detail.mjs';
import {connectionsPage,hierarchyPage,aboutPage} from './modules/explore.mjs';
import {parse,saveState,getState,setState} from './modules/router.mjs';
import {networkPage,mountNetwork} from './modules/network.mjs';
import {resolveView} from './modules/route-views.mjs';
const main=document.querySelector('#main');
let current='',serial=0,cleanup=null;
history.scrollRestoration='manual';
 const schoolBar=document.createElement('nav');schoolBar.className='school-scope-bar';schoolBar.setAttribute('aria-label','학교급별 보기');schoolBar.innerHTML='<span>학교급별 보기</span>'+[['all','전체'],['e','초등'],['m','중등'],['h','고등']].map(([id,label])=>`<a data-school-scope="${id}" href="#view=network&scope=${id}">${label}</a>`).join('');main.before(schoolBar);
function refreshSchoolLinks(p){
 document.querySelectorAll('[data-school-scope]').forEach(a=>{const sp=new URLSearchParams(p);sp.set('scope',a.dataset.schoolScope);for(const k of ['relation','claim','band','subject','category','flowNode','edgeCode'])sp.delete(k);a.href='#'+sp;a.setAttribute('aria-current',String(a.dataset.schoolScope===globalThis.atlasSchoolScope));});
}
function remember(){if(current)saveState(current,main);}
async function render(){
 const renderStarted=performance.now();
 const ticket=++serial,route=resolveView(location.hash,'legacy'),p=route.params,view=p.get('view');
 if(route.entry==='reader'){
  location.replace('./#'+p);
  return;
 }
 const scope=p.get('scope')||sessionStorage.getItem('atlas-school-scope')||'all';
 globalThis.atlasSchoolScope=Object.hasOwn(scopes,scope)?scope:'all';
 p.set('scope',globalThis.atlasSchoolScope);
 const key='#'+p;
 if(location.hash!==key)history.replaceState(history.state,'',key);
 sessionStorage.setItem('atlas-school-scope',globalThis.atlasSchoolScope);
 document.body.dataset.scope=globalThis.atlasSchoolScope;
 document.body.dataset.navView=route.menu;
 refreshSchoolLinks(p);
 const previous=parse(current).get('view'),previousCode=parse(current).get('code');
 if(cleanup){cleanup();cleanup=null;}
 if(view==='overview'||view==='network'){try{sessionStorage.setItem('atlas-return',key);}catch{}}
 document.body.dataset.view=view;
 if(view==='standard'&&previous==='standard'&&previousCode===p.get('code')&&main.querySelector('.reading-body')){
  current=key;
  main.dataset.readyRoute=key;
  scrollToSection(p.get('section'));
  return;
 }
 main.setAttribute('aria-busy','true');main.innerHTML='<div class="loading" role="status">자료를 불러오고 있습니다…</div>';
 try{
  if(view==='hierarchy'){
   await (p.get('mode')==='tasks'&&p.get('target')?taskPathway(p.get('target')):p.get('concept')?conceptPathway(p.get('concept')):p.get('map')?hierarchy():Promise.all([hierarchy(),conceptFlows(),conceptPathwaysIndex()]));if(ticket!==serial)return;
   const dispose=await hierarchyPage(p,main,()=>ticket===serial);if(ticket!==serial){dispose?.();return;}cleanup=dispose;
  }else{
   const html=view==='network'?await networkPage(p):view==='overview'?await overview(p):view==='standard'?await standardPage(p):view==='connections'?await connectionsPage(p):await aboutPage();
   if(ticket!==serial)return;main.innerHTML=html;
   if(view==='network')cleanup=mountNetwork(p,main,hash=>{current=hash;refreshSchoolLinks(parse(hash));});
  }
  if(ticket!==serial)return;
  current=location.hash||'#view=network';main.removeAttribute('aria-busy');
  const title=main.querySelector('h1,h2')?.textContent||'수학 교육과정';document.title=title+' · 수학의 연결 지도';document.querySelector('#announce').textContent=title;
  const snapshot=getState(key);
  if(snapshot)for(const d of main.querySelectorAll('details[data-open]'))d.open=snapshot.open.includes(d.dataset.open);
  requestAnimationFrame(()=>{
   if(ticket!==serial)return;
   main.dataset.renderMs=(performance.now()-renderStarted).toFixed(1);main.dataset.readyRoute=location.hash;
   const hp=main.querySelector('.hp-scroll'),goal=main.querySelector('.hp-goal');if(hp&&goal&&!snapshot)hp.scrollLeft+=goal.getBoundingClientRect().left-hp.getBoundingClientRect().left-hp.clientWidth/2+goal.getBoundingClientRect().width/2;
   main.dataset.resources=JSON.stringify(performance.getEntriesByType('resource').filter(r=>r.name.includes('/content/')).map(r=>({path:r.name.split('/content/')[1],bytes:r.decodedBodySize,transfer:r.transferSize,duration:r.duration})));
   if(view==='hierarchy'&&p.get('concept')&&p.get('relation')&&window.innerWidth<=800)main.querySelector('#concept-evidence, #path-evidence')?.scrollIntoView({block:'start'});
   else if(view==='connections'&&p.get('relation')&&window.innerWidth<=800)main.querySelector('#relation-evidence')?.scrollIntoView({block:'start'});
   else if(p.get('section'))scrollToSection(p.get('section'));
   else if(p.get('focus')){const item=[...main.querySelectorAll('[data-standard]')].find(x=>x.dataset.standard===p.get('focus'));if(item){for(let parent=item.parentElement;parent;parent=parent.parentElement)if(parent.tagName==='DETAILS')parent.open=true;item.classList.add('located');item.scrollIntoView({block:'center'});item.focus({preventScroll:true});}}
   else if(view==='overview'&&p.get('strand')&&!snapshot)(main.querySelector('.flow-row.is-selected .flow-network')||main.querySelector('.flow-row.is-selected'))?.scrollIntoView({block:'start'});
   else if(snapshot){window.scrollTo(0,snapshot.y);for(const el of main.querySelectorAll('[data-scroll-key]')){const pos=snapshot.scrolls?.[el.dataset.scrollKey];if(pos){el.scrollLeft=pos.x;el.scrollTop=pos.y;}}const focus=snapshot.focusKey?[...main.querySelectorAll('[data-focus-key]')].find(x=>x.dataset.focusKey===snapshot.focusKey):[...main.querySelectorAll('[data-standard]')].find(x=>x.dataset.standard===snapshot.focus);focus?.focus({preventScroll:true});}
   else {window.scrollTo(0,0);main.querySelector('h1')?.focus({preventScroll:true});}
  });
 }catch(error){
  if(ticket!==serial)return;
  current=key;
  main.removeAttribute('aria-busy');
  const recover=view==='hierarchy'?['hierarchy','수학 개념 목록으로']:['catalog','교육과정 탐색으로'];
  const retry=error.invalidSelection?'':error.needsReload?'<button class="button primary" data-reload>자료 새로고침</button>':'<button class="button primary" data-retry>다시 시도</button>';
  main.innerHTML=`<div class="empty" role="alert"><h1 tabindex="-1">자료를 열지 못했습니다.</h1><p>${esc(error.message)}</p>${retry}<a href="${url(recover[0],{scope:globalThis.atlasSchoolScope})}">${recover[1]}</a></div>`;
  document.title='자료를 열지 못했습니다 · 수학의 연결 지도';
  main.querySelector('h1').focus();
 }
}
function scrollToSection(section){
 const requested = document.getElementById(section || '');
 const frame = requested?.matches('.reading-section') ? requested : main.querySelector('.reading-section[id]');
 focusOutlineTarget(frame?.querySelector('h2'), main.querySelector('.reading-jumps'));
}
document.addEventListener('click',e=>{
 if(e.target.closest('a[href="#main"]')){e.preventDefault();main.focus();return;}
 const a=e.target.closest('a[href^="#"]');if(a&&a.getAttribute('href')!=='#main'){if(current)saveState(current,main,a.dataset.standard,a.dataset.focusKey);if(a.hasAttribute('data-keep-scroll')&&!a.closest('.flow-topic')){const state=getState(current);if(state){const next={...state};if(a.hasAttribute('data-flow-select')||a.closest('.network-heading,.network-toolbar'))next.scrolls={};setState(a.getAttribute('href'),next);}}}
 if(e.target.closest('[data-print]'))window.print();if(e.target.closest('[data-retry]'))render();if(e.target.closest('[data-reload]'))location.reload();
 const scope=e.target.closest('[data-scope]');if(scope){remember();const p=parse(location.hash);p.set('scope',scope.dataset.scope);location.hash=p.toString();}
});
main.addEventListener('submit',e=>{const form=e.target.closest('[data-filter]');if(!form)return;e.preventDefault();remember();const values=Object.fromEntries(new FormData(form));if(form.dataset.filter==='hierarchy'&&values.map){const live=parse(location.hash);for(const k of ['route','target','node','claim','compare','kind']){if(live.has(k))values[k]=live.get(k);else delete values[k];}}if(form.classList.contains('full-flow-search')&&e.submitter?.tagName==='BUTTON')delete values.strand;location.hash=url(form.dataset.filter,values);});
main.addEventListener('change',e=>{
 const form=e.target.closest('form[data-filter="overview"]');if(!form)return;
 if(e.target.matches('[data-flow-jump]')){for(const key of ['q','domain','subject'])if(form.elements[key])form.elements[key].value='';}
 if(e.target.name==='edgeCode'&&form.elements.flowNode)form.elements.flowNode.value=e.target.value;
 if(e.target.matches('[data-flow-jump],[data-auto-flow]'))form.requestSubmit();
});
window.addEventListener('hashchange',()=>{remember();render();});window.addEventListener('pagehide',remember);
const initialRoute=resolveView(location.hash,'legacy');
if(initialRoute.entry==='reader')location.replace('./#'+initialRoute.params);
else try{await initialize();await render();}catch(error){main.innerHTML=`<div class="empty" role="alert"><h1>교육과정을 불러오지 못했습니다.</h1><p>${esc(error.message)}</p><button class="button" onclick="location.reload()">새로고침</button></div>`;}
