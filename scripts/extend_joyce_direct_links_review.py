"""Complete II.5's static content-link reading; do not claim recursive closure."""
import copy
from literature_review import ROOT,load_registry,build_report,digest,target_value
from extend_lt2_length_assets_review import load,sha,write
from record_scoped_pdf_research import inspect_html_assets
from relation_literature_review import FILE,claim_snapshot,relation_snapshot,apply_literature_context
from check_euclid_area_extensions import check
SOURCE='JOYCE_EUCLID_II5_HTML_UNDATED';DATE='2026-11-17'
CACHE=ROOT/'tmp/literature/joyce-direct-links-20261117'
PRIOR='data/literature_evidence/JOYCE_EUCLID_II5_prerequisites_review_notes.json'
PRIOR_SHA='045147b29df7b8c0e9e68b9161ed1a470a9373dba8fb2e4af1fb922281b22165'
PRIOR_BIB='84346c572af21237ff4ed79ee938f53146590c121bf1afbdf0c5bc7a94924532'
NOTES='data/literature_evidence/JOYCE_EUCLID_II5_direct_links_review_notes.json'
MANIFEST='data/literature_evidence/JOYCE_EUCLID_II5_direct_links_asset_manifest.json'
ASSET_SPEC=load(ROOT/MANIFEST)
BASE=ASSET_SPEC['asset_base_url'];URL=ASSET_SPEC['url']
LI='12수과02-01';DE='12수과02-04';PL='12수과03-01';RU='12수과03-02';OU='12수과03-03';RE='12수과03-04'
TITLE='Euclid II.5 and all ten static content-link targets, with four citation-check pages: Joyce online edition,15 HTML pages/25 embedded images; year unverified'
SCOPE='같은온라인II.5의기존7페이지·13그림에남은직접연결II.14·III.35·VI.25·VI.28과인용대조용I.9·I.10·V.19·VI.19의본문/Guide·그림12개를추가해누적15HTML페이지·25삽입그림을읽었다. II.5원바이트를현재응답과다시대조했고,그HTML의12개정적본문앵커가가리키는고유10개대상은모두읽기명세에포함된다. JavaScript가만드는탐색링크·2차이상전체연결·원론전권의완료는아니다. II.14닮음대안·VI.25/VI.28인용·정적그림의불일치와자체수학모형을구별한다.'
LIMITS='정적본문앵커10대상과별도인용대조4페이지까지의누적15페이지·25그림이다. 원어·다른번역·역사원전/원연구·모든2차연결·정의/공준의재귀적증명·동적애플릿/브라우저배치·실제컴퍼스수행·학생검증은미확인이다. II.14의원적문제·I.9의삼등분불가능성역사와V.19삽입설은이온라인해설을읽은것이며원논문/역사증거를독립검증한것이아니다. 자체좌표·등식·반례를역사도형의실측·학생자료로바꾸지않는다.'

def c(n,codes,paths,support,limit):return dict(id=f'JDL17-{n:02d}',source_id=SOURCE,role='mathematical_explanation',standard_codes=codes,locations=[BASE+p for p in paths],support=support,does_not_establish=limit,independent_review=False,student_validated=False)
CLAIMS=[
 c(1,[LI,RU],['bookII/propII14.html'],'II.14의정사각형화는직사각형넓이ab와같은넓이를갖는변√(ab)를구하는일이다. 본문의II.5·I.47을이용한차의제곱논증과Guide의닮음대안을구별한다. 닮음대안에서추가할선은BH·FH이며대응순서를맞추면△BFH∼△BHE∼△HFE다.','Guide에적힌BH·BF와HGE를그대로옮기지않는다. 9×4의자체좌표예에서EH=6,GE=5/2이며HGE는앞의삼각형들과일반적으로닮지않는다. 정사각형화는같은넓이이며합동·같은변·산술평균을뜻하지않는다. 원적문제의역사·불가능성원증명을검토한것은아니다.'),
 c(2,[LI],['bookVI/propVI25.html','bookV/propV19.html','bookVI/propVI19.html','bookVI/propVI28.html','bookI/propI9.html','bookI/propI10.html'],'인용번호와실제연결내용을함께대조한다. VI.25의세비례선분과닮은도형넓이를연결하는문장은VI.19의따름정리에맞으며,페이지의V.19따름정리링크는다른비례변환이다. VI.28의AB이등분은선분을이등분하는I.10과대조하고각을이등분하는I.9와구별한다.','V.19의비례변환이나I.9의작도자체가틀렸다는뜻이아니다. I.10은그증명에서I.9를사용하지만선분이등분을인용하는직접명제는I.10이다. 원사이트의수정·다른번역·모든인용의전수검증을확보한것은아니다.'),
 c(3,[RU,OU,RE],['bookVI/propVI25.html','bookVI/propVI28.html','bookVI/propVI19.html'],'VI.25의같은넓이·닮은모양조건과VI.28의닮은나머지도형조건을분리한다. 정사각형나머지일때의A=x(a−x)와0<A≤a²/4를모든모양에그대로적용하지않는다. 고정된가로:세로2:1직사각형나머지의자체모형은A=(1/2)x(a−x)이고최댓값은a²/8이다.','길이비k와넓이비k²를구별하고각모형의양의길이·단위·방향·닮음조건을밝힌다. 이직각특수모형을모든비스듬한평행사변형의일반공식이나원문의좌표그대로라고소개하지않는다. a=10,A=20은정사각형나머지에서는가능하지만2:1모형의최대25/2를넘는다.'),
 c(4,[LI,RU],['bookIII/propIII35.html','bookII/propII5.html'],'III.35는원안에서만나는두현의분할길이곱을비교한다. 반지름R,교점의중심거리d에대해각곱은R²−d²로대조할수있다. 교점이중심인경우와한현만지름인경우도자체모형에서조건을나누어확인한다.','원밖의점에서측정한양의거리곱에R²−d²를그대로쓰지않는다. R=5,d=3의자체예에서8×2=4×4=16이며,원밖d=6의같은직선거리1×11=11은25−36=−11과다르다. 이수치예는모든경우의독립증명·III.36전체독해·학생수행검증을대신하지않는다.')]

def p(n,codes,q,e,i):return dict(id=f'JDL-P{n:02d}',standard_codes=codes,question=q,expected=e,interpretation=i,student_validated=False)
OBSERVATIONS=[
 p(1,[LI,RU],'II.14의자체좌표B=(0,0),E=(9,0),F=(13,0),G=(13/2,0),H=(9,6)에서어떤삼각형이닮았는가?','△BFH∼△BHE∼△HFE이며BE/EH=9/6=6/4=EH/EF다. HGE의직각변비는6/(5/2)=12/5로3/2와다르다. BF는이미지름이므로새로필요한선분은BH·FH다.','온라인Guide의문구·정적그림·자체상단반원좌표를구별한다. 원그림H의표시방향을그대로복사하거나원사이트를수정했다고하지않는다.'),
 p(2,[DE,RU],'9×4직사각형과넓이가같은정사각형의변은(9+4)/2인가?','변은√36=6이고넓이는36이다. 산술평균13/2를변으로쓰면넓이는169/4다. 원래직사각형과새정사각형은넓이는같지만합동이아니다.','길이와넓이,산술평균과기하평균을구별하는자체설계예다. 도형변환의코드·작도나사용성/학습효과를실제로검증한결과가아니다.'),
 p(3,[LI],'VI.25의V.19따름정리링크와VI.19따름정리,VI.28의I.9와I.10을어떻게대조할까?','각대상페이지의명제·따름정리를읽는다. 세비례선분과닮은도형넓이에맞는것은VI.19따름정리다. 선분AB이등분의직접작도는I.10이며각이등분I.9는그작도증명에사용된다. 인용된명제자체와잘못연결한위치를구별한다.','인용번호하나의오류로저작전체를부정하지않고,원사이트·다른판본이정정됐다고하지않는다.'),
 p(4,[RU,OU],'변3,4,5인직각삼각형의넓이6을같은모양으로24로만들려면변을몇배해야하는가?','넓이비는4지만변의배율은2다. 변6,8,10의넓이는24이며,변을4배한12,16,20의넓이는96이다.','닮음비와넓이비를구별하는자체수치모형이다. VI.25의일반다각형작도·전체비례이론의재귀적검증이나실제학생자료는아니다.'),
 p(5,[PL,RU,OU,RE],'a=10에서넓이20을만들때정사각형나머지와가로:세로2:1직사각형나머지는같은조건인가?','아니다. 정사각형모형은A=x(10−x)≤25이므로20을허용한다.2:1모형은A=(1/2)x(10−x)≤25/2이므로20을허용하지않는다.0<x<10과닮음/방향·넓이단위를계획에명시하고달라진범위를보고한다.','최대값·성립조건을설계가정과함께점검하는자체모형이다. 특수직각모형을모든평행사변형의일반증명으로바꾸지않는다.'),
 p(6,[RU,OU,RE],'원x²+y²=25에서교점E=(3,0)을지나는가로현과세로현의분할길이곱을비교하라. 원밖E=(6,0)은어떤가?','원안에서는가로길이8,2와세로길이4,4의곱이모두16=25−9다. 원밖의가로직선거리1,11의양의곱은11이고25−36=−11과다르므로원안조건을그대로옮기지않는다.','가로현만지름인경우와교점이중심인경우를구별한다. 실제측정이아닌자체좌표계산이며이예몇개를모든현의증명으로쓰지않는다.'),
 p(7,[LI,RU],'II.5해설의곱c²와VI.28직각특수모형의곱C를같은입력으로처리해도되는가?','기호의정의를확인한다. c가길이라면c²는넓이이고C는이미주어진넓이일수있다. 예컨대변c=4의정사각형넓이16을C=16으로옮기며C를다시제곱해256으로바꾸지않는다.','현대해설·자기모형의변수와단위를기록한다. 두페이지에같은문자가나온다는사실만으로뜻이나조건이같다고단정하지않는다.'),
 p(8,[LI],'II.5의정적본문링크대상을모두읽었으니전권의전제·역사서술·애플릿까지확인한것인가?','아니다. 현재같은HTML의12앵커가가리키는10고유본문대상은읽었고,인용대조4페이지를별도로추가했다. 누적15페이지·25그림이며스크립트탐색메뉴·2차이상전체연결·다른번역·역사원전·동적작동과실제수행은다른범위다.','직접본문링크의유한범위를마친일과전체사용자목표의완료를구별한다. 이전7페이지·13그림의읽기이력은그대로보존한다.')]
UPDATED_OBSERVATIONS={
 'INQ-P27':dict(expected='최초II.5본문/Guide·그림4개,후속선정6페이지·그림9개,추가직접연결/인용대조8페이지·그림12개를날짜와해시로구별한다. 누적15페이지·25그림이며footer연도를현재발행연도로확정하지않는다.',interpretation='정적본문앵커의10고유대상을읽었지만원론전권·원어·다른번역·모든2차연결·애플릿작동·문헌전수검토의완료는아니다.'),
 'INQ-P34':dict(expected='이전선정6페이지대조의이력을보존하고,II.14·III.35·VI.25·VI.28과인용대조I.9·I.10·V.19·VI.19를추가한범위를따로기록한다. 남은2차연결·역사원전·다른판본·실제수행의미확인을명시한다.',interpretation='정적본문앵커대상읽기와원전전권의기반증명·번역비교·실제학습효과를구별한다.'),
 'JEF-P09':dict(expected='최초II.5·그림4개와이전선정6페이지·새그림9개의날짜/해시를보존한다. 추가직접연결4페이지·인용대조4페이지와새그림12개는다음읽기이력으로남긴다. 현재누적15페이지·25그림을새책15권으로세지않는다.')}
INTERPRETATIONS={}
for rid in ['SEC_12수과02-01_C04','REV-12수과02-01-1']:
 INTERPRETATIONS[rid,'JDL17-01']=('activity_context','문헌의도형이름·닮음대응·기하평균과넓이를자기계산에대조한다.','산술평균·같은넓이·합동을혼합하지않고Guide의HGE및이미있는BF를그대로옮기지않는다. 자체반례는전체원전증명이나학생수행의확인이아니다.')
 INTERPRETATIONS[rid,'JDL17-04']=('activity_context','원의안쪽교점조건과길이곱·단위를자기탐구의계산과논증에대조한다.','원밖의양의거리곱에R²−d²를그대로쓰지않고원문의조건과자체좌표예를나눈다. 실제작도·전체일반증명·학생검증을확보한것은아니다.')
for rid in ['SEC_12수과03-02_C04','SEC_12수과03-03_C04','REV-12수과03-04-1','HP-inquiry-presentation','HP-inquiry-reflection']:
 INTERPRETATIONS[rid,'JDL17-03']=('activity_context','닮음비·넓이비·나머지도형의조건을실제계산·발표·성찰에서명시하고특수모형과일반화를구별한다.','정사각형의최대조건을2:1직사각형이나모든평행사변형에그대로쓰지않는다. 자체계산·가상반례는실제학습효과의근거가아니다.')

def main():
 registry=load_registry();newids={x['id'] for x in CLAIMS};known={x['id'] for x in registry['claims']}
 if newids<=known:
  assert registry['sources'][SOURCE]['snapshot_file']==NOTES;build_report();return
 assert not newids&known and check()['status']=='pass'
 s=registry['sources'][SOURCE];assert s['snapshot_file']==PRIOR and s['snapshot_sha256']==PRIOR_SHA and s['bibliography_snapshot']==PRIOR_BIB and sha(ROOT/PRIOR)==PRIOR_SHA
 acquisition=load(CACHE/'acquisition.json');assert acquisition['text_read'] and acquisition['images_read'] and acquisition['new_text_pages_actually_read']==8 and acquisition['new_images_actually_viewed']==12
 html,images=inspect_html_assets(ASSET_SPEC,CACHE);old_notes=load(ROOT/PRIOR)
 assert len(html)==15 and len(images)==25 and images[:13]==old_notes['image_read_manifest']
 assert [{k:v for k,v in x.items() if k not in ['title','key']} for x in html[:7]]==[{k:v for k,v in x.items() if k not in ['title','key']} for x in old_notes['html_read_manifest']]
 boundary=acquisition['parent_static_content_links'];assert boundary['anchor_occurrences']==12 and len(boundary['unique_targets'])==10 and set(boundary['unique_targets'])<={x['url'] for x in html}
 old_source=copy.deepcopy(s);old_claims=[copy.deepcopy(x) for x in registry['claims'] if x['source_id']==SOURCE];old_obs=copy.deepcopy(s['observations']);assert len(old_claims)==9 and len(old_obs)==18
 assert not {x['id'] for x in OBSERVATIONS}&{x['id'] for source in registry['sources'].values() for x in source.get('observations',[])}
 relations=load(ROOT/'data/revised_relations.json')['relations'];pairs={(r['id'],c['id']) for r in relations for c in CLAIMS if all(r[k].startswith('standard:') for k in ['from','to']) and {r[k][9:] for k in ['from','to']}<=set(c['standard_codes'])};assert pairs==INTERPRETATIONS.keys() and len(pairs)==9
 reviewed=load(ROOT/FILE);old_ids={c['id'] for c in old_claims};old_rows=[copy.deepcopy(x) for x in reviewed['records'] if x['claim_id'] in old_ids];assert len(old_rows)==6
 bibliography=load(ROOT/'data/sources.json');entry=next(x for x in bibliography if x['id']==SOURCE);old_entry=copy.deepcopy(entry);entry.update(title=TITLE,review_scope=SCOPE,does_not_establish=LIMITS,next_review=LIMITS)
 empirical=copy.deepcopy(s['empirical_scope']);empirical['inference_limit']=LIMITS
 notes=copy.deepcopy(old_notes);notes.update(date=DATE,read_scope=SCOPE,html_read_manifest=html,image_read_manifest=images,empirical_scope=empirical,previous_review=old_source,previous_bibliography=old_entry,previous_claims=old_claims,previous_observations=old_obs,previous_relation_records=old_rows,previous_notes_file=PRIOR,previous_notes_sha256=PRIOR_SHA,
  reading_log=old_notes['reading_log']+['2026-11-17: 남은정적본문직접연결4페이지와인용대조4페이지·새그림12개를읽었다.'],
  direct_link_followup=dict(new_html_pages=8,new_inline_images=12,cumulative_html_pages=15,cumulative_inline_images=25,parent_static_content_links=boundary,all_parent_static_content_anchor_targets_read=True,recursive_prerequisite_closure_proved=False,history_originals_verified=False,page_layout_and_applet_verified=False,own_math_not_student_data=True,rereviewed_prior_claims=9,rereviewed_prior_tasks=3,rereviewed_prior_relation_snapshots=6))
 notes['source_corrections']+= [
  dict(location='II.14 Guide, alternate proof',issue='BH/BF·HGE표기를BH/FH·대응순서BFH–BHE–HFE와대조한다.'),
  dict(location='II.14 static GIF',issue='표시된반원은BF위쪽인데정적그림H는아래쪽에놓여본문의DE를E방향으로연장해반원과만나는설명과맞지않는다. 자체좌표에서는위쪽H를쓰며원정적그림·동적작동의상태를구별한다.'),
  dict(location='VI.25 V.19,Cor href',issue='V.19따름정리의비례변환과VI.19따름정리의세비례선분/닮은도형넓이를직접대조한다. 해당문장에맞는인용은VI.19따름정리다.'),
  dict(location='VI.28 first bisection citation',issue='I.9는각이등분,I.10은선분이등분이다. AB이등분의직접작도를I.10과대조하되I.10증명에서I.9를사용한다는관계는보존한다.')]
 write(ROOT/NOTES,notes)
 s.update(date=DATE,snapshot_file=NOTES,snapshot_sha256=sha(ROOT/NOTES),snapshot_history=s.get('snapshot_history',[])+[dict(snapshot_file=PRIOR,snapshot_sha256=PRIOR_SHA,date=old_source['date'],read_scope=old_source['read_scope'])],bibliography_snapshot=digest(entry),html_read_manifest=html,image_read_manifest=images,read_scope=SCOPE,limits=LIMITS,empirical_scope=empirical,method_note='남은직접본문4페이지·인용대조4페이지·새그림12개를읽고부모HTML과정적본문앵커10대상의포함을확인했다. 전체2차연결·원어/역사원전·동적작동·실제수행은미확인이다.',editorial_action='같은출처에새수학근거4건·자체과제8개·관계대조9건을더했다. 기존9주장의범위·3과제설명·6관계스냅샷을명시적으로다시대조하고이전원기록을보존했다.',display={**s['display'],'title':TITLE})
 for obs in s['observations']:
  if obs['id'] in UPDATED_OBSERVATIONS:obs.update(UPDATED_OBSERVATIONS[obs['id']])
 s['observations']+=copy.deepcopy(OBSERVATIONS)
 for claim in registry['claims']:
  if claim['source_id']==SOURCE:claim['empirical_scope']=copy.deepcopy(empirical)
 for claim in copy.deepcopy(CLAIMS):
  claim.update(empirical_scope=copy.deepcopy(empirical),target_snapshots={f'revision:{code}':digest(target_value(f'revision:{code}')) for code in claim['standard_codes']});registry['claims'].append(claim)
 by_claim={x['id']:x for x in registry['claims']};by_relation={x['id']:x for x in relations}
 for row in reviewed['records']:
  if row['claim_id'] in old_ids:row['claim_snapshot']=claim_snapshot(by_claim[row['claim_id']],s)
 for (rid,cid),(role,finding,limit) in INTERPRETATIONS.items():reviewed['records'].append(dict(relation_id=rid,claim_id=cid,role=role,finding=finding,limit=limit,relation_snapshot=relation_snapshot(by_relation[rid]),claim_snapshot=claim_snapshot(by_claim[cid],s)))
 apply_literature_context(relations,registry,registry=reviewed)
 queue=load(ROOT/'data/content_review_queue.json');row=next(x for x in queue['literature_review'] if x['source']['id']==SOURCE);row.update(source=entry,claim_ids=[x['id'] for x in registry['claims'] if x['source_id']==SOURCE])
 write(ROOT/'data/sources.json',bibliography);write(ROOT/'data/literature_claim_reviews.json',registry);write(ROOT/'data/content_review_queue.json',queue);write(ROOT/FILE,reviewed);build_report()
 print('Same Joyce source extended:8pages/12images,4claims/8tasks/9contexts;9prior claim scopes,3task explanations and6context snapshots explicitly rereviewed')

if __name__=='__main__':main()
