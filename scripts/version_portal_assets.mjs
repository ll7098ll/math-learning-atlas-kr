// Resolve every browser module to its content version without changing Node imports.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {fileURLToPath} from 'node:url';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const site=path.basename(root)==='research'?path.dirname(root):path.join(root,'tmp/pathways-release');
const dist=path.join(site,'dist');
const hash=file=>crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex').slice(0,16);
const imports=Object.fromEntries(fs.readdirSync(path.join(dist,'modules')).filter(f=>f.endsWith('.mjs')).sort().map(f=>['./modules/'+f,'./modules/'+f+'?v='+hash(path.join(dist,'modules',f))]));
const file=path.join(dist,'index.html');
let html=fs.readFileSync(file,'utf8').replace(/<script type="importmap">[\s\S]*?<\/script>/g,'');
html=html.replace('<script type="module"',`<script type="importmap">${JSON.stringify({imports})}</script><script type="module"`);
html=html.replace(/(href|src)="([^"?]+\.(?:css|js))(?:\?[^"\s]*)?"/g,(match,attribute,name)=>fs.existsSync(path.join(dist,name))?`${attribute}="${name}?v=${hash(path.join(dist,name))}"`:match);
fs.writeFileSync(file,html,'utf8');
console.log(`Versioned ${Object.keys(imports).length} browser modules and entry assets`);
