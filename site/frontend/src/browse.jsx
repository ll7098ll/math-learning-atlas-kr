import React, { useEffect, useLayoutEffect, useRef, useState } from "react";
import { flushSync } from "react-dom";
import { ChevronDown, ChevronLeft, ChevronRight, ListFilter, Search, X } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { bandOf, categories, route, schools, search, selection, standardRoute, unique } from "./curriculum";
import { LoadState, Pdf, StandardRow, useContent } from "./shared";
import { ConnectionPreview } from "./connection-preview";
import "./browse-journey.css";

const pageSize = 24;
const allRanges = { scope: "", band: "", domain: "", category: "" };

function BrowseFilters({ standards, values, change }) {
  const { scope, band, domain, category } = values;
  const [expanded, setExpanded] = useState(false);
  const scoped = selection(standards, scope);
  const available = selection(scoped, "", "", "", category);
  const domains = unique(selection(available, "", band).map((s) => s.domain));
  const singleSchool = schools.some((entry) => entry.id === scope);
  const bandLabel = scope === "h" ? "과목" : singleSchool ? "학년군" : "학년군·과목";
  const groupOf = (standard) => scope === "h" ? standard.category : standard.level;
  const bandSelect = <label className="journey-select"><span id="journey-band-label">{bandLabel}</span>
    <select aria-labelledby="journey-band-label" value={band} onChange={(event) => change({ band: event.target.value, domain: "" })}>
      <option value="">모든 {bandLabel}</option>
      {unique(available.map(groupOf)).map((group) =>
        <optgroup key={group} label={group}>
          {unique(available.filter((s) => groupOf(s) === group).map(bandOf)).map((value) =>
            <option key={value}>{value}</option>)}
        </optgroup>
      )}
    </select>
  </label>;
  return <div className="journey-filters screen-only">
    <div className="journey-filter-line">
      <div className="journey-schools" role="group" aria-label="학교급 선택">
        <span aria-hidden="true">학교급</span>
        <div className="journey-school-options">
          {[{ id: "", title: "전체" }, ...schools].map((school) =>
            <button key={school.id} type="button" aria-pressed={scope === school.id}
              onClick={() => change({ ...allRanges, scope: school.id })}>{school.title}</button>
          )}
        </div>
      </div>
      {singleSchool && bandSelect}
      <button className="journey-filter-toggle" type="button" aria-expanded={expanded} aria-controls="journey-extra-filters"
        onClick={() => setExpanded(!expanded)}><ListFilter size={17} aria-hidden="true" />상세 조건
        <ChevronDown size={15} aria-hidden="true" />
      </button>
    </div>
    <div id="journey-extra-filters" className="journey-extra-filters" hidden={!expanded}>
      {!singleSchool && bandSelect}
      <label className="journey-select"><span id="journey-domain-label">내용 영역</span>
        <select aria-labelledby="journey-domain-label" value={domain} onChange={(event) => change({ domain: event.target.value })}>
          <option value="">모든 영역</option>
          {domains.map((value) => <option key={value}>{value}</option>)}
        </select>
      </label>
      <button className="journey-reset" type="button" onClick={() => change(allRanges)}>범위 초기화</button>
    </div>
  </div>;
}

function CurriculumStructure({ version, byCode, selected, query, fallback, onOpen }) {
  const request = useContent("curriculum-structure.json", version);
  useLayoutEffect(() => {
    const saved = history.state?.focusOnReturn;
    if (!request.data || !saved?.id?.startsWith("structure-")) return;
    const link = document.getElementById(saved.id);
    if (!link) return;
    link.closest(".structure-links").open = true;
    link.closest(".structure-category").open = true;
    link.focus({ preventScroll: true });
    window.scrollTo(0, saved.scroll);
  }, [request.data]);
  if (!request.data) return <LoadState request={request} label="공식 내용 체계를 불러오고 있습니다…" />;
  const codes = new Set(selected.map((s) => s.code));
  const terms = query.trim().toLocaleLowerCase("ko").split(/\s+/).filter(Boolean);
  const items = request.data.items.filter((item) => item.scopeCodes.some((code) => codes.has(code))
    && terms.every((term) => (item.text + " " + item.category + " " + item.domain).toLocaleLowerCase("ko").includes(term)));
  if (!items.length) return <div className="empty-state">
    <h3>이 범위에서 찾은 내용 체계 항목이 없습니다.</h3>
    <Button variant="outline" onClick={fallback}>{query ? "검색어 지우기" : "전체 범위 보기"}</Button>
  </div>;
  return <div className="structure">
    <p className="result-meta" role="status">공식 내용 체계 {items.length}개</p>
    {categories.map((category) => {
      const group = items.filter((item) => item.category === category);
      if (!group.length) return null;
      return <details className="structure-category" key={category} open={category === categories[0]}>
        <summary>{category}<span>{group.length}개</span></summary>
        <ul>{group.map((item) => {
          const scopes = unique(item.scopeCodes.map((code) => byCode.get(code)).map((s) =>
            s ? s.level === "고등학교" ? s.subject : s.level + " " + s.band : ""));
          return <li key={item.id}>
            <p className="row-location">{item.subject} · {item.domain}</p>
            <p className="official-text">{item.text}</p>
            <p className="small">공식 적용 범위　{scopes.filter(Boolean).join(" · ")}</p>
            <Pdf page={item.page}>교육과정 PDF {item.page}쪽</Pdf>
            {item.linkedCodes.length > 0 && <details className="structure-links">
              <summary>자체 대조로 연결한 성취기준 {item.linkedCodes.length}개</summary>
              <ul>{item.linkedCodes.map((code) => <li key={code}>
                <a id={`structure-${item.id}-${code}`} className="text-link" href={standardRoute(code)}
                  onClick={(event) => onOpen(event, code)}>{code} · {byCode.get(code).title}</a>
              </li>)}</ul>
            </details>}
          </li>;
        })}</ul>
      </details>;
    })}
  </div>;
}

export function Browse({ catalog, params, go, onOpen }) {
  const standards = catalog.standards;
  const rawScope = params.get("scope");
  const scope = ["e", "m", "h", "em", "mh"].includes(rawScope) ? rawScope : "";
  const band = params.get("band") || "";
  const domain = params.get("domain") || "";
  const category = params.get("category") || "";
  const q = params.get("q") || "";
  const tab = params.get("tab") === "structure" ? "structure" : "standards";
  const [draft, setDraft] = useState(q);
  const composing = useRef(false);
  const resultsTitle = useRef(null);
  useEffect(() => setDraft(q), [q]);
  const values = { scope, band, domain, category, q, tab: tab === "structure" ? tab : "" };
  const selected = selection(standards, scope, band, domain, category);
  const matches = search(selected, q);
  const pageCount = Math.max(1, Math.ceil(matches.length / pageSize));
  const focusIndex = matches.findIndex((s) => s.code === params.get("focus"));
  const page = Math.max(1, Math.min(pageCount, Number.parseInt(params.get("page"), 10)
    || (Math.floor(focusIndex / pageSize) + 1)));
  const shown = matches.slice((page - 1) * pageSize, page * pageSize);
  const home = !scope && !band && !domain && !category && !q && !params.has("page") && tab === "standards" && !params.has("focus");
  const school = schools.filter((entry) => scope.includes(entry.id)).map((entry) => entry.title).join(" · ");
  const activeFilters = [
    [school, "학교급", allRanges],
    [band, "학년군·과목", { band: "", domain: "", category: "" }],
    [domain, "내용 영역", { domain: "" }],
    [category, "과목 유형", { category: "" }],
    [q, "검색어", { q: "" }],
  ].filter(([value]) => value);
  const change = (delta) => go(route("catalog", { ...values, ...delta }));

  function showResults(delta) {
    flushSync(() => change(delta));
    resultsTitle.current?.focus();
  }

  function turnPage(nextPage) {
    change({ page: nextPage });
    resultsTitle.current?.focus({ preventScroll: true });
    resultsTitle.current?.scrollIntoView({ block: "start" });
  }

  const title = tab === "structure" ? "공식 내용 체계" : q ? `‘${q}’ 검색 결과` : "성취기준 목록";

  return <div className="browse-journey">
    <section className={home ? "journey-hero" : "journey-hero journey-compact"}>
      <div className="site-width journey-hero-inner">
        <div className="journey-intro">
          <p className="journey-edition">2022 개정 수학과 교육과정</p>
          <h1 tabIndex={-1}>수학 성취기준 탐색</h1>
          {home && <p className="journey-description">성취기준의 뜻과 이어지는 배움을 살펴보세요.</p>}
          <form className="search-form journey-search" role="search" onSubmit={(event) => {
            event.preventDefault();
            if (!composing.current) showResults({ q: draft.trim() });
          }}>
            <Search size={21} aria-hidden="true" />
            <Input type="search" value={draft} aria-label={tab === "structure" ? "공식 내용 체계 검색" : "성취기준 검색"}
              placeholder={tab === "structure" ? "낱말이나 영역 입력" : "개념·코드로 검색"}
              onCompositionStart={() => { composing.current = true; }}
              onCompositionEnd={(event) => { composing.current = false; setDraft(event.currentTarget.value); }}
              onChange={(event) => setDraft(event.target.value)} />
            <Button type="submit">검색</Button>
          </form>
          {home && <div className="journey-suggestions screen-only">
            <span>검색 예시</span>
            {["분수", "일차함수", "확률"].map((word) => <button type="button" key={word}
              onClick={() => showResults({ q: word })}>{word}</button>)}
          </div>}
        </div>
        {home && <div className="journey-preview-wrap screen-only"><ConnectionPreview onOpen={onOpen} catalog={catalog} /></div>}
      </div>
    </section>
    <div className="site-width journey-body">
      <BrowseFilters standards={standards} values={values} change={change} />
      <section className="results" aria-labelledby="browse-result-title">
        <header className="journey-results-header">
          <div className="journey-result-title">
            <h2 ref={resultsTitle} id="browse-result-title" tabIndex={-1}
              aria-describedby={tab === "standards" ? "browse-result-count" : undefined}>{title}</h2>
            {tab === "standards" && <p id="browse-result-count" className="journey-count" role="status">{matches.length}개
              <span className="sr-only"> 성취기준{pageCount > 1 && ` · ${(page - 1) * pageSize + 1}–${(page - 1) * pageSize + shown.length}번째 표시`}</span>
            </p>}
          </div>
          <nav className="journey-related-tools screen-only" aria-label="다른 교육과정 자료">
            <a href={route("catalog", { ...values, tab: tab === "standards" ? "structure" : "" })}>
              {tab === "standards" ? "공식 내용 체계" : "성취기준 목록"}
            </a>
            <a id="browse-compare"
              href={route("compare", { left: band, leftDomain: band ? domain : "" })} onClick={onOpen}>두 범위 비교</a>
          </nav>
        </header>
        {activeFilters.length > 0 && <ul className="active-filters journey-active-filters" aria-label="적용된 탐색 조건">
          {activeFilters.map(([value, label, delta]) => <li key={label}>
            <button type="button" aria-label={`${label} ‘${value}’ 해제`} onClick={() => showResults(delta)}>
              <span>{value}</span><X size={14} aria-hidden="true" />
            </button>
          </li>)}
        </ul>}
        {band.startsWith("기본수학") && <p className="notice">같은 번호의 공통수학을 대체하여 이수하는 과목입니다.</p>}
        {tab === "standards" ? <>
          {shown.length ? <ul className="standard-list journey-list">
            {shown.map((standard) => <StandardRow key={standard.code} standard={standard} onOpen={onOpen} scope={scope} />)}
          </ul> : <div className="empty-state">
            <h3>조건에 맞는 성취기준이 없습니다.</h3>
            <p>다른 개념이나 성취기준 코드로 검색해 보세요.</p>
            <div className="flex flex-wrap gap-2">
              {domain && <Button variant="outline" onClick={() => change({ domain: "" })}>영역 선택 해제</Button>}
              {(scope || band || domain || category) && <Button variant="outline" onClick={() => change(allRanges)}>전체 범위에서 검색</Button>}
              {q && <Button variant="outline" onClick={() => change({ q: "" })}>검색어 지우기</Button>}
            </div>
          </div>}
          {pageCount > 1 && <nav className="pagination" aria-label="목록 페이지">
            <Button variant="outline" disabled={page === 1} onClick={() => turnPage(page - 1)}><ChevronLeft />이전</Button>
            <span>{page} / {pageCount}쪽</span>
            <Button variant="outline" disabled={page === pageCount} onClick={() => turnPage(page + 1)}>다음<ChevronRight /></Button>
          </nav>}
        </> : <CurriculumStructure version={catalog.version} byCode={new Map(standards.map((s) => [s.code, s]))}
          selected={selected} query={q} onOpen={onOpen}
          fallback={() => showResults(q ? { q: "" } : allRanges)} />}
      </section>
    </div>
  </div>;
}
