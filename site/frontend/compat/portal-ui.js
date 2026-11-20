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

  const developerLinks = `<a href="mailto:ll7098ll@gmail.com">ll7098ll@gmail.com</a>
    <a href="https://github.com/ll7098ll">GitHub 프로필</a>`;
  const footer = document.createElement("footer");
  footer.className = "atlas-footer";
  footer.innerHTML = `<div><span><strong>수학의 연결 지도</strong><small>교육부 고시 제2022-33호 · 별책 8 수학과 교육과정</small></span>
    <div class="atlas-developer-links"><span>개발자 이병민</span>${developerLinks}<a href="./legacy.html#view=about">자료의 출처와 분석 기준</a></div></div>`;
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
    const mode = params.get("mode");
    if (view === "hierarchy" && ["goals", "tasks"].includes(mode) && main.querySelector(".gn-lanes, .tp-official")) {
      menu.setAttribute("aria-label", "목표와 과제 보기");
      const scope = params.get("scope") || "all";
      for (const [destination, label] of [["goals", "목표별 위계"], ["tasks", "과제와 조건"], ["", "개념군 목록"]]) {
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
      ["hierarchy", "", "개념군과 위계"],
      ["network", "", "전체 연결망"],
      ["overview", "flow", "개념 흐름"],
      ["overview", "structure", "학교급 구조"],
      ["overview", "expanded", "성취기준 펼쳐 보기"],
    ];
    const current = view === "overview"
      ? params.get("density") === "expanded" ? "expanded" : params.get("mode") || "flow"
      : view === "network" || view === "hierarchy" ? view : "";
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

  function prepareStandardReturn(params) {
    const view = params.get("view");
    const code = view === "network" ? params.get("node")
      : view === "connections" ? params.get("code")
      : view === "hierarchy" ? params.get("target") : "";
    const oldLink = main.querySelector(".atlas-return");
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
    link.className = "atlas-return";
    link.href = href;
    link.innerHTML = '<span aria-hidden="true">←</span> 성취기준 상세로';
    if (oldLink) oldLink.replaceWith(link);
    else heading.before(link);
  }

  function focusSection(element) {
    element.tabIndex = -1;
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
      caseSelect.value = available.includes(selectedCase) ? selectedCase : "";
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
      focusSection(article.querySelector("h2"));
    });
    listCases(params.get("taskCase"));
    const anchor = main.querySelector(".tp-goals") || articles[0].closest(".tp-previous-case") || articles[0];
    anchor.before(picker);
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
    if (!tool) {
      prepareReading(params);
      prepareStandardReturn(params);
      if (view === "network") prepareNetwork();
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
      about.before(resources);
    }
    if (about && !main.querySelector(".atlas-developer")) {
      const developer = document.createElement("section");
      developer.className = "about-summary atlas-developer";
      developer.innerHTML = `<h2>개발자 정보</h2>
        <div class="atlas-developer-links"><strong>이병민</strong>${developerLinks}
          <a href="https://github.com/ll7098ll/math-learning-atlas-kr">프로젝트 저장소</a>
        </div>`;
      about.after(developer);
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
