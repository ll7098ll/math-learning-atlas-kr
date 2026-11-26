(() => {
  const main = document.querySelector("main");
  if (!main) return;

  document.body.classList.add("atlas-compat");
  const page = location.pathname.replace(/\/$/, "").split("/").pop().replace(/\.html$/, "");
  const tool = page === "distribution-lab" || page === "inquiry-workbook";
  document.body.classList.toggle("atlas-tool", tool);
  main.id ||= "main";
  main.tabIndex = -1;

  const nav = [
    ["catalog", "교육과정 탐색", "./#view=catalog"],
    ["network", "연결 지도", "./legacy.html#view=network&scope=all"],
    ["compare", "학년군·과목 비교", "./#view=compare"],
    ["hierarchy", "개념으로 보기", "./legacy.html#view=hierarchy"],
    ["about", "자료 안내", "./legacy.html#view=about"],
  ];
  const header = document.createElement("header");
  header.className = "atlas-header";
  header.innerHTML = `<a class="atlas-skip" href="#main">본문으로 이동</a>
    <div class="atlas-header-inner">
      <a class="atlas-brand" href="./#view=catalog">
        <span class="atlas-mark" aria-hidden="true">
          <svg width="21" height="21" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M12 7v14"/><path d="M3 18a1 1 0 0 1-1-1V4a1 1 0 0 1 1-1h4a5 5 0 0 1 5 5 5 5 0 0 1 5-5h4a1 1 0 0 1 1 1v13a1 1 0 0 1-1 1h-5a4 4 0 0 0-4 4 4 4 0 0 0-4-4z"/>
          </svg>
        </span>수학의 연결 지도
      </a>
      <nav aria-label="주요 탐색">
        ${nav.map(([id, title, href]) => `<a href="${href}" data-atlas-nav="${id}">${title}</a>`).join("")}
      </nav>
      <span class="atlas-header-source"><a href="curriculum.pdf" target="_blank" rel="noopener">교육과정 원문 PDF</a></span>
    </div>`;
  const previousHeader = document.querySelector("body > .site-header");
  if (previousHeader) previousHeader.replaceWith(header);
  else document.body.prepend(header);
  const oldSkip = document.querySelector("body > .skip");
  oldSkip?.remove();
  header.querySelector(".atlas-skip").addEventListener("click", (event) => {
    event.preventDefault();
    main.focus();
    main.scrollIntoView({ block: "start" });
  });

  const developerLinks = `<a href="mailto:ll7098ll@gmail.com">ll7098ll@gmail.com</a>
    <a href="https://github.com/ll7098ll">GitHub 프로필</a>`;
  const footer = document.createElement("footer");
  footer.className = "atlas-footer";
  footer.innerHTML = `<div><span><strong>수학의 연결 지도</strong><small>교육부 고시 제2022-33호 · 별책 8 수학과 교육과정</small></span>
    <div class="atlas-developer-links"><span>개발자 이병민</span>${developerLinks}<a href="./legacy.html#view=about">이 자료는 어떻게 만들었나요?</a></div></div>`;
  const previousFooter = document.querySelector("body > .site-footer");
  if (previousFooter) previousFooter.replaceWith(footer);
  else main.after(footer);

  function route() {
    const params = new URLSearchParams(location.hash.slice(1));
    const alias = { map: "catalog", explore: "connections" }[params.get("view")];
    if (alias) params.set("view", alias);
    return params;
  }

  function codeFor(params) {
    return params.get("view") === "network" ? params.get("node")
      : params.get("view") === "hierarchy" ? params.get("target") : params.get("code");
  }

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

  function readingOrigin() {
    try {
      if (history.state?.atlasReadingOrigin) return history.state.atlasReadingOrigin;
      const pending = JSON.parse(sessionStorage.getItem("atlas-reading-origin"));
      if (!pending || !document.referrer) return null;
      const from = new URL(pending.href);
      const destination = new URL(pending.destination);
      const sourceParams = new URLSearchParams(from.hash.slice(1));
      if (!samePortalURL(from, document.referrer, "document") || !samePortalURL(destination, location.href, "document")
          || sourceParams.get("view") !== "standard" || sourceParams.get("code") !== pending.code) return null;
      const expected = new URLSearchParams(destination.hash.slice(1));
      const current = new URLSearchParams(location.hash.slice(1));
      // Legacy adds the saved school scope to routes that omit it.
      if (!expected.has("scope")) current.delete("scope");
      expected.sort();
      current.sort();
      if (current.toString() !== expected.toString()) return null;
      history.replaceState({ ...history.state, atlasReadingOrigin: pending }, "");
      sessionStorage.removeItem("atlas-reading-origin");
      return pending;
    } catch {
      return null;
    }
  }

  const origin = readingOrigin();
  if (origin) {
    window.addEventListener("hashchange", () => {
      if (!history.state?.atlasReadingOrigin) history.replaceState({ ...history.state, atlasReadingOrigin: origin }, "");
    });
    main.addEventListener("click", (event) => {
      const link = event.target.closest("a[href]");
      if (!link || event.defaultPrevented || event.button !== 0 || event.ctrlKey || event.metaKey
          || event.shiftKey || event.altKey || (link.target && link.target !== "_self")) return;
      const target = new URL(link.href);
      const reader = new URL(origin.href);
      const params = new URLSearchParams(target.hash.slice(1));
      if (!samePortalURL(target, reader, "path")
          || params.get("view") !== "standard" || params.has("section") || params.get("code") !== origin.code
          || (!tool && codeFor(route()) !== origin.code)) return;
      event.preventDefault();
      const resume = () => {
        try {
          sessionStorage.setItem("atlas-reading-resume", JSON.stringify({ code: origin.code, href: origin.href, state: origin.state }));
        } catch { /* Ordinary links still work with storage disabled. */ }
        location.assign(reader.href);
      };
      const entry = window.navigation?.entries().find((item) => item.key === origin.entryKey && samePortalURL(item.url, reader));
      if (entry) window.navigation.traverseTo(entry.key).finished.catch(resume);
      else resume();
    });
  }

  const folder = new URL("./", location.href);
  const isReader = (url) => samePortalURL(url, folder, "path");
  const isWorkspace = (url) => ["legacy", "distribution-lab", "inquiry-workbook"].some((name) =>
    samePortalURL(url, new URL(name, folder), "path"));

  function getContext(key) {
    try { return JSON.parse(sessionStorage.getItem(key)); } catch { return null; }
  }

  function saveContext(key, value) {
    try {
      if (value) sessionStorage.setItem(key, JSON.stringify(value));
      else sessionStorage.removeItem(key);
    } catch { /* Direct links still work when storage is disabled. */ }
  }

  function contextMatches(context, destination) {
    if (!context?.href || !context.destination) return false;
    const target = new URL(context.destination);
    if (!samePortalURL(target, destination, "document")) return false;
    const requested = new URLSearchParams(target.hash.slice(1));
    const actual = new URLSearchParams(destination.hash.slice(1));
    // The loader may have filled in a default scope, map route, or focused node.
    return [...requested].every(([key, value]) => actual.get(key) === value);
  }

  const pendingParent = getContext("atlas-compat-origin");
  if (pendingParent && document.referrer && contextMatches(pendingParent, new URL(location.href))) {
    const source = new URL(pendingParent.href);
    if (samePortalURL(source, document.referrer, "document") && (isReader(source) || isWorkspace(source))) {
      history.replaceState({ ...history.state, atlasParent: pendingParent }, "");
      saveContext("atlas-compat-origin", null);
    }
  }

  function returnLink(event, context) {
    event.preventDefault();
    const previous = window.navigation?.entries().find((entry) => entry.key === context.entryKey && samePortalURL(entry.url, context.href));
    const fallback = () => {
      const target = new URL(context.href);
      saveContext(isReader(target) ? "atlas-compat-resume" : "atlas-explore-resume", context);
      location.assign(target.href);
    };
    if (previous) window.navigation.traverseTo(previous.key).finished.catch(fallback);
    else fallback();
  }

  function prepareContextReturn() {
    const parent = history.state?.atlasParent;
    const heading = main.querySelector(".atlas-page-header");
    if (!heading) return;
    const old = heading.parentElement.querySelector(":scope > .atlas-context-return");
    if (parent && heading.closest(".guided-map") && new URLSearchParams(new URL(parent.href).hash.slice(1)).get("view") === "network") {
      old?.remove();
      return;
    }
    if (!parent || samePortalURL(old?.href, parent.href)) return;
    old?.remove();
    const link = document.createElement("a");
    link.href = parent.href;
    link.className = "atlas-return atlas-context-return";
    link.textContent = "← " + (parent.label || "찾아보던 화면으로");
    link.addEventListener("click", (event) => {
      if (!event.button && !event.ctrlKey && !event.metaKey && !event.altKey && !event.shiftKey) returnLink(event, parent);
    });
    heading.before(link);
  }

  let restoringWorkspace = Boolean(getContext("atlas-explore-resume") || history.state?.atlasDeparture);
  function restoreWorkspaceFocus() {
    if (!restoringWorkspace) return;
    const saved = [getContext("atlas-explore-resume"), history.state?.atlasDeparture].find((item) => samePortalURL(item?.href, location.href));
    if (!saved?.focusKey) return;
    const target = document.getElementById(saved.focusKey)
      || [...main.querySelectorAll("a[href]")].find((link) => samePortalURL(link.href, saved.focusKey));
    if (!target) return;
    restoringWorkspace = false;
    for (let ancestor = target.parentElement; ancestor; ancestor = ancestor.parentElement) {
      if (ancestor.tagName === "DETAILS") ancestor.open = true;
    }
    saveContext("atlas-explore-resume", null);
    history.replaceState({ ...history.state, atlasDeparture: null }, "");
    requestAnimationFrame(() => requestAnimationFrame(() => {
      if (!target.isConnected) return;
      target.focus({ preventScroll: true });
      window.scrollTo(0, saved.scroll || 0);
    }));
  }

  let nextParent;
  document.addEventListener("click", (event) => {
    const link = event.target.closest("a[href]");
    if (!link || event.defaultPrevented || event.button !== 0 || event.ctrlKey || event.metaKey
        || event.shiftKey || event.altKey || (link.target && link.target !== "_self") || link.hasAttribute("download")) return;
    const destination = new URL(link.href);
    if (samePortalURL(destination, location.href) || (!isReader(destination) && !isWorkspace(destination))) return;
    const params = route();
    const context = {
      href: location.href, destination: destination.href, entryKey: window.navigation?.currentEntry?.key,
      focusKey: link.id || link.href, scroll: window.scrollY,
      conceptPair: history.state?.atlasConceptPair,
      label: params.has("concept") ? "읽던 개념으로" : tool ? "읽던 탐구 도구로"
        : params.get("view") === "about" ? "자료 안내로" : "찾아보던 화면으로",
    };
    history.replaceState({ ...history.state, atlasDeparture: context }, "");
    if (isReader(destination)) saveContext("atlas-explore-origin", context);
    else {
      nextParent = context;
      // A link to a .html alias can load a new document before the host redirects.
      saveContext("atlas-compat-origin", context);
    }
  });
  window.addEventListener("hashchange", (event) => {
    if (contextMatches(nextParent, new URL(event.newURL))) {
      history.replaceState({ ...history.state, atlasParent: nextParent, atlasDeparture: null }, "");
      saveContext("atlas-compat-origin", null);
    }
    nextParent = undefined;
    restoringWorkspace = Boolean(history.state?.atlasDeparture || getContext("atlas-explore-resume"));
    prepareContextReturn();
    restoreWorkspaceFocus();
  });
  window.addEventListener("pageshow", () => {
    restoringWorkspace = Boolean(history.state?.atlasDeparture || getContext("atlas-explore-resume"));
    restoreWorkspaceFocus();
  });

  function sectionNavigation(params) {
    const view = params.get("view");
    const menu = document.createElement("nav");
    menu.className = "atlas-path";
    if (view === "standard") {
      menu.setAttribute("aria-label", "성취기준 이동");
      const summary = new URLSearchParams(params);
      summary.delete("section");
      const link = document.createElement("a");
      link.href = "./#" + summary;
      link.textContent = "성취기준 요약";
      menu.append(link);
      return menu;
    }
    const mode = params.get("mode");
    if (view === "hierarchy" && ["goals", "tasks"].includes(mode) && main.querySelector(".gn-lanes, .tp-official")) {
      menu.setAttribute("aria-label", "목표와 과제 보기");
      const scope = params.get("scope") || "all";
      for (const [destination, label] of [["goals", "목표에 필요한 것과 쓰이는 곳"], ["tasks", "수업 과제와 풀이"], ["", "수학 개념 목록"]]) {
        const link = document.createElement("a");
        const source = [...main.querySelectorAll(":scope > .cp-actions a")].find((item) =>
          new URLSearchParams(item.hash.slice(1)).get("mode") === destination);
        const values = new URLSearchParams({ view: "hierarchy", scope });
        if (destination) {
          values.set("mode", destination);
          values.set("target", params.get("target"));
          if (params.get("goal")) values.set("goal", params.get("goal"));
        }
        link.href = destination === mode ? "#" + params : source?.hash || "#" + values;
        if (destination === mode) link.setAttribute("aria-current", "page");
        link.textContent = label;
        menu.append(link);
      }
      return menu;
    }
    if (!["hierarchy", "network", "overview", "connections", "explore"].includes(view)) return menu;
    menu.setAttribute("aria-label", "연결 지도 보기");
    const modes = [
      ["hierarchy", "", "수학 개념 찾기"],
      ["network", "", "전체 연결망"],
      ["overview", "flow", "개념 흐름"],
      ["overview", "structure", "학교급별 성취기준"],
      ["overview", "expanded", "성취기준 펼쳐 보기"],
    ];
    const current = view === "hierarchy" && (params.has("concept") || params.has("map")) ? "" : view === "overview"
      ? params.get("density") === "expanded" ? "expanded" : params.get("mode") || "structure"
      : view === "network" || view === "hierarchy" ? view : "";
    for (const [target, mode, label] of modes) {
      const link = document.createElement("a");
      const values = new URLSearchParams({ view: target });
      if (target === "network") {
        values.set("mapMode", "full");
        const node = codeFor(params) || params.get("target");
        if (node) values.set("node", node);
      }
      if (params.get("scope")) values.set("scope", params.get("scope"));
      if (mode) values.set("mode", mode === "expanded" ? "structure" : mode);
      if (mode === "expanded") values.set("density", "expanded");
      link.href = "#" + values;
      if ((mode || target) === current) link.setAttribute("aria-current", "page");
      link.textContent = label;
      menu.append(link);
    }
    return menu;
  }

  function prepareHeading(params) {
    const heading = main.querySelector("h1");
    if (!heading) return;
    const frame = heading.closest(".page-heading, .network-intro, .network-heading, .standard-header, header")
      || heading.parentElement;
    if (frame === main) {
      if (heading.classList.contains("atlas-page-title")) return;
      const title = document.createElement("div");
      heading.before(title);
      title.append(heading);
      title.className = "atlas-page-header";
    } else {
      frame.classList.add("atlas-page-header");
    }
    heading.classList.add("atlas-page-title");
    const view = params.get("view");
    if (main.querySelector(".pathway-search") && heading.textContent !== "개념으로 보기") {
      heading.textContent = "개념으로 보기";
      const lead = frame.querySelector(".lead");
      if (lead) lead.textContent = "익숙한 수학 개념을 골라 학교급마다 배우는 내용과 연결되는 이유를 살펴보세요.";
    }
    const sectionName = tool ? (page === "distribution-lab" ? "분포 탐구" : "탐구 기록지")
      : view === "standard" ? "전체 상세 분석" : view === "connections" ? "연결 근거"
      : view === "network" ? (main.querySelector(".guided-map") ? "기준 하나씩 보기" : params.has("node") ? "선택한 기준의 연결" : "전체 연결망")
      : view === "hierarchy" ? ({ goals: "목표에 필요한 것과 쓰이는 곳", tasks: "수업 과제와 풀이" }[params.get("mode")]
        || (params.has("concept") || params.has("map") ? "개념의 연결" : "수학 개념 찾기"))
      : view === "overview" ? (params.get("mode") === "structure" ? "학교급별 성취기준" : "개념 흐름")
      : view === "about" ? "자료의 출처와 검토 내용" : "";
    if (sectionName && !frame.querySelector(".atlas-location")) {
      const crumb = document.createElement("nav");
      crumb.className = "atlas-location";
      crumb.setAttribute("aria-label", "현재 위치");
      const parent = document.createElement("a");
      const hub = nav.find(([key]) => key === (tool || view === "about" ? "about" : view === "standard" ? "catalog" : view === "hierarchy" ? "hierarchy" : "network"));
      parent.href = hub[2];
      parent.textContent = hub[1];
      const current = document.createElement("span");
      current.setAttribute("aria-current", "page");
      current.textContent = sectionName;
      crumb.append(parent);
      if (view === "hierarchy" && ["goals", "tasks"].includes(params.get("mode")) && params.get("target")) {
        const standard = document.createElement("a");
        standard.href = "./#" + new URLSearchParams({ view: "standard", code: params.get("target") });
        standard.textContent = params.get("target");
        crumb.append(standard);
      }
      crumb.append(current);
      heading.before(crumb);
    } else if (frame.querySelector(".atlas-location [aria-current]")?.textContent !== sectionName) {
      const current = frame.querySelector(".atlas-location [aria-current]");
      if (current) current.textContent = sectionName;
    }
    if (tool || view === "standard" || view === "about") return;
    if (main.querySelector(".guided-map")) return;
    const menu = sectionNavigation(params);
    const oldMenu = main.querySelector(".atlas-path");
    if (oldMenu?.dataset.route === params.toString()) return;
    main.querySelectorAll(".overview-views").forEach((element) => { element.hidden = true; });
    menu.dataset.route = params.toString();
    if (oldMenu) oldMenu.replaceWith(menu);
    else if (menu.children.length) {
      const section = heading.closest(".atlas-page-header");
      if (view !== "network" && menu.getAttribute("aria-label") === "연결 지도 보기") {
        const switcher = document.createElement("details");
        switcher.className = "atlas-view-switcher";
        const title = document.createElement("summary");
        title.textContent = "다른 방식으로 연결 보기";
        switcher.append(title, menu);
        section.after(switcher);
      } else section.after(menu);
    }
  }

  function prepareReading(params) {
    if (params.get("view") !== "standard") return;
    const frame = main.querySelector(".standard-header");
    if (frame && !main.querySelector(".atlas-path")) frame.before(sectionNavigation(params));
    const sidebar = main.querySelector(".reading-aside");
    const outline = sidebar?.querySelector("nav");
    if (!outline || sidebar.querySelector(".atlas-reading-outline")) return;
    const disclosure = document.createElement("details");
    disclosure.className = "atlas-reading-outline";
    const label = document.createElement("summary");
    label.textContent = "이 문서의 목차";
    disclosure.open = !matchMedia("(max-width: 700px)").matches;
    sidebar.append(disclosure);
    disclosure.append(label, outline);
  }

  function prepareStandardReturn(params) {
    const view = params.get("view");
    const code = ["network", "connections", "hierarchy"].includes(view) ? codeFor(params) : "";
    const oldLink = main.querySelector(".atlas-standard-return");
    if (!/^[0-9]+[가-힣]+(?:[0-9]+-)?[0-9]{2}-[0-9]{2}$/u.test(code || "")) {
      oldLink?.remove();
      return;
    }
    const heading = main.querySelector(".atlas-page-header");
    if (!heading) return;
    const target = new URLSearchParams({ view: "standard", code });
    if (params.get("scope")) target.set("scope", params.get("scope"));
    const href = "./#" + target;
    if (oldLink?.getAttribute("href") === href) return;
    const link = document.createElement("a");
    link.className = "atlas-return atlas-standard-return";
    link.href = href;
    link.innerHTML = '<span aria-hidden="true">←</span> 성취기준 상세로';
    if (oldLink) oldLink.replaceWith(link);
    else heading.before(link);
  }

  function focusSection(element) {
    if (!element.matches("summary, button, a[href], input, select, textarea, [tabindex]")) element.tabIndex = -1;
    element.focus({ preventScroll: true });
    element.scrollIntoView({ block: "start" });
  }

  function prepareNetwork() {
    const network = main.querySelector(".atlas-network");
    if (!network) return;
    const workspace = network.querySelector(".atlas-workspace");
    const svg = workspace.querySelector(".atlas-svg");
    let related = workspace.querySelector(".atlas-related-toggle");
    if (!related) {
      const form = network.querySelector(".atlas-controls");
      const intro = network.querySelector(".network-intro h1 + p");
      if (intro) intro.textContent = "점 하나가 성취기준 하나입니다. 점을 선택해 이어진 기준을 보고, ‘연결 근거’에서 두 기준이 이어지는 이유를 읽어 보세요.";
      const conceptLink = network.querySelector(".network-intro > a");
      if (conceptLink) conceptLink.textContent = "개념별로 찾아보기 ↗";
      if (!route().has("node") && ["all", null].includes(route().get("scope"))) {
        const examples = document.createElement("nav");
        examples.className = "atlas-map-examples";
        examples.setAttribute("aria-label", "예시 기준에서 지도 시작");
        const label = document.createElement("strong");
        label.textContent = "여기서 시작하기";
        examples.append(label);
        for (const [code, title] of [["6수01-10", "분수"], ["6수02-03", "비율"], ["9수01-03", "유리수"]]) {
          const link = document.createElement("a");
          link.href = "#" + new URLSearchParams({view: "network", scope: "all", mapMode: "full", node: code});
          link.textContent = title;
          examples.append(link);
        }
        form.before(examples);
      }
      form.querySelector(".atlas-search").firstChild.textContent = "성취기준 찾기";
      form.querySelector('[data-action="reset"]').textContent = "필터 초기화";
      const filters = document.createElement("details");
      filters.className = "atlas-advanced-filters";
      const label = document.createElement("summary");
      label.textContent = "영역·개념·연결선 필터";
      const fields = document.createElement("div");
      fields.className = "atlas-filter-fields";
      for (const field of form.querySelectorAll("label:has(select)")) fields.append(field);
      filters.open = [...fields.querySelectorAll("select")].some((field) => field.value && field.value !== "all");
      filters.append(label, fields);
      form.append(filters);

      const stage = workspace.querySelector(".atlas-stage");
      const toolbar = stage.querySelector(".atlas-tools");
      toolbar.querySelector('[data-action="out"]').after(toolbar.querySelector(".atlas-zoom"));
      const canvas = document.createElement("div");
      canvas.className = "atlas-canvas";
      canvas.append(stage.querySelector(".atlas-axis"), svg, stage.querySelector(".atlas-tooltip"));
      stage.prepend(toolbar, canvas);

      related = document.createElement("button");
      related.type = "button";
      related.className = "atlas-related-toggle";
      related.dataset.startedWithNode = String(route().has("node"));
      related.textContent = "선택 주변만 보기";
      related.setAttribute("aria-pressed", "false");
      related.addEventListener("click", () => {
        const active = workspace.classList.toggle("atlas-related-only");
        related.setAttribute("aria-pressed", String(active));
      });
      const jump = document.createElement("button");
      jump.type = "button";
      jump.textContent = "기준 정보로 이동";
      jump.addEventListener("click", () => focusSection(workspace.querySelector(".atlas-inspector")));
      toolbar.append(related, jump);

      const expand = toolbar.querySelector('[data-action="expand"]');
      workspace.addEventListener("keydown", (event) => {
        if (event.key !== "Escape" || !workspace.classList.contains("is-expanded")) return;
        event.preventDefault();
        event.stopPropagation();
        expand.click();
        expand.focus();
      }, true);
    }
    const filters = network.querySelector(".atlas-advanced-filters");
    const filterCount = [...filters.querySelectorAll("select")].filter((field) => field.value && field.value !== "all").length;
    const label = filterCount ? `영역·개념·연결선 필터 · ${filterCount}개 적용` : "영역·개념·연결선 필터";
    if (filters.firstElementChild.textContent !== label) filters.firstElementChild.textContent = label;
    const selected = Boolean(svg.querySelector(".atlas-dot.is-selected:not([aria-hidden=true])"));
    if (selected && !related.dataset.initialized) {
      related.dataset.initialized = "true";
      if (related.dataset.startedWithNode === "true") {
        workspace.classList.add("atlas-related-only");
        related.setAttribute("aria-pressed", "true");
      }
    }
    related.disabled = !selected;
    if (!selected && workspace.classList.contains("atlas-related-only")) {
      workspace.classList.remove("atlas-related-only");
      related.setAttribute("aria-pressed", "false");
    }
  }

  function prepareGoals() {
    const lanes = main.querySelector(".gn-lanes");
    const focus = lanes?.querySelector(".gn-focus");
    if (!focus) return;
    main.querySelector(".gn-intro").before(focus);
  }

  function preparePathwayActions() {
    for (const actions of main.querySelectorAll(":scope > .cp-actions")) {
      for (const link of actions.querySelectorAll("a")) {
        const target = new URLSearchParams(link.hash.slice(1));
        const view = target.get("view");
        const plainIndex = view === "hierarchy" && !target.has("q") && !target.has("mode") && !target.has("concept");
        link.hidden = view === "standard" || plainIndex || ["goals", "tasks"].includes(target.get("mode"));
      }
      actions.hidden = !actions.querySelector("a:not([hidden])");
    }
  }

  function prepareTasks(params) {
    const articles = [...main.querySelectorAll(".tp-case[data-task-case]")];
    if (!articles.length || main.querySelector(".atlas-task-picker")) return;
    const cases = new Map(articles.map((article) => [article.dataset.taskCase, article]));
    for (const body of main.querySelectorAll(".tp-route-body")) {
      const probe = body.querySelector(":scope > .tp-probe");
      if (probe) body.prepend(probe);
    }
    const goals = [...main.querySelectorAll(".tp-goal-card[data-goal-id]")];
    const picker = document.createElement("form");
    picker.className = "atlas-task-picker";
    picker.setAttribute("aria-label", "목표별 과제 찾아가기");
    const heading = document.createElement("h2");
    heading.textContent = "과제 찾아가기";
    picker.append(heading);

    const goalSelect = document.createElement("select");
    const caseSelect = document.createElement("select");
    const label = (text, control) => {
      const wrapper = document.createElement("label");
      wrapper.append(text, control);
      return wrapper;
    };
    if (goals.length) {
      goalSelect.append(new Option("모든 하위 목표", ""));
      for (const goal of goals) {
        goalSelect.append(new Option(goal.querySelector("h3").textContent, goal.dataset.goalId));
      }
      goalSelect.value = goals.some((goal) => goal.dataset.goalId === params.get("goal")) ? params.get("goal") : "";
      picker.append(label("하위 목표", goalSelect));
    }
    const submit = document.createElement("button");
    submit.type = "submit";
    submit.className = "button primary";
    submit.textContent = "과제로 이동";
    picker.append(label("대표 과제", caseSelect), submit);

    function listCases(selectedCase) {
      const goal = goals.find((item) => item.dataset.goalId === goalSelect.value);
      const ids = goal
        ? [...goal.querySelectorAll(".tp-goal-tasks a")].map((link) => new URLSearchParams(link.hash.slice(1)).get("taskCase"))
        : [...cases.keys()];
      const available = [...new Set(ids)].filter((id) => cases.has(id));
      caseSelect.replaceChildren(new Option(available.length ? "과제를 선택하세요" : "이 목표에 연결된 대표 과제가 없습니다", ""));
      for (const id of available) {
        const article = cases.get(id);
        const prefix = article.closest(".tp-previous-case") ? "기존 설계 · " : "";
        caseSelect.append(new Option(prefix + article.querySelector("h2").textContent, id));
      }
      caseSelect.value = available.includes(selectedCase) ? selectedCase : available.length === 1 ? available[0] : "";
      caseSelect.disabled = !available.length;
      submit.disabled = !caseSelect.value;
    }

    goalSelect.addEventListener("change", () => listCases(caseSelect.value));
    caseSelect.addEventListener("change", () => { submit.disabled = !caseSelect.value; });
    picker.addEventListener("submit", (event) => {
      event.preventDefault();
      const article = cases.get(caseSelect.value);
      if (!article) return;
      const previous = article.closest(".tp-previous-case");
      if (previous) previous.open = true;
      const next = new URLSearchParams(route());
      next.set("taskCase", caseSelect.value);
      if (goalSelect.value) next.set("goal", goalSelect.value);
      else next.delete("goal");
      next.delete("taskRoute");
      if (route().toString() === next.toString()) focusSection(article.querySelector("h2"));
      else location.hash = next.toString();
    });
    listCases(params.get("taskCase"));
    const anchor = main.querySelector(".tp-goals") || articles[0].closest(".tp-previous-case") || articles[0];
    anchor.before(picker);
    if (articles.length === 1) {
      const choice = document.createElement("details");
      choice.className = "atlas-task-choice";
      const label = document.createElement("summary");
      label.textContent = "하위 목표에서 과제 찾기";
      picker.before(choice);
      choice.append(label, picker);
    }
    const goalSection = main.querySelector(".tp-goals");
    if (goalSection && !params.has("goal")) {
      const disclosure = document.createElement("details");
      disclosure.className = "atlas-goal-summary";
      const summary = document.createElement("summary");
      summary.textContent = goalSection.querySelector("h2").textContent;
      goalSection.before(disclosure);
      disclosure.append(summary, goalSection);
    }
    const selected = cases.get(params.get("taskCase"));
    if (selected) {
      // The legacy router finishes by focusing its page heading in the next frame.
      requestAnimationFrame(() => requestAnimationFrame(() => {
        if (!selected.isConnected) return;
        const part = [...selected.querySelectorAll(".tp-route")]
          .find((item) => item.dataset.route === params.get("taskRoute"));
        focusSection(part?.querySelector("summary") || selected.querySelector("h2"));
      }));
    }
  }

  function updateNav() {
    const current = tool ? "about" : document.body.dataset.navView || "network";
    for (const link of header.querySelectorAll("[data-atlas-nav]")) {
      if (link.dataset.atlasNav === current) link.setAttribute("aria-current", "page");
      else link.removeAttribute("aria-current");
    }
  }

  async function prepareConceptIndex(params) {
    const form = main.querySelector(".pathway-search");
    if (!form || form.dataset.domainReady) return;
    form.dataset.domainReady = "pending";
    const list = main.querySelector("section .pathway-cards");
    if (!list) return;
    try {
      const { conceptPathwaysIndex } = await import("./modules/store.mjs");
      const index = await conceptPathwaysIndex();
      if (!form.isConnected) return;
      const groups = new Map(index.groups.map((group) => [group.id, group]));
      const domains = [...new Set(index.groups.map((group) => group.domain))];
      const filter = document.createElement("select");
      filter.name = "conceptDomain";
      filter.append(new Option("모든 개념 분야", ""));
      domains.forEach((domain) => filter.append(new Option(domain)));
      filter.value = domains.includes(params.get("conceptDomain")) ? params.get("conceptDomain") : "";
      const label = document.createElement("label");
      label.append("개념 분야", filter);
      const review = form.querySelector('[name="review"]').closest("label");
      review.before(label);
      const extra = document.createElement("details");
      extra.className = "atlas-index-review";
      const reviewLabel = document.createElement("summary");
      reviewLabel.textContent = "검토 상태";
      extra.open = Boolean(params.get("review"));
      review.before(extra);
      extra.append(reviewLabel, review);
      const header = main.querySelector(".atlas-page-header");
      const switcher = main.querySelector(".atlas-view-switcher");
      const explainer = main.querySelector(".atlas-explainer");
      if (header && switcher && explainer) {
        const options = document.createElement("div");
        options.className = "atlas-index-options";
        header.after(form);
        form.after(options);
        options.append(switcher, explainer);
      }
      const cards = [...list.querySelectorAll("details[data-open]")];
      let count = 0;
      for (const card of cards) {
        const id = card.querySelector("[data-concept-pathway]")?.dataset.conceptPathway;
        const group = groups.get(id);
        card.hidden = Boolean(filter.value && group?.domain !== filter.value);
        if (!card.hidden) count++;
        if (group) {
          const question = card.querySelector(":scope > p");
          if (question) {
            const subline = document.createElement("span");
            subline.className = "atlas-concept-question";
            subline.textContent = question.textContent;
            card.querySelector("summary").append(subline);
            question.remove();
          }
        }
      }
      const summary = list.previousElementSibling;
      if (summary?.tagName === "P" && !filter.value) {
        summary.textContent = `수학 개념 ${count}개 · 이 사이트에서 관련 성취기준을 묶었습니다.`;
      }
      if (filter.value && summary?.tagName === "P") {
        summary.textContent = `${filter.value} · 관련 개념 ${count}개`;
      }
      if (filter.value && !count && cards.length) {
        const all = document.createElement("a");
        const next = new URLSearchParams(params);
        next.delete("conceptDomain");
        all.href = "#" + next;
        all.className = "button";
        all.textContent = "모든 개념 분야에서 찾기";
        list.append(all);
      }
      form.dataset.domainReady = "ready";
    } catch {
      delete form.dataset.domainReady;
    }
  }

  async function prepareConceptPage(params) {
    const concept = params.get("concept");
    if (!concept || params.get("view") !== "hierarchy" || main.hasAttribute("aria-busy")) return;
    const heading = main.querySelector(".atlas-page-header");
    if (!heading || heading.dataset.conceptPage || main.querySelector('[role="alert"]')) return;
    const scope = params.get("scope") || "all";
    const overview = new URLSearchParams({ view: "hierarchy", concept, scope });
    if (params.has("mode") || params.has("relation")) {
      const back = document.createElement("a");
      back.href = "#" + overview;
      back.className = "atlas-concept-overview-link";
      back.textContent = "이 개념의 학년군·과목별 기준";
      heading.append(back);
      heading.dataset.conceptPage = "detail";
      return;
    }
    heading.dataset.conceptPage = "loading";
    try {
      const [store, { esc }] = await Promise.all([import("./modules/store.mjs"), import("./modules/ui.mjs")]);
      const data = await store.conceptPathway(concept);
      if (!heading.isConnected || route().get("concept") !== concept) return;
      const byCode = new Map(store.catalog.standards.map((s) => [s.code, s]));
      const members = data.concept.member_codes.map((code) => byCode.get(code)).filter((s) => store.inScope(s, scope));
      const section = document.createElement("section");
      section.className = "atlas-concept-overview";
      section.dataset.concept = concept;
      const criteria = new Map(members.map((s) => [s.code, s]));
      const perBand = new Map();
      const levelName = (s) => s.level + " · " + store.band(s);
      for (const standard of members) {
        const name = levelName(standard);
        if (!perBand.has(name)) perBand.set(name, []);
        perBand.get(name).push(standard);
      }
      const read = (s) => "./#" + new URLSearchParams({ view: "standard", code: s.code, scope: ["e", "m", "h"][store.levels.indexOf(s.level)] });
      section.innerHTML = `<p class="atlas-concept-question-line">${esc(data.concept.question)}</p>
        <h2>학년군·과목별 성취기준</h2><p class="small">관련 성취기준 ${members.length}개 · 이 사이트에서 찾아 연결했습니다.</p>`;
      if (!members.length) {
        const clear = document.createElement("a");
        const all = new URLSearchParams(overview);
        all.set("scope", "all");
        clear.className = "button";
        clear.href = "#" + all;
        clear.textContent = "모든 학교급에서 이 개념 보기";
        section.append(clear);
      }
      const requested = params.get("target");
      for (const [name, standards] of perBand) {
        const group = document.createElement("details");
        group.className = "atlas-concept-band";
        group.dataset.open = concept + "-" + name;
        group.open = perBand.size === 1 || Boolean(requested && standards.some((s) => s.code === requested));
        group.innerHTML = `<summary>${esc(name)} <small>${standards.length}개</small></summary><ul>${standards.map((s) =>
          `<li><a id="concept-${esc(concept)}-${esc(s.code)}" href="${esc(read(s))}"><strong>${esc(s.title)}</strong><small>${esc(s.code)} · ${esc(s.domain)}</small></a><p><span>공식 성취기준</span> ${esc(s.statement)}</p></li>`
        ).join("")}</ul>`;
        section.append(group);
      }

      if (members.length >= 2) {
        const pairs = data.relations.map((relation) => ({
          relation, a: criteria.get(relation.from.slice(9)), b: criteria.get(relation.to.slice(9)),
        })).filter(({ a, b }) => a && b && a !== b);
        // Prefer an authored cross-school expansion. L014 is the worked fraction example in the design.
        const example = pairs.find(({ relation }) => concept === "fraction" && relation.id === "L014")
          || pairs.find(({ relation, a, b }) => a.level !== b.level && relation.type === "generalizes")
          || pairs.find(({ a, b }) => a.level !== b.level)
          || pairs.find(({ a, b }) => levelName(a) !== levelName(b)) || pairs[0];
        const resume = getContext("atlas-explore-resume");
        const saved = history.state?.atlasConceptPair || (samePortalURL(resume?.href, location.href) && resume.conceptPair);
        const a = (saved?.concept === concept && criteria.get(saved.a)) || example?.a || members[0];
        const b = (saved?.concept === concept && criteria.get(saved.b)) || example?.b
          || members.find((s) => levelName(s) !== levelName(a)) || members.find((s) => s !== a);
        const sample = document.createElement("section");
        sample.className = "atlas-concept-comparison";
        sample.innerHTML = `<h2>두 기준에서 달라지는 점</h2><div class="atlas-concept-pair"></div>
          <div class="atlas-concept-reason"></div><div class="cp-actions"></div>`;
        const pair = sample.querySelector(".atlas-concept-pair");
        const controls = [a, b].map((standard, i) => {
          const column = document.createElement("div");
          column.innerHTML = `<label>${i ? "두 번째 기준" : "첫 번째 기준"}<select></select></label><p></p><a class="text-link"></a>`;
          const select = column.querySelector("select");
          for (const [name, standards] of perBand) {
            const optgroup = document.createElement("optgroup");
            optgroup.label = name;
            for (const s of standards) optgroup.append(new Option(s.title + " · " + s.code, s.code));
            select.append(optgroup);
          }
          select.value = standard.code;
          pair.append(column);
          return { select, statement: column.querySelector("p"), link: column.querySelector("a") };
        });
        function update() {
          const [left, right] = controls.map(({ select, statement, link }) => {
            const s = criteria.get(select.value);
            statement.innerHTML = `<small>${esc(levelName(s))} · 공식 성취기준</small>${esc(s.statement)}`;
            link.href = read(s);
            link.textContent = s.code + " 상세 읽기";
            return s;
          });
          const record = pairs.find(({ a, b }) => a === left && b === right)
            || pairs.find(({ a, b }) => a === right && b === left);
          const reason = sample.querySelector(".atlas-concept-reason");
          const actions = sample.querySelector(".cp-actions");
          actions.replaceChildren();
          if (record) {
            const r = record.relation;
            reason.innerHTML = `<strong>${esc(store.types[r.type] || r.type)} · 자체 분석</strong><p>${esc(r.rationale)}</p>`;
            const evidence = document.createElement("a");
            const where = new URLSearchParams({ view: "hierarchy", concept, scope, mode: "meaning", target: record.a.code, relation: r.id });
            evidence.href = "#" + where;
            evidence.textContent = "왜 연결되는지 보기";
            evidence.className = "text-link";
            actions.append(evidence);
          } else {
            reason.textContent = left === right ? "서로 다른 두 기준을 선택하면 공식 문장을 비교할 수 있습니다."
              : "이 두 기준 사이에 직접 기록된 관계가 없습니다. 위 공식 문장에서 다루는 표현을 비교해 보세요.";
          }
          if (left !== right) {
            const compare = document.createElement("a");
            compare.className = "button";
            compare.id = "compare-concept-" + concept;
            compare.href = "./#" + new URLSearchParams({ view: "compare", left: store.band(left), leftDomain: left.domain,
              leftCode: left.code, right: store.band(right), rightDomain: right.domain, rightCode: right.code });
            compare.textContent = "두 성취기준 나란히 보기";
            actions.append(compare);
          }
        }
        for (const { select } of controls) select.addEventListener("change", () => {
          history.replaceState({ ...history.state, atlasConceptPair: { concept, a: controls[0].select.value, b: controls[1].select.value } }, "");
          update();
        });
        update();
        const jump = document.createElement("button");
        jump.type = "button";
        jump.className = "atlas-concept-jump";
        jump.textContent = "두 기준에서 달라지는 점 보기 ↓";
        jump.addEventListener("click", () => focusSection(sample.querySelector("h2")));
        section.querySelector(".atlas-concept-question-line").after(jump);
        section.append(sample);
      }

      const more = document.createElement("details");
      more.className = "atlas-concept-depth";
      more.innerHTML = "<summary>개별 목표·과제와 전체 연결 분석</summary>";
      const deeper = [...main.querySelectorAll(":scope > :is(.cp-review, .cp-controls, .cp-tabs, .cp-map, .cp-actions, .cp-details, .cp-all-expansions, .cp-members, .cp-note)")];
      if (deeper.length) more.append(...deeper);
      heading.after(section);
      if (deeper.length) section.after(more);
      heading.dataset.conceptPage = "ready";
      restoreWorkspaceFocus();
    } catch {
      // Keep the original concept map and its links usable if the resource cannot be loaded.
      heading.dataset.conceptPage = "unavailable";
    }
  }

  function prepareSources() {
    const list = main.querySelector(".sources-list");
    if (!list || main.querySelector(".atlas-source-search")) return;
    const sources = [...list.querySelectorAll(":scope > .source-block")];
    if (!sources.length) return;
    const section = document.createElement("section");
    section.className = "atlas-source-search";
    section.innerHTML = `<h2>출처에서 찾기</h2><label>제목이나 검토 내용
      <input type="search" placeholder="예: 분수, 관찰, 보고서"></label><p role="status"></p>`;
    const more = document.createElement("button");
    more.type = "button";
    more.className = "button atlas-source-more";
    more.textContent = "출처 더 보기";
    const input = section.querySelector("input");
    const searchable = sources.map((source) => source.textContent.toLocaleLowerCase("ko"));
    let limit = 12;
    function show() {
      const q = input.value.trim().toLocaleLowerCase("ko");
      let count = 0;
      sources.forEach((source, index) => {
        const match = searchable[index].includes(q);
        source.hidden = !match;
        if (match) count++;
        source.classList.toggle("atlas-source-later", match && count > limit);
      });
      section.querySelector('[role="status"]').textContent = count
        ? `${count}건 중 ${Math.min(count, limit)}건 표시` : "검색 결과가 없습니다. 다른 단어로 찾아보세요.";
      more.hidden = count <= limit;
    }
    input.addEventListener("input", () => { limit = 12; show(); });
    more.addEventListener("click", () => {
      const first = list.querySelector(".atlas-source-later:not([hidden])");
      limit += 12;
      show();
      if (first) focusSection(first.querySelector("h3") || first);
    });
    list.before(section);
    list.after(more);
    show();
  }

  function prepareToolNavigation() {
    const intro = main.querySelector(":scope > header");
    if (!intro || main.querySelector(".atlas-tool-jump")) return;
    const workbook = page === "inquiry-workbook";
    const headings = workbook
      ? [...main.querySelectorAll(":scope > .sheet > h2, :scope > footer > h2")]
      : [...main.querySelectorAll("#plot-heading, .summary .metric:first-child h2, .panel > h2:not(#plot-heading)")];
    if (!headings.length) return;
    const jump = document.createElement("nav");
    jump.className = "atlas-tool-jump";
    jump.setAttribute("aria-label", "도구에서 이동");
    const control = document.createElement("select");
    const label = document.createElement("label");
    label.append(workbook ? "기록지에서 볼 장" : "보고 싶은 항목", control);
    const sections = headings.map((heading, i) => {
      heading.id ||= (workbook ? "workbook-part-" : "lab-part-") + (i + 1);
      control.append(new Option(heading.textContent, heading.id));
      return heading.parentElement;
    });
    const button = document.createElement("button");
    button.className = "button";
    button.type = "button";
    button.textContent = "항목으로 이동";
    function show(focus) {
      const anchor = location.hash.slice(1);
      const index = headings.findIndex((heading, i) => heading.id === anchor
        || (workbook && anchor && sections[i].id === anchor));
      const active = index < 0 ? 0 : index;
      control.selectedIndex = active;
      if (workbook) {
        sections.forEach((section, i) => section.classList.toggle("workbook-inactive", i !== active));
        previous.hidden = active === 0;
        next.hidden = active === sections.length - 1;
        previous.href = "#" + headings[Math.max(active - 1, 0)].id;
        next.href = "#" + headings[Math.min(active + 1, headings.length - 1)].id;
        step.textContent = (active + 1) + " / " + headings.length;
      }
      if (focus && (index >= 0 || workbook)) focusSection(headings[active]);
    }
    button.addEventListener("click", () => {
      if (location.hash === "#" + control.value) focusSection(headings[control.selectedIndex]);
      else location.hash = control.value;
    });
    jump.append(label, button);
    intro.after(jump);
    let previous, next, step;
    if (workbook) {
      const pager = document.createElement("nav");
      pager.className = "atlas-workbook-pager screen-only";
      pager.setAttribute("aria-label", "기록지 항목 이동");
      previous = document.createElement("a");
      previous.textContent = "이전";
      next = document.createElement("a");
      next.textContent = "다음";
      step = document.createElement("span");
      pager.append(previous, step, next);
      main.append(pager);
    } else {
      const controls = ["df", "mode", "range"].map((id) => document.getElementById(id));
      const query = new URL(location.href).searchParams;
      controls.forEach((select) => {
        if ([...select.options].some((option) => option.value === query.get(select.id))) {
          select.value = query.get(select.id);
        }
      });
      controls[0].dispatchEvent(new Event("change"));
      function saveSettings() {
        const url = new URL(location.href);
        for (const select of controls) {
          const defaultValue = ([...select.options].find((option) => option.defaultSelected) || select.options[0]).value;
          if (select.value === defaultValue) url.searchParams.delete(select.id);
          else url.searchParams.set(select.id, select.value);
        }
        history.replaceState(history.state, "", url);
      }
      controls.forEach((select) => select.addEventListener("change", saveSettings));
      document.getElementById("reset").addEventListener("click", saveSettings);
    }
    show(Boolean(location.hash));
    window.addEventListener("hashchange", () => show(true));
  }

  function connectMain() {
    for (const label of main.querySelectorAll(".page-heading .eyebrow, .network-intro .eyebrow, .network-heading .eyebrow")) {
      if (/^[A-Z &-]+$/.test(label.textContent.trim())) label.hidden = true;
    }
    for (const link of main.querySelectorAll('a[href^="#view="]')) {
      const href = link.getAttribute("href");
      const params = new URLSearchParams(href.slice(1));
      const view = params.get("view");
      if (view === "catalog" || (view === "standard" && !params.has("section"))) {
        link.setAttribute("href", "./" + href);
      }
    }

    const params = route();
    const view = params.get("view");
    document.body.classList.toggle("atlas-local-scope", ["about", "standard"].includes(view)
      || Boolean(main.querySelector('form select[name="scope"]')));
    prepareHeading(params);
    updateNav();
    if (!tool && !main.hasAttribute("aria-busy")) {
      const heading = main.querySelector("h1");
      if (heading && !main.querySelector('[role="alert"]')) document.title = heading.textContent + " · 수학의 연결 지도";
    }
    prepareContextReturn();
    if (tool) prepareToolNavigation();
    if (!tool) {
      prepareReading(params);
      prepareStandardReturn(params);
      if (view === "network") prepareNetwork();
      if (view === "hierarchy") {
        prepareConceptIndex(params);
        prepareConceptPage(params);
      }
      if (view === "hierarchy" && params.get("mode") === "goals") {
        prepareGoals();
        if (main.querySelector(".gn-lanes")) preparePathwayActions();
      }
      if (view === "hierarchy" && params.get("mode") === "tasks") {
        prepareTasks(params);
        if (main.querySelector(".tp-official")) preparePathwayActions();
      }
    }
    const about = main.querySelector(".about-summary");
    if (about && !main.querySelector(".atlas-resources")) {
      const resources = document.createElement("section");
      resources.className = "atlas-resources";
      resources.innerHTML = `<h2>탐구 도구</h2><ul><li><a href="./distribution-lab.html"><strong>정규분포와 t분포 탐구</strong><span>자유도에 따른 곡선과 확률 비교</span></a></li><li><a href="./inquiry-workbook.html"><strong>수학 탐구 기록지</strong><span>탐구 계획·수행·성찰 기록과 인쇄</span></a></li></ul>`;
      about.after(resources);
    }
    if (about && !main.querySelector(".atlas-developer")) {
      const developer = document.createElement("section");
      developer.className = "about-summary atlas-developer";
      developer.innerHTML = `<h2>개발자 정보</h2>
        <div class="atlas-developer-links"><strong>이병민</strong>${developerLinks}
          <a href="https://github.com/ll7098ll/math-learning-atlas-kr">프로젝트 저장소</a>
        </div>`;
      main.append(developer);
    }
    if (about) prepareSources();
    restoreWorkspaceFocus();
    const intro = main.querySelector(".pathway-intro");
    if (intro && intro.parentElement.tagName !== "DETAILS") {
      const note = document.createElement("details");
      note.className = "atlas-explainer";
      const summary = document.createElement("summary");
      const title = intro.querySelector("strong");
      summary.textContent = title?.textContent || "자료의 범위";
      title?.remove();
      intro.before(note);
      note.append(summary, intro);
    }
  }

  updateNav();
  connectMain();
  let printGraph;
  let printGoalSummary;
  let printConceptBands = [];
  window.addEventListener("beforeprint", () => {
    if (!printConceptBands.length) {
      printConceptBands = [...main.querySelectorAll(".atlas-concept-band:not([open])")];
      printConceptBands.forEach((item) => { item.open = true; });
    }
    const closed = main.querySelector(".atlas-goal-summary:not([open])");
    if (closed) {
      printGoalSummary = closed;
      closed.open = true;
    }
    for (const select of main.querySelectorAll(".hierarchy-summary select, .hierarchy-kind select")) {
      const label = select.closest("label");
      if (label) label.dataset.atlasPrintSelection = select.selectedOptions[0]?.textContent.trim() || "";
    }
    const graph = main.querySelector(".atlas-svg");
    if (graph && !printGraph) {
      const box = graph.getBBox();
      if (box.width > 0 && box.height > 0) {
        printGraph = { graph, viewBox: graph.getAttribute("viewBox") };
        graph.setAttribute("viewBox", [box.x - 24, box.y - 36, box.width + 48, box.height + 60].join(" "));
      }
    }
  });
  window.addEventListener("afterprint", () => {
    printConceptBands.forEach((item) => { item.open = false; });
    printConceptBands = [];
    if (printGoalSummary) {
      printGoalSummary.open = false;
      printGoalSummary = undefined;
    }
    if (!printGraph) return;
    const { graph, viewBox } = printGraph;
    if (viewBox === null) graph.removeAttribute("viewBox");
    else graph.setAttribute("viewBox", viewBox);
    printGraph = undefined;
  });
  window.addEventListener("hashchange", updateNav);
  if (!tool) new MutationObserver(connectMain).observe(main, { childList: true, subtree: true, attributes: true, attributeFilter: ["data-ready-route"] });
})();
