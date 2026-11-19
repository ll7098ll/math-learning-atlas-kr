"""Review the available author article text without inventing PDF or WWC samples."""
import copy,hashlib,json
from literature_review import ROOT,load_registry,read,digest,target_value,build_report
from relation_literature_review import FILE,claim_snapshot,relation_snapshot,apply_literature_context
from check_inversion_observation_models import check

SOURCE='LAI_BAROODY_JOHNSON_2008_INVERSION';GUIDE='IES_EARLY_2013'
URL='https://doi.org/10.1016/j.cogdev.2007.06.002'
AUTHOR='https://www.academia.edu/48267500/Fostering_Taiwanese_preschoolers_understanding_of_the_addition_subtraction_inverse_principle'
NOTES=f'data/literature_evidence/{SOURCE}_review_notes.json'
EXTENSION='data/literature_evidence/IES_EARLY_2013_lai_original_followup_review_notes.json'
CACHE=ROOT/'tmp/literature/lai-original-20261118'
SCOPE='저자명으로 공개된 웹 전사문의 초록·방법·채점·표1–4의 텍스트·결과·논의·참고문헌 대목을 읽고 가이드D.4·미주21 및 공식WWC77971 웹/내려받기 자료와 대조했다. 논문216–235쪽의 PDF파일·실제 판면과 그림1–4는 확보·대조하지 않았다.'
LIMIT='두 대만 공립유아학교의4·5세 아동과 활동을 받은 비교 조건에 관한 연구다. 학교와SES가 겹치며 한국 학생·개별 과제 효과·고정 발달 시점을 입증하지 않는다. 전사문의 표본/채점 표기와 가이드의30명은 미해결이며 원판·원자료·공식 정오표는 미확인이다.'
TEXT=dict(url=AUTHOR,uploaded_by='Menglung Lai (공개 검색에 표시된 이름;계정 소유·업로드 경위는 미검증)',article_pdf_obtained=False,article_printed_pages=[216,235],selected_sections=[dict(section=s,printed_pages=p) for s,p in [('초록·서론·개념/계산 구별',[216,219]),('대상·절차·과제',[219,223]),('채점·표2·오류 유형',[223,226]),('활동·결과·표3/4 텍스트',[226,229]),('논의·교육 함의·제한',[230,233]),('감사·참고문헌',[233,235])]])
OBSERVATIONS=[
 dict(id='LBI08-P1',standard_codes=['2수01-05','2수01-07'],question='처음 구슬 수를 세지 않은 상자에3개를 넣고 다른 구슬3개를 꺼냈다. 처음보다 많아졌는지, 같아졌는지, 적어졌는지 설명하라.3개를 넣고2개만 꺼내면 어떻게 될까? 마지막 구슬 수까지 알 수 있을까?',expected='처음에는 같은 수를 넣고 꺼내 수량이 같다. 같은 구슬을 꺼낼 필요는 없다. 두 번째에는 처음보다1개 많다. 처음 수를 모르므로 마지막의 정확한 개수는 정할 수 없다.',interpretation='수량의 관계와 개체 동일성, 정확한 개수 계산을 구별한다. 답을 고르는 것과 두 변화가 상쇄되는 이유를 설명하는 것을 따로 기록한다. 원논문의 원문 문항·검증된 국내 평가가 아닌 자체 과제다.',student_validated=False),
 dict(id='LBI08-P2',standard_codes=['2수01-07'],question='처음4개 이상 든 상자의 정확한 구슬 수는 모른다.3개 넣고2개 꺼내기,2개 꺼내고3개 넣기,1개 넣고3개 꺼내기,4개 꺼내고2개 넣기를 처음 수와 비교하라. 모든 역관계 문항에 ‘같다’고만 답한 기록도 이해의 증거가 되는가?',expected='앞의 두 경우는 처음보다1개 많고 뒤의 두 경우는2개 적다. 마지막 행동이 꺼내기여도 전체는 늘 수 있다. 같은 수를 넣고 빼는 문항만 모두 맞힌 응답은 일정한 답을 반복한 것일 수 있으므로 변화가 남는 문항과 설명도 확인한다.',interpretation='역관계와 비역관계의 응답을 함께 보되, ‘다르다’와 변화의 올바른 방향을 별도로 기록한다. 원문 채점 규칙의 모호함을 그대로 등급 기준으로 옮기지 않는다.8문항의 우연확률 계산은 교사용 점검이며 현재 학생의 단계·효과를 판정한 자료가 아니다.',student_validated=False),
]
CLAIMS=[
 ('LBI08-01',['2수01-05','2수01-07'],'웹 전사문 인쇄216–223·230–233쪽의 과제와 논의','연구는 처음 수를 직접 계산하기 어려운 가림 과제와 상쇄/비상쇄 변화를 구별했다. 같은 답을 얻는 계산과 처음 수를 몰라도 설명하는 역관계, 다른 개체를 꺼내도 같은 수량이 되는 이유를 나눠 묻는 데 참고한다.','그림1–4의 실제 배치·연결선은 보지 않았다. 가이드30명과 초록/방법/결과60명, 절차의30명 표기는 미해결이다. 모든 아동의 필수 순서나 현재 과제 효과로 확대하지 않는다.'),
 ('LBI08-02',['2수01-07'],'웹 전사문 인쇄220–229쪽의 연습·채점·오류 분석','연습 때의 피드백, 재시도 정답의0.5점, 역관계와 통제 문항의 응답 편향을 구별했다. 처음 응답·도움·재시도·정확한 변화 방향을 따로 남기는 관찰에 참고한다.','항상 같은 답을 한 기록은 개념 이해와 다르다. 전사문의 통제 문항 확률/기준·같다/많다 표기는 원판 미대조 상태여서 자체 등급표로 복사하지 않는다. 활동을 받은 비교군과 무처치,2주 활동과8주 전체 절차를 구별한다.'),
]
def write(p,v):(ROOT/p).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256((ROOT/p).read_bytes()).hexdigest()

def main():
 registry=load_registry()
 if SOURCE in registry['sources']:print('Existing review retained');return
 evidence=json.loads((CACHE/'reading-evidence.json').read_bytes());assert evidence['reading_completed'] and len(evidence['text_lines_read'])==147 and evidence['wwc_export_finding_rows']==0
 previous=copy.deepcopy(registry);bibliography=read(ROOT,'data/sources.json');queue=read(ROOT,'data/content_review_queue.json');reviews=read(ROOT,FILE)
 empirical=dict(design='individual_randomized_active_comparison_with_observed_school_SES',sample_description='초록·대상 절·집단별 결과는60명/30명씩, 절차 전사문과가이드 표는30명/15명씩으로 서로 다른 수를 적는다. 두 학교·두 연령 집단이며 정확한WWC분석 표본은 미확인이다.',inference_limit=LIMIT,local_effect_tested=False)
 notes=dict(source_id=SOURCE,source_url=URL,source_asset_kind='author_web_text',author_text_review=TEXT,read_scope=SCOPE,date='2026-11-18',reviewer='Codex',original_page_layout_review=False,pdf_read=False,contains_source_full_text=False,source_pdf_redistributed=False,empirical_scope=empirical,reading_evidence=evidence,exact_own_checks=check(),all_cited_originals_read=False,publisher_binary_fidelity_verified=False,official_erratum_verified=False,raw_student_data_read=False,independent_review=False,student_validated=False,
  reading_log=['초록부터 참고문헌까지 웹 추출문147행의 지정 대목을 읽었다. 표의 병합/열 순서와 그림은 전사문만으로 복원하지 않았다. 원판20쪽 독해·판면 대조로 세지 않는다.','대상 절의4세30명+5세30명·학교별30명, 집단별 결과30명씩과 절차의30명 표기를 함께 기록했다. 가이드0.54*의 분석 분모·하위 표본을 확정하지 않았다.','처음5/7개를 바로 알아보기 어렵게 고른 점·덧셈먼저/뺄셈먼저·8역관계/8통제·서로 다른 장난감/배치를 읽었다. 원문은 빠른 정답만으로 개념을 판정하지 않는다.','두 학교는각각다른SES지역이다. SES의 인과 효과와 학교 차이를 분리했다고 주장하지 않는다. 전체8주 절차와2주 활동, 약10분3회 역관계 활동 및 별도 합성/분해 비교 활동을 구별한다.','원문의ANCOVA·비모수검사·변화점수ANOVA는 다른 결과/검정이다. p=.055·.06·.057·.10을5%유의로 바꾸지 않는다. 부분점수·오류패턴 제외와 이항분포의 독립 이진 모형도 구별한다.','공식77971은2013년2.1심사·RCT·기준충족으로 표시하지만 해당 ZIP의 Studies1행/Findings0행에는30/60의 결과 분모가 없다. 빈 결과를 효과0이나 재현 분석 완료로 세지 않는다.'],
  source_corrections=[dict(kind='sample_scope_unresolved',location='웹 대상/절차/결과;가이드PDF90·95',issue='전체60명·집단30명씩과절차30명·가이드15명씩이 공존한다. 연령 하위 집단이 존재해도 어느 하위 집단을가이드가썼는지는확정할수없다.'),dict(kind='chance_model_wording_open_without_pdf',location='웹 인쇄223·226쪽 채점',issue='전사문은 통제 문항의 우연정답2/3·7/8기준에p=.04를 적는다. 독립 이진모형에서2/3이면상측확률1280/6561≈.195,1/2이면9/256≈.035다. 정확한 방향만 인정하는3지선다모형은17/6561이다. 모형과 채점 수용 범위를 명시하지 않으면 대체할 수 없다.'),dict(kind='transcription_or_source_wording_unresolved',location='웹 인쇄226쪽E.1설명·표3텍스트',issue='같다 응답편향 설명에 많다라고 적힌 대목과 표3의 행 이름/열 배치가 불명확하다. 원판·정오표 확인 전 출판 오류로 확정하거나 표를 복원하지 않는다.')])
 entry=dict(id=SOURCE,year=2008,title='Fostering Taiwanese preschoolers’ understanding of the addition–subtraction inverse principle',authors=['Lai, M.-L.','Baroody, A. J.','Johnson, A. R.'],url=URL,kind='역관계 과제·응답 편향 원연구의 웹 전사문 대조',review_scope=SCOPE,does_not_establish=LIMIT,next_review='출판 PDF·그림·표의 판면, 가이드 분석 분모와 원자료·정오표를 확인한다.',supports='숨겨진 처음 수·수량과 개체·응답 편향·지원과 재시도 기록 구별')
 write(NOTES,notes);bibliography.append(entry)
 article=dict(source_id=SOURCE,state='self_read_claim_mapping',reviewer='Codex',date='2026-11-18',snapshot_kind='authored_review_notes',source_asset_kind='author_web_text',author_text_review=TEXT,snapshot_file=NOTES,snapshot_sha256=sha(NOTES),redistribution_license='workspace_authored_notes',bibliography_snapshot=digest(entry),display=dict(title=entry['title'],url=URL,authors_year='Lai·Baroody·Johnson,2008'),read_scope=SCOPE,scope_note='처음 수를 모르는 역관계 설명과 계산 정답, 응답 편향·재시도·지원 조건을 구별한다. 전사문·공식 심사 기록 대조는 출판 PDF 판면 대조가 아니다.',method_note='공개 전사문의 선정 절과 공식WWC77971 HTML/ZIP을 대조하고 이항모형·항등식의 자체 예를 정확 검산했다.',limits=LIMIT,empirical_scope=empirical,observations=OBSERVATIONS,independent_review=False,student_validated=False,editorial_action='주장2건·자체 과제2개와 기존 관계1개의 맥락1건을 추가했다. 가이드의 표본 차이는 보류한다.')
 registry['sources'][SOURCE]=article
 for cid,codes,location,support,limit in CLAIMS:registry['claims'].append(dict(id=cid,source_id=SOURCE,role='empirical_result_with_scope',locations=[AUTHOR+' '+location],standard_codes=codes,support=support,does_not_establish=limit,empirical_scope=empirical,independent_review=False,student_validated=False,target_snapshots={f'revision:{code}':digest(target_value(f'revision:{code}')) for code in codes}))
 queue['literature_review'].append(dict(source=entry,status='self_read_claim_mapping',evidence_file='data/literature_claim_reviews.json',claim_ids=[x[0] for x in CLAIMS],claim_evidence_fields=['처음 수·역관계와 비역관계','응답 편향·재시도와 지원','전사·원판·공식분모의 범위']))
 guide=registry['sources'][GUIDE];old_guide=previous['sources'][GUIDE];prior_extension=copy.deepcopy(guide['reading_extension']);extension=read(ROOT,prior_extension['file']);old_extension=copy.deepcopy(extension)
 correction=next(x for x in guide['source_discrepancies'] if x['status']=='lai_analytic_sample_scope_open')
 correction['followup']='2026-11-18 공개 전사문의 대상·결과는60명/집단30명씩, 절차에는30명이 적혀 있다. 공식77971ZIP은결과0행이어서15명씩의분석대상을확정할수없다. 가이드30명·0.54*와원논문전체를분리하며원판·WWC분석근거확인전표본을교체하지않는다.'
 guide['scope_note']+=' Lai2008 공개 전사문과 공식77971을 추가 대조했으나30/60의분석범위는여전히미확인이다. 처음 수를 모르는 관계 설명·응답 편향·부분점수·지원 조건을 구별한다.'
 guide_entry=next(x for x in bibliography if x['id']==GUIDE);old_bib=copy.deepcopy(guide_entry)
 guide['read_scope']='가이드165쪽·별도심사프로토콜2.1의9쪽에대한기존전체추출문/판면대조범위를유지한다. Lai2008공개웹전사문과공식77971을추가대조했으며이번새가이드추출문·판면은0쪽이다.'
 guide_entry['review_scope']=guide['read_scope'];guide['bibliography_snapshot']=digest(guide_entry)
 next(x for x in queue['literature_review'] if x['source']['id']==GUIDE)['source']=guide_entry
 guide['reading_log']+=['가이드PDF90·95의기독해본문을Lai2008공개전사문/공식77971자료와다시대조했다. 새가이드추출문·판면은0쪽이다.30/60은미해결이며PDF판면과원자료는별도다.']
 guide['editorial_action']+=' 2026-11-18: Lai원연구 전사문과공식심사자료의대조를추가하고IE14한계를명확히했다. 기존과제14개를보존한다.'
 cross=dict(source_id=SOURCE,claim_ids=[x[0] for x in CLAIMS],snapshot_file=NOTES,snapshot_sha256=article['snapshot_sha256'],guide_sample=30,article_abstract_and_participants_total=60,article_group_n=[30,30],procedure_text_total=30,exact_wwc_sample_verified=False,wwc_export_finding_rows=0)
 guide.setdefault('primary_source_crosschecks',[]).append(cross)
 extension.update(previous_review=old_guide,previous_reading_extension=prior_extension,previous_bibliography=old_bib,cumulative_read_scope=guide['read_scope'],new_text_pdf_pages=[],new_visual_pdf_pages=[],new_image_records=[],new_image_sha256={},reading_log=guide['reading_log'],source_corrections=guide['source_discrepancies'],lai_original_crosscheck=cross)
 extension['previous_protocol_review']=copy.deepcopy(extension['protocol']);extension['protocol'].update(new_visual_pdf_pages=[],new_text_pdf_pages=[])
 write(EXTENSION,extension);guide['reading_extension']=dict(file=EXTENSION,sha256=sha(EXTENSION))
 claim=next(x for x in registry['claims'] if x['id']=='IE14');claim['does_not_establish']='가이드의30명과공개전사문의대상·결과60명,절차30명을구별한다. 공식77971내려받기자료는결과행이비어정확한WWC분모를확인하지못했다. 원판·분석자료확인전하위표본이나오자로단정하지않으며국내과제효과·전체연산전이를입증하지않는다.';claim['recommendations'][0]['application_limit']=claim['does_not_establish']
 claims={x['id']:x for x in registry['claims']};oldclaims={x['id']:x for x in previous['claims']}
 for row in reviews['records']:
  if claims[row['claim_id']]['source_id']==GUIDE:
   assert row['claim_snapshot']==claim_snapshot(oldclaims[row['claim_id']],old_guide)
   row['claim_snapshot']=claim_snapshot(claims[row['claim_id']],guide)
 relations=read(ROOT,'data/revised_relations.json')['relations'];relation=next(x for x in relations if x['id']=='REV-2수01-07-1')
 reviews['records'].append(dict(relation_id=relation['id'],claim_id='LBI08-01',role='activity_context',finding='처음 수를 모르는 상자에서 같은 수를 넣고 빼는 변화와1개가남는변화를비교하고,답과이유·지원전후를따로기록한다.',limit='역관계문항에같다고일률응답한것은이해의증거가아니다. 원판·정확한WWC분모·현재과제효과는미확인이며이연결을보편적인필수순서로읽지않는다.',relation_snapshot=relation_snapshot(relation),claim_snapshot=claim_snapshot(claims['LBI08-01'],article)))
 apply_literature_context(relations,registry,registry=reviews)
 write('data/sources.json',bibliography);write('data/content_review_queue.json',queue);write('data/literature_claim_reviews.json',registry);write(FILE,reviews)
 p=ROOT/'docs/분수단위조정관찰기록.md';body=p.read_text(encoding='utf-8');body+='\n\n## Lai2008 웹 전사문 대조에 따른 자체 관찰\n\n원판 미확보·전사문 대조 범위이며 실제 학생 검증이 아니다.\n\n| 과제 | 적용 기준 | 확인할 구분 |\n|---|---|---|\n| LBI08-P1 | 2수01-05·2수01-07 | 처음 수 미지·수량과 개체·정확한 개수와 상대 변화 |\n| LBI08-P2 | 2수01-07 | 일률 응답·상쇄와 비상쇄·마지막 행동과 전체 변화 |\n';p.write_text(body,encoding='utf-8')
 build_report();print(json.dumps(dict(new_sources=1,new_claims=2,new_tasks=2,new_contexts=1,changed_prior_claims=['IE14'],new_pdf_text_pages=0,new_visual_pages=0,web_article_sections=6)))

if __name__=='__main__':main()
