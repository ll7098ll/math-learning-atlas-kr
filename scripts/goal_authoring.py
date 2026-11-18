"""Shared authoring helpers; stable goals, scoped conditions and durable reviews."""
import hashlib
import json
from pathlib import Path
from datetime import date

ROOT=Path(__file__).resolve().parents[1]
AUTHOR_DATE=date.today().isoformat()
REVIEW=dict(state='self_checked',reviewer='Codex',date=AUTHOR_DATE,independent_review=False,student_validated=False)


def condition(text,kind='within_task',ref=None,reason=None,targets=None):
    return dict(text=text,kind=kind,**({'goal_id':ref} if ref else {}),**({'applies_to_goal_ids':targets} if targets else {}),rationale=reason or text)


def route(key,title,conditions,steps,result,question,expected):
    return dict(id=key,title=title,operator='AND',conditions=[c['text'] for c in conditions],
                condition_sources=[dict(condition_index=i,**{k:v for k,v in c.items() if k!='text'}) for i,c in enumerate(conditions)],
                steps=steps,result=result,diagnostic=dict(question=question,expected=expected))


class GoalAuthor:
    def __init__(self):
        self.entries=[];self.cases=[];self.code=None
        self.standards={s['code']:s for s in json.loads((ROOT/'data/standards.json').read_text(encoding='utf-8'))['standards']}

    def standard(self,code,scope,goals,pdf_pages,printed_pages):
        self.code=code
        official=self.standards[code]['statement_display']
        norm=lambda s:''.join(s.split())
        assert all(norm(span) in norm(official) for _,_,span,_ in goals),code
        self.entries.append(dict(code=code,official_goal=official,scope=scope,
            goals=[dict(id=code+':'+key,title=title,official_span=span,success=success) for key,title,span,success in goals],
            source_review=dict(kind='curriculum_text_and_application_notes',source_id='CURRICULUM_2022_33',pdf_pages=pdf_pages,printed_pages=printed_pages,
                               scope='공식 문장과 해설 및 적용 시 고려 사항의 텍스트 대조. 원문 이미지 대조 상태는 별도로 유지한다.'),review=dict(REVIEW)))

    def case(self,key,title,goals,goal,task,shared,routes,note):
        self.cases.append(dict(id='early-'+self.code+'-'+key,standard=self.code,title=title,goal_ids=[self.code+':'+g for g in goals],
            goal=goal,task=task,shared_conditions=shared,routes=routes,route_relationship='alternative_explanations',alternative_review=note,notes=note,review=dict(REVIEW)))

    def write(self,filename,scope,expected_codes):
        assert {e['code'] for e in self.entries}==set(expected_codes)
        for entry in self.entries:
            for goal in entry['goals']:
                goal['case_ids']=[c['id'] for c in self.cases if goal['id'] in c['goal_ids']]
                assert goal['case_ids'],goal['id']
        for case in self.cases:
            for route in case['routes']:
                for source in route['condition_sources']:
                    source.setdefault('applies_to_goal_ids',list(case['goal_ids']))
                    assert source['applies_to_goal_ids'] and set(source['applies_to_goal_ids'])<=set(case['goal_ids'])
        path=ROOT/'data'/filename
        previous=json.loads(path.read_text(encoding='utf-8')) if path.exists() else {}
        from complete_content_gaps import alternative_record
        for case in self.cases:
            if len(case['routes'])==1:
                case['alternative_decision']=alternative_record(case)
                case['alternative_review']=case['alternative_decision']['reason']+' '+case['alternative_decision']['decision']
                if case['standard']=='12확통02-06':
                    case['alternative_decision']['auxiliary_check']='조합법은 확률값의 검산으로 사용한다. 곱셈정리 설명은 조건부확률 경로를 유지한다.'
                    case['alternative_review']+=' '+case['alternative_decision']['auxiliary_check']
        for key,records,id_key in [('entries',self.entries,'code'),('cases',self.cases,'id')]:
            old={r[id_key]:r for r in previous.get(key,[])}
            for record in records:
                prior=old.get(record[id_key])
                body=lambda r:{k:v for k,v in r.items() if k not in ('review','history')}
                changed=prior is not None and body(prior)!=body(record)
                if prior and not changed:record['review']=prior['review']
                if changed:
                    assert not prior['review'].get('independent_review') and not prior['review'].get('student_validated'),'Reconcile external review before changing '+record[id_key]
                record['history']=list(prior.get('history',[])) if prior else []
                if not record['history'] or changed:
                    record['history'].append(dict(date=AUTHOR_DATE,reviewer='Codex',kind='self_check',scope=record.get('scope',record.get('task')),method='공식 문구·해설 범위, 예시 풀이, 반례, 조건 출처 및 대안 경로 대조',**({'previous_record':body(prior)} if changed else {})))
        data=dict(schema_version=1,source_pdf_sha256=hashlib.sha256((ROOT/'[별책8] 수학과 교육과정.pdf').read_bytes()).hexdigest(),analysis_scope=scope,entries=self.entries,cases=self.cases)
        path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        registry_path=ROOT/'data/hierarchy_review_registry.json'
        registry=json.loads(registry_path.read_text(encoding='utf-8'))
        for entry in self.entries:
            record=registry['standards'][entry['code']]
            if record['state']=='unreviewed':record['state']='in_progress'
            inventory=dict(source='data/'+filename,goal_ids=[g['id'] for g in entry['goals']],review_state=entry['review']['state'],scope=entry['scope'])
            if record.get('goal_analysis')!=inventory:
                record.setdefault('history',[]).append(dict(date=AUTHOR_DATE,reviewer='Codex',kind='goal_decomposition',scope=entry['scope'],source=inventory['source']))
                record['goal_analysis']=inventory
        registry_path.write_text(json.dumps(registry,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        print(json.dumps(dict(standards=len(self.entries),goals=sum(len(e['goals']) for e in self.entries),cases=len(self.cases))))
