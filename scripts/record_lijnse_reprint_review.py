"""Read the authorized 2010 reprint without promoting it to the 1995 original."""
from record_scoped_pdf_research import record
from literature_review import ROOT
from extend_lt2_length_assets_review import load

SOURCE='LIJNSE_2010_AUTHORIZED_REPRINT'; DATE='2026-11-17'
CACHE=ROOT/'tmp/literature/lijnse-developmental-reprint-20261117'
SHA='cddeebe3b3be461604c03c00a2984b26054f45e108eb1aeddb8e208c64547662'
URL='https://www.fisme.science.uu.nl/publicaties/literatuur/2010_book_sympPL_FI-website.pdf'
ORIGINAL='https://onlinelibrary.wiley.com/doi/abs/10.1002/sce.3730790205'
TEXT=[1,3,4,5,7,8,*range(93,104)]; VISUAL=[*TEXT,104]
LI='12수과02-01';DE='12수과02-04';PL='12수과03-01';RU='12수과03-02';OU='12수과03-03';RE='12수과03-04'
SCOPE='위트레흐트대 공식 PDF177쪽 중2010년 책의 표지·서지·목차·서문6쪽(PDF1,3,4,5,7,8)과6장 전체11쪽(PDF93–103,인쇄91–101)의 추출문·판면을 읽었다. 다음 장 앞의 쪽번호 전용 PDF104도 시각 확인했다. 6장 첫 각주는1995년 Science Education79(2),189–199의 허가받은 약간 편집한 재수록이라고 명시한다. 심포지엄2009-10-09,책/서문2010,원논문1995,앞선 프랑스어 논문1994를 구별한다. 원학술지의 동일 판면·문구 전수 대조나 책177쪽 전체 독해는 아니다.'
LIMIT='과학/물리교육의 방법론적 논의이며 국내 수학교육의 효과 연구가 아니다. 본문은 인용 연구를 논의하지만 새 통합 표본이나 대조 효과크기를 제공하는 것으로 취급하지 않는다. 1995년 원학술지 PDF와1994년 프랑스어판·인용 원연구/원자료·나머지 책 본문·정오표는 미확인이다. 학생 말의 의미를 찾는 원칙은 모든 답을 정답으로 인정하거나 교사가 선호하는 해석을 만들어 넣는 허가가 아니다. 예상 시나리오·계산 예·지원 뒤 반응을 실제 독립 수행·학습 효과로 바꾸지 않는다. 전문 연구의 이론 개발을 모든 학교 탐구에 요구하지 않는다.'
SPECS={SOURCE:dict(stem='lijnse-symposium-2010',render_stem='lijnse',sha256=SHA,total=177,pages=TEXT,text_pages=TEXT,visuals=VISUAL,pdf_url=URL,url=URL,year=2010,title='Developmental research and didactical structure — authorized slightly edited 2010 reprint of the 1995 article, complete chapter 6',authors=['Piet Lijnse'],scope=SCOPE,limit=LIMIT,design='과학/물리교육의 내용별 교수설계에 대한 방법론적 논의와 기존 연구 인용',sample='6장에 새로운 통합 고유 참여자 수·표집 설계·효과크기를 제시하지 않는다. 서문의 심포지엄 사진은 학생 표본 자료가 아니다.',student_outcome_study=False,supports=['내용별 설계 가정과 실제 수행','학생 발언의 의미·교사 지원·해석 수정','원판·재수록본·사전 시나리오의 범위'],next_review='1995년 원학술지 PDF 및1994년 프랑스어판과의 차이·인용 원연구/원자료를 후속 대조하고, 자체 기록지의 실제 응답을 별도로 확인한다.')}
CLAIMS=[
 (SOURCE,'LJ10-01',[DE,PL,RU],[94,95,96,99,100,101,102],'내용의 논리적 순서와 실제로 배울 경로를 구별하고, 설계할 때 과제 간 연결·예상 행동·교사 지원의 이유를 적는다. 실행에서는 예상과 실제 자료를 비교해 가정을 고친다.','과학 맥락의 방법론을 수학 탐구 기록 설계에 참고한다. 실생활 소재·토론의 추가만으로 학습 경로가 검증되거나 모든 학생이 같은 단계를 거친다고 보장하지 않는다. 계획된 시나리오는 실제 관찰 결과가 아니다.'),
 (SOURCE,'LJ10-02',[RU,OU,RE],[97,98,99,100,101],'학생의 말·그림·행동과 관찰자의 해석을 구분하고, 앞뒤 과제와 후속 설명으로 뜻을 확인한다. 교사가 준 질문·힌트와 학생의 후속 반응을 함께 남겨, 다른 설명과 해석 수정의 근거를 검토한다.','단일 발언을 곧바로 고정된 오개념·독립 이해로 진단하거나 호의적인 추측으로 정답 처리하지 않는다. 의미 확인과 수학적 타당성 판단은 각각 필요하다. 실제 기록·외부 검토·수정 후 재확인이 없는 자체 예를 학생 검증으로 세지 않는다.')]

def task(n,codes,question,expected,interpretation):
 return dict(id=f'LJ10-P{n:02d}',standard_codes=codes,question=question,expected=expected,interpretation=interpretation,student_validated=False)
OBSERVATIONS={SOURCE:[
 task(1,[DE,PL],'분수의 정의→기호→계산 순서를 그대로 두고 피자 그림과 토론만 넣었다. 학습 경로가 검증됐는가?','소재·참여 방식과 학생이 다음 질문을 가질 이유·과제 사이의 개념적 연결을 따로 적는다. 어떤 생각을 예상하고 왜 다음 과제가 필요한지, 실제로 확인할 설명과 반례를 계획한다. 실제 실행 전에는 미검증으로 남긴다.','자체 설계 점검이다. 실생활 소재나 명시적 설명을 배제하는 일반 처방이 아니며 실제 수업 효과를 확보한 결과가 아니다.'),
 task(2,[RU,OU,RE],'같은 크기의 전체를3등분한1조각과2등분한1조각을 비교하며 가상 학생이 “3이 더 크잖아요”라고 했다. 곧바로1/3>1/2라고 믿는다고 기록해도 되는가?','발언을 그대로 남기고 무엇의 크기를 말했는지 묻는다. 등분 수3>2를 말했는지, 조각 크기를 말했는지는 이 한 문장으로 정하지 않는다. 같은 전체의 그림·수직선과 추가 설명으로 뜻을 확인하고 수학적으로는1/3<1/2임을 따로 판단한다.','가상 대화이며 실제 학생 응답이 아니다. 의미를 이해하려는 원칙은 잘못된 분수 부등식을 정답으로 바꾸는 것이 아니다.'),
 task(3,[PL,RU,RE],'“학생은 스스로 공통 단위의 필요를 느낀다”고 계획했다. 실제로는 교사가 공통 분모를 제시한 뒤 답을 얻었다면 어떻게 남길까?','계획의 예상, 실제 교사 발문·힌트, 그 뒤 학생의 말·그림, 달라진 해석을 나누어 적는다. 도움 뒤의 정답과 학생이 스스로 필요를 제기한 증거를 구별하고, 새 조건에서 확인할 설명을 계획한다. 아직 재확인하지 않았다면 미실행이다.','지원이 학습에 무가치하다는 뜻이 아니다. 지원 수준이 다른 수행을 같은 조건의 독립 수행이나 인과적 학습 향상으로 합치지 않는다.'),
 task(4,[LI],'이 출처의1994·1995·2009·2010과PDF93–103·인쇄91–101·학술지189–199는 각각 무엇인가?','1994는앞선프랑스어논문,1995는원학술지,2009-10-09는심포지엄,2010은책과서문의연도다. 읽은것은2010책의6장인쇄91–101(PDF93–103)과선정서지/서문이며1995학술지189–199의동일PDF나책177쪽전체가아니다.','약간 편집한 허가 재수록과 원학술지 동일본을 구별하는 자체 출처 과제다. 두 판본의 쪽수11쪽이 같다는 사실만으로 문구·판면 동일성을 확정하지 않는다.')
]}
DETAILS={SOURCE:dict(complete_reprint_chapter_read=True,original_1995_full_article_read=False,publisher_direct_pdf_obtained=False,pdf_pages=177,reprint_chapter_pdf_pages=list(range(93,104)),reprint_chapter_printed_pages='91–101',front_matter_pdf_pages=[1,3,4,5,7,8],page_number_only_visual_pages=[104],reprint_book_year=2010,reprint_book_isbn='978-90-73346-70-3',reprint_editors=['Koos Kortland','Kees Klaassen'],symposium_date='2009-10-09',preface_date='October2010',original_year=1995,original_journal='Science Education',original_volume=79,original_issue=2,original_pages='189–199',original_doi='10.1002/sce.3730790205',original_url=ORIGINAL,preceding_french_article_year=1994,preceding_french_article_pages='93–108',chapter_footnote='PDF93 footnote1: slightly edited version; reprinted with permission',no_numbered_chapter_figures_or_tables=True,entire_book_read=False,original_binary_fidelity_verified=False,raw_classroom_records_read=False,cited_originals_all_read=False,actual_independent_review=0,actual_student_validation=0,prior_slo_bibliographic_snapshot_preserved=True,unresolved_source_inconsistencies=[dict(location='PDF98/102',issue='Grandy/Hamilton body1993 versus reference1992; cited original not checked'),dict(location='PDF97/102',issue='Klaassen1994b is the historical source reference; do not silently rewrite it to the year of another edition')],own_tasks_are_not_student_responses=True)}
CORRECTIONS={SOURCE:[
 'SLO의Science Education29권을이출처에그대로옮기지않는다. 출판사서지와재수록각주는79(2),1995,189–199를가리킨다. 재수록책은2010이며2009는심포지엄이다.',
 '6장11쪽 전체를 읽었지만1995원판·1994프랑스어판·전체177쪽을읽었다고바꾸지않는다. PDF104는쪽번호102뿐이며본문쪽수에더하지않는다.',
 '원문의didactical structure는학문목차·검증완료선수관계·유일한학습순서와동일하지않다. 소규모실행과해석수정을요구하는설계관점으로참고한다.',
 '학생발언·관찰자해석·후속확인과수학적타당성판단을구별한다. 호의적해석만으로모든답을정답처리하지않고실제교사발문/도움도기록한다.',
 '서문의심포지엄사진은학생참여표본이아니며과거의평가·인용연구서술을현재의일반교수법효과로바꾸지않는다. 원문의예측/시나리오를실제검증기록으로채우지않는다.'
]}
INTERPRETATIONS={}
for rid in ['SEC_12수과03-01_C04','HP-inquiry-execution']:
 INTERPRETATIONS[rid,'LJ10-01']=('activity_context','과제·예상행동·지원의이유를계획에적고실제수행과비교해설계가정을수정한다.','내용의논리적순서·생활소재·예상시나리오만으로실제학습경로나효과를검증하지않는다.')
for rid in ['SEC_12수과03-02_C04','SEC_12수과03-03_C04','REV-12수과03-04-1','HP-inquiry-presentation','HP-inquiry-reflection']:
 INTERPRETATIONS[rid,'LJ10-02']=('activity_context','학생의실제말/행동·교사발문과도움·후속설명·처음해석과수정근거를구분해발표와성찰에남긴다.','단일발언이나지원뒤정답을독립이해로확정하지않고의미확인과수학적타당성판단을구별한다. 가상대화는실제학생검증이아니다.')

def main():
 if SOURCE not in load(ROOT/'data/literature_claim_reviews.json')['sources']:
  a=load(CACHE/'acquisition.json')
  assert a['sha256']==SHA and a['reading_completed'] and a['images_viewed']
  assert a['read_text_pages']==TEXT and a['viewed_image_pages']==VISUAL
  assert not a['original_1995_full_article_read'] and not a['entire_book_read']
 record(specs=SPECS,claims=CLAIMS,observations=OBSERVATIONS,details=DETAILS,corrections=CORRECTIONS,interpretations=INTERPRETATIONS,cache=CACHE,date=DATE,category='내용별설계·발언해석의허가재수록본대조',detail_key='authorized_reprint_review',roles={c[1]:'related_theoretical_context' for c in CLAIMS})

if __name__=='__main__': main()
