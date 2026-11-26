export const schools = [
  { id: "e", title: "초등학교", description: "1~2 · 3~4 · 5~6학년군" },
  { id: "m", title: "중학교", description: "1~3학년군" },
  { id: "h", title: "고등학교", description: "공통 · 일반 선택 · 진로 선택 · 융합 선택" },
];

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

export function groupStandards(rows) {
  return schools.flatMap(({ title }) => {
    const schoolRows = rows.filter((standard) => standard.level === title);
    return unique(schoolRows.map(bandOf)).map((band) => {
      const bandRows = schoolRows.filter((standard) => bandOf(standard) === band);
      const domains = unique(bandRows.map((standard) => standard.domain)).map((domain) => ({
        name: domain, rows: bandRows.filter((standard) => standard.domain === domain),
      }));
      return { level: title, band, domains, count: bandRows.length };
    });
  });
}

export function catalogPageRows(matches, params) {
  const expanded = params.get("expand") === "all";
  if (expanded) return { expanded, page: 1, pageCount: 1, shown: matches, start: 0 };
  const pageSize = 24;
  const pageCount = Math.max(1, Math.ceil(matches.length / pageSize));
  const focusIndex = matches.findIndex((standard) => standard.code === params.get("focus"));
  const requested = Number.parseInt(params.get("page"), 10) || Math.floor(focusIndex / pageSize) + 1;
  const page = Math.max(1, Math.min(pageCount, requested));
  const start = (page - 1) * pageSize;
  return { expanded, page, pageCount, shown: matches.slice(start, start + pageSize), start };
}
