import React from "react";
import { BookOpen, Waypoints } from "lucide-react";
import { scopeId, standardRoute } from "./curriculum";
import "./connection-preview.css";

// REV-4수01-12-1 connects equal partitions to a one-place decimal.
export function ConnectionPreview({ catalog, onOpen }) {
  const decimal = catalog.standards.find((s) => s.code === "4수01-12");
  if (!decimal) return null;
  return <a className="connection-preview" id="fraction-decimal-preview"
    href={standardRoute(decimal.code, scopeId(decimal))}
    onClick={(event) => onOpen(event, decimal.code)}
    aria-label={`분수와 소수의 연결 예시. 십분의 삼과 영 점 삼은 같은 양입니다. ${decimal.code} ${decimal.title} 성취기준 읽기`}>
    <div className="preview-heading">
      <span><Waypoints size={16} aria-hidden="true" /> 연결 예시</span>
      <span>{decimal.level} · {decimal.band}</span>
    </div>
    <div className="preview-math" aria-hidden="true">
      <div className="preview-fraction">
        <span className="preview-disc" />
        <span className="preview-notation"><span>3</span><span>10</span></span>
      </div>
      <span className="preview-equals">=</span>
      <div className="preview-decimal">
        <span className="preview-number">0.3</span>
        <span className="preview-ruler"><i>0</i><i>1</i></span>
      </div>
    </div>
    <div className="preview-caption">
      <strong>분수와 소수의 연결</strong>
      <span><BookOpen size={15} aria-hidden="true" />성취기준 읽기</span>
    </div>
  </a>;
}
