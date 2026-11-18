"""Review the remaining linked area/volume pages without completing their attachments."""
import copy
import hashlib
import json
import re
from collections import Counter,defaultdict
from datetime import datetime
from urllib.parse import urljoin
from literature_review import ROOT,digest,target_value,load_registry,build_report
from relation_analysis_review import load_reviews
from record_lt2_public_review import SOURCE,URL
from complete_lt2_level_text_review import NOTES as PRIOR_NOTES

NOTES='data/literature_evidence/CLEMENTS_SARAMA_LT_area_volume_activities_review_notes.json'
PRIOR_SHA='b2cbee70dddd409ce91709e7365a239da85bcb8572539413ec8a48dc099c5eb0'
DOMAINS=['measurement-area','measurement-volume']
STUB=URL.rstrip('/')+'/math-activities/spatial-learning-at-home-area-senser-foundations'
SCOPE='공식 공개HTML 누적344개 지정 영어 본문: 일반6·영역 개요20·수준224·활동93·교사자료1. 기록된224수준 목록에서 넓이/부피에 연결된 미검토48페이지(넓이21·부피27)를 추가로 읽었다.47페이지는 활동 절차가 있고1페이지는 가정용 안내 소개만 있어 첨부 본문은 미검토다. 새67개 삽입 이미지URL을 시각 대조해 누적110개URL이며 같은 사진의 반복을 포함한다. 기록된 활동/교사자료824개URL 중94개 공개페이지 영어 본문 읽기·730개 본문 대기다. 모든 활동의 전체 절차·첨부PDF·영상·게임·교재·원연구/번역·실제 학생 검증 완료가 아니다.'

OBSERVATIONS=[
 dict(id='LT-P29',standard_codes=['6수03-12','6수03-13'],question='가로10cm·세로6cm인 같은 직사각형을 빈틈·겹침 없이 정확히 덮는다. 한 변1cm 정사각형 타일은 한 장100원,한 변2cm 정사각형은 한 장300원이다. 두 경우의 조각 수·넓이·총비용을 예상한 뒤 확인한다. 큰 타일 가격이500원이면“큰 단위가 언제나 더 싸다”는 판단이 유지되는가?',expected='작은 타일은 한 줄10장씩6줄로60장·넓이60cm²·비용6000원이다. 큰 타일은 한 줄5장씩3줄로15장이고 한 장4cm²여서 넓이는같은60cm²다.300원일 때4500원으로 더 싸지만500원이면7500원으로 작은 타일보다 비싸다. 큰 타일의변 길이는2배·넓이는4배이며 조각 수와조각당 가격을함께비교해야한다.',interpretation='자체 수치의 정확히 덮이는 가상 비용 비교다. 원문의인치/달러·48/12타일과 구별하고 실제 시장 가격이나 구매 권고로 사용하지 않는다. 줄눈·자르기·폐기·인건비를 제외한 타일 비용이라는 조건이다. 큰 조각이 언제나싼것으로일반화하지 않고,단위 변/넓이/조각 수/원 단위를구별한다. 예상은 결과나배열도움제시전에기록하며초기유아자료의교수효과/현재학생단계를판정하지않는다.',student_validated=False),
 dict(id='LT-P30',standard_codes=['6수03-11','6수03-13'],question='한 변1cm인 같은 정사각형12장을 자르거나 겹치지 않고2행6열과3행4열의직사각형으로 각각배치한다. 어느 쪽의넓이가더큰지,둘레도같은지예상하고 덮기/경계추적으로확인하라. 같은넓이라는이유로한종이직사각형을자르지않고다른직사각형과완전히포개거나둘중하나를반드시“더넓다”고선택해야하는가?',expected='둘다12cm²여서넓이는동률이다.2×6직사각형의둘레는2×(2+6)=16cm,3×4는2×(3+4)=14cm다. 내부칸의변은둘레에더하지않고바깥경계를한바퀴추적한다. 같은넓이여도모양/대응길이가달라완전히포개지는것과는다르다. 자르지않는종이비교와단위12장을다시배치하는활동은허용조작이다르다.',interpretation='같은단위·같은넓이·다른경계의자체예다. 원문의더큰정원을들라는발문에같은넓이재료를주었을때동률을허용한다. 모양이안포개진다는이유만으로넓이차를판정하지않고완전포함인지·같은단위덮기/재배치인지구별한다. 원문감각/도형놀이를국내저학년의둘레공식/넓이공식필수로앞당기지않으며자체계산을실제제작/학생설명으로집계하지않는다.',student_validated=False),
 dict(id='LT-P31',standard_codes=['6수03-09','6수03-18','6수03-19'],question='안쪽5cm×2cm×3cm의이상적인직육면체공간을1cm 정육면체로꽉채운다. 한층/층수/전체를설명하고5개씩3줄이라는앞면의15를전체부피로써도되는지확인한다. 교사는5×2밑면의네변에5×3옆면2장과2×3옆면2장을붙이고,5×3옆면하나의바깥5cm변에5×2윗면을붙여전개도를준비한다. 전개도1cm²칸수와내부의1cm³블록수를같다고해도되는가?',expected='밑면한층은5×2=10개이고3층이라전체30개·30cm³다. 앞면의5×3=15는두방향의자리수이며깊이2개를빠뜨렸다. 전개도에는5×2면2장,5×3면2장,2×3면2장이있어단위정사각형은20+30+12=62개·표면넓이62cm²다. 종이의여섯면·표면단위칸62개·내부단위정육면체30개는세는대상과단위가다르다.',interpretation='자체치수와펼친모형의설계다. 조립여분은제외하고종이두께는무시하는이상모형이며실제상자는안쪽치수/단위블록의크기/제작오차를확인한다. 원문의5개씩3줄=부피15라는예는한줄/한층/깊이조건없이는일반화하지않는다. 전개도의그림이나6면수만으로접힘/마주보는면/붙는변을검증했다고하지않고실제접어보는수행을따로관찰한다. 원문의각뿔/삼각기둥도전과제를초등전개도의새필수로추가하지않는다.',student_validated=False),
 dict(id='LT-P32',standard_codes=['4수03-17','4수03-18'],question='가상 용기A의들이는600mL,용기B의들이는800mL다. B에이미300mL가들어있는데가득찬A의600mL를모두부으면어떻게되는가? 넘쳤다는관찰만으로A의들이가B보다크다고할수있는가? 이번에는B를비우고같은A를가득채워옮기는조건을따로비교한다.',expected='처음에는300+600=900mL라B의들이800mL보다100mL가많아넘친다. 그러나들이는B가A보다200mL크므로넘침하나만으로용기순위를정할수없다. B를완전히비우고A의600mL만옮기면200mL만큼더담을수있다. 시작물양·가득참기준·흘림/잔류·받는용기를비웠는지등이용기들이비교의조건이다.',interpretation='원문물옮기기발문의빠질수있는초기조건을구체화한가상반례다. 실제물높이/용기모양/무게/흐르는시간만으로들이를확정하지않으며mL단위로표시한가상계산과실제눈금컵측정을구별한다. 같은용기의물양이변해도들이는그대로다. 한큰주스용기가작은용기두개와같은양이라는주어진관계도사진의가로/세로가두배라는뜻이아니며자체과제의조건으로따로확인한다. 도움/실행전예상/이후설명을각각기록한다.',student_validated=False),
 dict(id='LT-P33',standard_codes=['6수03-18','6수03-19'],question='안쪽5cm×3cm×2cm상자를한변2cm인정육면체로채운다. 블록을자르거나기울이지않고같은모서리에서시작해각방향2cm간격의줄/층에맞춰배치한다. 놓을수있는블록수와그블록이차지한부피,상자안의전체부피를각각구하라. 블록수를센뒤의답을처음예상으로기록해도되는가?',expected='각방향들어가는수는2개·1개·1개여서2개다. 한블록은8cm³이므로차지한부피16cm³,상자안의전체부피는30cm³이고빈공간은14cm³다.30÷8의몫3은이조건에서실제로배치되는블록수가아니다.1cm단위정육면체로교체하면30개로빈틈없이채울수있다. 전개도만본예상,상자를조립한후채우기전의예상,채운뒤확인한수는서로다른시점이어서소급해같은예상으로적지않는다.',interpretation='자체치수와축에정렬한배치조건의가상예다. 임의회전/자르기를허용한최적포장정리를주장하지않는다. 느슨한장난감/인형개수·큰블록개수를용기전체의표준부피로바꾸지않는다. 치즈를잘라단위정육면체를만드는원문과자르지않는블록과제는조건이다르다. 새단위/도식/교사도움뒤의수정예상을최초예상으로소급하지않고실제제작/측정오차와수학적관계를구별한다.',student_validated=False),
]

MAPPINGS=[
 ('LT29',OBSERVATIONS[0]['standard_codes'],['A Printer\'s Predicament / Floor Tiles / Rug Tiles / Quite a Quilt English bodies'], '단위의변길이·넓이·조각수·가격을구별하고완전덮기조건에서같은영역의총비용을비교하는자체설계에참고한다.', '인치/달러예·그림의크기를국내표준단위/현재가격으로전용하지않으며큰조각이면언제나싼것으로일반화하지않는다. 첨부타일/인쇄물전체의검토·현재학생효과를입증하지않는다.'),
 ('LT30',OBSERVATIONS[1]['standard_codes'],['The Biggest Garden / Finger Paint the Area and Perimeter / The Sorcerer\'s Umbrellas / Goldilocks and the Four Areas / Mosaic / Square Mover / Turtle Cage English bodies'], '같은넓이의동률·다른둘레·덮인영역과경계·포개기와단위재배치의조건을구별하는자체설계에참고한다.', '감각놀이/덮기와정확한넓이측정/둘레측정은다르다. 서로다른크기조각/겹침/빈틈을단순개수로집계하지않으며종이가안포개진다는이유만으로넓이순위를판정하지않는다. 원문모양/사진/시행실패를현재단계진단으로전용하지않는다.'),
 ('LT31',OBSERVATIONS[2]['standard_codes'],['Fill the Boat / Measure the Boat / Volume City [3D Row and Column Structurer;3D Array Structurer] / Exploring Rectangular Prisms English bodies'], '한줄/한층/전체의세방향단위와전개도의면/단위정사각형·내부단위정육면체를구별하는자체설계에참고한다.', '원문의불명확한깊이·15/25블록·50+준비물을모든모형에맞는고정개수로전용하지않는다.2×4×3과2×6×2는24이지만4×4×4는64다. 첨부전개도/영상·실제학생반응·현재학년밖전개도확장을검토완료/필수로하지않는다.'),
 ('LT32',OBSERVATIONS[3]['standard_codes'],['Water Buckets / Outdoor Play [two volume levels] / Volume Detectives / Which Holds More / Comparing Juice Containers / Bath Time English bodies'], '현재담긴양과용기전체의들이,옮기기의초기조건/단위반복/예상과결과를구별하는자체설계에참고한다.', '넘침/높이/무게/채움시간만으로들이순위·정확한용량을확정하지않는다. 제공관계1큰용기=2작은용기의양과그림의선형확대를구별하고모호한물음표분수를임의로복원하지않는다. 미국단위/1mL=1cm³/현재학생규준을새필수로넣지않는다.'),
 ('LT33',OBSERVATIONS[4]['standard_codes'],['How Many Cubes? [two levels] / Guessing Jar / Box O\' Blocks / Set Sail / Slice the Cheese / What Will Fit? / Will I Fit? English bodies'], '어림의시점·도움뒤재예상·배치가능한개수·표준부피/용기공간·빈틈과단위교환을구별하는자체설계에참고한다.', '같은부피라도모든물체가들어가거나어떤단위로도정확히채워지는것은아니다. 느슨한물체의개수/겉모습을정확한용량으로전용하지않으며원문의영역/부피중복URL·사진을독립단계/연구/참여자수로합산하지않는다. 실제학생검증/첨부/영상/원연구읽기는별도다.'),
]

IMAGE_DESCRIPTIONS=[
 '치수/단위표시없는격자사진이며8×6책표지의12개2×2단위배열을전사하지않는다.','서로다른길이차량그림이며같은단위넓이비교자료가아니다.',
 '용기의재료를쏟는사진이며물의양/용량수치를읽지않는다.','욕조/큰용기자료아이콘.','작은용기/계량도구자료아이콘.','물자료아이콘.',
 '물붓기사진이며가득참/들이/독립수행을판정하지않는다.','닫힌상자사진이며안쪽치수/채움개수를판정하지않는다.','활동사진이며첨부벽격자의정확한행열은미확인이다.',
 '빈틈이있는여러모양붙이기사진이며정확한단위넓이덮기자료가아니다.','접착종이자료아이콘.','종이에붙인도형자료사진아이콘.','색종이/잘라진조각자료아이콘.',
 '주스비교활동사진이며1대2의용량/선형치수를사진에서읽지않는다.','메모지장식사진이며첨부직사각형의치수/해답이아니다.','정육면체묶음을든사진이며전체치수/전략은판정하지않는다.',
 '모양끼우기놀이사진이며용기용량/정량검사자료가아니다.','상자와블록활동사진이며2×4×3등의완전채움을전사하지않는다.','그리기사진이며색칠된영역과둘레실제측정을동일시하지않는다.',
 '손가락물감자료아이콘.','종이/롤종이자료아이콘.','앞치마자료아이콘.','정리도구자료아이콘.',
 '바닥도형활동사진이며48/12개첨부인쇄물전체가아니다.','용기놀이사진이며용량의정확한값은미확인이다.','네침대그림이며활동의네직사각형치수/넓이를읽을수없다.',
 '용기속블록활동사진이며가려진수량/빈공간을확정하지않는다.','상자예상활동사진이며예상시점/답/첨부전개도를전사하지않는다.','놀이사진이며상자전개도나블록배열의정답이아니다.',
 '모자이크장식사진이며동일단위12개활동의실제정답이아니다.','타일활동사진이며일부격자사진을첨부전체로세지않는다.','식사사진이며현재물양/용기들이를전사하지않는다.',
 '상자/블록활동사진이며한층/전체개수와독립전략은미확인이다.','야외놀이사진이며단위들이측정결과가아니다.','야외감각놀이자료아이콘.','여러용기자료아이콘.','깔때기/계량도구자료아이콘.',
 '다른URL의같은야외놀이사진이며독립관찰/새참여자가아니다.','퀼트장식사진이며첨부격자/전체단위수를검토한것이아니다.','깔개활동사진이며4×6/5×5치수를사진에서확정하지않는다.',
 '돛단배장식그림이며점토공간의부피/완전채움을보여주지않는다.','치즈사진이며1인치크기/숨은부피/완전등분을확정하지않는다.','가정용공간안내의일부미리보기이며첨부전체는미검토다.',
 '색재료장식사진이며12개정사각형배열정답이아니다.','정원사진이며같은넓이의첨부직사각형배치가아니다.','비/우산/요정장식그림이며단위덮기의완전성을검증하지않는다.',
 '격자활동사진이며전체4×5첨부인쇄물을검토한것이아니다.','상자안어린이사진이며넓이/용량수치를판정하지않는다.','앞사진과동일SHA의다른URL이며독립학생관찰/연구가아니다.',
 '종이비교활동사진이며정확한넓이순위/학생전략을확정하지않는다.','색종이자료아이콘.','도시장식그림이며실제전개도/내부부피가아니다.','유사한도시장식그림이며다른단계의독립효과를입증하지않는다.',
 '탐정모자/돋보기장식그림이며물측정자료가아니다.','야외사진이며물의양/진단자료가아니다.','물옮기기사진이며초기용기상태/넘침/판정값전체는미확인이다.','물놀이사진이며정확한들이/독립수행을판정하지않는다.',
 'What Will Fit?표지이며책본문/바구니격자는미검토다.','다른URL의유사한책표지이며책본문읽기가아니다.','책자료아이콘표지이며본문전체는미검토다.',
 '바구니/농구공자료아이콘이며공과용기의정밀치수/들이가아니다.','바구니/해변공자료아이콘이며사진크기로부피를비교하지않는다.','바구니/축구공자료아이콘이며그림의꼭맞음을실제들이/빈틈0으로판정하지않는다.',
 '야외물용기사진이며정확한용량측정값은미확인이다.','물놀이용테이블자료아이콘.','계량컵/음료용기자료아이콘이며눈금값을측정결과로읽지않는다.','상자놀이사진이며맞음/공간/독립전략의실제관찰기록이아니다.',
]

def perimeter(cells):
 return sum((x+dx,y+dy) not in cells for x,y in cells for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)])

def verify():
 assert len(MAPPINGS)==len(OBSERVATIONS)==5 and len(IMAGE_DESCRIPTIONS)==67
 assert 10*6==60 and 5*3==15 and 2**2==4 and 15*4==60
 assert 60*100==6000 and 15*300==4500<6000<15*500==7500
 a={(x,y) for x in range(6) for y in range(2)};b={(x,y) for x in range(4) for y in range(3)}
 assert len(a)==len(b)==12 and perimeter(a)==16 and perimeter(b)==14
 assert 5*2*3==30 and 5*3==15 and 2*(5*2+5*3+2*3)==62
 rect=lambda x,y,w,h:{(i,j) for i in range(x,x+w) for j in range(y,y+h)}
 net=[rect(0,0,5,2),rect(0,-3,5,3),rect(0,2,5,3),rect(-3,0,3,2),rect(5,0,3,2),rect(0,-5,5,2)]
 assert sum(map(len,net))==len(set.union(*net))==62
 assert 300+600==900 and 900-800==100 and 800-600==200
 assert (5//2)*(3//2)*(2//2)==2 and 2*2**3==16 and 5*3*2-16==14 and 30//8==3

def main():
 verify();registry=load_registry();s=registry['sources'][SOURCE]
 if s['snapshot_file']==NOTES:
  assert {m[0] for m in MAPPINGS}<={c['id'] for c in registry['claims']}
  print('LT2 area/volume activity reading remains current; no automatic refresh');build_report();return
 assert s['snapshot_file']==PRIOR_NOTES and s['snapshot_sha256']==PRIOR_SHA
 assert hashlib.sha256((ROOT/PRIOR_NOTES).read_bytes()).hexdigest()==PRIOR_SHA
 old=copy.deepcopy(registry);relations=copy.deepcopy(load_reviews());prior=json.loads((ROOT/PRIOR_NOTES).read_text(encoding='utf-8'))
 cache=ROOT/'tmp/literature/lt2-area-volume-activities';pages=json.loads((cache/'activity-manifest.json').read_text(encoding='utf-8'));selection=json.loads((cache/'selection.json').read_text(encoding='utf-8'));images=json.loads((cache/'image-cache-manifest.json').read_text(encoding='utf-8'))
 expected=[a for a in prior['activity_followup_catalog']['records'] if not a['body_read'] and any('/'+d+'/' in u for u in a['linked_level_urls'] for d in DOMAINS)]
 assert selection==expected and len(pages)==len(selection)==48 and {a['url'] for a in pages}=={a['url'] for a in selection}
 assert len(images)==67 and {a['url'] for a in images}.isdisjoint(a['url'] for a in prior['image_read_manifest'])
 for a in pages+images:
  assert a['url'].startswith(URL) and a['status']==200 and hashlib.sha256((ROOT/a['file']).read_bytes()).hexdigest()==a['sha256']
  if 'final_url' in a:assert a['url']==a['final_url']
 fields=['key','url','title','sha256','status'];assets=prior['observed_html_assets']+[{k:a[k] for k in fields} for a in pages]
 assert len(assets)==len({a['url'] for a in assets})==len({a['key'] for a in assets})==344
 image_fields=['page_url','url','status','sha256','dimensions','content_type'];image_manifest=prior['image_read_manifest']+[dict(**{k:a[k] for k in image_fields},read_kind='inline_image_visual_review',redistributed=False) for a in images]
 assert len(image_manifest)==len({a['url'] for a in image_manifest})==110
 groups=copy.deepcopy(prior['read_groups']);groups['activities'] += [a['key'] for a in pages]
 assert {k:len(v) for k,v in groups.items()}==dict(general=6,domain_overviews=20,levels=224,activities=93,teacher_resources=1)
 followup=copy.deepcopy(prior['activity_followup_catalog']);read_urls={a['url'] for a in assets}
 for a in followup['records']:a['body_read']=a['url'] in read_urls
 followup.update(listed_body_read=sum(a['body_read'] for a in followup['records']),listed_body_pending=sum(not a['body_read'] for a in followup['records']))
 assert followup['listed_body_read']==94 and followup['listed_body_pending']==730 and len(followup['records'])==824
 assert not [a for a in followup['records'] if not a['body_read'] and any('/'+d+'/' in u for u in a['linked_level_urls'] for d in DOMAINS)]
 updates={};procedure_absent=[];image_refs={};attachments={};domain_counts=Counter()
 for a in pages:
  text=(ROOT/a['file']).with_suffix('.txt').read_text(encoding='utf-8');english=text.split('Objetivo de Aprendizaje:')[0];pos=list(re.finditer(r'Learning Objective:\n',english));body=english[pos[-1].start():]
  if '\nActivity\n' not in body:procedure_absent.append(a['url'])
  label=re.search(r'Last updated:\n([^\n]+)',text).group(1);updates[a['url'].split('/')[-1]]=datetime.strptime(re.sub(r'(\d+)(st|nd|rd|th)',r'\1',label),'%B %d, %Y').strftime('%Y-%m-%d')
  domain_counts['area' if 'Measurement: Area' in body else 'volume']+=1
  image_refs[a['url']]=sorted({urljoin(a['url'],v['src']) for v in a['images'] if '/upload/' in v.get('src','')})
  attachments[a['url']]=sorted(u for u in a['links'] if '.pdf' in u.lower())
 assert procedure_absent==[STUB] and domain_counts==dict(area=21,volume=27)
 assert {u for v in image_refs.values() for u in v}<={a['url'] for a in image_manifest}
 hashes=defaultdict(list)
 for a in images:hashes[a['sha256']].append(a['url'])
 duplicates=[dict(sha256=k,urls=v) for k,v in hashes.items() if len(v)>1];assert len(duplicates)==1 and len(duplicates[0]['urls'])==2
 corrections=[
  dict(kind='area_unit_count_cost_and_print_scale',locations=['A Printer\'s Predicament','Floor Tiles','Rug Tiles','Quite a Quilt'],action='책표지8×6과2×2단위는12조각/48제곱인치를구별한다. Floor Tiles의48/12조각과1/2달러는48/24달러총비용이지만현재가격으로전용하지않는다. 단위변2배는넓이4배이고혼합단위/타일가격/자르기조건을명시한다. 삽입격자사진/장식그림은첨부인쇄물의정확한치수·출력배율·해답전체가아니다.'),
  dict(kind='equal_area_tie_and_perimeter_scope',locations=['The Biggest Garden','Goldilocks and the Four Areas','Turtle Cage','Finger Paint the Area and Perimeter','Mosaic','Square Mover'],action='Biggest Garden은더큰정원을고르게하지만재료를같은넓이의두직사각형으로정하고둘다들도록한다. 자체발문은동률을명시하며형태/넓이/둘레를구별한다. 완전포함되지않는포개기만으로넓이순위를정하지않는다. 더많은색으로덮는일은영역을보여줄수있지만그자체가둘레측정은아니다. 같은수타일이라도같은단위/빈틈/겹침조건이필요하다.'),
  dict(kind='coverage_not_same_as_nonoverlap_measurement',locations=['Can You Cover the Shape?','The Sorcerer\'s Umbrellas','What Will Fit? area activity'],action='감각놀이단계는정확한단위반복을요구하지않는다는원문한계를보존한다. 원형우산의비방울실험은원재료배치/겹침/물성/경계조건에영향을받아모든원으로어떤영역도덮을수없다는정리가아니다. 빈틈없는비중첩측정과겹쳐비를가리는일을구별한다. 호박그림의외곽이아니라같은정사각형단위위에인쇄한그림이라는재료설명도구별한다.'),
  dict(kind='three_dimensions_net_and_supply_guard',locations=['Volume City / two levels','Fill the Boat','Measure the Boat'],action='5개씩3줄=15의예는깊이/층의구조를명시해야전체부피인지판정할수있다.25개를지급하는것과15개예의전부사용을동일시하지않는다.2×4×3/2×6×2는24,4×4×4는64로서서로다른치수라도같은부피인앞두개와셋째를구별한다.50+준비물표시만으로64개완전채움의실제수량확보를확정하지않는다. 전개도표면칸/면/내부부피·조립여분/안쪽치수/출력배율·각뿔/삼각기둥도전과국내범위를구별한다.'),
  dict(kind='prediction_timing_and_unit_reference',locations=['How Many Cubes? / two levels','Guessing Jar','Box O\' Blocks'],action='목표는상자를만들기전예상이라고하지만일부절차는조립후추정기록이라고적혀있다. 접기전/접은후채우기전/채운후확인을각각기록한다.10개막대단위도움뒤재예상을처음예상으로소급하지않는다. 같은규격블록을일렬로비교하는초기수준에서개수세기를필수로요구하지않고장난감/알같은느슨한물체의개수를정확한용기부피로바꾸지않는다.'),
  dict(kind='capacity_initial_state_and_linear_scale',locations=['Water Buckets','Outdoor Play / two volume levels','Comparing Juice Containers','Volume Detectives'],action='넘침으로두용기의들이를비교하려면처음용기는가득,받는용기는비움,흘림/잔류없음과같은채움기준을명시한다. 이미물든용기의넘침은들이순위를뒤집을수있다.1큰주스=2작은주스는주어진양의관계이며그림의가로/세로가두배라는뜻으로읽지않는다. Volume Detectives의도전분수중물음표기호는분모를확정할수없어임의복원하지않는다. 각방향2배의상사공간은부피8배라는교사용대조와미국단위/단계/국내들이목표를구별한다.'),
  dict(kind='material_volume_capacity_fit_and_gaps',locations=['Set Sail','Slice the Cheese','What Will Fit?','Too Big Too Small Just Right / two domains','Which Holds More'],action='점토재료의부피·배안공간의용량·그안에들어간단위블록의부피를구별한다. 같은점토양으로다른용량을만들수있고느슨한물체가들어갔다고빈틈0을보장하지않는다. 치즈를자르는조건과고정블록을자르지않는조건도다르다. 같은부피/넓이가모양/실제맞음과동일하지않으며사진/무게/높이/용어회상만으로정량측정/교수효과를확정하지않는다.'),
  dict(kind='stub_attachments_repeated_assets_and_scope',locations=['48 selected public pages','Spatial Learning at Home','67 selected new inline image URLs'],action='47페이지에는활동절차가있고Spatial Learning at Home은소개/서지와일부이미지만있다. 그첨부전체를읽은것으로집계하지않는다. 새67이미지URL에는같은SHA2URL한쌍과유사/반복사진·책표지·장식그림·자료아이콘이있다. 각URL확인을독립사진/단계/연구/참여자로합산하지않고원영상/첨부전개도/교재/원연구를검토완료하지않는다. 넓이/부피에나온유사활동URL도서로독립효과근거가아니다.'),
  dict(kind='access_support_and_school_scope',locations=['STEMIE adaptations and differentiation across selected pages'],action='소통방식/기다림/쥐기/교사배치도움과수학적판단을구별하며눈맞춤/감각반응/사진에서인지상태나독립전략을추정하지않는다. 원문은유아/초기수학의다양한활동이고형식적넓이/부피/전개도/단위공식을국내저학년의새필수로넣지않는다. 건강/물놀이/식품/도구에관한현재지침이나참여자에대한의료/진단판정을제공하는자료로쓰지않는다.'),
 ]
 p=ROOT/'data/sources.json';bibliography=json.loads(p.read_text(encoding='utf-8'));b=next(v for v in bibliography if v['id']==SOURCE);previous_b=copy.deepcopy(b)
 b.update(review_scope=SCOPE,next_review='기록된224수준의활동/교사자료824개URL중94개공개영어페이지를읽었고730개본문은대기다. 넓이/부피연결미검토48페이지는이번에확인했으나Spatial Learning at Home의소개밖첨부본문·첨부타일/전개도/그림책/영상/게임/교재/원연구·미검토출처는별도다. 단위/차원/조건/반례를우선대조하고동일URL/유사사진을독립근거로더하지않는다. 현재20개개요/224수준본문완료는전체사이트/한국어과제의진단정확도/효과완료가아니다.')
 log=['기록된224수준의활동목록에서넓이/부피에연결된미검토48개공개페이지의영어목표·절차·팁·자료·차별화·표시서지를읽었다. 넓이21·부피27이며47개절차와1개가정용안내소개를구별한다. 스페인어전체번역/첨부전체읽기가아니다.', '새삽입이미지67개URL을번호0–66으로확인했다. 일부는여러페이지에서공유되며같은SHA의사진2URL도있다. 첨부미리보기/표지/자료아이콘/사진/장식그림을구별하고실제학생의전략/수량/효과를전사하지않는다.', '이전296개공개HTML/43이미지URL과모든주장/관찰/수준목록을보존했다. 새48개를더해344개HTML이고110이미지URL이다. 본문읽기상태는824개목록에대해94/730으로갱신하며그목록자체를새활동이나원연구읽기로세지않는다.', '본문의같은넓이동률·단위변/넓이/가격·셋째차원/물체수·예상시점·용기초기상태/들이·사진/표지의한계를자체발문/기대설명에반영한다. 원문사이트자체를수정하거나공식정오표를확정한것이아니다.']
 notes=copy.deepcopy(prior)
 notes.update(date='2026-11-06',read_scope=SCOPE,previous_review=copy.deepcopy(s),previous_bibliography=previous_b,previous_notes_file=PRIOR_NOTES,previous_notes_sha256=PRIOR_SHA,observed_html_assets=assets,html_read_manifest=assets,image_read_manifest=image_manifest,image_reading_log=prior['image_reading_log']+[a['url'].split('/')[-1]+':'+d for a,d in zip(images,IMAGE_DESCRIPTIONS)],read_groups=groups,new_read_groups=dict(domain_overviews=0,levels=0,activities=48,teacher_resources=0),reading_log=prior['reading_log']+log,source_corrections=prior['source_corrections']+corrections,activity_update_dates={**prior['activity_update_dates'],**updates},activity_followup_catalog=followup,catalog_coverage={**prior['catalog_coverage'], 'read_activity_bodies':94,'pending_activity_bodies':730},selected_activity_image_urls=image_refs,linked_attachment_urls_not_read=attachments,new_image_exact_reuse_groups=duplicates,activity_procedure_coverage=dict(selected_pages=48,pages_with_procedure=47,introduction_only_pages=procedure_absent,full_activity_material_review=False),completed_area_volume_activity_records=selection,unread_followups=[b['next_review'],'안내소개1페이지와미리보기/책표지의확인을첨부전체·그림책전체·현재학생수행으로바꾸지않는다. 원문HTML/그림/추출전체텍스트는이식용묶음에복제하지않는다.'])
 npath=ROOT/NOTES;npath.write_text(json.dumps(notes,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 history=s.get('snapshot_history',[])+[dict(snapshot_file=PRIOR_NOTES,snapshot_sha256=PRIOR_SHA,date=s['date'],read_scope=s['read_scope'])]
 s.update(date='2026-11-06',snapshot_file=NOTES,snapshot_sha256=hashlib.sha256(npath.read_bytes()).hexdigest(),snapshot_history=history,bibliography_snapshot=digest(b),html_read_manifest=assets,image_read_manifest=image_manifest,read_scope=SCOPE,method_note='기록된수준목록에서넓이21/부피27개의남은공개영어페이지와새67이미지URL을대조했다. 절차47/소개1·동률/단위/셋째차원/초기물양/예상시점과첨부미검토를구별한다.',limits='누적344개공개영어페이지/110삽입이미지URL범위다. 이미지수에는같은사진의반복이포함된다.730개활동/교사자료본문·소개1페이지의첨부실제절차·미선정그림/첨부/영상/게임/원연구/교재/번역·한국어과제의진단정확도/효과·현재학생수행은미검토다. 사진/단계이름으로능력이나필수경로를확정하지않는다.',editorial_action='이전주장28건/관찰28건을보존하고8개기준에새주장5건/자체관찰5건을대응했다. 누적주장33건·관찰33건·기준48개다. 관계검토·독립검토·학생검증에더하지않는다.',observations=s['observations']+OBSERVATIONS)
 for cid,codes,locations,support,limit in MAPPINGS:
  registry['claims'].append(dict(id=cid,source_id=SOURCE,role='related_theoretical_context',locations=locations,support=support,does_not_establish=limit,standard_codes=codes,target_snapshots={'revision:'+c:digest(target_value('revision:'+c)) for c in codes},independent_review=False,student_validated=False))
 assert len({code for c in registry['claims'] if c['source_id']==SOURCE for code in c['standard_codes']})==48
 p.write_text(json.dumps(bibliography,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');(ROOT/'data/literature_claim_reviews.json').write_text(json.dumps(registry,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 p=ROOT/'data/content_review_queue.json';q=json.loads(p.read_text(encoding='utf-8'));row=next(v for v in q['literature_review'] if v['source']['id']==SOURCE);row.update(source=b,claim_ids=[c['id'] for c in registry['claims'] if c['source_id']==SOURCE]);p.write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 assert registry['claims'][:len(old['claims'])]==old['claims'] and s['observations'][:28]==old['sources'][SOURCE]['observations']
 assert all(registry['sources'][k]==v for k,v in old['sources'].items() if k!=SOURCE) and load_reviews()==relations
 build_report();print('Added48 LT2 area/volume pages (47 procedures,1 introduction),67 image URLs,5 claims/probes;730 linked public bodies pending')

if __name__=='__main__':main()
