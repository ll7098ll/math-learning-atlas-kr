"""Read a separate second-edition course scan; preserve the official excerpt."""
from record_scoped_pdf_research import record
from literature_review import ROOT
from extend_lt2_length_assets_review import load
from check_polya_problem_models import check
SOURCE='POLYA_SECOND_EDITION_COURSE_SCAN';DATE='2026-11-18'
CACHE=ROOT/'tmp/literature/polya-classroom-method-20261117'
SHA='f35773a5befa8d86c5a6475352743fbd6689f7f0b981bf208301ea50bf213e68'
URL='https://ifht.uerj.br/pluginfile.php/24455/mod_resource/content/1/Polya%20-%20How%20to%20solve%20it.pdf'
NI='12수과01-01';LI='12수과02-01';PL='12수과03-01';RU='12수과03-02';OU='12수과03-03';RE='12수과03-04'
SCOPE='UERJ 공개 강의 사본의 첫30PDF판면을 직접 읽었다. 글자 추출/OCR은0쪽이며 대부분 한 판면에 책 두 면을 스캔한 자료다. 표제·판권·세 서문·목차·옆으로 놓인 질문 목록(xvi–xvii)·Introduction(xix–xxi),Part I의20절 전체(인쇄1–32),Part II 대화 전체(33–36)와 경계의 사전37쪽 첫 면이 범위다. Part III 사전 전체·Part IV·전권을 읽은 것은 아니다. 기존 Princeton 공식 발췌 XXV–XXVII와 다른 사본/쪽 체계로 구별한다.'
LIMIT='원문의 교수 조언·예시 대화와 수학 예제를 읽었으며 새 실증 표본이나 국내 학생 효과를 확보하지 않았다. 2판 저작권1957·표시된 인쇄1971/1973·서문1944/1954/1956·스캔 메타데이터2006을 구별하고 이 사본의 실제 인쇄연도는 확정하지 않는다. 출판사 직접 파일/동일성·다른 판본·사전의 나머지와Part IV·인용 원연구/정오표·실제 독립/학생 검증은 미확인이다. 일반 질문은 고정 성공 알고리즘이나 모든 학생에게 같은 순서·발문을 요구하는 근거가 아니다.'
SPECS={SOURCE:dict(stem='polya-second-edition-university-course-copy',render_stem='polya',sha256=SHA,total=138,pages=list(range(1,31)),text_pages=[],visuals=list(range(1,31)),pdf_url=URL,url=URL,year=1957,title='How to Solve It, second-edition course scan — question list, complete Parts I–II and selected front matter; edition copyright1957, actual printing unverified',authors=['G. Pólya'],scope=SCOPE,limit=LIMIT,design='교수 조언·예시/이상화 대화·수학 예제의 방법론적 서술',sample='Part I의20절과Part II의이상화교사/학생대화이며 새 통합 고유 참여자 수·실험 설계·인과 효과크기를 보고하는 자료로 취급하지 않는다.',student_outcome_study=False,supports=['유연한 문제 이해·계획·실행·성찰','발문과 지원의 범위','보조 문제·조건·변수·검산과 증명'],next_review='Part III의나머지·Part IV와다른판본/인용원연구·정오표를후속대조하고자체과제의실제응답은별도로검증한다.')}
CLAIMS=[
 (SOURCE,'POLY18-01',[NI,PL,RU],[8,13,14,15,16,17,28,29],'구할 것·자료·조건을 밝히고 증명 문제에서는 가정과 결론을 구별한다. 이해·계획·실행·되돌아보기를 문제에 맞게 오가며, 보조 문제로 바꿨다면 원래 질문과 조건으로 돌아와 연결을 확인한다.','책의4부·Part II의대화 소제목과4단계는 서로 다른 구분이다. 목록을 한 번씩 채우는 절차나 언제나 해결되는 알고리즘으로 쓰지 않는다.'),
 (SOURCE,'POLY18-02',[LI,PL,RU],[12,13,14,17,18,22,23,28,29],'질문은 학생의 현재 생각에 맞게 고르고 일반적인 질문에서 필요한 구체적 도움으로 조정한다. 실제 발문·힌트와 그 뒤 학생이 한 일을 구별해 계획과 수행 기록에 남긴다.','원문의예시/이상화대화를 실제 학생자료로 세지 않는다. 도움을 적게 준다는 조언이 지원을 숨기거나 독립 수행을 꾸며 쓰는 허가가 아니며 정답을 암시한 질문의 성공을 보편 효과로 바꾸지 않는다.'),
 (SOURCE,'POLY18-03',[RU,OU,RE],[15,16,17,18,19,20,21,24,25,26,27,28],'보조선·보조변수와 원래 조건의 관계를 설명하고, 구한 답과 각 추론 단계를 확인한다. 직육면체 대각선에는 직각 조건이 필요하며 원뿔의 부피 변화율과 높이 변화율, 변하는 수면 반지름을 구별한다.','인쇄16쪽의rectangular parallelogram표기는7쪽문제·Fig1·세직각변이 가리키는직육면체와대조한다. 자체좌표/미분검산은 실제 측정이나 학생자료가 아니며 교과에 없는 미분을 모든 탐구에 요구하지 않는다.'),
 (SOURCE,'POLY18-04',[OU,RE],[19,20,21,26,29,30],'되돌아보기에서 결과·논증·다른 풀이·변형 문제를 구분한다. 대칭·단위·극한/특수 경우 검사는 오류를 찾는 데 쓰고, 성립 조건을 갖춘 유도와 증명은 따로 제시한다.','검사 몇 개를 통과한 사실만으로 모든 경우의 증명이 되지 않는다. 원문은 유도한 결과를 다시 살피는 조언이며 자체의일부러틀린식은Pólya의식이나실제학생오답이아니다.')]

def task(n,codes,q,e,i):return dict(id=f'POLY18-P{n:02d}',standard_codes=codes,question=q,expected=e,interpretation=i,student_validated=False)
OBSERVATIONS={SOURCE:[
 task(1,[NI,PL,RU],'계획대로 풀다가 조건이 맞지 않음을 알았다. 이해→계획→실행→되돌아보기 칸을 이미 채웠으니 계속 계산해야 하는가?','원래 질문·조건을 다시 살피고 계획을 바꾼 이유를 남긴다. 구할 것과 주어진 자료를 구별하며 증명 문제라면 가정과 결론을 명시한다. 단계 이름을 적은 일과 문제를 해결한 일을 구별한다.','자체 과정 점검이다. 네 단계를 고정된 일회 순서나 성공 보장으로 바꾸지 않는다.'),
 task(2,[LI,PL,RU],'“관련해서 풀어 본 문제는?”과“피타고라스 정리를 쓰면 되지?”는 같은 도움인가?','현재 생각·앞선 경험·교사의 의도를 확인한다. 뒤 질문은 핵심 방법을 더 직접 제시할 수 있다. 어느 질문을 했고 학생이 무엇을 추가했는지 기록하며 지원 뒤 정답을 도움 없는 발견으로 표시하지 않는다.','문구만으로 언제나 좋은/나쁜 질문을 판정하지 않는다. 가상 비교이며 실제 학생 응답이나 독립 검토가 아니다.'),
 task(3,[RU,OU],'서로 수직인 세 모서리가3,4,12인 직육면체의 공간 대각선을 보조 문제로 구하라. 세 모서리 길이만 같으면 항상 같은가?','밑면 대각선5를 먼저 구하고 공간 대각선√(5²+12²)=13을 구한다. 수직 조건을 뺀 자체 벡터(3,0,0),(12/5,16/5,0),(0,0,12)는 같은 모서리 길이지만 대각선 제곱917/5로169와 다르다.','정적 그림의 모양·인쇄16쪽의평행사변형단어만으로 적용하지 않는다. 좌표 예는 원문 그림의 실측·학생 자료가 아니다.'),
 task(4,[OU,RE],'일부러 만든 틀린 후보식 d²=a²+b²+c²+abc/(a+b+c)가 대칭·같은 배율 확대·c=0 검사를 통과하면 맞는가?','아니다. 이 식은 순열 대칭,길이12배시제곱144배, c=0에서a²+b²를 만족하지만3,4,12에서는3355/19로올바른169와다르다. 검사는 필요 조건 점검이며 유도·증명을 대신하지 않는다.','작성자가 만든 반례다. 이 식을 Pólya의 식·실제 학생 오답·검증된 진단 문항으로 소개하지 않는다.'),
 task(5,[RU,OU,RE],'미분을 배운 경우: 거꾸로 선 원뿔의 전체 반지름4ft·높이3ft,유입2ft³/min,수심1ft에서 높이 변화율을 구하라.','수면반지름x=(4/3)y,V=16πy³/27이므로2=(16π/9)y²dy/dt, y=1에서dy/dt=9/(8π)ft/min이다. x도변하므로x를상수로두면틀린3배값27/(8π)를얻는다.','0<y≤3의해당충전범위와단위를밝힌다. 원문수학예제검산이며실제유량/학생자료가아니다. y=0에분모y²공식을그대로대입하지않는다.'),
 task(6,[RU,RE],'a=3,b=4,c=12의 대각선을13으로 구했다. 단위를 바꾸거나높이를0으로보내는확인은 무엇을 더해 주는가?','같은 길이 단위로 고쳐 식의 차원을 확인하고,c=0이면밑면대각선5로이어짐을본다. 원래직육면체의양의높이조건과평면경계는구별한다. 이런확인은앞선유도를재검토하며검사만으로증명을새로얻는것은아니다.','검산·경계 확장·일반 증명의 범위를 구별하는 자체 과제이며 실제 성찰 효과를 측정한 것이 아니다.'),
 task(7,[LI,RU],'두 각의 각 변이 각각 평행하면 각의 크기는 언제나 같은가?','원문은 대응하는 반직선의 방향도 같다는 조건을 둔다. 자체 예u=(1,0),v=(3/5,4/5)에서u만(-1,0)으로뒤집으면평행은유지되지만각의코사인은3/5에서−3/5로바뀌어같은각이아니다.','원문19절의가정과결론을구별한다. 평행한직선과반직선방향을혼합하지않고이예를원론XI.10전체독해로쓰지않는다.'),
 task(8,[LI],'이 사본의30PDF판면을 읽었다면1957년 원판138본문쪽과Princeton 공식발췌까지 모두 같은 판본으로 확인한 것인가?','아니다. PDF는138판면이고대부분책두면스캔이다. 읽은범위는앞30판면의선정서지/질문목록·Part I1–32·Part II33–36·사전37첫면이다.2판저작권1957,표시인쇄1971/1973,메타데이터2006은다르며공식발췌XXV–XXVII와이사본Introductionxix–xxi를구별한다.','전체사전·Part IV·다른판본/인용원연구·실제인쇄연도·출판사직접파일동일성은미확인이다. 추출문/OCR0쪽을본문을안읽었다는뜻이나30텍스트쪽으로바꾸지않는다.')
]}
DETAILS={SOURCE:dict(read_kind='visual_only_scanned_spreads',pdf_pages=138,selected_pdf_pages=list(range(1,31)),machine_extracted_text_pages=[],ocr_used=False,question_list_pdf_pages=[8],question_list_printed_pages='xvi–xvii',question_list_rotation_reviewed=True,introduction_pdf_pages=[9,10],introduction_printed_pages='xix–xxi',complete_part_i_read=True,part_i_printed_pages='1–32',part_i_sections=list(range(1,21)),complete_part_ii_read=True,part_ii_printed_pages='33–36',part_ii_subheadings=5,part_iii_boundary_page_only=37,part_iii_complete=False,part_iv_read=False,whole_book_read=False,remaining_pdf_pages_without_visual_review=list(range(31,139)),source_figures_viewed=list(range(1,7)),edition_copyright_year=1957,original_copyright_year=1945,copyright_renewal_year=1973,listed_paperback_printings=[1971,1973],preface_dates=['1944-08-01','1954-08-30','1956-06-30'],paperback_isbn='0-691-02356-5',hardcover_isbn='0-691-08097-6',lc_card_literal='79-160544',pdf_metadata_creation='D:20061014103040',actual_printing_date_verified=False,publisher_direct_pdf_obtained=False,publisher_binary_fidelity_verified=False,official_excerpt_source_unchanged='POLYA_PRINCETON_INTRO_UNDATED',idealized_dialogue_is_not_student_data=True,raw_classroom_records_read=False,cited_originals_all_read=False,independent_review=0,student_validation=0)}
CORRECTIONS={SOURCE:['30PDF판면은대부분두면스캔이며30추출문쪽이나138본문쪽이아니다. 질문목록의회전과Part II옆의손글씨표시는스캔상태/사본주석이며학생응답으로세지않는다.','인쇄16쪽rectangular parallelogram표기는7쪽문제·세직각변·Fig1의직육면체(rectangular parallelepiped)와대조한다. 공식정오표나모든판본의오류를확인한것은아니다.','4부구성·4단계·Part II의5소제목을구별한다. 질문·단계는성공알고리즘이나모든학생에게같은일회순서를강제하는근거가아니다.','대칭·차원·경계검사는오류검출에쓰고유도/증명과구별한다. 자체의틀린후보식은원문에실린식이나실제학생자료가아니다.','두유량의차원과변하는수면반지름·수심을구별한다. 인용ETS연구/Time1956·원론XI.10·Part III교차참조와역사원전전체는미독이다.']}
INTERPRETATIONS={}
for rid in ['SEC_12수과01-01_C04','SEC_12수과03-01_C04','REV-12수과03-01-1','HP-inquiry-plan','HP-inquiry-execution']:
 INTERPRETATIONS[rid,'POLY18-01']=('activity_context','문제의구할것/가정·조건과보조문제의연결을계획하고실행중생각이바뀐이유를남긴다.','단계이름을채운것을해결·고정선수절차·성공보장으로바꾸지않는다. 예시대화는실제학생자료가아니다.')
for rid in ['SEC_12수과02-01_C04','SEC_12수과03-01_C04','REV-12수과02-01-1','HP-inquiry-execution']:
 INTERPRETATIONS[rid,'POLY18-02']=('activity_context','읽은조언·실제발문/힌트·학생이덧붙인설명을구별해계획과수행을대조한다.','지원뒤정답을도움없는발견으로기록하거나원문의이상화대화를독립검토/학생검증으로세지않는다.')
for rid in ['SEC_12수과03-02_C04','SEC_12수과03-03_C04','REV-12수과03-04-1','HP-inquiry-presentation','HP-inquiry-reflection']:
 INTERPRETATIONS[rid,'POLY18-03']=('activity_context','보조선/변수·직각조건·변화율의단위를계산과발표에서명시하고각추론을확인한다.','직육면체공식을모든평행육면체에쓰거나변하는수면반지름을상수로두지않는다. 자체검산은실제측정·학생자료가아니다.')
for rid in ['SEC_12수과03-03_C04','REV-12수과03-04-1','HP-inquiry-reflection']:
 INTERPRETATIONS[rid,'POLY18-04']=('inference_limit','결과의대칭·단위·특수경우검사와각단계의유도/증명을구별해성찰한다.','몇개검사를통과한후보식의일반적참을확정하지않고,작성자의반례를원문식·실제학생오답·학습효과로바꾸지않는다.')

def main():
 if SOURCE not in load(ROOT/'data/literature_claim_reviews.json')['sources']:
  a=load(CACHE/'acquisition.json');assert a['sha256']==SHA and a['reading_completed'] and a['images_viewed'] and a['read_text_pages']==[] and a['viewed_image_pages']==list(range(1,31)) and not a['whole_book_read'];assert check()['status']=='pass'
 record(specs=SPECS,claims=CLAIMS,observations=OBSERVATIONS,details=DETAILS,corrections=CORRECTIONS,interpretations=INTERPRETATIONS,cache=CACHE,date=DATE,category='문제해결발문·조건·논증의2판강의사본대조',detail_key='classroom_method_scan_review',roles={c[1]:('mathematical_explanation' if c[1]=='POLY18-03' else 'related_theoretical_context') for c in CLAIMS})

if __name__=='__main__':main()
