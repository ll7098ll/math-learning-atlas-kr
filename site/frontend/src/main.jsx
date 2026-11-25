import React, { useEffect, useLayoutEffect, useRef, useState } from "react";
import { createRoot } from "react-dom/client";
import { BookOpen } from "lucide-react";
import "./theme.css";
import { Browse } from "./browse";
import { Compare, Detail } from "./reading";
import { LoadState, Pdf, useContent } from "./shared";
import { oldRoute, paramsFrom, route } from "./curriculum";
import "../compat/atlas-shell.css";
import "../compat/atlas-print.css";

function restoreReadingSession() {
  try {
    const pending = JSON.parse(sessionStorage.getItem("atlas-reading-resume"));
    sessionStorage.removeItem("atlas-reading-resume");
    const current = paramsFrom(location.hash);
    if (pending?.href === location.href && current.get("view") === "standard" && current.get("code") === pending.code) {
      history.replaceState({ ...pending.state, detachedReturn: true }, "");
    }
    const explore = JSON.parse(sessionStorage.getItem("atlas-explore-origin"));
    sessionStorage.removeItem("atlas-explore-origin");
    if (explore?.destination === location.href && document.referrer) {
      const from = new URL(explore.href);
      const referrer = new URL(document.referrer);
      if (from.origin === location.origin && from.origin === referrer.origin && from.pathname === referrer.pathname) {
        history.replaceState({ ...history.state, exploreOrigin: explore }, "");
      }
    }
    const resume = JSON.parse(sessionStorage.getItem("atlas-compat-resume"));
    sessionStorage.removeItem("atlas-compat-resume");
    if (resume?.href === location.href && resume.focusKey) {
      const focusOnReturn = resume.state?.focusOnReturn || { id: resume.focusKey, href: resume.focusKey, scroll: resume.scroll };
      history.replaceState({ ...history.state, ...resume.state, detachedReturn: true, focusOnReturn }, "");
    }
  } catch {
    // The link still opens normally when a browser disables session storage.
  }
}

restoreReadingSession();

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
    history.pushState({ ...state, position: (history.state?.position ?? 0) + 1 }, "", target);
    setHash(target);
  }

  function navigateMenu(event) {
    if (event.defaultPrevented || event.button !== 0 || event.ctrlKey || event.metaKey || event.altKey || event.shiftKey) return;
    const link = event.target.closest("a[href]");
    if (!link || link.target || link.hasAttribute("download")) return;
    if (link.getAttribute("href").startsWith("#view=")) {
      event.preventDefault();
      go(link.hash);
    }
  }

  function rememberReading(event) {
    if (event.button !== 0 || event.ctrlKey || event.metaKey || event.altKey || event.shiftKey) return;
    const link = event.target.closest("a[href]");
    if (!link || link.target || link.origin !== location.origin) return;
    const page = link.pathname.slice(link.pathname.lastIndexOf("/") + 1).replace(/\.html$/, "");
    if (!["legacy", "inquiry-workbook", "distribution-lab"].includes(page)) return;
    const focusOnReturn = { id: link.id, href: link.href, scroll: window.scrollY };
    const state = { ...history.state, focusOnReturn };
    history.replaceState(state, "");
    try {
      const destination = new URLSearchParams(link.hash.slice(1));
      const reading = view === "standard" && page === "legacy" &&
        ["code", "target", "node"].some((key) => destination.get(key) === code);
      sessionStorage.setItem(reading ? "atlas-reading-origin" : "atlas-compat-origin", JSON.stringify({
        code, href: location.href, destination: link.href,
        entryKey: window.navigation?.currentEntry?.key, position: state.position ?? 0, state,
        focusKey: link.id || link.href, scroll: window.scrollY,
        label: view === "standard" ? "읽던 성취기준으로" : view === "compare" ? "비교 화면으로"
          : params.get("q") ? "검색 결과로" : "교육과정 탐색으로",
      }));
    } catch {
      // Native navigation works without storage.
    }
  }

  function openLinked(event, selectedCode) {
    if (event.button !== 0 || event.ctrlKey || event.metaKey || event.altKey || event.shiftKey) return;
    event.preventDefault();
    const focusOnReturn = { row: selectedCode, id: event.currentTarget.id, scroll: window.scrollY };
    const origin = location.hash || route("catalog");
    const position = history.state?.position ?? 0;
    const catalogReturn = view === "catalog" ? origin : history.state?.catalogReturn;
    const catalogPosition = view === "catalog" ? position : history.state?.catalogPosition;
    const catalogFocus = view === "catalog" ? focusOnReturn : history.state?.catalogFocus;
    const detachedReturn = history.state?.detachedReturn;
    const returnState = { ...history.state, position, focusOnReturn };
    history.replaceState(returnState, "");
    go(event.currentTarget.getAttribute("href"), {
      returnTo: origin, returnPosition: position, returnState, restore: focusOnReturn,
      catalogReturn, catalogPosition, catalogFocus, detachedReturn,
    });
  }

  function returnTo(event, target) {
    if (event.button !== 0 || event.ctrlKey || event.metaKey || event.altKey || event.shiftKey) return;
    event.preventDefault();
    const state = history.state;
    if (state?.exploreOrigin?.href === target) {
      const origin = state.exploreOrigin;
      const entry = window.navigation?.entries().find((item) => item.key === origin.entryKey && item.url === target);
      const resume = () => {
        try { sessionStorage.setItem("atlas-explore-resume", JSON.stringify(origin)); } catch { /* Optional storage. */ }
        location.assign(target);
      };
      if (entry) window.navigation.traverseTo(entry.key).finished.catch(resume);
      else resume();
      return;
    }
    const position = target === state?.returnTo ? state.returnPosition
      : target === state?.catalogReturn ? state.catalogPosition : undefined;
    if (!state?.detachedReturn && Number.isInteger(position) && position < state.position) {
      history.go(position - state.position);
    } else if (target === state?.returnTo && state?.returnState) {
      go(target, { ...state.returnState, detachedReturn: true });
    } else {
      const focusOnReturn = target === state?.catalogReturn ? state?.catalogFocus : state?.restore;
      const previousStandard = paramsFrom(target).get("view") === "standard";
      go(target, {
        focusOnReturn, detachedReturn: state?.detachedReturn,
        ...(previousStandard && state?.catalogReturn ? {
          returnTo: state.catalogReturn, catalogReturn: state.catalogReturn, catalogFocus: state.catalogFocus,
        } : {}),
      });
    }
  }

  useLayoutEffect(() => {
    if (!catalog) return;
    const prior = previous.current;
    const transition = prior.view && (prior.view !== view || (view === "standard" && prior.code !== code));
    previous.current = { view, code };
    const saved = history.state?.focusOnReturn;
    const row = view === "catalog" ? params.get("focus") : "";
    const id = saved?.id || ((saved?.row || row) && "std-" + (saved?.row || row));
    const locate = () => (id && document.getElementById(id)) || (saved?.href &&
      [...document.querySelectorAll("#main a[href]")].find((link) => link.href === saved.href));
    const restoreFocus = (target) => {
      if (!target) return false;
      if (saved?.href) {
        for (let note = target.closest("details"); note; note = note.parentElement?.closest("details")) {
          note.open = true;
        }
      }
      if (!target.getClientRects().length) return false;
      target.focus({ preventScroll: true });
      if (saved) window.scrollTo(0, saved.scroll);
      else target.scrollIntoView({ block: "center" });
      return true;
    };
    if (restoreFocus(locate())) return;
    if (saved?.href) {
      const observer = new MutationObserver(() => {
        if (restoreFocus(locate())) observer.disconnect();
      });
      observer.observe(document.getElementById("main"), { childList: true, subtree: true });
      return () => observer.disconnect();
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
    ["compare", "범위 비교", route("compare")],
    ["hierarchy", "개념으로 보기", oldRoute("hierarchy")],
    ["about", "자료 안내", oldRoute("about")],
  ];

  return <>
    <a className="skip-link" href="#main" onClick={(event) => {
      event.preventDefault();
      document.getElementById("main").focus();
    }}>본문으로 이동</a>
    <header className="site-header" onClick={navigateMenu} onClickCapture={rememberReading}>
      <div className="site-width header-inner">
        <a className="brand" href={route("catalog")}><span className="brand-mark"><BookOpen size={21} aria-hidden="true" /></span>수학의 연결 지도</a>
        <nav aria-label="주요 탐색">{menu.map(([id, label, href]) =>
          <a key={id} id={"nav-" + id} href={href} aria-current={(view === id || id === "catalog" && view === "standard") ? "page" : undefined}>
            {label}
          </a>)}</nav>
        <span className="header-source"><Pdf>교육과정 원문 PDF</Pdf></span>
      </div>
    </header>

    <main id="main" tabIndex={-1} onClickCapture={rememberReading}>
      {!catalog ? <div className="site-width loading-wrap"><LoadState request={request} label="교육과정 목록을 불러오고 있습니다…" /></div>
        : view === "standard" ? <Detail catalog={catalog} params={params} go={go} returnTo={returnTo} onOpen={openLinked} />
        : view === "compare" ? <Compare catalog={catalog} params={params} go={go} returnTo={returnTo} onOpen={openLinked} />
        : <Browse catalog={catalog} params={params} go={go} onOpen={openLinked} />}
    </main>

    <footer className="site-footer" onClickCapture={rememberReading}>
      <div className="site-width footer-inner">
        <div><strong>수학의 연결 지도</strong><p>교육부 고시 제2022-33호 · 별책 8 수학과 교육과정</p></div>
        <div className="footer-links">
          <span>개발자 이병민</span>
          <a className="text-link" href="mailto:ll7098ll@gmail.com">ll7098ll@gmail.com</a>
          <a className="text-link" href="https://github.com/ll7098ll">GitHub 프로필</a>
          <a id="footer-sources" className="text-link" href={oldRoute("about")}>자료의 출처와 분석 기준</a>
        </div>
      </div>
    </footer>
  </>;
}

createRoot(document.getElementById("root")).render(<App />);
