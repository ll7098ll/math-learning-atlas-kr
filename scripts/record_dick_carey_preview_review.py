"""Register read publisher previews, bounded design claims, and own mathematical probes."""
import copy
import hashlib
import json
from fractions import Fraction

from literature_review import ROOT, digest, target_value, load_registry, build_report
from relation_analysis_review import load_reviews

SOURCE='DICK_CAREY_2014'
URL='https://www.pearson.com/en-gb/subject-catalog/p/systematic-design-of-instruction-the-pearson-new-international-edition/P200000004082?view=educator'
NOTES='data/literature_evidence/DICK_CAREY_2014_review_notes.json'
PDFS={
    'preview40':dict(url='https://api.pageplace.de/preview/DT0400.9781292052663_A24569965/preview-9781292052663_A24569965.pdf',sha256='5b548b0034ef2cb66e53d57b94c1775bae1d7cb790243678e5bfe49c1e0bf506',pages=40,text_pages=list(range(2,41)),visual_pages=[1,2,3,4,7,8,10,13,15,22,26,31,32,37,38,39,40]),
    'sample8':dict(url='https://www.pearson.de/media/muster/ext/9781292052663.pdf',sha256='cd3a72a1d878812b06d508f9727a119657dfa90ca0ca150cbec0ef97e99cc2cd',pages=8,text_pages=list(range(2,9)),visual_pages=[2,3,4,6,7,8])}

MAPPINGS=[
    ('DC01',['6수02-03','6수04-03'],['preview40 PDF9–17 / 국제판4–12·원서16–24','표2.1·Needs Assessment'],
     '자료의 실제 상태·비교 기준·격차의 단위를 구별하고 미응답·도구·시간의 문제를 수학적 결손으로 단정하지 않는 자체 발문에 참고한다.',
     '교재의 설계 사례는 현재 학생 자료나 수업 효과 검증이 아니다. 비율 차와 상대 증가율을 구별하며 같은 집단·정의·분모의 비교인지 확인한다.'),
    ('DC02',['6수04-01','4수01-06'],['preview40 PDF18–28 / 국제판13–23·원서25–35','Clarity in Instructional Goals / 목표 평가 표와 연습'],
     '교사가 한 활동과 학습자가 설명할 수행을 구별하고 도구·조건·결과를 함께 명시하는 자체 목표 설계에 참고한다.',
     '명료한 문장·필드의 존재가 실제 학생의 이해·독립 수행·효과를 입증하지 않는다. 자체 관찰의 기대 설명을 이미 수집한 응답으로 바꾸지 않는다.'),
    ('DC03',['4수01-04','4수01-06','6수04-03'],['preview40 PDF31–33·37–40 / 국제판26–28·32–35·원서38–40·44–47','Goal Analysis Procedures의 순서·분기·반복 도식'],
     '해당 수행 경로의 순서·분기와 대안 풀이를 구별하는 자체 기록에 참고한다.',
     '한 수행에서 양쪽 분기를 모두 실행하지 않는다는 설명과 전체 목표 범위에서 여러 조건에 대비해 학습할 필요는 구별한다.5–15단계의 경험적 지침을 모든 과제의 수·시간 규칙으로 강제하지 않고 절차 화살표를 보편적 선수 관계로 승격하지 않는다.'),
    ('DC04',['9수03-15'],['preview40 PDF33–37 / 국제판28–32·원서40–44','Verbal Information / Intellectual Skills / 표3.1'],
     '정리의 말·기호 회상,조건에 맞는 적용,정당화라는 서로 다른 수행을 확인하는 자체 발문에 참고한다.',
     '원전의 학습 유형 비교는 진단 단계 규준이나 모든 학생의 필수 순서를 입증하지 않는다. 피타고라스식에는 직각변·빗변·양의 길이 조건을 명시하고 수치 대입만으로 일반 정당화를 완료했다고 하지 않는다.'),
    ('DC05',['4수03-10','6수04-01'],['sample8 PDF3–5 / 국제판115–117·원서127–129','수행목표 평가 표·연습·피드백'],
     '수학적 수행·사용 도구·응답 방식·판정 근거의 일치를 확인하는 자체 평정 설계에 참고한다.',
     '동그라미 같은 답안 동작과 분류·설명의 내용을 구별한다. 특정 필기 방식의 어려움을 수학적 결손으로 확정하지 않고 여러 사각형 포함 관계 지도 제외를 유지한다. 이 평정안의 진단 타당성은 검증하지 않았다.'),
    ('DC06',['4수01-06','6수04-03','9수03-15'],['sample8 PDF6–8 / 국제판118–120·원서130–132','Criterion-Referenced Assessment / Entry Skills Tests'],
     '특정 설계에서 가정한 출발 기능과 목표 수행을 구별하고 실제 응답으로 가정을 재확인하는 자체 관찰에 참고한다.',
     '원문도 가정한 출발 기능이 실제로 핵심이 아닐 수 있음을 허용한다. 하위 기능 분석 장 전체·사전/연습/사후 검사 설명의 나머지는 미검토이며 현재 선수 관계·검사 도구·교수 효과의 실증 검증으로 집계하지 않는다.')]

OBSERVATIONS=[
    dict(id='DC-P1',standard_codes=['6수02-03','6수04-03'],
         question='가상 설문에서 응답 완료율의 목표가75%,현재 기록이60%다. 기준을100명에 대응해 차와 현재를 기준으로 한 증가 비율을 구별하라. 미응답을 수학 문제의 오답으로 기록해도 되는가? 비교 전에 무엇을 확인할 것인가?',
         expected='100명에 대응하면 목표75명·현재60명의 차는15명,비율 차는15퍼센트포인트다. 현재60을 기준으로 한 증가는15/60=1/4=25%다. 두 수는 기준이 달라 같은 뜻이 아니다. 미응답은 오답과 다르고 같은 조사 범위·기간·응답 완료 정의·분모인지 확인해야 한다.',
         interpretation='백분율을 실제100명 조사로 바꾸지 않고 대응 모형으로 표시한다. 퍼센트포인트 명칭과 상대 변화 계산은 교사용 확장이며 기준량을 말·분수·그림으로 설명하는 것도 허용한다. 가상 비율로 자료 수집·학생 능력·결손의 원인·개선 효과를 확정하지 않는다.',student_validated=False),
    dict(id='DC-P2',standard_codes=['6수04-01'],
         question='교사가 블록을 나누어 준다와 학생이 같은 단위 자료3·5·10의 평균과 균등화 이유를 설명한다는 문장을 비교하라. 두 번째 목표에 사용할 도구와 도움 여부를 먼저 정하고 학생에게 합·자료 수·평균을 설명하게 하라.',
         expected='합18을 세 자료에 균등하게 나누면6이다.10에서3을3인 곳으로,1을5인 곳으로 옮겨6·6·6을 만들면 합18과 자료 수3이 유지된다. 원래 자료에6이 없어도 평균은6이다. 교사가 옮겼다는 활동만으로 학생이 이 이유를 설명했다고 기록할 수 없다.',
         interpretation='학습자의 설명·조작·계산과 교사의 제시를 따로 기록한다. 블록·그림·식 중 어떤 도구를 제공했는지,이동 방법을 알려 주었는지 보존한다. 답6만으로 총량 보존·평균 의미 전체를 확인했다고 하지 않고 자체 발문을 실제 반응으로 집계하지 않는다.',student_validated=False),
    dict(id='DC-P3',standard_codes=['4수01-04'],
         question='가상 과제18×14의 계산 원리를 한 방법으로 먼저 설명하라. 이후 비교용으로18×(10+4)와(20−2)×14의 과정을 검토하라. 한 경로의 부분 계산을 모두 하는 것과 두 경로를 동시에 해야 한다는 요구를 구별하라.',
         expected='첫 경로는180+72=252,둘째는280−28=252다. 각 경로에서 필요한 부분 계산과 합·차가 완성되어야 한다. 배열을(10+8)×(10+4)로 나누면100+40+80+32=252이고 교차 부분을 빠뜨리지 않는다. 한 답을 구하는 데 두 대안 경로를 모두 실행해야 하는 것은 아니다.',
         interpretation='먼저 선택한 경로·각 부분의 의미·검산과 이후 비교를 구별한다. 이 과제의 한 경로 성공을 기준 전체의 모든 수 범위·원리 숙달로 확대하지 않는다. 다른 조건에서 필요한 방법을 배울 필요와 한 실행에서 대안을 모두 거쳐야 한다는 주장은 다르다. 특정 절차를 보편적 선수로 승인하지 않는다.',student_validated=False),
    dict(id='DC-P4',standard_codes=['9수03-15'],
         question='피타고라스 정리의 식을 말하기,두 직각변이5cm·12cm인 직각삼각형의 빗변을 구하기,정리를 일반적으로 정당화하기는 같은 수행인가?5·5·6인 삼각형에도 두 작은 변의 제곱합을 가장 긴 변의 제곱과 같다고 써도 되는가?',
         expected='직각삼각형에서는5²+12²=169이므로 빗변은 양의 길이13cm다. c²=169의 음수해−13은 길이로 쓰지 않는다.5·5·6은 삼각형이지만25+25≠36이므로 그 식을 적용할 직각 조건이 없다. 식의 회상·수치 적용·일반 정당화는 각각 확인해야 한다.',
         interpretation='a,b의 직각변 역할·c의 빗변·단위·양의 길이 조건을 기록한다. 위 계산만으로 임의의 직각삼각형에 대한 넓이 보존 정당화를 수행했다고 집계하지 않는다. 기존 일반 정당화 과제는 유지하고 이 발문 하나로 인지 단계·교수 효과·정리 전체 숙달을 판정하지 않는다.',student_validated=False),
    dict(id='DC-P5',standard_codes=['4수03-10'],
         question='가상 평정안은 직사각형을 골라 이유를 설명하는 목표를 맞는 그림에 동그라미를 그렸는가 하나로만 판정한다. 손짓으로 골라 네 직각을 설명한 기록과,동그라미는 맞게 그렸지만 두 변이 길고 두 변이 짧아서라는 이유만 적은 기록을 같은 근거로 취급해도 되는가?',
         expected='선택 결과·응답 동작·직각 조건에 대한 설명은 별도 근거다. 손짓의 기록도 대상과 설명이 명확하면 수학적 수행을 확인할 수 있다. 두 변이 길고 두 변이 짧은 평행사변형도 있을 수 있으므로 그 이유만으로 직사각형을 정의할 수 없다. 답안 방식 하나로 분류와 설명의 목표를 모두 판정하지 않는다.',
         interpretation='이는 가상 기록 비교이고 실제 학생 평가가 아니다. 제시한 모양·도구·요청한 수행·관찰한 이유를 보존하고 소통·운동의 제약과 수학적 판단을 구별한다. 초등에서 여러 사각형 사이 포함 관계 지도를 필수로 넣지 않으며 평정안을 검증된 진단 도구로 부르지 않는다.',student_validated=False),
    dict(id='DC-P6',standard_codes=['4수01-06'],
         question='73÷5를 자연수 몫·나머지로 답하고 왜 나눗셈이 끝났는지 설명하라.73=5×13+8이므로 몫13·나머지8이라는 가상 오답 예를 검토하라. 교사가5×14를 알려 준 뒤 나온 답과 아무 도움 없이 한 설명을 어떻게 구별해 기록할 것인가?',
         expected='몫14·나머지3이며5×14+3=73과0≤3<5를 함께 만족한다. 나머지8에서는5개를 한 번 더 나눌 수 있어 끝나지 않았다. 그림·반복 배분·부분 몫·계산 중 사용한 방법과 도움 전후를 기록한다. 답14·3이 맞다는 사실만으로5단의 독립 암산이나 모든 출발 기능을 확인했다고 하지 않는다.',
         interpretation='특정 경로에서 실제 사용한 기능과 사전에 가정한 기능을 구별하고 필요하면 다른 수·표현으로 다시 확인한다. 도움 뒤 성공을 사전 능력으로 소급하지 않는다. 원전의 출발 기능 검사는 설계 가정을 확인할 참고 틀이며 이 자체 활동의 진단 정확도나 모든 나눗셈 경로의 필수 선수성을 검증하지 않았다.',student_validated=False)]


def verify():
    assert len(MAPPINGS)==len(OBSERVATIONS)==6
    assert len(set(c for m in MAPPINGS for c in m[1]))==7
    assert sum(len(p['text_pages']) for p in PDFS.values())==46
    assert sum(len(p['visual_pages']) for p in PDFS.values())==23
    assert Fraction(75,100)-Fraction(60,100)==Fraction(15,100)
    assert Fraction(75-60,60)==Fraction(1,4) and Fraction(1,4)*100==25
    assert sum([3,5,10])==18 and 18/3==6 and [3+3,5+1,10-4]==[6,6,6]
    assert 18*14==18*10+18*4==20*14-2*14==100+40+80+32==252
    assert 5**2+12**2==13**2==169 and (-13)**2==169
    assert 5+5>6 and 5**2+5**2!=6**2
    # An independent geometric counterexample to the long/short-side criterion.
    edges=[(4,0),(1,2),(-4,0),(-1,-2)]
    assert sorted(x*x+y*y for x,y in edges)==[5,5,16,16]
    assert all(edges[i][0]*edges[(i+1)%4][0]+edges[i][1]*edges[(i+1)%4][1]!=0 for i in range(4))
    assert divmod(73,5)==(14,3) and 5*13+8==73 and not 0<=8<5
    assert 90-77==13 and 95-81==14 and Fraction(90-77,77)*100!=13
    assert Fraction(95-81,81)*100!=14 and 150-90==60


def main():
    verify();registry=load_registry();before=set(load_reviews()['records'])
    if SOURCE in registry['sources']:
        print('Dick/Carey preview reading and targets remain current; no automatic refresh');build_report();return
    assert not {m[0] for m in MAPPINGS}&{c['id'] for c in registry['claims']}
    assets=[]
    for key,spec in PDFS.items():
        stem=f'DICK_CAREY_2014_{key}';file=ROOT/f'tmp/literature/{stem}.pdf'
        assert hashlib.sha256(file.read_bytes()).hexdigest()==spec['sha256']
        pages=json.loads((ROOT/f'tmp/literature/{stem}_pages.json').read_text(encoding='utf-8'))
        assert len(pages)==spec['pages']
        images=[]
        for p in spec['visual_pages']:
            image=ROOT/f'tmp/literature/{stem}-p{p}.png'
            images.append(dict(pdf_page=p,sha256=hashlib.sha256(image.read_bytes()).hexdigest()))
        assets.append(dict(key=key,url=spec['url'],sha256=spec['sha256'],pdf_pages=spec['pages'],text_read_pdf_pages=spec['text_pages'],visually_reviewed_pages=images,redistributed=False))
    notes=dict(source_id=SOURCE,source_url=URL,source_pdf_sha256=PDFS['preview40']['sha256'],date='2026-11-06',reviewer='Codex',
        contains_source_full_text=False,source_pdf_redistributed=False,pdf_assets=assets,
        reading_log=['국제판의40쪽 미리보기와8쪽 발췌에서 지정46쪽의 추출텍스트를 읽었다. 미리보기PDF2–40·발췌PDF2–8이며 텍스트 없는 두 겉표지는 텍스트 쪽 수에 넣지 않는다. 표제의 중복과 미리보기PDF6의 빈 쪽 안내가 포함된다.',
            '미리보기의 국제판1장 목표 동정·요구 분석·사례·평가 표·연습·참고문헌 전체(국제판2–25,원서14–37)와2장 목표 분석 앞부분(국제판26–35,원서38–47)을 확인했다.',
            '발췌의 수행목표 평가 표·연습·피드백·참고문헌과 평가 도입·출발 기능 검사(국제판115–120,원서127–132)를 읽었다. 다른 검사 유형의 전체 설명은 이어지는 쪽에 있어 미검토다.',
            '선정23쪽의 전체 페이지 이미지를 확인했다. 두 쪽에 걸친 설계모형의 병행·수정 화살표,표2.1·2.2·3.1,목표/수행목표 평가 표,조건 분기·연결·반복 도식과 본문을 대조했다.'],
        source_corrections=[
            dict(kind='edition_and_text_layer_guard',location='preview40 PDF2–5·7·31 / sample8 PDF2·6',
                action='2014년7판 국제판의 표제와 서지를 이미지로 확인했다. 본문은2009년 원서 장을 재수록하여 국제판 목차·하단 쪽 번호와 원서 번호가 다르며 PDF 물리 쪽도 구별한다. 서지는 판면의 인쇄ISBN9781292041254를 사용하고 추출층에 겹쳐 나온 다른ISBN을 혼합하지 않는다.'),
            dict(kind='percentage_point_and_rate_guard',location='preview40 PDF13·15 / 국제판8·10·원서20·22',
                observed='목표90%·현재77%의 차를13%,목표95%·현재81%의 차를14%로 표현하는 대목이 있다.',
                action='차는 각각13·14퍼센트포인트로 구별한다. 상대 증가율은 현재를 분모로 하므로 각각13/77·14/81이다. 교재 사례의 수치를 현재 학생 자료나 개선 효과로 옮기지 않는다.'),
            dict(kind='bound_not_exact_value_guard',location='preview40 PDF11·13 / 국제판6·8·원서18·20',
                action='평균 대기가2분30초 초과이고 목표90초인 설명에서 격차는60초 초과다. 표의60초 표현을 정확한 관측 차라고 복사하지 않으며 실제 평균을 새로 지어내지 않는다.'),
            dict(kind='illustration_and_heuristic_guard',location='preview40 PDF37·40 / 국제판32·35·원서44·47',
                action='표3.1의 유형 대응은 예시라는 원문의 한계를 유지한다.1~2시간당5–15단계라는 경험적 지침을 현재435기준·870목표의 단계 수 또는 시간 규칙으로 강제하지 않는다.'),
            dict(kind='mathematical_rule_condition_guard',location='preview40 PDF34 / 국제판29·원서41',
                action='피타고라스식의 역할 예를 실제 수학 과제로 쓸 때 a,b는 직각변,c는 빗변이며 길이는 양수라는 조건을 명시한다. 원전이 모든 삼각형에 적용한다고 주장한 것으로 해석하거나 수치 적용을 일반 정당화로 바꾸지 않는다.')],
        unread_followups=['목표 분석 장의 나머지와 하위·출발 기능 분석 장 본문 전체,학습자·맥락 분석 및 수행목표/평가 장의 미포함 부분·형성평가·부록·인용 원연구는 미검토다.',
            '공식 미리보기에 없는 본문을 다른 판본·2차 요약으로 대신 읽었다고 하지 않는다. 실제 독립 검토·익명 학생 반응·수정 후 재검증은 별도 근거가 필요하다.'],
        interpretation_limits=['설계 원전의 지정 범위 읽기다. IES식 권고 등급·현재 과제의 인과 효과·진단 규준·유일한 한국 성취기준 선수 순서의 직접 근거가 아니다.',
            '학습자와 맥락 분석은 내용 분석과 병행·반복할 수 있다. 자체 발문의 기대 설명을 실제 관측이나 원전의 검증 결과로 집계하지 않는다.',
            '파일 두 개의 물리 쪽은48쪽이나46쪽의 추출텍스트와23쪽 이미지를 확인한 범위이며 중복 표제·서지·빈 쪽이 포함된다. 원전 전권의48쪽을 새로 읽었다는 뜻이 아니다. 저작권 유보 PDF·이미지는 재배포하지 않는다.'])
    (ROOT/NOTES).write_text(json.dumps(notes,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    path=ROOT/'data/sources.json';sources=json.loads(path.read_text(encoding='utf-8'))
    b=next(v for v in sources if v['id']==SOURCE);previous=copy.deepcopy(b)
    b.update(title='The Systematic Design of Instruction, Seventh Edition, Pearson New International Edition',publisher='Pearson Education Limited',isbn='9781292041254',ebook_isbn='9781292052663',
        kind='교수설계 원전의 공식 미리보기·발췌 범위 검토',
        review_scope='40쪽 미리보기·8쪽 발췌의 지정46쪽 텍스트·선정23쪽 이미지. 목표 동정 장,목표 분석 앞부분,수행목표 평가 표와 평가 도입·출발 기능 검사. 하위 기능 장 전체와 전권·미포함 본문은 미검토.',
        next_review='목표 분석 나머지와 하위·출발 기능 분석 장 본문,학습자·맥락 분석·평가 장의 미포함 부분·형성평가·부록·인용 연구 및 실제 학생 반응을 추가 대조한다.')
    registry['sources'][SOURCE]=dict(source_id=SOURCE,state='self_read_claim_mapping',reviewer='Codex',date='2026-11-06',snapshot_kind='authored_review_notes',snapshot_file=NOTES,snapshot_sha256=hashlib.sha256((ROOT/NOTES).read_bytes()).hexdigest(),source_pdf_sha256=PDFS['preview40']['sha256'],redistribution_license='workspace_authored_notes',bibliography_snapshot=digest(b),previous_bibliography=previous,
        display=dict(title=b['title'],url=URL,authors_year='Dick·Carey·Carey,2014,7판 국제판;본문2009년 원서 재수록'),read_scope='두 공식PDF의 지정46쪽 추출텍스트·선정23쪽 이미지;목표 동정·목표 분석 앞부분·수행목표 평가 표·평가 도입·출발 기능 검사',
        scope_note='목표·수행·조건·평가의 일치를 점검하는 설계 틀이다. 특정 수행 경로와 선수 가정을 구별하며 현재 학생의 단계·수업 효과·보편적 필수 순서를 직접 입증하지 않는다.',
        method_note='국제판과 원서·PDF의 장/쪽 번호를 대조했다. 목표 분석 앞부분과 출발 기능 검사 대목을 읽었지만 하위 기능 분석 장 전체를 읽은 상태는 아니다. 자체 예의 수치·도구·도움 여부·판정 근거를 원문 사례와 구별했다.',
        limits='원전 전권이나 모든 장을 읽은 상태가 아니다. 목차에 있는 장과 실제 확보한 본문을 구별하고 인용 원연구·한국어 과제 효과는 미검토다. 수치 사례의 퍼센트포인트·격차 하한과 단계 수 지침을 별도 기록했다. 저작권 유보 PDF·이미지는 재배포하지 않는다.',
        editorial_action='현재7개 기준에 주장6건·가상 자체 관찰6건을 대응했다. 새 비율 대응은 분리 보존된 초기 대표 원고 본문도 별도 해시로 연결했다. 기존 대표 원고·관계 검토를 바꾸거나 신규 관계 승인·독립 검토·학생 검증으로 합산하지 않았다.',independent_review=False,student_validated=False,observations=OBSERVATIONS)
    for cid,codes,locations,support,limit in MAPPINGS:
        snapshots={'revision:'+c:digest(target_value('revision:'+c)) for c in codes}
        if '6수02-03' in codes:snapshots['initial:6수02-03']=digest(target_value('initial:6수02-03'))
        registry['claims'].append(dict(id=cid,source_id=SOURCE,role='related_theoretical_context',locations=locations,support=support,does_not_establish=limit,target_snapshots=snapshots,standard_codes=codes,independent_review=False,student_validated=False))
    path.write_text(json.dumps(sources,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (ROOT/'data/literature_claim_reviews.json').write_text(json.dumps(registry,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    path=ROOT/'data/content_review_queue.json';queue=json.loads(path.read_text(encoding='utf-8'))
    row=next(r for r in queue['literature_review'] if r['source']['id']==SOURCE)
    row.update(source=b,status='self_read_claim_mapping',evidence_file='data/literature_claim_reviews.json',claim_ids=[m[0] for m in MAPPINGS])
    path.write_text(json.dumps(queue,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    assert set(load_reviews()['records'])==before
    load_registry();build_report()
    print('Added Dick/Carey preview review: 6 scoped claims / 6 own observations; no relation approvals')


if __name__=='__main__':main()
