import React from "react";
import { ArrowLeft, BookOpen, GitCompareArrows, Network, Printer } from "lucide-react";
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "@/components/ui/accordion";
import { Button } from "@/components/ui/button";
import { bandOf, oldRoute, route, scopeId, selection, unique } from "./curriculum";
import { LoadState, Pdf, StandardRow, useContent } from "./shared";

function SourceInfo({ standard }) {
  return <div className="source-links">
    {standard.pdfPages.map((page) => <Pdf key={page} page={page}>PDF {page}쪽 열기</Pdf>)}
    {standard.printedPages.length > 0 && <span>인쇄 {standard.printedPages.join("·")}쪽</span>}
  </div>;
}

export function Detail({ catalog, params, returnTo }) {
  const code = params.get("code");
  const s = catalog.standards.find((standard) => standard.code === code);
  const request = useContent(s && "standards/" + encodeURIComponent(s.code) + ".json", catalog.version);
  if (!s) return <div className="site-width reading-page">
    <h1 tabIndex={-1}>이 성취기준을 찾을 수 없습니다.</h1>
    <a className="text-link" href={route("catalog", { q: code })}>교육과정에서 다시 검색</a>
  </div>;
  const band = bandOf(s);
  const scope = params.get("scope") || scopeId(s);
  const fallback = route("catalog", { scope: scopeId(s), band, domain: s.domain, focus: code });
  const back = history.state?.returnTo || fallback;
  const fromComparison = new URLSearchParams(back.slice(1)).get("view") === "compare";
  const analysis = request.data?.analysis;
  return <div className="site-width reading-page">
    <a className="back-link text-link" href={back} onClick={(event) => returnTo(event, back)}>
      <ArrowLeft size={16} aria-hidden="true" />
      {fromComparison ? "비교 화면으로" : history.state?.returnTo ? "찾아보던 목록으로" : "영역 목록으로"}
    </a>
    <nav className="breadcrumbs" aria-label="교육과정 위치">
      <a href={route("catalog", { scope: scopeId(s) })}>{s.level}</a>
      <span aria-hidden="true">/</span>
      <a href={route("catalog", { scope: scopeId(s), band })}>{band}</a>
      <span aria-hidden="true">/</span>
      <a href={fallback}>{s.domain}</a>
    </nav>
    <div className="reading-layout">
      <article className="reading-body">
        <header className="atlas-page-header">
          <span className="standard-code">{code}</span>
          <h1 className="atlas-page-title" tabIndex={-1}>{s.title}</h1>
          <p className="row-location">성취기준을 설명하는 분석 제목</p>
        </header>
        <section className="official-card" id="official">
          <h2>공식 성취기준</h2>
          <p>{s.statement}</p>
          <SourceInfo standard={s} />
          <p className="small">교육부 고시 제2022-33호 · 별책 8 수학과 교육과정</p>
        </section>
        {!analysis ? <LoadState request={request} label="분석과 수업 과제를 불러오고 있습니다…" />
          : <div className="analysis">
            <div className="analysis-heading">
              <h2>분석과 수업 과제</h2>
              <p className="small">자체 분석 {analysis.status} · {analysis.validated ? "학생 반응 검증 기록 있음" : "학생 반응 검증 전"}</p>
            </div>
            <Accordion type="multiple" defaultValue={["meaning"]} className="analysis-accordion">
              <AccordionItem value="meaning">
                <AccordionTrigger>핵심 의미와 적용 범위</AccordionTrigger>
                <AccordionContent>
                  <p>{analysis.idea}</p>
                  {analysis.sourceNotes?.map((note, i) => <p key={i} className="notice">교육과정 적용 범위 · {note.scope_note}</p>)}
                  <p className="small">{analysis.limit}</p>
                </AccordionContent>
              </AccordionItem>
              <AccordionItem value="task">
                <AccordionTrigger>대표 과제와 진단 질문</AccordionTrigger>
                <AccordionContent>
                  <p className="source-label">자체 설계 과제</p>
                  <p>{analysis.task}</p>
                  <div className="action-links">
                    <a className="text-link" href={oldRoute("hierarchy", { mode: "tasks", target: code, scope })}>과제별 경로와 전체 조건</a>
                    <a className="text-link" href={oldRoute("standard", { code, scope, section: "diagnosis" })}>오류와 후속 질문 읽기</a>
                  </div>
                </AccordionContent>
              </AccordionItem>
              <AccordionItem value="evidence">
                <AccordionTrigger>관계와 근거</AccordionTrigger>
                <AccordionContent>
                  <p>{s.sourceReview}</p>
                  <div className="action-links">
                    <a className="text-link" href={oldRoute("connections", { code, scope })}>성취기준 간 관계 근거</a>
                    <a className="text-link" href={oldRoute("hierarchy", { mode: "goals", target: code, scope })}>목표별 출발 조건과 후속 활용</a>
                    <a className="text-link" href={oldRoute("standard", { code, scope, section: "references" })}>문헌과 검토 범위</a>
                  </div>
                </AccordionContent>
              </AccordionItem>
            </Accordion>
            <details className="reading-toc" open>
              <summary>전체 상세 분석 목차</summary>
              <ol>{analysis.sections.map((section) => <li key={section.id}>
                <a className="text-link" href={oldRoute("standard", { code, scope, section: section.id })}>{section.title}</a>
              </li>)}</ol>
            </details>
          </div>}
      </article>
      <aside className="reading-tools" aria-label="이 성취기준으로 할 수 있는 일">
        <Button asChild variant="outline"><a href={route("compare", { left: band, leftDomain: s.domain, leftCode: code })}>
          <GitCompareArrows aria-hidden="true" />다른 범위와 비교
        </a></Button>
        <Button asChild variant="outline"><a href={oldRoute("network", { node: code, scope })}>
          <Network aria-hidden="true" />연결망에서 보기
        </a></Button>
        <Button variant="outline" type="button" onClick={() => window.print()}><Printer aria-hidden="true" />인쇄</Button>
      </aside>
    </div>
  </div>;
}

function ComparisonSide({ side, standards, params, change, onOpen }) {
  const band = params.get(side) || "";
  const domain = params.get(side + "Domain") || "";
  const code = params.get(side + "Code") || "";
  const available = band ? selection(standards, "", band) : [];
  const domains = unique(available.map((s) => s.domain));
  const matches = selection(available, "", "", domain);
  const shown = code && matches.some((s) => s.code === code) ? matches.filter((s) => s.code === code) : matches;
  const levels = unique(standards.map((s) => s.level));
  return <section className="comparison-side">
    <div className="comparison-header">
      <h2>{side === "left" ? "첫 번째 범위" : "두 번째 범위"}</h2>
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
    </div>
    {band ? <>
      <p className="result-meta" role="status">{shown.length}개 성취기준</p>
      {shown.length ? <ul className="standard-list">
        {shown.map((standard) => <StandardRow key={standard.code} idPrefix={side + "-"}
          standard={standard} onOpen={onOpen} scope={scopeId(standard)} />)}
      </ul> : <p className="notice">이 범위에 해당하는 성취기준이 없습니다.</p>}
    </> : <p className="no-selection"><BookOpen size={19} aria-hidden="true" />비교할 학년군이나 과목을 선택하세요.</p>}
  </section>;
}

export function Compare({ catalog, params, go, onOpen }) {
  const change = (delta) => go(route("compare", { ...Object.fromEntries(params), ...delta }));
  return <div className="site-width compare-page">
    <header className="atlas-page-header">
      <h1 className="atlas-page-title" tabIndex={-1}>두 범위 비교</h1>
      <p className="atlas-page-description">학년군이나 과목을 두 개 골라 공식 성취기준을 나란히 읽어 보세요.</p>
      <Button variant="outline" type="button" onClick={() => go(route("compare", {
        left: "3~4학년군", leftDomain: "수와 연산", leftCode: "4수01-09",
        right: "5~6학년군", rightDomain: "수와 연산", rightCode: "6수01-10",
      }))}>예시로 분수 기준 비교</Button>
    </header>
    <div className="comparison">
      {["left", "right"].map((side) => <ComparisonSide key={side} side={side} standards={catalog.standards}
        params={params} change={change} onOpen={onOpen} />)}
    </div>
  </div>;
}
