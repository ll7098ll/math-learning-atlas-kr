"""Bind twenty self-derivations to the already-read copy, preserving history."""
import copy
from literature_review import ROOT,load_registry,build_report,digest
from extend_lt2_length_assets_review import load,sha,write
from relation_literature_review import FILE,claim_snapshot,apply_literature_context
from record_polya_classroom_method_review import SOURCE,CACHE,SHA,URL,NI,LI,PL,RU,OU,RE
from check_polya_part_iv_derivations import check
from polya_part_iv_derivation_notes import RECORDS

DATE='2026-11-18'
PRIOR='data/literature_evidence/POLYA_SECOND_EDITION_complete_copy_review_notes.json'
PRIOR_SHA='c464cbd897224755fccd14b95dda6a8bf5582fdef066920472c37ec48e76c4aa'
PRIOR_BIB='be4c7fe5222b314dfce0e44ec31900e20266876e962c0d2ec32ec47153f5f26a'
NOTES='data/literature_evidence/POLYA_SECOND_EDITION_part_iv_derivations_review_notes.json'
PROOFS='data/literature_evidence/POLYA_SECOND_EDITION_part_iv_self_derivations.json'
ADDITION='Part IV의 20문제에 대해 조건·자체 유도·결론·한계를 각각 기록했다. PDF129–138의 문제·힌트·해설10판면을 다시 대조했으며 새 미독 페이지나 추출문을 추가한 것은 아니다. 네 반원호/여덟 1/4원호,정육면체의13축/23회전,시선각의실현조건,수열의두해,합의일반유도,평면격자/동전의완전분류를검산했다. 수치검사의유한사례와일반논증을구별한다.'
LIMIT_ADDITION='20문제의 자체 재유도는 외부 독립 검토가 아니다. 구면 이동만으로 털 색을 정하지 않고, 피라미드10(b)의 지지직선 해석에는 볼록 밑면/내부 높이발 조건이 필요하다. 산 높이16의 양의 분모만으로 각 배치가 실현되는 것은 아니다. 따라서 원문의 모든 무조건적 결론·출판사 원판/정오표·원자료·실제 독립/학생·시각 검증 완료로 승격하지 않는다.'
CLAIM_ADDITIONS={
 'POLY18-01':'Part IV의 자체 유도20건은 구면/평면·정수/연속·순서/구성 등 모형의 범위를 명시한다. 순수 기하학으로 실제 생물의 색이나 현재 국경을 확정하지 않는다.',
 'POLY18-02':'20건의 자체 재유도와 계산 검사를 외부 독립 검토나 학생 수행·지원 효과로 세지 않는다.',
 'POLY18-03':'산의 높이16은 경사각·시선각이 같은 수평면 위 두 지점을 실현하는지도 확인한다. α=β=60°,γ=120°는 공식의 분모가 양수여도 방위각 차의 코사인이−5라 불가능하다.',
 'POLY18-04':'20문제의 조건별 유도와 반례를 기록했지만 모든 원해답의 무조건적 타당성·외부 검토를 증명한 것은 아니다. 유한 검사와 일반 논증을 구별한다.',
 'POLYH18-01':'정사각형 시각의 원 방정식은 극단 시선이 되는 영역과 정사각형 외부 조건을 함께 적용한다. 지지 원 전체가 궤적은 아니며90°의 꼭짓점 끝은 제외한다.',
 'POLYH18-02':'정육면체의 비항등회전23개와 부호를 구별하지 않는 축13개를 나누고 평균의 가중을 명시한다. 동전292구성의 순서 비구별과 격자의 공유 변·외부 면 규칙을 유지한다.'}

def p(n,codes,q,e,i):return dict(id=f'POLYD18-P{n:02d}',standard_codes=codes,question=q,expected=e,interpretation=i,student_validated=False)
OBSERVATIONS=[
 p(1,[NI,LI,RU],'단위 정육면체에서 비항등 회전이 23개이고 축이 13개라면, 회전마다 축 길이를 적어 평균내도 원문의 축 길이 평균과 같은가?',
   '꼭짓점 축 4개는 각 2회전, 모서리 축 6개는 각 1회전, 면 축 3개는 각 3회전에 대응한다. 축별 평균은 (4√3+6√2+3)/13, 회전별로 중복 가중하면 (8√3+6√2+9)/23이다. 어떤 대상을 한 번씩 센 평균인지 먼저 정한다.',
   '원문의 분류를 평균의 표집 단위와 연결한 자체 과제다. 실제 회전 실험·무작위 방향의 평균 너비·학생 효과를 검증한 자료가 아니다.'),
 p(2,[PL,RU,OU,RE],'산의 높이 공식에서 두 하향 경사각을 각각60°, 시선 사이 각을120°로 넣으면 분모는 양수이다. 이것만으로 실제 같은 높이 평면의 두 지점이 존재하는가?',
   '수평 방위각 차 δ는 cosγ=sinα sinβ+cosα cosβ cosδ를 만족해야 한다. 주어진 각에서는 cosδ=(−1/2−3/4)/(1/4)=−5이므로 배치가 불가능하다. 공식의 양의 값과 실제 기하 조건의 충족을 나누어 확인한다.',
   '계산식의 정의역과 모형의 실현 가능성을 구별하는 자체 반례다. 실제 산·관측값이나 원문의 틀린 수치 예가 아니다.'),
 p(3,[LI,PL,RU,OU],'정사각형 [−1,1]²를 보는45° 궤적의 위쪽 부분에서 x²+(y−2)²=2를 얻었다. 이 원 전체를 해로 보고해도 되는가?',
   '위쪽 띠 |x|≤1,y>1에서 극단 시선이 윗변 양 끝으로 향한다는 조건이 필요하다. 위쪽 원호 y=2+√(2−x²)만 남고, 같은 원 위 (0,2−√2)는 정사각형 안이라 제외한다. 모서리 영역에서는 다른 꼭짓점 쌍과 다른 원호를 확인한다.',
   '원 방정식의 해와 원래 시각 문제의 해를 대조하는 자체 과제다. 한 원을 그린 사실이나 유한 표본만으로 모든 관찰점의 분류를 증명하지 않는다.'),
 p(4,[RU,OU,RE],'한 변을 단위 길이 두 개로 나눈 정육각형의 삼각 격자에서 단위 삼각형24개를 셌다. 단위 변은72개인가? 외부 면도 삼각형에 넣어야 하는가?',
   '삼각형 변의 발생 수72는 공유 변을 두 번 센다. 둘레의 단위 변12개는 한 번만 세므로 2L=72+12, L=42이다. 꼭짓점은19개여서19−42+24=1이다. 외부 면을 포함한 오일러의 전체 면 수는25이지만 단위 삼각형 수 T는24이다.',
   '공유 요소와 집계 단위를 비교하는 자체 격자 과제다. 오일러 수치 관계만으로 임의의 자료가 정육각형 격자를 이룬다고 보장하지 않는다.')]

def main():
 registry=load_registry();s=registry['sources'][SOURCE]
 if s['snapshot_file']==NOTES:build_report();return
 assert s['snapshot_file']==PRIOR and s['snapshot_sha256']==PRIOR_SHA and s['bibliography_snapshot']==PRIOR_BIB
 assert sha(ROOT/PRIOR)==PRIOR_SHA and sha(CACHE/'polya-second-edition-university-course-copy.pdf')==SHA
 assert [x['problem'] for x in RECORDS]==list(range(1,21)) and check()['status']=='pass'
 old_notes=load(ROOT/PRIOR);assert old_notes['classroom_method_scan_review']['whole_available_copy_read']
 assert old_notes['visual_pdf_pages']==list(range(1,139))
 for n in range(129,139):assert sha(CACHE/f'rendered/polya-{n}.png')==old_notes['rendered_page_sha256'][str(n)]
 old_source=copy.deepcopy(s);old_claims=[copy.deepcopy(x) for x in registry['claims'] if x['source_id']==SOURCE];old_obs=copy.deepcopy(s['observations'])
 assert len(old_claims)==6 and len(old_obs)==25
 assert not {x['id'] for x in OBSERVATIONS}&{x['id'] for z in registry['sources'].values() for x in z.get('observations',[])}
 reviewed=load(ROOT/FILE);ids={x['id'] for x in old_claims};old_rows=[copy.deepcopy(x) for x in reviewed['records'] if x['claim_id'] in ids];assert len(old_rows)==28
 proof=dict(source_id=SOURCE,source_pdf_sha256=SHA,date=DATE,reviewer='Codex',kind='workspace_self_derivations_not_external_review',records=RECORDS,
   source_problem_pdf_pages=[129,130,131],source_hints_and_solutions_pdf_pages=list(range(131,139)),reread_visual_pdf_pages=list(range(129,139)),new_text_pages=0,new_unread_pages=0,
   exact_checks=check(),all_twenty_problem_self_derivations_written=True,all_source_solutions_independently_reproved=False,
   source_solution_unconditional_validity_proved=False,publisher_binary_fidelity_verified=False,actual_independent_review=0,actual_student_validation=0,
   limit=LIMIT_ADDITION,contains_source_full_text=False,source_pdf_redistributed=False)
 write(ROOT/PROOFS,proof)
 bibliography=load(ROOT/'data/sources.json');entry=next(x for x in bibliography if x['id']==SOURCE);old_entry=copy.deepcopy(entry)
 entry.update(review_scope=s['read_scope']+' '+ADDITION,does_not_establish=s['limits']+' '+LIMIT_ADDITION,next_review='정식 출판사 판면/정오표·인용 원전과 실제 외부 검토·학생 반응을 후속 대조한다. 자체 20문제 재유도는 외부 검증이 아니다.')
 empirical=copy.deepcopy(s['empirical_scope']);empirical['inference_limit']=entry['does_not_establish']
 notes=copy.deepcopy(old_notes)
 notes.update(date=DATE,read_scope=entry['review_scope'],empirical_scope=empirical,previous_review=old_source,previous_bibliography=old_entry,previous_claims=old_claims,previous_observations=old_obs,previous_relation_records=old_rows,previous_notes_file=PRIOR,previous_notes_sha256=PRIOR_SHA,
   part_iv_derivation_followup=dict(self_derivations_file=PROOFS,self_derivations_sha256=sha(ROOT/PROOFS),problem_numbers=list(range(1,21)),reread_visual_pdf_pages=list(range(129,139)),new_unread_visual_pages=[],new_text_pages=[],new_claims=0,new_tasks=4,new_relation_entries=0,rereviewed_prior_claims=6,rereviewed_prior_relation_snapshots=28,source_solution_unconditional_validity_proved=False,all_source_solutions_independently_reproved=False,external_review_count=0,student_validation_count=0,exact_check=check()))
 notes['reading_log']=old_notes['reading_log']+['2026-11-18:이미 읽은 PDF129–138을 다시 대조하고 20문제의 조건별 자체 유도·전수 분류·예외를 기록했다. 새 미독/추출문 페이지는 0이다.']
 notes['source_corrections']=old_notes['source_corrections']+[dict(location='PartIV7/8/10/16/19/20',issue='Conditional self-derivations:select valid locus arcs;distinguish13axes from23rotations;keep interior condition for incircle;require realizable sight angles beyond positive height formula;count shared edges/outer face and unordered coin compositions. All20records include assumptions/general arguments and finite checks;not independent external review.')]
 write(ROOT/NOTES,notes)
 s.update(date=DATE,snapshot_file=NOTES,snapshot_sha256=sha(ROOT/NOTES),snapshot_history=s.get('snapshot_history',[])+[dict(snapshot_file=PRIOR,snapshot_sha256=PRIOR_SHA,date=old_source['date'],read_scope=old_source['read_scope'])],bibliography_snapshot=digest(entry),read_scope=entry['review_scope'],limits=entry['does_not_establish'],empirical_scope=empirical,
   method_note=s['method_note']+' '+ADDITION,editorial_action='20문제의 자체 재유도 원장을 추가하고 기존6주장·28관계스냅샷을조건과대조했다. 기존25과제는보존하고4자체과제를추가했다. 새출처·새주장·새관계해석은0건이다.')
 s['observations']+=copy.deepcopy(OBSERVATIONS)
 for claim in registry['claims']:
  if claim['id'] in ids:
   claim['empirical_scope']=copy.deepcopy(empirical);claim['does_not_establish']+=' '+CLAIM_ADDITIONS[claim['id']]
   claim['locations']=list(dict.fromkeys(claim['locations']+[f'{URL}#page={n}' for n in range(129,139)]))
 by_claim={x['id']:x for x in registry['claims']}
 for row in reviewed['records']:
  if row['claim_id'] in ids:row['claim_snapshot']=claim_snapshot(by_claim[row['claim_id']],s)
 relations=load(ROOT/'data/revised_relations.json')['relations'];apply_literature_context(relations,registry,registry=reviewed)
 queue=load(ROOT/'data/content_review_queue.json');row=next(x for x in queue['literature_review'] if x['source']['id']==SOURCE);row.update(source=entry,claim_ids=[x['id'] for x in old_claims])
 for name,value in [('data/sources.json',bibliography),('data/literature_claim_reviews.json',registry),('data/content_review_queue.json',queue),(FILE,reviewed)]:write(ROOT/name,value)
 build_report();print('Twenty conditional self-derivations;four tasks;6claims/28snapshots rechecked;0new sources/claims/relations.')

if __name__=='__main__':main()
