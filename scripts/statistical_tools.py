"""Standard-library teaching calculations, not a check of sampling validity.

python stats-inference.py practice-refill-time.csv practice-preference.csv
Both CSVs are fictional teaching data. Mean model: independent normal sample.
Proportion model: independent Bernoulli approximation, at least 10 of each outcome.
Method reference: https://www.itl.nist.gov/div898/handbook/eda/section3/eda3521.htm
"""
from math import exp,lgamma,log,pi,sqrt,isfinite,comb
from statistics import NormalDist,mean,stdev
import csv,json,sys

NORMAL=NormalDist()
def normal_pdf(x):return exp(-x*x/2)/sqrt(2*pi)
def t_pdf(x,df):
    if df<=0:raise ValueError('df must be positive')
    return exp(lgamma((df+1)/2)-lgamma(df/2)-0.5*log(df*pi)-(df+1)/2*log(1+x*x/df))
def t_cdf(x,df,steps=2000):
    if df<=0 or steps<=0 or steps%2 or not isfinite(x):raise ValueError('finite x, positive df and positive even steps required')
    if x==0:return 0.5
    width=abs(x)/steps
    integral=width/3*(t_pdf(0,df)+t_pdf(abs(x),df)+sum((4 if k%2 else 2)*t_pdf(k*width,df) for k in range(1,steps)))
    return 0.5+integral if x>0 else 0.5-integral
def t_quantile(p,df):
    if not 0<p<1 or df<=0:raise ValueError('0<p<1 and df>0 required')
    if p==0.5:return 0.0
    if p<0.5:return -t_quantile(1-p,df)
    lo,hi=0.,1.
    while t_cdf(hi,df)<p:
        hi*=2
        if hi>64:raise ValueError('teaching quantile range exceeded')
    for _ in range(45):
        mid=(lo+hi)/2
        if t_cdf(mid,df)<p:lo=mid
        else:hi=mid
    return (lo+hi)/2
def mean_interval(values,confidence=0.95,known_sigma=None):
    values=list(values);n=len(values)
    if n<2 or not all(isfinite(x) for x in values) or not 0<confidence<1:raise ValueError('finite sample n>=2 and 0<confidence<1 required')
    if known_sigma is not None and (not isfinite(known_sigma) or known_sigma<=0):raise ValueError('known sigma must be positive')
    center=mean(values);sd=stdev(values)
    se=(known_sigma if known_sigma is not None else sd)/sqrt(n)
    critical=NORMAL.inv_cdf((1+confidence)/2) if known_sigma is not None else t_quantile((1+confidence)/2,n-1)
    return dict(n=n,mean=center,sample_sd=sd,se=se,critical=critical,lower=center-critical*se,upper=center+critical*se,method='normal_known_sigma' if known_sigma is not None else 'student_t',confidence=confidence)
def proportion_interval(successes,n,confidence=0.95):
    if not isinstance(n,int) or not isinstance(successes,int) or n<=0 or not 0<=successes<=n or not 0<confidence<1:raise ValueError('integer count 0<=successes<=n and valid confidence required')
    if min(successes,n-successes)<10:raise ValueError('normal approximation requires at least 10 successes and failures in this teaching tool')
    phat=successes/n;se=sqrt(phat*(1-phat)/n);z=NORMAL.inv_cdf((1+confidence)/2)
    return dict(n=n,successes=successes,estimate=phat,se=se,critical=z,lower=phat-z*se,upper=phat+z*se,method='normal_approximation',confidence=confidence)
def mean_test(values,mu0,alternative='two-sided'):
    values=list(values);n=len(values)
    if n<2 or not all(isfinite(x) for x in [*values,mu0]):raise ValueError('finite sample n>=2 required')
    sd=stdev(values)
    if sd==0:raise ValueError('nonzero sample standard deviation required')
    t=(mean(values)-mu0)/(sd/sqrt(n));cdf=t_cdf(t,n-1)
    if alternative=='two-sided':p=2*min(cdf,1-cdf)
    elif alternative=='greater':p=1-cdf
    elif alternative=='less':p=cdf
    else:raise ValueError('unsupported alternative')
    return dict(statistic=t,df=n-1,p_value=p,null_mean=mu0,alternative=alternative)

def run(mean_file,proportion_file):
    with open(mean_file,encoding='utf-8-sig',newline='') as f:values=[float(r['seconds']) for r in csv.DictReader(f)]
    with open(proportion_file,encoding='utf-8-sig',newline='') as f:responses=[int(r['reuse']) for r in csv.DictReader(f)]
    if not all(x in (0,1) for x in responses):raise ValueError('reuse must be 0 or 1')
    return dict(data_kind='fictional_teaching_data',mean_known_sigma6=mean_interval(values,known_sigma=6),mean_unknown_sigma=mean_interval(values),
        proportion=proportion_interval(sum(responses),len(responses)),test_mu20=mean_test(values,20),
        criticals_975=dict(normal=NORMAL.inv_cdf(.975),t5=t_quantile(.975,5),t30=t_quantile(.975,30)),
        binomial100=dict(exact_45_to_55=sum(comb(100,k) for k in range(45,56))/2**100,normal_with_correction=NORMAL.cdf(1.1)-NORMAL.cdf(-1.1)))
if __name__=='__main__':
    if len(sys.argv)!=3:raise SystemExit('Usage: python stats-inference.py practice-refill-time.csv practice-preference.csv')
    print(json.dumps(run(*sys.argv[1:]),ensure_ascii=False,indent=2))
