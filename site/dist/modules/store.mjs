export const levels=['초등학교','중학교','고등학교'];
export const categories=['공통','일반 선택','진로 선택','융합 선택'];
export const scopes={all:levels,e:[levels[0]],m:[levels[1]],h:[levels[2]],em:levels.slice(0,2),mh:levels.slice(1)};
export const types={meaning_connection:'의미 연결',generalizes:'의미 확장',contrasts:'대조',requires_for_task:'과제별 선수 조건',has_subskill:'하위 사고',representation_translation:'표현 전환',instructional_sequence:'수업 순서 제안',supports_learning:'학습 지원'};
export let catalog;
const cache=new Map();
async function json(path,policy='no-cache'){
 const res=await fetch(path,{cache:policy});if(!res.ok){if(res.status===404&&policy==='default')throw Object.assign(new Error('자료가 갱신되었습니다. 새로고침해 주세요.'),{needsReload:true});throw Object.assign(new Error('자료를 불러오지 못했습니다. 잠시 후 다시 시도해 주세요.'),{status:res.status});}return res.json();
}
export async function initialize(){catalog=await json('content/catalog.json');return catalog;}
async function content(path){
 const immutable=catalog.resourceRoot&&(path==='hierarchy'||path.startsWith('relations/')||(path.startsWith('concept-pathways/')||path.startsWith('task-pathways/')));
 if(!cache.has(path))cache.set(path,json((path.startsWith('concept-pathways/')||path.startsWith('task-pathways/'))?`content/${path}.json`:immutable?`${catalog.resourceRoot}${path}.json`:`content/${path}.json?v=${catalog.version}`,immutable?'default':'no-cache').then(d=>{if(d.version!==catalog.version)throw Object.assign(new Error('자료가 갱신되었습니다. 새로고침해 주세요.'),{needsReload:true});return d;}).catch(e=>{cache.delete(path);throw e;}));return cache.get(path);
}
export const detail=async code=>(await content('standards/'+encodeURIComponent(code))).analysis;
export const connections=()=>content('connections');
export async function sources(){
 try{return (await content('sources')).sources;}
 catch(error){
  if(error.status!==404)throw error;
  return (await connections()).sources;
 }
}
export const hierarchy=()=>content('hierarchy');
export const standardRelations=code=>content('relations/'+encodeURIComponent(code));
export async function standardConnections(code){
 const data=await standardRelations(code);
 return Array.isArray(data.sources)?data:{...data,sources:await sources()};
}
export const conceptFlows=()=>content('flows');
export const conceptPathwaysIndex=()=>content('concept-pathways-index');
function pathwayObjectPath(index,namespace,key){
 if(!index.files)return namespace+'/'+index.datasetVersion+'/'+key;
 const hash=index.files[key];if(!/^[a-f0-9]{64}$/.test(hash||''))throw new Error('자료 목록을 확인할 수 없습니다. 새로고침해 주세요.');
 return namespace+'/items/'+hash;
}
export async function conceptPathway(id){const index=await conceptPathwaysIndex();if(!index.groups.some(g=>g.id===id))throw Object.assign(new Error('등록되지 않은 개념군입니다. 수학 개념 목록에서 다시 선택해 주세요.'),{invalidSelection:true});return content(pathwayObjectPath(index,'concept-pathways',id));}
export async function hierarchyGraph(){const index=await conceptPathwaysIndex();return content(pathwayObjectPath(index,'concept-pathways','graph'));}
export const standard=code=>catalog.standards.find(s=>s.code===code);
export const band=s=>s.level==='고등학교'?s.subject:s.band;
export const inScope=(s,scope)=>!!s&&(scopes[scope]||levels).includes(s.level||s.school_level);
export function select(params){
 const q=(params.get('q')||'').trim().toLowerCase();
 return catalog.standards.filter(s=>inScope(s,params.get('scope'))&&(!params.get('band')||band(s)===params.get('band'))&&(!params.get('domain')||s.domain===params.get('domain'))&&(!params.get('category')||s.category===params.get('category'))&&(!q||[s.code,s.title,s.statement,s.subject,s.domain,s.searchTerms].join(' ').toLowerCase().includes(q)));
}
export function relationGroups(relations,code,scope='all',type=''){
 const groups=new Map();
 for(const r of relations){
  if(!r.from.startsWith('standard:')||!r.to.startsWith('standard:')||![r.from,r.to].includes('standard:'+code)||type&&r.type!==type)continue;
  const other=standard((r.from==='standard:'+code?r.to:r.from).slice(9));if(!inScope(other,scope))continue;
  const key=[r.from,r.to,r.type].join('|');if(!groups.has(key))groups.set(key,{other,records:[],type:r.type});groups.get(key).records.push(r);
 }
 return [...groups.values()].sort((a,b)=>levels.indexOf(a.other.level)-levels.indexOf(b.other.level)||a.other.code.localeCompare(b.other.code,'ko'));
}

export const taskPathwaysIndex=()=>content('task-pathways-index');
export async function taskPathway(code){const index=await taskPathwaysIndex();if(!index.codes.includes(code))throw Object.assign(new Error('등록되지 않은 목표입니다. 수학 개념 목록에서 다시 선택해 주세요.'),{invalidSelection:true});return content(pathwayObjectPath(index,'task-pathways',code));}
export async function goalNetwork(){
 const index=await taskPathwaysIndex(),hash=index.goalGraph?.hash;
 if(!/^[a-f0-9]{64}$/.test(hash||''))throw Object.assign(new Error('목표 위계 자료가 갱신되었습니다. 새로고침해 주세요.'),{needsReload:true});
 return content('task-pathways/items/'+hash);
}
