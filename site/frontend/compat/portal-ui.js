(() => {
  const main = document.querySelector("main");
  if (!main) return;

  document.body.classList.add("atlas-compat");
  const file = location.pathname.split("/").pop();
  const tool = file === "distribution-lab.html" || file === "inquiry-workbook.html";
  document.body.classList.toggle("atlas-tool", tool);
  main.id ||= "main";
  main.tabIndex = -1;

  const nav = [
    ["catalog", "교육과정 탐색", "./#view=catalog"],
    ["compare", "비교", "./#view=compare"],
    ["hierarchy", "연결 지도", "./legacy.html#view=hierarchy"],
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

  const footer = document.createElement("footer");
  footer.className = "atlas-footer";
  footer.innerHTML = `<div><span><strong>수학의 연결 지도</strong><small>교육부 고시 제2022-33호 · 별책 8 수학과 교육과정</small></span><a href="./legacy.html#view=about">자료의 출처와 분석 기준</a></div>`;
  const previousFooter = document.querySelector("body > .site-footer");
  if (previousFooter) previousFooter.replaceWith(footer);
  else main.after(footer);

  function route() {
    return new URLSearchParams(location.hash.slice(1));
  }

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
    if (!["hierarchy", "network", "overview", "connections", "explore"].includes(view)) return menu;
    menu.setAttribute("aria-label", "연결 지도 보기");
    const modes = [
      ["hierarchy", "", "개념군과 위계"],
      ["network", "", "전체 연결망"],
      ["overview", "flow", "개념 흐름"],
      ["overview", "structure", "학교급 구조"],
      ["overview", "expanded", "성취기준 펼쳐 보기"],
    ];
    const current = view === "overview"
      ? params.get("density") === "expanded" ? "expanded" : params.get("mode") || "flow"
      : view === "network" ? "network" : "hierarchy";
    for (const [target, mode, label] of modes) {
      const link = document.createElement("a");
      const values = new URLSearchParams({ view: target });
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
    if (tool || view === "standard" || view === "about") return;
    const menu = sectionNavigation(params);
    const oldMenu = main.querySelector(".atlas-path");
    if (oldMenu?.dataset.route === params.toString()) return;
    main.querySelectorAll(".overview-views").forEach((element) => { element.hidden = true; });
    menu.dataset.route = params.toString();
    if (oldMenu) oldMenu.replaceWith(menu);
    else if (menu.children.length) {
      const section = heading.closest(".atlas-page-header");
      section.after(menu);
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

  function updateNav() {
    const view = route().get("view");
    const current = tool || view === "about" ? "about"
      : ["standard", "catalog", "map"].includes(view) ? "catalog" : "hierarchy";
    for (const link of header.querySelectorAll("[data-atlas-nav]")) {
      if (link.dataset.atlasNav === current) link.setAttribute("aria-current", "page");
      else link.removeAttribute("aria-current");
    }
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
    if (!tool) prepareReading(params);
    const about = main.querySelector(".about-summary");
    if (about && !main.querySelector(".atlas-resources")) {
      const resources = document.createElement("section");
      resources.className = "atlas-resources";
      resources.innerHTML = `<h2>탐구 도구</h2><ul><li><a href="./distribution-lab.html"><strong>정규분포와 t분포 탐구</strong><span>자유도에 따른 곡선과 확률 비교</span></a></li><li><a href="./inquiry-workbook.html"><strong>수학 탐구 기록지</strong><span>탐구 계획·수행·성찰 기록과 인쇄</span></a></li></ul>`;
      about.before(resources);
    }
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
  window.addEventListener("beforeprint", () => {
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
    if (!printGraph) return;
    const { graph, viewBox } = printGraph;
    if (viewBox === null) graph.removeAttribute("viewBox");
    else graph.setAttribute("viewBox", viewBox);
    printGraph = undefined;
  });
  window.addEventListener("hashchange", updateNav);
  if (!tool) new MutationObserver(connectMain).observe(main, { childList: true, subtree: true });
})();
