"""Extend the existing SLO2013 source with Bannan's complete chapter4."""
import copy
from literature_review import ROOT, load_registry, build_report, digest, target_value
from extend_lt2_length_assets_review import load, sha, write
from relation_literature_review import FILE, claim_snapshot, relation_snapshot, apply_literature_context

SOURCE='SLO_EDR_2013_INQUIRY_SELECTED'; DATE='2026-11-17'
CACHE=ROOT/'tmp/literature/slo-integrative-design-20261117'
PRIOR='data/literature_evidence/SLO_EDR_2013_curricular_design_review_notes.json'
PRIOR_SHA='0253158b434feeb048fd444f707fcab573f1328f171791934eb2899c38ce9bd5'
PRIOR_BIB='778afdb5691dce8f261b306e326df738d4c4920faabb6fd48a9c765ee8b1307a'
NOTES='data/literature_evidence/SLO_EDR_2013_integrative_design_review_notes.json'
SHA='952ca654a1d44ed91cd9304e7d8386b3b7bbd0d7364a61c2c60dd41600f18110'
NEW_TEXT=list(range(116,134)); NEW_VISUAL=list(range(115,135))
TITLE='Educational Design Research Part A: complete chapters2/3/4/6, selected introduction, revised November2013'
SCOPE='개정2013년 Part A206쪽 중 누적 추출문106쪽·판면113쪽을 대조했다. 새4장Bannan의PDF115–134 전체에서 ILDF의4단계/반복과 그림1·2, LAO의요구/대상자 분석·시제품·국소 평가·미완료 확산·참고문헌을 확인했다.115사진·134머리말/쪽번호 전용 쪽은 본문 추출문 수에 넣지 않는다. 기존2/3/6장 전체와 선정 도입의88텍스트/93판면 이력을 보존했다.2/3/4/6장 외는 선정 범위이며 전권 독해가 아니다. 인용2편은 출판사 서지의 쪽수만 대조했고 원논문 독해로 세지 않는다.'
LIMITS='ILDF와 LAO는 전문 설계연구의 틀과 역사적 문해 지원 사례다. 학교 수학 탐구에 자체 확장한 질문을 문해 효과·국내 학생 효과·실제 독립 검증으로 세지 않는다.5쌍/8쌍의 별도 탐색과 계획된50쌍 초과 현장 시험·100명 초과 잠재 채택자를 구별하며 합산 표본·확정 채택·학습 성과로 바꾸지 않는다. 인용 원논문/원자료·2009이전 장·Part A전권/Part B51사례·LAO 실제 실행·국내 학생 응답은 미확인이다. 본문의Table1 호출에 대응하는 표는 이 장의 실제 판면에서 찾지 못했고 자료를 복원하지 않는다. ILDF/IDLF 표기와 형성평가를 구분하는 저자의 관점을 위치별로 보존한다.'
ME='12수과01-01';LI='12수과02-01';DE='12수과02-04';PL='12수과03-01';RU='12수과03-02';OU='12수과03-03';RE='12수과03-04'

def c(n,codes,pages,support,limit):
 return dict(id=f'SID17-{n:02d}',source_id=SOURCE,role='related_theoretical_context',standard_codes=codes,locations=[f'PDF{p} / 인쇄{p-1}' for p in pages],support=support,does_not_establish=limit,independent_review=False,student_validated=False)

CLAIMS=[
 c(1,[ME,PL],[116,117,118,119,120],'탐구의 질문·자료·분석·설계 결정이 어떻게 연결되는지 기록하고, 시제품 개선과 학습자/맥락에 대해 얻은 지식을 구분한다. ILDF는 탐색·구현·국소 영향 평가·더 넓은 영향 평가를 반복적으로 연결하는 전문 연구 틀로 참고한다.','4단계를 모든 학생의 고정 시간표·수학적 선수 사슬로 바꾸지 않는다. 문서·시제품·게시만으로 연구/학습 성과가 성립하지 않고, 형성평가와 설계연구의 차이를 설명하는 이 장의 관점을 모든 평가 활동에 대한 보편 판정으로 쓰지 않는다.'),
 c(2,[DE,PL],[121,123,124,129,130],'만든 자료가 어떤 학습 추측·목표·과제 분석을 구현하고 어떤 질문/자료로 검토할지 연결한다. 종이 모형·시제품의 입력과 설명을 먼저 검토하고 의견/근거에 따른 수정 결정을 남긴다.','그림2는 설계의 추측·목표·평가 질문을 잇는 도식이지 효과 크기나 실제 달성 결과가 아니다. 그림을 수학적 인과 사슬·검증된 평가 척도로 바꾸지 않으며 없는Table1의 결과를 채우지 않는다.'),
 c(3,[PL,RU],[121,122,123,124],'처음 가정한 대상·사용 상황과 실제로 얻은 관찰/의견이 다르면 후속 자료를 모아 탐구 방향과 지원을 수정한다. 실제 자료에서 만든 합성 대상자 프로필과 자료 없이 만든 가상 인물을 구별한다.','원문은 한 부모의 발언 뒤에 추가 면담·조사와 분석이 있었다고 보고한다. 한 발언만으로 전체 요구가 증명됐다고 하지 않는다. 원문의합성 프로필을 자신의 실제 참여자·대표 표본으로 옮기거나 가상 인물을 실제 응답자로 세지 않는다.'),
 c(4,[OU,RE],[125,126,127,128,130,131],'보고/성찰에서 실제 수행한 소규모 탐색, 앞으로 할 현장 시험, 잠재 이용자 추적, 실제 채택·학습 결과의 확인 상태를 나눈다. 버전·도움·장소·대상에 따라 주장 가능한 범위를 밝힌다.','LAO의5쌍과8쌍은 별도 연구이고 중복 여부를 알 수 없어13명/13쌍으로 합산하지 않는다.50쌍 초과는 당시 계획이고100명 초과는 잠재 채택자이지 실제 학생 성과 표본이 아니다. 이 수치를 우리 사이트의 독립/학생 검증 수로 더하지 않는다.'),
 c(5,[LI,RU],[118,119,129,132,133],'인용한 문헌의 저자·연도·쪽수·그림/표 호출을 실제로 대조한 범위와 원문이 보고한 범위로 나누어 적는다. 출판사 서지 대조·원논문 독해·원자료 재분석을 구별하고 불일치와 후속 확인을 남긴다.','이 장의참고문헌은DBRC2003을21–24쪽으로 적지만 출판사 서지는5–8쪽이며21–24쪽은Bannan-Ritland2003이다. 서지 정정을 논문 본문 검증으로 세지 않는다. Table1 호출과 없는표·Jeffs2000 호출의 대응·ILDF/IDLF 오기를 임의의 데이터/연구로 복원하지 않는다.'),
 c(6,[DE,RE],[125,126,127,128,130,131],'개발 시험에서 관찰한 상호작용·지원 조건·불편과 분석 결과를 수정 또는 보류 결정에 연결하고, 바꾼 시제품에서 재확인할 부분을 정한다. 작동·사용성·소감·학습 설명·넓은 적용의 근거를 분리한다.','복합 지원이 함께 있는 사례에서 특정 기능 하나의 인과 효과를 분리했다고 하지 않는다. 연구자 도움이 많은 사용·워크숍·현장 사용은 같은 조건이 아니고, 개선 사례·긍정 소감·배포 성공만으로 다른 수학 과제/대상의 효과를 보장하지 않는다.')]

def p(n,code,q,e,i):return dict(id=f'SID-P{n:02d}',standard_codes=[code],question=q,expected=e,interpretation=i,student_validated=False)
OBSERVATIONS=[
 p(1,ME,'탐구 도구를 만들고 게시했다. 무엇을 개선했고 학습/사용 맥락에 대해 무엇을 알았는지도 모두 확인됐는가?','만든 것·작동 검사·게시와 실제 사용/학습 자료를 나눈다. 질문→자료→분석→설계 결정의 연결을 설명하고 확보하지 않은 근거는 미확인으로 남긴다.','전문 ILDF의 관점을 자체 학교 탐구에 참고한 가상 질문이다. 모든 학생에게 새 이론이나4단계 연구 프로그램을 요구하지 않는다.'),
 p(2,PL,'자료 왜곡을 설명하게 할 도구의 목표를 정했다. 추측·과제·시제품·확인 질문을 어떻게 연결할 것인가?','어떤 설명을 기대하는지와 과제/입력·시제품의 해당 표현·실제로 볼 풀이/말·판단 기준을 연결한다. 조작 성공과 왜곡의 근거 설명은 다른 확인 질문으로 남긴다.','원문 그림2를 자체 수학 개발 계획에 확장한다. 도식의 화살표나 계획을 실제 학습 향상·인과 증거로 세지 않는다.'),
 p(3,RU,'가상 설계 회의에서 한 사람이 함께 쓰는 도구가 필요하다고 말했다. 곧바로 모든 대상자의 요구라고 정할 수 있는가?','그 발언을 하나의 가설/관점으로 남기고 다른 대상·실제 과제에서 후속 관찰/면담과 기존 자료를 대조해 수정 여부를 판단한다.','원문에서도 한 부모의 발언 뒤에 후속 자료 수집과 분석이 있었다. 이 가상 회의를 실제 외부 검토로 기록하지 않는다.'),
 p(4,PL,'서로 다른 인터뷰에서 얻은 특징을 합친 프로필과 인터뷰 없이 만든 가상 인물이 있다. 참여자 수와 근거를 어떻게 적을 것인가?','합성 프로필은 근거가 된 실제 자료의 범위·합친 특징·빠진 관점과 구별해 적고 새로운 실제 응답자 한 명으로 세지 않는다. 가상 인물은 가상이라고 표시한다.','합성/가상 프로필은 실제 학생 응답·대표 표본·검증 인원을 늘리지 않는다. 이 과제 자체에는 인터뷰 자료가 없다.'),
 p(5,OU,'보고서에 별도 연구5쌍·8쌍, 앞으로50쌍 초과 시험 계획,100명 초과 잠재 이용자 추적이 나온다. 총 검증 학생 수는 얼마인가?','서로 단위·실행 상태·대상/중복이 달라 합산할 수 없다. 쌍을 학생 수로 바꾸거나 계획·잠재 이용자를 실제 성과 측정 표본으로 세지 않고 각 근거와 한계를 분리한다.','원문 사례 수치의 지위를 해석하는 자체 과제다. 우리 사이트의 실제 학생·독립 검증은 늘어나지 않는다.'),
 p(6,LI,'인용 목록의DBRC2003 쪽수21–24와 출판사 서지5–8이 다르다. 무엇을 정정하고 어디까지 읽었다고 할 것인가?','원목록의 표기·출판사 정정 쪽수/DOI·확인 날짜·범위를 기록한다.21–24쪽의Bannan-Ritland2003과 구별하며 서지 확인을 두 원논문의 전체 독해로 기록하지 않는다.','출판사 메타데이터만 대조한 정정이다. 없는Table1이나 불명확한 연도 호출의 자료를 만들어 넣지 않는다.'),
 p(7,DE,'분수 도구에 설명·공동 사용·음성 지원을 함께 바꾸고 도움이 된다는 소감만 얻었다는 가상 사례다. 음성 지원의 학습 효과를 입증했는가?','동시에 바뀐 요소·지원자 도움·과제/버전과 소감의 범위를 밝힌다. 어느 요소의 효과인지 분리되지 않았고 실제 이해 확인/다른 설명/새 버전 시험이 필요함을 적는다.','문해 지원 사례의 방법론적 한계를 자체 수학 도구에 확장한 질문이다. 임의의 효과 크기·인과 결과를 만들지 않는다.'),
 p(8,RE,'연구자가 계속 도와준 시연과 다른 학교에서 도움 없이 쓰는 경우를 같은 사용성/학습 효과라고 보고해도 되는가?','장소·과제·버전·지원의 범위를 구별한다. 시연의 관찰을 실제 현장 전체로 넓히지 않고 다른 조건에서 어떤 재확인이 필요한지 적는다.','실제 다른 학교의 사용이나 독립 검토를 수행했다는 기록이 아니다. 공개·잠재 이용·채택·학습 성과는 각각 별도 근거를 요구한다.')]

INTERPRETATIONS={}
for rid in ['SEC_12수과01-01_C04','REV-12수과03-01-1','HP-inquiry-plan']:
 INTERPRETATIONS[rid,'SID17-01']=('activity_context','질문·자료·분석·설계 결정과 시제품/지식의 두 산출을 계획에서 구별한다.','ILDF의4단계를 고정 시간표·수학적 선수 사슬로 바꾸지 않고 문서/게시를 학습 성과로 세지 않는다.')
for rid in ['SEC_12수과03-01_C04','HP-inquiry-execution']:
 INTERPRETATIONS[rid,'SID17-03']=('activity_context','실제 대상자의 관점과 후속 자료에 따라 초기 가정·지원·실행 계획을 수정한다.','한 발언·합성 프로필·가상 인물을 대표 표본이나 추가 실제 참여자로 세지 않는다.')
for rid in ['SEC_12수과03-03_C04','REV-12수과03-04-1','HP-inquiry-reflection']:
 INTERPRETATIONS[rid,'SID17-04']=('inference_limit','보고/성찰에서 실제 소규모 탐색·계획된 현장 시험·잠재 이용·채택·학습 성과를 나누고 조건을 밝힌다.','별도5쌍/8쌍·계획50쌍 초과·잠재 채택100명 초과를 합산하거나 국내 실제 검증/성과로 바꾸지 않는다.')
for rid in ['SEC_12수과02-01_C04','REV-12수과02-01-1']:
 INTERPRETATIONS[rid,'SID17-05']=('inference_limit','출판사 서지·읽은 본문/판면·인용 원연구/원자료의 대조 범위를 구별하고 불일치와 후속 확인을 남긴다.','DBRC쪽수는5–8이며21–24쪽Bannan논문과 구별한다. 서지 확인을 원논문 독해로 세거나 없는표를 채우지 않는다.')

def main():
 registry=load_registry();known={c['id'] for c in registry['claims']};newids={c['id'] for c in CLAIMS}
 if newids<=known:
  assert registry['sources'][SOURCE]['snapshot_file']==NOTES;build_report();return
 assert not newids&known
 s=registry['sources'][SOURCE];assert (s['snapshot_file'],s['snapshot_sha256'],s['bibliography_snapshot'])==(PRIOR,PRIOR_SHA,PRIOR_BIB)
 assert sha(ROOT/PRIOR)==PRIOR_SHA and sha(CACHE/'slo-design-part-a-2013.pdf')==SHA
 acq=load(CACHE/'acquisition.json');assert acq['reading_completed'] and acq['images_viewed'] and acq['read_text_pages']==NEW_TEXT and acq['viewed_image_pages']==NEW_VISUAL
 old_source=copy.deepcopy(s);old_notes=load(ROOT/PRIOR);old_claims=[copy.deepcopy(c) for c in registry['claims'] if c['source_id']==SOURCE]
 assert len(old_claims)==28 and len(s['observations'])==42
 assert not set(NEW_TEXT)&set(old_notes['selected_text_pages']) and not set(NEW_VISUAL)&set(old_notes['visual_pdf_pages'])
 assert not {o['id'] for o in OBSERVATIONS}&{o['id'] for src in registry['sources'].values() for o in src.get('observations',[])}
 relations=load(ROOT/'data/revised_relations.json')['relations'];pairs={(x['id'],c['id']) for x in relations for c in CLAIMS if all(x[k].startswith('standard:') for k in ['from','to']) and {x[k][9:] for k in ['from','to']}<=set(c['standard_codes'])}
 assert pairs==INTERPRETATIONS.keys() and len(pairs)==10
 reviewed=load(ROOT/FILE);old_rows=[copy.deepcopy(x) for x in reviewed['records'] if x['claim_id'] in {c['id'] for c in old_claims}];assert len(old_rows)==35
 bibliography=load(ROOT/'data/sources.json');entry=next(x for x in bibliography if x['id']==SOURCE);old_entry=copy.deepcopy(entry);entry.update(title=TITLE,review_scope=SCOPE,does_not_establish=LIMITS,next_review=LIMITS)
 notes=copy.deepcopy(old_notes)
 notes.update(date=DATE,read_scope=SCOPE,selected_text_pages=sorted(old_notes['selected_text_pages']+NEW_TEXT),visual_pdf_pages=sorted(old_notes['visual_pdf_pages']+NEW_VISUAL),rendered_page_sha256={**old_notes['rendered_page_sha256'],**{str(p):sha(CACHE/f'rendered/slo-design-part-a-2013-{p}.png') for p in NEW_VISUAL}},previous_review=old_source,previous_bibliography=old_entry,previous_claims=old_claims,previous_observations=copy.deepcopy(s['observations']),previous_relation_records=old_rows,previous_notes_file=PRIOR,previous_notes_sha256=PRIOR_SHA,reading_log=old_notes['reading_log']+['2026-11-17:4장 전체의 새 본문/참고문헌18쪽·판면20쪽을 실제 읽었다.115사진·134머리말/쪽번호 전용 쪽은 추출문 독해로 세지 않는다. 그림1/2와 실제/계획/잠재 이용 수치·서지 불일치를 구별했다.'])
 notes['integrative_design_followup']=dict(new_text_pages=NEW_TEXT,new_visual_pages=NEW_VISUAL,cumulative_text_pages=106,cumulative_visual_pages=113,chapter4_all_pdf_pages=NEW_VISUAL,chapter4_complete=True,prior_complete_chapters=[2,3,6],all_part_a_read=False,part_b_read=False,cited_originals_read=False,original_article_metadata_only=True,earlier_2009_chapter_read=False,lao_system_executed=False,raw_data_reanalyzed=False,local_student_validation=False,actual_implementation_verified=False)
 notes['publisher_metadata_checks']=[dict(url='https://journals.sagepub.com/doi/abs/10.3102/0013189X032001021',title='The Role of Design in Research: The Integrative Learning Design Framework',author='Brenda Bannan-Ritland',year=2003,volume=32,issue=1,pages='21–24',doi='10.3102/0013189X032001021',scope='publisher metadata only; original full text not read',checked_date=DATE),dict(url='https://journals.sagepub.com/doi/abs/10.3102/0013189X032001005',title='Design-Based Research: An Emerging Paradigm for Educational Inquiry',author='The Design-Based Research Collective',year=2003,volume=32,issue=1,pages='5–8',doi='10.3102/0013189X032001005',scope='publisher metadata only; original full text not read',checked_date=DATE)]
 notes['source_corrections']=old_notes['source_corrections']+[
  dict(location='PDF115/134',issue='115사진·134머리말/쪽번호 전용 쪽은 본문 추출문 읽기에 합산하지 않는다.'),
  dict(location='PDF126–128',issue='실행한별도5쌍/8쌍·예정50쌍초과·추적100명초과잠재채택자를 구별한다. 중복/단위/실행상태가달라 합산학생표본·인과효과·채택률로 바꾸지 않는다.'),
  dict(location='PDF129–130 and complete chapter pages115–134',issue='본문은Table1을 호출하지만 실제 장의 판면에는Figure1/2만 확인했고 대응Table1을 찾지 못했다. 원표·정오표 미확인이며 결과를 복원하지 않는다. PDF130은 여러 단/그림의 배치로 추출문 순서가 달라 실제 판면 순서로 대조했다.'),
  dict(location='PDF132 bibliography',issue='DBRC2003의21–24쪽은 출판사 서지의5–8쪽과 다르다.21–24쪽Bannan-Ritland2003과 구별한다. 출판사2편의서지만확인했으며 원논문독해·출판사정오표확보로 세지 않는다.'),
  dict(location='PDF116/129/131 and PDF126/133',issue='ILDF/IDLF표기·Jeffs2000호출과서지대응·다른본문호출/참고목록의차이를 보존한다.1990Dick/Carey참고문헌을2014같은7판본문확보로 세지 않는다. 형성평가의한계에대한Bannan의관점과6장의평가틀을 위치별로구별한다.')]
 write(ROOT/NOTES,notes)
 s.update(date=DATE,snapshot_file=NOTES,snapshot_sha256=sha(ROOT/NOTES),snapshot_history=s.get('snapshot_history',[])+[dict(snapshot_file=PRIOR,snapshot_sha256=PRIOR_SHA,date=old_source['date'],read_scope=old_source['read_scope'])],bibliography_snapshot=digest(entry),read_scope=SCOPE,limits=LIMITS,method_note='4장전체와기존2/3/6장·선정도입을대조했다. ILDF단계·두산출·추측/목표/평가·프로필·실제/계획/잠재이용·서지범위를구별했다. 원연구/국내학생효과의검증이아니다.',editorial_action='새주장6건·자체과제8개를더하고기존28주장·42과제와35관계해석의이전원장을보존했다.',observations=s['observations']+copy.deepcopy(OBSERVATIONS),display={**s['display'],'title':TITLE})
 for claim in copy.deepcopy(CLAIMS):
  claim.update(empirical_scope=copy.deepcopy(s['empirical_scope']),target_snapshots={f'revision:{code}':digest(target_value(f'revision:{code}')) for code in claim['standard_codes']});registry['claims'].append(claim)
 by_claim={c['id']:c for c in registry['claims']};by_relation={x['id']:x for x in relations}
 for row in reviewed['records']:
  if row['claim_id'] in {c['id'] for c in old_claims}:row['claim_snapshot']=claim_snapshot(by_claim[row['claim_id']],s)
 for (rid,cid),(role,finding,limit) in INTERPRETATIONS.items():reviewed['records'].append(dict(relation_id=rid,claim_id=cid,role=role,finding=finding,limit=limit,relation_snapshot=relation_snapshot(by_relation[rid]),claim_snapshot=claim_snapshot(by_claim[cid],s)))
 apply_literature_context(relations,registry,registry=reviewed)
 queue=load(ROOT/'data/content_review_queue.json');row=next(x for x in queue['literature_review'] if x['source']['id']==SOURCE);row.update(source=entry,claim_ids=[c['id'] for c in registry['claims'] if c['source_id']==SOURCE])
 write(ROOT/'data/sources.json',bibliography);write(ROOT/'data/literature_claim_reviews.json',registry);write(ROOT/'data/content_review_queue.json',queue);write(ROOT/FILE,reviewed);build_report()
 print('Extended same SLO source:6 claims,8 own tasks,10 relation entries;all prior claims/tasks preserved')
if __name__=='__main__':main()
