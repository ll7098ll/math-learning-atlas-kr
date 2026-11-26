import React, { useEffect, useLayoutEffect, useMemo, useRef, useState } from "react";
import { flushSync } from "react-dom";
import { ArrowRight, BookOpenText, ChevronDown, ChevronLeft, ChevronRight, Circle, GalleryHorizontalEnd, List, ListFilter, Sigma, Triangle, Search, Waypoints, X } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { bandOf, catalogPageRows, categories, groupStandards, oldRoute, overviewRoute, route, scopeId, schools, search, selection, standardRoute, unique } from "./curriculum";
import { LoadState, Pdf, StandardRow, useContent } from "./shared";
import { ConnectionPreview } from "./connection-preview";
import { SectionContents } from "./section-contents";
import "./browse-journey.css";

const allRanges = { scope: "", band: "", domain: "", category: "" };
const schoolIcons = { e: Circle, m: Triangle, h: Sigma };

function EntryPoints({ standards, onOpen }) {
  return <nav className="atlas-school-grid" aria-label="학교급 선택">
      {schools.map((school) => {
        const rows = selection(standards, school.id);
        const bands = unique(rows.map(bandOf));
        const range = school.id === "h" ? `${bands.length}개 과목` : bands.join(" · ").replaceAll("학년군 · ", " · ");
        const Icon = schoolIcons[school.id];
        return <a id={"school-" + school.id} className="atlas-school-entry" key={school.id}
          href={overviewRoute(standards, school.id)} onClick={onOpen}>
          <div className="atlas-entry-symbol" aria-hidden="true"><Icon size={23} strokeWidth={1.6} /></div>
          <div className="atlas-school-title"><h2>{school.title}</h2><ArrowRight size={19} aria-hidden="true" /></div>
          <p><span>{range}</span><span className="atlas-count-divider" aria-hidden="true">/</span><span>성취기준 {rows.length}개</span></p>
        </a>;
      })}
  </nav>;
}

function officialScopes(item, byCode) {
  return unique(item.scopeCodes.map((code) => byCode.get(code)).filter(Boolean).map((s) =>
    s.level === "고등학교" ? s.subject : `${s.level} ${s.band}`));
}

function useRestoreLoadedLink(loaded, prefix) {
  useLayoutEffect(() => {
    const saved = history.state?.focusOnReturn;
    if (!loaded || !saved?.id?.startsWith(prefix)) return;
    const link = document.getElementById(saved.id);
    if (!link) return;
    for (let group = link.closest("details"); group; group = group.parentElement?.closest("details")) group.open = true;
    link.focus({ preventScroll: true });
    window.scrollTo(0, saved.scroll);
  }, [loaded, prefix]);
}

function IdeaStandards({ item, selectedCodes, byCode, scope, onOpen }) {
  const linked = item.linkedCodes.map((code) => byCode.get(code)).filter(Boolean);
  const selected = linked.filter((s) => selectedCodes.has(s.code));
  const others = linked.filter((s) => !selectedCodes.has(s.code));
  const rangeWord = scope === "h" ? "과목" : "학년군";
  const links = (rows) => <div className="atlas-idea-links">{rows.map((s) =>
    <a id={`idea-${item.id}-${s.code}`} key={s.code} href={standardRoute(s.code, scopeId(s))}
      onClick={(event) => onOpen(event, s.code)}><span>{s.code}</span>{s.title}</a>)}</div>;
  return <div className="atlas-idea-mapping">
    <p>이 {rangeWord}의 관련 성취기준 {selected.length}개 · 이 사이트에서 찾아 연결했습니다.</p>
    {selected.length > 0 && links(selected)}
    {others.length > 0 && <details className="atlas-idea-others"><summary>다른 {rangeWord}의 관련 성취기준 {others.length}개</summary>{links(others)}</details>}
  </div>;
}

function ScopeIdeaGroup({ title, ideas, selectedCodes, byCode, scope, onOpen }) {
  return <details className="atlas-idea-group">
    <summary>{title}<span>{ideas.length}개</span></summary>
    <ul>{ideas.map((item) => {
      const scopes = officialScopes(item, byCode);
      return <li key={item.id}><p>{item.text}</p>
        <p className="small">{scopes.length > 1 ? "여러 학년군 공통" : "교육과정에 제시된 학년군·과목"} · {scopes.join(" · ")}</p>
        <Pdf page={item.page}>교육과정 PDF {item.page}쪽</Pdf>
        <IdeaStandards item={item} selectedCodes={selectedCodes} byCode={byCode} scope={scope} onOpen={onOpen} />
      </li>;
    })}</ul>
  </details>;
}

function BandDomains({ version, standards, rows, scope, band, onOpen }) {
  const request = useContent("curriculum-structure.json", version);
  useRestoreLoadedLink(request.data, "idea-");
  const areas = useMemo(() => unique(rows.map((s) => s.domain)).map((name, index) => ["band-area-" + index, name]), [rows]);
  const areaNames = new Set(areas.map(([, name]) => name));
  const selectedCodes = new Set(rows.map((s) => s.code));
  const ideas = request.data?.items.filter((item) => item.category === "핵심 아이디어"
    && item.scopeCodes.some((code) => selectedCodes.has(code))) ?? [];
  const additional = ideas.filter((item) => !areaNames.has(item.domain));
  const byCode = new Map(standards.map((s) => [s.code, s]));
  const ideaProps = { selectedCodes, byCode, scope, onOpen };
  return <>
    <div className="atlas-band-outline">
      {areas.length > 0 && <SectionContents items={areas} label="내용 영역 목차" linksId="band-area-links" />}
      {!request.data && <LoadState request={request} label="공식 핵심 아이디어를 불러오고 있습니다…" />}
      <div className="atlas-band-domains">{areas.map(([id, name]) => {
        const group = ideas.filter((item) => item.domain === name);
        const count = rows.filter((standard) => standard.domain === name).length;
        return <section className="atlas-band-domain" id={id} key={name} aria-labelledby={id + "-heading"}>
          <header className="journey-section-heading">
            <h3 id={id + "-heading"} tabIndex={-1}>{name}</h3>
            <a id={`overview-${scope}-${band}-${name}`} href={route("catalog", { scope, band, domain: name })} onClick={onOpen}
              aria-label={`${name} 성취기준 ${count}개 보기`}>성취기준 {count}개 보기<ArrowRight size={17} aria-hidden="true" /></a>
          </header>
          {group.length > 0 && <ScopeIdeaGroup title="공식 핵심 아이디어" ideas={group} {...ideaProps} />}
        </section>;
      })}</div>
    </div>
    {additional.length > 0 && <section className="atlas-scope-ideas" aria-labelledby="ideas-heading">
      <header className="journey-section-heading"><h2 id="ideas-heading">공식 핵심 아이디어</h2></header>
      {unique(additional.map((item) => item.domain || item.subject)).map((name) => {
        const group = additional.filter((item) => (item.domain || item.subject) === name);
        const title = group[0].domain ? name : name + " 과목 공통";
        return <ScopeIdeaGroup key={name} title={title} ideas={group} {...ideaProps} />;
      })}
    </section>}
    {request.data && !ideas.length && <p className="small">선택한 학년군·과목에 표시할 핵심 아이디어가 없습니다.</p>}
  </>;
}

function SearchConcepts({ version, query, selected, scope }) {
  const request = useContent("concept-pathways-index.json", version);
  useRestoreLoadedLink(request.data, "found-concept-");
  if (!request.data) return null;
  const term = query.normalize("NFKC").trim().replace(/\s+/g, "");
  const codes = new Set(selected.map((s) => s.code));
  const matching = request.data.groups.filter((group) => {
    const title = group.title.normalize("NFKC").replace(/\s+/g, "");
    const named = term.length > 1 ? title.includes(term) : title.split("·").includes(term);
    return named && group.member_codes.some((code) => codes.has(code));
  });
  if (!matching.length) return null;
  return <nav className="atlas-search-concepts" aria-label="검색어와 관련된 수학 개념">
    <span>관련 개념으로 더 보기</span>
    {matching.map((group) => <a key={group.id} id={"found-concept-" + group.id}
      href={oldRoute("hierarchy", { concept: group.id, scope, target: group.member_codes.find((code) => codes.has(code)) })}
    >{group.title}<ChevronRight size={14} aria-hidden="true" /></a>)}
  </nav>;
}

function ScopeOverview({ standards, version, scope, band, onOpen }) {
  const rows = selection(standards, scope, band);
  const heading = band ? "내용 영역" : scope === "h" ? "과목 선택" : "학년군 선택";
  const groups = unique(rows.map((s) => scope === "h" ? s.category : ""));
  const pairedName = band.replace(/^(기본|공통)수학([12])$/, (_, type, n) => (type === "공통" ? "기본수학" : "공통수학") + n);
  const counterpart = pairedName !== band && standards.some((s) => s.subject === pairedName) ? pairedName : "";
  return <section aria-labelledby="scope-heading">
    <header className="journey-section-heading">
      <h2 id="scope-heading">{heading}</h2>
      <div className="atlas-range-actions"><a id="scope-all" href={route("catalog", { scope, band })} onClick={onOpen}>성취기준 {rows.length}개<ArrowRight size={16} aria-hidden="true" /></a>
        {band && <>
          <a id="scope-structure" href={route("catalog", { scope, band, tab: "structure" })} onClick={onOpen}>공식 내용 체계<ArrowRight size={16} aria-hidden="true" /></a>
          <a id="scope-compare" href={route("compare", { left: band, right: counterpart })} onClick={onOpen}><GalleryHorizontalEnd size={16} aria-hidden="true" />{counterpart ? band + " · " + counterpart + " 비교" : "다른 학년군·과목과 비교"}</a>
        </>}
      </div>
    </header>
    {band ? <BandDomains key={scope + band} rows={rows} standards={standards} version={version} scope={scope} band={band} onOpen={onOpen} />
      : groups.map((group) => {
      const items = group ? rows.filter((s) => s.category === group) : rows;
      return <div className="atlas-overview-group" key={group}>
        {group && <h3>{group}</h3>}
        {group === "공통" && <p className="atlas-subject-note">기본수학1·2는 각각 공통수학1·2를 대체하여 이수할 수 있습니다.</p>}
        <div className="atlas-overview-grid">{unique(items.map(bandOf)).map((name) => {
          const count = items.filter((s) => bandOf(s) === name).length;
          const target = { scope, band: name, stage: "overview" };
          return <a id={`overview-${scope}-${band}-${name}`} key={name} href={route("catalog", target)} onClick={onOpen}>
            <strong>{name}</strong><span>성취기준 {count}개</span>
            <ArrowRight size={17} aria-hidden="true" />
          </a>;
        })}</div>
      </div>;
    })}
    {band.startsWith("기본수학") && counterpart && <p className="atlas-subject-note">같은 번호의 공통수학을 대체하여 이수할 수 있는 과목입니다.</p>}
  </section>;
}

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
        onClick={() => setExpanded(!expanded)}><ListFilter size={17} aria-hidden="true" />학년군·과목·영역 고르기
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
      <button className="journey-reset" type="button" onClick={() => change(allRanges)}>선택 지우기</button>
    </div>
  </div>;
}

function CurriculumStructure({ version, byCode, selected, query, fallback, onOpen }) {
  const request = useContent("curriculum-structure.json", version);
  useRestoreLoadedLink(request.data, "structure-");
  if (!request.data) return <LoadState request={request} label="공식 내용 체계를 불러오고 있습니다…" />;
  const codes = new Set(selected.map((s) => s.code));
  const terms = query.trim().toLocaleLowerCase("ko").split(/\s+/).filter(Boolean);
  const items = request.data.items.filter((item) => item.scopeCodes.some((code) => codes.has(code))
    && terms.every((term) => (item.text + " " + item.category + " " + item.domain).toLocaleLowerCase("ko").includes(term)));
  if (!items.length) return <div className="empty-state">
    <h3>선택한 조건에 맞는 내용 체계 항목이 없습니다.</h3>
    <Button variant="outline" onClick={fallback}>{query ? "검색어 지우기" : "모든 학년군·과목 보기"}</Button>
  </div>;
  return <div className="structure">
    <p className="result-meta" role="status">공식 내용 체계 {items.length}개</p>
    {categories.map((category) => {
      const group = items.filter((item) => item.category === category);
      if (!group.length) return null;
      return <details className="structure-category" key={category}>
        <summary>{category}<span>{group.length}개</span></summary>
        <ul>{group.map((item) => {
          const scopes = officialScopes(item, byCode);
          return <li key={item.id}>
            <p className="row-location">{[item.subject, item.domain].filter(Boolean).join(" · ")}</p>
            <p className="official-text">{item.text}</p>
            <p className="small">교육과정에 제시된 학년군·과목　{scopes.join(" · ")}</p>
            <Pdf page={item.page}>교육과정 PDF {item.page}쪽</Pdf>
            {item.linkedCodes.length > 0 && <details className="structure-links">
              <summary>이 사이트에서 연결한 성취기준 {item.linkedCodes.length}개</summary>
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

function ExpandedStandards({ standards, onOpen, scope, compact }) {
  const groups = groupStandards(standards);
  const closed = new Set(history.state?.closedCatalogGroups);
  function rememberGroup(event) {
    const group = event.currentTarget;
    const key = group.dataset.catalogGroup;
    const saved = new Set(history.state?.closedCatalogGroups);
    if (!group.isConnected || saved.has(key) === !group.open) return;
    if (group.open) saved.delete(key);
    else saved.add(key);
    history.replaceState({ ...history.state, closedCatalogGroups: [...saved] }, "");
  }
  return <div className="journey-expanded-list">{groups.map(({ level, band, domains, count }) => {
    const key = level + "/" + band;
    return <details className="journey-band-rows" key={key} data-catalog-group={key} open={!closed.has(key)} onToggle={rememberGroup}>
      <summary>{level} · {band}<span>{count}개</span></summary>
      {domains.map(({ name, rows }) => <section key={name}>
        <h3>{name}</h3>
        <ul className="standard-list journey-list">
          {rows.map((standard) => <StandardRow key={standard.code} standard={standard} onOpen={onOpen} scope={scope} compact={compact} />)}
        </ul>
      </section>)}
    </details>;
  })}</div>;
}

export function Browse({ catalog, params, go, onOpen, returnTo }) {
  const standards = catalog.standards;
  const rawScope = params.get("scope");
  const scope = ["e", "m", "h", "em", "mh"].includes(rawScope) ? rawScope : "";
  const band = params.get("band") || "";
  const domain = params.get("domain") || "";
  const category = params.get("category") || "";
  const q = params.get("q") || "";
  const compact = params.get("display") === "compact";
  const tab = params.get("tab") === "structure" ? "structure" : "standards";
  const [draft, setDraft] = useState(q);
  const composing = useRef(false);
  const resultsTitle = useRef(null);
  const selected = selection(standards, scope, band, domain, category);
  const matches = search(selected, q);
  const { expanded, shown, pageCount, page, start } = catalogPageRows(matches, params);
  const values = { scope, band, domain, category, q, display: compact ? "compact" : "", expand: expanded ? "all" : "", tab: tab === "structure" ? tab : "" };
  const exploreOrigin = history.state?.exploreOrigin;
  const overview = params.get("stage") === "overview" && schools.some((entry) => entry.id === scope)
    && !domain && !category && !q && !expanded && tab === "standards" && !params.has("focus") && !params.has("page")
    && (!band || selected.length > 0);
  const home = !scope && !band && !domain && !category && !q && !params.has("page") && !params.has("list")
    && !expanded && tab === "standards" && !params.has("focus");
  const school = schools.filter((entry) => scope.includes(entry.id)).map((entry) => entry.title).join(" · ");
  const screen = home ? "home" : overview ? `overview-${scope}-${band}` : "results-" + tab;
  useEffect(() => setDraft((home || overview) ? history.state?.searchDraft ?? q : q), [q, screen]);
  const previousScreen = useRef(screen);
  const headingRef = useRef(null);
  useLayoutEffect(() => {
    const switched = previousScreen.current !== screen;
    previousScreen.current = screen;
    if (!switched || history.state?.focusOnReturn || params.has("focus")) return;
    headingRef.current?.focus({ preventScroll: true });
    window.scrollTo(0, 0);
  }, [screen, params]);
  const activeFilters = [
    [school, "학교급", allRanges],
    [band, "학년군·과목", { band: "", domain: "", category: "" }],
    [domain, "내용 영역", { domain: "" }],
    [category, "과목 유형", { category: "" }],
    [q, "검색어", { q: "" }],
  ].filter(([value]) => value);
  const change = (delta) => {
    const target = { ...values, ...delta };
    if (!Object.values(target).some(Boolean)) target.list = 1;
    const next = route("catalog", target);
    if (next === location.hash) return;
    const trigger = document.activeElement;
    if (trigger?.id && trigger.closest(".browse-journey")) {
      history.replaceState({ ...history.state, focusOnReturn: { id: trigger.id, scroll: window.scrollY },
        searchDraft: home || overview ? draft : undefined }, "");
    }
    go(next);
  };

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
  const readingTitle = overview ? [school, band].filter(Boolean).join(" ") : domain || band || school || title;
  const heading = home ? "어느 학교급의 수학을 보시나요?" : readingTitle;
  const schoolOverview = schools.some((entry) => entry.id === scope) && overviewRoute(standards, scope);
  const bandOverview = schoolOverview && band && overviewRoute(standards, scope, band);

  return <div className="browse-journey">
    <section className={home ? "journey-hero journey-home" : "journey-hero journey-compact"}>
      <div className="site-width journey-hero-inner">
        <div className="journey-intro">
          {home ? <p className="journey-edition"><span aria-hidden="true" />2022 개정 수학과 교육과정</p>
            : <nav className="journey-trail" aria-label="탐색 위치">
              {exploreOrigin && <><a id="trail-origin" href={exploreOrigin.href} onClick={(event) => returnTo(event, exploreOrigin.href)}>
                <ChevronLeft size={14} aria-hidden="true" />{exploreOrigin.label || "읽던 화면으로"}</a><span aria-hidden="true">·</span></>}
              <a id="trail-home" href={route("catalog")} onClick={onOpen}>탐색 홈</a>
              {schoolOverview && (!overview || (bandOverview && bandOverview !== schoolOverview)) && <><ChevronRight size={14} aria-hidden="true" /><a id="trail-school"
                href={schoolOverview} onClick={onOpen}>{school}</a></>}
              {bandOverview && bandOverview !== schoolOverview && !overview && <><ChevronRight size={14} aria-hidden="true" /><a id="trail-band"
                href={bandOverview} onClick={onOpen}>{band}</a></>}
            </nav>}
          {(home || overview || heading !== title) && <h1 ref={headingRef} tabIndex={-1}>{heading}</h1>}
          {home && <><EntryPoints standards={standards} onOpen={onOpen} />
            <label className="journey-home-search-label" htmlFor="catalog-search-input">개념 또는 성취기준 코드 검색</label></>}
          {overview && <p className="journey-description">{band ? "수업할 영역을 고르면 해당 성취기준을 볼 수 있습니다." :
            scope === "h" ? "과목을 고르면 영역별 성취기준을 볼 수 있습니다." : "학년군을 고르면 영역별 성취기준을 볼 수 있습니다."}</p>}
          <form className="search-form journey-search" role="search" onSubmit={(event) => {
            event.preventDefault();
            if (!composing.current) showResults({ q: draft.trim() });
          }}>
            <Search size={21} aria-hidden="true" />
            <Input type="search" id="catalog-search-input" value={draft} aria-label={tab === "structure" ? "공식 내용 체계 검색" : "성취기준 검색"}
              placeholder={tab === "structure" ? "낱말이나 영역 검색" : scope || band ? "선택한 학년군·과목에서 검색" : "예: 분수, 4수01-12"}
              onCompositionStart={() => { composing.current = true; }}
              onCompositionEnd={(event) => { composing.current = false; setDraft(event.currentTarget.value); }}
              onChange={(event) => setDraft(event.target.value)} />
            <Button id="catalog-search-submit" type="submit">검색</Button>
          </form>
          {home && <div className="journey-suggestions screen-only">
            <span>검색 예시</span>
            {["분수", "일차함수", "확률"].map((word) => <button type="button" key={word} id={"suggest-" + word}
              onClick={() => showResults({ q: word })}>{word}</button>)}
          </div>}
        </div>
        {home && <div className="journey-preview-wrap screen-only"><ConnectionPreview /></div>}
      </div>
    </section>
    <div className="site-width journey-body">
      {home ? <nav className="atlas-home-tools" aria-label="다른 탐색 방법">
        <a id="home-all" href={route("catalog", { list: 1 })} onClick={onOpen}><List size={19} aria-hidden="true" />전체 성취기준 {standards.length}개 보기</a>
        <a id="home-concepts" href={oldRoute("hierarchy")}><Waypoints size={19} aria-hidden="true" />개념으로 둘러보기</a>
        <a id="home-structure" href={route("catalog", { tab: "structure" })} onClick={onOpen}><BookOpenText size={19} aria-hidden="true" />공식 내용 체계 보기</a>
        <a id="home-compare" href={route("compare")} onClick={onOpen}><GalleryHorizontalEnd size={19} aria-hidden="true" />두 학년군·과목 비교</a>
      </nav>
        : overview ? <ScopeOverview standards={standards} version={catalog.version} scope={scope} band={band} onOpen={onOpen} />
        : <>
      <BrowseFilters standards={standards} values={values} change={change} />
      <section className="results" aria-labelledby="browse-result-title">
        <header className="journey-results-header">
          <div className="journey-result-title">
            {heading === title
              ? <h1 ref={(element) => { headingRef.current = element; resultsTitle.current = element; }} id="browse-result-title" tabIndex={-1}
                  aria-describedby={tab === "standards" ? "browse-result-count" : undefined}>{title}</h1>
              : <h2 ref={resultsTitle} id="browse-result-title" tabIndex={-1}
                  aria-describedby={tab === "standards" ? "browse-result-count" : undefined}>{title}</h2>}
            {tab === "standards" && <p id="browse-result-count" className="journey-count" role="status">{matches.length}개
              <span className="sr-only"> 성취기준{pageCount > 1 && ` · ${start + 1}–${start + shown.length}번째 표시`}</span>
            </p>}
          </div>
          <nav className="journey-related-tools screen-only" aria-label="다른 교육과정 자료">
            {tab === "standards" && <a id="browse-display" href={route("catalog", {
              ...values, list: 1, page: page > 1 ? page : "", display: compact ? "" : "compact",
            })} onClick={onOpen}>{compact ? "원문 함께 보기" : "간단히 보기"}</a>}
            {tab === "standards" && (expanded || matches.length > 0) && <a id="browse-expand" href={route("catalog", {
              ...values, list: 1, expand: expanded ? "" : "all", display: "",
            })} onClick={onOpen}>{expanded ? "페이지로 나눠 보기" : "전체 원문 펼쳐 보기"}</a>}
            <a id="browse-tab" href={route("catalog", { ...values, tab: tab === "standards" ? "structure" : "", list: tab === "structure" ? 1 : "" })} onClick={onOpen}>
              {tab === "standards" ? "공식 내용 체계" : "성취기준 목록"}
            </a>
            <a id="browse-compare"
              href={route("compare", { left: band, leftDomain: band ? domain : "" })} onClick={onOpen}>학년군·과목 비교</a>
          </nav>
        </header>
        {activeFilters.length > 0 && <ul className="active-filters journey-active-filters" aria-label="현재 선택">
          {activeFilters.map(([value, label, delta]) => <li key={label}>
            <button type="button" aria-label={`${label} ‘${value}’ 해제`} onClick={() => showResults(delta)}>
              <span>{value}</span><X size={14} aria-hidden="true" />
            </button>
          </li>)}
        </ul>}
        {band.startsWith("기본수학") && <p className="notice">같은 번호의 공통수학을 대체하여 이수하는 과목입니다.</p>}
        {q.trim() && tab === "standards" && <SearchConcepts version={catalog.version} query={q} selected={selected} scope={scope} />}
        {tab === "standards" ? <>
          {expanded && shown.length ? <ExpandedStandards standards={shown} onOpen={onOpen} scope={scope} compact={compact} />
          : shown.length ? <ul className="standard-list journey-list">
            {shown.map((standard) => <StandardRow key={standard.code} standard={standard} onOpen={onOpen} scope={scope} compact={compact} />)}
          </ul> : <div className="empty-state">
            <h3>조건에 맞는 성취기준이 없습니다.</h3>
            <p>다른 개념이나 성취기준 코드로 검색해 보세요.</p>
            <div className="flex flex-wrap gap-2">
              {domain && <Button variant="outline" onClick={() => change({ domain: "" })}>영역 선택 해제</Button>}
              {(scope || band || domain || category) && <Button variant="outline" onClick={() => change(allRanges)}>모든 학년군·과목에서 검색</Button>}
              {q && <Button variant="outline" onClick={() => change({ q: "" })}>검색어 지우기</Button>}
            </div>
          </div>}
          {pageCount > 1 && <nav className="pagination" aria-label="목록 페이지">
            <Button id="browse-previous-page" variant="outline" disabled={page === 1} onClick={() => turnPage(page - 1)}><ChevronLeft />이전</Button>
            <span>{page} / {pageCount}쪽</span>
            <Button id="browse-next-page" variant="outline" disabled={page === pageCount} onClick={() => turnPage(page + 1)}>다음<ChevronRight /></Button>
          </nav>}
        </> : <CurriculumStructure version={catalog.version} byCode={new Map(standards.map((s) => [s.code, s]))}
          selected={selected} query={q} onOpen={onOpen}
          fallback={() => showResults(q ? { q: "" } : allRanges)} />}
      </section></>}
    </div>
  </div>;
}
