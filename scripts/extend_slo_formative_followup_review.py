"""Complete the selected formative-evaluation chapter, preserving prior source history."""
import copy,json
from pathlib import Path
from pypdf import PdfReader
from literature_review import ROOT,load_registry,build_report,digest,target_value
from extend_lt2_length_assets_review import load,sha,write
from relation_literature_review import FILE,claim_snapshot,relation_snapshot,apply_literature_context
SOURCE='SLO_EDR_2013_INQUIRY_SELECTED';DATE='2026-11-17'
CACHE=ROOT/'tmp/literature/slo-formative-followup-20261117'
PRIOR='data/literature_evidence/SLO_EDR_2013_INQUIRY_SELECTED_review_notes.json'
PRIOR_SHA='05bdad301852559e53b64f6758469581d459229a08a5fccf31b2fad36d3bacf3'
PRIOR_BIB='f95f6fe0a73fb617757dea59c7f1d6ec53ec7b6aac7bfd6fe6cf11066b45f636'
NOTES='data/literature_evidence/SLO_EDR_2013_formative_followup_review_notes.json'
URL='https://www.slo.nl/publish/pages/4474/educational-design-research-part-a.pdf'
SHA='952ca654a1d44ed91cd9304e7d8386b3b7bbd0d7364a61c2c60dd41600f18110'
NEW_TEXT=[4,*range(162,171)];NEW_VISUAL=[4,153,*range(162,171)]
TITLE='Educational Design Research Part A: selected introduction, contents and complete formative-evaluation chapter6, revised November2013'
SCOPE='개정2013년 Part A206쪽 중 누적30쪽 추출문·31쪽 판면을 대조했다. 이전20쪽에 목차PDF4·6장 나머지PDF162–170의10쪽 추출문과 이10쪽 및 삽화PDF153의11쪽 판면을 더했다.6장은 PDF153–170(인쇄152–169), 삽화·본문·표2·부록 그림2/3·참고문헌을 포함해 확인했다. PDF153은 추출 글자가 없는 삽화로 빈 쪽이나 텍스트 독해로 세지 않는다.1장 등은 여전히 선정 범위이며 전권 독해가 아니다.'
LIMITS='전문 연구의 관점을 학교 개발 탐구에 자체 확장한다. 전체 Part A·Part B51사례·인용 원연구·도구 원본/현행 링크·실제 학생 수행은 미확인이다.6장 결론은 측정 도구 개발·자료 수집/분석·보고의 상세 방법을 다루지 않았다고 밝힌다. 자체 기록지·발문은 별도 설계이지 출처가 검증한 척도나 학생 효과가 아니다. 부록/그림의 matchboard2012와 참고문헌2011의 연도 차는 확인했으나 작성 의도·정식 판본 동일성·정오표는 미확인이다.'
LI='12수과02-01';DE='12수과02-04';PL='12수과03-01';RU='12수과03-02';OU='12수과03-03';RE='12수과03-04'
def c(n,codes,pages,support,limit):return dict(id=f'FEV17-{n:02d}',source_id=SOURCE,role='related_theoretical_context',standard_codes=codes,locations=[f'PDF{p} / 인쇄{p-1}' for p in pages],support=support,does_not_establish=limit,independent_review=False,student_validated=False)
CLAIMS=[
 c(1,[DE,PL],[162,163,167,168],'산출물의 개발 단계·확인할 품질·질문을 먼저 적고 그 질문에 맞는 검토 방법과 자료를 고르는 자체 계획에 참고한다. 표2와 부록의 권고/기타 가능성을 구별하고 부분 시제품의 예상 실용성에는 전문가 반응·함께 따라 해 보는 방법을 대조한다.','표를 모든 학생 탐구의 필수 순서·자동 선택 규칙으로 쓰지 않는다. 같은 도구라도 질문·사용 맥락에 맞는 이유가 필요하며 방법을 골랐다는 사실만으로 실제 수행·효과가 생기지 않는다.'),
 c(2,[DE,RU],[162,163,168],'작성자 점검, 응답자의 시제품 반응, 대상자와의 사용 시연, 정상 맥락 밖 소규모 부분 사용, 현장 사용을 구별해 개발 시험의 실제 수행 범위를 기록한다. 질문지·인터뷰·관찰·시험·로그는 방법의 이름과 별도로 적는다.','계산·화면 작동·전문가의 예상·자체 역할극을 실제 대상자의 현장 사용으로 승격하지 않는다. 일부 사용 결과를 모든 사용 맥락이나 인과적 학습 효과로 일반화하지 않는다.'),
 c(3,[PL,RU],[164,165],'개선할 문제를 잘 드러낼 대상·역할을 질문에 맞게 선정하고 선정 이유와 미참여 범위를 적는 계획에 참고한다. 전문 지식의 평가자·처음 쓰는 학습자·수정 제안자의 역할은 한 사람에게 겹칠 수 있다.','목적 표집은 모집단 대표성·고정 최소 인원·통계적 정밀도를 보장하지 않는다. 학습 수준 집단을 나눈 원문의 예를 모든 수업의 의무 분류·참여자 수 처방으로 쓰지 않는다.'),
 c(4,[RU,OU],[164,165,166],'사용자가 말한 설명·직접 관찰·산출물·다른 시점의 기록을 같은 버전과 과제에 맞춰 대조하고 일치하지 않는 근거도 남긴다. 방법·시점·대상·장소를 달리한 대조의 목적을 보고한다.','같은 사람의 여러 의견을 독립 참여자 여러 명으로 세지 않는다. 자료 종류를 늘리거나 일치하는 응답만 고르는 것으로 편향 제거·인과·모집단 일반화를 입증하지 않는다.'),
 c(5,[OU,RE],[165,166],'작성자가 초기에 직접 검토할 때의 배움과 자기 산출물에 대한 애착·응답자의 호의적 반응 가능성을 함께 기록한다. 실제 외부 의견과 자기평가를 구별하고 반대 의견·수정/보류 이유를 성찰에 포함한다.','외부 검토 권고를 실제 독립 검토가 있었다는 근거로 쓰지 않는다. 작성자 내부의 반복 검사나 가상 동료 답변은 외부 독립 검토·실제 학생 반응의 수를 늘리지 않는다.'),
 c(6,[LI,RE],[166,167,168,169,170],'읽은 장의 범위·그림/본문/참고문헌의 표기 차와 아직 읽지 않은 원연구를 나눠 기록한다. 부록의 용어·모형을 참고하되 측정 도구·분석·보고 절차는 자신의 계획으로 명시한다.','6장 독해를 Part A전권·Part B사례·인용 문헌의 검증으로 확대하지 않는다. matchboard의2012/2011 표기를 임의로 통일하거나 자체 기록지를 원문이 검증한 평가 도구로 소개하지 않는다.')]
def p(n,code,q,e,i):return dict(id=f'FE-P{n:02d}',standard_codes=[code],question=q,expected=e,interpretation=i,student_validated=False)
OBSERVATIONS=[
 p(1,PL,'아직 일부만 만든 분수 설명 도구가 학생에게 쓸 만할지 알아보려 한다. 단계·품질·질문·방법·자료를 어떻게 계획할 것인가?','부분 시제품·예상 실용성을 표시하고 어떤 설명/조작에서 막힐지 질문한다. 전문가 반응이나 대상자와 함께 따라 해 보는 검토를 고려하며 참가자 역할·버전·체크/관찰 항목을 정한다.','표2의 한 조합을 학교 탐구에 자체 적용한 계획이다. 실제로 하지 않았다면 미실행이며 원문의 표가 표본 수나 모든 학생의 필수 절차를 정해 주지 않는다.'),
 p(2,DE,'작성자가 계산9개를 통과시키고 혼자 학생 역할을 해 보았다. 이를 대상자 walkthrough·실제 사용성 검증이라고 쓸 수 있는가?','작성자의 계산/자체 점검으로 기록한다. 대상자와 함께 실제로 따라 한 기록이 없으므로 대상자 시연을 했다고 쓰지 않는다. 실제 사용 맥락·사용자의 행동·목표 결과를 별도 확인할 계획을 남긴다.','원문 방법 이름과 수행 근거를 맞춘다. 계획·자체 점검·실제 대상자의 수행과 학습 결과를 같은 완료 표시로 합치지 않는다.'),
 p(3,RU,'대상자 몇 명이 도구 일부를 교실 밖에서 사용한 기록과 실제 수업 전체의 사용 기록은 어떻게 구분할 것인가?','부분·정상 맥락 밖의 소규모 사용과 현장 사용을 구별해 과제·시간·버전·대상·장소·사용 범위를 적는다. 관찰·인터뷰·시험 등 실제로 얻은 자료와 미실행 항목을 나눈다.','구체 기록이 없는 이 질문 자체는 학생 수행이 아니다. 방법 이름만으로 모든 현장·학생에게 일반화하거나 효과의 원인을 도구로 확정하지 않는다.'),
 p(4,PL,'잘 아는 친구만 검토자로 고르면 충분한가? 학습자·비평자·수정 제안자의 역할과 목적 표집의 한계를 설명하라.','질문이 처음 사용하는 사람의 이해인지 수학 내용의 정확성인지 구별하고 그에 맞는 역할·선정 이유를 적는다. 한 사람이 여러 역할을 할 수 있으나 그 사실을 밝힌다. 얻지 못한 관점도 기록한다.','원문의 정보가 풍부한 소규모 선정 논리를 참고하지만 대표 표본이라고 하지 않는다. 정해진 숫자나 학생 능력 집단을 의무로 만들지 않는다.'),
 p(5,OU,'가상 검토에서 A가2개,B가2개,C가1개의 의견을 냈다. 인터뷰에서 쉽다고 했지만 관찰에서는 같은 조작에 막혔다면 무엇을 보고할 것인가?','의견5개·참여자3명을 구별한다.3개의 독립 학습 효과로 세지 않는다. 같은 버전·과제인지 확인하고 말과 행동의 불일치·다른 설명 가능성·추가 확인을 함께 기록한다.','A/B/C와 수는 자체 가상 예다. 익명의 실제 참여 기록이 없는데 실제 응답으로 채우지 않으며 여러 의견·자료 종류가 자동으로 편향을 없애지 않는다.'),
 p(6,RE,'직접 만든 도구에 대한 칭찬만 받았고 외부 검토는 아직 없다. 자기평가와 독립 검토·수정 결정을 어떻게 기록할 것인가?','검토자의 실제 역할·받은 날짜·원문 의견을 구별하고 작성자 애착과 상대의 호의 가능성을 적는다. 사전 기준·반대 사례를 다시 확인하며 채택/보류의 이유를 남긴다. 외부 미실행은 그대로 표시한다.','이 기대 설명은 실제 칭찬·비판을 확보했다는 기록이 아니다. 작성자 검사와 가상 답변을 외부 독립 검토로 세지 않는다.'),
 p(7,LI,'6장의 부록은 matchboard2012라 하고 참고문헌은2011이라 한다.6장에는 자료 분석·보고의 상세 방법도 모두 제시됐는가?','두 위치의 연도 차를 남기고 도구 원본·정오표·판본은 미확인으로 둔다. 결론이 도구 개발·자료 수집/분석·보고의 상세 방법을 다루지 않았다고 밝힌 점을 적는다.','참고 목록을 읽은 것과 그 원문을 읽은 것을 구별한다. 출처가 다루지 않은 절차를 원문 인용인 것처럼 보태지 않는다.'),
 p(8,DE,'[자체 탐구 기록지의 검증 계획](https://math-learning-atlas-kr.gptpro2908176.chatgpt.site/inquiry-workbook.html#evaluation-plan)에 지금 있는 근거와 다음에 확인할 근거를 나눠 적어 보라.','개발 단계·질문·계획/실행·역할·버전·수집할 자료·판단 기준을 먼저 정하고 실제 사용 뒤에만 관찰/응답을 적는다. 근거 위치·제한·수정 전후·재확인과 미실행 범위를 남긴다.','기록지는 이 프로젝트의 자체 설계다. 빈칸 제공·인쇄·코드/계산 검사만으로 사용성·타당화된 척도·학생 효과가 검증된 것이 아니다.')]
INTERPRETATIONS={}
for rid in ['SEC_12수과03-01_C04','HP-inquiry-execution']:
 INTERPRETATIONS[rid,'FEV17-03']=('activity_context','질문에 맞는 대상·역할·목적 표집의 이유와 미참여 범위를 계획하고 실제 수행 기록과 대조한다.','목적 표집·역할의 겹침을 대표성이나 고정 표본 수 처방으로 바꾸지 않는다. 실제 참여 근거가 없으면 계획으로 남긴다.')
for rid in ['SEC_12수과03-02_C04','HP-inquiry-presentation']:
 INTERPRETATIONS[rid,'FEV17-04']=('inference_limit','수행에서 얻은 설명·관찰·산출물을 같은 버전·과제에 맞춰 보고하고 불일치와 후속 확인을 남긴다.','자료 종류·의견 수를 독립 참여자 수로 바꾸거나 여러 기록의 존재만으로 편향 제거·인과·모집단 일반화를 주장하지 않는다.')
for rid in ['SEC_12수과03-03_C04','REV-12수과03-04-1','HP-inquiry-reflection']:
 INTERPRETATIONS[rid,'FEV17-05']=('inference_limit','발표 뒤 실제 받은 의견과 자기평가를 구분하고 작성자 애착·응답자의 호의 가능성·수정/보류 이유를 성찰한다.','가상 의견이나 작성자 내부 재검사는 실제 외부 독립 검토·실제 학생 응답을 추가하지 않는다. 출처의 권고를 현장 검증의 완료로 쓰지 않는다.')
def main():
 registry=load_registry();known={c['id'] for c in registry['claims']};newids={c['id'] for c in CLAIMS}
 if newids<=known:
  assert registry['sources'][SOURCE]['snapshot_file']==NOTES;build_report();return
 assert not newids&known
 s=registry['sources'][SOURCE];assert s['snapshot_file']==PRIOR and s['snapshot_sha256']==PRIOR_SHA and s['bibliography_snapshot']==PRIOR_BIB
 assert sha(ROOT/PRIOR)==PRIOR_SHA and sha(CACHE/'slo-design-part-a-2013.pdf')==SHA
 reader=PdfReader(CACHE/'slo-design-part-a-2013.pdf');assert len(reader.pages)==206
 assert all(reader.pages[p-1].extract_text().strip() for p in NEW_TEXT) and not reader.pages[152].extract_text().strip()
 acquisition=load(CACHE/'acquisition.json');assert acquisition['reading_completed'] and acquisition['images_viewed'] and acquisition['new_text_pages']==NEW_TEXT and acquisition['new_visual_pages']==NEW_VISUAL
 old_source=copy.deepcopy(s);old_notes=load(ROOT/PRIOR);old_claims=[copy.deepcopy(c) for c in registry['claims'] if c['source_id']==SOURCE];assert len(old_claims)==8 and len(s['observations'])==16
 assert not set(NEW_TEXT)&set(old_notes['selected_text_pages']) and not set(NEW_VISUAL)&set(old_notes['visual_pdf_pages'])
 for page,expected in old_notes['rendered_page_sha256'].items():assert sha(ROOT/f'tmp/literature/stat-inquiry-completion/rendered/slo-design-part-a-2013-{page}.png')==expected
 images={str(p):sha(CACHE/f'rendered/slo-design-part-a-2013-{p}.png') for p in NEW_VISUAL}
 assert not {o['id'] for o in OBSERVATIONS}&{o['id'] for src in registry['sources'].values() for o in src.get('observations',[])}
 relations=load(ROOT/'data/revised_relations.json')['relations'];pairs={(x['id'],c['id']) for x in relations for c in CLAIMS if all(x[k].startswith('standard:') for k in ['from','to']) and {x[k][9:] for k in ['from','to']}<=set(c['standard_codes'])}
 assert pairs==INTERPRETATIONS.keys() and len(pairs)==7
 reviewed=load(ROOT/FILE);old_relation_rows=[copy.deepcopy(x) for x in reviewed['records'] if x['claim_id'] in {c['id'] for c in old_claims}];assert len(old_relation_rows)==10
 bibliography=load(ROOT/'data/sources.json');entry=next(x for x in bibliography if x['id']==SOURCE);old_entry=copy.deepcopy(entry)
 entry.update(title=TITLE,review_scope=SCOPE,does_not_establish=LIMITS,next_review=LIMITS)
 notes=copy.deepcopy(old_notes);notes.update(date=DATE,read_scope=SCOPE,selected_text_pages=sorted(old_notes['selected_text_pages']+NEW_TEXT),visual_pdf_pages=sorted(old_notes['visual_pdf_pages']+NEW_VISUAL),rendered_page_sha256={**old_notes['rendered_page_sha256'],**images},previous_review=old_source,previous_bibliography=old_entry,previous_claims=old_claims,previous_observations=copy.deepcopy(s['observations']),previous_relation_records=old_relation_rows,previous_notes_file=PRIOR,previous_notes_sha256=PRIOR_SHA,reading_log=old_notes['reading_log']+['2026-11-17: 목차·6장 후반과 부록/참고문헌의 새 추출문10쪽·판면11쪽을 실제 대조했다. PDF153은 삽화이며 추출문 쪽에 포함하지 않는다. 기존20쪽은 해시·읽기 이력을 보존했다.'],source_corrections=old_notes['source_corrections']+[dict(location='PDF153',issue='글자 추출이 비어 있지만 실제 판면에는 건축 삽화가 있다. 빈 페이지·텍스트 독해 쪽으로 세지 않는다.'),dict(location='PDF163 Table2; PDF167–168 Figures2/3',issue='표의 행/열·회색 강조와 부록의 권고/기타 가능성을 판면으로 구별했다. PDF160의 추출 라벨을 그쪽 그림에 넣지 않았던 이전 판단은 유지한다. 방법 표2는 실제PDF163에 있다.'),dict(location='PDF167–168 vs PDF170',issue='matchboard는 부록·그림에서2012, 참고문헌에서2011이다. 이 차이를 보존하며 원도구 판본·정오표는 미확인이다.'),dict(location='PDF166 Closing remark',issue='원문은 측정 도구 개발·자료 수집·분석·보고의 상세 방법을 다루지 않았다고 명시한다. 새 기록지의 구체 절차는 자체 설계다.')],formative_followup=dict(new_text_pages=NEW_TEXT,new_visual_pages=NEW_VISUAL,cumulative_text_pages=30,cumulative_visual_pages=31,chapter6_all_pdf_pages=list(range(153,171)),chapter6_complete_with_prior_reading=True,image_only_divider=153,all_part_a_read=False,part_b_read=False,cited_originals_read=False,matchboard_original_verified=False,own_protocol_not_validated_instrument=True))
 write(ROOT/NOTES,notes)
 history=s.get('snapshot_history',[])+[dict(snapshot_file=PRIOR,snapshot_sha256=PRIOR_SHA,date=old_source['date'],read_scope=old_source['read_scope'])]
 s.update(date=DATE,snapshot_file=NOTES,snapshot_sha256=sha(ROOT/NOTES),snapshot_history=history,bibliography_snapshot=digest(entry),read_scope=SCOPE,limits=LIMITS,method_note='6장 전체의 누적 본문/판면·표/그림·부록·참고문헌을 대조하고 학교 개발 탐구의 자체 계획에 확장했다. 인용 원문·실제 독립/학생 검증은 미완료다.',editorial_action='같은 출처에 새 주장6건·자체 과제8개를 더했다. 기존 주장8건·과제16개는 그대로 보존하고 관련10개 관계의 출처 해시를 명시적으로 재검토했다.',observations=s['observations']+copy.deepcopy(OBSERVATIONS),display={**s['display'],'title':TITLE})
 for claim in copy.deepcopy(CLAIMS):
  claim.update(empirical_scope=copy.deepcopy(s['empirical_scope']),target_snapshots={f'revision:{code}':digest(target_value(f'revision:{code}')) for code in claim['standard_codes']});registry['claims'].append(claim)
 by_claim={c['id']:c for c in registry['claims']};by_relation={x['id']:x for x in relations}
 for row in reviewed['records']:
  if row['claim_id'] in {c['id'] for c in old_claims}:row['claim_snapshot']=claim_snapshot(by_claim[row['claim_id']],s)
 for (rid,cid),(role,finding,limit) in INTERPRETATIONS.items():reviewed['records'].append(dict(relation_id=rid,claim_id=cid,role=role,finding=finding,limit=limit,relation_snapshot=relation_snapshot(by_relation[rid]),claim_snapshot=claim_snapshot(by_claim[cid],s)))
 apply_literature_context(relations,registry,registry=reviewed)
 queue=load(ROOT/'data/content_review_queue.json');row=next(x for x in queue['literature_review'] if x['source']['id']==SOURCE);row.update(source=entry,claim_ids=[c['id'] for c in registry['claims'] if c['source_id']==SOURCE])
 write(ROOT/'data/sources.json',bibliography);write(ROOT/'data/literature_claim_reviews.json',registry);write(ROOT/'data/content_review_queue.json',queue);write(ROOT/FILE,reviewed);build_report()
 print('Extended same SLO source:6 claims,8 own tasks,7 relation entries;all prior claims/tasks and720 relation interpretations preserved')
if __name__=='__main__':main()
