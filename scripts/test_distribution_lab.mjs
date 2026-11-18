import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import path from 'node:path';
import vm from 'node:vm';
const root=path.resolve(import.meta.dirname,'..');
const dist=process.argv[2]??(path.basename(root)==='research'?path.resolve(root,'../dist'):path.join(root,'tmp/pathways-release/dist'));
const html=await fs.readFile(path.join(dist,'distribution-lab.html'),'utf8');
const data=JSON.parse(html.match(/<script id="model-data" type="application\/json">(.*?)<\/script>/s)[1]);
const js=html.match(/<script>\s*([\s\S]*?)<\/script>/)[1];
const nodes=new Map();let downloaded,blob;
for(const id of ['model-data','df','mode','range','drawing','tails','central','status','boundary','moments','visible','chart-desc','comparison','reset','download'])nodes.set('#'+id,{value:'',textContent:'',innerHTML:'',listeners:{},addEventListener(type,f){this.listeners[type]=f;}});
nodes.get('#model-data').textContent=JSON.stringify(data);nodes.get('#df').value='5';nodes.get('#mode').value='tails';nodes.get('#range').value='5';
const doc={querySelector:s=>{assert(nodes.has(s),s);return nodes.get(s);},createElement:type=>{assert.equal(type,'a');return {click(){downloaded=this.download;}};}};
const context=vm.createContext({document:doc,Blob,URL:{createObjectURL(b){blob=b;return 'blob:test';},revokeObjectURL(){}},setTimeout:f=>f()});
vm.runInContext(js,context);let settings=0;
for(const df of [1,2,3,5,10,30,60])for(const mode of ['tails','central'])for(const extent of [5,15]){
 for(const [name,v] of Object.entries({df,mode,range:extent}))nodes.get('#'+name).value=String(v);
 nodes.get('#df').listeners.change();settings++;
 const row=data.student.find(r=>r.df===df),drawing=nodes.get('#drawing').innerHTML;
 assert(!/NaN|Infinity|undefined/.test(drawing));
 assert.equal((drawing.match(/class="normal"/g)??[]).length,1);assert.equal((drawing.match(/class="student"/g)??[]).length,1);
 assert(nodes.get('#tails').textContent.includes((row.tail2*100).toFixed(3)));
 assert(nodes.get('#central').textContent.includes(row.q975.toFixed(6)));
 assert.equal(Boolean(nodes.get('#boundary').textContent),mode==='central'&&row.q975>extent);
 assert.equal(nodes.get('#moments').textContent.includes('평균은 정의되지'),df===1);
 assert(nodes.get('#visible').textContent.includes('반올림'));
 assert.equal((nodes.get('#comparison').innerHTML.match(/<tr>/g)??[]).length,2);
 assert(nodes.get('#chart-desc').textContent.includes('같은 축'));
}
nodes.get('#reset').listeners.click();assert.deepEqual(['df','mode','range'].map(id=>nodes.get('#'+id).value),['5','tails','5']);
nodes.get('#download').listeners.click();assert.equal(downloaded,'normal-t-df5.csv');
const csv=(await blob.text()).trim().split('\n');assert.equal(csv.length,604);assert.equal(csv[0],'model,theoretical_not_observed');assert.equal(csv[2],'x,standard_normal_density,student_t_density');
for(const [i,line] of csv.slice(3).entries()){
 const vals=line.split(',').map(Number);assert(vals.every(Number.isFinite));assert.equal(vals[0],data.xs[i]);assert.equal(vals[1],data.normal.curve[i]);assert.equal(vals[2],data.student.find(r=>r.df===5).curve[i]);
}
console.log(JSON.stringify({status:'pass',distributionSettings:settings,csvCurveRows:601,reset:true,scope:'Executable page-script tests with a minimal DOM; not visual or real-browser download verification'}));
