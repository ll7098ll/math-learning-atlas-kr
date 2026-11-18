(function(root){
  'use strict';
  const presets=[
    {id:'e',title:'초등만',levels:['초등학교']},
    {id:'em',title:'초등·중학교',levels:['초등학교','중학교']},
    {id:'m',title:'중학교만',levels:['중학교']},
    {id:'mh',title:'중학교·고등학교',levels:['중학교','고등학교']},
    {id:'h',title:'고등학교만',levels:['고등학교']},
    {id:'all',title:'초·중·고 전체',levels:['초등학교','중학교','고등학교']}
  ];
  function get(id){return presets.find(p=>p.id===id)||presets[presets.length-1];}
  function allows(id,standard){return !!standard&&get(id).levels.includes(standard.level||standard.school_level);}
  function visibleHierarchy(map,route,standards,id){
    const claims=map.claims.filter(c=>c.routes.includes(route));
    const used=new Set([map.focus,...claims.flatMap(c=>[c.source,c.target])]);
    const nodes=map.nodes.filter(n=>used.has(n.id)).map(n=>({...n,boundary:!n.standards.some(c=>allows(id,standards.get(c)))}));
    return {nodes,claims,hiddenNodes:0,hiddenClaims:0,boundaryCount:nodes.filter(n=>n.boundary).length};
  }
  const api={presets,get,allows,visibleHierarchy};
  if(typeof module!=='undefined'&&module.exports){module.exports=api;return;}
  let saved;try{saved=localStorage.getItem('math-atlas-scope');}catch{}
  let current=get(new URLSearchParams(location.hash.slice(1)).get('scope')||saved||'all');
  api.current=()=>current;
  api.includes=s=>allows(current.id,s);
  api.sync=()=>{
    const params=new URLSearchParams(location.hash.slice(1));
    if(params.has('scope'))current=get(params.get('scope'));
    params.set('scope',current.id);if(!params.has('view'))params.set('view','map');
    history.replaceState(null,'','#'+params.toString());
    try{localStorage.setItem('math-atlas-scope',current.id);}catch{}
    const holder=document.getElementById('scope-options');
    if(holder)holder.innerHTML=presets.map(p=>`<button type="button" data-scope="${p.id}" aria-label="${p.title}" aria-pressed="${p.id===current.id}">${p.id==='mh'?'<span class="scope-long">'+p.title+'</span><span class="scope-short">중·고등학교</span>':'<span class="scope-option-label">'+p.title+'</span>'}<span class="scope-check" aria-hidden="true">${p.id===current.id?'✓':''}</span></button>`).join('');
  };
  api.set=id=>{current=get(id);const params=new URLSearchParams(location.hash.slice(1));params.set('scope',current.id);history.replaceState(null,'','#'+params.toString());api.sync();window.dispatchEvent(new CustomEvent('curriculum:scopechange'));};
  document.addEventListener('click',event=>{const button=event.target.closest('[data-scope]');if(button)api.set(button.dataset.scope);});
  root.CurriculumScope=api;
})(typeof window!=='undefined'?window:globalThis);
