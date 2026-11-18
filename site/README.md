# GitHub용 포털 스냅샷

콘텐츠 버전: `c7e86e2fa1af547e`. 원본 소스 커밋과 파일별 SHA256은 [snapshot.json](snapshot.json)에 기록했습니다.

저장소 루트에서 실행합니다.

```sh
python -m http.server 8000 --bind 127.0.0.1 --directory site/dist
python scripts/export_portal_snapshot.py --verify
node site/tests/test_goal_network.mjs
```

`dist/`는 현재 색인이 참조하는 파일만 포함합니다. 기존 Sites 저장 버전의 복원 아카이브, `.openai/` 설정과 Git 이력은 포함하지 않습니다. 원문 PDF는 Git 제외 대상이며 로컬에만 존재할 수 있습니다.

`tests/`의 연구 자료 참조 경로는 상위 저장소의 `data/`와 `scripts/`를 가리키도록 조정했습니다. 포털 HTML·CSS·JavaScript·JSON은 원본 작업본의 바이트를 유지했습니다.

앱이나 자료를 바꾸면 기존 스냅샷 해시는 달라집니다. 원본 작업 환경에 변경을 반영하고 관련 생성·검사를 마친 뒤 새 목적지로 추출하여 비교·반영합니다. 해시 검증 실패를 피하려고 검사를 끄지 않습니다. [개발·갱신 절차](../docs/DEVELOPMENT.md), [자료 공개 범위](../docs/RIGHTS.md)를 따릅니다.
