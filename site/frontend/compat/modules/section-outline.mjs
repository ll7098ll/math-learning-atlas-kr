function sectionTop(anchor, beside) {
  if (!anchor) return Infinity;
  const closed = anchor.parentElement?.closest("details:not([open])");
  const marker = closed?.querySelector(":scope > summary") || anchor;
  if (!marker.getClientRects().length) return Infinity;
  const rect = marker.getBoundingClientRect();
  if (beside) {
    const neighbor = beside.getBoundingClientRect();
    if ((neighbor.right <= rect.left || rect.right <= neighbor.left) && rect.top < neighbor.bottom) return neighbor.bottom;
  }
  return rect.top;
}

export function focusOutlineTarget(target, outline) {
  if (!target) return;
  if (!target.matches("summary, button, a[href], input, select, textarea, [tabindex]")) target.tabIndex = -1;
  if (outline) target.style.scrollMarginTop = outline.offsetHeight + 16 + "px";
  target.focus({ preventScroll: true });
  target.scrollIntoView({ block: "start" });
}

export function mountOutline(bar, entries, { title, linksId, container = bar.parentElement, trackScroll = true }) {
  const smallScreen = matchMedia("(max-width: 700px)");
  const updateLayout = () => bar.toggleAttribute("data-compact", smallScreen.matches || entries.length > 7);
  updateLayout();
  const toggle = document.createElement("button");
  toggle.type = "button";
  toggle.className = "reading-jumps-toggle";
  toggle.setAttribute("aria-controls", linksId);
  const label = document.createElement("strong");
  label.textContent = title;
  const current = document.createElement("span");
  toggle.append(label, current);

  const links = document.createElement("ul");
  links.id = linksId;
  links.className = "reading-jumps-links";
  bar.replaceChildren(toggle, links);

  let active;
  let chosenScroll;
  let frame = 0;
  function expand(open) {
    toggle.setAttribute("aria-expanded", String(open));
    links.dataset.expanded = String(open);
  }

  function select(index) {
    if (index === active || !controls[index]) return;
    controls[active]?.removeAttribute("aria-current");
    active = index;
    controls[index].setAttribute("aria-current", "location");
    current.textContent = entries[index].title;
  }

  const controls = entries.map((entry, index) => {
    const item = document.createElement("li");
    const link = document.createElement(entry.href ? "a" : "button");
    if (entry.href) link.setAttribute("href", entry.href);
    else link.type = "button";
    link.textContent = entry.title;
    link.addEventListener("click", (event) => {
      if (event.button !== 0 || event.altKey || event.ctrlKey || event.metaKey || event.shiftKey) return;
      expand(false);
      entry.jump(event, bar);
      chosenScroll = window.scrollY;
      select(index);
    });
    item.append(link);
    links.append(item);
    return link;
  });
  expand(false);
  select(0);
  toggle.addEventListener("click", () => expand(toggle.getAttribute("aria-expanded") === "false"));

  const controller = new AbortController();
  const signal = controller.signal;
  smallScreen.addEventListener("change", updateLayout, { signal });
  bar.addEventListener("keydown", (event) => {
    if (event.key !== "Escape" || toggle.getAttribute("aria-expanded") !== "true") return;
    expand(false);
    toggle.focus();
  }, { signal });

  function update() {
    frame = 0;
    if (!trackScroll || chosenScroll === window.scrollY) return;
    chosenScroll = undefined;
    const remaining = document.documentElement.scrollHeight - window.innerHeight - window.scrollY;
    const readingLine = bar.getBoundingClientRect().bottom + 24;
    const endProgress = 1 - Math.min(1, Math.max(0, remaining) / 64);
    const line = readingLine + Math.max(0, window.innerHeight / 2 - readingLine) * endProgress;
    let reached, upcoming;
    let latest = -Infinity;
    let earliest = Infinity;
    entries.forEach((entry, index) => {
      for (const anchor of entry.anchors()) {
        const top = sectionTop(anchor, entry.beside);
        if (top <= line && top > latest) {
          latest = top;
          reached = index;
        } else if (top > line && top < earliest) {
          earliest = top;
          upcoming = index;
        }
      }
    });
    select(reached ?? upcoming ?? 0);
  }

  function schedule() {
    if (trackScroll && !frame) frame = requestAnimationFrame(update);
  }
  window.addEventListener("scroll", schedule, { passive: true, signal });
  window.addEventListener("resize", () => { chosenScroll = undefined; schedule(); }, { signal });
  container.addEventListener("toggle", schedule, { capture: true, signal });
  container.addEventListener("focusin", (event) => {
    const index = entries.findIndex((entry) => entry.anchors().includes(event.target));
    if (index >= 0) {
      select(index);
      schedule();
    }
  }, { signal });
  const resize = new ResizeObserver(schedule);
  resize.observe(container);
  resize.observe(bar);
  update();
  return {
    bar, select, schedule,
    dispose() {
      controller.abort();
      resize.disconnect();
      cancelAnimationFrame(frame);
      bar.replaceChildren();
    },
  };
}
