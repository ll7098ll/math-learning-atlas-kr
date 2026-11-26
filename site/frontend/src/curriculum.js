import { bandOf, selection, unique } from "../compat/modules/catalog-model.mjs";
export { bandOf, catalogPageRows, groupStandards, inScope, schools, scopeId, search, selection, unique } from "../compat/modules/catalog-model.mjs";

export const categories = ["핵심 아이디어", "지식·이해", "과정·기능", "가치·태도"];

export function route(view, params = {}) {
  return "#" + new URLSearchParams({
    view,
    ...Object.fromEntries(Object.entries(params).filter(([, value]) => value !== "" && value != null)),
  });
}

export function overviewRoute(standards, scope, band = "") {
  const bands = unique(selection(standards, scope).map(bandOf));
  return route("catalog", { scope, band: band || (bands.length === 1 ? bands[0] : ""), stage: "overview" });
}

export const oldRoute = (view, params) => "./legacy.html" + route(view, params);
export const standardRoute = (code, scope) => route("standard", { code, scope });

export function paramsFrom(hash) {
  const params = new URLSearchParams(hash.slice(1));
  if (!["catalog", "standard", "compare"].includes(params.get("view"))) params.set("view", "catalog");
  return params;
}

const resources = new Map();

export function readContent(path, version) {
  const key = path + (version ? "?v=" + encodeURIComponent(version) : "");
  if (!resources.has(key)) {
    const promise = fetch("./content/" + key, { cache: "no-cache" }).then((response) => {
      if (!response.ok) throw new Error("자료를 불러오지 못했습니다.");
      return response.json();
    }).then((data) => {
      if (version && data.version !== version) throw new Error("자료가 갱신되었습니다. 페이지를 새로고침해 주세요.");
      return data;
    }).catch((error) => {
      resources.delete(key);
      throw error;
    });
    resources.set(key, promise);
  }
  return resources.get(key);
}

export function pdfLink(page) {
  const source = document.getElementById("curriculum-source").href;
  return page ? source + "#page=" + page : source;
}
