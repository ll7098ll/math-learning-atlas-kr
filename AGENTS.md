# 저장소 작업 안내

## 작업 전

- `README.md`, `docs/STATUS.md`, `docs/DEVELOPMENT.md`를 먼저 읽는다.
- 최신 로컬 콘텐츠 버전, 마지막 공개 배포, 이번 수정의 검증 범위를 구별한다.
- `tmp/`에는 큰 아카이브와 별도 Git 작업본이 있으므로 전역 재귀 검색을 피하고 명시한 폴더에서 검색한다.

## 원본과 생성물

- 현재 상세 원고는 `data/revisions_*.json`, 목표·과제는 `data/goal_hierarchy_*.json`에서 수정한다.
- `analyses/`, 생성 색인, `site/dist/content/`의 해시 파일만 수정하여 원본과 다르게 만들지 않는다.
- 이전 작성기·일회성 정정기를 일괄 실행하지 않는다. `run_revision_checks.py`도 생성물을 갱신하는 명령이다.
- `site/`는 GitHub용 현재 실행 스냅샷이다. 기존 Sites 작업본과 배포 이력을 덮어쓰지 않는다.

## 의미와 근거

- 공식 문구, 자체 분석, 문헌 주장, 독립 검토, 학생 검증을 구별한다.
- AND 조건·대안 경로·적용 목표·범위를 유지하고 모든 연결을 보편적인 필수 선수 관계로 바꾸지 않는다.
- 가상·모형 계산·공개 관측 자료를 구별한다. 기존 검토·수정 이력을 보존한다.

## 확인과 제출

- 문서·설정 변경은 `python scripts/check_repository.py`로 확인한다.
- 스냅샷은 `python scripts/export_portal_snapshot.py --verify`와 관련 `site/tests/*.mjs`로 검사한다.
- 검증 날짜·대상·결과와 미실행 범위를 정확히 기록한다. 이전 검사 기록을 새 검사 결과로 제시하지 않는다.
- 사용자 요청 범위 안에서 진행하되 비밀값·원문 파일·개인정보를 공개 Git 이력에 넣지 않는다. 파일별 기본 공개 범위는 `docs/RIGHTS.md`를 따른다.
