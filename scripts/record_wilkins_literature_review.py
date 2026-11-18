"""Record the full article actually read; this is not an automatic reviewer."""
import json,hashlib
from literature_review import ROOT,digest,target_value,load_registry,build_report

SOURCE='WILKINS_NORTON_2018'
PDF='data/literature_evidence/WILKINS_NORTON_2018.pdf'
SHA='78aadcd5850620ca38448258ae1e8b26dced5a8e25863c5be38532f6b10fe24b'
URL='https://link.springer.com/article/10.1186/s40594-018-0119-2'
MAPPINGS=[
 ('WN01','relation:L001',['6수01-10'],['PDF2 Table1','PDF4–5 MSPF/GMSF'],
  '전체·단위분수·분수량의 기준을 구별하는 분석 관점을 지원한다.',
  '1m별 분배가 모든 학습자의 필수 경로라는 실증 근거는 아니다.'),
 ('WN02','relation:L003',['6수01-10'],['PDF3–5 measurement schemes','PDF9 Fig7'],
  '단위분수의 반복을 분수량 구성과 연결하는 이론적 맥락이다.',
  '현재3m÷4 과제의 선수성·채점 타당성을 검증한 자료는 아니다.'),
 ('WN03','relation:L023',['4수01-09','4수01-10','6수01-10'],['PDF2 Table1','PDF5 Splitting'],
  '등분할과 반복의 역관계 및 두 행동의 조정을 구별하도록 한다.',
  '두 행동을 순서대로 실행한 성공만으로 splitting 구성을 확정할 수 없다.'),
 ('WN04','pilot:fraction-01',['6수01-10'],['PDF4–5 units coordination'],
  '분모가 어느 전체에 대한 것인지 유지하는 관점과 관련된다.',
  '1m의1/4과3m의1/4 비교는 자체 수학적 진단 설계다.'),
 ('WN05','pilot:fraction-02',['4수01-09','6수01-10'],['PDF2 Table1','PDF3 PWS'],
  '같은 크기로 나누고 부분을 전체와 함께 유지하는 의미를 지원한다.',
  '물리적 자르기 수행이 모든 학생에게 선행해야 한다는 뜻은 아니다.'),
 ('WN06','pilot:fraction-03',['4수01-10','6수01-10'],['PDF4 MSPF','PDF9 Fig7c'],
  '같은 단위분수를 반복해 진분수를 만드는 관점에 대응한다.',
  '진분수 생성 성공과 전체 복원·가분수의 동시 단위 조정을 구별한다.'),
 ('WN07','pilot:fraction-06',['6수01-10'],['PDF2 Table1','PDF5 units coordination'],
  '기준 전체와 측정 단위의 관계를 유지하는 관점을 제공한다.',
  '3m의1/4을3/4m로 바꾸는 식만 맞힌 반응으로 인지 단계를 판정하지 않는다.'),
 ('WN08','pilot:fraction-09',['4수01-10','6수01-10'],['PDF4 GMSF','PDF8 results','PDF9 Fig7d'],
  '가분수 생성과 가분수로부터 전체 복원을 별도로 확인할 이유를 지원한다.',
  '5÷3=5/3의 한 번 성공은 GMSF나 세 수준 동시 조정의 검증이 아니다.'),
 ('WN09','family:fraction',['4수01-09','4수01-10','4수01-11','6수01-06','6수01-07'],['PDF3 Table2','PDF4 Table3','PDF6 Fig6'],
  '측정 관점의 분수와 등분할·반복·전체 복원의 구별에 참고한다.',
  '음의 유리수·유리함수로의 전이나 한국 학년별 발달 순서를 이 논문이 직접 입증하지 않는다.')]

def main():
 path=ROOT/'data/literature_claim_reviews.json'
 registry=load_registry()
 if SOURCE in registry['sources']:
  print('Existing reviewed targets and source remain current; no automatic refresh');build_report();return
 file=ROOT/PDF;assert hashlib.sha256(file.read_bytes()).hexdigest()==SHA
 sp=ROOT/'data/sources.json';sources=json.loads(sp.read_text(encoding='utf-8'));b=next(s for s in sources if s['id']==SOURCE)
 previous=dict(b)
 b['review_scope']='공개 논문 PDF11쪽 전체의 이미지와 표1~4·그림1~7, 이론·방법·결과·결론·참고문헌을 확인. L001/L003/L023·분수 시범 주장5개·분수 분석군의 지원 범위를 대조. 종합 논문이 인용한 원연구 전부를 독립 재분석한 것은 아님.'
 b['next_review']='현재 자체 과제의 반응으로 연구 스킴을 판정하려면 원도구·채점·전이 타당성을 별도 검토하고 실제 응답을 확보해야 함.'
 source=dict(source_id=SOURCE,state='self_read_claim_mapping',reviewer='Codex',date='2026-11-04',
  snapshot_file=PDF,snapshot_sha256=SHA,redistribution_license='CC BY 4.0',license_url='https://creativecommons.org/licenses/by/4.0/',
  bibliography_snapshot=digest(b),previous_bibliography=previous,
  display=dict(title=b['title'],url=URL,authors_year='Wilkins and Norton 2018'),
  read_scope='PDF1~11 전체의 실제 이미지, 표1~4·그림1~7 및 참고문헌 확인',
  scope_note='논문의 측정적 분수 모델은 자체 과제의 관련 이론으로 사용한다. 세 수준의 동시 조정은 GMSF와 관련되며 MSPF의 필수 선행 조건으로 동일시하지 않는다.',
  method_note='5~8학년 미국·중국 자료를 포함한 선행 연구 종합이다. 스킴/조작별4문항과 연관 통계를 사용한 연구들을 논한다. 표4는 서로 다른 표본·일부 중첩/종단 자료이며 괄호의 MSPF 값은 가역성 문항을 제외한 합성 수행만이다. 비율의 감소만으로 화살표를 입증하지 않는다(PDF6~8).',
  limits='종합한 원연구의 원자료·채점·모든 분석을 독립 재검토하지 않았다. 현재 한국 교육과정의 과제·진단·필수 숙달 순서나 수업 효과를 이 논문으로 검증하지 않는다.',
  editorial_action='기존 화살표는 과제별 자체 가설로 유지하고, 진분수/가분수에서 전체를 복원하는 추가 관찰 두 개와 추론 제한을 상세 문서에 표시한다.',
  independent_review=False,student_validated=False,
  observations=[
   dict(id='WN-P1',standard_codes=['4수01-10','6수01-10'],question='길이가 표시되지 않은 종이띠가 어떤 전체의3/4이다. 이 띠만 이용해 그 전체를 구성하고, 지금 주어진 띠와1/4 단위의 관계를 설명하라.',
    expected='띠를 같은 길이3부분으로 나누면 한 부분이 원래 전체의1/4이고 이를4번 이어 전체를 만든다. 띠 길이가3/4m라고 주어진 것은 아니므로1m라는 길이를 임의로 가정하지 않는다.',
    interpretation='자체 관찰 설계다. 단계별 재구성과 관계 설명을 기록하며 한 성공으로 MSPF 판정을 확정하지 않는다.',student_validated=False),
   dict(id='WN-P2',standard_codes=['4수01-10','6수01-10'],question='다른 종이띠가 어떤 전체의5/3이다. 원래 전체와1/3 단위를 만들고, 전체·1/3·주어진 띠를 동시에 가리키며 관계를 설명하라.',
    expected='띠의 같은 길이5부분 중 하나가1/3이고 그3개가 전체다. 주어진 띠는전체보다 크며 다섯 단위의 묶음이다. 띠를 새 전체로 바꾸어5/5라 부르는 것과 구별한다.',
    interpretation='분수 생성·알고리즘 정답·가분수에서 전체 복원을 구별하는 자체 설계다. 여러 과제·설명·면담 없이 GMSF나 동시 조정을 확정하지 않는다.',student_validated=False)])
 claims=[]
 for cid,target,codes,locations,support,limit in MAPPINGS:
  claims.append(dict(id=cid,source_id=SOURCE,role='related_theoretical_context',locations=locations,support=support,does_not_establish=limit,
   target_snapshots={target:digest(target_value(target))},standard_codes=codes,independent_review=False,student_validated=False))
 registry['sources'][SOURCE]=source;registry['claims']+=claims
 sp.write_text(json.dumps(sources,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');path.write_text(json.dumps(registry,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 qp=ROOT/'data/content_review_queue.json';queue=json.loads(qp.read_text(encoding='utf-8'));row=next(r for r in queue['literature_review'] if r['source']['id']==SOURCE)
 row.update(source=b,status='self_read_claim_mapping',evidence_files=['data/literature_claim_reviews.json','docs/문헌주장별근거.md'],claim_ids=[c['id'] for c in claims])
 qp.write_text(json.dumps(queue,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');build_report()
if __name__=='__main__':main()
