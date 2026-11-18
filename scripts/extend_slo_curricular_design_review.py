"""Extend the same SLO source to curricular-development chapter2."""
import copy
from literature_review import ROOT,load_registry,build_report,digest,target_value
from extend_lt2_length_assets_review import load,sha,write
from relation_literature_review import FILE,claim_snapshot,relation_snapshot,apply_literature_context
SOURCE='SLO_EDR_2013_INQUIRY_SELECTED';DATE='2026-11-17';CACHE=ROOT/'tmp/literature/slo-curricular-design-20261117'
PRIOR='data/literature_evidence/SLO_EDR_2013_learning_design_review_notes.json'
PRIOR_SHA='990b08d8d65b5eed930e7f1f1f8f56cbc3c7dea89ae8746a497a66592c25d112'
PRIOR_BIB='876cb30c0042ebe478ca987984783e6415296ee63bf308cd3cd71ae214f4084f'
NOTES='data/literature_evidence/SLO_EDR_2013_curricular_design_review_notes.json'
SHA='952ca654a1d44ed91cd9304e7d8386b3b7bbd0d7364a61c2c60dd41600f18110'
NEW_TEXT=list(range(54,72));NEW_VISUAL=list(range(53,73))
TITLE='Educational Design Research Part A: complete curricular-development, learning-design and formative-evaluation chapters2/3/6, selected introduction, revised November2013'
SCOPE='개정2013년 Part A206쪽 중 누적 추출문88쪽·판면93쪽을 대조했다. 새2장PDF53–72의 본문/참고문헌18쪽과20판면에서 교육과정의 층위·의도/실행/성취 표상·10구성 요소/그림1·선정/정합성·형성평가·조건부 설계 원리를 읽었다. PDF53사진·72머리말/쪽번호 전용 쪽은 본문 추출문 수에 넣지 않는다. 저자는van den Akker이며2009이전 장과2013개정 장을 구별한다. 기존3/6장전체·선정 도입의70텍스트/73판면 이력을 보존했다.2/3/6장 외는 선정 범위로 전권 독해가 아니다.'
LIMITS='교육과정 개발의 전문 관점을 학교 탐구·자료 검토에 자체 확장한다. 국가/학교/수업/개인 층위는 학습 선수 사슬이 아니고 문서·실행·경험·성과는 서로 다른 근거다. 원문2009이전 장·인용 원논문·원자료·Part A전권/Part B51사례·현장 운영/학습 결과·현재 국내 효과는 미확인이다.10구성 요소를 모든 학생의 고정 양식으로 강제하거나 탐구량을 늘리기만 하지 않는다. 원문의선택/자율 논의가 공식 성취기준·사용자 목표의 임의 축소를 허용하는 것은 아니다. 설계 원리는 맥락/근거를 포함하는 휴리스틱이지 성공 보장이 아니다.'
ME='12수과01-01';LI='12수과02-01';DE='12수과02-04';PL='12수과03-01';RU='12수과03-02';OU='12수과03-03';RE='12수과03-04'
def c(n,codes,pages,support,limit):return dict(id=f'SCD17-{n:02d}',source_id=SOURCE,role='related_theoretical_context',standard_codes=codes,locations=[f'PDF{p} / 인쇄{p-1}' for p in pages],support=support,does_not_establish=limit,independent_review=False,student_validated=False)
CLAIMS=[
 c(1,[ME,PL],[54,55,56,57],'탐구의 목적·계획 문서와 교사의 해석·실제 운영·학습자의 경험·학습 결과를 구별해 필요한 근거를 계획한다. 국가/학교/수업/개인의 검토 층위와 성취기준·자체 과제의 역할도 구분한다.','교육과정의 층위를 수학적 선수 순서로 바꾸지 않는다. 잘 쓴 문서나 사이트 게시만으로 실제 수업 운영·경험·성과를 확인했다고 하지 않는다. 원문의 일반 틀이 국내 공식 기준을 대신하지 않는다.'),
 c(2,[DE,PL],[58,59,60,62,63],'질문/목적과 내용·활동·교사의 지원·자료·모둠·장소·시간·평가가 서로 맞는지 개발 계획을 점검한다. 도구나 장소를 바꾸면 활동과 평가에서 무엇을 함께 조정할지 설명한다.','rationale을 포함한10요소를 열한 요소나 모든 학생의 의무 문항으로 바꾸지 않는다. 자료/ICT 제공만으로 실행과 학습의 변화가 보장되지 않으며 원문 그림을 실제 효과의 증거로 쓰지 않는다.'),
 c(3,[PL,RU],[60,61,62,63,64],'이번 탐구의 지식·사회적 의미·학습자 관심을 비교하고 시간/자원에 맞게 활동의 우선순위·선정/보류 이유를 적는다. 목표와 사전 판단 기준을 유지하며 실제 제약에 따라 방법을 수정한다.','모든 요구·새 기능을 더하는 것을 보완 완료로 세지 않는다. 한 활동의 범위 조정을 공식 성취기준이나 사용자가 요청한 전체 목표의 임의 삭제로 바꾸지 않는다. 특정한 개발 순서·기간을 일률적으로 강제하지 않는다.'),
 c(4,[OU,RE],[57,65,66,67],'문서의 정합성·실제 사용성·경험·학습 결과에 각각 어떤 근거가 있는지 보고/성찰한다. 초안 의견과 현장 사용 기록을 구별하고 다른 관점의 비판·수정 제안도 남긴다.2장의 품질 정의와6장 세부 구분의 강조점은 위치별로 기록한다.','재미있었다는 소감·전문가의 예상·문서 완성을 실제 이해나 효과의 근거로 합치지 않는다. 표본 수가 늘거나 자료 종류를 섞었다고 자동으로 대표성·인과·독립 검토가 생기지 않는다.'),
 c(5,[LI,RU],[65,66,67,68,69,70,71],'가져온 설계 원리의 목적·맥락·특징/절차·이론적 이유와 실제 근거를 구별하고 자신의 수정 이유를 기록한다. 다른 상황에 적용할 때는 평가 절차·구현 조건·미확인 범위를 함께 남긴다.','원문의 조건부 휴리스틱을 보편적 성공 절차로 바꾸지 않는다. 작은 목적 표집에서 모집단으로 통계적 일반화를 하거나 참고문헌 목록을 원논문/이전 판본 독해로 세지 않는다. 자체 적용을 검증된 새 이론으로 소개하지 않는다.'),
 c(6,[DE,RE],[59,60,63,64,65,66],'만든 자료의 요구·활동·평가가 같은 목표를 향하는지 자체 검토한다. 불일치가 있으면 무엇을 바꿀지 정하고 사용자 맥락·지원·자원 조건을 포함해 다시 확인할 계획을 남긴다.','개발한 산출물의 검사 통과와 실제 대상자의 실행/성취를 구별한다. 새 도구·자료·서식만 추가한 것을 모든 구성 요소의 정합성이나 실제 효과 검증 완료로 세지 않는다.')]
def p(n,code,q,e,i):return dict(id=f'SCD-P{n:02d}',standard_codes=[code],question=q,expected=e,interpretation=i,student_validated=False)
OBSERVATIONS=[
 p(1,ME,'학습 목표와 과제가 적힌 원고를 게시했다. 교사의 해석·실제 수업·학생 경험·학습 결과도 모두 확인됐다고 할 수 있는가?','의도한 문서와 게시 상태의 근거로 적는다. 실제 교사의 해석·운영 기록·학습자 경험/학습 자료는 별도 근거가 필요하고, 없는 것은 미확인으로 남긴다. 국가/수업/개인의 층위를 선수 사슬과 구별한다.','문헌의 표상 구분을 자체 점검에 확장한 질문이다. 실제 교사·학생 응답을 확보했다는 기록이 아니다.'),
 p(2,PL,'분수 설명 도구의 계획에서 내용과 자료만 정했다. 활동·도움·모둠·장소·시간·평가는 어떤 관계로 점검할 것인가?','왜/무엇을 배우는지와 어떤 활동·자료·지원·함께/따로 하기·장소/시간·확인 근거가 맞는지 검토한다. 한 요소를 바꿀 때 다른 요소에서 바꿀 점과 유지할 점을 설명한다.','10요소의 전문 틀을 모두의 고정 양식으로 강제하지 않는다. 계획을 적은 사실과 실제 실행/정합성 검증을 구별한다.'),
 p(3,PL,'한 번의 활동 시간에 새 기능·새 주제를 계속 더하자는 의견이 나왔다. 선정/보류와 후속 계획을 어떻게 정할 것인가?','현재 목표·필수 기준·학습자 관심·필요 근거와 시간/자원을 비교해 이번 활동의 우선순위와 보류 이유를 적는다. 전체 기준/목표를 지우지 않고 후속 범위를 따로 남긴다.','원문의 과부하/선택 논의를 자체 계획에 참고한다. 적게 하자는 말을 요청된 전체 목표를 축소하거나 근거 없이 검증을 생략하는 허가로 쓰지 않는다.'),
 p(4,RU,'종이 자료를 화면 도구로 바꾸면 다른 계획은 그대로 두어도 되는가?','어디서 누구와 어떤 조작/설명을 할지, 교사가 어떻게 돕고 시간을 얼마나 쓰며 무엇으로 이해를 확인할지 다시 점검한다. 화면 작동·자료 제공과 학습 변화는 별도 근거로 남긴다.','이는 가상 변경 상황이다. 실제 사용성/학습 효과를 확보한 사례나 ICT가 항상 우월하다는 주장이 아니다.'),
 p(5,RE,'사용자가 재미있었다고 말했다는 가상 기록만 있다. 학습 목표를 달성했다거나 실제 효과가 검증됐다고 적어도 되는가?','경험에 관한 가상 진술과 목표에 따른 풀이/설명·실제 수행·성과를 나눈다. 실제 자료가 없다면 경험과 성과 모두 미검증이며 어떤 근거로 다음에 확인할지 계획한다.','소감·예상 효과·실제 이해를 같은 것으로 채우지 않는다. 이 질문 자체가 실제 사용자의 응답 기록은 아니다.'),
 p(6,LI,'다른 맥락에서 제시한 설계 원리 한 줄을 가져왔다. 무엇을 확인하고 자신의 적용을 어떻게 구분할 것인가?','목적·맥락·특징·절차와 이론/실제 근거를 분리하고 읽은 쪽/판본·바꾼 부분·조건 차이·미확인을 적는다. 자신의 조건에서 추가로 시험할 부분을 계획한다.','원리의 조건을 떼어 보편적 성공 보장으로 쓰거나 참고문헌의 존재를 원논문 독해로 세지 않는다. 이전 판본·원자료·새 맥락의 효과는 별도다.'),
 p(7,DE,'자료 왜곡을 판단하는 설명이 목표인데 평가는 버튼 위치를 외우는 것뿐이다. 만든 자료를 어떻게 보완할 것인가?','목표와 평가가 맞지 않음을 지적하고 왜곡된 축·비교 기준·근거를 설명하는 과제와 평가 기준을 맞춘다. 조작 지원·시간·자료도 함께 검토하고 수정 전후와 재확인 범위를 남긴다.','이것은 자체 설계의 가상 불일치 사례다. 새 양식·조작 시험만으로 실제 학생 이해가 검증됐다고 하지 않는다.'),
 p(8,OU,'발표에 원고·실행 기록·소감·평가 결과를 함께 넣으려 한다. 무엇이 계획이고 어떤 근거가 실제로 있는지 어떻게 나타낼 것인가?','자료 종류·날짜·버전·출처·대상·실행 범위와 연결한 주장/한계를 적는다. 빈 실행 기록·예상 소감·가상 평가를 실제 근거로 채우지 않고 서로 다른 표상의 확인 상태를 구별한다.','문서·운영·경험·성과를 나누는 자체 보고 계획이다. 실제 외부 독립 검토·학생 검증 수를 늘리지 않는다.')]
INTERPRETATIONS={}
for rid in ['SEC_12수과01-01_C04','REV-12수과03-01-1','HP-inquiry-plan']:
 INTERPRETATIONS[rid,'SCD17-01']=('inference_limit','탐구의 목적·계획 문서와 실제 운영·학습자의 경험·성과에 필요한 근거를 나누어 계획한다.','문서 작성·게시를 실제 수업/경험/성과로 승격하지 않는다. 교육과정의 층위와 수학적 선수 순서는 다른 구분이다.')
for rid in ['SEC_12수과03-01_C04','HP-inquiry-execution']:
 INTERPRETATIONS[rid,'SCD17-03']=('activity_context','이번 활동의 목표·근거·시간/자원에 맞는 우선순위와 선정/보류 이유를 적고 실제 수행에 따라 계획을 수정한다.','활동의 범위 조정을 전체 공식 기준이나 요청된 전체 목표의 임의 삭제로 바꾸지 않는다. 기능을 더하는 것만으로 보완 완료를 판정하지 않는다.')
for rid in ['SEC_12수과03-03_C04','REV-12수과03-04-1','HP-inquiry-reflection']:
 INTERPRETATIONS[rid,'SCD17-04']=('inference_limit','문서의 정합성·실제 사용·경험·학습 결과의 서로 다른 근거와 수정 제안을 보고/성찰에 연결한다.','소감·예상·문서 완성을 실제 이해/효과와 합치지 않는다. 자료 수·종류를 늘렸다는 사실만으로 대표성·인과·독립 검토가 성립하지 않는다.')
for rid in ['SEC_12수과02-01_C04','REV-12수과02-01-1']:
 INTERPRETATIONS[rid,'SCD17-05']=('activity_context','읽은 설계 원리의 목적·맥락·절차·근거와 실제 적용/수정의 차이를 수행 기록에 남긴다.','조건부 휴리스틱을 보편적 성공 보장·모집단 일반화로 바꾸지 않는다. 참고 목록과 원논문/이전 판본 독해를 구별한다.')

def main():
 registry=load_registry();known={c['id'] for c in registry['claims']};newids={c['id'] for c in CLAIMS}
 if newids<=known:
  assert registry['sources'][SOURCE]['snapshot_file']==NOTES;build_report();return
 assert not newids&known
 s=registry['sources'][SOURCE];assert s['snapshot_file']==PRIOR and s['snapshot_sha256']==PRIOR_SHA and s['bibliography_snapshot']==PRIOR_BIB
 assert sha(ROOT/PRIOR)==PRIOR_SHA and sha(CACHE/'slo-design-part-a-2013.pdf')==SHA
 acquisition=load(CACHE/'acquisition.json');assert acquisition['reading_completed'] and acquisition['images_viewed'] and acquisition['read_text_pages']==NEW_TEXT and acquisition['viewed_image_pages']==NEW_VISUAL
 old_source=copy.deepcopy(s);old_notes=load(ROOT/PRIOR);old_claims=[copy.deepcopy(c) for c in registry['claims'] if c['source_id']==SOURCE];assert len(old_claims)==22 and len(s['observations'])==34
 assert not set(NEW_TEXT)&set(old_notes['selected_text_pages']) and not set(NEW_VISUAL)&set(old_notes['visual_pdf_pages'])
 images={str(p):sha(CACHE/f'rendered/slo-design-part-a-2013-{p}.png') for p in NEW_VISUAL}
 assert not {o['id'] for o in OBSERVATIONS}&{o['id'] for src in registry['sources'].values() for o in src.get('observations',[])}
 relations=load(ROOT/'data/revised_relations.json')['relations'];pairs={(x['id'],c['id']) for x in relations for c in CLAIMS if all(x[k].startswith('standard:') for k in ['from','to']) and {x[k][9:] for k in ['from','to']}<=set(c['standard_codes'])};assert pairs==INTERPRETATIONS.keys() and len(pairs)==10
 reviewed=load(ROOT/FILE);old_rows=[copy.deepcopy(x) for x in reviewed['records'] if x['claim_id'] in {c['id'] for c in old_claims}];assert len(old_rows)==25
 bibliography=load(ROOT/'data/sources.json');entry=next(x for x in bibliography if x['id']==SOURCE);old_entry=copy.deepcopy(entry);entry.update(title=TITLE,review_scope=SCOPE,does_not_establish=LIMITS,next_review=LIMITS)
 notes=copy.deepcopy(old_notes);notes.update(date=DATE,read_scope=SCOPE,selected_text_pages=sorted(old_notes['selected_text_pages']+NEW_TEXT),visual_pdf_pages=sorted(old_notes['visual_pdf_pages']+NEW_VISUAL),rendered_page_sha256={**old_notes['rendered_page_sha256'],**images},previous_review=old_source,previous_bibliography=old_entry,previous_claims=old_claims,previous_observations=copy.deepcopy(s['observations']),previous_relation_records=old_rows,previous_notes_file=PRIOR,previous_notes_sha256=PRIOR_SHA,reading_log=old_notes['reading_log']+['2026-11-17:2장 전체의 새 본문/참고문헌18쪽·판면20쪽을 실제 읽었다.53사진과72머리말/쪽번호 전용 쪽은 추출문 독해로 세지 않는다. 기존2/3/6장 구분과 읽기 이력을 보존한다.'],curricular_design_followup=dict(new_text_pages=NEW_TEXT,new_visual_pages=NEW_VISUAL,cumulative_text_pages=88,cumulative_visual_pages=93,chapter2_all_pdf_pages=NEW_VISUAL,chapter2_complete=True,chapter3_complete_with_prior_reading=True,chapter6_complete_with_prior_reading=True,all_part_a_read=False,part_b_read=False,cited_originals_read=False,earlier_2009_chapter_read=False,raw_data_reanalyzed=False,actual_implementation_verified=False,local_student_validation=False,own_plan_fields_not_validated_instrument=True),source_corrections=old_notes['source_corrections']+[dict(location='PDF53/72',issue='53은 사진·72는머리말/쪽번호만있는쪽이다. 본문 추출문독해에합산하지않는다.'),dict(location='PDF56–60 Boxes1/2 and Figure1',issue='교육과정층위와의도/실행/성취표상은학습선수사슬이아니다. rationale을포함한10요소와나머지9요소를구별한다.'),dict(location='PDF66–67 vs chapter6 PDF160–161',issue='2장의consistency정의에는state-of-the-art지식과구성요소연결이함께들어가고6장세부구분에서는최신지식을relevance에도명시한다. 장별정의의강조점을보존하며임의로하나의검증척도로통일하지않는다.'),dict(location='PDF68–69 generalization',issue='설계원리는목적/맥락/이론/실제근거를가진휴리스틱이며성공보장이아니다. 작은목적표집의일반화와통계적모집단일반화를구별한다.')])
 write(ROOT/NOTES,notes)
 history=s.get('snapshot_history',[])+[dict(snapshot_file=PRIOR,snapshot_sha256=PRIOR_SHA,date=old_source['date'],read_scope=old_source['read_scope'])]
 s.update(date=DATE,snapshot_file=NOTES,snapshot_sha256=sha(ROOT/NOTES),snapshot_history=history,bibliography_snapshot=digest(entry),read_scope=SCOPE,limits=LIMITS,method_note='2장전체와기존3/6장·선정도입을대조했다. 층위·표상·구성요소·장별품질정의·조건부원리를구별하고자체계획/평가를보완했다. 현장실행·국내학생효과의검증이아니다.',editorial_action='새주장6건·자체과제8개를더하고기존22주장·34과제와25개관계해석의이전원장을보존했다.',observations=s['observations']+copy.deepcopy(OBSERVATIONS),display={**s['display'],'title':TITLE})
 for claim in copy.deepcopy(CLAIMS):claim.update(empirical_scope=copy.deepcopy(s['empirical_scope']),target_snapshots={f'revision:{code}':digest(target_value(f'revision:{code}')) for code in claim['standard_codes']});registry['claims'].append(claim)
 by_claim={c['id']:c for c in registry['claims']};by_relation={x['id']:x for x in relations}
 for row in reviewed['records']:
  if row['claim_id'] in {c['id'] for c in old_claims}:row['claim_snapshot']=claim_snapshot(by_claim[row['claim_id']],s)
 for (rid,cid),(role,finding,limit) in INTERPRETATIONS.items():reviewed['records'].append(dict(relation_id=rid,claim_id=cid,role=role,finding=finding,limit=limit,relation_snapshot=relation_snapshot(by_relation[rid]),claim_snapshot=claim_snapshot(by_claim[cid],s)))
 apply_literature_context(relations,registry,registry=reviewed)
 queue=load(ROOT/'data/content_review_queue.json');row=next(x for x in queue['literature_review'] if x['source']['id']==SOURCE);row.update(source=entry,claim_ids=[c['id'] for c in registry['claims'] if c['source_id']==SOURCE])
 write(ROOT/'data/sources.json',bibliography);write(ROOT/'data/literature_claim_reviews.json',registry);write(ROOT/'data/content_review_queue.json',queue);write(ROOT/FILE,reviewed);build_report();print('Extended same SLO source:6 claims,8 own tasks,10 relation entries;all prior claims/tasks preserved')
if __name__=='__main__':main()
