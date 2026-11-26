export const schools = [
  { id: "e", title: "초등학교", description: "1~2 · 3~4 · 5~6학년군" },
  { id: "m", title: "중학교", description: "1~3학년군" },
  { id: "h", title: "고등학교", description: "공통 · 일반 선택 · 진로 선택 · 융합 선택" },
];

export const categories = ["핵심 아이디어", "지식·이해", "과정·기능", "가치·태도"];
export const scopeId = (standard) => schools.find((school) => school.title === standard.level)?.id;
export const bandOf = (standard) => scopeId(standard) === "h" ? standard.subject : standard.band;
export const unique = (values) => [...new Set(values)];

export function inScope(standard, scope) {
  return !["e", "m", "h", "em", "mh"].includes(scope) || scope.includes(scopeId(standard));
}

export function selection(standards, scope, band, domain, category) {
  return standards.filter((s) => inScope(s, scope) && (!band || bandOf(s) === band)
    && (!domain || s.domain === domain) && (!category || s.category === category));
}

const normalize = (text) => text.normalize("NFKC").toLocaleLowerCase("ko")
  .replace(/[‐‑–−]/g, "-").replace(/[\[\]\s]/g, "");

export function search(standards, query) {
  const needle = normalize(query);
  if (!needle) return standards;
  const terms = query.trim().split(/\s+/).map(normalize).filter(Boolean);
  return standards.flatMap((s) => {
    const code = normalize(s.code);
    const haystack = [s.title, s.statement, s.domain, s.subject, s.level, bandOf(s), s.searchTerms || ""].map(normalize);
    const field = haystack.findIndex((value) => value.includes(needle));
    if (code === needle) return [{ s, rank: 0 }];
    if (code.includes(needle)) return [{ s, rank: 1 }];
    if (field >= 0) return [{ s, rank: field + 2 }];
    const fields = [code, ...haystack];
    return terms.length > 1 && terms.every((term) => fields.some((value) => value.includes(term)))
      ? [{ s, rank: fields.length + 2 }] : [];
  }).sort((a, b) => a.rank - b.rank).map(({ s }) => s);
}

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
