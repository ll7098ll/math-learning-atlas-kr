import React, { useLayoutEffect, useState } from "react";
import { ArrowLeft, ArrowLeftRight, BookOpen, ChevronRight, GitCompareArrows, Network, Printer } from "lucide-react";
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "@/components/ui/accordion";
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

function RelatedStandard({ entry, code, onOpen }) {
  const { standard, primary, examples } = entry;
  const { relation, label } = primary;
  const evidence = (id) => oldRoute("connections", { code, scope: "all", relation: id });
  return <li className="related-standard">
    <p className="related-kind">{label}</p>
    <h3><a id={`related-${code}-${standard.code}`} href={standardRoute(standard.code, scopeId(standard))}
      onClick={(event) => onOpen(event, standard.code)}>
      {standard.title}<ChevronRight size={17} aria-hidden="true" />
    </a></h3>
    <p className="related-location">{standard.level} · {bandOf(standard)} · {standard.code}</p>
    <p className="related-reason">{relation.rationale}</p>
    <a className="text-link related-evidence" href={evidence(relation.id)}
      aria-label={standard.title + " 연결의 적용 조건과 근거"}>적용 조건과 근거</a>
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
  const renderEntry = (entry) => <RelatedStandard key={entry.standard.code} entry={entry} code={code} onOpen={onOpen} />;
  return <section className="journey-connections" id="related-standards" aria-labelledby="related-title">
    <div className="journey-section-heading">
      <h2 id="related-title">연결된 성취기준 {groups && <span>{count}개</span>}</h2>
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

export function Detail({ catalog, params, returnTo, onOpen }) {
  const code = params.get("code");
  const s = catalog.standards.find((standard) => standard.code === code);
  const request = useContent(s && "standards/" + encodeURIComponent(s.code) + ".json", catalog.version);
  const relationPath = catalog.resourceRoot
    ? catalog.resourceRoot.replace(/^content\//, "") + "relations/" + encodeURIComponent(code) + ".json"
    : "connections.json";
  const relations = useContent(s && relationPath, catalog.version);
  if (!s) return <div className="site-width reading-page">
    <h1 tabIndex={-1}>이 성취기준을 찾을 수 없습니다.</h1>
    <a className="text-link" href={route("catalog", { q: code })}>교육과정에서 다시 검색</a>
  </div>;
  const band = bandOf(s);
  const scope = params.get("scope") || scopeId(s);
  const fallback = route("catalog", { scope: scopeId(s), band, domain: s.domain, focus: code });
  const origin = history.state?.returnTo;
  const back = origin || fallback;
  const from = new URLSearchParams(back.slice(1)).get("view");
  const catalogReturn = history.state?.catalogReturn;
  const analysis = request.data?.analysis;
  const backLabel = from === "standard" ? "직전에 본 성취기준" : from === "compare" ? "비교 화면으로"
    : origin ? "찾아보던 목록으로" : "영역 목록으로";
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
    <div className="journey-overview">
      <section id="meaning" aria-labelledby="meaning-title" className="journey-meaning">
        <h2 id="meaning-title"><BookOpen size={18} aria-hidden="true" />핵심 의미 <span>자체 해설{analysis && " · " + analysis.status}</span></h2>
        {analysis ? <p>{analysis.idea}</p> : <LoadState request={request} label="핵심 의미와 과제를 불러오고 있습니다…" />}
      </section>
      <section className="journey-official" id="official" aria-labelledby="official-title">
        <h2 id="official-title">공식 성취기준</h2>
        <p>{s.statement}</p>
        <SourceInfo standard={s} />
        <p className="official-source">교육부 고시 제2022-33호 · 별책 8 수학과 교육과정</p>
      </section>
    </div>
    <RelatedStandards catalog={catalog} standard={s} request={relations} onOpen={onOpen} analysisReady={!!analysis} />
    {analysis && <section className="journey-further" aria-labelledby="further-title">
      <h2 id="further-title">수업 과제와 상세 해설</h2>
      <Accordion type="multiple" className="analysis-accordion">
        <AccordionItem value="task">
          <AccordionTrigger>예시 과제와 진단 질문</AccordionTrigger>
          <AccordionContent forceMount>
            <p className="source-label">자체 설계 과제</p>
            <p>{analysis.task}</p>
            {analysis.probeObjects?.[0]?.question && <p><strong>진단 질문</strong>　{analysis.probeObjects[0].question}</p>}
            <div className="action-links">
              <a className="text-link" href={oldRoute("hierarchy", { mode: "tasks", target: code, scope })}>과제별 경로와 전체 조건</a>
              <a className="text-link" href={oldRoute("standard", { code, scope, section: "diagnosis" })}>오류와 후속 질문 읽기</a>
            </div>
          </AccordionContent>
        </AccordionItem>
        <AccordionItem value="evidence">
          <AccordionTrigger>적용 범위와 검토 근거</AccordionTrigger>
          <AccordionContent forceMount>
            <p>{analysis.limit}</p>
            {analysis.sourceNotes?.map((note, i) => <p key={i} className="notice">교육과정 적용 범위 · {note.scope_note}</p>)}
            <p className="small">{s.sourceReview} · {analysis.validated ? "학생 반응 검증 기록 있음" : "학생 반응 검증 전"}</p>
            <div className="action-links">
              <a className="text-link" href={oldRoute("connections", { code, scope: "all" })}>성취기준 간 전체 관계와 근거</a>
              <a className="text-link" href={oldRoute("hierarchy", { mode: "goals", target: code, scope })}>목표별 출발 조건과 후속 활용</a>
              <a className="text-link" href={oldRoute("standard", { code, scope, section: "references" })}>문헌과 검토 범위</a>
            </div>
          </AccordionContent>
        </AccordionItem>
      </Accordion>
      <details className="reading-toc">
        <summary>전체 상세 분석 목차</summary>
        <ol>{analysis.sections.map((section) => <li key={section.id}>
          <a className="text-link" href={oldRoute("standard", { code, scope, section: section.id })}>{section.title}</a>
        </li>)}</ol>
      </details>
    </section>}
    <aside className="reading-tools" aria-label="성취기준 도구">
      <Button asChild variant="outline"><a id="standard-compare"
        href={route("compare", { left: band, leftDomain: s.domain, leftCode: code })} onClick={onOpen}>
        <GitCompareArrows aria-hidden="true" />다른 범위와 비교
      </a></Button>
      <Button variant="outline" type="button" disabled={!analysis || !relations.data}
        onClick={() => window.print()}><Printer aria-hidden="true" />인쇄</Button>
    </aside>
  </article>;
}

function ComparisonControls({ side, title, band, domain, code, available, matches, standards, change }) {
  const domains = unique(available.map((s) => s.domain));
  const levels = unique(standards.map((s) => s.level));
  return <section className="comparison-header" aria-labelledby={side + "-controls"}>
      <h2 id={side + "-controls"}>{title}</h2>
      <label>학년군 · 과목
        <select value={band} onChange={(event) => change({ [side]: event.target.value, [side + "Domain"]: "", [side + "Code"]: "" })}>
          <option value="">범위 선택</option>
          {levels.map((level) => <optgroup label={level} key={level}>
            {unique(standards.filter((s) => s.level === level).map(bandOf)).map((name) => <option key={name}>{name}</option>)}
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

export function Compare({ catalog, params, go, returnTo, onOpen }) {
  const panels = ["left", "right"].map((side, index) => {
    const band = params.get(side) || "";
    const domain = params.get(side + "Domain") || "";
    const code = params.get(side + "Code") || "";
    const title = index === 0 ? "첫 번째 범위" : "두 번째 범위";
    const available = band ? selection(catalog.standards, "", band) : [];
    const matches = selection(available, "", "", domain);
    const chosen = matches.find((s) => s.code === code);
    return { side, title, band, domain, code, available, matches, shown: chosen ? [chosen] : matches };
  });
  const [left, right] = panels;
  const state = history.state;
  const back = state?.returnTo || route("catalog");
  const change = (delta) => {
    const { returnTo, returnPosition, returnState, catalogReturn, catalogPosition } = state || {};
    go(route("compare", { ...Object.fromEntries(params), ...delta }),
      { returnTo, returnPosition, returnState, catalogReturn, catalogPosition });
  };
  return <div className="site-width compare-page">
    <a className="atlas-return" href={back} onClick={(event) => returnTo(event, back)}>
      <ArrowLeft size={16} aria-hidden="true" />
      {new URLSearchParams(back.slice(1)).get("view") === "standard" ? "성취기준 상세로" : "교육과정 탐색으로"}
    </a>
    <header className="atlas-page-header">
      <h1 className="atlas-page-title" tabIndex={-1}>두 범위 비교</h1>
      <p className="atlas-page-description">학년군이나 과목을 두 개 골라 공식 성취기준을 나란히 읽어 보세요.</p>
      <div className="comparison-actions">
        <Button variant="outline" type="button" onClick={() => change({
          left: "3~4학년군", leftDomain: "수와 연산", leftCode: "4수01-09",
          right: "5~6학년군", rightDomain: "수와 연산", rightCode: "6수01-10",
        })}>예시로 분수 기준 비교</Button>
        <Button variant="outline" type="button" disabled={!left.band || !right.band} onClick={() => change({
          left: right.band, leftDomain: right.domain, leftCode: right.code,
          right: left.band, rightDomain: left.domain, rightCode: left.code,
        })}><ArrowLeftRight aria-hidden="true" />두 범위 바꾸기</Button>
      </div>
    </header>
    <div className="comparison-controls">
      {panels.map((panel) => <ComparisonControls key={panel.side} {...panel} standards={catalog.standards} change={change} />)}
    </div>
    <div className="comparison">
      {panels.map(({ side, title, band, domain, shown }) => <section key={side} className="comparison-side" aria-labelledby={side + "-results"}>
        <h2 id={side + "-results"}>{title} 결과</h2>
        {band ? <>
          <p className="result-meta" role="status">{[band, domain, `${shown.length}개 성취기준`].filter(Boolean).join(" · ")}</p>
          {shown.length ? <ul className="standard-list">
            {shown.map((standard) => <StandardRow key={standard.code} idPrefix={side + "-"}
              standard={standard} onOpen={onOpen} scope={scopeId(standard)} />)}
          </ul> : <p className="notice">이 범위에 해당하는 성취기준이 없습니다.</p>}
        </> : <p className="no-selection">위에서 학년군이나 과목을 선택하세요.</p>}
      </section>)}
    </div>
  </div>;
}
