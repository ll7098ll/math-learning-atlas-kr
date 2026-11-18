"""Freeze an attributed public series; rebuild CSV without a network dependency."""
from pathlib import Path
from decimal import Decimal
from datetime import datetime,timezone,timedelta
import argparse,csv,hashlib,json,urllib.request
R=Path(__file__).resolve().parents[1]
URL='https://api.worldbank.org/v2/country/KOR/indicator/NY.GDP.MKTP.KD.ZG?date=2020%3A2024&format=json'
SOURCE=R/'data/source_evidence/world-bank-korea-gdp-growth-2020-2024.json'
PROVENANCE=SOURCE.parent/'world-bank-korea-gdp-growth-provenance.json'

def build(fetch=False):
 if fetch:
  with urllib.request.urlopen(URL,timeout=30) as response:raw=response.read()
  parsed=json.loads(raw)
  assert parsed[0]['total']==5 and len(parsed[1])==5
  SOURCE.parent.mkdir(parents=True,exist_ok=True)
  SOURCE.write_bytes(raw)
  retrieved_date=datetime.now(timezone(timedelta(hours=9))).date().isoformat()
 else:
  previous=json.loads(PROVENANCE.read_text(encoding='utf-8'))
  assert previous['raw_sha256']==hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'Frozen raw response changed; fetch and review deliberately'
  assert previous['source_url']==URL
  retrieved_date=previous['retrieved_date']
 data=json.loads(SOURCE.read_text(encoding='utf-8'),parse_float=Decimal)
 assert {r['date'] for r in data[1]}==set(map(str,range(2020,2025)))
 assert all(r['countryiso3code']=='KOR' and r['indicator']['id']=='NY.GDP.MKTP.KD.ZG' and r['value'] is not None for r in data[1])
 meta=dict(provider='World Bank, World Development Indicators',indicator='NY.GDP.MKTP.KD.ZG',
  title='GDP growth (annual %)',country='KOR',years=[2020,2021,2022,2023,2024],
  source_url=URL,definition_url='https://data.worldbank.org/indicator/NY.GDP.MKTP.KD.ZG',
  retrieved_date=retrieved_date,api_lastupdated=data[0]['lastupdated'],license='CC BY 4.0',
  raw_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
  scope='World Bank 공개 통계의 동결본. GDP 수준·명목 GDP·물가상승률 자료가 아니며 관측 시계열만으로 원인을 판단하지 않는다. 통계 개정 시 값이 달라질 수 있다.')
 PROVENANCE.write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 fields=['year','country','indicator','value','unit','data_kind','source_url','retrieved_date','api_lastupdated']
 dest=R/'data/teaching_examples/source-korea-gdp-growth.csv'
 with dest.open('w',encoding='utf-8',newline='') as f:
  writer=csv.DictWriter(f,fieldnames=fields);writer.writeheader()
  for row in sorted(data[1],key=lambda r:r['date']):
   writer.writerow(dict(year=row['date'],country='KOR',indicator=meta['indicator'],value=str(row['value']),
    unit='percent_per_year',data_kind='published_statistic',source_url=URL,retrieved_date=meta['retrieved_date'],api_lastupdated=meta['api_lastupdated']))
 print('Frozen source series: 5 rows; source values preserved, no derived index')
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--fetch',action='store_true');build(parser.parse_args().fetch)
