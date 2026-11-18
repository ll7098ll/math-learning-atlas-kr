"""Persist scoped PDF, repository XML or native HTML notes and review history."""
import hashlib
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from urllib.parse import urljoin
from pypdf import PdfReader
from PIL import Image

from extend_lt2_length_assets_review import load, sha, write
from literature_review import ROOT, build_report, digest, load_registry, target_value
from relation_literature_review import FILE, apply_literature_context, claim_snapshot, relation_snapshot


def inspect_html_assets(spec, cache):
    """Bind read HTML and embedded images to actual cached response bytes."""
    class Images(HTMLParser):
        def __init__(self):
            super().__init__(); self.paths=[]
        def handle_starttag(self, tag, attrs):
            if tag.lower()=='img':
                src=dict(attrs).get('src')
                if src:self.paths.append(src)
    base=spec['asset_base_url']; pages=[]; links={}
    assert base.startswith('https://') and base.endswith('/')
    def asset(row):
        p=(cache/row['file']).resolve()
        assert p.is_relative_to(cache.resolve()) and p.is_file()
        assert row['status']==200 and row['url'].startswith(base)
        assert sha(p)==row['sha256']
        return p
    for row in spec['html_assets']:
        p=asset(row);assert row['content_type']=='text/html'
        parser=Images();parser.feed(p.read_text(encoding='utf-8'))
        assert row['url'] not in links
        links[row['url']]={urljoin(row['url'],src) for src in parser.paths}
        pages.append({k:row[k] for k in ['key','url','title','sha256','status','content_type']})
    assert len({p['key'] for p in pages})==len(pages)
    assert any(p['url']==spec['url'] and p['sha256']==spec['sha256'] for p in pages)
    images=[]
    for row in spec['image_assets']:
        p=asset(row)
        assert row['page_url'] in links and row['url'] in links[row['page_url']]
        assert row['content_type'].startswith('image/')
        with Image.open(p) as im:assert list(im.size)==row['dimensions']
        images.append({**{k:row[k] for k in ['page_url','url','sha256','status','content_type','dimensions']},
                       'read_kind':'inline_image_visual_review','redistributed':False})
    assert len({i['url'] for i in images})==len(images)
    return pages,images


def record(*, specs, claims, observations, details, corrections, interpretations, cache,
           date, category, detail_key, roles=None):
    roles = roles or {}
    registry = load_registry()
    if set(specs) <= registry['sources'].keys():
        build_report()
        return
    assert not set(specs).intersection(registry['sources'])
    bibliography, queue = load(ROOT/'data/sources.json'), load(ROOT/'data/content_review_queue.json')
    assert not set(specs).intersection(row['id'] for row in bibliography)
    assert not set(specs).intersection(row['source']['id'] for row in queue['literature_review'])
    for sid, spec in specs.items():
        asset_kind=spec.get('asset_kind','pdf')
        if asset_kind=='pdf':
            pdf = cache/f'{spec["stem"]}.pdf'
            assert sha(pdf) == spec['sha256']
            reader = PdfReader(pdf)
            assert len(reader.pages) == spec['total']
            text_pages=spec.get('text_pages',spec['pages'])
            assert all(reader.pages[p-1].extract_text().strip() for p in text_pages)
            images = {str(p):sha(cache/'rendered'/f'{spec.get("render_stem",spec["stem"])}-{p}.png') for p in spec['visuals']}
            source_fields=dict(source_asset_kind='pdf',source_pdf_sha256=spec['sha256'])
            note_fields=dict(source_pdf_url=spec['pdf_url'],pdf_pages=spec['total'],selected_text_pages=text_pages,
                             visual_pdf_pages=spec['visuals'],rendered_page_sha256=images)
            method='지정 본문과 표·그림의 실제 판면을 대조했다.'
            if not text_pages:
                assert spec['visuals'] and set(spec['pages'])<=set(spec['visuals'])
                note_fields['text_extraction_incomplete']=True
                method='기계적 글자 추출이 불완전해 지정 PDF 판면을 직접 읽었다. 추출 텍스트를 읽은 쪽으로 집계하지 않는다.'
        elif asset_kind=='repository_docx':
            from docx_source_review import inspect_docx_source
            manifest=inspect_docx_source(spec,cache)
            source_fields=dict(source_asset_kind=asset_kind,source_asset_sha256=spec['sha256'],repository_docx_review=manifest)
            note_fields=dict(source_docx_url=spec['docx_url'],source_asset_redistributed=False,pdf_read=False,original_page_layout_review=False)
            method='공식 저장소 DOCX의 지정 본문 블록·차트 XML/캐시 수치와 삽입 이미지를 대조했다. DOCX 전체 판면·차트의 시각 배치와 출판 PDF의 동일성은 미확인이다.'
        elif asset_kind=='publisher_html':
            pages,images=inspect_html_assets(spec,cache)
            source_fields=dict(source_asset_kind=asset_kind,source_asset_sha256=spec['sha256'],asset_base_url=spec['asset_base_url'],
                               html_read_manifest=pages,image_read_manifest=images)
            note_fields=dict(source_asset_redistributed=False,pdf_read=False,original_page_layout_review=False)
            method='확보한 HTML의 지정 본문과 삽입 그림을 읽고 실제 응답 바이트·그림 크기를 대조했다. 동적 페이지 배치나 애플릿의 작동을 확인한 것은 아니다.'
        else:
            assert asset_kind=='repository_xml'
            xml=cache/f'{spec["stem"]}.xml'
            assert sha(xml)==spec['sha256']
            article=ET.fromstring(xml.read_bytes())
            assert article.tag=='article'
            assert spec['doi'] in [''.join(e.itertext()).strip() for e in article.findall('.//article-id')]
            elements=[]
            for element_id in spec['section_ids']:
                element=article.find(f'.//*[@id="{element_id}"]')
                assert element is not None and ''.join(element.itertext()).strip(),element_id
                elements.append(dict(id=element_id,sha256=hashlib.sha256(ET.tostring(element,encoding='utf-8')).hexdigest()))
            manifest=dict(url=spec['xml_url'],repository=spec['repository'],article_identifier=spec['article_identifier'],
                publication_doi=spec['doi'],binary_obtained=True,content_type='application/xml',selected_elements=elements)
            source_fields=dict(source_asset_kind=asset_kind,source_asset_sha256=spec['sha256'],repository_xml_review=manifest)
            note_fields=dict(source_xml_url=spec['xml_url'],source_asset_redistributed=False,
                             pdf_read=False,original_page_layout_review=False)
            method='공식 저장소 XML의 지정 절·채점 지침·부록 문항을 읽었다. PDF 판면과 그림 자체의 시각 대조는 하지 않았다.'
        empirical = dict(design=spec['design'], sample_description=spec['sample'], inference_limit=spec['limit'],
                         student_outcome_study=spec.get('student_outcome_study',True), causal_effect_established=False, local_effect_tested=False)
        entry = dict(id=sid, year=spec['year'], url=spec['url'], title=spec['title'], authors=spec['authors'],
                     kind=category, review_scope=spec['scope'], does_not_establish=spec['limit'],
                     supports=spec['supports'], next_review=spec.get('next_review','자체 과제의 실제 응답과 다른 표본의 문항을 추가 대조한다.'))
        bibliography.append(entry)
        note = f'data/literature_evidence/{sid}_review_notes.json'
        write(ROOT/note, dict(source_id=sid, source_url=spec['url'],**source_fields,**note_fields,
            date=date, reviewer='Codex', read_scope=spec['scope'], empirical_scope=empirical,
            contains_source_full_text=False, source_pdf_redistributed=False, reading_log=[spec['scope']],
            source_corrections=[dict(location='방법·문항·표·그림·서술의 대조', issue=corrections[sid])],
            **{detail_key:details[sid]}))
        registry['sources'][sid] = dict(source_id=sid, state='self_read_claim_mapping', reviewer='Codex', date=date,
            snapshot_kind='authored_review_notes',**source_fields,
            snapshot_file=note, snapshot_sha256=sha(ROOT/note), redistribution_license='workspace_authored_notes',
            bibliography_snapshot=digest(entry), display=dict(title=spec['title'], url=spec['url'],
                authors_year=f'{spec["authors"][0]}{" 외" if len(spec["authors"])>1 else ""}, {spec["year"] if spec["year"] is not None else "연도 미상"}'),
            read_scope=spec['scope'], limits=spec['limit'], empirical_scope=empirical,
            scope_note='문항 설계·학생의 실제 응답·분석 분류·자체 설계 과제를 구별한다.',
            method_note=method+' 원문의 표본·시점·응답 단위와 국내 과제의 범위를 나누어 기록한다.',
            editorial_action='읽은 범위에 맞는 문헌 근거와 자체 관찰 과제를 반영했다.',
            independent_review=False, student_validated=False, observations=observations[sid])
        queue['literature_review'].append(dict(source=entry, status='self_read_claim_mapping',
            evidence_file='data/literature_claim_reviews.json', claim_evidence_fields=spec['supports'],
            claim_ids=[cid for src,cid,*_ in claims if src==sid]))
    new = {}
    for sid,cid,codes,pages,support,limit in claims:
        new[cid] = dict(id=cid,source_id=sid,role=roles.get(cid,'empirical_result_with_scope'),
            empirical_scope=registry['sources'][sid]['empirical_scope'],standard_codes=codes,
            locations=([f'{specs[sid]["xml_url"]}#{p}' for p in pages] if specs[sid].get('asset_kind')=='repository_xml'
                       else [f'{specs[sid]["docx_url"]} · DOCX본문블록{p}' for p in pages] if specs[sid].get('asset_kind')=='repository_docx'
                       else [f'{specs[sid]["url"]} · {p}' for p in pages] if specs[sid].get('asset_kind')=='publisher_html'
                       else [f'{specs[sid]["pdf_url"]}#page={p}' for p in pages]),support=support,does_not_establish=limit,
            independent_review=False,student_validated=False,
            target_snapshots={f'revision:{code}':digest(target_value(f'revision:{code}')) for code in codes})
    registry['claims'].extend(new.values())
    relations = load(ROOT/'data/revised_relations.json')['relations']
    pairs = {(r['id'],cid) for r in relations for cid,claim in new.items()
             if all(r[k].startswith('standard:') for k in ('from','to'))
             and {r[k][9:] for k in ('from','to')}<=set(claim['standard_codes'])}
    assert pairs == interpretations.keys(), pairs
    reviewed = load(ROOT/FILE)
    by_relation = {r['id']:r for r in relations}
    for (rid,cid),(role,finding,limit) in interpretations.items():
        claim=new[cid]
        reviewed['records'].append(dict(relation_id=rid,claim_id=cid,role=role,finding=finding,limit=limit,
            relation_snapshot=relation_snapshot(by_relation[rid]),
            claim_snapshot=claim_snapshot(claim,registry['sources'][claim['source_id']])))
    apply_literature_context(relations,registry,registry=reviewed)
    write(ROOT/'data/sources.json',bibliography)
    write(ROOT/'data/content_review_queue.json',queue)
    write(ROOT/'data/literature_claim_reviews.json',registry)
    write(ROOT/FILE,reviewed)
    build_report()
    print(f'{category}: {len(specs)} sources, {len(claims)} claims, '
          f'{sum(len(rows) for rows in observations.values())} tasks, {len(pairs)} relation entries')
