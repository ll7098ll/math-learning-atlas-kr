import React, { useEffect, useLayoutEffect, useRef, useState } from "react";
import { ArrowDownUp, BookOpen, ChevronLeft, ChevronRight, ListFilter, Search, X } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Sheet, SheetClose, SheetContent, SheetDescription, SheetHeader, SheetTitle, SheetTrigger } from "@/components/ui/sheet";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { bandOf, categories, inScope, route, schools, search, selection, standardRoute, unique } from "./curriculum";
import { LoadState, Pdf, StandardRow, useContent } from "./shared";

const pageSize = 24;
const allRanges = { scope: "", band: "", domain: "", category: "" };

function Filters({ standards, values, change }) {
  const { scope, band, domain } = values;
  const scoped = selection(standards, scope);
  const bands = unique(scoped.map(bandOf));
  const domains = unique(selection(scoped, "", band).map((s) => s.domain));
  const high = scope === "h";
  return <div className="filters">
    <fieldset>
      <legend>학교급</legend>
      <div className="school-options">
        {[{ id: "", title: "초·중·고 전체" }, ...schools].map((school) =>
          <Button key={school.id} variant={scope === school.id ? "secondary" : "ghost"}
            className="school-option" aria-pressed={scope === school.id}
            onClick={() => change({ scope: school.id, band: "", domain: "", category: "" })}>
            {school.title}
          </Button>
        )}
      </div>
    </fieldset>
    <label>{high ? "과목" : "학년군 · 과목"}
      <select value={band} onChange={(event) => change({ band: event.target.value, domain: "", category: "" })}>
        <option value="">{high ? "모든 과목" : "모든 학년군·과목"}</option>
        {(high ? unique(scoped.map((s) => s.category)) : []).map((category) =>
          <optgroup key={category} label={category}>
            {unique(scoped.filter((s) => s.category === category).map(bandOf)).map((value) =>
              <option key={value}>{value}</option>)}
          </optgroup>
        )}
        {!high && bands.map((value) => <option key={value}>{value}</option>)}
      </select>
    </label>
    <label>내용 영역
      <select value={domain} onChange={(event) => change({ domain: event.target.value })}>
        <option value="">모든 영역</option>
        {domains.map((value) => <option key={value}>{value}</option>)}
      </select>
    </label>
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
  const home = !scope && !band && !domain && !category && !q && !params.has("page");
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
    change(delta);
    resultsTitle.current?.focus();
  }

  function turnPage(nextPage) {
    change({ page: nextPage });
    resultsTitle.current?.focus({ preventScroll: true });
    resultsTitle.current?.scrollIntoView({ block: "start" });
  }

  return <>
    <section className={home ? "hero" : "hero hero-condensed"}>
      <div className="site-width hero-inner">
        <p className="hero-meta">2022 개정 수학과 교육과정</p>
        <h1 tabIndex={-1}>수학 교육과정 탐색</h1>
        {home && <p className="hero-copy">학교급과 과목을 고르거나 성취기준 코드·개념으로 찾아보세요.</p>}
        <form className="search-form" role="search" onSubmit={(event) => {
          event.preventDefault();
          if (!composing.current) showResults({ q: draft.trim() });
        }}>
          <Search size={21} aria-hidden="true" />
          <Input type="search" value={draft} aria-label="성취기준 검색" placeholder="예: 분수, 변화율, 6수01-10"
            onCompositionStart={() => { composing.current = true; }}
            onCompositionEnd={(event) => { composing.current = false; setDraft(event.currentTarget.value); }}
            onChange={(event) => setDraft(event.target.value)} />
          <Button type="submit">검색</Button>
        </form>
      </div>
    </section>
    <div className={home ? "site-width explorer explorer-home" : "site-width explorer"}>
      {!home && <aside className="desktop-filters" aria-label="교육과정 필터">
        <h2><ListFilter size={17} aria-hidden="true" /> 탐색 범위</h2>
        <Filters standards={standards} values={values} change={change} />
        <Button variant="outline" className="mt-5 w-full" onClick={() => showResults(allRanges)}>범위 초기화</Button>
      </aside>}
      <section className="results">
        <div className="results-heading">
          <div>
            {!activeFilters.length && <p className="row-location">초·중·고 전체</p>}
            <h2 ref={resultsTitle} tabIndex={-1}>{q ? `‘${q}’ 검색 결과` : home ? "학교급으로 찾아보기" : band || "선택 범위의 교육과정"}</h2>
          </div>
          <Sheet>
            <SheetTrigger asChild><Button variant="outline" className="mobile-filters"><ListFilter />범위 변경</Button></SheetTrigger>
            <SheetContent side="right" className="filter-sheet">
              <SheetHeader>
                <SheetTitle>탐색 범위</SheetTitle>
                <SheetDescription>학교급과 학년군·과목, 영역을 고릅니다.</SheetDescription>
              </SheetHeader>
              <div className="sheet-fields"><Filters standards={standards} values={values} change={change} />
                <div className="mt-6 flex flex-wrap gap-3">
                  <Button variant="outline" onClick={() => change(allRanges)}>범위 초기화</Button>
                  <SheetClose asChild><Button>결과 보기</Button></SheetClose>
                </div>
              </div>
            </SheetContent>
          </Sheet>
        </div>
        {activeFilters.length > 0 && <ul className="active-filters" aria-label="적용된 탐색 조건">
          {activeFilters.map(([value, label, delta]) => <li key={label}>
            <button type="button" aria-label={`${label} ‘${value}’ 해제`} onClick={() => showResults(delta)}>
              <span>{value}</span><X size={14} aria-hidden="true" />
            </button>
          </li>)}
        </ul>}
        {band.startsWith("기본수학") && <p className="notice">같은 번호의 공통수학을 대체하여 이수하는 과목입니다.</p>}
        {home && <div className="school-cards">
          {schools.map((entry) => <a key={entry.id} className="school-card"
            href={route("catalog", { scope: entry.id, tab: values.tab })}>
            <BookOpen size={21} aria-hidden="true" />
            <h3>{entry.title}</h3><p>{entry.description}</p>
            <span>{standards.filter((s) => inScope(s, entry.id)).length}개 성취기준 <ChevronRight size={16} aria-hidden="true" /></span>
          </a>)}
        </div>}
        <Tabs value={tab} onValueChange={(value) => change({ tab: value === "standards" ? "" : value })}>
          <div className="tabs-row">
            <TabsList aria-label="교육과정 자료" variant="line">
              <TabsTrigger value="standards">성취기준</TabsTrigger>
              <TabsTrigger value="structure">내용 체계</TabsTrigger>
            </TabsList>
            <a id="browse-compare" className="text-link compare-link"
              href={route("compare", { left: band, leftDomain: band ? domain : "" })} onClick={onOpen}>
              <ArrowDownUp size={15} aria-hidden="true" />두 범위 비교
            </a>
          </div>
          <TabsContent value="standards">
            <p className="result-meta" role="status">{matches.length}개 성취기준
              {pageCount > 1 && ` · ${(page - 1) * pageSize + 1}–${(page - 1) * pageSize + shown.length}번째 표시`}
            </p>
            {shown.length ? <ul className="standard-list">
              {shown.map((standard) => <StandardRow key={standard.code} standard={standard} onOpen={onOpen} scope={scope} />)}
            </ul> : <div className="empty-state">
              <h3>조건에 맞는 성취기준이 없습니다.</h3>
              <div className="flex flex-wrap gap-2">
                {domain && <Button variant="outline" onClick={() => change({ domain: "" })}>영역 선택 해제</Button>}
                <Button variant="outline" onClick={() => go(route("catalog", { q }))}>전체 범위에서 검색</Button>
                {q && <Button variant="ghost" onClick={() => change({ q: "" })}>검색어 지우기</Button>}
              </div>
            </div>}
            {pageCount > 1 && <nav className="pagination" aria-label="목록 페이지">
              <Button variant="outline" disabled={page === 1} onClick={() => turnPage(page - 1)}><ChevronLeft />이전</Button>
              <span>{page} / {pageCount}쪽</span>
              <Button variant="outline" disabled={page === pageCount} onClick={() => turnPage(page + 1)}>다음<ChevronRight /></Button>
            </nav>}
          </TabsContent>
          <TabsContent value="structure">
            <CurriculumStructure version={catalog.version} byCode={new Map(standards.map((s) => [s.code, s]))}
              selected={selected} query={q} onOpen={onOpen}
              fallback={() => showResults(q ? { q: "" } : allRanges)} />
          </TabsContent>
        </Tabs>
      </section>
    </div>
  </>;
}
