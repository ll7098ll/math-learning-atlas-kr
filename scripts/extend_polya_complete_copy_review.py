"""Finish reading the available138-spread copy; publisher fidelity stays open."""
import copy
from literature_review import ROOT,load_registry,build_report,digest
from extend_lt2_length_assets_review import load,sha,write
from relation_literature_review import FILE,claim_snapshot,apply_literature_context
from record_polya_classroom_method_review import SOURCE,CACHE,SHA,URL,NI,LI,PL,RU,OU,RE
from check_polya_complete_copy_models import check
DATE='2026-11-18'
PRIOR='data/literature_evidence/POLYA_SECOND_EDITION_definition_induction_review_notes.json'
PRIOR_SHA='c4f4eada59819f5184571ea107feedc0876a3f0a6df510ad64207d1195dd5b3b'
PRIOR_BIB='39a14675773eb7c3a6fa45ec311a906d77dceb60e09a7ed9a3bd5296e482ca2d'
NOTES='data/literature_evidence/POLYA_SECOND_EDITION_complete_copy_review_notes.json'
TITLE='How to Solve It, second-edition public course scan — all138 PDF spreads read, Parts I–IV; actual printing/publisher fidelity unverified'
SCOPE='이전30/54/86PDF판면의기록과해시를보존하고PDF87–138의52판면을추가로직접읽어확보한사본138판면전체를읽었다. 대부분책두면스캔이며추출문/OCR은0쪽이다. 서지·서문·목차·질문목록·Introduction과Part I1–32,II33–36,III37–232,IV233–253의20문제·힌트·해답및Fig1–31이범위다. 목차PDF6–7을다시대조했다. 이는이사본전체의시각독해완료이며출판사직접원본과의동일성·실제인쇄연도·다른판본/정오표·인용원문·모든해답의독립재증명을마친것은아니다. Princeton공식발췌는별도출처로유지한다.'
LIMITS='교수조언·이상화대화·수학예제·회고/역사적일화의방법론적서술이며새실증표본·국내학생효과가아니다. 2판저작권1957·표시인쇄1971/1973·서문1944/1954/1956·스캔2006과미확정실제인쇄연도를구별한다. 사본138판면전체읽기와출판사원본/다른판본·공식정오표·Heath/고대원문·Stanford원문제/학술지원게재본·인용연구원자료의확인은별개다. 모든원해답을독립재증명하거나실제독립/학생·시각검증을확보하지않았다. 모형의정의역·시간구간·0인분모·높이발의내외부·실수/복소수근과중복도를명시하며경계/유한사례·유추/감정·차원검사만으로일반증명이나효과를확정하지않는다.'
CLAIM_LIMIT_ADDITIONS={
 'POLY18-01':'실제문제에서는모형화에쓴가정·무시한조건·근사오차와목적을명시한다. 가상의최종상태를그린것만으로실현가능성을증명하지않고역으로찾은절차를허용된정방향연산으로확인한다.',
 'POLY18-02':'휴식·무의식·동물의우회·재능/의욕에관한일화와비유를현대의인과연구·학생진단·검증된지원효과로세지않는다. 속담과질문목록도보편성공규칙이아니다.',
 'POLY18-03':'인쇄177의기울기몫은수평/수직대칭축과축위의점을따로확인한다. 배의최근접문제는시간범위·상대속도0을구별한다. Part IV10(b)의거리를변을포함하는직선까지로해석하면높이발이밑면밖일수있어내접원결론에는내부조건이필요하다. 변선분과지지직선을혼합하지않는다.',
 'POLY18-04':'정의역밖퇴화극한은유효한반례를찾는힌트이며원래정의역안의실제반례를제시한다. A이면B와B의참만으로A의참이증명되지않고확신의증가도주어진확률모형없이수치화하지않는다. 차원검사는상수나근사의유효범위를정하지못한다.',
 'POLYH18-01':'허용된부호·양의길이·분모·시간구간을변형전후에유지한다. 사다리꼴의보조삼각형은|b−d|<a−c<b+d를요구하며c=a경계의평행사변형은별도존재/유일성문제다.',
 'POLYH18-02':'숫자퍼즐의비음수십진정수와음수부호허용을구별한다. 인쇄220의n개근은복소수에서중복도를세는관례로명확히하고실근·서로다른근과구별한다. 정사각기둥의부피/겉넓이두조건이양의해하나만을정한다고가정하지않는다.'}

def p(n,codes,q,e,i):return dict(id=f'POLYC18-P{n:02d}',standard_codes=codes,question=q,expected=e,interpretation=i,student_validated=False)
OBSERVATIONS=[
 p(1,[LI,PL,RU],'0부터9까지각숫자를한번씩써서만든정수들의합이100일수없다는주장은음수부호를허용해도같은가?','비음수정수의십진표기라면각수는자리숫자합과9로나눈나머지가같아총합은45와합동이다.100은9의배수가아니므로불가능하다. 음수부호를허용하면70+9+8+6+5+3+2+1−4=100은각숫자를한번씩사용한다. 두해석의허용조건이다르다.','원문163–170의퍼즐/증명을수의범위와함께읽는다. 부호를허용한자체예는의도된비음수퍼즐의반례나실제학생오답이아니며생략한조건을명확히하는비교다.'),
 p(2,[LI,RU,OU],'직선대칭을(q−b)/(p−a)=−1/m으로만계산해도수평선·수직선·축위의점에항상적용되는가?','몫의분모와대칭축의표현범위를확인한다. Ax+By+C=0,A²+B²>0에서점R=(x,y)의대칭점은R−2(Ax+By+C)/(A²+B²)(A,B)이다. y=2에대한(3,5)는(3,−1),x=4에대한(6,−1)은(2,−1),축위(3,2)는그대로다.','인쇄177의표현을정의와예외조건에대조하는자체좌표과제다. 수선/중점조건을쓰며0으로나누는몫을형식적으로계산하지않는다. 실제측정·학습효과나모든판본의정오표가아니다.'),
 p(3,[RU,OU,RE],'정사각기둥의밑변x>0,높이y>0에서x²y=63,2x²+4xy=102를얻었다. x=3,y=7만보고해도되는가?','y=63/x²를대입하면(x−3)(x²+3x−42)=0이다. 양의밑변은3과(−3+√177)/2의두개다. 두번째높이는(93+3√177)/56이며두쌍모두원래부피/겉넓이를만족한다. 나머지밑변(−3−√177)/2는음의길이여서제외한다.','인쇄175–176은두조건의식세우기이며유일해를보장하지않는다. 정확한이차수체계산으로원식과양의범위를대조한자체과제다. 실수후보와기하학적해를구별하며학생자료가아니다.'),
 p(4,[PL,RU,OU,RE],'두점을배로모형화하여상대위치r0=(1,1),상대속도v=(1,0)일때수선거리1이현재이후의최소거리인가? 상대속도가0이면어떤가?','제곱거리는(1+t)²+1이다. 모든실수시간에서는t=−1의거리1이지만현재이후t≥0에서는t=0의√2가최소다. v≠0이면t*=max(0,−r0·v/|v|²)를쓰고v=0이면거리는항상|r0|로시간이하나로정해지지않는다.','인쇄193–196의상대운동/수선작도를시간범위와함께적용한자체점운동모형이다. 과거·미래/유한구간을혼합하거나실제항해안전지침·관측자료로제시하지않는다.'),
 p(5,[RU,OU,RE],'삼각형의내접반지름r,외접반지름R,가장긴높이H에대해r+R≤H를반박하려면퇴화극한만보이면되는가?','극한은실제반례를찾는힌트다. 변13,13,24인삼각형은삼각부등식을엄격히만족하고넓이는60이다. r=12/5,R=169/10,H=120/13이므로r+R=193/10>H다. 원래정의역안의비퇴화삼각형으로반박한다.','원문190–191은극한뒤거의180도인실제경우도언급한다. 자체유리수반례는원문의퇴화그림을유효한삼각형으로세지않도록하며실제학생자료나원문의틀린정리주장이아니다.'),
 p(6,[PL,RU,OU],'사다리꼴의두밑변a>c>0와다른변b,d를고정한채c를a까지늘려도항상같은조건의도형이존재하고하나로정해지는가?','보조삼각형의세변b,d,a−c는|b−d|<a−c<b+d를만족해야한다.10,4,5,5는높이4·넓이28이지만10,7,6,3은퇴화경계다. a=c일때는평행사변형이어서b=d가필요하며,밑변10·옆변5라도높이가4인경우넓이는40,높이가5인경우넓이는50으로여러해가가능하다.','인쇄211–213의변형을허용조건에대조한자체과제다. 보조문제의존재·경계에서의유일성을따로검토하며한특수예나불가능한연속변형을일반증명으로바꾸지않는다.'),
 p(7,[LI,RU,OU],'인쇄220의“n차방정식은정확히n개의근”을실수의서로다른근이n개라는뜻으로읽어도되는가?','대수학의기본정리는n≥1의복소수계수다항식에대해복소근을중복도와함께센다. x²+1은실근0개·복소근±i이고,(x−1)²은서로다른근1에중복도2다. 서로다른근이최대n개라는사실과낮은차수의예몇개만으로일반정리를증명한것은아니다.','원문의불완전증명예를체계·정의역·중복도와함께읽는다. 이과제는기본정리전체의독립증명이나모든학생에게복소수이론을요구하는근거가아니다.'),
 p(8,[RU,OU,RE],'공간좌표를쓰는경우:Part IV10(b)의거리를변을포함하는직선까지로해석하자. 밑면꼭짓점(0,0),(4,0),(0,3),꼭짓점(6,6,8)이각변직선까지같은거리에있으면높이발이내접원의중심인가?','높이발(6,6)은밑면밖이며x=0,y=0,3x+4y−12=0까지거리는모두6이다. 공간꼭짓점에서각직선까지의거리는√(6²+8²)=10이다. 그러나반지름6의원은내접원이아니라방접원이며두접점은변의연장선에놓인다. 내접원결론에는볼록밑면내부의높이발조건등이필요하다.','변선분과지지직선까지의거리를구별한자체반례다. 선분거리로해석하면이예의조건부터성립하지않음을밝힌다.245–246의동거리논증을내외부확인없이내접원결론으로옮기지않으며다른판본/공식정오표를확인한것은아니다.')]
UPDATED_OBSERVATIONS={'POLY18-P08':dict(expected='최초30/54/86판면기록은보존하고남은PDF87–138의52판면을직접읽어확보한사본138판면전체를읽었다. Part I1–32,II33–36,III37–232,IV233–253의20문제·힌트·해답과Fig1–31을확인했다. 추출문/OCR은0쪽이다.2판저작권1957·표시인쇄1971/1973·스캔2006·미확정실제인쇄연도를구별한다.',interpretation='완료는이사본전체의시각독해범위다. Princeton공식발췌와의판본동일성·출판사원본/정오표·인용원연구/역사원문·모든해답의독립재증명·실제독립/학생검증은별개이며이전읽기기록을덮어쓰지않는다.')}

def main():
 registry=load_registry();s=registry['sources'][SOURCE]
 if s['snapshot_file']==NOTES:build_report();return
 assert s['snapshot_file']==PRIOR and s['snapshot_sha256']==PRIOR_SHA and s['bibliography_snapshot']==PRIOR_BIB and sha(ROOT/PRIOR)==PRIOR_SHA and check()['status']=='pass'
 a=load(CACHE/'complete-copy-acquisition-20261118.json');assert a['source_pdf_sha256']==SHA and a['reading_completed'] and a['images_viewed'] and a['viewed_image_pages']==list(range(87,139)) and a['new_text_pages']==[] and not a['ocr_used'] and a['contents_mapping_verified'] and sha(CACHE/'polya-second-edition-university-course-copy.pdf')==SHA
 old_notes=load(ROOT/PRIOR);images={str(n):sha(CACHE/f'rendered/polya-{n}.png') for n in range(1,139)};assert {k:images[k] for k in old_notes['rendered_page_sha256']}==old_notes['rendered_page_sha256']
 old_source=copy.deepcopy(s);old_claims=[copy.deepcopy(x) for x in registry['claims'] if x['source_id']==SOURCE];old_obs=copy.deepcopy(s['observations']);assert len(old_claims)==6 and len(old_obs)==17
 assert not {x['id'] for x in OBSERVATIONS}&{x['id'] for v in registry['sources'].values() for x in v.get('observations',[])}
 reviewed=load(ROOT/FILE);ids={c['id'] for c in old_claims};old_rows=[copy.deepcopy(x) for x in reviewed['records'] if x['claim_id'] in ids];assert len(old_rows)==28
 bibliography=load(ROOT/'data/sources.json');entry=next(x for x in bibliography if x['id']==SOURCE);old_entry=copy.deepcopy(entry);entry.update(title=TITLE,review_scope=SCOPE,does_not_establish=LIMITS,next_review=LIMITS)
 empirical=copy.deepcopy(s['empirical_scope']);empirical['inference_limit']=LIMITS
 detail=copy.deepcopy(old_notes['classroom_method_scan_review']);detail.update(selected_pdf_pages=list(range(1,139)),part_iii_selected_printed_pages='37–232',part_iii_complete=True,part_iv_read=True,part_iv_printed_pages='233–253',definition_first_page_only=None,practical_problems_first_page_only=None,remaining_pdf_pages_without_visual_review=[],source_figures_viewed=list(range(1,32)),whole_book_read=True,whole_available_copy_read=True,complete_publisher_edition_verified=False,all_source_solutions_independently_reproved=False)
 notes=copy.deepcopy(old_notes);notes.update(date=DATE,read_scope=SCOPE,visual_pdf_pages=list(range(1,139)),rendered_page_sha256=images,empirical_scope=empirical,previous_review=old_source,previous_bibliography=old_entry,previous_claims=old_claims,previous_observations=old_obs,previous_relation_records=old_rows,previous_notes_file=PRIOR,previous_notes_sha256=PRIOR_SHA,classroom_method_scan_review=detail,
  reading_log=old_notes['reading_log']+['2026-11-18:남은PDF87–138의52판면을직접읽고목차6–7을대조했다. 사본138판면전체시각독해,추출문/OCR0쪽.'],prior_followup_sections_describe_their_own_dates_and_scopes=True,
  complete_copy_followup=dict(new_visual_pages=list(range(87,139)),new_text_pages=[],ocr_used=False,cumulative_visual_pages=138,whole_book_read=True,whole_available_copy_read=True,complete_publisher_edition_verified=False,part_iii_complete=True,part_iii_printed_pages='37–232',part_iv_read=True,part_iv_printed_pages='233–253',part_iv_problems=list(range(1,21)),part_iv_hints=list(range(1,21)),part_iv_solutions=list(range(1,21)),source_figures_viewed=list(range(1,32)),contents_rechecked_pdf_pages=[6,7],last_printed_page_observed=253,reading_notes=a['reading_notes'],new_claims=0,new_tasks=8,new_relation_entries=0,rereviewed_prior_claims=6,rereviewed_prior_tasks=1,rereviewed_prior_relation_snapshots=28,historical_originals_read=False,cited_originals_all_read=False,all_source_solutions_independently_reproved=False,actual_independent_review=0,actual_student_validation=0))
 notes['source_corrections'] += [dict(location='printed163–170,digit puzzle',issue='Unsigned nonnegative decimal domain is needed for the intended impossibility proof. If negative signs are allowed,the own signed example totals100 with digits0–9once. This is a domain comparison,not an erratum to the intended unsigned puzzle.'),dict(location='printed175–177,equations/reflection',issue='Two positive square-prism branches; slope quotients need horizontal/vertical/on-axis exceptions. Exact algebra/normal-vector formulation retains original conditions.'),dict(location='printed190–196,specialization',issue='Use a nondegenerate triangle as a counterexample after a limit heuristic; closest motion needs a time domain and relative-velocity-zero case.'),dict(location='printed211–213,trapezoid',issue='The auxiliary triangle requires strict feasibility inequalities. Equal-base boundary needs equal legs and does not retain uniqueness.'),dict(location='printed220,FTA',issue='Specify complex roots with multiplicity; do not identify all roots with distinct real roots or a partial argument with a full proof.'),dict(location='Part IV10(b),printed235/245–246',issue='Equal distances to supporting side-lines alone may give an excircle centered outside the base. Own explicit3Dexample shows need to distinguish segments/lines and add an interior-foot condition for the incircle conclusion. No official/all-edition erratum claimed.'),dict(location='Part IV1/6/12/14 and other examples',issue='Retain southern-pole model starts,center-point nonuniqueness,limiting versus executable motion,and both quartic parameter branches. Selected exact recalculations are not an exhaustive independent reproof of all20solutions.')]
 write(ROOT/NOTES,notes)
 s.update(date=DATE,snapshot_file=NOTES,snapshot_sha256=sha(ROOT/NOTES),snapshot_history=s.get('snapshot_history',[])+[dict(snapshot_file=PRIOR,snapshot_sha256=PRIOR_SHA,date=old_source['date'],read_scope=old_source['read_scope'])],bibliography_snapshot=digest(entry),read_scope=SCOPE,limits=LIMITS,empirical_scope=empirical,method_note='동일사본의남은52판면과목차를직접대조했다. 확보사본138판면전체시각독해완료·추출문/OCR0쪽이며출판사원본동일성/인용원문검증완료가아니다.',editorial_action='기존6주장의한계/위치·1과제설명·28관계근거스냅샷을다시대조하고원기록을보존했다. 자체과제8개를더하며새주장/관계해석은추가하지않았다.',display={**s['display'],'title':TITLE})
 for obs in s['observations']:
  if obs['id'] in UPDATED_OBSERVATIONS:obs.update(UPDATED_OBSERVATIONS[obs['id']])
 s['observations']+=copy.deepcopy(OBSERVATIONS)
 by_claim={c['id']:c for c in registry['claims']}
 locations={'POLY18-01':[87,88,90,97,117,118,125,126,127,128],'POLY18-02':[98,110,111,115,116,124,127,128],'POLY18-03':[99,100,108,109,110,130,134,135],'POLY18-04':[94,95,96,97,101,102,105,106,107,108,113,114,120,121,122],'POLYH18-01':[100,109,110,117,118,125,126,127,130,136],'POLYH18-02':[93,94,97,99,100,122,136]}
 for cid in ids:
  claim=by_claim[cid];claim['empirical_scope']=copy.deepcopy(empirical);claim['does_not_establish']+=' '+CLAIM_LIMIT_ADDITIONS[cid]
  claim['locations']=list(dict.fromkeys(claim['locations']+[f'{URL}#page={n}' for n in locations[cid]]))
  if cid=='POLY18-03':claim['support']+=' 기울기분모·시간범위·높이발의위치와같은예외조건을확인한다.'
 for row in reviewed['records']:
  if row['claim_id'] in ids:row['claim_snapshot']=claim_snapshot(by_claim[row['claim_id']],s)
 relations=load(ROOT/'data/revised_relations.json')['relations'];apply_literature_context(relations,registry,registry=reviewed)
 queue=load(ROOT/'data/content_review_queue.json');row=next(x for x in queue['literature_review'] if x['source']['id']==SOURCE);row.update(source=entry,claim_ids=[x['id'] for x in registry['claims'] if x['source_id']==SOURCE])
 write(ROOT/'data/sources.json',bibliography);write(ROOT/'data/literature_claim_reviews.json',registry);write(ROOT/'data/content_review_queue.json',queue);write(ROOT/FILE,reviewed);build_report()
 print('Available copy138/138visually read;52new spreads;6claims/1task explanation/28snapshots rereviewed,8own tasks added; publisher/original-study fidelity remains open')

if __name__=='__main__':main()
