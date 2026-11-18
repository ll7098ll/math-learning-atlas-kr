"""Bind public LT2 HTML reading to bounded claims and newly authored observations."""
import copy
import hashlib
import json
from fractions import Fraction

from literature_review import ROOT, digest, target_value, load_registry, build_report
from relation_analysis_review import load_reviews

SOURCE='CLEMENTS_SARAMA_LT'
URL='https://www.learningtrajectories.org/'
SHA='30002cad0913a5e8777a9fbf06fd1e137c93e86c3bdc970457b3af6faf95c85f'
NOTES='data/literature_evidence/CLEMENTS_SARAMA_LT_review_notes.json'
GROUPS={
    'general':['home','explore','about','resources','faq','research'],
    'domain_overviews':['counting','shapes','length','fractions'],
    'levels':['corresponder','counter-small','producer-small','place-value','all-rectangles','shape-identifier','end-to-end','unit-relater','conceptual-ruler','unit-fraction','fraction-maker','fraction-repeater'],
    'activities':['counting-wand','how-many-hand','guess-fraction','guess-rule','building-iteration','hanging-fractions']}

MAPPINGS=[
    ('LT01',['2수01-01','2수03-10','4수01-09'],['FAQ: When are children at a level / Can children work at more than one level / sub-trajectory','소개·영역별 Inclusive Teaching Approaches'],
     '사고·활동·목표를 함께 보되 최초 반응과 도움 후 반응,여러 수행을 구별하는 자체 관찰 설계에 참고한다.',
     '수준은 절대적 단계가 아니며 연령·하위 경로의 변이를 유지한다. 한 응답·이름·교사 도움 뒤 성공을 현재 한국 학생의 인지 단계·보편적 필수 순서·검사 점수로 바꾸지 않는다.'),
    ('LT02',['2수01-01'],['Counting 개요','Corresponder / Counter (Small Numbers) / Producer (Small Numbers)','Counting Wand / How Many in a Hand? 공개 영어 본문'],
     '수 이름 암송·대상과의 일대일 대응·마지막 수의 기수 의미·요청한 개수 만들기를 구별하는 발문에 참고한다.',
     '작은 수량의 활동은 현행0~100 목표 전체의 숙달 증거가 아니다. 함께 센 답과 독립적인 답을 구별하고 운동·말하기 제약을 수량 결손으로 단정하지 않는다.'),
    ('LT03',['2수01-02'],['Counter of Quantitative Units/Place Value'],
     '무엇을 한 단위로 세는지와 묶음 교환의 양 보존을 확인하는 자체 활동에 참고한다.',
     '묶음과 낱개를 함께 다루는 공개 설명이 네 자리 수 전체의 현재 숙달이나 자릿값 완전 숙달을 계산 시작의 선행 관문으로 입증하지 않는다. 물리적 조각 수·수량 단위를 구별한다.'),
    ('LT04',['2수03-04','2수03-05','4수03-10'],['2D Shapes 개요','Shape Recognizer—All Rectangles / Shape Identifier','Guess My Rule: 공개 영어 본문'],
     '모양의 방향·크기와 닫힘·변·각의 조건을 구별하는 자체 분류와 설명에 참고한다.',
     '원문의 사각형 포함 관계와 사다리꼴 정의를 국내 초등의 필수 지도 범위로 옮기지 않는다.1~2학년의 직관적 모양과3~4학년의 간단한 성질을 구별하고 여러 사각형 사이 관계 지도 제외를 보존한다.'),
    ('LT05',['2수03-10','2수03-12'],['Measurement: Length 개요','End-to-End Length Measurer / Length Unit Relater and Repeater / Conceptual Ruler Measurer','Building Up to Iteration: 공개 영어 본문'],
     '같은 길이 단위의 반복·끝점·빈틈과 겹침,어림과 측정 후 비교를 확인하는 자체 활동에 참고한다.',
     '단위 조각 수만 맞거나 수치가 우연히 같아도 올바른 측정이라 판단하지 않는다. 실제 길이·단위가 달라질 조건과 도움을 기록하고 원문의 활동 효과를 현재 학생에게 부여하지 않는다.'),
    ('LT06',['4수01-09','4수01-10','4수01-11','4수01-15'],['Fractions 개요','Unit Fraction Recognizer / Fraction Maker / Fraction Repeater','Guess My Fraction / Hanging Fractions on a Number Line: 공개 영어 본문'],
     '같은 기준 전체·등분한 단위의 반복·1보다 큰 분수와 같은 분모 연산을 설명하는 자체 발문에 참고한다.',
     '분모 역순 비교는 같은 전체의 양의 단위분수 범위를 유지한다. 원문 소개의 의심스러운4/6 예는 복사하지 않는다. 다른 분모 덧셈과 모든 분수 경로를 이 기준의 새 필수 수행으로 넣지 않는다.')]

OBSERVATIONS=[
    dict(id='LT-P1',standard_codes=['2수01-01'],
         question='가상 활동이다. 단추5개를 각각 한 번씩 세고 모두 몇 개인지 설명하라. 다른 곳의 단추 중3개만 골라 접시에 놓아라. 모임을 세는 과제와 필요한 개수를 만드는 과제에서 무엇을 확인했는가? 빈 접시도 기록하라.',
         expected='처음 모임은5개이고 마지막 수5는 모임 전체의 개수다.3개 만들기는 목표3을 유지하며 세 번째에서 멈춰 남은 단추를 옮기지 않는다. 빈 접시는0개다. 수 이름을 길게 암송하는 것만으로 이 수행들이 확인되는 것은 아니다.',
         interpretation='말한 수·가리킨 대상·중복/누락·전체 답·멈춘 시점과 기록을 따로 보존한다. 혼자 한 수행과 함께 센 수행을 구별하고 말·손짓·옮기기 등 사용한 소통 방식을 기록한다. 가상 발문이며 학생 반응·단계 점수·0~100 전체 숙달을 확보한 자료가 아니다.',student_validated=False),
    dict(id='LT-P2',standard_codes=['2수01-02'],
         question='가상 막대는 한 묶음마다 낱개10개다. 두 묶음과 낱개7개의 전체를 낱개 단위로 세라. 한 묶음을 풀어 한 묶음과 낱개17개로 바꾸면 전체는 같은가? 묶음을 하나의 물리적 조각으로 세는 수와 전체 낱개 수를 구별하라.',
         expected='2십+7일=27일이고1십+17일도27일이다. 묶음을 그대로 한 조각으로 세면 처음은2+7=9조각,푼 뒤는1+17=18조각이지만 전체 낱개 수27은 같다. 조각 수만 더해9나18을 전체 낱개 수라고 답하지 않는다.',
         interpretation='단위 이름·묶음 크기·묶음 수·총량과 교환 전후를 함께 기록한다. 학생이 먼저 설명한 방식과 교사가 묶음을 풀어 보인 뒤의 방식을 구별한다. 두 자리 예는 네 자리 이하 자릿값 전체의 검사나 계산 시작 전 완전 숙달의 증거가 아니다.',student_validated=False),
    dict(id='LT-P3',standard_codes=['2수03-04','2수03-05','4수03-10'],
         question='교사가 만든 가상 카드에는 닫힌 삼각형,직사각형과 그것을 돌린 모양,직각이 없는 평행사변형,정사각형이 있다.1~2학년에서는 닫힌 경계를 따라 변·꼭짓점을 세고 같은 모양의 방향 변화를 설명하라.3~4학년에서는 직사각형·정사각형의 변과 직각 조건을 조작으로 확인하라.',
         expected='삼각형은 변·꼭짓점3개,각 사각형은4개다. 돌린 직사각형도 네 직각과 마주 보는 변의 길이가 유지된다. 네 직각이 없는 평행사변형을 두 변이 길고 두 변이 짧다는 이유만으로 직사각형이라 하지 않는다. 정사각형은 네 직각과 같은 네 변을 확인한다.',
         interpretation='방향·색·전형적 외형과 변·각 조건을 구별한다. 손그림의 흔들림과 의도된 열린 경계도 구별한다. 정사각형이 직사각형 조건도 만족한다는 사실은 교사용 검산이며 여러 사각형 사이 포함 관계 지도를 학생 필수 수행으로 요구하지 않는다. 실제 학생·도형 활동 효과를 검증한 기록이 아니다.',student_validated=False),
    dict(id='LT-P4',standard_codes=['2수03-10','2수03-12'],
         question='길이 숫자를 알려 주지 않은 실제 띠를 먼저 어림하고,기록한 뒤 같은 단위를 반복해 재어 비교하라. 다음 가상 오류 검토는 어림 기록 뒤에 별도로 제시한다:2cm 막대4개를 놓았다는 사실만으로 정확한 측정인가? 빈틈과 겹침이 서로 같은 길이만큼 있으면 숫자가 맞아도 올바른지 설명하라.',
         expected='8cm는1cm 간격8개 또는2cm 단위4번이다. 단위 길이가 같고 시작부터 끝까지 빈틈·겹침 없이 이어야 한다. 빈틈1cm·겹침1cm가 있어 합계8cm가 나와도 덮지 못한 부분과 중복이 있으므로 올바른 측정이 아니다. 어림값은 측정 전 기록하고 측정값과 차이를 비교한다.',
         interpretation='양 보존·단위 크기·반복 위치·끝점·개수를 따로 확인한다. 검산용 구간[0,2],[3,5],[5,7],[6,8]은 길이 합8이지만2~3이 비고6~7이 겹친다. 구간 표기는 교사용 확인이며 학생에게 좌표 형식을 새로 요구하지 않는다. 실제 띠를 제공할 때에는 길이를 먼저 알려 주지 않고 어림 기록 뒤 측정한다.',student_validated=False),
    dict(id='LT-P5',standard_codes=['4수01-09','4수01-11'],
         question='같은 전체를 나타내는 두 띠를 각각3등분·6등분했을 때 한 조각의 분수를 비교하라. 이어 한 전체가12cm인 띠의1/3과 다른 전체가24cm인 띠의1/6의 실제 길이를 비교하라. 실제 길이가 같으면 수로서의1/3과1/6도 같은가?',
         expected='같은 전체에서는1/3이1/6보다 크고1/3은1/6 두 개와 같다.12cm의1/3과24cm의1/6은 각각4cm여서 실제 길이는 같지만 두 분수의 기준 전체가 다르다. 수로서1/3과1/6이 같은 것은 아니다. 각 띠의 등분과 기준 전체를 표시해야 한다.',
         interpretation='분수 값·기준 전체·실제 양과 조각 수를 따로 기록한다. 분모가 크면 항상 작다는 말을 분자가 다른 임의 분수로 확장하지 않는다. 이 수치·띠는 자체 설계이며 원문의 그림이나 학생 반응을 전사한 것이 아니다.',student_validated=False),
    dict(id='LT-P6',standard_codes=['4수01-10','4수01-15'],
         question='같은 기준 전체의1/5 길이 조각7개를 이어 수직선에 놓고 분수와 대분수로 나타내라. 그중4개와3개를 합할 때4/5+3/5=7/10이라는 가상 오답 예를 검토하라. 조각 한 개·전체1·전체를 넘는 양을 구별하라.',
         expected='1/5 조각5개가 전체1이고2개가 남으므로7/5=1과2/5다. 같은1/5 단위4개와3개를 합하면7개,곧7/5이며 분모5는 유지된다.7/10은1보다 작아4/5보다도 작으므로 이 양의 덧셈의 합이 될 수 없다.',
         interpretation='전체를 넘는 반복·같은 단위·등호와 대분수의 묶음을 설명하게 한다. 서로 다른 크기의 전체에서 가져온1/5 조각을 섞지 않는다. 다른 분모의 통분을 필수 선수로 추가하지 않고 가상 오답을 실제 학생 응답으로 집계하지 않는다.',student_validated=False)]


def verify():
    assert len(set(sum(GROUPS.values(),[])))==28
    assert len(set(c for m in MAPPINGS for c in m[1]))==11
    assert len(set(o['id'] for o in OBSERVATIONS))==6
    targets=set(c for m in MAPPINGS for c in m[1])
    assert all(set(o['standard_codes'])<=targets and o['student_validated'] is False for o in OBSERVATIONS)
    assert len(set(range(5)))==5 and len(set(range(3)))==3
    assert 2*10+7==1*10+17==27 and 2+7==9 and 1+17==18
    def edges(points):
        return [(points[(i+1)%len(points)][0]-x,points[(i+1)%len(points)][1]-y) for i,(x,y) in enumerate(points)]
    def right_angles(points):
        e=edges(points)
        return [e[i][0]*e[(i+1)%len(e)][0]+e[i][1]*e[(i+1)%len(e)][1]==0 for i in range(len(e))]
    rect=[(0,0),(4,0),(4,2),(0,2)]; rotated=[(-y,x) for x,y in rect]
    square=[(0,0),(2,0),(2,2),(0,2)]; parallelogram=[(0,0),(4,0),(5,2),(1,2)]
    assert all(right_angles(rect)) and all(right_angles(rotated)) and all(right_angles(square))
    assert not any(right_angles(parallelogram))
    assert sorted(x*x+y*y for x,y in edges(rect))==sorted(x*x+y*y for x,y in edges(rotated))==[4,4,16,16]
    assert [x*x+y*y for x,y in edges(square)]==[4,4,4,4]
    intervals=[(0,2),(3,5),(5,7),(6,8)]
    coverage=[sum(a<=i and i+1<=b for a,b in intervals) for i in range(8)]
    assert sum(b-a for a,b in intervals)==8
    assert coverage==[1,1,0,1,1,1,2,1] and coverage.count(0)==coverage.count(2)==1
    assert Fraction(1,3)>Fraction(1,6) and Fraction(1,3)==2*Fraction(1,6)
    assert 12*Fraction(1,3)==24*Fraction(1,6)==4
    assert 7*Fraction(1,5)==Fraction(7,5)==1+Fraction(2,5)
    assert Fraction(4,5)+Fraction(3,5)==Fraction(7,5) and Fraction(7,10)<Fraction(4,5)
    assert Fraction(3,4)+Fraction(1,3)==Fraction(13,12)
    assert Fraction(3+1,4+3)==Fraction(4,7) and Fraction(4,6)==Fraction(2,3)<Fraction(3,4)


def main():
    verify(); registry=load_registry(); before=set(load_reviews()['records'])
    if SOURCE in registry['sources']:
        print('LT2 public reading and targets remain current; no automatic refresh'); build_report(); return
    assert not {m[0] for m in MAPPINGS}&{c['id'] for c in registry['claims']}
    cached=ROOT/'tmp/literature/lt2'
    manifest=json.loads((cached/'manifest.json').read_text(encoding='utf-8'))
    assert {a['key'] for a in manifest}==set(sum(GROUPS.values(),[]))
    for a in manifest:
        assert a['status']==200 and a['url']==a['final_url']
        assert a['url'].startswith(URL)
        assert hashlib.sha256((ROOT/a['file']).read_bytes()).hexdigest()==a['sha256']
    assert next(a for a in manifest if a['key']=='home')['sha256']==SHA
    assets=[{k:a[k] for k in ['key','url','title','sha256','status']} for a in manifest]
    notes=dict(source_id=SOURCE,source_url=URL,source_asset_kind='publisher_html',source_asset_sha256=SHA,source_asset_redistributed=False,
        date='2026-11-06',reviewer='Codex',contains_source_full_text=False,source_pdf_redistributed=False,pdf_read=False,original_page_layout_review=False,
        primary_asset_note='기준 자산 해시는 공식 홈페이지HTML 한 파일이다. 나머지27개HTML의 주소·해시는 observed_html_assets에 각각 보존하며 홈페이지 해시를 사이트 전체 해시로 부르지 않는다.',
        observed_html_assets=assets,read_groups=GROUPS,
        reading_log=['공식 공개HTML28개의 지정 영어 본문을 읽었다. 일반 소개·목록·FAQ·서지·연구 목록6개,영역 개요4개,수준12개,활동6개다. 영역 전체의 모든 수준·활동을 읽었다는 집계가 아니다.',
            '세기4수준·평면도형2수준·길이3수준·분수3수준의 설명·사례·교수 안내와 활동 목록을 확인했다.',
            'Counting Wand,How Many in a Hand?,Guess My Fraction,Guess My Rule,Building Up to Iteration,Hanging Fractions의 공개 영어 목표·절차·교수 팁·차별화·표시된 참고문헌을 확인했다. 소개만 읽은 것이 아니며 영어·스페인어의 동등성을 검증한 것도 아니다.',
            '홈페이지의0~8세 대상,FAQ의 수준/하위 경로/연령 한계,자원 페이지의2026년 권장 인용과 꼬리말의2017/2019 표기를 구별했다. 연구 목록의 논문 서지 확인을 원논문 독해로 집계하지 않는다.'],
        source_corrections=[dict(kind='source_incorrect_example_transcription_guard',location='Fractions 개요',
            observed='3/4+1/3의 잘못된 덧셈 예에4/6이 적혀 있다.',correct_sum='13/12',sum_numerators_and_denominators='4/7',
            action='원문 자체가 오답을 논하는 대목이나4/6은 분자끼리·분모끼리 더한 결과4/7과도 다르다. 원인을 확정하지 않고 기호를 복사하지 않는다. 올바른 합과 가상 오답을 구별하며 이 다른 분모 계산을 국내3~4학년 필수 과제로 전용하지 않는다.'),
            dict(kind='bibliographic_version_guard',location='Resources의Suggested Citation / 공통 꼬리말',observed='자원 페이지는2026년 인용을 권장하고 꼬리말은2017/2019를 유지한다.',
                action='이번 온라인 자원 서지는2026년 권장 인용과 확인일을 사용한다. 개별 활동의2025·2026 갱신일을 따로 남기고 모든 내용이2026년에 작성됐다고 판단하지 않는다.'),
            dict(kind='scope_and_definition_guard',location='FAQ / Shape Identifier / Guess My Fraction',
                action='하위 경로의 순서·연령 차를 허용하고 사다리꼴 정의와 사각형 포함 관계를 국내 필수 범위로 옮기지 않는다. 분모 역순 비교는 같은 전체의 양의 단위분수로 한정한다.')],
        activity_update_dates={'counting-wand':'2026-03-03','how-many-hand':'2026-03-04','guess-fraction':'2025-07-27','guess-rule':'2026-04-15','building-iteration':'2025-07-23','hanging-fractions':'2026-02-03'},
        unread_followups=['다른 영역·미선정 수준/활동의 본문,회원 전용 자료,동영상·그림·첨부PDF·게임 실행은 미검토다. 링크와 목록의 존재를 그 내용의 검토로 집계하지 않는다.',
            'Research Projects의 서지에 연결된 개별 연구·관련 교재 전권·정오표·현행 한국 학생의 실제 반응과 번역 동등성은 후속 대조 대상이다.'],
        interpretation_limits=['연구자가 제공한 경로·활동 안내에 대한 범위별 읽기다. 현재 과제의 효과 크기·진단 규준·한 필수 선수 경로·한국 학년별 연령 규준을 직접 입증하지 않는다.',
            '현재 목표의 포함 관계 지도 제외·수 범위를 유지한다. 자체 문항·수치·기대 설명은 원문 문항의 복사나 실제 학생 자료가 아니다.',
            '저작권 유보와 사이트 밖 별도 배포 금지 안내를 확인했다. HTML·자료·영상·그림을 재배포하지 않고 자체 기록·주소·해시만 보존한다.'])
    (ROOT/NOTES).write_text(json.dumps(notes,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    path=ROOT/'data/sources.json'; sources=json.loads(path.read_text(encoding='utf-8'))
    b=next(s for s in sources if s['id']==SOURCE); previous=copy.deepcopy(b)
    b.update(title='Learning and Teaching with Learning Trajectories [LT]2',year=2026,accessed='2026-11-06',
        citation_version_note='Resources의2026년 권장 인용을 사용했다. 공통 꼬리말은2017/2019 표기를 유지한다. 개별 활동 갱신일은 읽기 기록에 따로 보존한다.',
        review_scope='공식 공개HTML28개의 지정 영어 본문: 일반·목록·서지6개,세기·평면도형·길이·분수 개요4개,선정12수준·6활동. 이미지·영상·첨부PDF·원연구·교재 전권·스페인어 동등성은 미대조.',
        next_review='미선정 영역·수준·활동,연구 목록의 개별 원논문·관련 교재와 현재 한국어 과제의 실제 반응·교수 효과를 추가 대조한다.')
    registry['sources'][SOURCE]=dict(source_id=SOURCE,state='self_read_claim_mapping',reviewer='Codex',date='2026-11-06',snapshot_kind='authored_review_notes',snapshot_file=NOTES,snapshot_sha256=hashlib.sha256((ROOT/NOTES).read_bytes()).hexdigest(),
        source_asset_kind='publisher_html',source_asset_sha256=SHA,redistribution_license='workspace_authored_notes',bibliography_snapshot=digest(b),previous_bibliography=previous,
        display=dict(title=b['title'],url=URL,authors_year='Clements·Sarama,2026 권장 인용;2026-11-06 확인'),read_scope='공식 공개HTML28개 지정 영어 본문: 일반6·영역 개요4·선정 수준12·활동6;이미지·영상·첨부PDF·개별 원연구는 미대조',
        scope_note='목표·사고 경로·활동을 함께 조사하는 틀로 참고한다. 수준을 절대적 단계·고정 연령·국내 성취기준의 단일 필수 경로로 사용하지 않는다.',
        method_note='세기·평면도형·길이·분수의 공개 수준과6개 활동 절차를 실제 읽고 현재11개 기준의 뜻·풀이·조건과 대조했다. 사이트의 연구 안내·목록과 개별 원논문의 검증을 구별한다.',
        limits='0~8세를 위한 온라인 자원이며 국내 학년 전체·현재 과제 효과·진단 정확도의 직접 근거가 아니다. 미선정 내용·영상·그림·첨부PDF·교재 전권과 원논문은 미검토다. 의심스러운 분수 계산 예는 읽기 기록에서 자체 검산하고 그대로 옮기지 않았다. 원문HTML·자산은 재배포하지 않는다.',
        editorial_action='11개 기준에 주장6건·가상 자체 관찰6건을 추가했다. 세기·개수 만들기,단위 교환,방향과 도형 성질,빈틈과 겹침,같은 전체·단위분수·전체를 넘는 반복을 구별한다. 기존 대표 원고·관계 검토는 유지하고 독립 검토·학생 검증으로 합산하지 않았다.',
        independent_review=False,student_validated=False,observations=OBSERVATIONS)
    for cid,codes,locations,support,limit in MAPPINGS:
        registry['claims'].append(dict(id=cid,source_id=SOURCE,role='related_theoretical_context',locations=locations,support=support,does_not_establish=limit,
            target_snapshots={'revision:'+c:digest(target_value('revision:'+c)) for c in codes},standard_codes=codes,independent_review=False,student_validated=False))
    path.write_text(json.dumps(sources,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (ROOT/'data/literature_claim_reviews.json').write_text(json.dumps(registry,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    path=ROOT/'data/content_review_queue.json'; queue=json.loads(path.read_text(encoding='utf-8'))
    row=next(r for r in queue['literature_review'] if r['source']['id']==SOURCE)
    row.update(source=b,status='self_read_claim_mapping',evidence_file='data/literature_claim_reviews.json',claim_ids=[m[0] for m in MAPPINGS])
    path.write_text(json.dumps(queue,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    assert set(load_reviews()['records'])==before
    load_registry(); build_report()
    print('Added LT2 public reading: 6 scoped claims / 6 own observations; no relation approvals')


if __name__=='__main__':main()
