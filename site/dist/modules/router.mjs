import {resolveView} from './route-views.mjs';

export const parse = hash => resolveView(hash, 'legacy').params;
const snapshots=new Map();
export function setState(key,state){snapshots.set(key,state);try{sessionStorage.setItem('atlas-state:'+key,JSON.stringify(state));}catch{}}
export function saveState(key,root,focus,focusKey){
 const state={y:window.scrollY,open:[...root.querySelectorAll('details[data-open][open]')].map(d=>d.dataset.open),scrolls:Object.fromEntries([...root.querySelectorAll('[data-scroll-key]')].map(el=>[el.dataset.scrollKey,{x:el.scrollLeft,y:el.scrollTop}])),focus:focus||document.activeElement?.closest('[data-standard]')?.dataset.standard||snapshots.get(key)?.focus,focusKey:focusKey||document.activeElement?.dataset.focusKey||snapshots.get(key)?.focusKey};
 setState(key,state);
}
export function getState(key){if(snapshots.has(key))return snapshots.get(key);try{return JSON.parse(sessionStorage.getItem('atlas-state:'+key));}catch{return null;}}
