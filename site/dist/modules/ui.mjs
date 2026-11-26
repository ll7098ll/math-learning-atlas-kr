import {catalog,band,standard} from './store.mjs';
export const esc=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
export const url=(view,values={})=>'#'+new URLSearchParams({view,scope:globalThis.atlasSchoolScope||'all',...Object.fromEntries(Object.entries(values).filter(([,v])=>v!==''&&v!=null))});
export const standardURL=code=>url('standard',{code});
export const uniq=a=>[...new Set(a)];
export function overviewModes(active){return `<nav class="overview-views" aria-label="전체 조망 방식"><a href="${url('network',{mapMode:'full'})}" ${active==='network'?'aria-current="page"':''}>전체 연결망</a>${[['flow','개념별 목록',{mode:'flow'}],['structure','학교급 구조',{mode:'structure'}],['expanded','기준 펼쳐 보기',{mode:'structure',density:'expanded'}]].map(([id,title,params])=>`<a href="${url('overview',params)}" ${active===id?'aria-current="page"':''}>${title}</a>`).join('')}</nav>`;}
export const pill=(text,cls='')=>`<span class="tag ${cls}">${esc(text)}</span>`;
export const tone=d=>window.DomainIcons?.tone(d)||'blue';
export const icon=d=>window.DomainIcons?.icon(d)||'';
export const domainBadge=d=>`<span class="domain-label tone-${tone(d)}">${icon(d)}${esc(d)}</span>`;
export function heading(kicker,title,description,tools=''){
 return `<div class="page-heading"><div><p class="eyebrow">${esc(kicker)}</p><h1 tabindex="-1">${esc(title)}</h1>${description?`<p class="lead">${esc(description)}</p>`:''}</div>${tools?`<div class="heading-tools">${tools}</div>`:''}</div>`;
}
export function standardRow(s,full=false){return `<a class="standard-row" href="${standardURL(s.code)}" data-standard="${esc(s.code)}"><span class="row-code">${esc(s.code)}</span><span class="row-main"><strong>${esc(s.title)}</strong>${full?`<span class="row-statement">${esc(s.statement)}</span>`:''}<small>${esc(s.level)} · ${esc(band(s))} · ${esc(s.domain)}</small></span><span class="row-arrow" aria-hidden="true">↗</span></a>`;}
export function options(values,current,empty){return `<option value="">${esc(empty)}</option>`+values.map(v=>`<option value="${esc(v)}" ${v===current?'selected':''}>${esc(v)}</option>`).join('');}
export function scopeSelect(current='all'){return `<label>학교급<select name="scope">${[['all','초·중·고 전체'],['e','초등학교'],['m','중학교'],['h','고등학교']].map(([v,t])=>`<option value="${v}" ${current===v?'selected':''}>${t}</option>`).join('')}</select></label>`;}
export function empty(title,text='조건을 바꾸어 다시 찾아보세요.'){return `<div class="empty"><h2>${esc(title)}</h2><p>${esc(text)}</p><a class="button" href="${url('overview')}">전체 조망으로</a></div>`;}
export const list=items=>`<ul>${(items||[]).map(t=>`<li>${esc(Array.isArray(t)?t.join(' · '):t)}</li>`).join('')}</ul>`;
export function relationLiteratureHTML(relation){
 const entries=relation.literature_context||[];
 if(!entries.length)return '';
 return `<h3>관계별 문헌 대조</h3><ul>${entries.map(note=>{
  const label=esc(`${note.claim_id} · ${note.title}`);
  const citation=/^https?:\/\//.test(note.url)?`<a href="${esc(sourceHref(note.url))}" target="_blank" rel="noopener noreferrer">${label}</a>`:label;
  return `<li><strong>${esc(note.role)}</strong> · ${citation}<p>${esc(note.finding)} ${esc(note.limit)}</p></li>`;
 }).join('')}</ul>`;
}
export function markdown(text){
 function inline(t){t=t.replace(/\\\|/g,'|');
  const links=[];t=t.replace(/\[([^\]]+)\]\(([^)]+)\)/g,(_,label,raw)=>{let target=/^https?:\/\//.test(raw)?sourceHref(raw):null;const code=raw.match(/(?:^|\/)([^/]+)\.md$/)?.[1];if(!target&&standard(code))target=standardURL(code);links.push(target?`<a href="${esc(target)}" ${target.startsWith('http')?'target="_blank" rel="noopener noreferrer"':''}>${esc(label)}</a>`:esc(label));return `@@LINK${links.length-1}@@`;});
  return esc(t).replace(/\*\*([^*]+)\*\*/g,'<strong>$1</strong>').replace(/`([^`]+)`/g,'<code>$1</code>').replace(/@@LINK(\d+)@@/g,(_,i)=>links[+i]);
 }
 const lines=String(text||'').split('\n'),out=[];
 for(let i=0;i<lines.length;i++){
  const line=lines[i].trim();if(!line)continue;
  if(/^#{1,6}\s/.test(line)){out.push(`<h3>${inline(line.replace(/^#+\s*/,''))}</h3>`);}
  else if(line.startsWith('|')){const rows=[];while(i<lines.length&&lines[i].trim().startsWith('|')){const cells=lines[i].trim().replace(/^\||\|$/g,'').split(/(?<!\\)\|/).map(v=>v.trim());if(!cells.every(c=>/^[-: ]+$/.test(c)))rows.push(cells);i++;}i--;out.push(`<div class="table-wrap"><table>${rows.map((r,j)=>`<tr>${r.map(c=>`<${j?'td':'th'}>${inline(c)}</${j?'td':'th'}>`).join('')}</tr>`).join('')}</table></div>`);}
  else if(/^[-*]\s/.test(line)){const items=[];while(i<lines.length&&/^[-*]\s/.test(lines[i].trim())){items.push(`<li>${inline(lines[i].trim().replace(/^[-*]\s/,''))}</li>`);i++;}i--;out.push('<ul>'+items.join('')+'</ul>');}
  else out.push('<p>'+inline(line)+'</p>');
 }
 return out.join('');
}
// Keep citation identifiers in the source data and use verified reading addresses for outbound links.
const sourceReadingURLs = new Map([
 ["https://doi.org/10.17501/26307413.2023.6101", "https://proceedings.tiikmpublishing.com/index.php/foe/article/view/1340"],
 ["https://journals.sagepub.com/doi/10.1177/23328584241281483", "https://files.eric.ed.gov/fulltext/EJ1455604.pdf"],
 ["https://journals.sagepub.com/doi/abs/10.3102/0013189X11428813", "https://hdl.handle.net/2149/3184"],
 ["https://doi.org/10.1080/15248372.2011.554928", "https://education.umd.edu/sites/default/files/uploads/Mix%20et%20al.%202011%20One-to-One%20Play.pdf"],
 ["https://wedocs.unep.org/handle/20.500.11822/22395", "https://globalecolabelling.net/wp-content/uploads/2023/07/UN-Environment-Guidelines.pdf"],
 ["https://dash.harvard.edu/bitstreams/7312037c-9058-6bd4-e053-0100007fdf3b/download#page=14", "https://dash.harvard.edu/server/api/core/bitstreams/7312037c-9058-6bd4-e053-0100007fdf3b/content#page=14"],
 ["https://www.ipcc.ch/report/ar6/syr/", "https://www.ipcc.ch/report/ar6/syr/downloads/report/IPCC_AR6_SYR_SPM.pdf"],
 ["https://digitallibrary.un.org/record/4042857", "https://sdg2advocacyhub.org/wp-content/uploads/2024/03/food_waste_index_report_2024.pdf"],
 ["https://journals.sagepub.com/doi/10.3102/0013189X12463781", "https://research.ou.nl/ws/files/1027555/ER-DBR-FinalUnBlinded.pdf"],
 ["https://journals.sagepub.com/doi/10.3102/0013189X032001009", "https://www.les.unina.it/wp-content/uploads/2023/09/Design.pdf"],
 ["https://www.tandfonline.com/doi/abs/10.1207/s15327809jls0202_2", "https://www.cs.uml.edu/ecg/projects/cricketscience/pdf/brown-1992-design-experiments.pdf"],
 ["https://www.tandfonline.com/doi/abs/10.1207/s1532690xci0102_1", "https://images.scholastic.co.uk/assets/a/d6/6f/palincsar-reciprocal-teaching-1619152.pdf"],
 ["https://doi.org/10.1080/19345747.2016.1204640", "https://pmc.ncbi.nlm.nih.gov/articles/PMC5791897/"],
 ["https://doi.org/10.1177/07342829211037195", "https://files.eric.ed.gov/fulltext/EJ1316908.pdf"],
 ["https://doi.org/10.3102/0002831219842788", "https://files.eric.ed.gov/fulltext/EJ1234710.pdf"],
 ["https://doi.org/10.1177/23328584211026657", "https://files.eric.ed.gov/fulltext/EJ1323924.pdf"],
 ["https://doi.org/10.1177/2332858419879446", "https://files.eric.ed.gov/fulltext/EJ1238415.pdf"],
 ["https://doi.org/10.1348/000709908X398106", "https://pact.cs.cmu.edu/pubs/Rittle-Johnson%2C%20Koedinger%202009.pdf"],
 ["https://doi.org/10.3390/educsci14040350", "https://mdpi-res.com/d_attachment/education/education-14-00350/article_deploy/education-14-00350.pdf"],
 ["https://doi.org/10.3390/higheredu5010027", "https://mdpi-res.com/d_attachment/higheredu/higheredu-05-00027/article_deploy/higheredu-05-00027.pdf"],
 ["https://doi.org/10.4067/S0718-50062021000100181", "https://scielo.conicyt.cl/scielo.php?pid=S0718-50062021000100181&script=sci_arttext&tlng=es"],
]);
function sourceHref(url) {
 return sourceReadingURLs.get(url) ?? url;
}
export function sourcesHTML(sources){return sources.map(s=>`<article class="source-block"><h3>${/^https?:\/\//.test(s.url||'')?`<a href="${esc(sourceHref(s.url))}" target="_blank" rel="noopener noreferrer">${esc(s.title)} ↗</a>`:esc(s.title)}</h3><p>${esc(s.review_scope||s.kind)}</p>${s.does_not_establish?`<p class="muted">${esc(s.does_not_establish)}</p>`:''}</article>`).join('');}
