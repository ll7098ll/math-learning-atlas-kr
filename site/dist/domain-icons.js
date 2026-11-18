(function(root){
  const drawings={
    number:'<rect x="4" y="2" width="24" height="28" rx="3"/><path d="M9 8h14M10 16h4m-2-2v4m6-2h4M10 23l4 4m0-4-4 4m9-2h4"/>',
    relation:'<path d="M4 3v25h25M7 23c5 0 4-15 11-15 4 0 4 8 10 3"/><circle cx="18" cy="8" r="2"/>',
    geometry:'<path d="M3 27 15 5l13 22Z"/><circle cx="23" cy="9" r="5"/><path d="M10 27v-5h5"/>',
    data:'<path d="M3 3v25h27M8 24v-7h4v7m4 0V10h4v14m4 0V5h4v19"/>',
    matrix:'<path d="M8 3H4v26h4m16-26h4v26h-4M11 10h2m6 0h2m-10 6h2m6 0h2m-10 6h2m6 0h2"/>',
    sets:'<ellipse cx="12" cy="16" rx="9" ry="11"/><ellipse cx="21" cy="16" rx="9" ry="11"/>',
    sequence:'<circle cx="6" cy="8" r="3"/><circle cx="16" cy="16" r="3"/><circle cx="26" cy="24" r="3"/><path d="m9 10 4 4m6 4 4 4"/>',
    probability:'<rect x="4" y="4" width="24" height="24" rx="5"/><circle cx="10" cy="10" r="1"/><circle cx="22" cy="10" r="1"/><circle cx="16" cy="16" r="1"/><circle cx="10" cy="22" r="1"/><circle cx="22" cy="22" r="1"/>',
    calculus:'<path d="M4 3v25h25M6 24c7 0 5-17 15-17M8 28l15-23M11 21h9v-9"/>',
    algebra:'<path d="m5 11 12 15m0-15L5 26M22 4c7-3 10 3 4 7l-4 4h8"/>'
  };
  function kind(domain){
    if(/도형|측정|공간|벡터|이차곡선/.test(domain))return 'geometry';
    if(/행렬/.test(domain))return 'matrix';
    if(/집합|명제/.test(domain))return 'sets';
    if(/수열/.test(domain))return 'sequence';
    if(/확률|경우의 수/.test(domain))return 'probability';
    if(/미분|적분/.test(domain))return 'calculus';
    if(/다항식|방정식|부등식/.test(domain))return 'algebra';
    if(/도형|측정|공간|벡터|이차곡선/.test(domain))return 'geometry';
    if(/자료|통계/.test(domain))return 'data';
    if(/변화|관계|함수|예측|최적화/.test(domain))return 'relation';
    return 'number';
  }
  function tone(domain){const k=kind(domain);return ['geometry'].includes(k)?'green':['data','probability'].includes(k)?'purple':['relation','sequence','calculus','algebra'].includes(k)?'orange':'blue';}
  function icon(domain){return `<svg class="domain-icon" viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${drawings[kind(domain)]}</svg>`;}
  const api={kind,tone,icon};if(typeof module!=='undefined'&&module.exports)module.exports=api;else root.DomainIcons=api;
})(typeof window!=='undefined'?window:globalThis);
