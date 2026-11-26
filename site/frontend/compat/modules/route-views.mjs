const workspaces = new Map([
  ["network", "network"], ["overview", "network"], ["connections", "network"],
  ["hierarchy", "hierarchy"], ["about", "about"],
]);
const readerViews = new Set(["catalog", "standard", "compare"]);

export function resolveView(hash, entry) {
  const params = new URLSearchParams(hash.replace(/^#/, ""));
  const requested = params.get("view");
  if (requested === "overview" && params.get("mode") !== "flow") {
    params.set("view", "catalog");
    params.set("list", "1");
    if (params.get("density") === "expanded") params.set("expand", "all");
    if (!params.get("band") && params.get("subject")) params.set("band", params.get("subject"));
    for (const key of ["mode", "density", "subject"]) params.delete(key);
    return { params, entry: "reader", menu: "catalog" };
  }
  const view = requested === "map" ? "catalog" : requested === "explore" ? "connections" : requested;
  const legacy = workspaces.has(view) || (view === "standard" && (entry === "legacy" || params.has("section")));
  const resolved = legacy || readerViews.has(view) ? view : entry === "legacy" ? "network" : "catalog";
  params.set("view", resolved);
  if (resolved === "catalog" && (entry === "legacy" || requested === "map")) params.set("list", "1");
  return {
    params,
    entry: workspaces.has(resolved) || legacy ? "legacy" : "reader",
    menu: workspaces.get(resolved) || (resolved === "standard" ? "catalog" : resolved),
  };
}
