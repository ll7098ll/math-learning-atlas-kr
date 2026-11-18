"""Bind actually reviewed linked worksheets separately from the LT2 HTML source."""
import copy,hashlib,json
from collections import defaultdict
from literature_review import ROOT,digest,target_value,load_registry,build_report
from relation_analysis_review import load_reviews
from record_lt2_public_review import SOURCE,URL
from extend_lt2_area_volume_activities_review import NOTES as PRIOR_NOTES

NOTES='data/literature_evidence/CLEMENTS_SARAMA_LT_measurement_pdf_review_notes.json'
PRIOR_SHA='b8085a011ea514eae8a3ebc3ebc2e728041342cc79bbbb26d18cf916a1671b20'
SCOPE='공식 공개HTML 누적344개 지정 영어 본문(일반6·개요20·수준224·활동93·교사자료1)과110개 삽입 이미지URL의 이전 읽기를 보존했다. 넓이/부피48페이지에서 실제 연결된 LT2 수학PDF16개URL의19쪽 내용을 모두 이미지로 확인했다. 동일SHA의3쌍을 제외하면13개 파일·16쪽이다. 대부분 도형/격자 중심 자료로 추출문자만 읽은 것이 아니며,주HTML의 PDF판/전체사이트 읽기로 바꾸지 않는다. 기록된824개 활동/교사자료 중94개 공개 영어페이지 본문 읽기·730개 대기는 그대로다. 모든 첨부/영상/게임/교재/원연구·번역·실제 독립/학생 검증 완료가 아니다.'
PDF_NOTES={
 '1583353156064':['PDF1: Floor Tiles의 빈 직사각형이다. 격자/수치/물리 단위가 없으며 이 파일 하나로48개나12개를 세지 않는다.'],
 '1583353226406':['PDF1: 작은 격자는6열8행48칸이다. 선의 미세한 간격 차이와 실제 출력 치수는 별도로 확인하고 PDF에cm/in 숫자가 표시된 것으로 쓰지 않는다.'],
 '1583353243997':['PDF1: 큰 격자는3열4행12칸이다. 앞48칸 자료와 같은 외곽/같은 배율로 사용할 때 단위 변 약2배·단위 넓이4배라는 본문 의도에 대응한다. 서로 다른 출력 배율에서 정확한 덮기를 보장하지 않는다.'],
 '1584734829908':['PDF1: 벽 부분은5열4행20칸이며 지붕/굴뚝은 벽의20단위에 포함하지 않는다.','PDF2: 같은 벽의 왼쪽4칸·아래5칸이 부분 격자로 주어져 모서리1칸을 공유한다. 드러난 작은 칸8개와 큰 빈 부분1개를9단위로 세지 않고 동일 단위를 이어 전체20을 구성한다.','PDF3: 벽은 빈 직사각형이다. 전체 격자/부분 격자/빈 벽은 같은 링크의 세 쪽으로서 다른 단계 과제에서 어떤 쪽과 도움을 썼는지 기록한다. 세 쪽을 독립 연구/학생으로 세지 않는다.'],
 '1589393198115':['PDF1: 중앙3열6행과 양쪽 각1열2행으로 단위 격자22칸이다.3×2×1상자의 표면22단위²와 내부6단위³를 구별하는 조건부 대조에 쓸 수 있지만,별도 접는 선·여섯 면의 구획·단위 이름/실제 조립 성공을 이 그림에서 읽지 않는다. 덮개/절단/붙임 조건과 원문 조립 전후의 예상 시점은 별도 확인한다.'],
 '1606931162619':['PDF1: 파란 두 직사각형과 녹색 정사각형 단위가 있다. 같은 배율의 단위로4×3과6×2 배열을 구성하는 같은12단위 넓이 비교다. 숫자/물리 단위가 직접 표시된 것은 아니며 원문이 제시한 같은 넓이 조건과 도형을 함께 확인한다.'],
 '1608070312536':['PDF1: 앞 Estimating Area와 같은 두 파란 직사각형/녹색 단위 구성을 쓴다. 이 파일에는 LT2표지와 각색 출처가 더 있어 파일SHA는 다르다. 겉모양/인용문 추가를 새 독립 실증 근거로 세지 않고 두 정원의 넓이 동률을 허용한다.'],
 '1608572065121':['PDF1: 호박 사진16개가4행4열로 배치되어 있다. 사진 밖의 흰 여백·호박의 불규칙 외곽과 재는 정사각형 단위는 다르며 잘라 쓸 경계/단위 크기를 확인해야 한다.','PDF2: 바구니 그림은4열3행12칸이다. 사진16개가 인쇄됐다는 수량과 이 바구니의12단위를 구별한다. 두 쪽의 단위가 같은 크기로 잘려 맞는지 출력 후 확인하기 전에는 사진12장이 정확히 덮인다고 확정하지 않는다. 실제 호박의3차원 부피/바구니 들이를 측정한 자료가 아니다.'],
 '1608590819262':['PDF1: 퀼트 격자는7열4행28칸이고 새 그림은 번갈아14칸에 있다. 빈14칸도 전체 넓이에 포함한다. 아래 별도 정사각형은 덮기 단위이며 새의 검은 외곽 넓이를 재는 과제가 아니다. 출력 후 단위 변과 격자 변의 일치·여백을 확인한다.'],
 '1620402696194':['PDF1: 네 개의 빈 직사각형이며 격자·치수·단위·정답표는 없다. 픽셀 수를cm²로 바꾸거나 침대 장식 그림의 면적과 같게 쓰지 않는다. 같은 단위 덮기/허용한 자르기·포개기로 실제 비교한다.'],
 '1622048101479':['PDF1:8열10행80칸의 일반 격자종이다. 완성된 특정 상자의 전개도/부피80을 제시한 것이 아니며 자르는 경계·접는 위치·단위 치수는 교사가 정한다.'],
 '1622048118054':['PDF1: 정사각형 여섯 면이 가로4개,둘째 면 위아래 각1개인 정육면체 전개도다. 숫자 치수/단위 격자/붙임 여분은 없다.6면을6개 내부 단위블록으로 바꾸지 않으며 출력 배율과 실제 블록 크기를 맞춘다.'],
 '1622048132504':['PDF1: 서로 대응하는 직사각형 면6개의 전개도다. 숫자 치수/단위 격자/붙임 여분이 없어 활동 본문의 예시 부피를 이 그림에서 직접 읽었다고 하지 않는다. 접는 변/안쪽 치수·제작 오차·블록 규격을 별도로 확인한다.'],
 '1628260916513':['PDF1:1622048101479와 동일SHA의8열10행 격자종이다. 다른 수준 페이지의 재사용이며 새 도형/독립 자료로 합산하지 않는다.'],
 '1628260971100':['PDF1:1622048118054와 동일SHA의 정육면체 전개도다. 다른 수준의 서술/예시와 파일의 치수 표시를 구별한다.'],
 '1628260998775':['PDF1:1622048132504와 동일SHA의 직육면체 전개도다. 다른 단계의 학생 반응/효과나 별도 전개도로 세지 않는다.'],
}

OBSERVATIONS=[
 dict(id='LT-P34',standard_codes=['6수03-12','6수03-13'],question='교사는 한 변1cm의 같은 정사각형으로 가로5칸·세로4칸인 직사각형 벽을 만든다. 첫 제시는 왼쪽 한 열과 아래 한 행의 칸만 그리고 나머지 내부 선은 지운 부분 격자다. 지붕은 측정 대상에서 제외한다. 보이는 작은 칸과 큰 빈 부분을 각각 하나로 세면 되는가? 처음 예상과 격자를 완성한 뒤의 설명을 따로 남겨라.',expected='왼쪽4칸과 아래5칸은 모서리1칸을 공유해 드러난 작은 칸8개다. 큰 빈 부분은 같은 단위12칸에 해당하므로 전체는5×4=20칸·20cm²다. 큰 빈 부분 하나를1cm²로 세어9라 하거나4+5=9를 전체로 쓰지 않는다. 지붕/굴뚝은 정한 벽 영역에 더하지 않는다.',interpretation='첨부의 전체/부분/빈 벽 구성을 참고한 자체cm 과제다. 처음 부분 격자만 본 전략,교사의 선 추가·단위 제시,전체 격자를 본 뒤 수정은 서로 다른 근거다. 원본의 실제1인치 출력이나 학생의 자발적 배열 구성을 관찰했다고 하지 않는다. 숨은 칸을 다 그려야만 이해한 것으로 판정하지 않고 줄/열 설명도 기록한다.',student_validated=False),
 dict(id='LT-P35',standard_codes=['6수03-12','6수03-13'],question='한 변1cm인 같은 정사각형을7열4행으로 빈틈·겹침 없이 배열한 종이에 새 그림을 번갈아14칸에 넣고14칸은 비웠다. 종이 전체 넓이는14cm²인가,28cm²인가? 새 그림을 지우거나 더 그렸을 때 전체 넓이가 달라지는지도 설명하라. 덮기 단위를 따로 인쇄했다면 쓰기 전에 무엇을 맞춰야 하는가?',expected='전체는7×4=28칸·28cm²이고 새 그림이 있는14칸과 빈14칸을 모두 포함한다. 새 그림을 바꿔도 종이의 경계/단위가 같으면 전체 넓이는 그대로다. 새의 불규칙한 검은 외곽 넓이나 그림 수14를 전체 넓이로 쓰지 않는다. 별도 단위는 격자와 같은 변 길이인지 확인해 빈틈·겹침 없이 사용한다.',interpretation='퀼트의 장식/빈칸/전체와 단위 일치를 구별하는 자체1cm 과제다. 출력 배율과 절단 여백이 다른 자료를 같은 단위라고 가정하지 않는다. 호박 사진16개/바구니12칸도 인쇄 수량·단위 넓이·실제 물체 부피를 구별한다. 그림 수 세기/곱셈 정답만으로 실제 덮기나 단위 반복 수행을 관찰했다고 하지 않는다.',student_validated=False),
 dict(id='LT-P36',standard_codes=['6수03-09','6수03-18','6수03-19'],question='이상적인 정육면체 전개도의 각 면은 원래 한 변2cm인 정사각형이다. 교사가 종이를 가로·세로 모두200%로 확대해 각 면의 변이4cm가 되었다. 두 모형의 면 수,표면 넓이,내부 부피와1cm 정육면체로 빈틈없이 채울 때의 개수를 비교하라. 여섯 면이라는 이유로 블록도6개라고 해도 되는가?',expected='면은 둘 다6개다. 원래 표면 넓이는6×2²=24cm²·부피2³=8cm³·단위블록8개이고,확대 후96cm²·64cm³·64개다. 변2배·표면 넓이4배·부피8배이며 면 수는 그대로다. 면6개와 내부 단위블록 수를 구별한다.',interpretation='실제 첨부에는 없는cm 치수를 명시한 자체 대조다.200%는 각 방향 길이 비율이며 프린터의 실제 출력 결과를 측정한 것이 아니다. 실제 제작은 단위블록 규격·안쪽 치수·종이 두께/여분·붙는 변과 접힘을 확인한다. 일반80칸 격자종 전체를 상자 부피80으로 바꾸거나 치수 없는 첨부에 예시 부피를 확정하지 않는다. 계산/도면 검토와 실제 조립·채움 수행은 따로 기록한다.',student_validated=False),
]
MAPPINGS=[
 ('LT34',OBSERVATIONS[0]['standard_codes'],['1584734829908.pdf PDF1–3 / 1583353156064,1583353226406,1583353243997.pdf PDF1 / 1620402696194.pdf PDF1'],'전체/부분/빈 격자의 제시 조건,같은 단위로 숨은 영역을 구성하기,벽과 지붕 등 측정 대상의 경계를 구별하는 자체 설계에 참고한다.','작은 칸8개와 큰 빈 부분1개는 같은 넓이 단위9개가 아니다. 실제 출력 치수/허용 조작·교사 도움을 확인하고 정답 수만으로 자발적 배열 구성/현재 학생 단계를 판정하지 않는다.'),
 ('LT35',OBSERVATIONS[1]['standard_codes'],['1608590819262.pdf PDF1 / 1608572065121.pdf PDF1–2 / 1606931162619,1608070312536.pdf PDF1'],'장식 수와 전체 영역,빈칸의 넓이,같은 넓이 동률과 출력한 단위의 일치를 구별하는 자체 설계에 참고한다.','새14개와 전체28칸·호박16사진과 바구니12칸을 구별한다. 사진 외곽/프린터 여백을 같은 단위로 가정하거나 장식 그림/물체 수를3차원 부피·들이로 전용하지 않는다. 같은 구성의 다른 파일은 독립 연구가 아니다.'),
 ('LT36',OBSERVATIONS[2]['standard_codes'],['1589393198115.pdf PDF1 / 1622048101479,1622048118054,1622048132504.pdf PDF1 / 1628260916513,1628260971100,1628260998775.pdf PDF1'],'일반 격자종과 특정 전개도,면 수/표면 단위/내부 단위,출력 배율과 단위블록 규격을 구별하는 자체 설계에 참고한다.','치수 없는 전개도에서 예시 부피/출력 치수/실제 접기 성공을 확정하지 않는다.16URL은13개 파일이며3쌍은 같은SHA의 재사용이다. 서로 다른 수준의 독립 효과/학생 수로 합산하지 않는다.'),
]

def verify():
 assert 4+5-1==8 and 5*4-8==12 and 5*4==20
 assert 7*4==28 and 28//2==14
 assert 6*2**2==24 and 6*4**2==96 and 2**3==8 and 4**3==64
 assert 3*6+2*2==22 and 2*(3*2+3*1+2*1)==22 and 3*2*1==6
 assert 6*8==48 and 3*4==12 and 8*10==80

def main():
 verify();registry=load_registry();s=registry['sources'][SOURCE]
 if s['snapshot_file']==NOTES:
  assert {m[0] for m in MAPPINGS}<={c['id'] for c in registry['claims']}
  print('LT2 linked PDF reading remains current; no automatic refresh');build_report();return
 assert s['snapshot_file']==PRIOR_NOTES and s['snapshot_sha256']==PRIOR_SHA
 assert hashlib.sha256((ROOT/PRIOR_NOTES).read_bytes()).hexdigest()==PRIOR_SHA
 old=copy.deepcopy(registry);relations=copy.deepcopy(load_reviews());prior=json.loads((ROOT/PRIOR_NOTES).read_text(encoding='utf-8'))
 assets=json.loads((ROOT/'tmp/literature/lt2-measurement-pdf/manifest.json').read_text(encoding='utf-8'))
 html=json.loads((ROOT/'tmp/literature/lt2-area-volume-activities/activity-manifest.json').read_text(encoding='utf-8'));links=defaultdict(list)
 for page in html:
  for u in page['links']:
   if u.startswith(URL+'documents/') and u.endswith('.pdf'):links[u].append(page['url'])
 assert len(assets)==len(links)==16 and {a['url'] for a in assets}==set(links)
 manifest=[];hashes=defaultdict(list);log={}
 for a in assets:
  assert a['status']==200 and a['linked_page_urls']==sorted(set(links[a['url']]))
  assert hashlib.sha256((ROOT/a['file']).read_bytes()).hexdigest()==a['sha256']
  for r in a['renders']:assert hashlib.sha256((ROOT/r['file']).read_bytes()).hexdigest()==r['sha256']
  ident=a['url'].split('/')[-1][:-4];assert len(PDF_NOTES[ident])==a['pdf_pages']
  manifest.append(dict(**{k:a[k] for k in ['url','linked_page_urls','status','content_type','sha256','pdf_pages']},read_kind='linked_pdf_content_and_visual_review',redistributed=False,content_read_method='visual_worksheet_with_available_text',content_pdf_pages=list(range(1,a['pdf_pages']+1)),visual_pdf_pages=list(range(1,a['pdf_pages']+1)),rendered_pages=[{k:r[k] for k in ['pdf_page','sha256']} for r in a['renders']]))
  hashes[a['sha256']].append(a['url']);log[a['url']]=PDF_NOTES[ident]
 assert len(hashes)==13 and sum(a['pdf_pages'] for a in assets)==19
 assert sum(next(a['pdf_pages'] for a in assets if a['sha256']==k) for k in hashes)==16
 corrections=[dict(kind='linked_pdf_worksheet_scope',locations=list(log),action='16개URL/19쪽을실제시각대조했고13개파일/16개고유쪽과구별했다.3쌍은같은SHA의재사용이며다른단계의효과로합산하지않는다. HTML주출처와별도PDF첨부를구별하고원본/도면/추출전체텍스트를이식용묶음에복제하지않는다.'),dict(kind='worksheet_units_and_representation',locations=list(log),action='48/12타일·5×4벽의부분격자·7×4퀼트의14장식/14빈칸·16호박사진/12바구니칸·같은넓이정원·치수없는네직사각형·80칸일반격자종/특정전개도·22표면칸/내부6단위의조건을구별한다. 치수/출력배율/접는선/단위규격/실제조립성공이그림에서확인되지않으면미확인으로남긴다.')]
 p=ROOT/'data/sources.json';bibliography=json.loads(p.read_text(encoding='utf-8'));b=next(v for v in bibliography if v['id']==SOURCE);previous_b=copy.deepcopy(b)
 next_review='기록된824개활동/교사자료중730개공개영어본문은대기다. 이번16개LT2수학PDF링크의19쪽을확인했으나,외부수학놀이매뉴얼2링크·가정용소개1페이지의실제안내·링크가없는별도타일/도식·그림책/영상/게임/교재/원연구/번역·다른출처미검토범위는별도다. 단위/차원/전체부분/제시조건/도움과예상시점을우선대조하며실제독립/학생검증으로승격하지않는다.'
 b.update(review_scope=SCOPE,next_review=next_review)
 pending={k:[u for u in v if u not in links and '/downloads/' not in u] for k,v in prior['linked_attachment_urls_not_read'].items()};pending={k:v for k,v in pending.items() if v}
 notes=copy.deepcopy(prior);notes.update(date='2026-11-06',read_scope=SCOPE,previous_review=copy.deepcopy(s),previous_bibliography=previous_b,previous_notes_file=PRIOR_NOTES,previous_notes_sha256=PRIOR_SHA,pdf_read=True,primary_asset_is_pdf=False,original_page_layout_review=False,supplementary_pdf_read_manifest=manifest,pdf_reading_log=log,pdf_exact_reuse_groups=[dict(sha256=k,urls=v) for k,v in hashes.items() if len(v)>1],supplementary_pdf_coverage=dict(urls=16,page_occurrences=19,distinct_sha256_files=13,pages_after_file_deduplication=16,all_selected_pages_visual_reviewed=True,whole_site_attachment_review=False),reading_log=prior['reading_log']+['실제수학PDF16개URL의19쪽을이미지로확인했고동일SHA3쌍을제외한13개파일16쪽과구별했다. 추출문자가없는쪽도도형을확인했다.'],source_corrections=prior['source_corrections']+corrections,linked_attachment_urls_not_read=pending,unread_followups=[next_review,'가정용소개페이지의실제배포자료·미선정첨부·영상/게임/원연구·실제독립/학생검증은미확인이다.'])
 npath=ROOT/NOTES;npath.write_text(json.dumps(notes,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 history=s.get('snapshot_history',[])+[dict(snapshot_file=PRIOR_NOTES,snapshot_sha256=PRIOR_SHA,date=s['date'],read_scope=s['read_scope'])]
 s.update(date='2026-11-06',snapshot_file=NOTES,snapshot_sha256=hashlib.sha256(npath.read_bytes()).hexdigest(),snapshot_history=history,bibliography_snapshot=digest(b),read_scope=SCOPE,supplementary_pdf_read_manifest=manifest,method_note='실제연결된LT2수학PDF16URL의19쪽을모두이미지로대조했다. 추출문자부재를빈페이지로해석하지않고도형/격자를확인했으며중복SHA3쌍·단위/전체/제시조건/출력배율/전개도한계를구별한다.',limits='344개HTML/110개삽입이미지URL및별도수학PDF16URL의명시범위다. PDF는13개파일·16개고유쪽이며현재학생자료/독립연구가아니다.730개공개본문·외부매뉴얼·가정용첨부·나머지첨부/영상/게임/그림책/원연구/번역·한국어과제의진단정확도/교수효과는미검토다. 실제출력/조립/채움/학생수행은자체계산과구별한다.',editorial_action='이전주장33건/관찰33건을보존하고5개기준에새주장3건/자체관찰3건을대응했다. 누적주장36건·관찰36건·기준48개다. 관계검토·독립검토·학생검증에더하지않는다.',observations=s['observations']+OBSERVATIONS)
 for cid,codes,locations,support,limit in MAPPINGS:
  registry['claims'].append(dict(id=cid,source_id=SOURCE,role='related_theoretical_context',locations=locations,support=support,does_not_establish=limit,standard_codes=codes,target_snapshots={'revision:'+c:digest(target_value('revision:'+c)) for c in codes},independent_review=False,student_validated=False))
 assert len({code for c in registry['claims'] if c['source_id']==SOURCE for code in c['standard_codes']})==48
 p.write_text(json.dumps(bibliography,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');(ROOT/'data/literature_claim_reviews.json').write_text(json.dumps(registry,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 p=ROOT/'data/content_review_queue.json';q=json.loads(p.read_text(encoding='utf-8'));row=next(v for v in q['literature_review'] if v['source']['id']==SOURCE);row.update(source=b,claim_ids=[c['id'] for c in registry['claims'] if c['source_id']==SOURCE]);p.write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 assert registry['claims'][:len(old['claims'])]==old['claims'] and s['observations'][:33]==old['sources'][SOURCE]['observations']
 assert all(registry['sources'][k]==v for k,v in old['sources'].items() if k!=SOURCE) and load_reviews()==relations
 build_report();print('Added16 linked LT2 PDF URLs/19 reviewed pages (13 file hashes/16 unique pages),3 claims/probes;730 linked public bodies pending')

if __name__=='__main__':main()
