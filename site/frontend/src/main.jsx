import React, { useEffect, useLayoutEffect, useRef, useState } from "react";
import { createRoot } from "react-dom/client";
import "./theme.css";
import { Browse } from "./browse";
import { Compare, Detail } from "./reading";
import { LoadState, useContent } from "./shared";
import { paramsFrom, route } from "./curriculum";
import { resolveView } from "../compat/modules/route-views.mjs";
import "../compat/atlas-shell.css";
import "../compat/atlas-print.css";

function samePortalURL(first, second, match = "route") {
  if (!first || !second) return false;
  const a = new URL(first, location.href);
  const b = new URL(second, location.href);
  // Sites redirects these HTML entry points. GitHub Pages serves the .html names.
  const pathname = (url) => url.pathname.replace(/\/index(?:\.html)?\/?$/, "/")
    .replace(/\/(legacy|inquiry-workbook|distribution-lab)(?:\.html)?\/?$/, "/$1");
  return a.origin === location.origin && a.origin === b.origin && pathname(a) === pathname(b)
    && (match === "path" || a.search === b.search)
    && (match !== "route" || a.hash === b.hash);
}

function restoreReadingSession() {
  try {
    const pending = JSON.parse(sessionStorage.getItem("atlas-reading-resume"));
    sessionStorage.removeItem("atlas-reading-resume");
    const current = paramsFrom(location.hash);
    if (samePortalURL(pending?.href, location.href) && current.get("view") === "standard" && current.get("code") === pending.code) {
      history.replaceState({ ...pending.state, detachedReturn: true }, "");
    }
    const explore = JSON.parse(sessionStorage.getItem("atlas-explore-origin"));
    sessionStorage.removeItem("atlas-explore-origin");
    if (samePortalURL(explore?.destination, location.href) && samePortalURL(explore.href, document.referrer, "document")) {
      history.replaceState({ ...history.state, exploreOrigin: explore }, "");
    }
    const resume = JSON.parse(sessionStorage.getItem("atlas-compat-resume"));
    sessionStorage.removeItem("atlas-compat-resume");
    if (samePortalURL(resume?.href, location.href) && resume.focusKey) {
      const focusOnReturn = resume.state?.focusOnReturn || { id: resume.focusKey, href: resume.focusKey, scroll: resume.scroll };
      history.replaceState({ ...history.state, ...resume.state, detachedReturn: true, focusOnReturn }, "");
    }
  } catch {
    // The link still opens normally when a browser disables session storage.
  }
}

function routeReader() {
  const { params, entry } = resolveView(location.hash, "reader");
  if (entry === "legacy") {
    location.replace("./legacy.html#" + params);
    return false;
  }
  if (location.hash && params.get("view") !== new URLSearchParams(location.hash.slice(1)).get("view")) {
    history.replaceState(history.state, "", "#" + params);
  }
  return true;
}

const showReader = routeReader();
if (showReader) restoreReadingSession();

function App() {
  const [hash, setHash] = useState(location.hash);
  const params = paramsFrom(hash);
  const view = params.get("view");
  const code = params.get("code");
  const request = useContent("catalog.json");
  const catalog = request.data;
  const previous = useRef({});

  useEffect(() => {
    const update = () => { if (routeReader()) setHash(location.hash); };
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
    if (link.classList.contains("atlas-skip")) {
      event.preventDefault();
      document.getElementById("main").focus();
    } else if (link.id === "nav-compare" && view !== "compare") {
      openLinked(event, undefined, link);
    } else if (samePortalURL(link.href, location.href, "path") && link.hash.startsWith("#view=")) {
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

  function openLinked(event, selectedCode, link = event.currentTarget) {
    if (event.button !== 0 || event.ctrlKey || event.metaKey || event.altKey || event.shiftKey) return;
    event.preventDefault();
    const focusOnReturn = { row: selectedCode, id: link.id, scroll: window.scrollY };
    const origin = location.hash || route("catalog");
    const position = history.state?.position ?? 0;
    const catalogReturn = view === "catalog" ? origin : history.state?.catalogReturn;
    const catalogPosition = view === "catalog" ? position : history.state?.catalogPosition;
    const catalogFocus = view === "catalog" ? focusOnReturn : history.state?.catalogFocus;
    const detachedReturn = history.state?.detachedReturn;
    const returnState = { ...history.state, position, focusOnReturn };
    history.replaceState(returnState, "");
    go(link.hash, {
      returnTo: origin, returnPosition: position, returnState, restore: focusOnReturn,
      catalogReturn, catalogPosition, catalogFocus, detachedReturn,
    });
  }

  function returnTo(event, target) {
    if (event.button !== 0 || event.ctrlKey || event.metaKey || event.altKey || event.shiftKey) return;
    event.preventDefault();
    const state = history.state;
    if (samePortalURL(state?.exploreOrigin?.href, target)) {
      const origin = state.exploreOrigin;
      const entry = window.navigation?.entries().find((item) => item.key === origin.entryKey && samePortalURL(item.url, target));
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
      [...document.querySelectorAll("#main a[href]")].find((link) => samePortalURL(link.href, saved.href)));
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
    const heading = document.querySelector("#main h1")?.textContent;
    if (!heading) return;
    const standard = view === "standard" && catalog?.standards.some((s) => s.code === code);
    document.title = (standard ? code + " · " : "") + heading + " · 수학의 연결 지도";
  }, [view, code, catalog, hash]);

  useLayoutEffect(() => {
    const header = document.querySelector(".atlas-header");
    const footer = document.querySelector(".atlas-footer");
    const current = view === "standard" ? "catalog" : view;
    for (const link of header.querySelectorAll("[data-atlas-nav]")) {
      if (link.dataset.atlasNav === current) link.setAttribute("aria-current", "page");
      else link.removeAttribute("aria-current");
    }
    header.addEventListener("click", rememberReading, true);
    header.addEventListener("click", navigateMenu);
    footer.addEventListener("click", rememberReading, true);
    return () => {
      header.removeEventListener("click", rememberReading, true);
      header.removeEventListener("click", navigateMenu);
      footer.removeEventListener("click", rememberReading, true);
    };
  }, [hash]);

  return <main id="main" tabIndex={-1} onClickCapture={rememberReading}>
      {!catalog ? <div className="site-width loading-wrap"><LoadState request={request} label="교육과정 목록을 불러오고 있습니다…" /></div>
        : view === "standard" ? <Detail catalog={catalog} params={params} go={go} returnTo={returnTo} onOpen={openLinked} />
        : view === "compare" ? <Compare catalog={catalog} params={params} go={go} returnTo={returnTo} onOpen={openLinked} />
        : <Browse catalog={catalog} params={params} go={go} onOpen={openLinked} returnTo={returnTo} />}
  </main>;
}

if (showReader) createRoot(document.getElementById("root")).render(<App />);
