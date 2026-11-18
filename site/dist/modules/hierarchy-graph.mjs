// Pure direction model: semantic links never become ordering constraints.
export function directionGraph(data, target, depth = 3) {
 const ids = new Set(data.nodes.map(n => typeof n === 'string' ? n : n.id));
 if (!ids.has(target)) throw new Error('등록되지 않은 목표입니다.');
 const edges = data.relations.filter(r => ids.has(r.from.slice(9)) && ids.has(r.to.slice(9)) && ['generalizes','requires_for_task'].includes(r.type) && r.review_state !== 'candidate');
 const forward = new Map([...ids].map(id => [id, []])), reverse = new Map([...ids].map(id => [id, []]));
 for (const r of edges) { forward.get(r.from.slice(9)).push(r); reverse.get(r.to.slice(9)).push(r); }
 // Tarjan detects arbitrary cycles, including self loops, before assigning levels.
 let sequence = 0;
 const positions = new Map(), low = new Map(), stack = [], active = new Set(), cycles = [];
 function visit(id) {
  positions.set(id, sequence); low.set(id, sequence++); stack.push(id); active.add(id);
  for (const edge of forward.get(id)) {
   const next = edge.to.slice(9);
   if (!positions.has(next)) { visit(next); low.set(id, Math.min(low.get(id), low.get(next))); }
   else if (active.has(next)) low.set(id, Math.min(low.get(id), positions.get(next)));
  }
  if (positions.get(id) === low.get(id)) {
   const component = []; let next;
   do { next = stack.pop(); active.delete(next); component.push(next); } while (next !== id);
   if (component.length > 1 || forward.get(id).some(r => r.to.slice(9) === id)) cycles.push(component);
  }
 }
 for (const id of ids) if (!positions.has(id)) visit(id);
 const cyclic = new Set(cycles.flat());
 const limit = depth === 'all' ? ids.size : Math.max(1, Math.min(10, Number(depth) || 3));
 function walk(adjacency, backwards) {
  const distances = new Map([[target, 0]]), paths = new Map([[target, []]]), queue = [target];
  for (let i = 0; i < queue.length; i++) {
   const id = queue[i], distance = distances.get(id);
   if (distance >= limit || cyclic.has(id)) continue;
   for (const edge of adjacency.get(id)) {
    const next = (backwards ? edge.from : edge.to).slice(9);
    if (cyclic.has(next) || distances.has(next)) continue;
    distances.set(next, distance + 1);
    paths.set(next, backwards ? [edge, ...paths.get(id)] : [...paths.get(id), edge]); queue.push(next);
   }
  }
  distances.delete(target); paths.delete(target);
  return { distances, paths };
 }
 const before = walk(reverse, true), after = walk(forward, false);
 const visible = new Set([target, ...before.distances.keys(), ...after.distances.keys()]);
 return { target, before, after, cycles, cyclic, edges: edges.filter(r => visible.has(r.from.slice(9)) && visible.has(r.to.slice(9))), depth: limit };
}
