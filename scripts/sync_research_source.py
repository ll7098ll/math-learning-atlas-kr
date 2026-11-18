"""Copy the reproducible research sources into the Site source repository."""
from pathlib import Path
import shutil,re,json
from urllib.parse import unquote
R=Path(__file__).resolve().parents[1];SITE=R/'tmp/pathways-release';DEST=SITE/'research'
assert SITE.is_dir() and R.name!='research'
for folder in ['data','analyses','docs','indexes','scripts']:
 for src in (R/folder).rglob('*'):
  if not src.is_file() or '__pycache__' in src.parts or src.suffix not in ['.json','.md','.py','.mjs','.cjs','.csv','.png']:continue
  target=DEST/src.relative_to(R);target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,target)
for src in [R/'README.md',R/'[별책8] 수학과 교육과정.pdf']:
 target=DEST/src.name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,target)
for name in ['distribution-lab.html','inquiry-workbook.html']:
 src=R/'portal'/name;target=DEST/'portal'/name
 target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,target)
literature=R/'data/literature_claim_reviews.json'
if literature.exists():
 for review in json.loads(literature.read_text(encoding='utf-8'))['sources'].values():
  if review.get('snapshot_kind')=='authored_review_notes':
   assert review['redistribution_license']=='workspace_authored_notes'
   assert Path(review['snapshot_file']).suffix=='.json'
   continue # Authored JSON notes were copied above; the cached source PDF stays outside research/.
  assert review['redistribution_license'] in ['CC BY 4.0','Public domain (explicit report declaration)'],'Literature redistribution needs a documented license'
  if review['redistribution_license']=='Public domain (explicit report declaration)':assert review['license_location'] and review['license_statement']
  src=(R/review['snapshot_file']).resolve();assert src.is_relative_to((R/'data/literature_evidence').resolve())
  target=DEST/src.relative_to(R);target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,target)
# Historical plans link a handful of earlier portal source snapshots.
# Preserve those referenced files, without copying temporary dependencies.
for src in [R/'README.md',*(R/'docs').glob('*.md'),*(R/'indexes').glob('*.md')]:
 for raw in re.findall(r'\]\(([^\s)]+)\)',src.read_text(encoding='utf-8')):
  if raw.startswith(('https:','http:','#')):continue
  path=(src.parent/unquote(raw.split('#')[0])).resolve()
  if path.is_file() and path.is_relative_to(R/'portal'):
   target=DEST/path.relative_to(R);target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(path,target)
(SITE/'RESEARCH.md').write_text('''# 연구 자료와 재생성

개별 보강 원본과 문서는 `research/`에 보관한다.

Python 3와 Node.js가 있는 환경에서 다음을 실행한다.

```text
python research/scripts/run_revision_checks.py
```

435개 기준의 개별 항목 검사, 문서·포털 자료 재생성, 원문·출처 검사와 모델 검사를 함께 실행한다. 생성 결과는 같은 저장소의 `dist/`에 쓴다. 편집 원본은 `research/data/revisions_*.json`이며 초기 세 사례의 원본은 `research/data/initial_case_studies.json`에 보존한다. 이전 생성기를 실행한 뒤에도 이 통합 명령으로 개별 보강을 반영한다.
''',encoding='utf-8')
print('reproducible sources synchronized')
