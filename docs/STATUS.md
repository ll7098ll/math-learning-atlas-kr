# 현재 상태와 버전

확인 기준일: **2026년 11월 18일(KST)**. 이 문서는 작업 폴더의 원장·생성 데이터·검사 결과·기존 게시 기록을 대조한 요약이다. 웹사이트에 새로 접속해 응답을 확인한 기록은 아니며, 여기의 ‘최신’은 이 저장소에서 확인한 작업본을 뜻한다. 교육과정 후속 개정까지 조사했다는 의미는 아니다.

## 로컬 작업본과 공개 사이트

| 구분 | 현재 확인한 값 | 근거 |
|---|---|---|
| 로컬 내용 버전 | `c7e86e2fa1af547e` | [검사 결과](../data/revision_checks.json) |
| 로컬 과제 데이터셋 | `1eb09e3dfdcd4f6d` | [목표 연결 감사](../data/goal_network_audit.json) |
| 로컬 개념군 데이터셋 | `c40bf927e329ac5a` | [전체 위계 감사](../data/hierarchy_completion_audit.json) |
| 가장 최근의 성공 게시 기록 | Sites 버전 **91**, 내용 `c7e86e2fa1af547e` | [게시 원장](../data/school_revision_deployment.json) |
| v91 게시 시각 | 2026-11-18 13:37:21 KST | 같은 게시 원장; 원기록 `2026-11-18T04:37:21.247243+00:00` |
| v91 소스 커밋 | `e9f10e511c88b6c0c55daafa0868cab001461060` | [v91 게시 결과](../data/site_publication_c7e86e2fa1af547e.json) |
| GitHub 업로드 | 공개 저장소 생성·`main` 최초 업로드 완료 | [공개 저장소](https://github.com/ll7098ll/math-learning-atlas-kr) |
| GitHub 최초 커밋 | `22c681bc0f522c994d2c9e3189edf9516f97c0da` · 2,751개 파일 | [최초 커밋](https://github.com/ll7098ll/math-learning-atlas-kr/commit/22c681bc0f522c994d2c9e3189edf9516f97c0da) |
| GitHub 자동 검사 | 최초 커밋 `22c681b`의 전체 단계 성공 | [확인한 Actions 실행](https://github.com/ll7098ll/math-learning-atlas-kr/actions/runs/44239839367) |
| GitHub Pages | 이 저장소의 스냅샷 `c7e86e2fa1af547e` · `main`에서 검사 후 자동 배포 | [포털 열기](https://ll7098ll.github.io/math-learning-atlas-kr/) · [배포 기록](https://github.com/ll7098ll/math-learning-atlas-kr/actions/workflows/checks.yml) |

**최신 게시 원장에서는 로컬과 공개 내용 버전이 `c7e86e2fa1af547e`로 일치한다.** [보완 결과 원장](../data/content_completion_result_2026-11-04.json)의 `latest_publication_attempt`는 `succeeded`이고, `source_pushed`, `saved_version_created`, `deployed`가 모두 `true`다. 이번 문서 정비는 별도로 갱신된 성공 기록을 확인해 반영했으며, 이 문서 작업에서 사이트를 새로 배포한 것은 아니다.

[전체 위계 감사](../data/hierarchy_completion_audit.json)의 `deployment_matches_working_source=false`는 **v91 게시 전인 13:33:11 KST에 생성한 감사**에 남아 있는 값이다. 구조 검사 당시에는 공개 v90과 달랐고, 그 뒤 13:37:21 KST의 게시 기록이 추가됐다. 이 시점 차이를 보존하며, 현재 배포 판정에는 더 최신인 v91 게시 원장을 사용한다. 검사 통과나 GitHub 업로드만으로 별도 Sites 게시를 추정하지 않는다.

공개 주소는 [수학의 연결 지도](https://math-learning-atlas-kr.gptpro2908176.chatgpt.site)다. Sites 버전 번호는 해당 서비스의 저장 이력이며, 별도의 소프트웨어 배포 버전 번호를 새로 부여한 것은 아니다.

## 분석 범위와 현재 집계

기준 문서는 교육부 고시 제2022-33호 수학과 교육과정이다. [성취기준 원장](../data/standards.json)에 기준 파일명, 263쪽, SHA256을 기록했다. 이후 다른 교육과정 판본을 사용하려면 버전과 대응 관계를 별도로 관리해야 한다.

| 지표 | 현재 수 | 집계 원장과 의미 |
|---|---:|---|
| 성취기준·상세 분석 초안 | 435 | [성취기준](../data/standards.json), [분석 상태](../data/analysis_registry.json); 초등 121·중학교 60·고등학교 254 |
| 고등학교 과목 | 15 | [프로젝트 검사](../data/project_validation.json) |
| 하위 목표 | 870 | [과제 범위](../data/task_pathway_coverage.json) |
| 명시적 과제 | 571 | 같은 원장; 현재 설계 570·이전 설계 보존 1 |
| 목표 연결의 과제·경로·방향쌍 | 565·626·1,481 | [목표 연결 감사](../data/goal_network_audit.json); 위의 전체 과제 수와 집계 범위가 다름 |
| 연구용 개념군 | 46 | [전체 위계 감사](../data/hierarchy_completion_audit.json) |
| 보강 관계 전체 | 4,373 | [현재 관계 원장](../data/revised_relations.json) |
| 성취기준 사이의 관계 | 2,239 | [전체 위계 감사](../data/hierarchy_completion_audit.json); 개별 사고 요소를 양 끝으로 갖는 관계는 제외 |
| 전체 출처 | 176 | [출처 원장](../data/sources.json); 기준 교육과정 포함 |
| 교육과정 외 문헌의 범위별 주장 대응 | 출처 175·주장 1,053 | [문헌 주장 원장](../data/literature_claim_reviews.json) |
| 문헌 기반 추가 관찰·자체 과제 | 1,236 | [보완 결과 원장](../data/content_completion_result_2026-11-04.json)의 `literature_observation_extensions`; 명시적 과제 571과 별도 집계 |
| 문헌과 관계의 범위별 해석 | 874 | [관계 문헌 원장](../data/relation_literature_reviews.json); 대상 관계 389개 |
| 문헌 주장에 최소 한 범위가 연결된 기준 | 435/435 | [연결 범위](../data/literature_mapping_coverage_2026-11-13.json); 기준 전체의 문헌 검증 완료 수가 아님 |
| 공식 내용 체계 항목 자체 의미 대조 | 571/571 | [보완 결과 원장](../data/content_completion_result_2026-11-04.json) |
| 성취기준 원문 이미지 자체 대조 | 435/435 | [원문 이미지 대조 범위](원문이미지대조범위.md) |

[이전 관계 원장](../data/relations.json)의 3,652개는 [현재 보강 관계](../data/revised_relations.json)의 4,373개와 다른 집계다. `project_validation.json`은 이전 관계 원장을 검사하므로 두 수치를 섞지 않는다. 공식 내용 항목 571개, 명시적 과제 571개도 우연히 수가 같을 뿐 서로 다른 대상을 센 것이다.

## 가장 최근의 내용 변경

로컬 버전 `c7e86e2fa1af547e`에는 Xin·Jitendra·Deatline-Buchman(2005)의 비례 문장제 원연구 대조를 반영했다. 공개 사본의 논문 181–192쪽 전체 12쪽과 표 3개·그림 2개를 확인한 기록이며, 출처 1개·주장 3건·자체 과제 4건·관계 해석 11건을 더했다. 기존 출처 174개·주장 1,050건·과제 1,232건·해석 863건의 보존 여부를 함께 기록했다.

시작 표본 22명, 네 시점 완료 19명, 학습장애 완료 표본 16명을 구별하고, 시점별 지원·부분점수·지연 검사 전 전략 복습·인쇄 186쪽 수량 대응을 보완했다. 이는 국내 학생 효과나 특정 도식의 단독 효과를 입증한 결과가 아니다. 자세한 범위와 제한은 [원논문 대조 기록](../data/literature_evidence/XIN_JITENDRA_DEATLINE_BUCHMAN_2005_review_notes.json)과 [전체 자료 보완 진행](전체자료보완진행.md)에 있다.

v91 게시 결과는 이 원연구 보완에 관련된 성취기준 7개와 공개 리소스 84개의 HTTP 바이트 대조를 기록한다. 이전 v90에는 IES 분수 지도 가이드 90쪽·검토 프로토콜 8쪽 판면 대조가 반영되어 있으며, 당시 성취기준 18개·공개 리소스 117개 대조가 기록되어 있다. 두 게시 모두 실제 브라우저 화면 검증은 미완료로 남긴다. 이번 문서 정비에서 공개 응답을 다시 확인한 것은 아니다.

## 검사로 확인한 범위

[프로젝트 검사](../data/project_validation.json), [보강 원장 검사](../data/revision_quality.json), [통합 검사](../data/revision_checks.json)는 저장된 기록상 `pass`다. 이 문서의 상태 확인은 기존 결과를 대조한 것이며, 이번 문서 작성만으로 모든 검사를 새로 실행했다고 주장하지 않는다. 실제 재실행 방법은 [개발 안내](DEVELOPMENT.md)를 따른다.

통합 검사는 필수 필드·출처 참조·JavaScript 문법·네트워크 모델·과제의 전체 AND 조건·개념군 탐색·학교급 범위·12절 상세 문서 구조 등을 다룬다. [목표 연결 감사](../data/goal_network_audit.json)는 원장과 출력의 일치 및 목표 조건의 무순환을 확인한다. 이 검사는 관계의 보편적 선수성이나 모든 학생에게 맞는 학습 순서를 증명하지 않는다.

## 아직 완료되지 않은 연구와 확인

[후속 완료 감사](../data/post_mapping_completion_audit_2026-11-16.json)는 `full_objective_complete=false`다. 최소 문헌 연결 대기 0건이나 자체 검사 통과를 전체 연구 완료로 바꾸지 않는다.

| 남은 범위 | 현재 상태 |
|---|---|
| 교수설계 7판 국제판의 정식 전체 판면·그림·표·정오표와 인용 원연구 | 후속 대조 필요 |
| 별도 9판의 미확보 인쇄 71–405쪽 335쪽과 공식판 동일성 | 미완료 |
| 출처별 선정 범위 밖 본문·원연구·판본·번역 | 개별 출처의 후속 검토 범위를 유지 |
| 실제 외부 독립 검토 | 0건 |
| 익명화한 실제 학생 응답과 수정 후 재확인 | 0건 |
| 기록지·분포 도구의 실제 브라우저·인쇄·모바일 시각 확인 | 미확인 |

검토 단위와 근거 기록 양식은 [독립 검토와 학생 검증 목록](독립검토와학생검증목록.md), 문헌별 읽은 범위와 남은 범위는 [문헌 주장별 근거](문헌주장별근거.md)와 [미확보 원문 목록](미확보원문목록.md)을 따른다.

## 기록을 갱신할 때

- 원본 원장을 고치고 관련 생성·검사를 완료한 뒤 이 문서의 수치와 버전을 갱신한다. 검사 실패나 미실행을 완료로 표시하지 않는다.
- 공개 버전은 게시 성공·해당 자료 확인을 뒷받침하는 기록이 있을 때 갱신한다. 로컬 작업 버전과 공개 버전을 각각 남긴다.
- `2026-11-04`, `2026-11-13`처럼 날짜가 붙은 일부 원장과 문서는 이후에도 누적 갱신된다. 파일명만으로 내용의 최신 날짜를 판단하지 않고 내부 날짜·버전·상태를 확인한다.
- [정적 자산 보존 계획](../data/portal_asset_retention.json)의 현재 범위는 작업본과 최근 저장 버전 2개(v91·v90)다. 이 파일은 계획이며, 실제 이동 이력은 [별도 원장](../data/portal_asset_archive_history.json)에 기록한다.
- 큰 연구 기록의 과거 수치·당시 판단은 이력으로 보존하고, 현재 읽을 요약은 이 문서와 [변경 이력](../CHANGELOG.md)에 둔다.
