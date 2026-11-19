# 초중고 수학 사고 분석과 연결 연구

[![Repository checks](https://github.com/ll7098ll/math-learning-atlas-kr/actions/workflows/checks.yml/badge.svg?branch=main)](https://github.com/ll7098ll/math-learning-atlas-kr/actions/workflows/checks.yml)

[GitHub Pages에서 포털 열기](https://ll7098ll.github.io/math-learning-atlas-kr/) · [GitHub 공개 저장소](https://github.com/ll7098ll/math-learning-atlas-kr) · [자동 검사와 배포 기록](https://github.com/ll7098ll/math-learning-atlas-kr/actions/workflows/checks.yml)

교육부 고시 제2022-33호 수학과 교육과정을 바탕으로 **435개 성취기준**의 수학적 의미, 세부 사고, 진단 과제와 학교급 사이의 연결을 탐색하는 연구 자료와 정적 웹 포털입니다.

공식 교육과정 문장, 자체 분석, 문헌에서 뒷받침하는 범위, 실제 검증 결과를 구별합니다. 화살표는 해당 목표·과제의 조건을 나타내며 모든 학생에게 적용되는 필수 학습 순서나 학습 완료 판정은 아닙니다.

## 현재 버전 — 2026년 11월 19일

| 구분 | 확인된 상태 |
|---|---|
| 이 저장소의 포털 스냅샷 | `908d62e6b7884436` |
| 기존 Sites 공개본 | v113 · `908d62e6b7884436` · 2026-11-19 13:19 KST |
| GitHub Pages | `main`의 검사를 통과한 `site/dist/` 자동 배포 |
| 교육과정 기준 | 제공된 고시 제2022-33호 PDF. 후속 교육과정 개정 여부를 확인했다는 뜻은 아님 |
| 연구 검증 | 자체 점검·구조 검사 기록 있음. 실제 독립 검토 0건, 학생 반응 검증 0건 |

[기존 Sites 포털](https://math-learning-atlas-kr.gptpro2908176.chatgpt.site) · [저장소 상태와 근거](docs/STATUS.md) · [변경 기록](CHANGELOG.md)

최근 업데이트에서는 High 5s 효과 논문과 MDRC 관찰 도구를 대조해 성취기준 해설과 관찰 과제를 보강했습니다. 현재 원장에는 문헌 주장 1,073건과 문헌 기반 관찰 과제 1,246개가 있습니다. [변경 범위와 근거](docs/STATUS.md#가장-최근의-내용-변경)

포털 수정사항을 배포하려면 `site/dist/`와 그에 대응하는 `site/snapshot.json`을 함께 갱신해 `main`에 올립니다. GitHub Actions가 검사를 거쳐 배포합니다. [갱신 절차](docs/GITHUB.md#github-pages-자동-배포)

## 무엇을 볼 수 있나요?

- 학교급 → 학년군·과목 → 영역별 성취기준 검색과 435개 상세 분석
- 870개 하위 목표의 출발 조건, 후속 활용, 대안 경로와 전체 AND 조건
- 571개 명시적 과제의 설명, 진단 질문, 기대 수행과 적용 범위
- 46개 개념군과 2,239개 성취기준 간 관계
- 원문 대조, 문헌 주장별 근거와 미검증 항목을 구분한 연구 기록

명시적 과제 571개에는 현재 설계 570개와 보존한 이전 설계 1개가 포함됩니다. 목표 연결망에서는 565개 과제, 626개 경로, 1,481개 목표 쌍을 탐색할 수 있습니다. 문헌 기반 관찰 과제는 별도 원장에서 관리합니다.

## 먼저 읽기

| 목적 | 문서 |
|---|---|
| 전체 문서 찾기 | [문서 안내](docs/README.md) |
| 최신 수치·완료 조건 확인 | [현재 상태](docs/STATUS.md), [전체 자료 보완 진행](docs/전체자료보완진행.md) |
| 연구 원칙 이해 | [연구 계획](docs/연구계획.md), [분석 규칙](docs/분석규칙.md), [분석 양식](docs/성취기준분석양식.md) |
| 교육과정·분석 탐색 | [초등학교](indexes/초등학교성취기준.md), [중학교](indexes/중학교성취기준.md), [고등학교](indexes/고등학교성취기준.md) |
| 개발·검증 | [개발 안내](docs/DEVELOPMENT.md), [구조](docs/ARCHITECTURE.md), [데이터 안내](docs/DATA.md) |
| GitHub 업로드 | [업로드 절차](docs/GITHUB.md), [기여 방법](CONTRIBUTING.md), [자료 이용·권리](docs/RIGHTS.md) |
| 앞으로 할 작업 | [정비 계획과 후속 과제](docs/ROADMAP.md) |

## 로컬에서 포털 실행

Python 3가 설치된 환경에서 저장소 루트에서 실행합니다. 포털 보기에는 Python 외 패키지나 Node.js 설치가 필요하지 않습니다.

```sh
python -m http.server 8000 --bind 127.0.0.1 --directory site/dist
```

브라우저에서 <http://127.0.0.1:8000>을 엽니다. `index.html`을 파일로 직접 열면 JSON 자료 요청이 실패할 수 있습니다. 서버는 터미널에서 `Ctrl+C`로 종료합니다.

GitHub Pages의 원문 링크는 기존 공개 포털의 PDF를 엽니다. 로컬에서 원문 PDF를 열려면 파일을 별도로 준비합니다. 원문 확보 위치와 해시는 [자료 이용·권리](docs/RIGHTS.md)를 참고하세요.

## 저장소 구조

```text
README.md               프로젝트 입구
CHANGELOG.md            근거가 확인된 변경 기록
CONTRIBUTING.md          수정·기여·검증 절차
SECURITY.md              민감정보 및 취약점 제보 안내
docs/                   연구·개발·운영 문서
indexes/                학교급·분석·연결 색인
analyses/               435개 상세 분석과 통합 사례
data/                   편집 원본, 검토 원장, 출처, 검증 결과
scripts/                생성기, 검산, 감사와 저장소 검사
site/frontend/          교육과정 탐색기와 공통 화면 스타일의 소스
site/dist/              실행 가능한 포털과 현재 콘텐츠
site/tests/             포털 모델 검사
site/snapshot.json      스냅샷 버전·파일 해시·복사 범위
.github/                CI, 이슈·PR 양식
```

기존 작업 폴더의 `tmp/pathways-release/`와 `portal/` 아래 과거 사이트들은 별도 Git 이력을 가진 로컬 작업본입니다. 이 저장소에는 임시 아카이브나 중첩 Git 저장소를 넣지 않고 최신 포털을 `site/`로 복사했습니다. 원래 작업본을 수정하거나 삭제하지 않았습니다.

## 검사와 갱신

검증에 사용한 환경은 Python 3.12.14, Node.js 24.14.0입니다. 연구 스크립트의 PDF·이미지 처리가 필요하면 다음 의존성을 설치합니다. 고정 버전은 재현 환경이며 최신 패키지 버전이라는 의미는 아닙니다.

```sh
python -m pip install -r requirements.txt
python scripts/check_repository.py
python scripts/export_portal_snapshot.py --verify
node site/tests/test_content_objects.mjs
node site/tests/test_goal_network.mjs
node site/tests/test_catalog_groups.mjs
```

자료의 편집 원본은 `data/revisions_*.json`, 목표·조건은 `data/goal_hierarchy_*.json`입니다. 생성된 상세 문서나 해시 파일만 수정하면 다음 생성에서 덮어써질 수 있습니다.

`scripts/run_revision_checks.py`는 원문 자료와 기존 배포 작업본을 사용하는 전체 재생성 명령입니다. GitHub에서 새로 받은 공개 파일만으로 이 명령의 모든 검사를 수행할 수 있는 것은 아닙니다. 필요한 파일, 생성 순서와 검사 범위는 [개발 안내](docs/DEVELOPMENT.md)에 정리했습니다. 일반적인 저장소 점검과 CI는 위 명령을 사용합니다.

## 이용·기여

현재 자체 코드·문서 전체에 적용할 공개 라이선스는 아직 정하지 않았습니다. 외부 문헌과 교육과정의 권리도 각각 구분합니다. 저장소 공개를 재배포·상업적 이용 허가로 해석하지 말고 [자료 이용·권리](docs/RIGHTS.md)를 확인하세요.

내용 오류에는 성취기준 코드, 원문 쪽수, 재현 가능한 반례와 출처를 함께 제시해 주세요. [기여 방법](CONTRIBUTING.md)과 이슈 양식을 사용할 수 있습니다. 실제 학생 자료나 비밀값은 공개 이슈에 넣지 않습니다.
