"""Extend the existing reprint review with its preceding French archive version."""
import copy
from literature_review import ROOT,load_registry,build_report,digest
from extend_lt2_length_assets_review import load,sha,write
from relation_literature_review import FILE,claim_snapshot,apply_literature_context
from record_scoped_pdf_research import inspect_html_assets
from record_lijnse_reprint_review import SOURCE,URL as REPRINT_URL

DATE='2026-11-18';CACHE=ROOT/'tmp/literature/lijnse-french-original-20261118'
PRIOR='data/literature_evidence/LIJNSE_2010_AUTHORIZED_REPRINT_review_notes.json'
PRIOR_SHA='b3ffa72aa0bc53fccc398c1a9181e6902c534bb5ffd939afb3ca5179b419d018'
PRIOR_BIB='ed2b38bd26713984dade477602f269b112adcae95ece1901a8b091d88c311721'
NOTES='data/literature_evidence/LIJNSE_1994_2010_comparison_review_notes.json'
FRENCH_URL='https://www.persee.fr/doc/didas_1250-0739_1994_num_3_1_955'
TITLE='Developmental research and didactical structure — 2010 authorized reprint, compared with the complete preceding 1994 French archive article'
SCOPE='이전2010책6장인쇄91–101(PDF93–103)전체·선정서지/서문17추출문/18판면의읽기이력을보존한다. 이번에는Persée공식아카이브의1994 Didaskalia3,93–108전체16학술지판면과각쪽의HTML본문,별도서지페이지를읽었다. HTML17문서중16개가본문쪽조각이며93/94쪽의빠진프랑스어/영어초록은실제판면에서읽었다. 새PDF나로컬OCR독해가아니다.2010장11쪽의추출문을다시읽고PDF94/98/100/102의4판면을재대조했다.1994판의편집부번역표시·물리범위와2010재수록의과학범위·선정문맥/서지차이를분리한다.1995 Science Education79(2),189–199원판의직접본문/판면은여전히미확인이다.'
LIMITS='같은연구계열의1994프랑스어판과2010약간편집한영어재수록의대조이며독립된두실증연구나새표본/국내효과가아니다.1994판은편집부번역이라고인쇄돼있어저자가프랑스어로직접쓴자필원문으로단정하지않는다.1995저자번역/수정원판의본문·원출판사바이너리동일성·1994학술지전체호/2010책전권·인용원전/원자료·정오표는미확인이다.선정대조는모든문장의번역동일성검증이아니며서지차이를원전확인없이임의로정정하지않는다.학생발언의뜻확인과수학적타당성판단은별개이며호의적해석이모든답을정답으로만들지않는다.역사적교수법비판을모든오류의교사원인·지원금지·국내효과로일반화하지않는다.실제독립/학생/브라우저시각검증은미완료다.'
COMPARISONS=[
 dict(topic='판본·번역 주체',french_pages=[93,94],reprint_pdf_pages=[93],finding='1994판은표제에물리(physique),편집부번역표시가있고프랑스어·영어초록을포함한다.2010장은과학(science)범위의제목이며첫각주가1995수정영어원판과1994선행프랑스어논문을구별한다.',limit='1995직접본문을읽은것이아니며선행프랑스어출판물의확보를모든번역/원판검증으로바꾸지않는다.'),
 dict(topic='문헌이 받아들이는 목표에 대한 표현',french_pages=[95],reprint_pdf_pages=[94],finding='1994본문은물리수업개선이라는목표가받아들여졌는지확신하지않는다는취지이고,2010선정문장은그러한목표를당연하게볼수있겠다는취지다.1994의학과소속/예산/연구존립문맥도2010해당부분과분량이다르다.',limit='두판본의표현차이를기록한다.1995원판이없으므로어느단계에서왜달라졌는지나번역오류의책임은확정하지않는다.'),
 dict(topic='연속성의 부정 표현',french_pages=[101],reprint_pdf_pages=[98],finding='양쪽모두공통지식과과학지식의양끝점을척도로설명한뒤연속적으로연결할수없다는뜻은아니라고서술한다.이중부정을빠뜨려연속연결불가능이라는주장으로옮기지않는다.',limit='그자체로모든학생에게동일한연속발달경로가검증됐다는뜻은아니다.'),
 dict(topic='교수 비판의 범위',french_pages=[101],reprint_pdf_pages=[98],finding='1994는잘못된교수라는말을절대적비난이아니라다르게가르칠방법을아직모른다는뜻으로풀어쓴다.2010해당문맥은더압축돼있다.학생구성과교사활동의상호관계를보는방법론적논의다.',limit='모든오개념의유일원인을교사로확정하거나구체적학생자료없이인과효과를주장하지않는다.'),
 dict(topic='같은 저자·연도의 다른 서지',french_pages=[100,106,107],reprint_pdf_pages=[98,102],finding='1994참고목록의Davidson1990은책Essays on actions and events(OUP)이고2010목록의Davidson1990은학술지The structure of content and truth이다.양쪽에서Grandy/Hamilton본문1993과목록1992차이도남아있다.',limit='같은저자·연도를동일문헌식별자로삼지않고두서지기록을각판본대로보존한다.이들인용원전은읽지않았으며임의로어느쪽연도/제목을정답으로고치지않는다.'),
 dict(topic='시나리오와 결과 검증',french_pages=[102,103,104,105,106],reprint_pdf_pages=[99,100,101,102],finding='양쪽은예상한과제·교사/학생행동을실제실행과대조해고치는시나리오와여러질적/양적방법을논한다.설명만으로증명하려하기보다다른이가무엇을했는지판단하고과정을재구성할수있게한다는문맥이다.',limit='예상시나리오를실제응답으로채우거나검증/재현근거를생략해도된다는허가로쓰지않는다.학습효과와수학적증명은따로검토한다.')]

def main():
 registry=load_registry();s=registry['sources'][SOURCE]
 if s['snapshot_file']==NOTES:build_report();return
 assert s['snapshot_file']==PRIOR and s['snapshot_sha256']==PRIOR_SHA and s['bibliography_snapshot']==PRIOR_BIB and sha(ROOT/PRIOR)==PRIOR_SHA
 a=load(CACHE/'acquisition.json');assert a['reading_completed'] and a['images_viewed'] and a['read_text_pages']==a['viewed_image_pages']==list(range(93,109))
 assert not a['pdf_obtained'] and not a['local_ocr_used'] and not a['original_1995_article_read']
 spec=dict(url=FRENCH_URL,asset_base_url='https://www.persee.fr/',sha256=a['html_assets'][0]['sha256'],html_assets=a['html_assets'],image_assets=a['image_assets'])
 pages,images=inspect_html_assets(spec,CACHE);assert len(pages)==17 and len(images)==16
 old_source=copy.deepcopy(s);old_notes=load(ROOT/PRIOR)
 old_claims=[copy.deepcopy(c) for c in registry['claims'] if c['source_id']==SOURCE];old_obs=copy.deepcopy(s['observations']);assert len(old_claims)==2 and len(old_obs)==4
 reviewed=load(ROOT/FILE);ids={c['id'] for c in old_claims};old_rows=[copy.deepcopy(row) for row in reviewed['records'] if row['claim_id'] in ids];assert len(old_rows)==7
 bib=load(ROOT/'data/sources.json');entry=next(x for x in bib if x['id']==SOURCE);old_entry=copy.deepcopy(entry)
 entry.update(title=TITLE,review_scope=SCOPE,does_not_establish=LIMITS,next_review='1995원학술지189–199직접판면·1994/1995/2010전체대조·선정인용원전/원자료·실제독립/학생검증을후속확인한다.')
 empirical=copy.deepcopy(s['empirical_scope']);empirical['inference_limit']=LIMITS
 comparison=dict(source_url=FRENCH_URL,version_id='LIJNSE_1994_FRENCH_PERSEE',archive='Persée',year=1994,journal='Didaskalia',issue=3,doi='10.3406/didas.1994.955',printed_pages=list(range(93,109)),translation_credit='Traduit par la rédaction',source_asset_kind='official_archive_html_and_page_images',source_asset_sha256=spec['sha256'],asset_base_url=spec['asset_base_url'],html_read_manifest=pages,image_read_manifest=images,complete_article_read=True,html_text_incomplete_pages=[93,94],missing_abstracts_read_on_images=True,pdf_obtained=False,local_ocr_used=False,original_1995_article_read=False,original_1995_binary_fidelity_verified=False,all_cited_originals_read=False,all_sentences_translation_fidelity_verified=False,reprint_text_pdf_pages_rechecked=list(range(93,104)),reprint_visual_pdf_pages_rechecked=[94,98,100,102],comparisons=COMPARISONS,independent_review=0,student_validation=0)
 notes=copy.deepcopy(old_notes);notes.update(date=DATE,read_scope=SCOPE,empirical_scope=empirical,previous_review=old_source,previous_bibliography=old_entry,previous_claims=old_claims,previous_observations=old_obs,previous_relation_records=old_rows,previous_notes_file=PRIOR,previous_notes_sha256=PRIOR_SHA,french_version_comparison=comparison)
 notes['reading_log']+=['2026-11-18:Persée서지1페이지와본문HTML16쪽조각·실제16학술지판면93–108을읽었다.93/94쪽초록은HTML에빠져판면에서읽었다.2010장11쪽추출문을재독하고4선정판면을다시대조했다.새PDF/OCR·1995원판·독립실증표본확보는아니다.']
 notes['source_corrections'] += [dict(location='1994pp93–108 versus2010chapter91–101',issue='Complete preceding French article now read,distinct from2010slightly edited English reprint and unread1995original. Preserve editor translation credit,physics/science scope and separate bibliographies;do not infer identical texts or independent replications.'),dict(location='1994p101;2010p96',issue='Both versions retain double negation:not a claim that continuous connection is impossible. This is also not a verified universal student learning trajectory.'),dict(location='1994p106;2010p100',issue='Davidson1990points to different works in the two reference lists. Keep each version rather than merge by author/year;the cited originals were not obtained. Grandy/Hamilton body1993/reference1992 discrepancy remains unresolved.')]
 write(ROOT/NOTES,notes)
 s.update(date=DATE,snapshot_file=NOTES,snapshot_sha256=sha(ROOT/NOTES),snapshot_history=s.get('snapshot_history',[])+[dict(snapshot_file=PRIOR,snapshot_sha256=PRIOR_SHA,date=old_source['date'],read_scope=old_source['read_scope'])],bibliography_snapshot=digest(entry),read_scope=SCOPE,limits=LIMITS,empirical_scope=empirical,method_note='2010재수록PDF의기존17추출문/18판면기록을유지하고1994공식아카이브의본문HTML16쪽조각·판면16개와별도서지를대조했다.초록누락은실제이미지로보완했으며새PDF/OCR독해로세지않는다.',editorial_action='동일문헌계열의선행프랑스어판읽기와선정대조를추가했다.기존2주장범위·1출처과제설명과7관계근거스냅샷을재검토하며새주장·과제·관계해석·독립표본은추가하지않았다.',display={**s['display'],'title':TITLE})
 for obs in s['observations']:
  if obs['id']=='LJ10-P04':
   obs.update(question='1994프랑스어판93–108과2010재수록91–101을모두읽었다.1995학술지189–199의원판도확인됐는가? 같은저자·연도의서지를합쳐도되는가?',expected='아니다.1994는편집부번역표시가있는프랑스어논문,1995는미확보학술지수정영어판,2009-10-09는심포지엄,2010은약간편집한재수록책의연도다.이번에는1994아카이브HTML본문16쪽조각/실제16판면과별도서지를읽었고,2010의6장인쇄91–101(PDF93–103)전체독해는유지한다.1994와2010의Davidson1990참고목록은각각책과학술지논문을가리킨다.저자·연도만으로합치지않고판본·제목·문헌종류를나누며1995원판·인용원전은미확인으로남긴다.',interpretation='동일연구계열의선행판과편집재수록을구별하는자체출처과제다.서지·선정문맥차이가있으며번역의모든문장동일성·1995원판·학술지전체호/2010책전권·새독립연구나실제학생검증을확인한것은아니다.')
 by_page={int(p['key'][5:]):p['url'] for p in pages if p['key'].startswith('page-')}
 for c in registry['claims']:
  if c['source_id']!=SOURCE:continue
  c['empirical_scope']=copy.deepcopy(empirical)
  pp=[96,98,99,102,103,104,105,106] if c['id']=='LJ10-01' else [99,100,101,103,104]
  c['locations'] += [by_page[p] for p in pp]
  c['does_not_establish'] += ' 1994프랑스어선행판전체와2010편집재수록을대조했지만1995원학술지의직접본문/판면과모든번역문장동일성은미확인이다.같은문헌계열을두독립실증연구로세거나같은저자·연도만으로서지를합치지않는다.'
 by_claim={c['id']:c for c in registry['claims']}
 for row in reviewed['records']:
  if row['claim_id'] in ids:row['claim_snapshot']=claim_snapshot(by_claim[row['claim_id']],s)
 relations=load(ROOT/'data/revised_relations.json')['relations'];apply_literature_context(relations,registry,registry=reviewed)
 queue=load(ROOT/'data/content_review_queue.json');next(row for row in queue['literature_review'] if row['source']['id']==SOURCE)['source']=entry
 write(ROOT/'data/sources.json',bib);write(ROOT/'data/literature_claim_reviews.json',registry);write(ROOT/'data/content_review_queue.json',queue);write(ROOT/FILE,reviewed);build_report()
 print('Same Lijnse family extended:complete1994French16HTMLbodyfragments/16images plusrecord;2claim scopes/1task explanation/7snapshots rereviewed;no new sources,claims,tasks,contexts or empirical samples')

if __name__=='__main__':main()
