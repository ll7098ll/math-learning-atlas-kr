# 개발과 검증

확인 기준일: 2026-11-18. 프로젝트 루트에서 실행하는 명령을 기준으로 한다. 데이터의 역할은 [구조 문서](ARCHITECTURE.md), 연구 편집 원칙은 [분석 규칙](분석규칙.md)을 참고한다.

## 실행 환경

배포된 포털은 정적 HTML·CSS·JavaScript로 실행된다. 보기에는 npm이 필요하지 않다. GitHub용 교육과정 탐색기 UI를 수정할 때는 Node.js와 npm으로 React·Tailwind CSS·shadcn/ui를 빌드한다. 연구 자료 생성과 검증에는 Python을 사용한다.

- Python 3.12를 기준으로 준비한다. 이번 점검에서 확인한 실제 런타임은 3.12.14다. 외부 Python 패키지는 `pypdf`와 `Pillow`다. PDF 목록 재추출에는 `pypdf`, 문헌의 DOCX·HTML 이미지 검증에는 `Pillow`가 쓰인다.
- Node.js 22 이상을 기준으로 준비한다. 검사 코드가 `import.meta.dirname`을 사용한다. 이번 문서 정비 환경의 실제 Node 버전은 `v24.14.0`이었다.
- 로컬 파일을 직접 여는 `file://` 대신 HTTP 서버를 사용한다. 브라우저는 JSON과 모듈을 요청해서 읽는다.

먼저 실행 파일을 확인한다.

```text
python --version
node --version
```

Windows에서 Python 버전 대신 Store 실행 안내가 나타나거나 명령이 동작하지 않으면 실제 Python 실행 파일을 사용한다. 이번 점검 시 기본 `python`은 WindowsApps 별칭이었다. 아래의 `python`은 정상 설치된 Python 실행 파일 또는 활성화된 가상 환경을 뜻한다.

```text
python -m venv .venv
```

PowerShell에서는 `./.venv/Scripts/python.exe`, macOS·Linux에서는 `./.venv/bin/python`을 `python` 대신 사용하면 활성화 스크립트 없이 실행할 수 있다.

```text
python -m pip install -r requirements.txt
```

`requirements.txt`는 이번 환경에서 확인한 `pypdf==6.21.4`, `Pillow==13.0.0`을 기록한다. 모든 도구의 최신 출시 버전이라는 뜻은 아니다. 정적 포털을 보기 위해 이 패키지를 설치할 필요는 없다.

## GitHub 스냅샷을 로컬에서 보기

GitHub용 포털은 `site/`다. 그 안의 `dist/index.html`, `dist/modules/`, `dist/content/`가 함께 있어야 한다.

```text
python -m http.server 8000 --bind 127.0.0.1 --directory site/dist
```

브라우저에서 `http://127.0.0.1:8000`을 연다. 종료는 서버 터미널에서 `Ctrl+C`다. `portal/`에는 통계 실험실과 탐구 워크북의 원본 HTML만 있으므로 그 폴더만 서비스하면 전체 포털은 나타나지 않는다.

Git에 올리는 스냅샷에서는 기준 PDF를 제외한다. 원본 작업 환경의 로컬 스냅샷에는 PDF가 있을 수 있다. GitHub에서 내려받은 경우 공식 PDF를 별도로 준비하고 해시를 대조한 뒤, 로컬 PDF 열기가 필요하면 `site/dist/curriculum.pdf`로 복사한다. PDF가 없어도 탐색과 상세 분석 데이터는 사용할 수 있다.

원본 작업 환경의 포털은 `tmp/pathways-release/dist/`다. 해당 폴더가 있는 개발자는 HTTP 서버의 `--directory`를 그 경로로 바꿔 실행할 수 있다. 아래 통합 생성 스크립트는 이 기존 작업 구조 또는 Sites 저장소의 `research/` 구조를 전제로 한다.

## 변경 종류에 따른 작업

| 변경 | 원본과 절차 |
|---|---|
| README·개발 안내 | Markdown을 수정하고 상대 링크를 검사한다. 전체 분석 재생성은 필요하지 않다. |
| 성취기준 표시 문장 보정 | 기준 PDF와 `source_corrections.json` 및 대조 근거를 함께 관리한다. 다른 판본으로 기준을 바꾸지 않는다. |
| 상세 분석의 해설·오류·진단 | 해당 `data/revisions_*.json`을 수정하고 자료를 재생성한다. |
| 목표·과제·조건 | 해당 `data/goal_hierarchy_*.json`과 필요한 검토 원장을 수정한다. 조건 적용 목표와 경로의 전체 AND를 보존한다. |
| 관계 설명·근거 | `relations.json`과 관련 관계 검토 원장을 함께 확인한다. 자동 생성되는 `revised_relations.json`만 수정하지 않는다. |
| 문헌 근거 | 출처·실제 읽은 위치·지원 범위·한계·대상 내용 해시를 함께 갱신한다. |
| 포털 화면 | GitHub용 탐색·비교·읽기 화면의 원본은 `site/frontend/`다. 기존 연결망·과제·전체 분석은 저술 환경의 HTML과 모듈에서 관리한다. 두 UI를 함께 내보내려면 아래 빌드와 스냅샷 갱신 절차를 사용한다. |

`author_*`, `record_*`, `extend_*`, `correct_*`, `integrate_*` 파일 중에는 특정 시점의 자료를 작성·교체하는 일회성 스크립트가 있다. 이름 목록 전체를 순서대로 실행하는 설치 과정은 없다. 기존 JSON과 검토 이력이 입력인지 출력인지 먼저 읽는다.

특히 `expand_analyses.py --freeze-content`와 `expand_secondary.py --freeze-content`는 수작업 원고 모듈로 JSON을 다시 만드는 옵션이다. JSON을 직접 편집한 뒤 무심코 실행하면 편집 내용을 덮어쓸 수 있다. 현재 상세 분석 Markdown도 개별 보강 생성기에 의해 다시 작성되므로 문서만 편집하는 방식으로 원장 변경을 대신하지 않는다.

## 검증 명령

### 문서와 연구 구조

```text
python scripts/validate_project.py
```

기준 PDF 해시, 전체 435개 성취기준, 학교급별 개수, 관계·출처 참조, 분석 상태와 Markdown의 로컬 파일 링크를 검사한다. 결과를 `data/project_validation.json`에 쓰므로 완전히 읽기 전용인 명령은 아니다. 문서 자체의 앵커 위치나 외부 URL의 접속 상태까지 검증하지는 않는다. 이 기존 전체 검사는 루트의 기준 PDF와 원문 대조 증거가 필요한 원본 작업 환경용이다. PDF·이미지가 제외된 GitHub 복사본에서 그대로 실행하면 누락 파일 검사에서 실패할 수 있다.

### 관련 부분만 확인

```text
python scripts/test_goal_hierarchy.py
python scripts/test_content_objects.py
python scripts/test_portal_retention.py
python scripts/test_literature_review.py
python scripts/test_source_image_reviews.py
```

각각 목표 조건, 불변 항목, 보관 계획, 문헌 근거의 상태·해시, 원문 이미지 근거를 검사한다. `test_source_image_reviews.py`는 기준 PDF와 대조 이미지를 확보한 환경에서 실행한다. 세부 내용 변경에는 해당 영역의 `check_*.py`도 적용한다. 예를 들어 확률과 통계 목표를 바꾸면 `python scripts/check_probability_statistics.py`를 실행한다.

GitHub 스냅샷에 대한 읽기 전용 Node 검사는 다음과 같다.

```text
node site/tests/test_goal_network.mjs
node site/tests/test_content_objects.mjs
node site/tests/test_catalog_groups.mjs
```

검사 범위는 목표 870개·경로 626개·목표 쌍 1,481개와 화면 상태 3,480개, 불변 항목 482개, 목록 화면 상태 710개다. 스냅샷용 검사는 루트의 연구 원장을 직접 참조하도록 경로를 조정했다. 기존 `tmp/pathways-release/tests/` 검사는 그 안의 `research/` 복사본을 참조한다. 원본 작업 환경에서 루트 원장을 바꾼 후 사본을 갱신하지 않으면 오래된 자료와 비교할 수 있다.

### 자료 재생성과 통합 검사

아래는 기준 PDF·원문 대조 자료·기존 Sites 작업 폴더를 갖춘 저술 환경용이다. `site/`를 포함한 GitHub 복사본만으로 이 과정을 그대로 실행할 수 있는 것은 아니다.

```text
python scripts/run_revision_checks.py
```

이 명령은 원문·문헌·내용 범위 검사, 수학 모형 검산, 포털 데이터와 분석 문서 생성, 목표 연결 감사, JavaScript 구문 및 화면 모델 검사를 묶어서 실행한다. 중간 단계가 실패하면 이후 단계도 중단한다.

이 과정에서 `analyses/`, 일부 `docs/`, `data/` 보고서, 포털 `dist/`, Sites 작업 폴더의 `research/` 사본이 갱신된다. 커밋 전에는 변경 목록을 검토한다. 생성 작업과 동일 원장 수정을 동시에 수행하지 않는다. 이 명령의 통과는 실제 브라우저의 시각적 확인이나 독립적인 교육 내용 검증을 대신하지 않는다.

자료만 다시 만들 때는 다음 명령을 사용한다.

```text
python scripts/build_portal_data.py
node scripts/version_portal_assets.mjs
```

첫 명령의 기본 출력은 `tmp/pathways-release/dist/`이며, 루트 이름이 `research`이면 상위 저장소의 `dist/`다. `MATH_ATLAS_DIST` 환경 변수로 데이터 출력 위치를 지정할 수 있지만, 해당 경로에 앱 HTML·JS·CSS를 자동 복사하지 않는다. 두 번째 명령과 다른 통합 검사는 이 환경 변수 대신 기존 작업 경로를 사용하므로 환경 변수 하나로 전체 빌드 위치가 변경되는 것은 아니다.

`build_task_pathways.py`는 다른 생성기에서 호출하는 `build(site)` 함수다. 파일을 직접 실행하는 것만으로 과제 데이터가 생성되지 않는다. `build_concept_pathways.py`를 단독으로 실행할 때는 실제 사이트 경로를 명시한다.

```text
python scripts/build_concept_pathways.py --site-dir tmp/pathways-release
```

## 실행 후 확인

자동 검사 후 목록에서 초등·중학교·고등학교를 각각 선택하고 성취기준 상세, 목표별 출발 조건·후속 활용, 과제별 조건, CSV 내려받기를 확인한다. 브라우저에서 오래된 탭을 사용하고 있다면 새로고침하고 현재 카탈로그 버전과 색인 참조가 일치하는지 확인한다.

검사 결과에는 실행 날짜, 명령, 종료 결과와 대상 버전을 남긴다. 로컬 생성 버전, Git 커밋, Sites 저장 버전, 실제 공개 버전은 별개이므로 공개 기록이 없는 로컬 변경을 배포 완료로 기록하지 않는다.

## GitHub 스냅샷 갱신

`scripts/export_portal_snapshot.py`는 기존 `tmp/pathways-release`에서 현재 색인의 참조를 따라 앱·자료·검사를 새로운 출력 폴더로 복사한다. 기존 출력 폴더를 자동 덮어쓰지 않으므로, 다시 내보낼 때는 별도의 새 목적지를 사용하고 검사 후 필요한 파일을 반영한다. 옵션은 다음 명령으로 확인한다.

```text
python scripts/export_portal_snapshot.py --help
```

이 도구는 수정한 원장으로 포털을 재생성하지 않는다. 데이터 편집 후에는 원본 저술 환경에서 생성·검증을 먼저 끝내고 스냅샷을 갱신한다. `site/dist/`에서 직접 수정한 앱 코드도 원본에 반영한 뒤 새 목적지로 내보낸다. 검토한 `dist/`, `tests/`와 그에 대응하는 `snapshot.json`을 함께 반영하고 `python scripts/export_portal_snapshot.py --verify`와 관련 Node 검사를 통과해야 갱신이 끝난다. 파일만 수정하고 예전 해시 목록을 남기면 CI가 실패한다. 스냅샷 출력 이후에도 자동으로 GitHub push나 Sites 재배포를 수행하지 않는다.

스냅샷의 `source_commit`은 원본 작업본이 깨끗한 경우에만 기록한다. 미커밋 변경이 있으면 `source_commit=null`로 두고 `source_base_commit`과 `source_worktree_clean=false`를 기록한다. 이 경우 실제 복사 범위는 파일별 SHA256으로 확인하며, 기준 커밋의 파일과 모두 같다고 주장하지 않는다.

### GitHub용 교육과정 탐색기 빌드

저장소 루트에서 실행한다. 마지막 명령의 출력 폴더는 아직 존재하지 않는 경로를 사용한다.

```text
npm --prefix site/frontend ci
npm --prefix site/frontend run build
python scripts/export_portal_snapshot.py --frontend tmp/curriculum-explorer-build --output tmp/curriculum-explorer-review
python scripts/export_portal_snapshot.py --verify --output tmp/curriculum-explorer-review
```

`--frontend`는 React 진입점과 번들을 추가한다. 기존 전체 상세와 연구 도구는 `legacy.html`에서 열고, 공식 내용 체계 색인은 두 원장에서 생성한다. 연결망·목표·과제·자료 안내·분포 탐구·탐구 기록지의 공통 탐색과 스타일은 `site/frontend/compat/`에서 수정한다. `atlas-tokens.css`와 `atlas-page.css`의 색·글꼴·페이지 제목 컴포넌트는 React 화면과 기존 화면에 함께 적용한다. 검사한 새 스냅샷의 `dist/`, `tests/`, `snapshot.json`을 함께 반영한다. Sites와 GitHub Pages의 공개 콘텐츠 판본은 각 환경의 게시 기록을 기준으로 확인한다.
