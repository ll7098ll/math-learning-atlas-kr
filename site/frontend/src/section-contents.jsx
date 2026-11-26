import React, { useLayoutEffect, useRef } from "react";
import { focusOutlineTarget, mountOutline } from "../compat/modules/section-outline.mjs";
import "../compat/atlas-outline.css";

export function sectionHeading(id) {
  return document.getElementById(id)?.querySelector("h2, h3");
}

export function SectionContents({ items, label, title = "목차", linksId = "reading-jumps-links", hrefFor, onJump }) {
  const nav = useRef(null);
  const callbacks = useRef({ hrefFor, onJump });
  callbacks.current = { hrefFor, onJump };
  const usesLinks = Boolean(hrefFor);

  useLayoutEffect(() => {
    const outline = mountOutline(nav.current, items.map(([id, name]) => ({
      title: name,
      href: callbacks.current.hrefFor?.(id),
      anchors: () => [sectionHeading(id)],
      jump: (event, bar) => {
        if (usesLinks) callbacks.current.onJump(event, id);
        else focusOutlineTarget(sectionHeading(id), bar);
      },
    })), { title, linksId });
    return outline.dispose;
  }, [items, title, linksId, usesLinks]);

  useLayoutEffect(() => {
    if (!hrefFor) return;
    // Keep focused outline links mounted when an asynchronous section is loaded.
    const links = nav.current.querySelectorAll(".reading-jumps-links a");
    items.forEach(([id], index) => links[index].setAttribute("href", hrefFor(id)));
  }, [hrefFor, items, title, linksId]);

  return <nav ref={nav} className="reading-jumps screen-only" aria-label={label} />;
}
