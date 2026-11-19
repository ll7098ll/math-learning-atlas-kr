import React, { useEffect, useLayoutEffect, useRef, useState } from "react";
import { createRoot } from "react-dom/client";
import { BookOpen } from "lucide-react";
import { Browse } from "./browse";
import { Compare, Detail } from "./reading";
import { LoadState, Pdf, useContent } from "./shared";
import { oldRoute, paramsFrom, route } from "./curriculum";
import "./theme.css";
import "../compat/atlas-print.css";

function App() {
  const [hash, setHash] = useState(location.hash);
  const params = paramsFrom(hash);
  const view = params.get("view");
  const code = params.get("code");
  const request = useContent("catalog.json");
  const catalog = request.data;
  const previous = useRef({});

  useEffect(() => {
    const update = () => setHash(location.hash);
    history.scrollRestoration = "manual";
    window.addEventListener("hashchange", update);
    return () => window.removeEventListener("hashchange", update);
  }, []);

  function go(target, state = {}) {
    if (location.hash === target) return;
    history.pushState(state, "", target);
    setHash(target);
  }

  function openStandard(event, selectedCode) {
    if (event.button !== 0 || event.ctrlKey || event.metaKey || event.altKey || event.shiftKey) return;
    event.preventDefault();
    const restore = { row: selectedCode, id: event.currentTarget.id, scroll: window.scrollY };
    history.replaceState({ ...history.state, restore }, "");
    go(event.currentTarget.getAttribute("href"), {
      returnTo: location.hash || route("catalog"),
      restore,
    });
  }

  function returnTo(event, target) {
    if (event.button !== 0 || event.ctrlKey || event.metaKey || event.altKey || event.shiftKey) return;
    event.preventDefault();
    go(target, { restore: history.state?.restore });
  }

  useLayoutEffect(() => {
    if (!catalog) return;
    const prior = previous.current;
    const transition = prior.view && (prior.view !== view || (view === "standard" && prior.code !== code));
    previous.current = { view, code };
    const saved = history.state?.restore;
    if (view === "catalog" || view === "compare") {
      const row = saved?.row || params.get("focus");
      const target = row && document.getElementById(saved?.id || "std-" + row);
      if (target) {
        target.focus({ preventScroll: true });
        if (saved) window.scrollTo(0, saved.scroll);
        else target.scrollIntoView({ block: "center" });
        return;
      }
      if (saved) window.scrollTo(0, saved.scroll);
    }
    if (transition) {
      window.scrollTo(0, 0);
      document.querySelector("#main h1")?.focus({ preventScroll: true });
    }
  }, [hash, view, code, catalog]);

  useEffect(() => {
    const title = view === "standard" ? catalog?.standards.find((s) => s.code === code)?.title
      : view === "compare" ? "두 범위 비교" : "교육과정 탐색";
    if (title) document.title = title + " · 수학의 연결 지도";
  }, [view, code, catalog]);

  const menu = [
    ["catalog", "교육과정 탐색", route("catalog")],
    ["compare", "비교", route("compare")],
    ["hierarchy", "연결 지도", oldRoute("hierarchy")],
    ["about", "자료 안내", oldRoute("about")],
  ];

  return <>
    <a className="skip-link" href="#main" onClick={(event) => {
      event.preventDefault();
      document.getElementById("main").focus();
    }}>본문으로 이동</a>
    <header className="site-header">
      <div className="site-width header-inner">
        <a className="brand" href={route("catalog")}><span className="brand-mark"><BookOpen size={21} aria-hidden="true" /></span>수학의 연결 지도</a>
        <nav aria-label="주요 탐색">{menu.map(([id, label, href]) =>
          <a key={id} href={href} aria-current={(view === id || id === "catalog" && view === "standard") ? "page" : undefined}>
            {label}
          </a>)}</nav>
        <span className="header-source"><Pdf>교육과정 원문 PDF</Pdf></span>
      </div>
    </header>

    <main id="main" tabIndex={-1}>
      {!catalog ? <div className="site-width loading-wrap"><LoadState request={request} label="교육과정 목록을 불러오고 있습니다…" /></div>
        : view === "standard" ? <Detail catalog={catalog} params={params} returnTo={returnTo} />
        : view === "compare" ? <Compare catalog={catalog} params={params} go={go} onOpen={openStandard} />
        : <Browse catalog={catalog} params={params} go={go} onOpen={openStandard} />}
    </main>

    <footer className="site-footer">
      <div className="site-width footer-inner">
        <div><strong>수학의 연결 지도</strong><p>교육부 고시 제2022-33호 · 별책 8 수학과 교육과정</p></div>
        <a className="text-link" href={oldRoute("about")}>자료의 출처와 분석 기준</a>
      </div>
    </footer>
  </>;
}

createRoot(document.getElementById("root")).render(<App />);
