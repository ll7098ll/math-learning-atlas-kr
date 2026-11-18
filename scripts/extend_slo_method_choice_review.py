"""Extend the same SLO2013 source with Kelly's complete method-choice chapter5."""
import copy
from fractions import Fraction
from literature_review import ROOT,load_registry,build_report,digest,target_value
from extend_lt2_length_assets_review import load,sha,write
from relation_literature_review import FILE,claim_snapshot,relation_snapshot,apply_literature_context
SOURCE='SLO_EDR_2013_INQUIRY_SELECTED';DATE='2026-11-17';CACHE=ROOT/'tmp/literature/slo-method-choice-20261117'
PRIOR='data/literature_evidence/SLO_EDR_2013_integrative_design_review_notes.json'
PRIOR_SHA='9272f9ab58d6dc1cb91e0e790a828985112c2e9aee7cea622f88393bbb2574c8'
PRIOR_BIB='0d586b9b09afe8d4da4159da93aa5fcecf037cef76b28c6e18b687a9d39cd9d0'
NOTES='data/literature_evidence/SLO_EDR_2013_method_choice_review_notes.json'
SHA='952ca654a1d44ed91cd9304e7d8386b3b7bbd0d7364a61c2c60dd41600f18110'
NEW_TEXT=list(range(136,152));NEW_VISUAL=list(range(135,153))
TITLE='Educational Design Research Part A: complete chapters2/3/4/5/6, selected introduction, revised November2013'
SCOPE='개정2013년 Part A206쪽 중 누적 추출문122쪽·판면131쪽을 대조했다. 새5장Kelly의PDF135–152 전체에서 연구 목적/방법·닫힌/열린/복합 문제·설계연구 적합성·평가 설계/측정과 재설계·이론/휴리스틱·참고문헌·사이버인프라 부록을 읽었다.135사진·152머리말/쪽번호 전용 쪽은 본문 추출문 수에 넣지 않는다. 기존2/3/4/6장 전체와 선정 도입의106텍스트/113판면 이력을 보존했다. 인용2006책의 저자 소속기관 서지와 USGS의지진예측FAQ를 보조 대조했으나 인용 원연구 전체·이전 판본 독해는 아니다.1/7장 등의 나머지는 선정 범위로 Part A전권 독해가 아니다.'
LIMITS='전문 교육설계 연구의 방법 선택·평가 문제를 자체 학교 수학 탐구에 참고한다. 모든 학생에게 복합 문제·새 이론·무작위시험을 요구하거나 닫힌 문제를 쉬운 문제로 바꾸지 않는다. 평가 목표/문항/분모/점수법 변경을 학습 향상으로 해석하지 않고 설계 휴리스틱·수학적 논증·실제 효과의 근거를 나눈다. 뇌/문해/조기대수/지진/LiDAR 사례와 당시 컴퓨팅·투자 수치는 현재 수업 처방·정확한 지진 예측·현행 인프라 성능이 아니다. 참고문헌2008과 본문2006의차이, Rittel/Webber1977호출의대응은 정확판본 미확인으로 보존한다. Part A전권/Part B51사례·인용 원논문/원자료·2009이전장·실제 독립/학생/시각 검증은 남는다.'
ME='12수과01-01';LI='12수과02-01';DE='12수과02-04';PL='12수과03-01';RU='12수과03-02';OU='12수과03-03';RE='12수과03-04'
def c(n,codes,pages,support,limit):return dict(id=f'SMC17-{n:02d}',source_id=SOURCE,role='related_theoretical_context',standard_codes=codes,locations=[f'PDF{p} / 인쇄{p-1}' for p in pages],support=support,does_not_establish=limit,independent_review=False,student_validated=False)
CLAIMS=[
 c(1,[ME,PL],[136,137,138,143,144],'탐구에서 설명·비교·평가·개발 중 무엇을 묻는지 밝히고 목적·대상·제약에 맞는 방법과 필요한 근거를 계획한다. 여러 방법의 이름을 나열하는 것과 질문에 답할 자료/분석을 실제로 확보하는 것을 구별한다.','이 장의 방법별 기능 목록을 모든 질문의 고정 처방이나 인과 보증으로 쓰지 않는다. 설계연구·설문·면담·시험이라는 이름만으로 대표성·타당성·실제 효과가 성립하지 않고 모든 학생에게 전문 연구 프로그램을 요구하지 않는다.'),
 c(2,[PL,RU],[137,138,139,140],'초기 상태·목표·허용하는 방법과 알려진 해결책을 확인하고, 해결 절차가 분명한 과제와 설계 대안/판단 기준 자체를 탐색할 과제를 나눈다. 실제 제약과 기존 해법의 한계를 근거로 방법을 고르고 수정한다.','원문의 닫힌 문제는 초기/목표/연산의 명확성에 관한 구분이지 쉽다는 뜻이 아니다. 체스의 예를 짧은 계산·항상 적은 자원으로 해결되는 문제로 바꾸지 않는다. 한 활동의 방법 선택을 공식 기준이나 사용자가 요청한 전체 보완 목표를 삭제하는 근거로 쓰지 않는다.'),
 c(3,[OU,RE],[142,143,144,145,150],'보고/성찰에서 무엇을 측정했는지와 평가 목표·문항·분모·판단 기준·버전을 밝힌다. 설계 과정에서 평가를 바꾸면 수정 이유와 새 판단의 근거를 남기고, 이전 결과와 직접 비교할 수 있는 범위를 따진다.','평가 목표가 발전한다는 말은 평가/근거를 생략해도 된다는 뜻이 아니다. 점수법·분모 변경에서 생긴 수치 상승을 학습 향상으로 세지 않는다. 휴리스틱·여러 하위 설명을 한 개의 검증된 보편 이론이나 인과 효과로 바꾸지 않는다.'),
 c(4,[LI,RU],[140,141,146,147,148,149,150,151],'선정 자료의 실제 주장·출판/확인 시점·조건·판본·보조 대조의 범위를 기록한다. 과학 기술의 발견과 학교 수업 적용, 지형/단층의 측정과 특정 시각/위치/규모의 지진 예측, 역사적 인프라 수치와 현행 성능의 차이를 설명한다.','원문은 뇌 연구에 대한 관심만으로 교수·학습 전략이 도출되지 않는다고 명시한다. LiDAR지형측정 사례를 정확한 미래지진예측 보장으로 쓰지 않는다.2006서지확인을2008정확쇄나원논문독해로 세지 않고 인용 불일치를 임의 복원하지 않는다.'),
 c(5,[DE,RE],[141,142,143,144,145,150],'개발 산출물의 수학적 조건/논증·작동·실제 이용·학습 설명에 대해 어떤 검토를 했는지 나누고, 재설계에 쓴 자료·다른 설명·판단 이유·새 버전 재확인 계획을 남긴다.','직사각형 넓이의 수학적 증명·시제품 작동·작성자의 판단이 실제 학습 효과나 새로운 교육이론을 입증하지 않는다. 설계연구에 여러 방법을 결합하거나 무작위시험을 예로 들었다고 학생의 모든 개발 과제에 같은 절차를 강제하지 않는다.')]
def p(n,code,q,e,i):return dict(id=f'SMC-P{n:02d}',standard_codes=[code],question=q,expected=e,interpretation=i,student_validated=False)
OBSERVATIONS=[
 p(1,ME,'모둠의 설명을 비교하는 질문, 도구의 작동을 확인하는 질문, 학습 효과를 묻는 질문에 같은 설문 하나면 충분한가?','목적과 대상·판단할 주장부터 나누고 실제 설명 자료·시험 입력/결과·학습 수행/비교 조건 등 필요한 근거를 고른다. 설문 반응을 모든 목적의 충분한 근거로 삼지 않는다.','방법의 명칭과 실제 근거를 구별하는 자체 가상 과제다. 설문이나 실험이라는 이름만으로 실제 수행·대표성·인과가 확인되지 않는다.'),
 p(2,PL,'원문이 닫힌 문제의 예로 든 체스는 항상 쉽고 짧은 시간에 풀리는가? 내 개발 과제의 방법은 무엇으로 고를 것인가?','초기/목표/허용 규칙이 알려져 있다는 구분과 계산 난도·필요 자원을 나눈다. 자신의 질문·기존 해법·제약·판단 기준이 얼마나 명확한지 근거로 필요한 방법을 정한다.','닫힌/열린 문제 구분을 우열·난도 등급이나 모든 과제에 설계연구를 강제하는 처방으로 쓰지 않는다. 이 과제는 체스를 해결한 결과가 아니다.'),
 p(3,OU,'동일한 설명에서 동등 가중의4조건 중3개를 충족했다. 실패한 조건만 빼고3조건으로 다시 채점하면75점에서100점이 된다. 학습이25% 향상됐는가?','각 조건 충족을[참,참,참,거짓]으로 고정하면3/4=75%,앞의3조건만으로는3/3=100%다. 차이는25퍼센트포인트이고 점수의 상대 증가는(100−75)/75=1/3이다. 둘 다 기준/분모 변경으로 생겼으며 응답이나 실제 학습이 바뀐 증거가 아니다. 기준·버전·빠진 조건을 기록한다.','자체 계산 반례이며 학생 점수가 아니다. 퍼센트포인트 차이와 상대 증가율도 구별한다. 이 비교는 학습 효과의 추정값을 제공하지 않는다.'),
 p(4,LI,'뇌 연구에 관심이 커졌다는 문장이나 지형측정 기술 사례만으로 수업 효과·정확한 지진 예측이 입증됐다고 써도 되는가?','원문의 기술·관심·적용 가능성 논의와 실제 수업 효과·특정 날짜/위치/규모의 예측 근거를 구별한다. 원문은 뇌 관심에서 교수법이 바로 도출되지 않는다고 쓰며, USGS의공식FAQ도 정확한 지진 예측과 확률적 전망을 구분한다.','문헌의 추론 범위를 대조하는 자체 질문이다. 뇌 연구/지진의 원자료를 재분석했거나 현재의 교수법·재난 대응을 추천하는 과제가 아니다.'),
 p(5,RU,'오래된 자료의컴퓨팅 성능·투자 계획과 참고연도2006/2008의차이를 발견했다. 수행 기록에 어떻게 남길 것인가?','원문의 시점·수치 단위·계획/실제 여부·출처·확인 날짜와 현재 미확인을 적는다. 본문/참고목록의2006/2008차이와 저자 소속기관의2006서지확인을 나누며 정확한2008쇄는 미확인으로 남긴다.','역사적 수치를 현재 성능으로 옮기거나 서지 대조를 원책 전체 독해로 세지 않는다. 불일치가 있다고 다른 판본의 가능성을 검증 없이 지우지 않는다.'),
 p(6,DE,'둘레20의직사각형 최대넓이를25로 증명했고 종이 도구의 계산도 맞았다. 도구의 학습 효과도 입증했는가?','양의 변과같은둘레라는 조건 아래 A=25−(x−5)²≤25라는 논증과 만든 도구의 작동 검토를 적는다. 실제 이용/풀이 설명/학습 변화에는 별도 자료와 조건 확인이 필요하다.','기존 자체 수학 모형에 근거 종류를 묻는 과제다. 수학적 증명의 참과 실제 학생 효과를 같은 것으로 세지 않는다.'),
 p(7,RE,'설명 활동을 고치면서 평가 문항·점수법도 바꿨다. 수정 전후의 숫자가 달라졌다는 사실만으로 더 좋은 활동이라고 보고해도 되는가?','자료·대상·과제·지원·버전·판단 기준과 바꾼 이유를 남긴다. 같은 뜻으로 비교할 수 있는지와 다른 설명을 검토하고 새 버전에서 필요한 재확인을 계획한다.','평가를 발전시키는 것과 사후에 유리한 기준만 고르는 것을 구별한다. 빈 계획·작성자 선호·점수 상승을 실제 검증이나 타당화된 척도로 바꾸지 않는다.')]
INTERPRETATIONS={}
for rid in ['SEC_12수과01-01_C04','REV-12수과03-01-1','HP-inquiry-plan']:
 INTERPRETATIONS[rid,'SMC17-01']=('activity_context','질문의설명·비교·평가·개발목적과대상·제약에맞는방법/근거를계획한다.','방법 이름만으로 대표성·실제 수행·인과가 확인되지 않으며 모든 학생에게 전문 연구 프로그램을 강제하지 않는다.')
for rid in ['SEC_12수과03-01_C04','HP-inquiry-execution']:
 INTERPRETATIONS[rid,'SMC17-02']=('activity_context','초기/목표/방법과기존해법·제약·판단기준을확인해과제에맞는실행방법을선택하고수정한다.','닫힌 문제를 쉽다고 단정하거나 방법 선택을 전체 공식 기준/사용자 목표를 삭제하는 허가로 쓰지 않는다.')
for rid in ['SEC_12수과03-03_C04','REV-12수과03-04-1','HP-inquiry-reflection']:
 INTERPRETATIONS[rid,'SMC17-03']=('inference_limit','평가목표·문항·분모·점수법·버전과변경이유를보고/성찰하고비교가능성을따진다.','평가 기준을 바꿔 생긴 점수 상승을 실제 학습 향상으로 세지 않는다. 평가의 발전이 근거를 생략하는 허가는 아니다.')
for rid in ['SEC_12수과02-01_C04','REV-12수과02-01-1']:
 INTERPRETATIONS[rid,'SMC17-04']=('inference_limit','과학기술사례·출판시점·판본·보조대조범위를수행기록에남기고적용의근거를구별한다.','뇌 연구 관심·LiDAR측정·과거 인프라 수치를 현재 교수법/정확한 지진 예측/현행 성능으로 승격하지 않는다.')

def main():
 registry=load_registry();known={c['id'] for c in registry['claims']};newids={c['id'] for c in CLAIMS}
 if newids<=known:
  assert registry['sources'][SOURCE]['snapshot_file']==NOTES;build_report();return
 assert not newids&known
 s=registry['sources'][SOURCE];assert(s['snapshot_file'],s['snapshot_sha256'],s['bibliography_snapshot'])==(PRIOR,PRIOR_SHA,PRIOR_BIB)
 assert sha(ROOT/PRIOR)==PRIOR_SHA and sha(CACHE/'slo-design-part-a-2013.pdf')==SHA
 acq=load(CACHE/'acquisition.json');assert acq['reading_completed'] and acq['images_viewed'] and acq['read_text_pages']==NEW_TEXT and acq['viewed_image_pages']==NEW_VISUAL
 old_source=copy.deepcopy(s);old_notes=load(ROOT/PRIOR);old_claims=[copy.deepcopy(c) for c in registry['claims'] if c['source_id']==SOURCE]
 assert len(old_claims)==34 and len(s['observations'])==50
 assert not set(NEW_TEXT)&set(old_notes['selected_text_pages']) and not set(NEW_VISUAL)&set(old_notes['visual_pdf_pages'])
 assert not {o['id'] for o in OBSERVATIONS}&{o['id'] for src in registry['sources'].values() for o in src.get('observations',[])}
 relations=load(ROOT/'data/revised_relations.json')['relations'];pairs={(x['id'],c['id']) for x in relations for c in CLAIMS if all(x[k].startswith('standard:') for k in ['from','to']) and {x[k][9:] for k in ['from','to']}<=set(c['standard_codes'])};assert pairs==INTERPRETATIONS.keys() and len(pairs)==10
 reviewed=load(ROOT/FILE);old_rows=[copy.deepcopy(x) for x in reviewed['records'] if x['claim_id'] in {c['id'] for c in old_claims}];assert len(old_rows)==45
 bibliography=load(ROOT/'data/sources.json');entry=next(x for x in bibliography if x['id']==SOURCE);old_entry=copy.deepcopy(entry);entry.update(title=TITLE,review_scope=SCOPE,does_not_establish=LIMITS,next_review=LIMITS)
 notes=copy.deepcopy(old_notes)
 notes.update(date=DATE,read_scope=SCOPE,selected_text_pages=sorted(old_notes['selected_text_pages']+NEW_TEXT),visual_pdf_pages=sorted(old_notes['visual_pdf_pages']+NEW_VISUAL),rendered_page_sha256={**old_notes['rendered_page_sha256'],**{str(p):sha(CACHE/f'rendered/slo-design-part-a-2013-{p}.png') for p in NEW_VISUAL}},previous_review=old_source,previous_bibliography=old_entry,previous_claims=old_claims,previous_observations=copy.deepcopy(s['observations']),previous_relation_records=old_rows,previous_notes_file=PRIOR,previous_notes_sha256=PRIOR_SHA,reading_log=old_notes['reading_log']+['2026-11-17:5장 전체의 새 본문/참고문헌/부록16쪽·판면18쪽을 실제 읽었다.135사진·152머리말/쪽번호 전용 쪽은 추출문 독해에 넣지 않는다. 연구 적합성·평가/측정의 변경·이론/휴리스틱·역사적 과학 사례의 한계를 구별했다.'])
 notes['method_choice_followup']=dict(new_text_pages=NEW_TEXT,new_visual_pages=NEW_VISUAL,cumulative_text_pages=122,cumulative_visual_pages=131,chapter5_all_pdf_pages=NEW_VISUAL,chapter5_complete=True,prior_complete_chapters=[2,3,4,6],all_part_a_read=False,part_b_read=False,cited_originals_read=False,earlier_2009_chapter_read=False,exact_2008_printing_verified=False,raw_data_reanalyzed=False,local_student_validation=False,actual_implementation_verified=False,external_checks_are_limited=True)
 notes['scope_boundary_checks']=[dict(url='https://research.utwente.nl/en/publications/educational-design-research-2/',kind='author institution bibliographic record',title='Educational design research',year=2006,isbn='0415396352',scope='metadata only; the exact2008printing and original book full text not read',checked_date=DATE),dict(url='https://www.usgs.gov/faqs/can-you-predict-earthquakes?cat=Advisories&id=101287&page=1&rc=1',kind='official scientific FAQ',title='Can you predict earthquakes?',page_updated_date='2026-11-04',scope='single FAQ text only; date/time, location and magnitude prediction distinguished from probabilistic forecasts; no linked research full text or raw data read',checked_date=DATE)]
 response=[True,True,True,False];old_score=Fraction(sum(response),len(response));new_score=Fraction(sum(response[:3]),len(response[:3]));assert old_score==Fraction(3,4) and new_score==1
 notes['own_scoring_counterexample']=dict(data_kind='own_synthetic_unchanged_response',response=response,old_equal_weight_criteria=[0,1,2,3],new_equal_weight_criteria=[0,1,2],old_score_percent=str(old_score*100),new_score_percent=str(new_score*100),difference_percentage_points=str((new_score-old_score)*100),relative_score_increase=str(new_score/old_score-1),actual_student_data=False,learning_effect_established=False)
 notes['source_corrections']=old_notes['source_corrections']+[
  dict(location='PDF135/152',issue='135사진·152머리말/쪽번호만있는쪽은 본문 추출문 수에 넣지 않는다. 이 장에는 별도 번호 그림/표가 없고 목록·참고문헌·부록을 실제 판면으로 대조했다.'),
  dict(location='PDF138–139',issue='닫힌/열린 구분은 초기/목표/방법의 명확성이지 난도 등급이 아니다. 전문 설계연구 적합성을 모든 학교 탐구의 의무 유형이나 전체 목표 축소로 바꾸지 않는다.'),
  dict(location='PDF142–145',issue='평가 목표·측정의 발전은 평가 생략 허가가 아니다. 기준/분모/점수법 변경과 학습 변화의 근거를 나누고 설계 휴리스틱·여러 하위 설명·수학적 증명·실제 효과를 구별한다.'),
  dict(location='PDF140–141 and PDF149–151',issue='뇌 연구 관심에서 교수법이 자동 도출되지 않는다는 원문의 제한을 보존한다. LiDAR측정과 정확한 지진 예측은 다르고 USGS단일FAQ로 이 추론 경계를 보조 대조했다. 과거 컴퓨팅·투자 계획은 현행 수치로 옮기지 않는다.'),
  dict(location='PDF136/148 and PDF138 bibliography calls',issue='van den Akker외 본문2006/참고2008차이를 보존한다. 저자 소속기관은2006서지를 제공하지만 정확한2008쇄·Rittel/Webber1977호출의대응·여러본문호출의미등재는 미확인이다. 임의로 연도/원문을 복원하지 않는다.')]
 write(ROOT/NOTES,notes)
 s.update(date=DATE,snapshot_file=NOTES,snapshot_sha256=sha(ROOT/NOTES),snapshot_history=s.get('snapshot_history',[])+[dict(snapshot_file=PRIOR,snapshot_sha256=PRIOR_SHA,date=old_source['date'],read_scope=old_source['read_scope'])],bibliography_snapshot=digest(entry),read_scope=SCOPE,limits=LIMITS,method_note='5장전체와기존2/3/4/6장·선정도입을대조했다. 목적/문제/방법·평가변경/측정·이론/휴리스틱·역사적사례의추론범위를구별하고자체채점반례를검산했다. 실제국내학생효과/원연구전체검증이아니다.',editorial_action='새주장5건·자체과제7개를더하고기존34주장·50과제와45관계해석의이전원장을보존했다.',observations=s['observations']+copy.deepcopy(OBSERVATIONS),display={**s['display'],'title':TITLE})
 for claim in copy.deepcopy(CLAIMS):claim.update(empirical_scope=copy.deepcopy(s['empirical_scope']),target_snapshots={f'revision:{code}':digest(target_value(f'revision:{code}')) for code in claim['standard_codes']});registry['claims'].append(claim)
 by_claim={c['id']:c for c in registry['claims']};by_relation={x['id']:x for x in relations}
 for row in reviewed['records']:
  if row['claim_id'] in {c['id'] for c in old_claims}:row['claim_snapshot']=claim_snapshot(by_claim[row['claim_id']],s)
 for (rid,cid),(role,finding,limit) in INTERPRETATIONS.items():reviewed['records'].append(dict(relation_id=rid,claim_id=cid,role=role,finding=finding,limit=limit,relation_snapshot=relation_snapshot(by_relation[rid]),claim_snapshot=claim_snapshot(by_claim[cid],s)))
 apply_literature_context(relations,registry,registry=reviewed)
 queue=load(ROOT/'data/content_review_queue.json');row=next(x for x in queue['literature_review'] if x['source']['id']==SOURCE);row.update(source=entry,claim_ids=[c['id'] for c in registry['claims'] if c['source_id']==SOURCE])
 write(ROOT/'data/sources.json',bibliography);write(ROOT/'data/literature_claim_reviews.json',registry);write(ROOT/'data/content_review_queue.json',queue);write(ROOT/FILE,reviewed);build_report()
 print('Extended same SLO source:5 claims,7 own tasks,10 relation entries;prior claims/tasks and interpretations preserved')
if __name__=='__main__':main()
