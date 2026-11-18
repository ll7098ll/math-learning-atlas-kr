"""Record reviewed English pattern and algebra activity pages in LT2."""
import copy
from urllib.parse import urljoin, urlparse

from extend_lt2_length_assets_review import load, sha, write
from literature_review import ROOT, build_report, digest, load_registry, target_value
from record_lt2_public_review import SOURCE, URL


DATE = '2026-11-09'
PRIOR = 'data/literature_evidence/CLEMENTS_SARAMA_LT_fractions_assets_review_notes.json'
PRIOR_SHA = 'efe36f1034fdf03d0df74c5407b2c61328b90875059381065e94974ddf1c6f35'
NOTES = 'data/literature_evidence/CLEMENTS_SARAMA_LT_patterns_activities_review_notes.json'
CACHE = ROOT / 'tmp/literature/lt2-patterns-activities'
SCOPE = '규칙성·대수적 사고에 연결된 영어 페이지 47개를 대조했다. 활동 절차 45개와 가정 안내 소개 2개다. 활동·교사자료 목록 824개 중 562개를 확인했고 262개가 남았다.'
LIMITS = '새 연결 PDF 7개와 삽입 이미지 68개 URL, 영상·별도 가정 안내·인용 연구는 후속 범위다. 유한한 배열만으로 규칙이 하나로 확정되거나 학생이 검증된다고 판단하지 않는다.'

READING = """
attribute-match-intuitive-patterner-foundations|같은 두 물건을 고르되 색·크기·모양 중 어떤 속성이 같은지 밝힌다. 두 물건이 닮았다는 사실과 규칙이 반복되는 것은 구별한다.
candy-stories|같은 전체에서 더 적게 주면 더 많이 남는다. 90에서 35를 빼면 55, 40을 빼면 50이다. 두 경우 모두 실제로 줄 수 있는 수를 전제로 한다.
child-patterns|서기와 앉기의 순서를 반복하고 다음 동작의 근거를 말한다. 사람의 이름과 반복되는 동작을 구별한다.
clothes-patterns|옷의 색 띠에서 최소 반복 단위를 찾고 같은 순서를 세 번 읽는다. 일부만 보이는 띠에서는 규칙을 추정한다.
cost-patterns|빨간 모자가 파란 모자의 세 배면 R=3B다. 파란 모자가 2일 때 빨강은 6이고 두 모자의 합은 8이다. 가격과 모자 개수를 구별한다.
counting-poems-and-finger-plays|동화와 시에서 반복되는 색·소리·박자의 순서를 가리킨다. 이야기를 따라 하는 것과 반복 단위를 설명하는 것을 구별한다.
creative-patterns|ABB와 ABCA를 다른 재료로 옮긴다. ABCA를 잇는 경계에는 A가 두 번 연속 나온다.
cube-patterns--pattern-translator-and-unit-recognizer|파랑·파랑·노랑 탑을 세 번 이으면 9개다. 탑 한 개와 블록 낱개를 구별한다.
dancing-patterns-patterner|박수·박수·차기의 AAB를 반복한다. 동작 속도나 응답 방식이 달라도 순서가 유지되는지 본다.
doggie-algebra|개가 D마리이고 한 마리마다 눈이 두 개이면 눈 수 E=2D다. 1D=2E와 D=4L을 개수의 방정식으로 쓰지 않고, 네 다리 조건에서는 L=4D로 나타낸다.
doggie-equations|한 마리에 코 하나를 가정하면 N=D다. 눈으로 바꿀 때 개수 관계는 E=2D이며 도전 문구의 D=2E와 방향이 다르다.
dum-di-dum-dum|점과 줄을 작은 소리와 큰 소리에 대응한다. 점·줄·줄의 단위와 실제 소리의 길이를 구별한다.
fill-in-the-pattern-on-the-snake|보라·노랑의 AB 순서를 따라 복제한다. 뱀이 굽어도 정한 시작점과 진행 방향을 유지한다.
finding-patterns|뚜껑을 놓고 색·크기·모양의 차이를 설명한다. 파랑·초록에서 빨강이 추가된 사례의 규칙 변경을 따로 기록한다.
finger-sticks-finger-play|노래에 맞춘 손동작과 박수에서 따라 한 동작과 다음 순서를 예상한 응답을 구별한다.
generating-conjectures|0을 더해도 값이 같고 더하는 순서와 묶는 방법을 바꿔도 덧셈의 합이 같다. 일부 사례 확인과 일반적으로 성립하는 까닭을 구별한다.
groovy-patterns-pattern-recognizer|발 구르기·박수 같은 AB를 다른 속도로 반복한다. 두 동작의 순서와 빠르기를 구별한다.
growing-patterns-numeric-patterner|한 단계에 타일 두 개를 더한다는 규칙은 어디에 무엇을 붙이는지에 달렸다. 0·1·3·5에서는 첫 차가 1이라 뒤부터 2씩이라는 조건에서 7이다.
how-many-do-you-have|한 사람당 눈 두 개를 가정한 표에서 2·4·6은 누적 수다. 사람마다 실제 신체 조건이 다를 수 있어 모형의 조건을 명시한다.
i-see-a-pattern|커튼·책꽂이 등에서 무엇을 어떤 방향으로 읽는지 정해 반복 단위를 말한다.
lets-make-a-pattern-patterner-ab|돼지·오리의 순서를 색 블록으로 옮긴다. 원본과 겉모습이 달라도 서로 다른 두 역할이 번갈아야 한다.
lets-talk-about-patterns|줄무늬·목걸이에서 속성을 정해 반복 여부를 판단한다. 여러 색이 있다는 사실만으로 반복이라 하지 않는다.
make-a-longer-pattern-patterner|완성된 ABC와 덜 채운 AAB를 늘린다. AAB A A의 마지막에는 B를 넣어 단위를 마친다.
making-jewelry|노랑·파랑·빨강 세 번이라면 9개다. 인쇄 예시는 중간 빨강이 한 번 더 있어 실제 나열은 10개다. 순서의 오류와 재료의 변경을 구별한다.
math-hopscotch|1·2·1·2는 밟는 칸의 이름이고, 움직임을 세면 네 번이다. 칸 번호와 도약 횟수를 나누어 묻는다.
movement-patterns|박수·무릎 두드리기를 따라 한 뒤 멈추고 순서를 말한다. 교사의 동시 시범과 독립 설명을 구별한다.
musical-patterns-stemie|일정 박자와 동작 단위의 반복을 나눈다. 도전 문구는 AB라 쓰지만 박수·박수·발·발의 최소 단위는 AABB다.
pasta-patterns-pattern-translator-and-unit-recognizer|꼬인 면·곧은 면의 AB를 작은 것·큰 것으로 옮긴다. 속성이 바뀌어도 위치별 대응이 보존되어야 한다.
pattern-beat|모든 수를 말하며 짝수에 강세를 두는 것과 짝수만 세는 것을 구별한다.
pattern-fixer-with-beads|첫 지시는 파랑·빨강인데 뒤의 읽기 예는 빨강·파랑으로 바뀐다. 시작 위치를 고정하고 빠진 것과 하나 더 끼운 것을 구별한다.
pattern-strips-patterner|AAB·ABB·ABC·AABB를 복제한다. 거리를 두어 보고 다시 만들 때의 기억과 반복 단위 설명을 따로 본다.
pattern-strips-patterner-ab|사각형·원 두 개를 한 단위로 가리킨다. 두 손가락 지원과 독립적으로 반복 단위를 찾는 반응을 구별한다.
pattern-task-cards|흰색·흰색·빨강·빨강을 원·원·정사각형·정사각형으로 옮긴다. AABB의 순서와 단위를 보존한다.
patterning-at-home|가정 안내의 목표와 서지만 확인했다. 해당 영어 본문에 활동 절차나 직접 PDF 링크가 없다.
patterning-talk-intuitive-patterner-foundations|일상 대화 안내를 소개하지만 영어 본문에 활동 절차와 직접 PDF 링크가 없다. 안내서 내용은 별도 대조한다.
patterns-in-the-environment|책의 소개와 주변에서 찾은 규칙을 구별한다. 실제 배열의 반복과 처음 몇 개의 모양만 설명한 경우를 나눈다.
patterns-on-a-hundreds-chart-relational-thinker-with-multiplication|두 가지 배수 색이 겹치는 칸은 두 수의 공배수다. 본문이 말하는 공약수와 구별한다.
rhythmic-patterns|박수 두 번과 발 구르기 두 번이 한 AABB 단위다. 단위가 끝나기 전에 시작할 때의 순서를 설명한다.
scissor-function|처음 끈 하나에서 한 번에 내부 한 곳을 자르면 조각은 자른 횟수보다 하나 많다. 원문의 5=6은 표의 대응을 등식처럼 쓴 것으로 y=x+1로 고친다.
stringing-beads|AAB와 ABB를 다른 재료로 만들되 목걸이의 시작과 끝을 잇는 경우에는 닫힌 경계에서도 단위가 이어지는지 확인한다.
the-cats-need-their-costumes|고양이 C마리마다 눈 두 개와 목 하나면 E=2C, N=C, 합은 E+N=3C다. 원문에 반대로 적힌 대응식과 역할을 구별한다.
top-secret-patterns-on-a-hundreds-chart-part-1-numeric-patterner|한 행에는 연속된 수가 열 개 있지만 모든 행의 값이 1~10은 아니다. 같은 열에서 아래 칸이 있으면 10을 더한다.
top-secret-patterns-on-a-hundreds-chart-part-2-numeric-patterner|짝수의 일의 자리 순환은 2·4·6·8·0이다. 10은 수이며 일의 자리 숫자는 0이다. 뒤로 이동할 때 판에 0 칸이 있는지 먼저 확인한다.
true-or-false-number-patterns|덧셈에서 0·1, 순서와 묶음에 관한 규칙을 찾는다. 사례에서 맞는지와 다른 연산에도 적용되는지를 구별한다.
true-or-false-with-number-sentences-relational-thinker-|7+2와 3+6은 둘 다 9다. 5+□=7+4에서 빈칸은 6이다.
true-or-false-with-number-sentences-relational-thinker-symbolic-|앞 수준과 같은 수식을 제시한다. 수준명이 다르더라도 문제 예의 기호 사용이 달라졌다고 추정하지 않는다.
weaving-patterns|위·아래나 안·밖 중 무엇을 반복하는지 정한다. 끈을 한 번 통과시키는 동작과 울타리 기둥 개수를 구별한다.
"""

CLAIMS = [
    ('LT110',['2수02-01','2수02-02'],[2,6,7,11,20,22,23,26,27,29,32,39],
     '최소 반복 단위와 단위의 개수, 재료를 바꿔도 유지되는 순서를 구별한다.',
     '목걸이의 추가 빨강과 음악 예의 AABB를 원문 수준명에 맞춰 덮어 쓰지 않는다. 시작점과 경계를 먼저 정한다.'),
    ('LT111',['2수01-09','4수02-02','4수02-03'],[1,15,43,44,45],
     '같은 전체를 전제로 뺄셈의 남은 양을 비교하고, 등식 양쪽의 값을 따로 확인한다.',
     '예시의 참 여부를 확인한 것과 덧셈 성질이 성립하는 까닭을 설명하는 것을 구별한다.'),
    ('LT112',['2수01-10','4수02-01','6수02-01'],[4,9,10,18,40],
     '동물 마릿수, 한 마리당 수, 전체의 수를 이름 붙이고 방향이 맞는 대응식을 쓴다. 고양이 C마리의 눈 수는 E=2C다.',
     '동물 한 마리의 신체 조건이나 가격 배율이 일정하다는 가정이 필요하다. 단위 이름을 붙인 짝을 수의 등식으로 읽지 않는다.'),
    ('LT113',['4수02-01','4수02-03','6수02-01'],[38],
     '끈 하나에서 한 차례에 아직 자르지 않은 내부 한 곳을 자르면 조각 수는 1 증가해 y=x+1이다.',
     '처음 끈이 여러 개이거나 한 차례에 여러 곳을 자를 때는 시작값 또는 증가량이 바뀐다.'),
    ('LT114',['2수01-02','2수01-03','6수01-05'],[36,41,42],
     '1~100 수판에서 같은 열은 10씩 증가하고 짝수의 일의 자리는 2·4·6·8·0을 반복한다. 두 배수 색이 겹치는 수는 공배수다.',
     '맨 아래에서는 아래 칸이 없고 1~100 판에 0이 없을 수 있다. 숫자 10과 일의 자리 0을 구별한다.'),
    ('LT115',['2수02-01','4수02-01','6수02-01'],[17],
     '타일이 늘어나는 위치와 한 단계 증가량, 처음 항을 함께 적는다. 0·1·3·5는 모든 차가 같은 수열이 아니다.',
     '뒤의 차가 2로 계속된다는 규칙에서는 7이다. 유한한 앞 항들만 보고 다음 수가 반드시 7이라고 판단하지 않는다.'),
]

OBSERVATIONS = [
    dict(id='LT-P101',standard_codes=['2수02-01','2수02-02'],question='박수·박수·발 구르기·발 구르기가 계속 반복된다. 가장 짧은 단위를 말하고 같은 규칙을 빨강과 파랑으로 옮겨 두 단위를 만들어라.',expected='단위는 박수·박수·발·발이다. 박수를 빨강, 발을 파랑으로 정하면 빨강·빨강·파랑·파랑을 두 번 놓는다.',interpretation='두 가지 동작이라는 사실과 단위가 네 자리라는 사실을 구별한다.',student_validated=False),
    dict(id='LT-P102',standard_codes=['2수01-09','4수02-02','4수02-03'],question='7+2=3+6은 참인가? 5+□=7+4의 □를 구하고 양쪽의 식을 바꾸어 써도 같은 값인지 확인하라.',expected='첫 식은 양쪽이 9다. 다음 식의 오른쪽은 11이므로 □는 6이며, 좌우를 바꾸어도 양쪽 값은 11이다.',interpretation='등호 뒤 숫자를 답으로 읽는지와 양쪽 값의 동등함을 설명하는지를 따로 본다.',student_validated=False),
    dict(id='LT-P103',standard_codes=['2수01-10','4수02-01','6수02-01'],question='고양이가 C마리이고 한 마리마다 눈 두 개와 목 하나가 있다. 눈 수 E와 목 수 N을 C로 나타내라. 다섯 마리일 때 눈과 목의 수를 합하면 얼마인가?',expected='E=2C이고 N=C다. 다섯 마리면 눈 10개와 목 5개로 합은 15다.',interpretation='문자의 뜻을 먼저 정하고 E=2C와 C=2E가 다른지 수로 대입해 확인한다.',student_validated=False),
    dict(id='LT-P104',standard_codes=['4수02-01','4수02-03','6수02-01'],question='한 번에 끈의 아직 잘리지 않은 내부 한 곳을 자른다. 처음 끈 하나에서 5번 자르면 조각은 몇 개인가? 처음 끈 두 개에서 총 5번 자르면 몇 개인가?',expected='처음 하나면 1+5=6개다. 처음 두 개면 2+5=7개다.',interpretation='대응하는 두 수를 그대로 등호로 잇는지와 처음 수를 반영하는지를 확인한다.',student_validated=False),
    dict(id='LT-P105',standard_codes=['2수01-02','2수01-03','6수01-05'],question='1~100 수판에서 2의 배수와 5의 배수를 칠한다. 두 색이 겹치는 가장 작은 칸은 무엇인가? 짝수 10의 일의 자리와 아래 한 칸의 수는 각각 무엇인가?',expected='두 색이 겹치는 첫 수는 10이다. 10의 일의 자리 숫자는 0이고 아래에는 20이 있다.',interpretation='공배수, 일의 자리 숫자, 한 행 내려가는 변화를 구별한다.',student_validated=False),
    dict(id='LT-P106',standard_codes=['2수02-01','4수02-01','6수02-01'],question='타일 수가 0·1·3·5인 배열이다. 처음부터 2씩 늘었는가? 세 번째 항부터 앞 항보다 2개씩 많다는 규칙에서 다음 항은 얼마인가?',expected='0에서 1은 1 늘고 그 뒤 두 차는 2다. 주어진 조건에서 5보다 2 큰 7이 다음 항이다.',interpretation='처음과 이후의 차를 나눠 계산하며 정해 준 규칙과 관찰한 값만으로 추측한 규칙을 구별한다.',student_validated=False),
]


def verify_examples(bodies):
    t = [r['body'] for r in bodies]
    assert 'D = 4L' in t[9] and 'D = 2E' in t[10] and 'C = 2E' in t[40]
    assert '5 (cuts) =\n6 (pieces of string)' in t[38]
    assert '0, 1, 3, 5' in t[17] and 'correct answer = 7' in t[17]
    assert 'Clap-Clap-Stomp-Stomp' in t[26] and 'AB pattern' in t[26]
    assert 'yellow, blue, red, yellow, blue, red, red, yellow, blue, red' in t[23]
    assert 90 - 35 == 55 and 90 - 40 == 50 and 7 + 4 - 5 == 6
    assert [b-a for a,b in zip([0,1,3],[1,3,5])] == [1,2,2]
    return dict(eyes_per_animal=2, legs_per_animal=4, cats_eyes_necks_per_cat=3,
                strand_pieces_after_five_cuts=[6,7], even_units_digits=[2,4,6,8,0],
                growth_initial_differences=[1,2,2], jewelry_printed_length=10, jewelry_described_length=9)


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
    pages, bodies, selected = [load(CACHE / name) for name in ('activity-manifest.json', 'english-bodies.json', 'selection.json')]
    followup = copy.deepcopy(prior['activity_followup_catalog'])
    assert selected == [row for row in followup['records'] if not row['body_read']
                        and any('/math/patterns-structure-and-algebraic-thinking/' in url for url in row['linked_level_urls'])]
    reading = [line.split('|', 1) for line in READING.strip().splitlines()]
    assert len(pages) == len(bodies) == len(selected) == len(reading) == 47
    assert [row['url'] for row in pages] == [row['url'] for row in selected] == [row['url'] for row in bodies]
    assert [row['url'].rsplit('/', 1)[-1] for row in pages] == [row[0] for row in reading]
    examples = verify_examples(bodies)

    old_images = {row['url'] for row in prior['image_read_manifest']}
    old_pdfs = {row['url'] for row in prior['supplementary_pdf_read_manifest']}
    images, pdfs, logs = {}, {}, []
    groups = copy.deepcopy(prior['read_groups'])
    for page, body, (_, note) in zip(pages, bodies, reading):
        url = page['url']
        assert page['status'] == 200 and page['final_url'] == url and url.startswith(URL)
        assert sha(ROOT / page['file']) == page['sha256']
        landing = url.rsplit('/', 1)[-1] in {'patterning-at-home', 'patterning-talk-intuitive-patterner-foundations'}
        assert ('\nActivity\n' in body['body']) != landing
        assert 'Type:\nTeacher Resources' not in body['body']
        groups['activities'].append(page['key'])
        logs.append(dict(url=url, page_kind='family_resource_landing' if landing else 'activity_procedure', note=note))
        linked_images = {urljoin(url, image['src']) for image in page['images'] if '/upload/' in image.get('src', '')} - old_images
        linked_pdfs = {link for link in page['links'] if urlparse(link).path.lower().endswith('.pdf') and '/downloads/' not in link} - old_pdfs
        if linked_images:
            images[url] = sorted(linked_images)
        if linked_pdfs:
            pdfs[url] = sorted(linked_pdfs)
    assert sum(row['page_kind'] == 'family_resource_landing' for row in logs) == 2
    assert len({url for links in images.values() for url in links}) == 68
    assert len({url for links in pdfs.values() for url in links}) == 7
    assert {k: len(v) for k, v in groups.items()} == dict(general=6, domain_overviews=20, levels=224, activities=546, teacher_resources=16)
    manifest = prior['html_read_manifest'] + [{k: row[k] for k in ('key', 'url', 'title', 'sha256', 'status')} for row in pages]
    read_urls = {row['url'] for row in manifest}
    assert len(manifest) == len(read_urls) == 812
    for row in followup['records']:
        row['body_read'] = row['url'] in read_urls
    followup['listed_body_read'] = sum(row['body_read'] for row in followup['records'])
    followup['listed_body_pending'] = len(followup['records']) - followup['listed_body_read']
    assert (followup['listed_body_read'], followup['listed_body_pending']) == (562, 262)

    bibliography_path = ROOT / 'data/sources.json'
    bibliography = load(bibliography_path)
    entry = next(row for row in bibliography if row['id'] == SOURCE)
    previous_entry = copy.deepcopy(entry)
    entry.update(review_scope=SCOPE, next_review=LIMITS)
    notes = dict(prior)
    notes.update(date=DATE, read_scope=SCOPE, previous_review=copy.deepcopy(source), previous_bibliography=previous_entry,
                 previous_notes_file=PRIOR, previous_notes_sha256=PRIOR_SHA, html_read_manifest=manifest,
                 observed_html_assets=manifest, read_groups=groups, activity_followup_catalog=followup,
                 catalog_coverage={**prior['catalog_coverage'], 'read_activity_bodies': 562, 'pending_activity_bodies': 262},
                 new_read_groups=dict(domain_overviews=0, levels=0, activities=47, teacher_resources=0, inline_images=0, supplementary_pdf_urls=0),
                 patterns_reading_log=logs, completed_patterns_records=selected,
                 patterns_pdf_urls_not_reviewed=pdfs, patterns_image_urls_not_reviewed=images,
                 patterns_procedure_scope=dict(activity_procedures=45, family_resource_landing_pages=2),
                 patterns_checked_examples=examples,
                 patterns_cited_works_pending=[
                     dict(linking_pages=[pages[9]['url'],pages[10]['url']], url='https://www.jstor.org/stable/45184560', read_scope='인용된 출판본, 별도 공개 발표 자료와 대조 대기'),
                     dict(linking_pages=[pages[18]['url']], url='https://doi.org/10.5951/jresematheduc.46.5.0511', read_scope='서지 확인'),
                 ],
                 reading_log=prior['reading_log'] + ['규칙성·대수적 사고의 영어 활동 절차 45개와 가정 안내 소개 2개를 대조했다.'],
                 source_corrections=prior['source_corrections'] + [dict(
                     kind='pattern_unit_equation_and_chart_corrections', locations=[pages[i]['url'] for i in (9, 10, 17, 23, 26, 29, 36, 38, 40, 41, 42)],
                     action='반복 단위와 경계, 대응식의 방향, 등호와 수판의 읽기 조건을 구별했다.')],
                 unread_followups=[LIMITS, '규칙성·대수적 사고 활동의 첨부와 연결 원연구를 대조한다.'])
    note_path = ROOT / NOTES
    write(note_path, notes)
    history = source['snapshot_history'] + [dict(snapshot_file=PRIOR, snapshot_sha256=PRIOR_SHA,
                                               date=source['date'], read_scope=source['read_scope'])]
    source.update(date=DATE, snapshot_file=NOTES, snapshot_sha256=sha(note_path), snapshot_history=history,
                  bibliography_snapshot=digest(entry), html_read_manifest=manifest, read_scope=SCOPE, limits=LIMITS,
                  method_note='영어 활동 절차의 반복 단위, 등식, 대응 관계와 수판을 대조했다.',
                  editorial_action='문헌 대응 6건과 자체 관찰 과제 6개를 추가했다.', observations=source['observations'] + OBSERVATIONS)
    for cid, codes, indices, support, limit in CLAIMS:
        registry['claims'].append(dict(id=cid, source_id=SOURCE, role='related_theoretical_context', standard_codes=codes,
                                       locations=[pages[i]['url'] for i in indices], support=support, does_not_establish=limit,
                                       independent_review=False, student_validated=False,
                                       target_snapshots={'revision:' + code: digest(target_value('revision:' + code)) for code in codes}))
    queue_path = ROOT / 'data/content_review_queue.json'
    queue = load(queue_path)
    row = next(row for row in queue['literature_review'] if row['source']['id'] == SOURCE)
    row.update(source=entry, claim_ids=[claim['id'] for claim in registry['claims'] if claim['source_id'] == SOURCE])
    write(bibliography_path, bibliography)
    write(ROOT / 'data/literature_claim_reviews.json', registry)
    write(queue_path, queue)
    build_report()
    print('Reviewed 47 English pages; added 6 mappings and 6 observations. Public activity bodies pending: 262.')


if __name__ == '__main__':
    main()
