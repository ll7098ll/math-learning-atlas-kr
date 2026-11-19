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
    for (const label of main.querySelectorAll(".page-heading .eyebrow, .network-heading .eyebrow")) {
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
      || Boolean(main.querySelector('.pathway-search select[name="scope"]')));
    const heading = main.querySelector("h1");
    if (!tool && heading && !main.querySelector(".atlas-path")) {
      const back = document.createElement("nav");
      back.className = "atlas-path";
      back.setAttribute("aria-label", "관련 화면");
      if (view === "standard") {
        params.delete("section");
        const link = document.createElement("a");
        link.href = "./#" + params;
        link.textContent = "성취기준 요약으로";
        back.append(link);
      } else if (["hierarchy", "network", "overview", "connections", "explore"].includes(view)) {
        back.innerHTML = `<a href="./legacy.html#view=hierarchy">개념군과 위계</a><a href="./legacy.html#view=network">전체 연결망</a><a href="./legacy.html#view=overview&amp;mode=structure">학교급 구조</a>`;
        const active = view === "network" ? 1 : view === "overview" && params.get("mode") === "structure" ? 2 : 0;
        back.children[active].setAttribute("aria-current", "page");
      }
      if (back.children.length) main.prepend(back);
    }
    const about = main.querySelector(".about-summary");
    if (about && !about.querySelector(".atlas-resources")) {
      const resources = document.createElement("section");
      resources.className = "atlas-resources";
      resources.innerHTML = `<h3>수업 자료와 탐구 도구</h3><div><a href="./distribution-lab.html">정규분포와 t분포 탐구</a><a href="./inquiry-workbook.html">수학 탐구 기록지</a></div>`;
      about.append(resources);
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
  window.addEventListener("hashchange", updateNav);
  if (!tool) new MutationObserver(connectMain).observe(main, { childList: true, subtree: true });
})();
