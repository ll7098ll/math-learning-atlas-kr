# 기여 안내

성취기준의 수학적 의미, 과제 조건, 문헌 근거와 구현을 함께 검토하는 연구 프로젝트다. 먼저 [README](README.md), [분석 규칙](docs/분석규칙.md), [개발 안내](docs/DEVELOPMENT.md)를 읽는다.

## 수정 위치

| 수정 내용 | 우선 확인할 원본 |
|---|---|
| 교육과정 원문 표시 오류 | `data/standards.json`, `data/source_corrections.json`와 해당 PDF 쪽 |
| 성취기준 상세 분석 | `data/revisions_*.json`, `data/analysis_details.json`, `data/secondary_analysis_details.json` |
| 하위 목표·과제·조건·대안 경로 | `data/goal_hierarchy_*.json` |
| 관계의 의미·방향·적용 범위 | `data/relations.json`, `data/revised_relations.json`와 관계 검토 원장 |
| 문헌 근거·읽기 범위 | `data/sources.json`, `data/literature_claim_reviews.json`, `data/literature_evidence/`의 검토 노트 |
| 포털 화면 | 탐색기의 `site/frontend/`와 기존 포털 소스. 생성한 스냅샷은 `site/dist/`에서 확인한다. [구조 안내](docs/ARCHITECTURE.md) |

생성된 Markdown만 수정하면 다음 생성 때 사라질 수 있다. 생성 경로를 먼저 확인하고 원본과 표시 결과를 함께 고친다. `author_*`, `record_*`, `--freeze-content`와 같은 원고 작성·기록 명령은 전체 갱신 명령으로 일괄 실행하지 않는다.

## 내용 수정에 필요한 정보

1. 성취기준 코드, 관계 ID 또는 과제 ID와 문제가 있는 문장을 적는다.
2. 수정안과 적용 조건을 적는다. 반례가 있다면 조건을 포함한 최소 예를 제시한다.
3. 원문 출처, 확인한 쪽·절, 직접 읽은 범위와 확인하지 못한 범위를 구분한다.
4. 영향을 받는 JSON, 분석 문서, 색인과 검토 상태를 확인한다.
5. 해당 변경을 확인하는 검사와 실제 실행 결과를 PR에 남긴다.

수학적 연결, 특정 과제의 선수 조건, 수업 순서와 학생에게 확인된 학습 경로는 서로 다른 주장이다. AND 조건과 대안 경로를 합치지 않는다. 자동 검사를 통과했다는 이유로 독립 검토 또는 학생 반응 검증 상태를 올리지 않는다. 검토 당시 대상의 해시가 달라졌다면 기존 검토의 유효 범위를 다시 확인한다.

## 검증

파일과 명령의 전체 목록은 [개발 안내](docs/DEVELOPMENT.md)에 있다. 공개 저장소에 포함되는 자료만으로 실행할 수 있는 검사의 예는 다음과 같다.

```text
python scripts/check_repository.py
python scripts/export_portal_snapshot.py --verify
python scripts/test_goal_hierarchy.py
python scripts/test_hierarchy_review.py
python scripts/test_general_math_models.py
python scripts/test_advanced_math_models.py
python scripts/test_content_completion.py
```

원문 PDF, 페이지 이미지, 로컬 다운로드와 기존 별도 포털 저장소는 기본 업로드 대상에서 제외한다. 공개 저장소의 `site/` 스냅샷은 별도 설치 없이 실행할 수 있다. 다만 공개 저장소를 새로 복제한 환경에서 `validate_project.py`나 모든 연구 테스트를 한 번에 실행하면 필요한 증거 파일이 없어 실패할 수 있다. 전체 검사는 해당 원문을 정당하게 확보하고 기록된 SHA256과 일치하는지 확인한 환경에서 수행한다. 제외된 자료를 검사 통과 목적으로 임의의 사본이나 더미 파일로 대체하지 않는다.

## PR에 포함할 내용

- 문제와 수정 후 동작 또는 문장
- 영향을 받는 성취기준·과제·관계와 근거
- 수행한 검사, 결과와 수행하지 못한 검사의 이유
- 생성물 변경 여부와 검토 이력 처리

학생 이름, 학교·학급을 식별할 수 있는 응답 원본, 접근 토큰과 인증 파일은 올리지 않는다. 출처의 저작권과 이용 조건을 유지한다. 현재 저장소 전체에 적용하는 라이선스는 확정하지 않았으며, 임의의 오픈소스 라이선스로 제3자 자료까지 재허락하지 않는다. 공개 범위는 [GitHub 준비 안내](docs/GITHUB.md)에서 확인한다.

