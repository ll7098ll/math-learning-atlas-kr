"""Audit related textbook evidence without inventing an intervention sample."""
import copy,hashlib,json,csv,io,zipfile
from literature_review import ROOT,digest
from relation_literature_review import claim_snapshot
from check_textbook_aggregation_models import check

GUIDE='IES_EARLY_2013'
NOTES='data/literature_evidence/SOOD_JITENDRA_2007_textbook_audit_notes.json'
IDENTITY='data/literature_evidence/SOOD_publication_identity_followup_notes.json'
EXTENSION='data/literature_evidence/IES_EARLY_2013_textbook_followup_review_notes.json'
def read(p):return json.loads((ROOT/p).read_bytes())
def write(p,v):(ROOT/p).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256((ROOT/p).read_bytes()).hexdigest()

def main():
 l=read('data/literature_claim_reviews.json');old=copy.deepcopy(l);s=l['sources'][GUIDE]
 assert len(l['sources'])==176 and len(l['claims'])==1055 and not (ROOT/NOTES).exists() and not (ROOT/EXTENSION).exists()
 a=read('tmp/literature/sood-textbook-2007-20261118/acquisition.json');assert a['reading_completed'] and a['visual_pdf_pages']==list(range(1,14)) and a['text_pdf_pages']==[] and sha(a['file'])==a['pdf_sha256']
 a['reading_log']=[line.replace('の','의') for line in a['reading_log']]
 for page,digest_value in a['rendered_page_sha256'].items():assert sha(f'tmp/literature/sood-textbook-2007-20261118/rendered/page-{int(page):02d}.png')==digest_value
 acquired=read('tmp/literature/sood-original-followup-20261118/acquisition.json');assets=acquired['assets'];export=next(x for x in assets if x['url'].endswith('/StudyExport/77991'));assert sha(export['file'])==export['sha256']
 with zipfile.ZipFile(ROOT/export['file']) as z:
  studies=list(csv.DictReader(io.StringIO(z.read('Studies.csv').decode('utf-8-sig'))));findings=list(csv.DictReader(io.StringIO(z.read('Findings.csv').decode('utf-8-sig'))))
 assert len(studies)==1 and studies[0]['StudyID']=='77991' and studies[0]['ReviewID']=='68172' and findings==[]
 identity=dict(source_id=GUIDE,date='2026-11-18',reviewer='Codex',contains_source_full_text=False,primary_metadata=[dict(title='An Exploratory Study of a Number Sense Program to Develop Kindergarten Students’ Number Proficiency',authors=['Sheetal Sood','Asha K. Jitendra'],doi='10.1177/0022219411422380',url='https://journals.sagepub.com/doi/10.1177/0022219411422380',university_url='https://experts.umn.edu/en/publications/an-exploratory-study-of-a-number-sense-program-to-develop-kinderg/',online_date='2011-10-04',issue_date='2013-07',journal='Journal of Learning Disabilities',volume=46,issue=4,printed_pages=[328,346],body_obtained=False,abstract_total=101,abstract_classrooms=5,abstract_school_description='one high-poverty elementary school',abstract_control_risk_cells=[22,18],abstract_intervention_risk_cells=[36,25],source_scope='출판사·저자 소속대학의 공개 초록과 서지. 본문·표·그림은 미확보다.')],official_wwc_export=dict(url=export['url'],sha256=export['sha256'],study_rows=1,finding_rows=0,study_id='77991',review_id='68172',citation_year=2009,umi='3373089',protocol='2.1',standards='2.1',rating=studies[0]['Study_Rating'],sample_count_not_available=True,empty_findings_not_zero_effect=True),body_or_sample_identity_verified=False,original_2009_dissertation_read=False,additional_independent_sample_count=0,independent_review=False,student_validated=False)
 identity['interpretation']='2011온라인·2013권호는 같은 DOI다. 초록의40명/61명·101명·5학급은 가이드와 유사하지만 학위논문과 동일 원자료인지 확인하지 못했다.2015논문의135명·9학급과 합치거나 대체하지 않는다. 공식 내보내기의 결과0행으로 정확한 분석 분모나 효과를 복원할 수 없다.'
 identity['asset_metadata']=[x for x in assets if x.get('status')==200]
 write(IDENTITY,identity)
 note=dict(source_id=GUIDE,related_work_id='SOOD_JITENDRA_2007_TEXTBOOKS',date='2026-11-18',reviewer='Codex',related_publication=dict(title='A Comparative Analysis of Number Sense Instruction in Reform-Based and Traditional Mathematics Textbooks',authors=['Sheetal Sood','Asha K. Jitendra'],year=2007,journal='The Journal of Special Education',volume=41,issue=3,printed_pages=[145,157],url=a['url'],pdf_sha256=a['pdf_sha256'],pdf_pages=13),contains_source_full_text=False,source_pdf_redistributed=False,publisher_binary_fidelity_verified=False,text_pdf_pages=[],visual_pdf_pages=list(range(1,14)),rendered_page_sha256=a['rendered_page_sha256'],table2_orientation_reread_pdf_page=6,new_page_count_from_orientation_reread=0,tables_read=[1,2],data_figures=0,reading_log=a['reading_log'],parent_reference=dict(file='data/literature_evidence/SOOD_MACKEY_2015_related_publication_audit.json',pdf_page=15,reference_number=22),design='comparative_textbook_content_analysis',books=['HB2004','HM2005','SF2004','EM2004'],number_sense_lessons=dict(HB=11,HM=6,SF=9,EM=8),all_book_content_read=False,original_coder_records_obtained=False,student_outcome_study=False,local_effect_tested=False,independent_review=False,student_validated=False,official_erratum_verified=False,exact_own_checks=check())
 note['audit_findings']=[
  dict(pdf_pages=[2,3,10],issue='자료 단위와 선정 범위',detail='4종 미국1학년 교사의 지도서에서 수감각 목표 수업만 코딩했다.11+6+9+8=34는 수업 수다. 수 세기는 이전 학년에서 도입됐다는 이유로 제외했다.',action='학생34명·독립연구34건·수감각 전체나2022한국 교과서 평가로 확대하지 않는다.'),
  dict(pdf_pages=[3,4,7,9,10],issue='항목 수와 실제 활동 기회',detail='반복 횟수를 적지 않은 짝 활동은1건으로 세지만 문항7개 학습지는7건으로 센다. 한 항목의 여러 표상은 각각 센다.',action='항목 합계를 고유 과제·실제 반복·수업 시간·학생 이해 수로 바꾸지 않는다.'),
  dict(pdf_pages=[5,6,9],issue='집계·조건별 분모',detail='표2의 수 관계267건/26수업은10.27이나 책별 비율 평균은10.30이다. 수업 내 복습263건/26수업은10.12이나 책별 비율 평균은10.38이다. 표1은10.27과10.38을 싣는다. HM의 충분 복습50건은 전체6수업 분모와 표의25.00이 다르다.',action='모든 행에 같은 합산·분모를 가정하지 않는다. 원 코딩표·편집 근거 없이 원문 수치를 교체하지 않는다.'),
  dict(pdf_pages=[4,5,6,8],issue='조건부 피드백 비율',detail='EM은8수업 중 피드백50%, 그중 설명 피드백50%다. 이를 전체 수업50%나 학생 성취율로 읽을 수 없다.',action='해당 표의 이진 분류를 따르면 전체8수업의 설명 피드백은2수업·25%다. 학생 효과는 측정하지 않았다.'),
  dict(pdf_pages=[5,6,9],issue='미해결 수치',detail='HB의 후속 복습43.83%+54.17%=98%다. 소수 둘째 자리 반올림만으로100%가 되지 않는다. 본문의 전통 교재 수업 내 충분49%·후속42%와 표1의42.31%·59%도 그대로 합치지 않는다.',action='원 코딩표·공식 정오표 확인 전 교정값과 하나의 전체 비율을 확정하지 않는다.'),
  dict(pdf_pages=[4,9,10,11],issue='기준과 학습 효과',detail='동일 수업10문항·후속 수업4문항은 연구의 코딩 기준이다. 재코딩30%의 일치도는 내용 분류의 확인이며 학생 관찰이나 우리 자료의 독립 검토가 아니다.',action='모든 학생에게 필요한 연습량·고정 표상 순서·교재의 인과 효과나 학생 유지 효과로 적용하지 않는다.')]
 write(NOTES,note)
 bib=read('data/sources.json');entry=next(x for x in bib if x['id']==GUIDE);n=read(s['reading_extension']['file']);previous=copy.deepcopy(s['reading_extension'])
 s['read_scope']='가이드165쪽·심사프로토콜9쪽의 기존 전체 대조, Lai2008웹전사문과 Sood·Mackey2015의18판면·추출문1쪽을 보존한다. 관련 Sood·Jitendra2007 교과서 비교 논문13판면을 추가 읽고2013논문 초록·서지와 공식WWC77991 내보내기를 대조했다.2007논문의 전문 추출문·2009학위논문·2013논문 본문은 읽은 범위에 추가하지 않는다. 새 가이드 독해는0쪽이다.'
 s['scope_note']+=' 2007교과서 비교의 항목 수·표상 중복·조건부 비율과 집계 분모를 대조했다.34수업을 학생 수로,10/4문항 코딩 기준을 보편적인 연습량으로 읽지 않는다.2013초록101명·5학급과2009학위논문의 동일 원자료 여부는 미확인이다.'
 s['editorial_action']+=' 2026-11-18: 관련 교과서 비교 원논문13판면과 출판물 식별·공식 내보내기를 대조했다. 원 코딩표·학생 결과·정확한 WWC재분석과 동일 표본을 복원하지 않았으며 신규 효과 주장·과제는0이다.'
 discrepancy=next(x for x in s['source_discrepancies'] if x['status']=='sood_nonverbal_maintenance_discrepancy_open')
 discrepancy['followup']='직후0.37ns와유지0.12ns를 분리한다.2013공개초록도 유지의 긍정 효과를 요약하지만 본문과 원학위논문은 미확보다. 공식77991내보내기는 연구1행·결과0행이다.2015별도논문의 충돌이나2007교재 코딩으로2009유지 효과의 의미를 확정하지 않는다.'
 references=copy.deepcopy(s['related_published_article_audits']);references.append(dict(file=NOTES,sha256=sha(NOTES),original_thesis_read=False,new_effect_claims=0,student_outcome_study=False));s['related_published_article_audits']=references
 identity_ref=dict(file=IDENTITY,sha256=sha(IDENTITY),original_thesis_read=False,new_effect_claims=0)
 s['publication_identity_followup']=identity_ref
 n.update(previous_review=copy.deepcopy(old['sources'][GUIDE]),previous_bibliography=copy.deepcopy(entry),previous_reading_extension=previous,cumulative_read_scope=s['read_scope'],new_text_pdf_pages=[],new_visual_pdf_pages=[],new_image_sha256={},new_image_records=[],related_published_article_audits=references,publication_identity_followup=identity_ref,source_corrections=copy.deepcopy(s['source_discrepancies']))
 n['reading_log'].append('関連2007논문13판면을 읽고2표·항목/수업/표상/비율의 분모를 대조했다.2013논문은 공개 초록·서지만 확인했고 공식 내보내기는1연구·0결과행이었다. 새 가이드·원학위논문·2013본문 독해는0쪽이다.'.replace('関連','관련'))
 write(EXTENSION,n);s['reading_extension']=dict(file=EXTENSION,sha256=sha(EXTENSION));entry['review_scope']=s['read_scope'];s['bibliography_snapshot']=digest(entry)
 q=read('data/content_review_queue.json');next(x for x in q['literature_review'] if x['source']['id']==GUIDE)['source']=copy.deepcopy(entry)
 reviews=read('data/relation_literature_reviews.json');claims={c['id']:c for c in l['claims']};count=0
 for row in reviews['records']:
  c=claims[row['claim_id']]
  if c['source_id']==GUIDE:
   assert row['claim_snapshot']==claim_snapshot(c,old['sources'][GUIDE]);row['claim_snapshot']=claim_snapshot(c,s);count+=1
 assert l['claims']==old['claims']
 for sid in l['sources']:assert l['sources'][sid]['observations']==old['sources'][sid]['observations']
 for p,v in [('data/sources.json',bib),('data/content_review_queue.json',q),('data/literature_claim_reviews.json',l),('data/relation_literature_reviews.json',reviews)]:write(p,v)
 print(json.dumps(dict(status='recorded',new_visual_pdf_pages=13,new_full_extracted_text_pages=0,new_sources=0,new_claims=0,new_tasks=0,new_contexts=0,refreshed_context_snapshots=count)))

if __name__=='__main__':main()
