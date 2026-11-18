"""Build a self-contained theoretical distribution exploration page."""
from pathlib import Path
import json,math
from statistical_tools import NORMAL,normal_pdf,t_pdf,t_cdf,t_quantile
ROOT=Path(__file__).resolve().parents[1]
DFS=[1,2,3,5,10,30,60]
def model_data():
 xs=[round(i/20,2) for i in range(-300,301)]
 def row(df):
  pdf=normal_pdf if df is None else lambda x:t_pdf(x,df)
  cdf=NORMAL.cdf if df is None else lambda x:t_cdf(x,df)
  return dict(df=df,curve=[pdf(x) for x in xs],tail2=2*(1-cdf(2)),q975=NORMAL.inv_cdf(.975) if df is None else t_quantile(.975,df),visible={str(k):2*cdf(k)-1 for k in [5,15]})
 return dict(xs=xs,normal=row(None),student=[row(df) for df in DFS],model_kind='theoretical_not_observed',generated_by='scripts/build_distribution_lab.py')
def build(out):
 data=model_data();template=(ROOT/'portal/distribution-lab.html').read_text(encoding='utf-8')
 assert template.count('@@MODEL_DATA@@')==1
 body=template.replace('@@MODEL_DATA@@',json.dumps(data,ensure_ascii=False,separators=(',',':')))
 out=Path(out);out.mkdir(parents=True,exist_ok=True);(out/'distribution-lab.html').write_text(body,encoding='utf-8')
 return data
if __name__=='__main__':
 from build_portal_data import OUT
 build(OUT);print('Built normal/t distribution lab')
