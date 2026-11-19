"""Record bounded file equivalence and a related article's unresolved reporting conflicts."""
import copy,hashlib,json
from literature_review import ROOT,digest
from relation_literature_review import claim_snapshot
from check_sood_publication_consistency import check

GAISE='GAISE_2020';EARLY='IES_EARLY_2013'
GN='data/literature_evidence/GAISE_2020_official_rendering_comparison_notes.json'
SN='data/literature_evidence/SOOD_MACKEY_2015_related_publication_audit.json'
EN='data/literature_evidence/IES_EARLY_2013_related_publication_followup_notes.json'

def read(p):return json.loads((ROOT/p).read_bytes())
def write(p,v):(ROOT/p).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256((ROOT/p).read_bytes()).hexdigest()

def main():
 l=read('data/literature_claim_reviews.json');old=copy.deepcopy(l)
 assert len(l['sources'])==176 and len(l['claims'])==1055
 assert not (ROOT/GN).exists() and not (ROOT/SN).exists() and not (ROOT/EN).exists()
 g=read('tmp/literature/gaise-fidelity-20261118/comparison.json')
 a=read('tmp/literature/sood-published-20261118/acquisition.json')
 assert g['status']=='pass' and g['sequential_pdf_and_image_verification'] and g['pages_compared']==126 and not g['differing_pdf_pages']
 assert a['reading_completed'] and a['visual_pdf_pages']==list(range(1,19)) and a['text_pdf_pages']==[1]
 article=a['assets'][0];assert sha(article['file'])==article['sha256']
 audit=dict(parent_source_id=EARLY,source_id=EARLY,related_publication=dict(title='Examining the Effects of Number Sense Instruction on Mathematics Competence of Kindergarten Students',authors=['Sheetal Sood','Megan Mackey'],year=2015,journal='International Journal of Humanities Social Sciences and Education',volume=2,issue=2,printed_pages=[14,31],url=article['url'],pdf_sha256=article['sha256'],pdf_pages=18),date='2026-11-18',reviewer='Codex',contains_source_full_text=False,source_pdf_redistributed=False,registered_as_additional_effect_source=False,original_sood_2009_dissertation_obtained=False,same_or_independent_sample_verified=False,visual_pdf_pages=a['visual_pdf_pages'],text_pdf_pages=[1],rendered_page_sha256=a['rendered_page_sha256'],tables_read=[1,2],data_figures=0,author_photos_on_pdf_page=18,reading_log=a['reading_log'],independent_review=False,student_validated=False,official_erratum_verified=False,exact_own_arithmetic_checks=check())
 audit['findings']=[
  dict(pdf_pages=[1,3,8],issue='표본 분모의 불일치',detail='초록·방법의77+58=135,표1의총계77+40=117,방법의성별합77+27+21=125,기초검정의N=101과df99가양립하지않는다. 표1의GCI성별31+27과민족25+33은58이다.',action='61/40이나77/58중하나를실제분석표본으로선택하지않는다. 반올림연령평균·SD로61/40가정의t≈2.682와77/58가정의t≈3.150을계산했지만이는후보모형대조일뿐실제표본복원이아니다.'),
  dict(pdf_pages=[3,12],issue='교사 수의 불일치',detail='방법은중재5교사·비교4교사라고하지만실행논의는중재3교사중2명이계산기를사용하지않았다고쓴다.',action='3교사와5교사를통합하거나오탈자로정정하지않는다.'),
  dict(pdf_pages=[4,5,6,12],issue='수업량과다요소처치',detail='양집단모두하루60분·주5일,공통교육과정40분이다. 나머지20분에수감각묶음과정규과정내용을달리한다. 단원별5+5+4+4=18차시이며자료·집단형태·내용이함께달라진다.',action='중재집단에만20분을추가한설계나개별교구·계산기의고유효과로읽지않는다. 기기별상수연산동작을보장하지않는다.'),
  dict(pdf_pages=[6,7,8],issue='척도와전이범위',detail='SESAT는기초검사이며직후·3주유지에는ENCBM과수감각척도를사용한다. 비언어계산8문항은처음수세기와답에각1점으로최대16점이다. 공간배열유지내적일관성은.55,비언어계산유지는.66이다.',action='8문항정오율이나일반수학성취전이로바꾸지않는다. 검사지표별분모·부분점수·시점·신뢰도를구별한다.'),
  dict(pdf_pages=[8,9,10,11],issue='결과와논의의범위충돌',detail='ENCBM집단주효과는모두유의하지않고논의도Bonferroni후직후차이가유의하지않다고한다. 그러나다른논의는두검사모두우세하다고넓게쓴다. 유지의수식별에서는비교집단이우세하다고설명한다. 결과별평균·SD표는실려있지않다.',action='모든직후·유지효과가긍정적이라고요약하거나누락평균·효과크기를추정하지않는다. 정확한대조·표본이불명확하여추가효과주장과자체과제를등록하지않는다.'),
  dict(pdf_pages=[9,10,13],issue='유지와분석단위',detail='직후와유지간비유의차이를유지라고설명한다. 학급배정인데학생단위반복측정분석을사용하고다층모형은향후제안이다.',action='비유의차이를동등성·개별학생유지증명으로바꾸지않는다. 실제수행하지않은다층모형분석이나군집보정완료로기술하지않는다.'),
  dict(pdf_pages=[13,14,15,16,17,18],issue='원학위논문과의관계미확인',detail='논의·결론·참고문헌·저자약력을모두읽었지만2015논문과가이드가인용한2009학위논문이같은자료인지확인하지못했다.',action='2015논문읽기를2009학위논문독해완료나독립재현1건으로세지않는다. 가이드의비언어계산직후.37ns·유지.12ns와미주의유지서술차이는보류한다.')]
 audit['not_established']=['정확한배정·분석표본','2009학위논문의실제본문·표본·분석','원자료·공식정오표','WWC의정확한재분석','국내과제효과','독립검토·실제학생검증']
 write(SN,audit)
 s=l['sources'][GAISE];n=read(s['snapshot_file'])
 s.setdefault('snapshot_history',[]).append({k:copy.deepcopy(s[k]) for k in ['snapshot_file','snapshot_sha256','date','read_scope']})
 s['read_scope']='기존126쪽전체추출문·전체판면독해를유지한다. 현행공식PDF와기존확보본126쪽을같은렌더러·1900px조건의PNG/RGB및추출문·내용스트림·페이지상자로대조했다. 이번새독해쪽수는0이다.'
 s['limits']='두PDF는바이트해시가다르다. 명시한렌더링조건과페이지내용대조는126쪽일치했으나모든해상도·벡터·주석·링크·접근성의동일성은미검증이다. 인용원연구·원자료·More4U·원도구·공식정오표는미확인이다. 원문의불일치는보존하고PDF·페이지이미지는재배포하지않는다.'
 s['editorial_action']+=' 2026-11-18: 공식PDF와126쪽의지정조건판면·내용동등성을확인했다. 바이너리동일성이나새126쪽독해로세지않는다.'
 s['reading_log'].append(s['editorial_action'].split(' 2026-11-18:')[-1])
 n['previous_batch_new_pages']={k:copy.deepcopy(n.get(k)) for k in ['new_read_pdf_pages','new_visually_reviewed_pages']}
 n['previous_interpretation_limits']=copy.deepcopy(n['interpretation_limits']);n['unread_followups']=[s['limits']]
 n['interpretation_limits']=[s['limits'] if '현재ASA 다른주소의PDF' in text else text for text in n['interpretation_limits']]
 n.update(date='2026-11-18',read_scope=s['read_scope'],previous_notes_file=old['sources'][GAISE]['snapshot_file'],previous_notes_sha256=old['sources'][GAISE]['snapshot_sha256'],previous_review=copy.deepcopy(old['sources'][GAISE]),official_asset_comparison=g,publisher_binary_fidelity_verified=False,official_rendering_equivalence_verified=True,new_read_pdf_pages=[],new_visually_reviewed_pages=[],new_text_pdf_pages=[],new_visual_pdf_pages=[],reading_log=copy.deepcopy(s['reading_log']))
 s['snapshot_file']=GN;write(GN,n);s['snapshot_sha256']=sha(GN)
 s=l['sources'][EARLY];n=read(s['reading_extension']['file']);previous=copy.deepcopy(s['reading_extension'])
 s['read_scope']='가이드165쪽·별도심사프로토콜2.1의9쪽에대한기존전체추출문/판면대조와Lai2008웹전사문범위를유지한다. 관련Sood·Mackey2015논문18판면·추출문1쪽을추가읽었으나2009원학위논문대체본·독립효과근거로등록하지않는다. 새가이드독해는0쪽이다.'
 s['scope_note']+=' 관련2015논문의표본·교사수·결과서술불일치를별도감사했다. 원2009학위논문과동일표본인지독립표본인지미확인이며추가긍정효과로세지않는다.'
 s['editorial_action']+=' 2026-11-18: Sood·Mackey2015관련논문의전18판면을감사하고불일치때문에효과근거추가를보류했다.2009학위논문미확보상태는유지한다.'
 ref=dict(file=SN,sha256=sha(SN),original_thesis_read=False,new_effect_claims=0)
 s['related_published_article_audits']=[ref]
 n.update(previous_review=copy.deepcopy(old['sources'][EARLY]),previous_reading_extension=previous,cumulative_read_scope=s['read_scope'],new_text_pdf_pages=[],new_visual_pdf_pages=[],new_image_sha256={},new_image_records=[],related_published_article_audits=[ref])
 n['reading_log'].append('관련2015논문18판면과추출문1쪽을읽고별도감사했다.가이드·원2009학위논문의새쪽수는0이다.표본·교사수·결과서술의충돌을보존하고신규효과주장·과제를추가하지않았다.')
 write(EN,n);s['reading_extension']=dict(file=EN,sha256=sha(EN))
 bib=read('data/sources.json');q=read('data/content_review_queue.json')
 for sid in [GAISE,EARLY]:
  entry=next(e for e in bib if e['id']==sid);entry['review_scope']=l['sources'][sid]['read_scope'];l['sources'][sid]['bibliography_snapshot']=digest(entry)
  next(e for e in q['literature_review'] if e['source']['id']==sid)['source']=copy.deepcopy(entry)
 reviews=read('data/relation_literature_reviews.json');claims={c['id']:c for c in l['claims']};count=0
 for row in reviews['records']:
  c=claims[row['claim_id']];sid=c['source_id']
  if sid in [GAISE,EARLY]:
   assert row['claim_snapshot']==claim_snapshot(c,old['sources'][sid])
   row['claim_snapshot']=claim_snapshot(c,l['sources'][sid]);count+=1
 assert l['claims']==old['claims']
 for sid in l['sources']:assert l['sources'][sid]['observations']==old['sources'][sid]['observations']
 for p,v in [('data/sources.json',bib),('data/content_review_queue.json',q),('data/literature_claim_reviews.json',l),('data/relation_literature_reviews.json',reviews)]:write(p,v)
 print(json.dumps(dict(status='recorded',changed_sources=2,new_claims=0,new_tasks=0,new_contexts=0,refreshed_context_snapshots=count,new_visual_pages_read=18,new_extracted_text_pages_read=1,gaise_comparison_pages=126)))

if __name__=='__main__':main()
