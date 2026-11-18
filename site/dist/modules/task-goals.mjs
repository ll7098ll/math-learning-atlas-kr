import {esc,url,list} from './ui.mjs';
import {renderExtraVisual} from './task-visuals.mjs';

const sourceLabels={goal:'이 경로에서 사용하는 출발 수행',entry_capability:'기초 출발 능력',within_task:'이 과제 안에서 구성·확인',task_assumption:'주어진 수학적 가정'};

export function renderTaskVisual(visual){
 if(!visual)return '';
 if(visual.kind!=='block_heights')return renderExtraVisual(visual);
 const models=visual.models.map(model=>`<div class="tp-model"><h4>${esc(model.label)}</h4><table><caption>자리별 블록 수 · 뒤쪽 줄이 위에</caption><tbody>${[...model.heights].reverse().map((row,i)=>`<tr><th scope="row">${i===0?'뒤':'앞'}</th>${row.map(n=>`<td>${esc(n)}</td>`).join('')}</tr>`).join('')}</tbody></table><p>합계 ${esc(model.heights.flat().reduce((sum,n)=>sum+n,0))}개</p></div>`).join('');
 const views=visual.views.map(view=>`<div class="tp-view"><h4>${esc(view.label)}</h4><svg viewBox="0 0 84 84" role="img" aria-label="${esc(view.label)}: ${view.cells.length}행 ${view.cells[0].length}열 중 ${view.cells.flat().filter(Boolean).length}칸이 차 있습니다.">${view.cells.map((row,y)=>row.map((filled,x)=>`<rect x="${x*40+2}" y="${y*40+2}" width="40" height="40" class="${filled?'filled':'empty'}"/>`).join('')).join('')}</svg></div>`).join('');
 return `<figure class="tp-visual"><figcaption>${esc(visual.title)}</figcaption><p>${esc(visual.description)}</p><div class="tp-model-grid">${models}</div><div class="tp-view-grid">${views}</div><p class="tp-visual-note">같은 모습이 나온다는 사실만으로 숨은 높이나 전체 개수가 하나로 정해지지는 않습니다.</p></figure>`;
}

export function conditionList(route,data,scope){
 if(!route.condition_sources)return list(route.conditions);
 return `<ul class="tp-conditions">${route.conditions.map((text,i)=>{
  const source=route.condition_sources.find(s=>s.condition_index===i);
  const goal=source?.kind==='goal'?data.goal_references[source.goal_id]:null;
  const targets=(source?.applies_to_goal_ids||[]).map(id=>data.goal_analysis?.goals.find(g=>g.id===id)?.title).filter(Boolean);
  return `<li><p>${esc(text)}</p>${source?`<details class="tp-condition-origin"><summary>${esc(sourceLabels[source.kind])}</summary>${goal?`<a href="${esc(url('hierarchy',{mode:'tasks',target:goal.code,goal:goal.id,scope}))}">${esc(goal.title)} · ${esc(goal.code)} ↗</a>`:''}<p>${esc(source.rationale)}</p>${targets.length?`<p>이 조건이 적용되는 목표: ${targets.map(esc).join(' · ')}</p>`:''}${goal?'<p>이 경로에서 사용하는 수행입니다. 출발 성취기준 전체를 먼저 숙달해야 한다는 뜻은 아닙니다.</p>':''}${source.kind==='entry_capability'?'<p>관찰·조작·기초 세기처럼 이 과제에서 함께 확인할 능력입니다.</p>':''}</details>`:''}</li>`;
 }).join('')}</ul>`;
}

export function renderGoalAnalysis(data,p,route){
 const entry=data.goal_analysis;if(!entry)return '<p class="tp-pending">이 성취기준 전체의 하위 목표와 과제 조건은 추가 대조가 필요합니다. 아래 대표 과제와 기존 원고는 각각 명시한 범위에서 읽어 주세요.</p>';
 const requested=p.get('goal'),focus=entry.goals.find(g=>g.id===requested);
 const goals=focus?[focus,...entry.goals.filter(g=>g.id!==focus.id)]:entry.goals;
 return `<section class="tp-goals"><header><span class="tp-tag">공식 문구와 해설을 나눈 자체 분석</span><h2>이 성취기준에서 확인할 하위 목표 ${entry.goals.length}개</h2><p>${esc(entry.scope)}</p></header>${focus?'<p class="tp-focus-note">선택한 하위 목표를 먼저 표시합니다. 카드 순서는 학습 순서가 아닙니다.</p>':''}<div class="tp-goal-grid">${goals.map(g=>`<article class="tp-goal-card${g.id===focus?.id?' is-selected':''}" data-goal-id="${esc(g.id)}"><h3>${esc(g.title)}</h3><p class="tp-span">공식 문구: “${esc(g.official_span)}”</p><p><strong>확인할 수행:</strong> ${esc(g.success)}</p><div class="tp-goal-tasks">${g.case_ids.map(id=>{const c=data.cases.find(c=>c.id===id);return `<a href="${esc(route({goal:g.id,taskCase:id}))}">${esc(c.title)} ↗</a>`;}).join('')}</div></article>`).join('')}</div><p class="tp-note">문장·해설·적용 시 고려 사항: 교육과정 PDF ${entry.source_review.pdf_pages.join(', ')}쪽(책자 ${entry.source_review.printed_pages.join(', ')}쪽). ${esc(entry.source_review.scope)} 하위 목표의 구분과 경로 조건은 자체 설계이며 독립 검토·학생 반응 검증 전입니다.</p></section>`;
}
