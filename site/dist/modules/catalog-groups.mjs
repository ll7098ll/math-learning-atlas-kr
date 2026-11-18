import {catalog, levels, band, select, inScope} from './store.mjs';
import {esc, url, uniq, domainBadge, standardRow} from './ui.mjs';

export function catalogGroups(p, items, full) {
 const scope=p.get('scope')||'all';
 const link=changes=>url('catalog',{...Object.fromEntries(p),limit:'',...changes});
 const base=new URLSearchParams(p);base.delete('band');base.delete('domain');
 const candidates=select(base),expanded=p.get('expand')==='all';
 const domainCandidates=candidates.filter(s=>!p.get('band')||band(s)===p.get('band'));
 const domainLinks=uniq(domainCandidates.map(s=>s.domain)).map(d=>`<a class="cg-domain-chip ${p.get('domain')===d?'active':''}" href="${esc(link({domain:p.get('domain')===d?'':d}))}" ${p.get('domain')===d?'aria-current="page"':''}>${domainBadge(d)}<small>${domainCandidates.filter(s=>s.domain===d).length}</small></a>`).join('');
 const selection=[scope==='all'?'초·중·고 전체':levels.find(level=>inScope({level},scope)),p.get('band')||'전체 학년군·과목',p.get('domain')||'모든 영역'];
 const jumps=levels.filter(level=>inScope({level},scope)).map(level=>{
  const ss=candidates.filter(s=>s.level===level);
  return ss.length?`<div class="cg-jump-school"><span>${esc(level)}</span><div>${uniq(ss.map(band)).map(b=>`<a class="cg-band-chip ${p.get('band')===b?'active':''}" href="${esc(link({band:p.get('band')===b?'':b,domain:''}))}" ${p.get('band')===b?'aria-current="page"':''}>${esc(b)} <small>${ss.filter(s=>band(s)===b).length}</small></a>`).join('')}</div></div>`:'';
 }).join('');
 const schoolSections=levels.map((level,levelIndex)=>{
  const ss=items.filter(s=>s.level===level);if(!ss.length)return '';
  return `<section class="cg-school cg-school-${levelIndex}" data-catalog-school="${esc(level)}"><header class="cg-school-header"><div><span>${esc(level==='고등학교'?'과목별 성취기준':'학년군별 성취기준')}</span><h2>${esc(level)}</h2></div><strong>${ss.length}<small>개 성취기준</small></strong></header>${uniq(ss.map(band)).map(b=>{
   const matches=ss.filter(s=>band(s)===b),category=level==='고등학교'?matches[0].category:'';
   return `<section class="cg-band" data-catalog-band="${esc(b)}"><header class="cg-band-header"><div>${category?`<span class="cg-category">${esc(category)}</span>`:''}<h3>${esc(b)}</h3></div><span>${uniq(matches.map(s=>s.domain)).length}개 영역 · ${matches.length}개 기준</span></header>${b.startsWith('기본')?'<p class="cg-note">같은 번호 공통수학의 대체 이수 과목입니다.</p>':''}<div class="cg-domains">${uniq(matches.map(s=>s.domain)).map(d=>{
    const rows=matches.filter(s=>s.domain===d),key=[level,b,d].join('|');
    return `<details class="cg-domain" data-open="catalog-${esc(key)}" data-catalog-domain="${esc(d)}" ${expanded||p.get('domain')===d||p.get('q')?'open':''}><summary><span>${domainBadge(d)}<small>${rows.length}개 성취기준</small></span><b aria-hidden="true">＋</b></summary><p class="cg-preview">${rows.slice(0,3).map(s=>esc(s.title)).join(' · ')}${rows.length>3?' 외':''}</p><div class="cg-rows">${rows.map(s=>standardRow(s,full)).join('')}</div></details>`;
   }).join('')}</div></section>`;
  }).join('')}</section>`;
 }).join('');
 return `<div class="cg-browser"><nav class="cg-jumps" aria-label="학년군과 과목 바로 선택"><h2><span>1</span> 학년군 · 과목 선택</h2>${jumps}</nav><nav class="cg-domain-jumps" aria-label="내용 영역 바로 선택"><h2><span>2</span> 내용 영역 선택</h2><div><a class="cg-domain-chip ${p.get('domain')?'':'active'}" href="${esc(link({domain:''}))}" ${p.get('domain')?'':'aria-current="page"'}>모든 영역 <small>${domainCandidates.length}</small></a>${domainLinks}</div></nav></div><p class="cg-selection" aria-label="현재 선택 범위">${selection.map(s=>`<span>${esc(s)}</span>`).join('<b aria-hidden="true">›</b>')}<strong>${items.length}개 성취기준</strong></p><div class="cg-tools"><p>영역을 누르면 성취기준 원문을 펼칠 수 있습니다.</p><a class="text-link" href="${esc(link({expand:expanded?'':'all'}))}">${expanded?'영역 접기':'모든 영역 펼치기'}</a></div><div class="cg-schools">${schoolSections}</div>`;
}
