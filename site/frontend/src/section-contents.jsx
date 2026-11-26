import React, { useEffect, useRef, useState } from "react";
import { ChevronDown } from "lucide-react";
import "./section-contents.css";

export function sectionHeading(id) {
  return document.getElementById(id)?.querySelector("h2, h3");
}

export function SectionContents({ items, label, title = "목차", linksId = "reading-jumps-links", hrefFor, onJump }) {
  const nav = useRef(null);
  const toggle = useRef(null);
  const chosen = useRef(null);
  const [expanded, setExpanded] = useState(false);
  const [active, setActive] = useState(items[0][0]);

  useEffect(() => {
    const outline = nav.current;
    const headings = items.map(([id]) => sectionHeading(id));
    let frame = 0;
    function update() {
      frame = 0;
      if (chosen.current === window.scrollY) return;
      chosen.current = null;
      const readingLine = outline.getBoundingClientRect().bottom + 24;
      const remaining = document.documentElement.scrollHeight - window.innerHeight - window.scrollY;
      const endProgress = 1 - Math.min(1, Math.max(0, remaining) / 64);
      const line = readingLine + Math.max(0, window.innerHeight / 2 - readingLine) * endProgress;
      const index = headings.findLastIndex((heading) => heading && heading.getBoundingClientRect().top <= line);
      setActive(items[Math.max(index, 0)][0]);
    }
    function schedule() {
      if (!frame) frame = requestAnimationFrame(update);
    }
    function resize() {
      chosen.current = null;
      schedule();
    }
    const observer = new ResizeObserver(schedule);
    observer.observe(outline.parentElement);
    observer.observe(outline);
    window.addEventListener("scroll", schedule, { passive: true });
    window.addEventListener("resize", resize);
    update();
    return () => {
      observer.disconnect();
      window.removeEventListener("scroll", schedule);
      window.removeEventListener("resize", resize);
      cancelAnimationFrame(frame);
    };
  }, [items]);

  function jump(event, id) {
    if (hrefFor) {
      onJump(event, id);
      if (event.defaultPrevented) setExpanded(false);
      return;
    }
    const heading = sectionHeading(id);
    if (!heading) return;
    heading.focus({ preventScroll: true });
    heading.scrollIntoView({ block: "start" });
    chosen.current = window.scrollY;
    setActive(id);
    setExpanded(false);
  }

  return <nav ref={nav} className="reading-jumps screen-only" aria-label={label} onKeyDown={(event) => {
    if (event.key !== "Escape" || !expanded) return;
    setExpanded(false);
    toggle.current.focus();
  }}>
    <button ref={toggle} className="reading-jumps-toggle" type="button"
      aria-controls={linksId} aria-expanded={expanded} onClick={() => setExpanded(!expanded)}>
      <strong>{title}</strong><span>{items.find(([id]) => id === active)?.[1] ?? items[0][1]}</span><ChevronDown size={17} aria-hidden="true" />
    </button>
    <ul id={linksId} className="reading-jumps-links" data-expanded={expanded}>
      {items.map(([id, name]) => {
        const attributes = { "aria-current": active === id ? "location" : undefined, onClick: (event) => jump(event, id) };
        return <li key={id}>{hrefFor ? <a href={hrefFor(id)} {...attributes}>{name}</a>
          : <button type="button" {...attributes}>{name}</button>}</li>;
      })}
    </ul>
  </nav>;
}
