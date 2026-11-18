"""Extend the same image-only course scan; preserve the initial 30-spread review."""
import copy
from literature_review import ROOT,load_registry,build_report,digest,target_value
from extend_lt2_length_assets_review import load,sha,write
from relation_literature_review import FILE,claim_snapshot,relation_snapshot,apply_literature_context
from record_polya_classroom_method_review import SOURCE,CACHE,SHA,URL,NI,LI,PL,RU,OU,RE
from check_polya_auxiliary_models import check
DATE='2026-11-18'
PRIOR='data/literature_evidence/POLYA_SECOND_EDITION_COURSE_SCAN_review_notes.json'
PRIOR_SHA='1e7fa19598749b8c74468af04c0ae62d0ace77fa6e4fb0a7785c07d3078ae729'
PRIOR_BIB='f1973ac97307c6a1ec0825b471cf9c94e558e46c47b4490caccc5cc38fb85ca8'
NOTES='data/literature_evidence/POLYA_SECOND_EDITION_heuristic_followup_review_notes.json'
TITLE='How to Solve It, second-edition course scan — complete Parts I–II and selected dictionary pp37–85; 54 PDF spreads, actual printing unverified'
SCOPE='이전 첫30PDF판면의 서지·질문 목록·Part I1–32/20절·Part II33–36 읽기 이력을 보존하고 PDF31–54(인쇄38–85)24판면을 추가로 직접 읽었다. 누적54판면이며 대부분 책 두 면의 스캔이다. Part III의Analogy부터Decomposing and Recombining까지(37–85상단)와Definition85첫 면을 확인했다. 추출문/OCR은0쪽이다. 사전 나머지·Part IV·138판면 전권·인용 원연구의 완료는 아니다. Princeton 공식 발췌 XXV–XXVII는 별도 출처로 유지한다.'
LIMITS='교수 조언·수학 예제·이상화 대화의 방법론적 서술이며 새 실증 표본이나 국내 학생 효과가 아니다. 2판 저작권1957·표시 인쇄1971/1973·서문1944/1954/1956·스캔2006과 미확정 실제 인쇄연도를 구별한다. 출판사 직접 파일/동일성·다른 판본·PDF55–138·인용 원연구/정오표·실제 독립/학생 검증은 미확인이다. 인쇄72쪽의 방정식 수 조언은 임의의 실수 비선형 방정식의 존재·유일성 정리로 적용하지 않는다. 유추·몇 가지 검산·역사적 용어를 각각 증명·현재의 형식 정의로 바꾸지 않는다.'

def c(n,codes,pages,support,limit):
 return dict(id=f'POLYH18-{n:02d}',source_id=SOURCE,role='mathematical_explanation',standard_codes=codes,locations=[f'{URL}#page={p}' for p in pages],support=support,does_not_establish=limit,independent_review=False,student_validated=False)
CLAIMS=[
 c(1,[LI,RU,OU,RE],[38,39,40,45,53,54],'보조 문제와 원래 문제의 연결 방향을 밝힌다. y=x²로 바꾼 사차방정식에서는 y의 해에서 원래 x의 모든 부호 가지를 회복하고, 제곱처럼 한 방향으로만 따라가는 변형 뒤에는 원래 식·정의역·조건을 다시 확인한다.','서로 풀 수 있는 두 문제가 같은 미지수나 일대일 대응을 가져야 하는 것은 아니다. 원문 x⁴−13x²+36=0은 y=4,9에서 x=±2,±3을 회복한다. 자체 근호 반례와 직육면체 역문제는 원문 그대로의 문항·실제 학생 오답이 아니며 보조 문제의 답을 검토 없이 원래 답으로 옮기지 않는다.'),
 c(2,[LI,PL,RU],[48,53],'조건의 충분성·모순·중복을 미지수의 범위와 식의 구조에 맞게 따진다. 실수 범위에서 방정식 개수와 미지수 개수만으로 해의 존재·유일성이나 조건의 중복을 판정하지 않는다.','인쇄72쪽의 개수 조언을 임의의 비선형 방정식에 일반화하지 않는다. x²+y²=0은 실수에서 유일한(0,0)을 정하며, x(x−1)=0과 x(x−2)=0은 한 미지수의 두 식이 모두 필요하면서 공통해0을 갖는다. 선형계에서도 개수 외에 일관성·독립성 등이 필요하며 복소수 등 다른 범위에 같은 반례의 결론을 옮기지 않는다.')]

def p(n,codes,q,e,i):return dict(id=f'POLYH18-P{n:02d}',standard_codes=codes,question=q,expected=e,interpretation=i,student_validated=False)
OBSERVATIONS=[
 p(1,[LI,RU],'실수 방정식 x⁴−13x²+36=0에서 y=x²로 바꾸어 y=4,9를 얻었다. 이것이 원래 미지수의 답인가?','(y−4)(y−9)=0에서 얻은 값은 y의 해다. y≥0을 확인하고 x²=4 또는9에서 x=−3,−2,2,3을 모두 회복한다. x→y는 일대일이 아니지만 각 y해에서 원래 해를 모두 되찾을 수 있다.','원문 인쇄51–55쪽과 대조한 자체 과제다. 변수를 바꾼 문제의 해 개수·부호를 원래 문제와 혼합하지 않고 정의역과 복원 규칙을 남긴다.'),
 p(2,[RU,OU,RE],'실수 방정식 √(x+2)=x를 제곱해 x=−1,2를 얻었다. 둘 다 답인가?','아니다. 제곱식 x²−x−2=(x−2)(x+1)=0의 후보를 원래 식에 대입한다. 원래 오른쪽은 음이 아니어야 하므로 x≥0이며,−1에서는√1=1≠−1이다.2만 원래 해다. x+2≥0만 확인해서는−1을 걸러내지 못한다.','제곱은 원래 식에서 제곱식으로의 함의이며 추가 조건 없이 역방향이 보장되지 않는다. 이 근호 문항은 작성자의 예이며 원문의 문항·실제 학생 오류가 아니다.'),
 p(3,[LI,PL,RU],'실수 범위에서 식이 미지수보다 적으면 해가 하나일 수 없고, 많으면 반드시 모순 또는 중복인가?','아니다. x²+y²=0은 각 제곱이0이상이라 x=y=0만 가능하다. x(x−1)=0과 x(x−2)=0의 해집합은{0,1}과{0,2}로 공통해는0이며 어느 식을 빼도 해가 늘어난다. 식 하나·미지수 하나인 x²+1=0,x=0,x²=1,0x=0은 각각 해가0,1,2,무한 개다.','실수와 비선형 식이라는 범위를 명시한 반례다. 유한 수 대입으로 유일성을 증명하지 않으며 이 반례를 선형대수의 조건 검토가 무용하다는 뜻으로 바꾸지 않는다. 원문72쪽의 조언에 적용 범위를 보완한다.'),
 p(4,[RU,OU,RE],'직육면체의 두 모서리가3,4이고 공간 대각선d가13,5,4일 때 나머지 모서리c는 각각 가능한가?','서로 수직인 양의 길이에서 c²=d²−25다. d=13이면c=12이고 음의−12는 길이가 아니다. d=5이면c=0인 평면 경계로 양의 높이 직육면체는 아니다. d=4이면c²=−9이므로 실수 길이가 없다.','인쇄66쪽의 역문제를 바탕으로 만든 수치 예다. 원래 양의 길이 조건·경계 확장·실수 해 부재를 구별하며 실제 도형 측정·학생 수행 검증은 아니다.')]
UPDATED_OBSERVATIONS={
 'POLY18-P04':dict(expected='아니다. 이 식은 순열 대칭,길이12배시제곱144배,c=0에서a²+b²를 만족하지만3,4,12에서는3355/19로올바른169와다르다. 검사는 필요 조건 점검이며 유도·증명을 대신하지 않는다. 같은 순서의 재계산은 같은 실수를 반복할 수 있으므로 약한 추론 단계를 찾고 다른 유도·검사 순서로 대조한다.'),
 'POLY18-P08':dict(expected='아니다. 최초30판면의 서지/질문 목록·Part I1–32·Part II33–36·사전37첫면 읽기는 이전 기록으로 보존한다. 이후PDF31–54의24판면을 읽어 현재 누적54판면이며 사전37–85의 선정 항목과Definition첫 면까지다.2판저작권1957·표시인쇄1971/1973·스캔2006과 미확정 실제 인쇄연도를 구별하고 공식발췌XXV–XXVII와 동일 판본으로 단정하지 않는다.',interpretation='추출문/OCR은 여전히0쪽이다. 누적54판면은 전권138판면·전체사전/Part IV·인용 원연구·출판사 직접 파일 동일성을 확인한 뜻이 아니다. 최초30판면 기록을 나중54판면을 읽은 기록으로 덮어쓰지 않는다.')}
INTERPRETATIONS={}
for rid in ['SEC_12수과02-01_C04','REV-12수과02-01-1','SEC_12수과03-02_C04','HP-inquiry-presentation','SEC_12수과03-03_C04','REV-12수과03-04-1','HP-inquiry-reflection']:
 INTERPRETATIONS[rid,'POLYH18-01']=('inference_limit','치환·제곱·역문제에서 원래 미지수·해의 복원·정의역·양의 길이 조건을 계산과 논증에 명시한다.','보조 문제의 해를 검토 없이 원래 답으로 옮기거나 양의 부호만 취해 해를 빠뜨리지 않는다. 자체 반례는 실제 학생 오답·검증된 효과가 아니다.')
for rid in ['SEC_12수과02-01_C04','REV-12수과02-01-1','SEC_12수과03-01_C04','HP-inquiry-execution']:
 INTERPRETATIONS[rid,'POLYH18-02']=('inference_limit','조건을 세는 일과 해의 존재·유일성·조건의 독립성을 증명하는 일을 구별하고 실수 비선형 반례로 적용 범위를 점검한다.','식과 미지수의 개수만으로 모순·중복·불충분을 단정하지 않는다. 실수 범위·식의 구조를 명시하며 이론적 반례를 학생 자료로 바꾸지 않는다.')

def main():
 registry=load_registry();newids={x['id'] for x in CLAIMS};known={x['id'] for x in registry['claims']}
 if newids<=known:
  assert registry['sources'][SOURCE]['snapshot_file']==NOTES;build_report();return
 assert not newids&known and check()['status']=='pass'
 s=registry['sources'][SOURCE];assert s['snapshot_file']==PRIOR and s['snapshot_sha256']==PRIOR_SHA and s['bibliography_snapshot']==PRIOR_BIB and sha(ROOT/PRIOR)==PRIOR_SHA
 a=load(CACHE/'dictionary-followup-acquisition-20261118.json');assert a['source_pdf_sha256']==SHA and a['reading_completed'] and a['images_viewed'] and a['new_visual_pages']==list(range(31,55)) and a['new_text_pages']==[] and not a['ocr_used']
 assert sha(CACHE/'polya-second-edition-university-course-copy.pdf')==SHA
 old_notes=load(ROOT/PRIOR);images={str(n):sha(CACHE/f'rendered/polya-{n}.png') for n in range(1,55)};assert {k:images[k] for k in old_notes['rendered_page_sha256']}==old_notes['rendered_page_sha256']
 old_source=copy.deepcopy(s);old_claims=[copy.deepcopy(x) for x in registry['claims'] if x['source_id']==SOURCE];old_obs=copy.deepcopy(s['observations']);assert len(old_claims)==4 and len(old_obs)==8
 assert not {x['id'] for x in OBSERVATIONS}&{x['id'] for v in registry['sources'].values() for x in v.get('observations',[])}
 relations=load(ROOT/'data/revised_relations.json')['relations'];pairs={(r['id'],c['id']) for r in relations for c in CLAIMS if all(r[k].startswith('standard:') for k in ['from','to']) and {r[k][9:] for k in ['from','to']}<=set(c['standard_codes'])};assert pairs==INTERPRETATIONS.keys() and len(pairs)==11
 reviewed=load(ROOT/FILE);old_ids={c['id'] for c in old_claims};old_rows=[copy.deepcopy(x) for x in reviewed['records'] if x['claim_id'] in old_ids];assert len(old_rows)==17
 bibliography=load(ROOT/'data/sources.json');entry=next(x for x in bibliography if x['id']==SOURCE);old_entry=copy.deepcopy(entry);entry.update(title=TITLE,review_scope=SCOPE,does_not_establish=LIMITS,next_review=LIMITS)
 empirical=copy.deepcopy(s['empirical_scope']);empirical['inference_limit']=LIMITS
 detail=copy.deepcopy(old_notes['classroom_method_scan_review']);detail.update(selected_pdf_pages=list(range(1,55)),part_iii_boundary_page_only=None,part_iii_selected_printed_pages='37–85',definition_first_page_only=85,remaining_pdf_pages_without_visual_review=list(range(55,139)),source_figures_viewed=list(range(1,17)))
 notes=copy.deepcopy(old_notes);notes.update(date=DATE,read_scope=SCOPE,visual_pdf_pages=list(range(1,55)),rendered_page_sha256=images,empirical_scope=empirical,previous_review=old_source,previous_bibliography=old_entry,previous_claims=old_claims,previous_observations=old_obs,previous_relation_records=old_rows,previous_notes_file=PRIOR,previous_notes_sha256=PRIOR_SHA,classroom_method_scan_review=detail,
  reading_log=old_notes['reading_log']+['2026-11-18:PDF31–54의24판면을 직접 읽었다. 인쇄38–85이며 누적54PDF판면, 추출문/OCR0쪽이다.'],
  heuristic_dictionary_followup=dict(new_visual_pages=list(range(31,55)),new_text_pages=[],ocr_used=False,cumulative_visual_pages=54,printed_pages='38–85',complete_dictionary_entries=['Analogy','Auxiliary Elements','Auxiliary Problem','Bolzano','Bright Idea','Can You Check the Result?','Can You Derive the Result Differently?','Can You Use the Result?','Carrying Out','Condition','Corollary','Could You Derive Something Useful from the Data?','Decomposing and Recombining'],cross_reference_entries=['Condition,Contradictory','Could You Restate the Problem?'],definition_first_page_only=85,whole_book_read=False,part_iii_complete=False,part_iv_read=False,rereviewed_prior_claims=4,rereviewed_prior_tasks=2,rereviewed_prior_relation_snapshots=17,actual_independent_review=0,actual_student_validation=0))
 notes['source_corrections'] += [dict(location='printed51–56, auxiliary problem',issue='Recover all original roots after y=x²; distinguish equivalence of solvable problems from bijection of individual solution sets. Squaring can enlarge the candidate set; verify the original conditions.'),dict(location='printed72, Condition',issue='Equation/unknown counts do not establish the general nonlinear real claims. Own counterexamples x²+y²=0 and x(x−1)=x(x−2)=0 bound the advice; not an official erratum or claim about every edition.'),dict(location='printed43 and59–61',issue='Analogy supplies plausible ideas rather than proof. Repeating identical checks can repeat the same error; use another derivation/order and inspect weak steps.'),dict(location='printed46, historical terminology',issue='Historical analogy/isomorphism terminology is not adopted as a current formal algebra definition; no modern-definition fidelity review claimed.')]
 write(ROOT/NOTES,notes)
 s.update(date=DATE,snapshot_file=NOTES,snapshot_sha256=sha(ROOT/NOTES),snapshot_history=s.get('snapshot_history',[])+[dict(snapshot_file=PRIOR,snapshot_sha256=PRIOR_SHA,date=old_source['date'],read_scope=old_source['read_scope'])],bibliography_snapshot=digest(entry),read_scope=SCOPE,limits=LIMITS,empirical_scope=empirical,method_note='동일 PDF의 추가24판면을 직접 읽었다. 누적54판면·추출문/OCR0쪽이며 전권/사전 전체 완료가 아니다.',editorial_action='기존4주장의 범위·2과제 설명·17관계 근거 스냅샷을 다시 대조하고 원기록을 보존했다. 새 근거2건·자체 과제4개·관계 한계11건을 추가했다.',display={**s['display'],'title':TITLE})
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
 print('Same Polya scan extended:24new visual spreads,54cumulative;2claims/4tasks/11limits;4claim scopes,2task explanations and17snapshots rereviewed')

if __name__=='__main__':main()
