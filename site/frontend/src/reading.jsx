import React, { useLayoutEffect, useState, useSyncExternalStore } from "react";
import { ArrowLeft, ArrowLeftRight, ArrowRight, BookOpen, ChevronDown, ChevronRight, GitCompareArrows, Network, Printer } from "lucide-react";
import { Button } from "@/components/ui/button";
import { bandOf, oldRoute, route, scopeId, selection, standardRoute, unique } from "./curriculum";
import { LoadState, Pdf, StandardRow, useContent } from "./shared";
import "./reading-journey.css";

function SourceInfo({ standard }) {
  return <div className="source-links">
    {standard.pdfPages.map((page) => <Pdf key={page} page={page}>원문 PDF {page}쪽</Pdf>)}
    {standard.printedPages.length > 0 && <span>인쇄본 {standard.printedPages.join("·")}쪽</span>}
  </div>;
}

function connectionKind(relation, outgoing) {
  if (relation.type === "generalizes") return outgoing ? "이 개념을 확장하는 기준" : "이 기준의 바탕이 되는 개념";
  if (relation.type === "requires_for_task") return outgoing ? "이 기준을 활용하는 과제" : "이 과제에 쓰이는 개념";
  if (relation.type === "contrasts") return "차이를 짚어 볼 개념";
  return "의미를 함께 살펴볼 기준";
}

function connectionsFor(standard, standards, relations) {
  const byCode = new Map(standards.map((item) => [item.code, item]));
  const peers = new Map();
  const current = "standard:" + standard.code;
  for (const relation of relations) {
    const outgoing = relation.from === current;
    if (!outgoing && relation.to !== current) continue;
    const peer = outgoing ? relation.to : relation.from;
    if (!peer.startsWith("standard:") || peer === current) continue;
    const other = byCode.get(peer.slice("standard:".length));
    if (!other) continue;
    const directional = relation.type === "requires_for_task" || relation.type === "generalizes";
    const direction = directional ? (outgoing ? "out" : "in") : "shared";
    const example = { relation, direction, label: connectionKind(relation, outgoing) };
    const entry = peers.get(other.code) ?? { standard: other, examples: [] };
    entry.examples.push(example);
    if (!entry.primary || (entry.primary.direction === "shared" && directional)) entry.primary = example;
    peers.set(other.code, entry);
  }

  const all = [...peers.values()];
  const preview = [];
  for (const direction of ["in", "out"]) {
    const entry = all.find((item) => item.primary.direction === direction);
    if (entry) preview.push(entry);
  }
  if (preview.length === 0 && all.length) preview.push(all[0]);
  if (preview.length === 1 && all.length > 1) {
    const first = preview[0];
    preview.push(all.find((item) => item.standard.level !== first.standard.level) || all.find((item) => item !== first));
  }
  return { preview, more: all.filter((entry) => !preview.includes(entry)) };
}

function RelatedStandard({ entry, origin, onOpen }) {
  const { standard, primary, examples } = entry;
  const code = origin.code;
  const { relation, label } = primary;
  const evidence = (id) => oldRoute("connections", { code, scope: "all", relation: id });
  const comparison = route("compare", {
    left: bandOf(origin), leftDomain: origin.domain, leftCode: code,
    right: bandOf(standard), rightDomain: standard.domain, rightCode: standard.code,
  });
  return <li className="related-standard">
    <p className="related-kind">{label}</p>
    <h3><a id={`related-${code}-${standard.code}`} href={standardRoute(standard.code, scopeId(standard))}
      onClick={(event) => onOpen(event, standard.code)}>
      {standard.title}<ChevronRight size={17} aria-hidden="true" />
    </a></h3>
    <p className="related-location">{standard.level} · {bandOf(standard)} · {standard.code}</p>
    <p className="related-reason">{relation.rationale}</p>
    <div className="related-actions">
      <a className="text-link related-evidence" href={evidence(relation.id)}
        aria-label={standard.title + " 연결의 적용 조건과 근거"}>적용 조건과 근거</a>
      <a className="text-link related-evidence" href={comparison} id={`related-${code}-compare-${standard.code}`}
        aria-label={code + "와 " + standard.code + " 두 기준 원문 비교"} onClick={(event) => onOpen(event)}>두 기준 원문 비교</a>
    </div>
    {examples.length > 1 && <details className="related-alternatives">
      <summary>두 기준 사이의 다른 연결 설명 {examples.length - 1}개</summary>
      <ul>{examples.filter((example) => example !== primary).map((example) => <li key={example.relation.id}>
        <p className="related-kind">{example.label}</p>
        <p>{example.relation.rationale}</p>
        <a className="text-link related-evidence" href={evidence(example.relation.id)}
          aria-label={standard.title + " · " + example.relation.id + "의 적용 조건과 근거"}>적용 조건과 근거</a>
      </li>)}</ul>
    </details>}
  </li>;
}

function RelatedStandards({ catalog, standard, request, onOpen, analysisReady }) {
  const code = standard.code;
  const [level, setLevel] = useState(() => {
    const saved = history.state?.relatedFilter;
    return saved?.code === code ? saved.level : "";
  });

  function chooseLevel(value) {
    history.replaceState({ ...history.state, relatedFilter: { code, level: value } }, "");
    setLevel(value);
  }
  useLayoutEffect(() => {
    const saved = history.state?.focusOnReturn;
    if (!analysisReady || !request.data || !saved?.id?.startsWith("related-" + code + "-")) return;
    const target = document.getElementById(saved.id);
    if (!target) return;
    const details = target.closest("details");
    if (details) details.open = true;
    target.focus({ preventScroll: true });
    window.scrollTo(0, saved.scroll);
  }, [code, request.data, analysisReady]);

  const groups = request.data && connectionsFor(standard, catalog.standards, request.data.relations);
  const count = groups && groups.preview.length + groups.more.length;
  const levels = groups ? unique(groups.more.map((entry) => entry.standard.level)) : [];
  const more = groups?.more.filter((entry) => !level || entry.standard.level === level);
  const renderEntry = (entry) => <RelatedStandard key={entry.standard.code} entry={entry} origin={standard} onOpen={onOpen} />;
  return <section className="journey-connections" id="related-standards" aria-labelledby="related-title">
    <div className="journey-section-heading">
      <h2 id="related-title" tabIndex={-1}>연결된 성취기준 {groups && <span>{count}개</span>}</h2>
      <a className="journey-map-link" href={oldRoute("network", { node: code, scope: "all" })}><Network size={16} aria-hidden="true" />연결 지도</a>
    </div>
    {!groups ? <LoadState request={request} label="이 기준과 연결된 성취기준을 불러오고 있습니다…" />
      : count === 0 ? <p className="small">이 기준과 직접 연결된 다른 성취기준은 아직 기록되지 않았습니다.</p>
      : <>
        <p className="journey-caption">각 설명은 자체 분석에서 다룬 과제와 개념에 적용됩니다.</p>
        <ul className="related-items">{groups.preview.map(renderEntry)}</ul>
        {groups.more.length > 0 && <details className="related-more">
          <summary>연결된 성취기준 {groups.more.length}개 더 보기</summary>
          {groups.more.length > 12 && levels.length > 1 && <label className="related-filter">학교급으로 좁히기
            <select value={level} onChange={(event) => chooseLevel(event.target.value)}>
              <option value="">모든 학교급</option>
              {levels.map((name) => <option key={name}>{name}</option>)}
            </select>
          </label>}
          <ul className="related-items">{more.map(renderEntry)}</ul>
        </details>}
      </>}
  </section>;
}

const readingPanels = [
  ["official", "공식 원문"], ["meaning", "핵심 해설"], ["task", "수업 과제"],
  ["related-standards", "기준 연결"], ["evidence", "검토 근거"], ["full-analysis", "전체 분석"],
];

function jumpToPanel(id) {
  const heading = document.getElementById(id)?.querySelector("h2");
  if (heading) {
    heading.focus({ preventScroll: true });
    heading.scrollIntoView({ block: "start" });
  }
}

function manuscriptProbe(analysis) {
  const paired = (item) => item?.question && item.expected;
  const structured = analysis?.probeObjects?.find(paired) || analysis?.revision?.diagnostics?.find(paired);
  if (structured) return structured;
  const row = analysis?.probes?.find((item) => Array.isArray(item) && item[0] && item[1]);
  return row && { question: row[0], expected: row[1], interpretation: row[2], followup: row[3] };
}

function ManuscriptTask({ analysis, probe, code, scope }) {
  const task = analysis.revision?.task || analysis.task;
  const paragraphs = task?.split(/\n\s*\n/).filter(Boolean) || [];
  const observation = analysis.stepObjects?.find((item) => item.observable)?.observable;
  return <>
    <div className="task-prompt manuscript-task">
      <h3>{task ? "해설 원고의 대표 과제" : "해설 원고의 확인 질문"}</h3>
      {paragraphs.length > 0 && <p>{paragraphs[0]}</p>}
    </div>
    {probe ? <div className="task-observation">
      <div><h4>학생에게 물어볼 질문</h4><p>{probe.question}</p></div>
      <div><h4>살펴볼 설명 · 기대 수행</h4><p>{probe.expected}</p>
        {probe.followup && <p className="probe-followup"><strong>다시 물어볼 때</strong> {probe.followup}</p>}
      </div>
    </div> : observation && <div className="task-observation"><div><h4>살펴볼 수행</h4><p>{observation}</p></div></div>}
    <p className="task-review">{analysis.validated ? "학생 반응 검증 기록 있음" : "학생 반응 검증 전"}</p>
    <details className="reading-disclosure">
      <summary>대표 과제의 해설과 관찰점</summary>
      <div className="reading-disclosure-body">
        {paragraphs.slice(1).map((paragraph, index) => <p key={index}>{paragraph}</p>)}
        {probe?.interpretation && <><h4>답변을 해석할 때 살펴볼 점</h4><p>{probe.interpretation}</p></>}
        {analysis.revision?.taskSolution && <><h4>원고에 제시한 풀이</h4><p>{analysis.revision.taskSolution}</p></>}
        <a className="text-link" href={oldRoute("standard", { code, scope, section: "task" })}>대표 과제 해설 전문</a>
      </div>
    </details>
  </>;
}

function TaskReading({ data, analysis, request, analysisRequest, scope, code, params, go }) {
  const requestedCase = params.get("taskCase");
  const requestedRoute = params.get("taskRoute");
  const cases = (data?.cases || []).filter((item) => item.standard === code);
  const activeCases = cases.filter((item) => !item.superseded_by_case_ids?.length);
  const probe = manuscriptProbe(analysis);
  const hasManuscript = !!(analysis?.revision?.task || analysis?.task || probe);
  const explicit = !!(requestedCase || requestedRoute || (analysis && !hasManuscript));
  const task = requestedCase ? cases.find((item) => item.id === requestedCase)
    : requestedRoute ? activeCases.find((item) => item.routes.some((r) => r.id === requestedRoute)) : activeCases[0];
  const path = requestedRoute ? task?.routes.find((item) => item.id === requestedRoute) : task?.routes[0];
  const target = oldRoute("hierarchy", { mode: "tasks", target: code, scope, taskCase: task?.id, taskRoute: path?.id });
  const selectionURL = (taskCase, taskRoute) => route("standard", {
    ...Object.fromEntries(params), panel: "task", taskCase, taskRoute,
  });
  function openTask(event) {
    if (event.button !== 0 || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
    event.preventDefault();
    go(event.currentTarget.getAttribute("href"), { ...history.state, focusOnReturn: undefined });
  }
  const showTask = explicit && task && path;
  return <section className="reading-block journey-task" id="task" aria-labelledby="task-title">
    <div className="reading-section-title"><h2 id="task-title" tabIndex={-1}>수업에서 물어보기</h2><span>자체 설계 과제</span></div>
    {!explicit && (analysis ? <ManuscriptTask analysis={analysis} probe={probe} code={code} scope={scope} />
      : <LoadState request={analysisRequest} label="대표 질문을 불러오고 있습니다…" />)}
    {showTask && <>
      <div className="task-prompt explicit-task">
        <h3>{task.title}</h3>
        {task.superseded_by_case_ids?.length > 0 && <p className="task-review">이전 설계 · 보존한 과제</p>}
        <p>{task.task}</p>
      </div>
      {task.routes.length > 1 && <label className="task-picker">살펴볼 설명 경로
        <select value={path.id} onChange={(event) => go(selectionURL(task.id, event.target.value), { ...history.state, focusOnReturn: undefined })}>
          {task.routes.map((item) => <option key={item.id} value={item.id}>{item.title}</option>)}
        </select>
      </label>}
      <div className="task-observation">
        <div><h4>학생에게 물어볼 질문</h4><p>{path.diagnostic.question}</p></div>
        <div><h4>살펴볼 설명 · 기대 수행</h4><p>{path.diagnostic.expected}</p></div>
      </div>
      <p className="task-review">{task.review?.student_validated ? "학생 반응 검증 기록 있음" : "학생 반응 검증 전"} · {task.review?.independent_review ? "독립 검토 기록 있음" : "독립 검토 전"}</p>
      <details className="reading-disclosure" key={task.id + path.id}>
        <summary>이 과제의 목표와 적용 조건</summary>
        <div className="reading-disclosure-body">
          <h4>확인할 수행</h4><p>{task.goal}</p>
          {task.shared_conditions?.length > 0 && <><h4>모든 경로에 적용할 조건</h4><ul>{task.shared_conditions.map((text, i) => <li key={i}>{text}</li>)}</ul></>}
          <h4>‘{path.title}’ 경로에서 함께 필요한 조건</h4>
          <ul>{path.conditions.map((text, i) => <li key={i}>{text}</li>)}</ul>
        </div>
      </details>
      <a className="reading-next" id={"task-path-" + code} href={target}>이 과제의 풀이와 전체 경로 <ArrowRight size={16} aria-hidden="true" /></a>
    </>}
    {explicit && data && !showTask && <p className="notice">이 기준에서 요청한 과제나 설명 경로를 찾을 수 없습니다.</p>}
    {!data && <LoadState request={request} label="다른 과제를 불러오고 있습니다…" />}
    {data && <div className="task-choices">
      {explicit && hasManuscript && <a className="reading-next" onClick={openTask} href={selectionURL("", "")}><ArrowLeft size={16} aria-hidden="true" />해설 원고의 대표 과제로</a>}
      {activeCases.some((item) => !showTask || item.id !== task.id) && <>
        <h3>다른 과제의 경로와 조건</h3>
        <ul>{activeCases.filter((item) => !showTask || item.id !== task.id).map((item) => <li key={item.id}>
          <a className="reading-next" onClick={openTask} href={selectionURL(item.id, "")}>{item.title} <ArrowRight size={16} aria-hidden="true" /></a>
        </li>)}</ul>
      </>}
      {!hasManuscript && !activeCases.length && <a className="text-link" href={oldRoute("hierarchy", { mode: "goals", target: code, scope })}>이 기준의 하위 목표 보기</a>}
    </div>}
  </section>;
}
export function Detail({ catalog, params, go, returnTo, onOpen }) {
  const code = params.get("code");
  const s = catalog.standards.find((standard) => standard.code === code);
  const request = useContent(s && "standards/" + encodeURIComponent(s.code) + ".json", catalog.version);
  const relationPath = catalog.resourceRoot
    ? catalog.resourceRoot.replace(/^content\//, "") + "relations/" + encodeURIComponent(code) + ".json"
    : "connections.json";
  const relations = useContent(s && relationPath, catalog.version);
  const taskIndex = useContent(s && "task-pathways-index.json", catalog.version);
  const taskHash = taskIndex.data?.files?.[code];
  const taskData = useContent(taskHash && "task-pathways/items/" + taskHash + ".json", catalog.version);
  const requestedCase = params.get("taskCase");
  const panel = params.get("panel") || ((requestedCase || params.get("taskRoute")) ? "task" : "");
  useLayoutEffect(() => {
    if (panel && !history.state?.focusOnReturn) jumpToPanel(panel);
  }, [panel, code, requestedCase]);
  const readingReady = !!(request.data && relations.data && taskIndex.data && (!taskHash || taskData.data));
  useLayoutEffect(() => {
    if (!panel || !readingReady || history.state?.focusOnReturn) return;
    const heading = document.getElementById(panel)?.querySelector("h2");
    if (heading && document.activeElement === heading) heading.scrollIntoView({ block: "start" });
  }, [panel, readingReady]);
  if (!s) return <div className="site-width reading-page">
    <h1 tabIndex={-1}>이 성취기준을 찾을 수 없습니다.</h1>
    <a className="text-link" href={route("catalog", { q: code })}>교육과정에서 다시 검색</a>
  </div>;
  const band = bandOf(s);
  const scope = params.get("scope") || scopeId(s);
  const fallback = route("catalog", { scope: scopeId(s), band, domain: s.domain, focus: code });
  const origin = history.state?.returnTo;
  const exploreOrigin = !origin && history.state?.exploreOrigin;
  const back = origin || exploreOrigin?.href || fallback;
  const from = new URLSearchParams(back.slice(1)).get("view");
  const catalogReturn = history.state?.catalogReturn;
  const analysis = request.data?.analysis;
  const backLabel = from === "standard" ? "직전에 본 성취기준" : from === "compare" ? "비교 화면으로"
    : origin ? "찾아보던 목록으로" : exploreOrigin?.label || "영역 목록으로";
  const panelURL = (id) => route("standard", { ...Object.fromEntries(params), panel: id });
  function openPanel(event, id) {
    if (event.button !== 0 || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
    event.preventDefault();
    if (panel === id) jumpToPanel(id);
    else go(panelURL(id), { ...history.state, focusOnReturn: undefined });
  }
  return <article className="site-width reading-page journey-page" key={code}>
    <nav className="journey-return" aria-label="탐색으로 돌아가기">
      <a className="atlas-return" href={back} onClick={(event) => returnTo(event, back)}><ArrowLeft size={16} aria-hidden="true" />{backLabel}</a>
      {from === "standard" && catalogReturn && <a className="text-link journey-catalog-return" href={catalogReturn}
        onClick={(event) => returnTo(event, catalogReturn)}>찾아보던 목록으로</a>}
    </nav>
    <header className="journey-heading">
      <div className="journey-location">
        <span className="standard-code">{code}</span>
        <nav className="breadcrumbs" aria-label="교육과정 위치">
          <a href={route("catalog", { scope: scopeId(s) })}>{s.level}</a><span aria-hidden="true">/</span>
          <a href={route("catalog", { scope: scopeId(s), band })}>{band}</a><span aria-hidden="true">/</span>
          <a href={fallback}>{s.domain}</a>
        </nav>
      </div>
      <h1 tabIndex={-1} aria-describedby="journey-title-source">{s.title}</h1>
      <p className="sr-only" id="journey-title-source">자체 분석 제목</p>
    </header>
    <nav className="reading-jumps" aria-label="이 기준의 읽을거리">
      {readingPanels.map(([id, label]) => <a key={id} href={panelURL(id)} aria-current={panel === id ? "location" : undefined}
        onClick={(event) => openPanel(event, id)}>{label}</a>)}
    </nav>
    <section className="journey-official" id="official" aria-labelledby="official-title">
      <h2 id="official-title" tabIndex={-1}><BookOpen size={19} aria-hidden="true" />공식 성취기준</h2>
      <blockquote>{s.statement}</blockquote>
      <p className="official-source">교육부 고시 제2022-33호 · 별책 8 수학과 교육과정</p>
      <SourceInfo standard={s} />
    </section>
    <section id="meaning" aria-labelledby="meaning-title" className="reading-block journey-meaning">
      <div className="reading-section-title"><h2 id="meaning-title" tabIndex={-1}>핵심 의미</h2><span>자체 해설{analysis && " · " + analysis.status}</span></div>
      {analysis ? <p>{analysis.revision?.mathematicalMeaning || analysis.idea}</p> : <LoadState request={request} label="핵심 해설을 불러오고 있습니다…" />}
    </section>
    <TaskReading key={code} scope={scope} code={code} params={params} go={go} analysis={analysis} analysisRequest={request} data={taskData.data || (taskIndex.data && !taskHash ? {} : null)}
      request={taskIndex.data ? taskData : taskIndex} />
    <RelatedStandards key={code} catalog={catalog} standard={s} request={relations} onOpen={onOpen} analysisReady={!!analysis} />
    <section className="reading-block journey-evidence" id="evidence" aria-labelledby="evidence-title">
      <h2 id="evidence-title" tabIndex={-1}>적용 범위와 검토 근거</h2>
      {analysis ? <>
        <p>{analysis.limit}</p>
        {analysis.sourceNotes?.map((note, i) => <p key={i} className="small">교육과정 적용 범위 · {note.scope_note}</p>)}
        <p className="review-line">{s.sourceReview}{analysis.revision?.review?.independentReview != null && (analysis.revision.review.independentReview ? " · 독립 검토 기록 있음" : " · 독립 검토 전")} · {analysis.validated ? "학생 반응 검증 기록 있음" : "학생 반응 검증 전"}</p>
      </> : <LoadState request={request} label="검토 범위를 불러오고 있습니다…" />}
      <div className="action-links">
        <a className="text-link" href={oldRoute("standard", { code, scope, section: "references" })}>문헌의 주장과 검토 범위</a>
        <a className="text-link" href={oldRoute("connections", { code, scope: "all" })}>관계별 근거</a>
        <a className="text-link" href={oldRoute("hierarchy", { mode: "goals", target: code, scope })}>목표별 출발 조건과 후속 활용</a>
      </div>
    </section>
    <section className="reading-block journey-full" id="full-analysis" aria-labelledby="full-title">
      <h2 id="full-title" tabIndex={-1}>전체 상세 분석</h2>
      {analysis && <ol className="reading-chapters">{analysis.sections.map((section) => <li key={section.id}>
        <a href={oldRoute("standard", { code, scope, section: section.id })}>{section.title}<ChevronRight size={15} aria-hidden="true" /></a>
      </li>)}</ol>}
      <a className="reading-next" href={oldRoute("standard", { code, scope, section: "curriculum" })}>전체 원고 열기 <ArrowRight size={16} aria-hidden="true" /></a>
    </section>
    <aside className="reading-tools" aria-label="성취기준 도구">
      <Button asChild variant="outline"><a id="standard-compare"
        href={route("compare", { left: band, leftDomain: s.domain, leftCode: code })} onClick={onOpen}>
        <GitCompareArrows aria-hidden="true" />다른 범위와 비교
      </a></Button>
      <Button variant="outline" type="button" disabled={!readingReady}
        onClick={() => window.print()}><Printer aria-hidden="true" />인쇄</Button>
    </aside>
  </article>;
}

function ComparisonControls({ side, title, band, domain, code, available, matches, standards, change }) {
  const domains = unique(available.map((s) => s.domain));
  const levels = unique(standards.map((s) => s.level));
  return <section className="comparison-header" aria-labelledby={side + "-controls"}>
      <h2 id={side + "-controls"}>{title}</h2>
      <label className="comparison-band">학년군 · 과목
        <select id={side + "-band"} value={band} onChange={(event) => change({ [side]: event.target.value, [side + "Domain"]: "", [side + "Code"]: "" })}>
          <option value="">학년군 또는 과목 선택</option>
          {levels.map((level) => <optgroup label={level} key={level}>
            {unique(standards.filter((s) => s.level === level).map(bandOf)).map((name) => <option key={name} value={name}>{level === "고등학교" ? name : level + " " + name}</option>)}
          </optgroup>)}
        </select>
      </label>
      {band && <>
        <label>내용 영역
          <select value={domain} onChange={(event) => change({ [side + "Domain"]: event.target.value, [side + "Code"]: "" })}>
            <option value="">모든 영역</option>
            {domains.map((name) => <option key={name}>{name}</option>)}
          </select>
        </label>
        <label>성취기준
          <select value={code} onChange={(event) => change({ [side + "Code"]: event.target.value })}>
            <option value="">선택 영역의 모든 기준</option>
            {matches.map((s) => <option key={s.code} value={s.code}>{s.code} · {s.title}</option>)}
          </select>
        </label>
      </>}
    </section>;
}

function RangeResults({ panel, onOpen, change, initialCount }) {
  const { side, title, band, domain, code, chosen, shown } = panel;
  const restored = history.state?.focusOnReturn?.id;
  const [expanded, setExpanded] = useState(() =>
    shown.slice(initialCount).some((standard) => restored === side + "-std-" + standard.code));
  function chooseBand() {
    const select = document.getElementById(side + "-band");
    select.focus({ preventScroll: true });
    select.scrollIntoView({ block: "center" });
  }
  return <section className="comparison-side" aria-labelledby={side + "-results"}>
    <header className="comparison-result-heading">
      <p className="comparison-side-label">{title}</p>
      <h2 id={side + "-results"}>{band || "선택한 범위가 없습니다"}</h2>
      {band && <p className="result-meta" role="status">{[domain || "모든 영역", shown.length + "개 성취기준"].join(" · ")}</p>}
    </header>
    {!band ? <button className="select-range" onClick={chooseBand}>학년군 또는 과목 고르기 <ArrowRight size={16} aria-hidden="true" /></button>
      : shown.length ? <>
        <ul className="standard-list compare-result-list" data-expanded={expanded} data-compact={initialCount === 1}>
          {shown.map((standard) => <StandardRow key={standard.code} idPrefix={side + "-"} standard={standard} onOpen={onOpen} scope={scopeId(standard)} />)}
        </ul>
        {chosen && <div className="comparison-original"><SourceInfo standard={chosen} /></div>}
        {shown.length > initialCount && <button type="button" className="select-range" aria-expanded={expanded}
          onClick={() => setExpanded(!expanded)}>{expanded ? "처음 " + initialCount + "개만 보기" : "나머지 " + (shown.length - initialCount) + "개 기준 보기"}</button>}
      </> : <div className="comparison-empty"><p>이 선택에 맞는 성취기준이 없습니다.</p>
        <button type="button" className="select-range" onClick={() => {
          if (code || domain) change({ [side + "Domain"]: "", [side + "Code"]: "" });
          else chooseBand();
        }}>{code || domain ? "영역과 코드 선택 해제" : "학년군 또는 과목 다시 고르기"}</button>
      </div>}
  </section>;
}

const compactComparison = () => window.matchMedia("(max-width: 700px)").matches;
function subscribeComparisonWidth(update) {
  const query = window.matchMedia("(max-width: 700px)");
  query.addEventListener("change", update);
  return () => query.removeEventListener("change", update);
}

export function Compare({ catalog, params, go, returnTo, onOpen }) {
  const panels = ["left", "right"].map((side, index) => {
    const band = params.get(side) || "";
    const domain = params.get(side + "Domain") || "";
    const code = params.get(side + "Code") || "";
    const title = index === 0 ? "첫 번째 범위" : "두 번째 범위";
    const available = band ? selection(catalog.standards, "", band) : [];
    const matches = selection(available, "", "", domain);
    const chosen = matches.find((s) => s.code === code);
    return { side, title, band, domain, code, available, matches, chosen, shown: code ? (chosen ? [chosen] : []) : matches };
  });
  const [left, right] = panels;
  const rangesReady = left.available.length > 0 && right.available.length > 0;
  const compact = useSyncExternalStore(subscribeComparisonWidth, compactComparison);
  const [editingRanges, setEditingRanges] = useState(false);
  const state = history.state;
  const back = state?.returnTo || state?.exploreOrigin?.href || route("catalog");
  const change = (delta) => {
    if (!rangesReady) setEditingRanges(false);
    go(route("compare", { ...Object.fromEntries(params), ...delta }), { ...state, focusOnReturn: undefined });
    if (!rangesReady && (delta.left ?? left.band) && (delta.right ?? right.band)) {
      requestAnimationFrame(() => {
        const toggle = document.getElementById("comparison-edit");
        if (toggle?.getClientRects().length) toggle.focus();
      });
    }
  };
  return <div className="site-width compare-page" data-ranges-ready={rangesReady} data-pair={!!left.chosen && !!right.chosen}>
    <a className="atlas-return" href={back} onClick={(event) => returnTo(event, back)}>
      <ArrowLeft size={16} aria-hidden="true" />
      {!state?.returnTo && state?.exploreOrigin ? state.exploreOrigin.label || "읽던 화면으로"
        : new URLSearchParams(back.slice(1)).get("view") === "standard" ? "성취기준 상세로" : "교육과정 탐색으로"}
    </a>
    <header className="atlas-page-header">
      <h1 className="atlas-page-title" tabIndex={-1}>두 범위 비교</h1>
      <p className="atlas-page-description">두 학년군이나 과목에서 무엇을 배우는지 공식 원문으로 살펴보세요. 영역이나 성취기준 하나까지 좁힐 수 있습니다.</p>
      <div className="comparison-actions">
        {!left.band && !right.band && <Button variant="outline" type="button" onClick={() => change({
          left: "3~4학년군", leftDomain: "수와 연산", leftCode: "4수01-09",
          right: "5~6학년군", rightDomain: "수와 연산", rightCode: "6수01-10",
        })}>분수의 의미와 나눗셈 예시 열기 <ArrowRight aria-hidden="true" /></Button>}
        <Button variant="outline" type="button" disabled={!left.band || !right.band} onClick={() => change({
          left: right.band, leftDomain: right.domain, leftCode: right.code,
          right: left.band, rightDomain: left.domain, rightCode: left.code,
        })}><ArrowLeftRight aria-hidden="true" />두 범위 교환</Button>
        <Button variant="outline" type="button" disabled={!left.shown.length && !right.shown.length} onClick={() => window.print()}><Printer aria-hidden="true" />비교 인쇄</Button>
      </div>
    </header>
    {rangesReady && <button type="button" id="comparison-edit" className="comparison-edit" aria-controls="comparison-controls"
      aria-expanded={editingRanges} onClick={() => setEditingRanges(!editingRanges)}>
      <span>비교 범위 변경 <small>{left.band} · {right.band}</small></span><ChevronDown aria-hidden="true" size={18} />
    </button>}
    <div className="comparison-controls" id="comparison-controls" data-editing={editingRanges}>
      {panels.map((panel) => <ComparisonControls key={panel.side} {...panel} standards={catalog.standards} change={change} />)}
    </div>
    <div className="comparison">
      {panels.map((panel) => <RangeResults key={[panel.side, panel.band, panel.domain, panel.code].join("|")} panel={panel} change={change} onOpen={onOpen} initialCount={compact && rangesReady ? 1 : 3} />)}
    </div>
  </div>;
}
