"""Extend the actually read teaching body; preserve prior claims and licensed PDF."""
import copy,hashlib,json
from literature_review import ROOT,digest,target_value,load_registry,build_report
from relation_analysis_review import load_reviews
from record_ies_early_literature_review import SOURCE,SHA,PAGES,VISUAL,RATINGS

NEW_TEXT=sorted((set(range(1,65))-set(PAGES))|set(range(98,107)))
NEW_VISUAL=[3,11,12,27,28,35,36,37,49,50,51,55,56,57,58,59,60,63,64,100,101,102,103,104,105,106]
TEXT=sorted(set(PAGES+NEW_TEXT));IMAGES=sorted(set(VISUAL+NEW_VISUAL))
SCOPE='누적81쪽 텍스트·32쪽 전체 페이지 이미지와 미주78/252 해당 대목을 확인. PDF1–64의 도입·권고1–5 교수 본문·용어집과 선정 근거 부록·Table D5를 읽었다. 전체165쪽·모든 부록·원연구 정독은 아니다.'
OBS=[
 dict(id='IE-P7',standard_codes=['2수01-01','2수01-04','2수01-05'],question='빨간 구슬 3개와 파란 구슬 2개를 합친 모임을 실물·그림·식으로 나타내라. 그중 파란 2개를 치우면 몇 개가 남는가? 식의 각 수와 기호가 무엇을 나타내는지 가리키거나 말하라.',expected='합치면 5개로 3+2=5이고,파란 2개를 치우면 빨간 3개가 남아 5−2=3이다. 그림의 표식은 구슬에 하나씩 대응하며 같은 구슬을 그림에도 그렸다고 실물과 그림을 더해 10개로 세지 않는다. 등호 양쪽은 같은 개수를 나타낸다.',interpretation='양의 파악·일대일 대응·그림·기호 읽기·설명 방법과 도움을 따로 기록한다. 말하기나 그리기의 어려움만으로 수량 이해 부재를 확정하지 않고 가리키기·실물 이동 등 다른 표현도 확인한다. +·−·=는 현재 기준 범위의 자체 예이며 원문의 부등호를 새 필수 기호로 추가하지 않는다. 실제 학생 검증은 없다.',student_validated=False),
 dict(id='IE-P8',standard_codes=['2수01-01'],question='1부터 10까지 한 칸에 한 수가 적힌 띠에서 말을 2에 두었다. 새로 들어가는 칸만 하나씩 세며 앞으로 3칸,이어서 1칸 움직여라. 처음부터 1에서 3칸 움직인 경우와 도착한 수가 같은가?',expected='2에서 새 칸 3·4·5로 3칸 이동해 5에 도착하고,다음 한 칸은 6이다. 1에서 3칸 움직이면 2·3·4를 지나 4에 도착한다. 출발 칸을 첫 이동 칸으로 다시 세지 않는다. 도착한 수 5와 이동한 칸 수 3은 역할이 다르다.',interpretation='미리 정한 이동이며 실제 주사위 실험이나 학생 결과가 아니다. 개인별 이동·발화·중복·누락·출발점과 도착점을 관찰하고 게임 승패·시간·집단 정답을 개인 숙달로 바꾸지 않는다. 이 작은 수 예는 0~100 전체나 어떤 놀이든 효과가 있다는 검증이 아니며 가이드의 3–6세 범위를 유지한다.',student_validated=False)]
MAPPINGS=[
 ('IE08',OBS[0]['standard_codes'],4,['PDF48–52 / printed42–46','PDF63–64 / printed57–58'],'실물·그림·말과 수·연산 기호를 같은 수량 관계에 대응하고,여러 표현과 열린 질문으로 설명을 관찰하는 자체 설계에 참고한다.','권고4는 Minimal이다. 다요소 개입의 결과를 특정 발문·그림·기호 활동만의 인과 효과로 귀속하지 않는다. 언어 산출이나 그림 표현의 어려움을 수량 개념 부재와 동일시하지 않고 현재 한국 초등 발문의 진단 정확도·번역 동등성을 입증했다고 하지 않는다.'),
 ('IE09',OBS[1]['standard_codes'],5,['PDF53–62 / printed47–56','PDF27 / printed21','PDF63–64 / printed57–58'],'목표에 맞는 놀이·일상 활동에서 수량·수 이름·일대일 대응을 개인별로 관찰하고 다음 활동을 조정하는 설계에 참고한다.','권고5는 Minimal이다. 특정 숫자판 연구를 모든 놀이·모든 수학 영역의 효과나 고정된 일일 수업 시간의 처방으로 확대하지 않는다. 승패·참여 시간·집단 수행으로 개인 숙달을 판정하지 않으며 현재 학생 효과나 필수 선수 순서의 검증으로 쓰지 않는다.')]

def verify():
 assert len(NEW_TEXT)==45 and len(TEXT)==81 and len(IMAGES)==32 and set(NEW_VISUAL)<=set(TEXT)
 assert 3+2==5 and 5-2==3
 assert list(range(3,6))==[3,4,5] and 2+3+1==6 and 1+3==4

def main():
 verify();registry=load_registry();s=registry['sources'][SOURCE]
 if 'reading_extension' in s:
  assert {c[0] for c in MAPPINGS}<={c['id'] for c in registry['claims']}
  print('Early-math extension remains current; no automatic refresh');build_report();return
 assert s['snapshot_kind']=='source_pdf' and s['snapshot_sha256']==SHA and s['text_pdf_pages']==PAGES and s['evidence_ratings']==RATINGS
 assert not {c[0] for c in MAPPINGS}&{c['id'] for c in registry['claims']}
 before=copy.deepcopy(registry);relations=copy.deepcopy(load_reviews())
 bpath=ROOT/'data/sources.json';bibliography=json.loads(bpath.read_text(encoding='utf-8'));b=next(x for x in bibliography if x['id']==SOURCE)
 previous_bibliography=copy.deepcopy(b);b['review_scope']=SCOPE
 b['next_review']='미검토 부록A–C·근거 부록의 나머지 연구표D1–4/D6–8·미주와 참고문헌 전체·원연구·당시 프로토콜·정오표를 후속 대조한다. 측정 연구 수9/10과 EPIC 목록 차이는 확인 전 수치 인용 보류. 실제 학생 응답과 한국어 진단 정확도는 미검증이다.'
 log=['기존36쪽 외45쪽을 읽어 누적81쪽 텍스트를 확인했다. 도입·권고1–5 교수 본문·용어집 PDF1–64의 텍스트 범위는 모두 포함하나 전체165쪽을 읽었다는 뜻은 아니다.',
 '새26쪽 이미지를 실제 대조해 누적32쪽이다. 연구표D5 PDF100–106의 열·범례·주석1–25와 앞 문맥98–99를 읽고 대조했다.',
 '권고4·5의 Minimal,다요소 개입과 불명확한 비교 처치,언어·표현·개념의 구별을 유지한다. 원문 부등호·원그래프·미국 단위·수업 시간 예를 현재 학년의 새 필수로 옮기지 않는다.',
 'D5의 Positive는 통계적 유의 또는 효과크기0.25SD 이상이므로 ns가 붙은 Positive를 통계적으로 유의하다고 쓰지 않는다. ?는 비교 수업 정보 부족이며 미지도 확정이 아니다. X는 구성 요소 포함으로 개별 요소의 독립 효과를 뜻하지 않는다.',
 'PDF103의 PCER2008 제2장 두 비교는 각각 같은 수100의 비교 집단을 표시하지만,그 사실만으로 원연구의 참여자 동일성·저자의 계수 의도를 확정하지 않는다. 표본·비교·결과·측정 시점을 독립 연구로 합산하지 않는다.',
 '측정 서술은9/10편·7개 개입을 제시하지만 D5에는 EPIC의 측정 열에도 X가 있다. EPIC 포함 여부와 계수 단위 차이를 추가로 확인해야 하므로 단순9연구/10비교로 해결했다고 하지 않는다.',
 '지도의 다섯 내용 영역과 여섯 결과 영역을 구별한다. 측정 포함 교육과정의 일반 수리력 결과를 측정 단독 성취나 특정 활동의 효과로 바꾸지 않는다. LOGO의 바닥형/컴퓨터형 대조는 둘 다 LOGO를 받은 비교다.']
 comparisons=[('Clements_Sarama_2007b','Building Blocks','X'),('Clements_Sarama_2008','Building Blocks','?'),('Clements_2011','Building Blocks','X'),('Fantuzzo_2011','EPIC','X'),('Klein_2008','Pre-K + DLM','X'),('PCER_2008_ch2','Creative Curriculum','?'),('PCER_2008_ch2','Bright Beginnings','?'),('PCER_2008_ch3','Creative Curriculum','?'),('Sarama_2008','Building Blocks + Pre-K','?'),('Sophian_2004','researcher-developed measurement curriculum','X'),('Weaver_1991','LOGO','X')]
 assert len(comparisons)==11 and len({r[0] for r in comparisons})==10 and len({r[1] for r in comparisons})==8
 discrepancy=dict(locations=['PDF32 / printed26','PDF96 / printed90','PDF98–106 / printed92–100','PDF142 endnote78 only','PDF151 endnote252 only'],issue='측정 연구 수 본문9/부록10 및 서술7개 개입과 TableD5 EPIC 측정 열 포함의 차이',status='table_checked_counting_intent_unconfirmed',followup='D5의 측정 열이 표시된 비교 행11개·인용/PCER장 단위10개·명칭8종은 표를 세는 자체 기록이다. 독립 연구 수나 저자의9/10 계수 의도와 동일하지 않다. 원연구·해당 미주 전체·정오표 확인 전 연구 수와 개입 수의 확정 인용을 보류한다.')
 notes=dict(source_id=SOURCE,source_url=s['display']['url'],source_pdf_sha256=SHA,contains_source_full_text=False,licensed_source_pdf_preserved=True,previous_review=copy.deepcopy(s),previous_bibliography=previous_bibliography,new_text_pdf_pages=NEW_TEXT,new_visual_pdf_pages=NEW_VISUAL,cumulative_text_pdf_pages=TEXT,cumulative_visual_pdf_pages=IMAGES,cumulative_read_scope=SCOPE,unread_full_pdf_pages=sorted(set(range(1,166))-set(TEXT)),reading_log=log,source_corrections=[discrepancy],measurement_table_audit=dict(location='PDF100–106 / TableD5',rows=[dict(citation_unit=a,intervention=b,measurement_column=c) for a,b,c in comparisons],comparison_rows=11,citation_or_chapter_units=10,intervention_names=8,counts_are_independent_studies=False,author_counting_intent_confirmed=False),new_image_sha256={str(p):hashlib.sha256((ROOT/f'tmp/literature/ies-early-2013-p{p}.png').read_bytes()).hexdigest() for p in NEW_VISUAL})
 rel='data/literature_evidence/IES_EARLY_2013_extension_review_notes.json';file=ROOT/rel;file.write_text(json.dumps(notes,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 s.update(date='2026-11-06',bibliography_snapshot=digest(b),reading_extension=dict(file=rel,sha256=hashlib.sha256(file.read_bytes()).hexdigest()),text_pdf_pages=TEXT,visual_pdf_pages=IMAGES,read_scope=SCOPE,reading_log=s['reading_log']+log,source_discrepancies=[discrepancy],limits='전체165쪽 중81쪽 텍스트와32쪽 이미지의 자체 읽기다. 미검토 부록·전체 미주·참고문헌·원연구·원자료·당시 프로토콜·정오표는 후속 대조가 필요하다. 한국 초등 전체의 진단 정확도·번역 동등성·학생 효과·필수 선수 방향을 입증하지 않는다. 측정 연구 수9/10은 연구표 대조 후에도 계수 의도와 EPIC 포함 여부가 확인되지 않아 수치 인용을 보류한다.',editorial_action='기존 주장7건·자체 관찰6건을 보존하고 권고4·5의 주장2건·자체 관찰2건을 더했다. 누적9건·8건이며 새 관계 검토·독립 검토·학생 검증으로 합산하지 않는다.',observations=s['observations']+OBS)
 for cid,codes,n,locations,support,limit in MAPPINGS:
  registry['claims'].append(dict(id=cid,source_id=SOURCE,role='instructional_recommendation_with_evidence_scope',locations=locations,support=support,does_not_establish=limit,target_snapshots={'revision:'+c:digest(target_value('revision:'+c)) for c in codes},standard_codes=codes,independent_review=False,student_validated=False,local_effect_tested=False,recommendations=[dict(number=n,evidence_rating=RATINGS[str(n)],application_limit=limit)]))
 for name,value in [('sources',bibliography),('literature_claim_reviews',registry)]:
  (ROOT/f'data/{name}.json').write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 qpath=ROOT/'data/content_review_queue.json';q=json.loads(qpath.read_text(encoding='utf-8'));row=next(v for v in q['literature_review'] if v['source']['id']==SOURCE);row.update(source=b,claim_ids=[v['id'] for v in registry['claims'] if v['source_id']==SOURCE]);qpath.write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 assert registry['claims'][:len(before['claims'])]==before['claims'] and s['observations'][:6]==before['sources'][SOURCE]['observations']
 assert load_reviews()==relations
 build_report();print('Extended early-math teaching body: 2 claims,2 own observations; original PDF and prior claims preserved')

if __name__=='__main__':main()
