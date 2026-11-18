"""Register the early arithmetic pilot and its larger randomized follow-up."""
from extend_lt2_length_assets_review import load, write
from literature_review import ROOT, build_report, load_registry
from record_direct_learning_trajectory_trials import register, verify_pdf


PILOT = dict(
    id='CLEMENTS_ET_AL_2020_ARITHMETIC_PILOT', year=2020, file='clements-2020-arithmetic-published',
    title='Efficacy of a learning trajectory approach compared to a teach-to-target approach for addition and subtraction',
    authors=['Douglas H. Clements', 'Julie Sarama', 'Arthur J. Baroody', 'Candace Joswick'],
    doi='https://doi.org/10.1007/s11858-019-01122-z',
    url='https://testmoodle.ndna.org.uk/pluginfile.php/120678/mod_resource/content/8/Efficacy_of_Learning_Trajectory_Clements%2C%202020.pdf',
    publisher='https://link.springer.com/article/10.1007/s11858-019-01122-z',
    sha256='fae8dcca766683c1c06766ebe31d63cba426aeb29666aea8fafe67f28f8d6185',
    pdf_pages=12, printed_pages=[637, 648], text_pages=[6, 7, 8, 10], visual_pages=[6, 7, 8],
    scope='출판판 인쇄 642~644·646쪽의 방법·결과·한계를 읽고 표 1·2와 그림 2의 판면을 확인했다. ERIC 저자 원고와 분모를 대조했다.',
    kind='초기 수학 지도 조건의 두 학급 예비 비교',
    sample='영재 프로그램의 유치원 두 학급에서 26명이 참여했고 사전·사후 단계 변화는 순차 13명·건너뛰기 12명으로 집계했다.',
    design='one_classroom_per_condition_arithmetic_pilot',
    causal_effect_established=False,
    limit='조건마다 학급이 하나이므로 학급과 지도 조건을 분리하기 어렵다. 한 학교의 단기 개별 지도 결과를 국내 집단 수업이나 모든 연산 과제에 적용할 수 없다.',
    next_review='별도 출판 부록의 수 범위·과제 분류·개별 판정을 대조한다.',
    supports=['동의·검사 분모와 학급 단위 비교', '수업 중 변화와 독립 사후검사', '상황제의 미지 위치와 수 범위'],
    checks={6: ['180', 'randomly assigned'], 7: ['24 items', '45 add', 'before the completion'], 8: ['Two-level increase', 'Neutral']},
    results=dict(
        initial_by_class=[13, 13], analyzed=[13, 12], minutes_about=180,
        table_2_counts=dict(ordered=[2, 4, 0, 7, 0, 0], skip=[0, 0, 1, 5, 5, 1]),
        table_2_order=['2단계 증가', '1단계 증가', '부분 증가', '유지', '부분 감소', '1단계 감소'],
        pre_post_mean_by_arm=[[.18, .28], [.19, .25]],
        author_manuscript=dict(url='https://files.eric.ed.gov/fulltext/ED619220.pdf', pdf_pages=38,
                               sha256='e7b3f4c47d309ead832bb5343db6b7cd0e62a70adbf29f5828a926f2c4234a2d',
                               selected_text_pages=[2, 15, 16, 18, 19, 20, 26], visual_pdf_pages=[19]),
    ),
    corrections=[
        ('인쇄 643~644쪽 표 1·2', '초기 학급 인원은 13명씩이다. 건너뛰기 학급의 사전검사 완료 전 이탈 1명을 제외한 단계 변화 분모는 12명이다.'),
        ('인쇄 643쪽 표 1 나이 열', '열에는 개월 단위로 표시됐으나 5.4와 5.5가 실렸다. 원자료 없이 나이 단위를 고쳐 인용하지 않는다.'),
        ('인쇄 642·646쪽 연구 설계 설명', '학급 하나를 순차 조건에 무작위 배정했다는 방법과 조건별 학급 하나의 한계를 함께 기록한다. 아동 단위 무작위 실험으로 분류하지 않는다.'),
    ],
    claims=[
        ('LTAP-01', ['2수01-05'], [6, 7, 8, 10],
         '예비 연구는 학급 하나씩을 두 조건에 두었다. 사전·사후 단계 변화에서 순차 지도는 13명 중 6명이 한 단계 이상 올라갔고, 건너뛰기는 12명 중 1명이 부분적으로 올라갔다.',
         '조건별 학급이 하나라 학급과 지도 조건의 차이를 분리하기 어렵다. 순차군의 한 단계 증가와 비교군의 부분 증가는 서로 다른 범주다.'),
        ('LTAP-02', ['2수01-01', '2수01-05'], [7, 8, 10],
         '사전·사후 검사는 세기 24문항과 덧셈·뺄셈 45문항을 구별했다. 수업 중 확인된 단계와 별도 사후검사의 단계가 달랐고, 두 조건의 모든 아동은 하나 이상의 수준 안에서 일부 향상을 보였다.',
         '수업 중 비계가 있는 응답과 독립 검사 응답을 합산할 수 없다. 수준 안의 향상을 다음 수준에 도달한 것으로 판정하지 않는다.'),
        ('LTAP-03', ['2수01-04', '2수01-05', '2수01-06'], [6, 7, 10],
         '비교군은 처음에 높은 수준의 처음 양·부분 미지 과제를 다뤘지만, 후반에는 같은 수준 또는 더 낮은 과제도 받았다. 저자는 일부 검사에서 수가 커지는 변화와 상황의 복잡성이 함께 달라졌음을 보고했다.',
         '자릿수와 미지 위치가 함께 바뀐 문항 결과로 어느 요소가 어려웠는지 분리할 수 없다. 특정 수 범위나 수준을 고정된 선수 요건으로 사용하지 않는다.'),
    ],
)
TRIAL = dict(
    id='CLEMENTS_ET_AL_2021_ARITHMETIC_TRIAL', year=2021, file='clements-2021-arithmetic-accepted',
    title='Comparing the Efficacy of Early Arithmetic Instruction Based on a Learning Trajectory and Teaching-to-a-Target',
    authors=['Douglas H. Clements', 'Julie Sarama', 'Arthur J. Baroody', 'Traci S. Kutaka', 'Pavel Chernyavskiy',
             'Candace Joswick', 'Menglong Cong', 'Ellen Joseph'],
    doi='https://doi.org/10.1037/edu0000633', url='https://files.eric.ed.gov/fulltext/ED619003.pdf',
    publisher='https://psycnet.apa.org/doi/10.1037/edu0000633',
    sha256='685c5866d210d2e0b3a862d63b843bfbdd83097d04a79760d09884c21e19136d',
    pdf_pages=46, printed_pages=[1, 46], pdf_edition='ERIC 공개 저자 원고', journal_issue_pages=[1323, 1337],
    text_pages=[2, 7, 9, 10, 13, 14, 18, 19, 23, 24, 25, 26, 27, 32, 33],
    visual_pages=[9, 10, 25, 26, 27],
    scope='ERIC 저자 원고의 배정·검사·모형·한계 관련 문단과 그림 1·2, 표 2~4를 읽고 선정 판면을 대조했다. 출판사 권호 판면과 별도 부록은 미확보다.',
    method_note='저자 원고의 방법·표·그림과 대상 성취기준의 수행 범위를 대조했다.',
    sample='4개 학교 16교실에서 동의 319명 중 28명이 제외되거나 탈락했다. 사전검사 뒤 배정한 순차 143명과 목표 직접 148명이 분석 대상이다.',
    design='individual_random_assignment_arithmetic_trial',
    limit='초기 연산 개별 지도 조건을 비교했다. 중간검사 노출과 세기 지원도 조건에 포함됐으므로 순서 단독 효과나 국내 학급·과제 효과는 확인할 수 없다.',
    next_review='출판사 판면과 별도 보충 표·그림, 사전검사와 중간검사 문항의 노출 차이를 대조한다.',
    supports=['아동 단위 무작위 배정과 사후검사', '전체 효과와 초기 세기·연산에 따른 모형', '상황의 유형과 미지 위치'],
    checks={13: ['319', '291', '16 classrooms'], 19: ['Thirteen items'], 23: ['143', '148'],
            25: ['1.20', '0.53', '0.04', '0.03, 0.30'], 27: ['0.96', '0.78']},
    results=dict(
        consented=319, excluded_or_attrited=28, analyzed=[143, 148],
        arithmetic_pretest_items=21, added_posttest_items=13,
        baseline_model_d=1.20,
        table_4_treatment=dict(estimate=.53, credible_95=[.37, .68]),
        table_4_interaction=dict(estimate=.17, credible_95=[.04, .30], prose_interval=[.03, .30]),
        figure_2_points=[[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 0], [0, 1], [1, -1], [1, 0], [1, 1]],
        figure_2_estimates=[.96, .78, .59, .51, .54, .57, .05, .30, .55],
    ),
    corrections=[
        ('저자 원고 24~25쪽 표 3·4와 본문', '기본 모형 d=1.20, 무작위 절편을 포함한 표 4 조건 계수 .53, 절편을 제외한 최종 모형을 구분한다. 3원 상호작용 구간 하한은 표 .04와 본문 .03을 각 위치대로 기록한다.'),
        ('저자 원고 26~27쪽 그림 2', '초기 세기·연산을 각각 평균 및 평균에서 ±1 표준편차로 설정한 모형 추정이다. 아홉 칸을 실제로 따로 배정한 집단으로 읽지 않는다.'),
        ('저자 원고 18~19·32쪽 평가', '사후 연산검사에 13문항이 추가됐다. 순차군에만 실시한 중간검사는 사후검사와 일부 문항 노출이 겹친다.'),
    ],
    claims=[
        ('LTAR-01', ['2수01-05'], [13, 14, 18, 19],
         '확대 연구는 사전검사 뒤 아동을 무작위 배정했고 순차 지도 143명과 목표 직접 지도 148명을 분석했다. 목표 직접 지도군은 사전검사에서 보인 수준보다 세 단계 높은 상황제를 다뤘다.',
         '두 집단 모두 개별 수업을 받았다. 같은 학급에서 일반 수업을 받았을 때와 비교하거나 수업 후 유지 효과를 확인한 결과가 아니다.'),
        ('LTAR-02', ['2수01-04', '2수01-05', '2수01-06'], [23, 24, 25],
         '사후 연산 점수는 기본 모형에서 순차 지도군이 더 높았고 보고된 표준화 효과크기는 d=1.20이다. 상호작용과 무작위 절편을 포함한 표 4의 조건 계수 .53은 그와 다른 추정치다.',
         '표 4의 계수를 모든 학생의 동일한 이득으로 해석할 수 없다. 두 자리 계산 원리나 특정 상황제 유형만의 효과크기도 아니다.'),
        ('LTAR-03', ['2수01-01', '2수01-05'], [25, 26, 27],
         '초기 세기와 연산 수준을 조합한 모형에서 두 점수가 낮은 지점의 추정 차이는 .96이었다. 초기 연산이 높고 세기가 낮은 지점의 추정 차이는 .05였고 구간은 0을 포함했다.',
         '평균과 평균에서 한 표준편차 떨어진 지점을 계산한 결과다. 실제 아홉 집단을 따로 무작위 배정한 결과나 개인별 단계 판정 기준이 아니다.'),
        ('LTAR-04', ['2수01-01', '2수01-04', '2수01-05'], [7, 9, 10, 18, 19],
         '그림 1은 합류·제거·부분과 전체·비교 상황에서 미지의 위치를 바꿨다. 원고는 전체를 다시 세는 방법과 시작 수를 정하고 더하는 횟수를 추적하는 이어 세기를 구별했다.',
         '같은 계산이 나와도 처음 양, 변화량, 두 부분과 차이의 뜻은 다르다. 이어 세기를 특정 상황에서 유일한 풀이 또는 필수 단계로 요구하지 않는다.'),
        ('LTAR-05', ['2수01-05', '2수01-06'], [18, 19, 32, 33],
         '사후 연산검사에 더 어려운 13문항을 추가했다. 순차 지도군에만 중간검사를 실시했고 사후검사와 일부 문항이 겹쳤다.',
         '중간검사 노출이 다른 지도 조건의 비교다. 원점수 차이나 정답률을 동일 문항의 향상이나 순서 단독 효과로 읽을 수 없다.'),
    ],
)


def main():
    registry = load_registry()
    bibliography_path = ROOT / 'data/sources.json'
    queue_path = ROOT / 'data/content_review_queue.json'
    bibliography, queue = load(bibliography_path), load(queue_path)
    pending = []
    for spec in (PILOT, TRIAL):
        if spec['id'] in registry['sources']:
            assert {row[0] for row in spec['claims']} == {c['id'] for c in registry['claims'] if c['source_id'] == spec['id']}
        else:
            pending.append((spec, verify_pdf(spec)))
    if pending:
        assert [sum(row) for row in PILOT['results']['table_2_counts'].values()] == [13, 12]
        assert 319 - 28 == sum(TRIAL['results']['analyzed'])
        for spec, images in pending:
            register(spec, images, bibliography, queue, registry)
        write(bibliography_path, bibliography)
        write(ROOT / 'data/literature_claim_reviews.json', registry)
        write(queue_path, queue)
    build_report()


if __name__ == '__main__':
    main()
