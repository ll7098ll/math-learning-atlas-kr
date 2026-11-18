"""Register a scoped comparison of kindergarten counting and number-line training."""
from extend_lt2_length_assets_review import load, write
from literature_review import ROOT, build_report, load_registry
from record_direct_learning_trajectory_trials import register, verify_pdf


PDF = 'https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2018.00975/pdf'
SPEC = dict(
    id='FRISO_VAN_DEN_BOS_ET_AL_2018_COUNTING_NUMBER_LINE',
    year=2018,
    title='Counting and Number Line Trainings in Kindergarten: Effects on Arithmetic Performance and Number Sense',
    authors=['Friso-van den Bos, I.', 'Kroesbergen, E. H.', 'Van Luit, J. E. H.'],
    authors_year='Friso-van den Bos 외, 2018',
    doi='https://doi.org/10.3389/fpsyg.2018.00975', url=PDF,
    publisher=PDF.removesuffix('/pdf') + '/full',
    file='friso-2018-counting-number-line',
    sha256='6f28b4a58f4a990ff2e050208ca5c5c06d90bee4c33e1f179e7097b0397c6eac',
    pdf_pages=11, printed_pages='1–11', text_pages=[1, 3, 4, 5, 6, 7, 8, 9, 11], visual_pages=[6, 7, 8],
    kind='초기 수 개념 지도 조건의 준실험 비교', causal_effect_established=False,
    design='사전 세기·연산 점수를 맞춘 세 조건의 준실험. 시점, 아동, 지도 소집단의 3수준 모형.',
    sample='네덜란드 유치원 90명 참여, 여러 변인에서 이상치를 보인 1명 제외. 평균 5세 8개월.',
    scope='출판판 초록, 표본·수업·도구·분석·표 2와 3·사후 비교·한계·이용 조건의 9쪽과 선정 판면 3쪽을 대조했다.',
    limit='정규 수업 대비 결과와 두 활동군 직접 비교를 구분한다. 무작위 배정, 장기 추적, 개별 게임 효과, 국내 성취기준 달성은 확인하지 않았다.',
    next_review='활동지·문항 전체와 아동별 원자료를 확보해 각 게임의 기여와 결과 민감도를 확인할 범위다.',
    supports='세기·수직선 두 활동의 과제 구성, 정규 수업 대비 단기 결과와 직접 비교, 평가 도구의 차이.',
    checks={
        3: ('Ninety Dutch kindergartners', 'Data of one child', 'three children from each class'),
        4: ('16 addition problems', 'maximum (100)', 'squared correlation'),
        5: ('Post hoc tests indicated', '0.11', 'Benjamini'),
        6: ('0.25', '0.45', 'explained variance'),
        7: ('2 .04', '0 .16', '1 .69'),
        8: ('were not signiﬁcant', 'number line group'),
        11: ('License (CC BY)',),
    },
    results=dict(
        participants=90, excluded_outlier=1, planned_sessions=12, weeks=6, minutes_per_session_approx=20,
        posttest_after_last_session_weeks_max=2,
        counting_vs_usual_time_interaction_B={'addition': 2.04, 'symbolic_number_line': 0.16, 'ENT_R': 1.69},
        number_line_vs_usual_time_interaction_p={'addition': 0.34, 'symbolic_number_line': 0.08, 'ENT_R': 0.25},
        number_line_vs_counting_post_hoc_p={'addition': 0.11, 'symbolic_number_line': 0.25, 'ENT_R': 0.45},
    ),
    corrections=[
        ('PDF 1·5·6·8쪽', '초록의 세기 접근만 효과적이라는 결론은 두 지도군 직접 비교 결과보다 넓다. 각 비교의 기준군을 구별한다.'),
        ('PDF 4·6쪽', '수직선 결과의 R²는 표시 위치와 목표 위치의 선형 관련이다. 점별 위치 오차의 크기와 별개다.'),
    ],
    claims=[
        ('FCNL-01', ['2수01-01', '2수01-05'], [3, 4, 5],
         '유치원 90명이 참여하고 이상치 1명을 제외했다. 학급마다 세기·수직선·정규 수업 조건에 세 명씩 배치하면서 사전 세기와 연산 점수를 맞췄다. 두 활동군은 6주간 세 명씩 약 20분 수업을 12회 받았다. 세기군은 실물의 개수 세기와 이어 세기를, 수직선군은 수와 위치의 양방향 대응과 수가 적힌 선형 게임을 했다.',
         '복수 활동을 묶은 준실험이다. 개별 게임의 효과와 국내 학생의 활동 순서는 확인하지 않았다.'),
        ('FCNL-02', ['2수01-01', '2수01-05'], [4, 5, 6, 7, 8],
         '정규 수업군 대비 세기 활동군의 증가 차이는 덧셈 정답 수 B=2.04, 기호 수직선 선형 적합도 B=.16, ENT-R 세기 하위검사 B=1.69로 보고됐다. 수직선 활동군의 정규 수업 대비 차이는 유의하지 않았다. 두 활동군 직접 비교도 각각 p=.11, .25, .45로 유의하지 않았다.',
         '덧셈 평가는 합이 20까지인 화면 문항 16개였다. 두 활동의 동등성이나 세기군의 우위, 상황에서 뺄셈의 의미, 장기 유지는 확인하지 않았다.'),
        ('FCNL-03', ['2수01-01', '2수01-03'], [4, 6, 7, 9],
         '기호 수직선 과제는 양 끝 1과 100 사이에서 22개 목표 수의 위치를 표시하게 했다. 평가지표는 표시 위치와 목표 위치 사이 상관의 제곱이었다. 일정한 방향과 비율로 위치를 어긋나게 잡아도 선형 관계가 높게 나올 수 있으므로 실제 발문에서는 기준점, 수의 순서, 위치 오차를 따로 살핀다.',
         '선형 적합도는 위치 오차의 직접 지표가 아니다. 0을 포함한 수직선이나 네 자리 수의 위치 이해를 평가하지 않았다.'),
        ('FCNL-04', ['2수01-03'], [4, 5, 7, 8, 9],
         '기호 크기 비교는 1~9의 두 수를 고르는 별도 과제였다. 숫자와 점 배열 크기 비교에서는 시점에 따른 지도 조건 차이가 유의하지 않았다. 수직선 배치 결과를 크기 비교 향상으로 옮겨 해석할 근거가 없다.',
         '한 자리 수의 제한된 자극과 별도 평가 결과다. 네 자리 수나 자릿값에 따른 크기 비교의 지도 효과는 확인하지 않았다.'),
    ],
)


def main():
    registry = load_registry()
    source_id = SPEC['id']
    if source_id in registry['sources']:
        recorded = {row['id'] for row in registry['claims'] if row['source_id'] == source_id}
        assert recorded == {row[0] for row in SPEC['claims']}
    else:
        bibliography_path = ROOT / 'data/sources.json'
        queue_path = ROOT / 'data/content_review_queue.json'
        bibliography, queue = load(bibliography_path), load(queue_path)
        register(SPEC, verify_pdf(SPEC), bibliography, queue, registry)
        write(bibliography_path, bibliography)
        write(queue_path, queue)
        write(ROOT / 'data/literature_claim_reviews.json', registry)
    build_report()


if __name__ == '__main__':
    main()
