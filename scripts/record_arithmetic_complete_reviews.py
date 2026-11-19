"""One bounded arithmetic review migration, preserving earlier authored notes."""
import copy,hashlib,json
from literature_review import ROOT,load_registry,digest
from relation_literature_review import claim_snapshot
from check_arithmetic_trial_measurement_models import check

SPECS=[('pilot','CLEMENTS_ET_AL_2020_ARITHMETIC_PILOT',12,9),('trial','CLEMENTS_ET_AL_2021_ARITHMETIC_TRIAL',46,41)]
NOTES=[f'data/literature_evidence/{sid}_complete_visual_review_notes.json' for _,sid,_,_ in SPECS]
LIMITS=[
 '조건별 한 학급인 영재 유치원 두 학급의 단기 개별 지도 예비 연구다. 학급과 조건이 분리되지 않고 순서·수 범위·문제 구조·반응별 조정도 함께 달랐다. 수업 중 수행·예상 수준과 독립 사후검사·수준 내 개선을 구별한다. 단계 순서가 모든 학생의 필요조건이거나 국내 과제의 효과라고 입증하지 않았다.',
 '4개 학교16개 교실의 편의표본을 사전검사 뒤 개인별 배정한 두 활성 개별 지도 조건 비교다. 순서·기초 세기 지원·이전 수준 비계·LT전용 중간검사 노출이 결합돼 순서만의 독립 효과가 아니다. 분량과 회기수는 동일하지 않았고 국내 집단 수업·장기 유지·검증된 정서 효과·모든 학생의 필수 순서를 입증하지 않았다.'
]
def read(p):return json.loads((ROOT/p).read_bytes())
def sha(p):return hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
def write(p,d):(ROOT/p).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def main():
 l=load_registry();old=copy.deepcopy(l);bib=read('data/sources.json');q=read('data/content_review_queue.json');model=check()
 assert len(l['sources'])==176 and len(l['claims'])==1055 and not any((ROOT/p).exists() for p in NOTES)
 for i,(label,sid,total,new) in enumerate(SPECS):
  s=l['sources'][sid];prior=read(s['snapshot_file']);progress=read(f'tmp/literature/arithmetic-complete-20261119/{label}/reading-progress.json')
  assert progress['reading_completed'] and progress['actually_viewed_pdf_pages_this_turn']==list(range(1,total+1)) and len(progress['new_visual_pdf_pages'])==new
  assert progress['source_pdf_sha256']==s['source_pdf_sha256']==sha(f'tmp/literature/arithmetic-complete-20261119/{label}/source.pdf')
  for n,h in progress['rendered_page_sha256'].items():assert sha(f'tmp/literature/arithmetic-complete-20261119/{label}/rendered/page-{int(n):02d}.png')==h
  scope=(f'확보된 PDF{total}판면의 본문·표·그림·참고문헌 전체를 실제 판면으로 읽었다. 기존{total-new}판면과 새{new}판면을 합친 범위이며 이번 새 전문 추출문 독해는0쪽이다. ')
  scope+=('공식 출판사 별도 부록8판면(A–D)도 모두 읽었다. 본문12쪽과 부록8쪽은 별도 파일이다. ERIC38쪽 저자본의 이전 선정 대조는 보존하며 그 파일 전체 독해를 뜻하지 않는다.' if i==0 else 'ERIC46쪽 저자 원고이며 출판사15쪽 판면과 바이너리 동일성·별도S부록은 미확인이다.')
  empirical=copy.deepcopy(s['empirical_scope']);empirical['inference_limit']=LIMITS[i]
  if i==1:empirical['sample_description']='4개 학교16개 교실에서 동의319명 중28명을 제외·탈락해 순차143명·목표148명,291명을 분석했다. 연구 중 이사6명을 포함하므로28명 모두를 배정 전 제외라고 하지 않는다.'
  s['snapshot_history']=copy.deepcopy(s.get('snapshot_history',[]))+[dict(snapshot_file=s['snapshot_file'],snapshot_sha256=s['snapshot_sha256'],date=s['date'],read_scope=s['read_scope'])]
  s.update(date='2026-11-19',read_scope=scope,visual_pdf_pages=list(range(1,total+1)),empirical_scope=empirical,limits=LIMITS[i],
    scope_note='확보 본문 전체 판면에서 배정·지도 조건 묶음·평가 규칙·집계 분모와 추정량을 구별했다. 더 유용한 지도 경로를 모든 학생의 필수 순서로 바꾸지 않는다. 원 반응·공식 정오표·국내 검증은 미확인이다.',
    method_note='본문 전체의 실제 판면과 공식 확보 부록을 읽고 표시된 집계·판정 조건·반올림 가정을 검산했다. 원 학생 반응·Rasch/Bayesian 모형을 재추정하지 않았다.',
    editorial_action='2026-11-19: 덧셈·뺄셈 연구 본문 전체 대조와 예비 연구 공식 부록 대조로 기존 주장8건을 보완했다. 새 출처·주장·과제·관계는0이다.')
  n=copy.deepcopy(prior);n.update(date=s['date'],read_scope=scope,empirical_scope=empirical,previous_review=old['sources'][sid],previous_snapshot_file=s['snapshot_file'],previous_snapshot_sha256=s['snapshot_sha256'],
    visual_pdf_pages=list(range(1,total+1)),rendered_page_sha256=progress['rendered_page_sha256'],previous_rendered_page_sha256=prior['rendered_page_sha256'],new_visual_pdf_pages=progress['new_visual_pdf_pages'],new_text_pdf_pages=[],new_full_extracted_text_pages=0,whole_article_visual_read=True,
    exact_own_checks=model,publisher_binary_fidelity_verified=False,raw_student_data_read=False,all_cited_originals_read=False,official_erratum_verified=False,independent_review=False,student_validated=False)
  n['reading_log']=prior['reading_log']+[scope]
  if i==0:
   a=read('tmp/literature/arithmetic-complete-20261119/pilot/official-supplement-acquisition.json');p=read('tmp/literature/arithmetic-complete-20261119/pilot/supplement-reading-progress.json')
   assert a['obtained'] and a['status']==200 and a['pdf_pages']==8 and sha('tmp/literature/arithmetic-complete-20261119/pilot/official-supplement.pdf')==a['sha256']
   assert p['reading_completed'] and p['actually_viewed_pdf_pages_this_turn']==list(range(1,9))
   for page,h in p['rendered_page_sha256'].items():assert sha(f'tmp/literature/arithmetic-complete-20261119/pilot/supplement-rendered/page-{int(page):02d}.png')==h
   n['official_supplement_review']=dict(url=a['url'],publisher_linking_page=a['discovered_on'],status=200,content_type=a['content_type'],sha256=a['sha256'],bytes=a['bytes'],pdf_pages=8,visual_pdf_pages=list(range(1,9)),rendered_page_sha256=p['rendered_page_sha256'],new_visual_pages=8,new_full_extracted_text_pages=0,reading_log=p['reading_log'],source_pdf_redistributed=False)
   n['audit_findings']=[
    dict(pdf_pages=[2,3,4,5,10],finding='8개 사고 수준은 수 크기·문제 구조·전략을 함께 포함한다. 저자는 순서의 정확한 준수가 학습의 필요조건이라고 결론하지 않는다. 형성평가와 다음 수준 지도·반응별 난도 조정을 포함한 교수 묶음이다.'),
    dict(pdf_pages=[6,7,9],finding='학급1을무작위로조건에배정했으나조건마다학급은하나다. LT아동01은지도자의실수로수준4를건너뛴사례가있다. 본문교수계획의21–100과공식부록B의20–100표기를유지하며계획과실제지도수행을동일시하지않는다.'),
    dict(pdf_pages=[7,8],finding='독립수준판정은해당수준및모든이전수준에서거의모든문항정답을요구한다. 수준별3문항이상의전체또는하나를제외한정답기준,수업중3연속과제기준,수준내최소20%개선은서로다르다. 본실험75%와도동일기준이아니다.'),
    dict(pdf_pages=[7,8,9],supplement_pdf_pages=[5,6],finding='표1의Age(months)와5.4/5.5단위문제는미해결이다. 표2와부록C의LT13명은한수준증가4/두수준증가2/유지7인데본문645는증가하지않은LT아동을6명으로쓴다. 원문표기와자체집계를보존하며공식정정값을확정하지않는다.'),
    dict(pdf_pages=[8,9,10],supplement_pdf_pages=[5,6,7,8],finding='고급전략을시도하다실행오류로정답률이내려간사례는개념후퇴와구별한다. 부록C의수업기반예상수준은독립사후결과가아니다. 부록D의8명/5명은수업중상승폭에따른사후분류이지무작위조건·유지율이아니다. 단계번호간격을등간척도로증명하지않는다.'),
    dict(pdf_pages=[11,12],finding='연구비·저자의출판관련이해관계·독립기관감독과참고문헌을읽었다. 논문자체의감독을이프로젝트의외부독립검토실적으로세지않는다.')]
  else:
   n['audit_findings']=[
    dict(pdf_pages=[1,3,13,14,36,38,46],finding='ERIC원고표지의2021학술지서지와PDF메타데이터의Word5.5.22파일명·미정리인용필드를함께기록한다. 출판사15쪽판면동일성은미확인이다. 동의319/탈락28/분석291과학교전체학생수를구별한다. 연구중이사6명도포함돼탈락전부를배정전이라고하지않는다.'),
    dict(pdf_pages=[4,5,11,14,15,16,18,19,35],finding='수준은확률적사고패턴이며유일경로가아니다. 초기75%는해당수준과모든이전수준의공동조건이다. 양조건모두격려·피드백·조작물·시범을허용하나LT만이전수준비계와세기지원을제공한다. 사전21/사후13추가,병렬분석2요인후선택한사후1요인Rasch를모든국내진단과제의검증으로바꾸지않는다.'),
    dict(pdf_pages=[14,20,21,31],finding='계획15회180+분/초기20회240분과실측LT206분13.4회/skip212분14.3회를구별한다.0.9회차이의인쇄95%CI끝점1.43/0.37순서를유지한다. 분량비유의는동일연습기회나최적수업량의입증이아니다.'),
    dict(pdf_pages=[22,23,24,25,26,27],finding='기본모형d1.20,임의절편포함표4의.53,임의절편제외최종모형과그림2의9모형점은서로다르다. 표3의478.1−469.6은8.5이나본문은8.74(SE8.24)다. 가까운소수첫째자리반올림만으로일치하지않는다는검산이며모형재추정·공식정정은아니다.3원상호작용하한.04/.03을보존한다. 사전·사후표준화점수차를동일원점수성장·퇴행으로읽지않는다.'),
    dict(pdf_pages=[27,28,31],finding='±1SD의9모형점은9개실제무작위집단이아니다. 전체문항정확성46.18/30.27%와기초사전집단93/114명의목표문제정답46/30명(49.5/26.3%)은별도분모다. 집단평균·일부목표문항비교를개별아동의전체숙달이나모든문항별유의성으로바꾸지않는다.'),
    dict(pdf_pages=[30,31,32,33,35],finding='LT만사후와같은문항의중간검사를시작/중단규칙과함께경험했다. 미시행은실제오답이아니다. 질적좌절노트·세기시간배분기전은독립검증된정서인과효과가아니다. 편의표집·개별지도·가족정보제한·적응훈련·후속노출통제연구의한계를보존한다.')]
   n['unobtained_supplement_followup']=read('tmp/literature/arithmetic-complete-20261119/trial/official-supplement-followup.json')
  n['source_corrections']+= [dict(location='전체판면후속대조2026-11-19',issue=x['finding'],status='bounded_own_audit_not_official_erratum') for x in n['audit_findings']]
  write(NOTES[i],n);s.update(snapshot_file=NOTES[i],snapshot_sha256=sha(NOTES[i]))
  b=next(v for v in bib if v['id']==sid);b.update(review_scope=scope,does_not_establish=LIMITS[i],next_review='원반응·공식정오표·인용원연구·출판사본문파일동일성과국내학생검증은미완료다. 본실험별도S부록·예비연구ERIC38쪽저자본전체를이번독해로대체하지않는다.');s['bibliography_snapshot']=digest(b)
  next(v for v in q['literature_review'] if v['source']['id']==sid)['source']=copy.deepcopy(b)
  for c in l['claims']:
   if c['source_id']==sid:c['empirical_scope']=copy.deepcopy(empirical)
 cs={c['id']:c for c in l['claims']}
 updates={
 'LTAP-01':('표2와공식부록C의LT13명중6명은한수준이상증가했고7명은유지했다. skip12명중1명은부분증가했다. 수업중예상수준과독립사후수준을별도로기록했다.','서로다른변화범주와조건별한학급의비교다. 본문645의비증가6명과표/부록의7명은불일치가남는다. 부록D의수업중상승8명/5명을무작위집단이나유지율로읽지않으며순서의필요조건·국내과제효과로확대하지않는다.'),
 'LTAP-02':('세기24문항과연산45문항을사용했다. 독립수준은해당수준과모든이전수준의수행으로판정했고,수업중3연속과제·수준내최소20%개선·독립사후수준이동을구별했다.','수준별3문항이상에서전체또는하나를제외한정답이라는예비연구규칙은본실험75%규칙과다르다. 도움받은수행과독립수행을합치지않으며고급전략의실행오류나수준내개선을개념퇴행·다음수준숙달로단정하지않는다.'),
 'LTAP-03':('건너뛰기조건은처음에높은수범위의시작/부분미지문제로시작했으나후반에는동일하거나낮은수준·일부n+1지도를허용했다. 문제구조와수범위가함께달랐고공식부록B는실제지도와별도의계획을기록한다.','수크기·미지수위치·비계·순서의독립효과를분리하지않았다. 본문21–100과부록20–100의표기를유지한다. LT조건에서도수준4를실수로생략한사례가있으며저자는순서의정확한준수를학습의필요조건으로결론하지않는다.'),
 'LTAR-01':('사전검사뒤학생을난수로두개별지도조건에배정했고LT143명·목표148명을분석했다. 목표조건은초기사고수준보다세수준위의문제를다뤘으며두조건모두격려·피드백·조작물·시범을받았다.','무처치·정규집단수업대비효과나장기유지를검증하지않았다. 동의319명에서제외·탈락28명에는연구중이사6명도포함된다. LT의기초세기지원·이전수준비계·추가중간검사가결합돼순서만의독립효과가아니다.'),
 'LTAR-02':('기본모형의전체조건차이d=1.20과임의절편포함표4의조건계수0.53(95%신용구간0.37–0.68)을구별한다. 최종선택모형은교실·지도팀임의절편을제외했다.','최종모형·표4·그림2는동일추정량이아니다. 표3의표시WAIC차8.5와본문8.74,3원상호작용하한표.04/본문.03을보존한다. 동일하지않은효과를모든학생·두자리계산·모든문제유형의효과크기로적용하지않고모형재추정을했다고하지않는다.'),
 'LTAR-03':('그림2의사전연산·세기낮음모형점은0.96,연산높음·세기낮음점은0.05로후자의신용구간은0을포함했다. 이는평균및±1표준편차의아홉모형평가점이다.','아홉점을실제무작위하위집단이나개인별단계판정경계로읽지않는다. 분량의비유의는효과동등성·동일연습량을입증하지않는다. 실측LT206분13.4회/목표212분14.3회와계획수업량은별도이며가족특성별효과·국내집단수업효과는미확인이다.'),
 'LTAR-04':('그림1은합침·덜어냄·부분전체·비교에서미지수역할을구별한다. 모두세기와기준수를유지하고추가횟수를추적하는이어세기를나누며초기수준75%는해당수준및모든이전수준의공동조건이다.','의미역할을빈칸위치만으로대체하거나이어세기를유일한필수경로로삼지않는다.75%는연구의초기수준배정규칙으로국내과제의보편적숙달기준이아니다. 저자는수준을확률적패턴으로설명하고정확한순서준수가필요조건이아님을명시한다.'),
 'LTAR-05':('연산사전21문항에13문항을추가해사후검사를구성했다. LT만사후와같은문항의중간검사를시작·중단규칙과함께추가로경험했다. 목표문제의기초사전집단93/114명중46/30명정답은별도비교다.','동일검사의원점수증가나순서만의효과로해석하지않는다. 중단후미시행은실제오답이아니며표준화점수감소가개념퇴행을뜻하지않는다. 전체46.18/30.27%를전체아동숙달률로바꾸거나일부목표문항결과를모든개별문항의유의성으로확대하지않는다.')}
 for cid,(support,limit) in updates.items():cs[cid].update(support=support,does_not_establish=limit)
 for cid in ['LTAP-01','LTAP-02','LTAP-03']:cs[cid]['locations'].append(l['sources'][SPECS[0][1]]['display']['url'])
 reviews=read('data/relation_literature_reviews.json');oldcs={c['id']:c for c in old['claims']};refreshed=0
 for row in reviews['records']:
  cid=row['claim_id']
  if cid in updates:
   sid=cs[cid]['source_id'];assert row['claim_snapshot']==claim_snapshot(oldcs[cid],old['sources'][sid]);row['claim_snapshot']=claim_snapshot(cs[cid],l['sources'][sid]);refreshed+=1
 assert all(l['sources'][sid]['observations']==old['sources'][sid]['observations'] for sid in l['sources'])
 for p,d in [('data/sources.json',bib),('data/content_review_queue.json',q),('data/literature_claim_reviews.json',l),('data/relation_literature_reviews.json',reviews)]:write(p,d)
 print(json.dumps(dict(status='recorded',main_visual_pages=58,official_supplement_visual_pages=8,total_visual_pages=66,new_visual_pages=58,new_full_extracted_text_pages=0,changed_claims=8,new_claims=0,new_tasks=0,refreshed_context_snapshots=refreshed)))

if __name__=='__main__':main()
