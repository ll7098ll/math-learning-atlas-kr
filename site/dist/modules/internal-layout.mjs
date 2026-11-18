// Only authored directed relations define layers. Unconnected and cyclic
// criteria stay in an explicitly unordered lane, never a presumed base layer.
export function layoutInternalNetwork(model){
 const directed=model.edges.filter(e=>['generalizes','requires_for_task'].includes(e.type)&&e.records.some(r=>r.review_state==='self_checked'));
 const degree=new Map(model.nodes.map(n=>[n.code,0])),out=new Map(),touched=new Set(),rank=new Map();
 for(const e of directed){degree.set(e.to,degree.get(e.to)+1);if(!out.has(e.from))out.set(e.from,[]);out.get(e.from).push(e.to);touched.add(e.from);touched.add(e.to);}
 const queue=model.nodes.filter(n=>degree.get(n.code)===0&&touched.has(n.code)).map(n=>n.code);
 for(const id of queue)rank.set(id,0);
 for(let i=0;i<queue.length;i++)for(const next of out.get(queue[i])||[]){rank.set(next,Math.max(rank.get(next)||0,rank.get(queue[i])+1));degree.set(next,degree.get(next)-1);if(degree.get(next)===0)queue.push(next);}
 for(const [id,d] of degree)if(d>0)rank.delete(id);
 const max=Math.max(-1,...rank.values()),lanes=max+2,width=Math.max(1200,lanes*270+160);
 model.stages=Array.from({length:lanes},(_,i)=>({index:i,id:'internal-'+i,title:i<=max?'관계 단계 '+(i+1):'순서 미정',label:i<=max?'의미 확장·과제 조건의 상대 단계 '+(i+1):'방향 미기록 또는 순환 검토 대상',x:160+i*270,center:295+i*270,width:270,count:0}));
 let top=90;
 for(const band of model.bands){const cells=model.stages.map(()=>[]);for(const n of model.nodes.filter(n=>n.domain===band.domain)){n.stage=rank.has(n.code)?rank.get(n.code):max+1;cells[n.stage].push(n);model.stages[n.stage].count++;}
  band.y=top;band.height=60+Math.max(2,...cells.map(c=>Math.ceil(c.length/2)))*26;
  cells.forEach((cell,i)=>cell.forEach((n,j)=>{n.x=model.stages[i].x+50+(j%2)*120;n.y=top+44+Math.floor(j/2)*26;}));top+=band.height;
 }
 model.width=width;model.height=top+40;model.internal=true;return model;
}
