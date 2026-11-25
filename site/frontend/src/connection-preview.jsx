import React from "react";
import { ArrowUpRight, BookOpen } from "lucide-react";
import { oldRoute } from "./curriculum";
import "./connection-preview.css";

// L014 records the extension from natural-number quotients to signed rational numbers.
export function ConnectionPreview() {
  return <a className="connection-preview" id="fraction-decimal-preview"
    href={oldRoute("hierarchy", { concept: "fraction", scope: "em", mode: "expansion", target: "6수01-10", relation: "L014" })}
    aria-label="초등학교에서 배운 분수, 중학교에서는? 십분의 삼을 영 점 삼으로 표현하는 그림. 초등 분수에서 중학교 유리수로 어떻게 이어지는지 보기">
    <div className="preview-heading">
      <span><BookOpen size={16} aria-hidden="true" />학년이 올라가면</span>
      <span>초등 · 중학교</span>
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
      <strong>초등학교에서 배운 분수, 중학교에서는?</strong>
      <span>분수·소수·유리수<ArrowUpRight size={16} aria-hidden="true" /></span>
    </div>
  </a>;
}
