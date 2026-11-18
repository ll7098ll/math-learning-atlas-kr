"""Recalculate published anonymous ratings; these are not responses to our tasks."""
import csv,json,math,hashlib
from fractions import Fraction
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
CSV='data/teaching_examples/published-units-coordination-ratings-2015.csv'
NOTES='data/literature_evidence/VT_ASSESSMENT_review_notes.json'

def kappa(a,b,weighted=False):
 n=len(a);levels=[1,2,3]
 weight=lambda x,y:Fraction(1)-Fraction(abs(x-y),2) if weighted else Fraction(x==y)
 po=sum((weight(x,y) for x,y in zip(a,b)),Fraction())/n
 pe=sum((weight(x,y)*a.count(x)*b.count(y) for x in levels for y in levels),Fraction())/(n*n)
 return (po-pe)/(1-pe)

def ranks(values):
 return [Fraction(sum(i+1 for i,x in enumerate(sorted(values)) if x==v),values.count(v)) for v in values]

def rho(a,b):
 a=ranks(a);b=ranks(b);ma=sum(a)/len(a);mb=sum(b)/len(b)
 cov=sum((x-ma)*(y-mb) for x,y in zip(a,b))
 return float(cov)/math.sqrt(float(sum((x-ma)**2 for x in a)*sum((y-mb)**2 for y in b)))

def build_report(root=ROOT):
 with (root/CSV).open(encoding='utf-8',newline='') as f:rows=list(csv.DictReader(f))
 assert len(rows)==20 and [int(r['published_case']) for r in rows]==list(range(1,21))
 assert {r['data_kind'] for r in rows}=={'published_ratings_not_local_student_responses'}
 assert {r['source_table'] for r in rows}=={'Norton_et_al_2015_Table4_PDF15'}
 scores={k:[int(r[k]) for r in rows] for k in ['R5','R6','R7','R8','VideoFinal']}
 assert all(v in [1,2,3] for seq in scores.values() for v in seq)
 notes=json.loads((root/NOTES).read_text(encoding='utf-8'))
 assert hashlib.sha256((root/CSV).read_bytes()).hexdigest()==notes['published_ratings_csv_sha256']
 pairs=[]
 for a,b,expected,expected_w in [('R5','R6',0.57,0.65),('R7','R8',0.68,0.75)]:
  value=float(kappa(scores[a],scores[b]));weighted=float(kappa(scores[a],scores[b],True))
  assert round(value,2)==expected and round(weighted,2)==expected_w
  pairs.append(dict(raters=[a,b],exact_agreements=sum(x==y for x,y in zip(scores[a],scores[b])),n=20,kappa=value,linear_weighted_kappa=weighted))
 correlations={r:rho(scores[r],scores['VideoFinal']) for r in ['R5','R6','R7','R8']}
 assert [round(v,2) for v in correlations.values()]==[0.93,0.73,0.78,0.84]
 result=dict(status='pass',data_kind='published_table_recalculation',source_id='VT_ASSESSMENT',source_pdf_sha256=notes['source_pdf_sha256'],source_table='Table4 PDF15',n=20,
  reconciled_stage_counts={str(k):scores['VideoFinal'].count(k) for k in [1,2,3]},pair_agreement=pairs,spearman_to_reconciled_video=correlations,
  local_student_validation=False,independent_review=False,limitations='논문 표4의 공개 평정만 재계산했다. 녹화·원응답·모든 타당도 분석을 재검토하지 않았다. 상관은 정확 일치도와 다르며 같은20명을 재평정한 자료다. 자체 과제의 효과·인지 단계는 검증하지 않는다.')
 (root/'data/units_coordination_recalculation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(json.dumps(dict(status='pass',published_cases=20,local_student_validation=False),ensure_ascii=False));return result
if __name__=='__main__':build_report()
