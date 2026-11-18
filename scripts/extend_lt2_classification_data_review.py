"""Register LT2 classification and data activities, graphs, and checked examples."""
import copy
from fractions import Fraction
from urllib.parse import urljoin, urlparse

from extend_lt2_composing_2d_assets_review import pdf_name, verified_assets
from extend_lt2_length_assets_review import asset_pairs, linked_pairs, load, reuse_groups, sha, write
from literature_review import ROOT, build_report, digest, load_registry, target_value
from record_lt2_public_review import SOURCE, URL


DATE = '2026-11-09'
PRIOR = 'data/literature_evidence/CLEMENTS_SARAMA_LT_spatial_orientation_review_notes.json'
PRIOR_SHA = '6db45a6bbe1da50aa2da070d9562713a20afd413213a99e5ef2ee72b7a1f2f44'
NOTES = 'data/literature_evidence/CLEMENTS_SARAMA_LT_classification_data_review_notes.json'
CACHE = ROOT / 'tmp/literature/lt2-classification-data-activities'
ASSETS = ROOT / 'tmp/literature/lt2-classification-data-assets'
STUDY_URL = 'https://researchers.mq.edu.au/en/publications/young-childrens-reasoning-through-data-exploration/'
SCOPE = ('공개 영어 HTML 1045개를 대조했다. 활동·교사자료 목록 824개 중 795개를 확인했고 29개가 남았다. '
         '분류와 자료의 영어 페이지 35개, LT2 PDF 4개 URL·7쪽과 이미지 42개 URL을 확인했다.')
LIMITS = ('활동 소개 두 건의 별도 안내와 직접 연결되지 않은 활동지, 영상, 인용 원연구와 실제 학생 반응은 후속 범위다. '
          '자화상 연구의 저자 초록과 서지는 확인했으며 방법·결과의 본문은 별도다.')

READING = """
a-guessing-game-stemie|색 말 열두 개에서 예상과 뽑은 결과를 기록한다. 매번 말을 되넣는지는 명시하지 않는다.
alike-and-not-alike-stemie|같고 다른 속성을 보고, 만지고, 말로 설명한다. 교사가 가리킨 경우와 자발적으로 찾은 경우를 구별한다.
baby-data-scientists|일상에서 서로 다른 감각 특성을 탐색하게 한다. 인용한 영아 행동의 연령 설명은 발달 판정 기준으로 쓰지 않는다.
caps-for-sale-hat-graphing-stemie|같은 모자 자료를 색이나 무늬로 다시 분류한다. 다른 기준의 범주 수를 그대로 합치지 않는다.
classifying-in-play|놀이 중 장난감의 속성으로 묶고 분류 이유를 말한다.
classifying-with-two-rules|두 분류 규칙으로 놀이를 확장한다. 고정된 이원표를 제공하는 활동과 구별한다.
classy-art-for-classification|알려진 자화상에서 특징을 정한 뒤 새 그림에 규칙을 적용하고, 실제 분류를 공개해 맞춰 본다.
data-detectives-stemie|조사 질문을 만들고 응답을 표와 그래프로 정리한다. 질문별 응답자 수와 조사 대상 집단을 표시한다.
favorite-foods|학생별 한 응답을 세어 가장 많이 또는 적게 나온 범주와 동률을 확인한다.
graph-with-things|실물과 그래프 단위를 일대일로 맞춘다. 신발 한 짝, 한 켤레, 학생 한 명을 구별한다.
graphing-temperatures-over-time-stemie|실제 시각과 온도를 기록한다. 일과명 범주 그래프와 실제 시간축 그래프를 구별한다.
guess-my-rule-consistent-flexible-sorter|소수의 예로 규칙을 추측한다. 여러 규칙에 맞으면 다른 결과가 나올 카드를 추가한다.
guess-my-rule-sorter-by-similar-attributes|분류된 도형에 새 도형을 더한다. 색과 모양이 함께 바뀌면 분류 기준을 가르는 예가 필요하다.
informal-matching|모양·색 등 어떤 공통점으로 짝지었는지 짚는다.
lets-make-pasta-stemie|두 방법으로 만든 면을 같은 속성과 단위로 비교한다. 방법별 세 표본에서 관찰한 차이는 일반 효과를 보장하지 않는다.
loose-parts-collage|두 속성을 함께 적용해 둘 다와 둘 다 아닌 경우를 분류한다.
math-in-everyday-routines|일과 활동 안내를 소개한다. 별도 안내의 절차는 본문 대조에 포함하지 않았다.
nature-sets-stemie|자연물의 크기·색 등 선택한 속성을 말하거나 가리켜 분류한다. 도움을 따로 기록한다.
one-of-these-things-is-not-like-the-others|정해진 기준으로 잘못 놓인 물체를 찾는다. 기준이 없으면 서로 다른 답을 정당화할 수 있다.
patterning-talk-similarity-intuiter-foundations|닮은 점을 말하는 일과 자료의 소개다. 별도 안내 원본은 구별한다.
picture-graphs|한 그림이 나타내는 단위를 정하고 범주별 개수 차이를 해석한다.
pizza-anyone|여러 자르기 방식에 대한 선택 자료를 모은다. 선택 횟수와 응답한 사람 수를 구별한다.
putting-the-data-pieces-together|개별 사례를 모아 전체 그림을 읽되 범주별 합계와 개인별 응답을 구별한다.
rainbow-match|색 기준으로 물체를 맞춘다. 색이 있는 원과 빈 원에 색을 정하는 준비 방식을 구별한다.
researcher-note|유아가 분류 도중 기준을 바꿀 수 있음을 설명한다. 수업 사례의 성취 판정과 구별한다.
seashell-super-sort-stemie|크기와 온전함의 두 속성으로 조개를 나눈다. 큰 것과 작은 것의 경계를 먼저 정한다.
secret-rule-classifier|예와 비예를 비교해 숨은 규칙을 찾는다. 남은 후보를 가르는 물체를 제시한다.
sort-and-count|한 기준으로 분류하고 범주별 개수와 전체를 확인한다.
sort-by-one-attribute|교사가 제시한 한 속성으로 분류한다. 물체의 한 면과 입체의 이름을 구별한다.
sort-race|분류 정확성과 걸린 시간을 따로 기록한다. 앉아서 분류할 수 있는 선택지를 둔다.
sort-stuff|같은 물체를 크기·모양·기능 중 어떤 기준으로 묶었는지 설명한다.
sorting-books|빨간 표지 책 중 입을 벌린 그림이 있는 책을 좁혀 찾는다. 두 조건을 동시에 적용한다.
super-venn-hierarchical-classifier|두 속성에 따라 각 영역에 놓는다. 어느 속성도 없는 경우를 바깥에 둔다.
the-animals-would-not-sleep-sorting-story-time-stemie|같은 동물 예를 새 기준으로 다시 분류한다. 이야기 읽기와 분류 수행을 따로 본다.
which-hoop-are-you|동률과 어느 과목도 가장 좋아하지 않는 경우가 있다. 네 영역을 확보하고 질문의 기준을 먼저 정한다.
"""

PDF_NOTES = {
    '1591642867649': [([1], '최대 다섯 기준을 기록하고 새 그림 다섯 개의 각 조건과 예상 분류를 적는 빈 표다.')],
    '1591642965807': [([1], '네 조건과 그림 다섯 장의 예상 분류를 채운 예시다. 기준을 결합하는 명시적 규칙이나 확인된 정답은 없다.')],
    '1592862733347': [([1,2], '운동화 여덟 켤레와 샌들 네 켤레가 그림과 막대그래프에 동일하게 나타난다. 단위는 켤레다.'), ([3], '빈 쪽이다.')],
    '1607105937334': [([1], '서로 다른 시각 간격을 가진 표와 일과명별 막대그래프다. 온도 수치의 단위 표기는 없다.'),
                      ([2], '실제 시간 간격을 반영한 축과 다섯 측정점이다. 점 사이에 그은 곡선은 추가 측정값을 제공하지 않는다.')],
}

IMAGE_NOTES = [
    ([3], '손으로 만든 것과 공장에서 만든 것의 예측을 붙임쪽지로 모은 예시다. 정답이나 정확도 자료는 아니다.'),
    ([11], '운동화 세 켤레와 샌들 한 켤레를 그린 작은 삽입 그림이다. 연결 PDF의 여덟 켤레와 네 켤레 예시와 별개다.'),
    ([12,20,22], '겹치는 영역과 바깥을 설명하는 삽입 그림이다. 두 속성으로 분류할 때 네 영역을 구별한다.'),
    ([17,41], '일과의 수학 대화와 닮은 속성을 보여 주는 미리보기다. 배포용 원본은 별개다.'),
    ([19,29,33,34,35,37,39,40], '음식·물체·동물·색·의사표시 등 예시와 준비물이다. 그림 개수를 수업의 표본 수로 보지 않는다.'),
    ([25,26,36], '분류에 연결한 그림책 표지다. 책 본문은 별도다.'),
    ([0,1,2,4,5,6,7,8,9,10,13,14,15,16,18,21,23,24,27,28,30,31,32,38], '활동·교구·현장 사진 및 교사 안내 이미지다. 학생 수행이나 효과 자료와 구별한다.'),
]

CLAIMS = [
    ('LT168','LT-P159',['6수04-04','6수04-05','6수04-06','9수04-06'],(0,),(),
     '말을 뽑을 때 매번 되넣는지 정하고, 그 시점에 남은 색별 개수와 전체 개수로 가능성을 비교한다. 관찰한 상대도수는 모형의 확률과 따로 기록한다.',
     '각각의 말이 같은 가능성으로 뽑힌다는 가정이 필요하다. 색깔별 개수가 다르면 색이 나올 가능성도 다르다. 원문은 복원 여부를 정하지 않는다.',
     '빨강 8개, 파랑 3개, 노랑 1개 중 빨강 하나를 뽑았다. 되넣고 다시 뽑을 때와 되넣지 않고 다시 뽑을 때 빨강이 나올 가능성을 각각 구한다.',
     '되넣으면 8/12이고 되넣지 않으면 7/11이다. 후자의 경우 빨강 말과 전체가 각각 하나씩 줄었다.',
     '말을 되넣는 조건을 설명하게 하고 분자와 분모에 세는 대상을 확인한다.'),
    ('LT169','LT-P160',['2수04-02','2수04-03','4수04-01','6수04-03'],(3,7,8,9,20,21,22),('1592862733347',),
     '표와 그래프에서 기호 하나의 단위와 조사 단위를 명시한다. 여러 답을 허용하면 선택 횟수와 응답자 수가 달라질 수 있다.',
     '신발 그림의 단위는 켤레다. 한 학생이 두 종류를 골랐다면 그 학생은 응답자 한 명으로 센다.',
     '두 가지 피자 모양을 골라도 된다. 6명이 모두 응답했고 네모를 4명, 세모를 5명이 골랐다. 응답자는 몇 명이며 선택은 몇 번인가? 두 가지를 다 고른 사람은 몇 명인가?',
     '응답자는 6명이고 선택은 9번이다. 각 모양을 고른 수에 두 모양을 모두 고른 사람이 두 번 들어가므로 3명이 둘 다 골랐다.',
     '표의 단위를 사람과 선택으로 나눠 쓰게 한다. 저학년에서는 응답자와 선택의 구별을 먼저 확인한다.'),
    ('LT170','LT-P161',['4수04-02','4수04-03','9수02-06','9수02-16'],(10,),('1607105937334',),
     '온도와 실제 경과 시간의 관계를 나타낼 때 같은 시간 간격을 같은 축 길이로 표시한다. 일과별 범주 막대의 간격에는 경과 시간의 의미가 없다.',
     '첨부 자료는 간격이 다른 실제 시각을 기록한다. 측정점 사이를 이은 선이나 곡선에서 실제 중간 온도와 극값을 확정할 수 없다.',
     '9시, 10시, 13시에 각각 15 °C, 17 °C, 20 °C를 측정했다. 가로축에서 두 간격의 길이는 어떤 비여야 하는가? 11시의 실제 온도를 알 수 있는가?',
     '한 시간과 세 시간이므로 길이는 1 대 3이다. 11시는 측정하지 않아 실제값을 알 수 없다.',
     '같은 온도 차이와 같은 시간당 변화량을 구별하고, 관측점과 연결선을 각각 가리키게 한다.'),
    ('LT171','LT-P162',['2수04-01'],(4,11,12,13,18,24,26,28,30,33),(),
     '분류된 몇 가지 예가 두 속성을 동시에 공유하면 복수의 규칙이 관찰에 맞을 수 있다. 두 규칙이 다르게 판정하는 예를 확인한다.',
     '이미 정해진 기준을 적용하는 과제와 자료에서 기준을 추측하는 과제를 구별한다. 한 카드가 두 가설을 가르더라도 가능한 모든 규칙을 배제하는 것은 아니다.',
     '빨간 원만 왼쪽, 파란 네모만 오른쪽에 놓였다. 왼쪽 규칙이 빨강인지 원인지 구분하려면 어떤 카드를 추가하고 무엇을 확인할까?',
     '빨간 네모를 제시한다. 빨강 기준이면 왼쪽이고 원 기준이면 오른쪽이다. 또는 파란 원의 반대 판정을 확인한다.',
     '다른 판정을 내릴 예를 학생이 고르고 두 기준을 각각 적용하게 한다.'),
    ('LT172','LT-P163',['2수04-01','10공수2-02-03','10기수2-02-03'],(5,15,25,31,32,34),(),
     '두 속성의 유무를 각각 묻고 한쪽만, 다른 쪽만, 둘 다, 둘 다 아닌 네 영역에 분류한다. 전체 안에서 교집합과 바깥 영역의 개수를 확인한다.',
     '고유한 선호 하나를 고르게 한 응답과 두 질문에 각각 답한 예·아니요 응답을 구별한다. 두 질문을 따로 묻는 것은 답이 확률적으로 독립이라는 뜻이 아니다.',
     '카드 14장 중 빨강은 8장, 원은 6장, 빨간 원은 3장이다. 두 속성 중 하나 이상을 가진 카드와 둘 다 아닌 카드는 각각 몇 장인가?',
     '하나 이상은 8+6−3=11장이고 둘 다 아닌 카드는 14−11=3장이다. 빨강만 5장, 원만 3장, 빨간 원 3장도 확인할 수 있다.',
     '같은 카드가 두 집합에 속할 수 있음을 두 고리와 네 영역으로 설명하게 한다.'),
    ('LT173','LT-P164',['2수04-01','12인수01-01','12인수03-03'],(6,),('1591642867649','1591642965807'),
     '분류 규칙을 만드는 예와 규칙을 시험할 새 예를 분리한다. 새 예에 대한 예측을 기록한 뒤 정답을 공개해 비교한다.',
     '첨부의 예시는 네 속성과 예측표를 보여 준다. 그림만으로 개인의 나이나 수학 역량을 판정할 수 없으며, 규칙 기반 손분류가 영상 자동 분류를 구현한 것도 아니다.',
     '새 카드 10장에 규칙을 적용해 8장과 일치했다. 틀린 카드 두 장을 본 뒤 규칙을 바꿨다. 바꾼 규칙의 정확도를 다시 어떻게 확인할까?',
     '처음 규칙의 관찰 일치율은 8/10이다. 바꾼 규칙은 이전 두 묶음과 겹치지 않는 새 카드에 먼저 적용하고 정답과 비교한다.',
     '규칙 설정, 답을 보기 전의 예측, 정답 대조, 수정 후 새 자료 확인을 별도로 기록한다.'),
    ('LT174','LT-P165',['4수04-03','6수04-01','6수04-03'],(7,14),(),
     '같은 속성을 같은 단위로 잰 뒤 자료의 중심과 퍼짐을 따로 비교한다. 방법별로 재료와 측정 조건을 맞춘다.',
     '만든 면의 길이 또는 두께는 서로 다른 측정량이다. 방법별로 소수 표본을 관찰한 결과를 일반화하지 않는다.',
     '같은 자로 잰 길이가 A 방법에서 4, 5, 6 cm이고 B 방법에서 2, 5, 8 cm다. 평균과 최댓값에서 최솟값을 뺀 값을 비교한다.',
     '두 평균은 모두 5 cm다. 최댓값과 최솟값의 차는 A가 2 cm, B가 6 cm다. 이 자료에서는 B의 범위가 더 크다.',
     '평균이 같아도 개별 길이의 퍼짐이 다를 수 있음을 설명하게 한다.'),
]

OBSERVATIONS = [
    dict(id=oid,standard_codes=codes,question=question,expected=expected,interpretation=interpretation,student_validated=False)
    for _,oid,codes,_,_,_,_,question,expected,interpretation in CLAIMS
]


def verify_examples():
    red_with_replacement, red_without_replacement = Fraction(8,12), Fraction(7,11)
    assert red_with_replacement > red_without_replacement
    responses = [{'네모','세모'}]*3 + [{'네모'}] + [{'세모'}]*2
    assert (len(responses),sum(map(len,responses)),sum(len(s)==2 for s in responses)) == (6,9,3)
    times = [9*60,11*60+30,12*60,13*60+30,14*60+30]
    assert [b-a for a,b in zip(times,times[1:])] == [150,30,90,60]
    assert Fraction(10-9,13-10) == Fraction(1,3)
    assert 8+6-3 == 11 and 14-11 == 3
    a,b = [4,5,6],[2,5,8]
    assert Fraction(sum(a),len(a)) == Fraction(sum(b),len(b)) == 5
    assert (max(a)-min(a),max(b)-min(b)) == (2,6)
    return dict(second_red_with_replacement=str(red_with_replacement),second_red_without_replacement=str(red_without_replacement),
                example_temperature_times_in_minutes=times,example_temperature_values=[37,49,54,59,57],
                shoe_chart_pair_counts=[8,4],multiselect_respondents=6,multiselect_choices=9,
                two_trait_region_counts=[5,3,3,3],example_model_initial_match='8/10',
                length_means_cm=[5,5],length_ranges_cm=[2,6])


def main():
    registry = load_registry()
    source = registry['sources'][SOURCE]
    if source['snapshot_file'] == NOTES:
        assert source['snapshot_sha256'] == sha(ROOT / NOTES)
        assert {row[0] for row in CLAIMS} <= {row['id'] for row in registry['claims']}
        assert source['observations'][-len(OBSERVATIONS):] == OBSERVATIONS
        build_report()
        return
    assert source['snapshot_file'] == PRIOR and sha(ROOT / PRIOR) == PRIOR_SHA
    prior = load(ROOT / PRIOR)
    pages, bodies, selected = [load(CACHE / name) for name in ('activity-manifest.json','english-bodies.json','selection.json')]
    followup = copy.deepcopy(prior['activity_followup_catalog'])
    assert selected == [row for row in followup['records'] if not row['body_read']
                        and any('/math/classification-and-data-analysis/' in url for url in row['linked_level_urls'])]
    reading = [line.split('|',1) for line in READING.strip().splitlines()]
    assert len(pages) == len(bodies) == len(selected) == len(reading) == 35
    assert [row['url'] for row in pages] == [row['url'] for row in selected] == [row['url'] for row in bodies]
    assert [row['url'].rsplit('/',1)[-1] for row in pages] == [row[0] for row in reading]

    old_images = {row['url'] for row in prior['image_read_manifest']}
    old_pdfs = {row['url'] for row in prior['supplementary_pdf_read_manifest']}
    images, pdfs, logs = {}, {}, []
    groups = copy.deepcopy(prior['read_groups'])
    for index,(page,body,(_,note)) in enumerate(zip(pages,bodies,reading,strict=True)):
        url = page['url']
        assert page['status'] == 200 and page['final_url'] == url and url.startswith(URL)
        assert sha(ROOT / page['file']) == page['sha256']
        teacher = 'Type:\nTeacher Resources' in body['body']
        intro = '\nActivity\n' not in body['body']
        assert teacher == (index == 24) and intro == (index in (16,19))
        kind = 'teacher_resource' if teacher else 'activity_introduction' if intro else 'activity_procedure'
        groups['teacher_resources' if teacher else 'activities'].append(page['key'])
        logs.append(dict(url=url, page_kind=kind, note=note))
        linked_images = {urljoin(url, img['src']) for img in page['images'] if '/upload/' in img.get('src','')} - old_images
        linked_pdfs = {link for link in page['links'] if urlparse(link).path.lower().endswith('.pdf') and '/downloads/' not in link} - old_pdfs
        if linked_images:
            images[url] = sorted(linked_images)
        if linked_pdfs:
            pdfs[url] = sorted(linked_pdfs)
    assert {k:len(v) for k,v in groups.items()} == dict(general=6,domain_overviews=20,levels=224,activities=764,teacher_resources=31)

    raw_pdfs, raw_images = [load(ASSETS / f'{kind}-manifest.json') for kind in ('pdf','image')]
    new_pdfs, new_images, pdf_notes, image_notes = verified_assets(raw_pdfs,raw_images,PDF_NOTES,IMAGE_NOTES)
    assert (len(new_pdfs),sum(a['pdf_pages'] for a in new_pdfs),len(new_images)) == (4,7,42)
    assert asset_pairs(new_pdfs) == linked_pairs(pdfs) and asset_pairs(new_images) == linked_pairs(images)
    all_pdfs = prior['supplementary_pdf_read_manifest'] + new_pdfs
    all_images = prior['image_read_manifest'] + new_images
    unique_pdfs = {a['sha256']:a['pdf_pages'] for a in all_pdfs}
    assert (len(all_pdfs),sum(a['pdf_pages'] for a in all_pdfs),len(unique_pdfs),sum(unique_pdfs.values())) == (182,623,168,567)
    assert (len(all_images),len({a['sha256'] for a in all_images})) == (1054,1020)
    asset_urls = {pdf_name(asset['url']):asset['url'] for asset in new_pdfs}

    manifest = prior['html_read_manifest'] + [{k:row[k] for k in ('key','url','title','sha256','status')} for row in pages]
    read_urls = {row['url'] for row in manifest}
    assert len(manifest) == len(read_urls) == 1045
    for row in followup['records']:
        row['body_read'] = row['url'] in read_urls
    followup['listed_body_read'] = sum(row['body_read'] for row in followup['records'])
    followup['listed_body_pending'] = len(followup['records']) - followup['listed_body_read']
    assert (followup['listed_body_read'],followup['listed_body_pending']) == (795,29)

    bibliography_path = ROOT / 'data/sources.json'
    bibliography = load(bibliography_path)
    entry = next(row for row in bibliography if row['id'] == SOURCE)
    previous_entry = copy.deepcopy(entry)
    entry.update(review_scope=SCOPE,next_review=LIMITS)
    notes = dict(prior)
    notes.update(
        date=DATE, read_scope=SCOPE, previous_review=copy.deepcopy(source), previous_bibliography=previous_entry,
        previous_notes_file=PRIOR, previous_notes_sha256=PRIOR_SHA, html_read_manifest=manifest,
        observed_html_assets=manifest, read_groups=groups, activity_followup_catalog=followup,
        catalog_coverage={**prior['catalog_coverage'],'read_activity_bodies':795,'pending_activity_bodies':29},
        new_read_groups=dict(domain_overviews=0,levels=0,activities=34,teacher_resources=1,inline_images=42,supplementary_pdf_urls=4),
        classification_data_reading_log=logs, completed_classification_data_records=selected,
        classification_data_checked_examples=verify_examples(), classification_data_pdf_reading_log=pdf_notes,
        classification_data_image_reading_log=image_notes,
        supplementary_pdf_read_manifest=all_pdfs, image_read_manifest=all_images,
        supplementary_pdf_coverage=dict(urls=182,page_occurrences=623,distinct_sha256_files=168,
            pages_after_file_deduplication=567,all_selected_pages_visual_reviewed=True,whole_site_attachment_review=False),
        pdf_exact_reuse_groups=reuse_groups(all_pdfs),
        pdf_reading_log={**prior['pdf_reading_log'],**{
            url:[f"{', '.join(map(str,row['pdf_pages']))}쪽. {row['note']}" for row in rows] for url,rows in pdf_notes.items()
        }},
        reading_log=prior['reading_log'] + ['분류와 자료 영어 활동 절차 32개, 소개 2개, 교사자료 1개와 LT2 PDF 7쪽·이미지 42개 URL을 대조했다.'],
        source_corrections=prior['source_corrections'] + [dict(
            kind='counting_units_elapsed_time_and_classification_evidence',
            locations=[pages[i]['url'] for i in (0,6,10,20,21,34)] + list(asset_urls.values()),
            action='복원 여부, 응답자·선택·켤레, 시간 간격, 분류 규칙의 반례와 검증 자료를 구별했다.',
        )],
        classification_data_cited_study=dict(
            url=STUDY_URL, linking_page=pages[6]['url'], read_scope='저자 대학 저장소 초록과 서지',
            reported_sample='호주의 수학 성취도가 높은 1학년 학생 9명',
            status='full_chapter_not_read', limit='참가자 9명의 과제 수행 기록이며 일반 학생 또는 자동 분류 정확도를 보장하지 않는다.',
        ),
        unread_followups=prior['unread_followups'] + [LIMITS],
    )
    note_path = ROOT / NOTES
    write(note_path,notes)
    history = source['snapshot_history'] + [dict(snapshot_file=PRIOR,snapshot_sha256=PRIOR_SHA,date=source['date'],read_scope=source['read_scope'])]
    source.update(
        date=DATE, snapshot_file=NOTES, snapshot_sha256=sha(note_path), snapshot_history=history,
        bibliography_snapshot=digest(entry), html_read_manifest=manifest, read_scope=SCOPE, limits=LIMITS,
        method_note='분류와 자료의 본문 및 첨부에서 조사 단위, 시간 간격과 규칙 확인의 조건을 대조했다.',
        editorial_action='문헌 대응 7건과 자체 관찰 과제 7개를 추가했다.', observations=source['observations'] + OBSERVATIONS,
        image_read_manifest=all_images, supplementary_pdf_read_manifest=all_pdfs,
    )
    for cid,_,codes,indices,files,support,limit,*_ in CLAIMS:
        registry['claims'].append(dict(
            id=cid,source_id=SOURCE,role='related_theoretical_context',standard_codes=codes,
            locations=[pages[i]['url'] for i in indices] + [asset_urls[file] for file in files],
            support=support,does_not_establish=limit,independent_review=False,student_validated=False,
            target_snapshots={f'revision:{code}':digest(target_value(f'revision:{code}')) for code in codes},
        ))
    queue_path = ROOT / 'data/content_review_queue.json'
    queue = load(queue_path)
    row = next(row for row in queue['literature_review'] if row['source']['id'] == SOURCE)
    row.update(source=entry,claim_ids=[claim['id'] for claim in registry['claims'] if claim['source_id'] == SOURCE])
    write(bibliography_path,bibliography)
    write(ROOT / 'data/literature_claim_reviews.json',registry)
    write(queue_path,queue)
    build_report()
    print('Reviewed 35 classification and data pages, 4 PDFs and 42 images; added 7 claims and 7 observations.')


if __name__ == '__main__':
    main()

