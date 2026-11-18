# 구조와 데이터 흐름

확인 기준일: 2026-11-18. 실행 방법은 [개발 안내](DEVELOPMENT.md), 연구의 해석 원칙은 [분석 규칙](분석규칙.md)을 따른다.

## 구성

이 프로젝트는 교육과정 원문, 연구 원장, 읽기용 Markdown, 정적 웹 포털로 구성된다. 포털은 브라우저의 JavaScript 모듈과 JSON으로 동작하며 서버 데이터베이스나 프런트엔드 번들러를 요구하지 않는다.

| 위치 | 역할 | 편집 기준 |
|---|---|---|
| `[별책8] 수학과 교육과정.pdf` | 기준 교육과정 원문 | 기존 파일을 다른 판본으로 대체하지 않는다. |
| `data/` | 성취기준, 분석, 목표·과제·조건, 출처와 검토 이력 | 의미와 근거를 고치는 주된 위치다. |
| `analyses/` | 성취기준별 상세 분석과 통합 사례 | 대부분 원장에서 재생성된다. 직접 수정 전에 생성기를 확인한다. |
| `indexes/` | 학교급·과목·상세 분석·관계 색인 | 생성 자료와 직접 관리하는 진행 기록을 구분한다. |
| `docs/` | 연구 방법, 결과 보고, 개발·배포 설명 | 각 문서의 날짜와 적용 범위를 함께 읽는다. |
| `scripts/` | 생성기, 내용 검산, 원장 검증, 회귀 검사 | 일반 실행 진입점과 일회성 저술·수정 스크립트를 구분한다. |
| `portal/` | 통계 실험실·탐구 워크북 HTML 원본 | 완성된 포털 전체 앱은 이 두 HTML과 별도로 존재한다. |
| `site/` | GitHub용 현재 포털 스냅샷 | `dist/`에 앱과 현재 참조 데이터, `tests/`에 루트 연구 원장을 참조하는 Node 검사, manifest에 파일 무결성 기록이 있다. |
| `tmp/pathways-release/` | 기존 Sites 작업 저장소, Git 추적 제외 | `dist/`에 포털 앱과 생성 데이터, `tests/`에 Node 검사, `research/`에 연구 원본 사본이 있다. |

`site/`는 최신 로컬 작업 버전의 앱과 현재 색인이 참조하는 파일을 선별한 결과다. `scripts/export_portal_snapshot.py`가 기존 작업 폴더에서 내보내며, Git 이력·Sites 내부 설정·과거 자료 전체를 복사하지 않는다. 재배포하거나 교육과정 내용을 재생성하는 작업도 아니다. 기준 PDF는 이 GitHub 스냅샷에서 제외하므로 PDF 열기 기능은 원문을 별도로 준비해야 한다.

`tmp/pathways-release/`는 기존 개발 경로다. 그 안의 `research/`는 루트 연구 자료의 복사본이며 양쪽을 독립 편집하면 내용이 갈라진다. GitHub에서 받는 `site/`는 원본 작업 폴더의 저장 이력이나 전체 저술 환경을 대체하지 않는다.

## 연구 원장

| 자료 | 책임 |
|---|---|
| `data/standards.json` | 공식 코드, 학교급·학년군·과목·영역, 원문·표시 문장, PDF 쪽수와 기준 PDF의 SHA-256 |
| `data/source_corrections.json` | 원문 대조에 따른 표시 문장 보정과 근거 |
| `data/analysis_registry.json` | 분석 파일 위치, 작성 상태, 학생 반응 검증 여부 |
| `data/analysis_details.json`, `secondary_analysis_details.json` | 초기 초등 추가 분석 및 중고등 분석 |
| `data/revisions_*.json` | 현재 상세 분석의 개별 보강 원본 |
| `data/initial_case_studies.json` | 초기 세 사례의 보존 원고 |
| `data/goal_hierarchy_*.json` | 하위 목표, 대표 과제, 경로, 조건의 출발 능력과 적용 목표 |
| `data/task_route_cases.json` | 과제 화면의 추가 설계 및 보존한 이전 설계 |
| `data/elements.json`, `relations.json` | 사고 요소와 관계 원본 |
| `data/revised_relations.json` | 개별 보강을 적용한 관계 출력 |
| `data/concept_taxonomy.json` | 전체 성취기준의 개념군 분류 |
| `data/sources.json`, `literature_claim_reviews.json` | 출처 목록, 읽은 범위, 주장별 지원 내용과 한계 |
| `data/curriculum_standard_image_reviews.json` | 원문 이미지와 대상 내용의 대조 기록 |
| `data/*review*.json`, `data/*audit*.json` | 개별 검토·감사 기록. 파일별 작성 주체와 검증 범위가 다르다. |

성취기준, 목표, 과제, 경로, 관계는 각각 ID로 연결한다. 조건의 `applies_to_goal_ids`는 해당 조건이 지원하는 목표 범위를 지정한다. 과제의 한 경로에서 함께 필요한 AND 조건을 일부만 떼어 표시하거나 다른 목표의 필수 선수 조건으로 확장하면 원장의 의미가 바뀐다. 의미 연결, 교수 설계 순서, 과제 수행 조건도 서로 바꾸어 해석하지 않는다.

## 생성 흐름

```text
기준 PDF + 보정 기록
  └─ build_inventory.py → standards.json, 학교급별 색인

분석·개별 보강·목표 원장 + Markdown + 출처
  └─ build_portal_data.py
       ├─ detailed_revision.apply → 분석 Markdown, 보강 범위·관계 JSON
       ├─ content/catalog.json → 최초 목록과 검색
       ├─ 성취기준 상세·관계·시범 위계 JSON
       ├─ build_concept_pathways → 개념군 색인·항목·전체 그래프
       ├─ build_task_pathways → 과제 색인·항목·목표 연결 그래프
       └─ 통계 실험실·탐구 워크북 HTML, CSV·계산 도구

앱 JavaScript/CSS + 생성 데이터
  └─ version_portal_assets.mjs → import map과 파일별 캐시 버전
       └─ 정적 HTTP 서버 또는 사이트 배포
```

`build_portal_data.py`는 데이터만 출력하는 함수가 아니다. `detailed_revision.apply` 등을 통해 분석 Markdown과 원장 요약도 갱신한다. 따라서 원장에서 생성된 문서만 고치면 다음 실행에서 수정 내용이 사라질 수 있다.

## 포털 모듈

GitHub 스냅샷의 `site/dist/modules/`를 기준으로 한다. 기존 Sites 작업 저장소에서도 같은 모듈 이름을 사용한다.

| 모듈 | 책임 |
|---|---|
| `catalog.mjs`, `catalog-groups.mjs` | 학교급 → 학년군·과목 → 영역 탐색과 검색 |
| `detail.mjs` | 성취기준 원문·상세 분석 |
| `goal-network.mjs` | 선택 목표의 출발 조건, 후속 활용, 탐색 경로 |
| `task-pathways.mjs` | 과제별 설명·진단과 경로의 전체 조건 |
| `concept-pathways.mjs`, `hierarchy-path-view.mjs` | 개념군 관계와 단계별 탐색 |
| `network-model.mjs`, `network.mjs` | 전체 연결망 모델과 화면 |
| `store.mjs` | 색인 초기화, 필요할 때 데이터 로딩, 중복 요청 공유, 버전 검사 |

목표 연결 자료는 최초 화면에서 전부 내려받지 않는다. 과제 색인의 `goalGraph.hash`가 가리키는 파일을 목표 탐색에 필요할 때 읽는다. 화면의 탐색 이력은 사용자가 살펴본 관계를 나타내며 학습 완료나 AND 조건 충족 판정 자료가 아니다.

## 버전과 보관

포털의 `catalog.version`은 생성 데이터에서 계산한 SHA-256의 앞 16자리다. 배포 날짜, Git 커밋 SHA, Sites 저장 버전 번호와 다른 식별자이며 서로 대신 사용할 수 없다. 과제·개념군 색인은 각각 별도의 `datasetVersion`도 가진다.

`scripts/content_objects.py`는 항목을 일정한 JSON 형식으로 직렬화하고 전체 SHA-256을 파일명으로 사용한다. 위치는 `content/task-pathways/items/<hash>.json` 또는 `content/concept-pathways/items/<hash>.json`이다. 동일 내용은 기존 파일을 재사용하고, 동일 해시 위치의 바이트가 다르면 덮어쓰지 않고 실패한다. 성취기준 관계 자료는 `content/versions/<catalog.version>/`으로 묶인다.

따라서 `catalog.json` 하나만 복사해서는 실행 가능한 배포물이 되지 않는다. 카탈로그, 과제·개념군 색인, 해당 색인이 참조하는 자료, 앱 파일을 함께 다룬다. GitHub의 `site/`는 현재 버전만 담는다. 기존 Sites 작업 환경의 [보관 기록](../data/portal_asset_retention.json)은 작업 중 버전과 최근 저장 버전 2개를 보존 대상으로 기록한다. `plan_portal_retention.py`의 기본 인수는 5개이므로 저장된 정책과 실행 인수를 구별한다. 이 스크립트는 참조와 해시를 점검해 이동 계획을 만들며 직접 파일을 이동하거나 삭제하지 않는다.

## 검증 경계

자동 검사는 코드·참조·개수·해시·경로·수치와 화면 모델의 일관성을 확인한다. 원문 이미지 대조, 자체 수학적 분석, 외부 독립 검토, 학생 반응 검증은 각각 별도의 근거를 요구한다. 자동 검사가 통과했다는 이유로 검토 상태를 상향하지 않는다. 최신 수치와 공개·로컬 버전의 대응은 해당 원장 및 공개 기록에서 확인한다.
