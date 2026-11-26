import React from "react";
import { ArrowRight, ArrowUpRight, Network } from "lucide-react";
import { oldRoute } from "./curriculum";
import "./connection-preview.css";

// L014 records the extension from natural-number quotients to signed rational numbers.
export function ConnectionPreview() {
  return <section className="map-preview" aria-labelledby="map-preview-title">
    <h2 id="map-preview-title"><Network aria-hidden="true" size={23} />수학 연결 지도</h2>
    <p>분수에서 유리수까지, 한 기준을 골라 다른 학년에서 어떻게 이어지는지 살펴보세요.</p>
    <div className="map-sample">
      <a id="map-start-fraction" href={oldRoute("network", { scope: "all", node: "6수01-10" })}><small>초등 5~6학년</small>나눗셈의 몫과 분수</a>
      <ArrowRight size={20} aria-label="개념의 확장" />
      <a id="map-start-rational" href={oldRoute("network", { scope: "all", node: "9수01-03" })}><small>중학교</small>양수·음수와 유리수</a>
    </div>
    <div className="map-preview-actions">
      <a id="home-map" href={oldRoute("network", { scope: "all" })}>학년·개념으로 지도 열기 <ArrowRight size={16} aria-hidden="true" /></a>
      <a id="fraction-decimal-preview" href={oldRoute("hierarchy", { concept: "fraction", scope: "em", mode: "expansion", target: "6수01-10", relation: "L014" })}>두 기준이 이어지는 이유 <ArrowUpRight size={15} aria-hidden="true" /></a>
    </div>
  </section>;
}
