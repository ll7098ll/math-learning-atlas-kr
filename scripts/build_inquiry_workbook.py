"""Build an original printable inquiry worksheet; model examples, no student data."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def build(out):
 rows=[]
 for x in range(1,10):
  y=10-x;rows.append(f'<tr data-x="{x}"><td>{x}</td><td>{y}</td><td>{2*x+2*y}</td><td>{x*y}</td></tr>')
 drawings=[]
 for x in [1,5,9]:
  y=10-x;w,h=12*x,12*y
  drawings.append(f'<svg viewBox="0 0 165 160" role="img" aria-label="x={x}cm,y={y}cm,넓이{x*y}cm²"><rect data-model-x="{x}" x="28" y="22" width="{w}" height="{h}" fill="#dbe8d1" stroke="#38654f" stroke-width="1.5"/><text x="28" y="14" font-size="12">x={x}cm</text><text x="{w+32}" y="{h/2+25}" font-size="12">{y}cm</text><text x="28" y="150" font-size="12">A={x*y}cm² · P=20cm</text></svg>')
 body=(ROOT/'portal/inquiry-workbook.html').read_text(encoding='utf-8')
 for key,value in [('@@RECTANGLE_TABLE@@',''.join(rows)),('@@RECTANGLE_DRAWINGS@@',''.join(drawings))]:
  assert body.count(key)==1;body=body.replace(key,value)
 out=Path(out);out.mkdir(parents=True,exist_ok=True);(out/'inquiry-workbook.html').write_text(body,encoding='utf-8')
 return body
if __name__=='__main__':
 from build_portal_data import OUT
 build(OUT);print('Built original printable inquiry workbook')
