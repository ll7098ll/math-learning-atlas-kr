import React, { useEffect, useState } from "react";
import { ChevronRight } from "lucide-react";
import { Button } from "@/components/ui/button";
import { pdfLink, readContent, standardRoute } from "./curriculum";

export function useContent(path, version) {
  const [request, setRequest] = useState({ attempt: 0 });
  const key = path + ":" + (version || "");
  useEffect(() => {
    if (!path) return;
    let mounted = true;
    readContent(path, version).then(
      (data) => { if (mounted) setRequest((state) => ({ ...state, key, data, error: null })); },
      (error) => { if (mounted) setRequest((state) => ({ ...state, key, data: null, error })); },
    );
    return () => { mounted = false; };
  }, [path, version, key, request.attempt]);

  return {
    data: request.key === key ? request.data : undefined,
    error: request.key === key ? request.error : undefined,
    retry: () => setRequest((state) => ({ key: null, attempt: state.attempt + 1 })),
  };
}

export function LoadState({ request, label }) {
  return request.error
    ? <div className="notice" role="alert"><p>{request.error.message}</p><Button onClick={request.retry}>다시 시도</Button></div>
    : <p className="notice" role="status">{label}</p>;
}

export function Pdf({ page, children }) {
  return <a className="text-link" href={pdfLink(page)} target="_blank" rel="noopener">{children}</a>;
}

export function StandardRow({ standard, onOpen, scope, idPrefix = "", compact = false }) {
  const s = standard;
  return <li className="standard-row">
    <a id={idPrefix + "std-" + s.code} href={standardRoute(s.code, scope)} data-standard-code={s.code}
      onClick={onOpen && ((event) => onOpen(event, s.code))}>
      <div className="standard-row-body">
        <h3>{s.title}</h3>
        <p className="row-location"><span className="standard-code">{s.code}</span>
          <span>{s.level} · {s.level === "고등학교" ? s.subject : s.band} · {s.domain}</span>
        </p>
        {!compact && <p className="row-statement"><span className="source-label">공식 성취기준</span>{s.statement}</p>}
      </div>
      <ChevronRight className="row-chevron" size={18} aria-hidden="true" />
    </a>
  </li>;
}
