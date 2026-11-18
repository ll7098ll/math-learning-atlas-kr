import {esc} from './ui.mjs';

export function renderTaskResources(resources=[],references=[]){
 const downloads=resources.length?`<div class="tp-resources">${resources.map(resource=>`<a class="button" href="${esc(resource.path)}" download>${esc(resource.label)} ↓</a>`).join('')}</div>`:'';
 const links=references.filter(reference=>reference.url?.startsWith('https://'));
 return downloads+(links.length?`<p class="tp-note">참고 자료: ${links.map(reference=>`<a href="${esc(reference.url)}" target="_blank" rel="noopener noreferrer">${esc(reference.title)} ↗</a> (확인 ${esc(reference.accessed)})`).join(' · ')}</p>`:'');
}

function linearIntersection(v){
 const [xmin,xmax]=v.x_range,[ymin,ymax]=v.y_range;
 const X=x=>54+(x-xmin)/(xmax-xmin)*452,Y=y=>260-(y-ymin)/(ymax-ymin)*236;
 const colors=['#286c78','#b56836'];
 const grid=[],xStep=v.x_tick_step||1;
 for(let x=Math.ceil(xmin/xStep)*xStep;x<=xmax;x+=xStep)grid.push(`<line x1="${X(x)}" y1="24" x2="${X(x)}" y2="260" class="tp-plot-grid"/><text x="${X(x)}" y="281" text-anchor="middle">${x}</text>`);
 for(let y=Math.ceil(ymin);y<=ymax;y++)grid.push(`<line x1="54" y1="${Y(y)}" x2="506" y2="${Y(y)}" class="tp-plot-grid"/><text x="43" y="${Y(y)+4}" text-anchor="end">${y}</text>`);
 const lines=v.lines.map((line,i)=>`<line x1="${X(xmin)}" y1="${Y(line.slope*xmin+line.intercept)}" x2="${X(xmax)}" y2="${Y(line.slope*xmax+line.intercept)}" stroke="${colors[i%colors.length]}" stroke-width="3"/>`).join('');
 const [px,py]=v.intersection;
 return `<figure class="tp-visual"><figcaption>${esc(v.title)}</figcaption><div class="tp-plot-legend">${v.lines.map((line,i)=>`<span style="color:${colors[i%colors.length]}">${esc(line.label)}</span>`).join('')}</div><svg class="tp-wide-plot" viewBox="0 0 560 305" role="img" aria-label="${esc(v.lines.map(line=>line.label).join(' 및 '))}의 교점 (${esc(px)},${esc(py)})">${grid.join('')}<line x1="54" y1="${Y(0)}" x2="506" y2="${Y(0)}" class="tp-plot-axis"/><line x1="${X(0)}" y1="24" x2="${X(0)}" y2="260" class="tp-plot-axis"/>${lines}<circle cx="${X(px)}" cy="${Y(py)}" r="5" fill="#99464b"/><text x="${X(px)+10}" y="${Y(py)-10}" font-weight="700">(${esc(px)}, ${esc(py)})</text><text x="520" y="${Y(0)+5}">${esc(v.x_label||'x')}</text><text x="${X(0)+8}" y="18">${esc(v.y_label||'y')}</text></svg><p>${esc(v.note)}</p></figure>`;
}

function boxplots(v){
 const [lo,hi]=v.range,X=x=>70+(x-lo)/(hi-lo)*440;
 const plots=v.groups.map((group,i)=>{
  const y=55+i*78,[min,q1,med,q3,max]=group.five_numbers;
  return `<text x="20" y="${y+5}" font-weight="700">${esc(group.label)}</text><line x1="${X(min)}" y1="${y}" x2="${X(max)}" y2="${y}" class="tp-box-line"/><line x1="${X(min)}" y1="${y-10}" x2="${X(min)}" y2="${y+10}" class="tp-box-line"/><line x1="${X(max)}" y1="${y-10}" x2="${X(max)}" y2="${y+10}" class="tp-box-line"/><rect x="${X(q1)}" y="${y-17}" width="${X(q3)-X(q1)}" height="34" class="tp-box-fill"/><line x1="${X(med)}" y1="${y-17}" x2="${X(med)}" y2="${y+17}" class="tp-box-median"/>${group.five_numbers.map(n=>`<text x="${X(n)}" y="${y-26}" text-anchor="middle">${esc(n)}</text>`).join('')}`;
 }).join('');
 const ticks=[];for(let n=Math.ceil(lo);n<=hi;n++)ticks.push(`<line x1="${X(n)}" y1="185" x2="${X(n)}" y2="192" class="tp-plot-axis"/><text x="${X(n)}" y="210" text-anchor="middle">${n}</text>`);
 return `<figure class="tp-visual"><figcaption>${esc(v.title)}</figcaption><svg class="tp-wide-plot" viewBox="0 0 560 235" role="img" aria-label="${esc(v.groups.map(g=>g.label+'의 최솟값·제1사분위수·중앙값·제3사분위수·최댓값은 '+g.five_numbers.join(', ')).join('; '))}">${plots}<line x1="70" y1="185" x2="510" y2="185" class="tp-plot-axis"/>${ticks.join('')}<text x="527" y="210">분</text></svg><p>${esc(v.note)}</p><div class="tp-plot-data">${v.groups.map(g=>`<p><strong>${esc(g.label)} 원자료 ${g.values.length}개:</strong> ${g.values.map(esc).join(', ')}</p>`).join('')}</div></figure>`;
}

function pythagorasTiles(v){
 const {a,b,c}=v,L=a+b,X=x=>80+320*x/L,Y=y=>45+320*y/L;
 const points=[[a,0],[L,a],[b,L],[0,b]];
 const corners=[[0,0],[L,0],[L,L],[0,L]];
 const polygon=ps=>ps.map(([x,y])=>`${X(x)},${Y(y)}`).join(' ');
 const triangles=corners.map((corner,i)=>`<polygon points="${polygon([corner,points[i],points[(i+3)%4]])}" fill="${i%2?'#dce9ed':'#e8e0cf'}" class="tp-tile-outline"/>`).join('');
 return `<figure class="tp-visual"><figcaption>${esc(v.title)}</figcaption><svg class="tp-wide-plot tp-tile-plot" viewBox="0 0 480 415" role="img" aria-label="한 변 ${esc(L)}인 정사각형 안에 넓이 ${esc(a*b/2)}인 직각삼각형 네 개와 한 변 ${esc(c)}, 넓이 ${esc(c*c)}인 가운데 정사각형이 있습니다.">${triangles}<polygon points="${polygon(points)}" class="tp-tile-center"/><text x="${X(a/2)}" y="28" text-anchor="middle">a=${esc(a)}</text><text x="${X(a+b/2)}" y="28" text-anchor="middle">b=${esc(b)}</text><text x="240" y="${Y(L/2)}" text-anchor="middle" font-weight="700">c²=${esc(c*c)}</text><text x="${X(a+b/2)+10}" y="${Y(a/2)-10}">c=${esc(c)}</text><text x="240" y="395" text-anchor="middle">a+b=${esc(L)}</text><path d="M${X(0)+15},${Y(0)}v15h-15" fill="none" class="tp-tile-outline"/><text x="${X(a/3)}" y="${Y(b/3)}" text-anchor="middle">ab/2</text></svg><p>${esc(v.note)}</p></figure>`;
}

export function renderExtraVisual(visual){
 if(visual.kind==='fixed_perimeter')return fixedPerimeter(visual);
 if(visual.kind==='image_matrix_panels')return imageMatrixPanels(visual);
 if(visual.kind==='loss_descent')return lossDescent(visual);
 if(visual.kind==='binomial_normal')return binomialNormal(visual);
 if(visual.kind==='statistics_summary')return statisticsSummary(visual);
 if(visual.kind==='distribution_curves')return distributionCurves(visual);
 if(visual.kind==='riemann_rectangles')return riemannRectangles(visual);
 if(visual.kind==='signed_linear_integral')return signedLinearIntegral(visual);
 if(visual.kind==='set_operations')return setOperations(visual);
 if(visual.kind==='matrix_product')return matrixProduct(visual);
 if(visual.kind==='pythagoras_tiles')return pythagorasTiles(visual);
 if(visual.kind==='linear_intersection')return linearIntersection(visual);
 if(visual.kind==='boxplots')return boxplots(visual);
 return '';
}

function fixedPerimeter(v){
 const panels=v.rectangles.map(({x,y})=>{
  const width=x*18,height=y*18,left=(220-width)/2,top=30+(162-height)/2;
  return `<section class="tp-set-panel"><h4>${esc(x)}cm × ${esc(y)}cm</h4><svg viewBox="0 0 220 225" role="img" aria-label="가로${esc(x)}cm,세로${esc(y)}cm. 둘레${esc(2*(x+y))}cm,넓이${esc(x*y)}cm²인 직사각형입니다."><rect x="${left}" y="${top}" width="${width}" height="${height}" fill="#d8eadc" stroke="#42755b" stroke-width="2"/><text x="110" y="${top-9}" text-anchor="middle">${esc(x)}</text><text x="${left+width+9}" y="${top+height/2+4}">${esc(y)}</text><text x="110" y="216" text-anchor="middle">넓이 ${esc(x*y)}cm² · 둘레 ${esc(2*(x+y))}cm</text></svg></section>`;
 }).join('');
 return `<figure class="tp-visual"><figcaption>${esc(v.title)}</figcaption><div class="tp-stat-panels">${panels}</div><p>${esc(v.note)}</p></figure>`;
}

function imageMatrixPanels(v){
 const panels=v.panels.map(panel=>{
  const rows=panel.values.length,cols=panel.values[0].length,cell=48;
  const cells=panel.values.map((row,i)=>row.map((value,j)=>`<rect x="${20+j*cell}" y="${15+i*cell}" width="${cell}" height="${cell}" fill="rgb(${value},${value},${value})" stroke="#71907d"/><text x="${44+j*cell}" y="${44+i*cell}" text-anchor="middle" style="fill:${value<128?'#fff':'#142a1b'}">${esc(value)}</text>`).join('')).join('');
  return `<section class="tp-set-panel"><h4>${esc(panel.label)}</h4><svg viewBox="0 0 ${40+cols*cell} ${30+rows*cell}" role="img" aria-label="${esc(panel.label)}: ${esc(panel.values.map(row=>row.join(', ')).join('; '))}">${cells}</svg></section>`;
 }).join('');
 return `<figure class="tp-visual"><figcaption>${esc(v.title)}</figcaption><div class="tp-stat-panels">${panels}</div><p>${esc(v.note)}</p></figure>`;
}

function lossDescent(v){
 const X=a=>60+(a+.2)/3.6*440,Y=l=>250-l*4.3;
 const curve=Array.from({length:121},(_,i)=>{const a=-.2+i*.03;return `${i?'L':'M'}${X(a)},${Y(14*a*a-46*a+38)}`;}).join('');
 const steps=v.steps.map((row,i)=>`<circle cx="${X(row.coefficient)}" cy="${Y(row.loss)}" r="${i<3?4:2.5}" fill="#b36b36"/>${i<3?`<text x="${X(row.coefficient)+8}" y="${Y(row.loss)-7}">${i}회</text>`:''}`).join('');
 const points=v.steps.map(row=>`${X(row.coefficient)},${Y(row.loss)}`).join(' ');
 const grid=[0,10,20,30,40,50].map(l=>`<path d="M60,${Y(l)}H500" stroke="#e3ebe5"/><text x="48" y="${Y(l)+4}" text-anchor="end">${l}</text>`).join('');
 return `<figure class="tp-visual"><figcaption>${esc(v.title)}</figcaption><svg class="tp-wide-plot" viewBox="0 0 560 305" role="img" aria-label="손실함수 L(a)=14a²−46a+38. 최소는 a=23/14에서 3/14이며, 학습률 1/56에서 0부터 갱신한 계수들이 최소점으로 접근합니다.">${grid}<path d="M60,20V250H510" fill="none" stroke="#829e8c"/><path d="${curve}" fill="none" stroke="#286b55" stroke-width="2.5"/><polyline points="${points}" fill="none" stroke="#b36b36" stroke-width="1.5" stroke-dasharray="4 3"/>${steps}<circle cx="${X(v.optimum)}" cy="${Y(v.minimum)}" r="4" fill="#315f77"/>${[0,1,2,3].map(a=>`<text x="${X(a)}" y="270" text-anchor="middle">${a}</text>`).join('')}<text x="518" y="270">a</text><text x="65" y="19">L(a)</text><text x="${X(v.optimum)}" y="292" text-anchor="middle">최소 a=23/14 · L=3/14</text></svg><p>${esc(v.note)}</p></figure>`;
}

function binomialNormal(v){
 const panels=v.panels.map(panel=>{
  const X=x=>30+(x+4)*28,Y=y=>185-y*320,id='tp-binomial-'+panel.n;
  const bars=panel.bins.filter(bin=>Math.abs(bin.center)<4.5).map(bin=>`<rect x="${X(bin.center-bin.width/2)}" y="${Y(bin.height)}" width="${28*bin.width}" height="${320*bin.height}" fill="#d0e3d6" stroke="#83a68d" stroke-width="0.5"/>`).join('');
  const curve=Array.from({length:101},(_,i)=>{const x=-4+i*.08,y=Math.exp(-x*x/2)/Math.sqrt(2*Math.PI);return `${i?'L':'M'}${X(x)},${Y(y)}`;}).join('');
  return `<section class="tp-set-panel"><h4>n=${esc(panel.n)} · p=0.5</h4><svg viewBox="0 0 280 220" role="img" aria-label="시행 수 ${esc(panel.n)}의 이항분포를 표준화한 막대와 표준정규 밀도 곡선입니다."><defs><clipPath id="${id}"><rect x="30" y="20" width="224" height="165"/></clipPath></defs><g clip-path="url(#${id})">${bars}<path d="${curve}" fill="none" stroke="#315f77" stroke-width="2"/></g><path d="M30,20V185H256" fill="none" stroke="#829e8c"/>${[-4,0,4].map(x=>`<text x="${X(x)}" y="204" text-anchor="middle">${x}</text>`).join('')}<text x="260" y="205">z</text><text x="35" y="18">표준화한 밀도</text></svg></section>`;
 }).join('');
 return `<figure class="tp-visual"><figcaption>${esc(v.title)}</figcaption><div class="tp-stat-panels">${panels}</div><p>${esc(v.note)}</p></figure>`;
}

function statisticsSummary(v){
 const categories=v.categories.map((item,i)=>{const x=65+105*i,h=item.count*1.1;return `<rect x="${x}" y="${180-h}" width="60" height="${h}" fill="#bcd9c6"/><text x="${x+30}" y="${172-h}" text-anchor="middle">${esc(item.count)}</text><text x="${x+30}" y="202" text-anchor="middle">${esc(item.label)}</text>`;}).join('');
 const bins=v.bins.map(item=>{const x=40+10*(item.lower-15),h=item.count*40;return `<rect x="${x}" y="${180-h}" width="50" height="${h}" fill="#d9e8df" stroke="#86ac95"/><text x="${x+25}" y="${172-h}" text-anchor="middle">${esc(item.count)}</text>`;}).join('');
 return `<figure class="tp-visual"><figcaption>${esc(v.title)}</figcaption><div class="tp-set-panels"><section class="tp-set-panel"><h4>재사용 응답 · 200개</h4><svg viewBox="0 0 290 225" role="img" aria-label="재사용 120개,미재사용 80개인 가상 범주형 응답의 막대그래프입니다."><path d="M40,25V180H265" fill="none" stroke="#829e8c"/>${categories}<text x="20" y="22">개</text><text x="30" y="184">0</text></svg></section><section class="tp-set-panel"><h4>보충 시간 · 9개</h4><svg viewBox="0 0 290 225" role="img" aria-label="가상 시간 자료의 15~20초,20~25초,25~30초,30~35초 계급 빈도는 1,3,3,2입니다. 왼쪽 경계 포함,오른쪽 경계 제외입니다."><path d="M40,25V180H255" fill="none" stroke="#829e8c"/>${bins}${[15,20,25,30,35].map(n=>`<text x="${40+10*(n-15)}" y="202" text-anchor="middle">${n}</text>`).join('')}<text x="260" y="203">초</text><text x="20" y="22">개</text><text x="30" y="184">0</text></svg></section></div><p>${esc(v.note)}</p></figure>`;
}

function distributionCurves(v){
 const colors=['#286b55','#b06438','#63749e'],X=x=>40+(x+4)*60,Y=y=>230-y*470;
 const grid=[0,.2,.4].map(y=>`<path d="M40,${Y(y)}H520" stroke="#e3ebe5"/><text x="32" y="${Y(y)+4}" text-anchor="end">${y}</text>`).join('');
 const curves=v.curves.map((curve,i)=>`<path d="${curve.points.map(([x,y],j)=>`${j?'L':'M'}${X(x)},${Y(y)}`).join('')}" fill="none" stroke="${colors[i]}" stroke-width="${i===2?2:2.5}" ${i===2?'stroke-dasharray="6 4"':''}/>`).join('');
 const legend=v.curves.map((curve,i)=>`<p><strong style="color:${colors[i]}">${esc(curve.label)}</strong> · 오른쪽 97.5% 임계값 ${esc(curve.critical.toFixed(3))}</p>`).join('');
 return `<figure class="tp-visual"><figcaption>${esc(v.title)}</figcaption><svg class="tp-wide-plot" viewBox="0 0 560 275" role="img" aria-label="0 중심의 대칭인 표준정규와 자유도 5,30의 t분포 곡선입니다. 자유도가 작은 t분포의 중심은 낮고 꼬리는 두껍습니다.">${grid}<path d="M40,30V230H530" fill="none" stroke="#829e8c"/>${curves}${[-4,-2,0,2,4].map(x=>`<text x="${X(x)}" y="250" text-anchor="middle">${x}</text>`).join('')}<text x="40" y="22">밀도</text><text x="540" y="250">x</text></svg><div class="tp-plot-data">${legend}</div><p>${esc(v.note)}</p></figure>`;
}

function riemannRectangles(v){
 const panels=v.partitions.map(n=>{
  const X=x=>35+210*x,Y=y=>200-165*y;
  const rects=Array.from({length:n},(_,i)=>`<rect x="${X(i/n)}" y="${Y(((i+1)/n)**2)}" width="${210/n}" height="${165*((i+1)/n)**2}" fill="#d2e6d8" stroke="#91b49b" stroke-width="0.7"/>`).join('');
  const curve=Array.from({length:61},(_,i)=>`${i?'L':'M'}${X(i/60)},${Y((i/60)**2)}`).join('');
  const left=(n-1)*(2*n-1)/(6*n*n),right=(n+1)*(2*n+1)/(6*n*n),number=x=>x.toFixed(5).replace(/0+$/,'').replace(/\.$/,'');
  return `<section class="tp-set-panel"><h4>n=${esc(n)} · 폭 1/${esc(n)}</h4><svg viewBox="0 0 280 235" role="img" aria-label="분할 수 ${esc(n)}, 오른쪽 끝점 직사각형 넓이 합 ${esc(number(right))}. 실제 넓이 1/3보다 큽니다.">${rects}<path d="M25,200H257M35,210V20" stroke="#829e8c" fill="none"/><path d="${curve}" stroke="#2d6550" stroke-width="2.5" fill="none"/><text x="29" y="218">0</text><text x="240" y="218">1</text><text x="259" y="202">x</text><text x="42" y="26">y=x²</text></svg><p>왼쪽 합 ${esc(number(left))}<br/>오른쪽 합 ${esc(number(right))}</p></section>`;
 }).join('');
 return `<figure class="tp-visual"><figcaption>${esc(v.title)}</figcaption><div class="tp-set-panels">${panels}</div><p>${esc(v.note)}</p></figure>`;
}

function signedLinearIntegral(v){
 const zero=-v.intercept/v.slope,X=x=>65+370*(x-v.start)/(v.end-v.start),Y=y=>125-75*y;
 const value=x=>v.slope*x+v.intercept;
 const polygon=(start,end)=>[[start,0],[start,value(start)],[end,value(end)],[end,0]].map(([x,y])=>`${X(x)},${Y(y)}`).join(' ');
 const number=x=>Number(x).toLocaleString('ko-KR',{maximumFractionDigits:3});
 return `<figure class="tp-visual"><figcaption>${esc(v.title)}</figcaption><svg class="tp-wide-plot" viewBox="0 0 500 265" role="img" aria-label="${esc(v.variable)}가 ${esc(v.start)}에서 ${esc(zero)}까지일 때 축 아래의 넓이는 ${esc(v.negative_area)}, ${esc(zero)}부터 ${esc(v.end)}까지 축 위의 넓이는 ${esc(v.positive_area)}입니다. 부호 있는 합은 ${esc(v.signed_total)}, 두 넓이의 합은 ${esc(v.total_area)}입니다."><polygon points="${polygon(v.start,zero)}" fill="#f0d5cc"/><polygon points="${polygon(zero,v.end)}" fill="#cfe6d5"/><path d="M45,125H460" stroke="#7b9184"/><path d="M${X(v.start)},${Y(value(v.start))}L${X(v.end)},${Y(value(v.end))}" stroke="#2e6653" stroke-width="3" fill="none"/>${[v.start,zero,v.end].map(x=>`<path d="M${X(x)},121v8" stroke="#7b9184"/><text x="${X(x)}" y="145" text-anchor="middle">${esc(number(x))}</text>`).join('')}<text x="470" y="130">${esc(v.variable)}</text><text x="${X((v.start+zero)/2)}" y="222" text-anchor="middle">음의 기여 −${esc(v.negative_area)}</text><text x="${X((zero+v.end)/2)}" y="35" text-anchor="middle">양의 기여 +${esc(v.positive_area)}</text><text x="250" y="252" text-anchor="middle">정적분 ${esc(v.signed_total)} · 넓이 합 ${esc(v.total_area)}</text></svg><p>${esc(v.note)}</p></figure>`;
}

function setOperations(v){
 const A=new Set(v.left),B=new Set(v.right),regions={a:v.universe.filter(x=>A.has(x)&&!B.has(x)),both:v.universe.filter(x=>A.has(x)&&B.has(x)),b:v.universe.filter(x=>!A.has(x)&&B.has(x)),neither:v.universe.filter(x=>!A.has(x)&&!B.has(x))};
 const values=xs=>xs.length?xs.map(esc).join(', '):'∅';
 const setText=xs=>xs.length?'{'+values(xs)+'}':'∅';
 const panels=v.operations.map((op,i)=>{
  const id=esc(v.key+'-'+i),fill=(a,b)=>{const selected=op.kind==='union'?a||b:op.kind==='intersection'?a&&b:op.kind==='difference'?a&&!b:!a;return selected?'#d8eadc':'#fff';};
  return `<section class="tp-set-panel"><h4>${esc(op.label)} <small>${setText(op.result)}</small></h4><svg viewBox="0 0 240 154" role="img" aria-label="${esc(op.label)}의 결과는 ${values(op.result)}입니다. 연두색 영역을 선택합니다."><defs><clipPath id="${id}-a"><circle cx="94" cy="82" r="48"/></clipPath><clipPath id="${id}-b"><circle cx="146" cy="82" r="48"/></clipPath><mask id="${id}-not-a" maskUnits="userSpaceOnUse" x="0" y="0" width="240" height="154"><rect width="240" height="154" fill="white"/><circle cx="94" cy="82" r="48" fill="black"/></mask><mask id="${id}-not-b" maskUnits="userSpaceOnUse" x="0" y="0" width="240" height="154"><rect width="240" height="154" fill="white"/><circle cx="146" cy="82" r="48" fill="black"/></mask></defs><rect x="18" y="15" width="206" height="134" rx="6" fill="${fill(false,false)}" stroke="#a7bcae"/><circle cx="94" cy="82" r="48" fill="${fill(true,false)}" mask="url(#${id}-not-b)"/><circle cx="146" cy="82" r="48" fill="${fill(false,true)}" mask="url(#${id}-not-a)"/><g clip-path="url(#${id}-a)"><circle cx="146" cy="82" r="48" fill="${fill(true,true)}"/></g><circle cx="94" cy="82" r="48" fill="none" stroke="#537b66"/><circle cx="146" cy="82" r="48" fill="none" stroke="#537b66"/><text x="27" y="31">U</text><text x="73" y="33">A</text><text x="162" y="33">B</text><text x="74" y="85" text-anchor="middle">${values(regions.a)}</text><text x="120" y="85" text-anchor="middle">${values(regions.both)}</text><text x="168" y="85" text-anchor="middle">${values(regions.b)}</text><text x="42" y="140">${values(regions.neither)}</text></svg></section>`;
 }).join('');
 return `<figure class="tp-visual"><figcaption>${esc(v.title)}</figcaption><p>전체집합 U=${setText(v.universe)} · A=${setText(v.left)} · B=${setText(v.right)}. 연두색 영역이 연산 결과입니다.</p><div class="tp-set-panels">${panels}</div></figure>`;
}

function matrixProduct(v){
 const table=m=>`<div class="tp-matrix"><table><caption>${esc(m.label)}</caption><thead><tr><th scope="col">대상</th>${m.columns.map(col=>`<th scope="col">${esc(col)}</th>`).join('')}</tr></thead><tbody>${m.values.map((row,i)=>`<tr><th scope="row">${esc(m.rows[i])}</th>${row.map(value=>`<td>${esc(value)}</td>`).join('')}</tr>`).join('')}</tbody></table></div>`;
 return `<figure class="tp-visual"><figcaption>${esc(v.title)}</figcaption><div class="tp-matrix-product">${table(v.left)}<span aria-hidden="true">×</span>${table(v.right)}<span aria-hidden="true">=</span>${table(v.result)}</div><p>${esc(v.note)}</p></figure>`;
}
