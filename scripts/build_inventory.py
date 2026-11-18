"""Index the fixed 2022 curriculum source without inventing semantic analyses."""
from __future__ import annotations

import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / '[별책8] 수학과 교육과정.pdf'
EXTRACT = ROOT / 'tmp/pdfs/curriculum-extracted.txt'
CODE = r'(?:[2469]수\d{2}-\d{2}|10(?:공수|기수)[12]-\d{2}-\d{2}|12(?:대수|확통|기하|경수|인수|직수|수문|실통|수과)\d{2}-\d{2}|12미적[ⅠⅡ]-\d{2}-\d{2})'
DEFINITION = re.compile(r'^\[(' + CODE + r')\]\s*(.*)$')
REFERENCE = re.compile(r'\[(' + CODE + r')\]')
SUBJECTS = {
    '10공수1': ('공통수학1', '공통'), '10공수2': ('공통수학2', '공통'),
    '10기수1': ('기본수학1', '공통'), '10기수2': ('기본수학2', '공통'),
    '12대수': ('대수', '일반 선택'), '12미적Ⅰ': ('미적분Ⅰ', '일반 선택'),
    '12확통': ('확률과 통계', '일반 선택'), '12미적Ⅱ': ('미적분Ⅱ', '진로 선택'),
    '12기하': ('기하', '진로 선택'), '12경수': ('경제 수학', '진로 선택'),
    '12인수': ('인공지능 수학', '진로 선택'), '12직수': ('직무 수학', '진로 선택'),
    '12수문': ('수학과 문화', '융합 선택'), '12실통': ('실용 통계', '융합 선택'),
    '12수과': ('수학과제 탐구', '융합 선택'),
}
COMMON_DOMAINS = {'01': '수와 연산', '02': '변화와 관계', '03': '도형과 측정', '04': '자료와 가능성'}


def dump(path: str, data: object) -> None:
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def main() -> None:
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    from pypdf import PdfReader
    reader = PdfReader(PDF)
    # Recreate the extraction from the source on every run, so its provenance is fixed.
    texts = [(p.extract_text() or '') for p in reader.pages]
    EXTRACT.parent.mkdir(parents=True, exist_ok=True)
    EXTRACT.write_text('\n'.join(f'=== PDF PAGE {i} ===\n{t}' for i, t in enumerate(texts, 1)), encoding='utf-8')
    lines: list[tuple[int, str]] = [(p, line.strip()) for p, t in enumerate(texts, 1) for line in t.splitlines()]
    corrections_path = ROOT / 'data/source_corrections.json'
    corrections_data = json.loads(corrections_path.read_text(encoding='utf-8')) if corrections_path.exists() else {'corrections': {}}
    corrections = corrections_data['corrections']
    additionally_reviewed = set(corrections_data.get('additional_reviewed_codes', []))
    additional_evidence = corrections_data.get('additional_review_evidence', {})
    records = []
    section = None
    seen = set()
    for i, (page, line) in enumerate(lines):
        heading = re.match(r'^\(([1-9])\)\s*(.+)$', line)
        if heading:
            section = (heading.group(1).zfill(2), heading.group(2).strip())
        match = DEFINITION.match(line)
        if not match:
            continue
        code, first = match.groups()
        if code in seen:
            raise ValueError(f'Duplicate definition: {code}')
        seen.add(code)
        chunks = [first]
        source_pages = [page]
        j = i
        while not re.search(r'다\s*\.\s*$', chunks[-1]):
            j += 1
            if j >= len(lines):
                raise ValueError(f'Unterminated statement: {code}')
            next_page, next_line = lines[j]
            if DEFINITION.match(next_line) or next_line.startswith(('(가)', '(나)', '•')):
                raise ValueError(f'Unexpected boundary in {code}: {next_line}')
            if not next_line:
                continue
            # Page furniture is excluded only when a statement crosses a PDF page.
            if next_page != page and (next_line.isdigit() or next_line in {'수학과 교육과정', '공통 교육과정'} or next_line.startswith('선택 중심 교육과정')):
                continue
            chunks.append(next_line)
            if next_page not in source_pages:
                source_pages.append(next_page)
        if code[0] in '2469':
            level = '중학교' if code.startswith('9') else '초등학교'
            prefix = code[:2]
            domain = code[2:4]
            grade = {'2': '1~2학년군', '4': '3~4학년군', '6': '5~6학년군', '9': '1~3학년군'}[code[0]]
            subject, category = '수학', '공통 교육과정'
            domain_name = COMMON_DOMAINS[domain]
        else:
            level, grade = '고등학교', '과목별'
            prefix = next((p for p in SUBJECTS if code.startswith(p)), None)
            if prefix is None:
                raise ValueError(f'Unknown subject: {code}')
            subject, category = SUBJECTS[prefix]
            rest = code[len(prefix):].lstrip('-')
            domain = rest.split('-')[0]
            if section is None or section[0] != domain or len(section[1]) > 30:
                raise ValueError(f'Section mismatch: {code}: {section}')
            domain_name = section[1]
        raw = '\n'.join(chunks)
        normalized = re.sub(r'\s+', ' ', raw).strip()
        flags = []
        if any(0xE000 <= ord(ch) <= 0xF8FF for ch in raw):
            flags.append('수식의 전용 글리프 원문 대조 필요')
        if re.search(r'(?:[가-힣] ){4,}[가-힣]', normalized):
            flags.append('PDF 자간으로 인한 어절 분리 원문 대조 필요')
        records.append({
            'code': code, 'school_level': level, 'grade_band': grade,
            'subject': subject, 'subject_category': category,
            'domain_code': domain, 'domain': domain_name,
            'statement_extracted': normalized, 'statement_raw_lines': chunks,
            'source_id': 'CURRICULUM_2022_33', 'source_pdf_pages': source_pages,
            'source_printed_pages': [p - 6 for p in source_pages],
            'extraction_status': '검토 필요' if flags else '텍스트 추출',
            'quality_flags': flags, 'analysis_status': '미착수',
            'statement_display': corrections.get(code, normalized),
            'source_review_status': '원문 이미지 대조 보정' if code in corrections else ('원문 이미지 대조' if code in additionally_reviewed else '미대조'),
            'unresolved_quality_flags': [] if code in corrections else flags,
        })
        if code in additional_evidence:
            records[-1]['source_review_evidence'] = additional_evidence[code]
    referenced = set(REFERENCE.findall('\n'.join(texts)))
    missing = sorted(referenced - seen)
    if missing:
        raise ValueError(f'Referenced standards without definitions: {missing}')
    counts = Counter(r['school_level'] for r in records)
    if counts != Counter({'초등학교': 121, '중학교': 60, '고등학교': 254}):
        raise ValueError(f'Unexpected counts for this fixed source: {counts}')
    gaps = []
    groups = defaultdict(list)
    for record in records:
        group, number = record['code'].rsplit('-', 1)
        groups[group].append(int(number))
    for group, numbers in groups.items():
        if sorted(numbers) != list(range(1, max(numbers) + 1)):
            gaps.append(group)
    if gaps:
        raise ValueError(f'Numbering gaps: {gaps}')
    registry_path = ROOT / 'data/analysis_registry.json'
    registry = json.loads(registry_path.read_text(encoding='utf-8')) if registry_path.exists() else []
    for entry in registry:
        record = next(r for r in records if r['code'] == entry['code'])
        record['analysis_status'] = entry['status']
        record['analysis_file'] = entry['file']
    dump('data/standards.json', {
        'schema_version': '1.0', 'curriculum_version': '교육부 고시 제2022-33호',
        'source_file': PDF.name, 'source_sha256': hashlib.sha256(PDF.read_bytes()).hexdigest(),
        'source_pdf_page_count': len(texts),
        'normalization': '줄바꿈과 연속 공백만 병합. 수식 및 어절은 추정 복원하지 않음.',
        'standards': records,
    })
    dump('data/inventory_quality.json', {
        'counts_by_school_level': dict(counts), 'total': len(records),
        'high_school_subjects': len({r['subject'] for r in records if r['school_level'] == '고등학교'}),
        'duplicate_definitions': [], 'missing_referenced_codes': missing, 'numbering_gaps': gaps,
        'original_flagged_record_count': sum(bool(r['quality_flags']) for r in records),
        'visually_corrected_record_count': len(corrections),
        'additional_visually_reviewed_record_count': len(additionally_reviewed - set(corrections)),
        'records_requiring_source_review': [{'code': r['code'], 'pdf_pages': r['source_pdf_pages'], 'flags': r['unresolved_quality_flags']} for r in records if r['unresolved_quality_flags']],
        'source_review': '자동 구조 검증 완료. 텍스트 추출과 원문 육안 대조는 별도 상태로 관리.',
    })
    write_indexes(records)
    print(json.dumps({'counts': dict(counts), 'total': len(records), 'original_extraction_warnings': sum(bool(r['quality_flags']) for r in records), 'unresolved_extraction_warnings': sum(bool(r['unresolved_quality_flags']) for r in records)}, ensure_ascii=False))


def write_indexes(records: list[dict]) -> None:
    target_dir = ROOT / 'indexes'
    target_dir.mkdir(exist_ok=True)
    for level in ['초등학교', '중학교', '고등학교']:
        subset = [r for r in records if r['school_level'] == level]
        output = [f'# {level} 성취기준 전체 목록', '', f'2022년 고시 원문의 {len(subset)}개 성취기준. 문장과 분석 상태를 구분하여 관리한다.', '',
                  'PDF 쪽수는 파일의 첫 페이지부터 센 값이다. 수식 글리프와 어절 분리 경고가 있는 문장은 원문 대조가 필요하다.', '',
                  '[프로젝트 안내](../README.md) · [진행 현황](진행현황.md)', '']
        current = None
        for r in subset:
            group = (r['grade_band'] if level != '고등학교' else r['subject'], r['domain'])
            if group != current:
                output += ['', f'## {group[0]} {group[1]}', '', '| 성취기준 | 표시 문장 | PDF 쪽 | 상세 분석 | 원문 대조 |', '|---|---|---:|---|---|']
                current = group
            status = r['analysis_status']
            if r.get('analysis_file'):
                status = f"[{status}](../{r['analysis_file']})"
            statement = r['statement_display'].replace('|', '\\|')
            flag = '보정 대조' if r['source_review_status'] == '원문 이미지 대조 보정' else ('대조' if r['source_review_status'] == '원문 이미지 대조' else ('필요' if r['unresolved_quality_flags'] else '미대조'))
            output.append(f"| {r['code']} | {statement} | {', '.join(map(str, r['source_pdf_pages']))} | {status} | {flag} |")
        (target_dir / f'{level}성취기준.md').write_text('\n'.join(output) + '\n', encoding='utf-8')
    output = ['# 수학 내용 체계 진행 현황', '', '전체 목록화와 상세 사고 분석의 진행률을 각각 관리한다. 초안 작성은 연구 검토나 학생 반응 검증의 완료를 뜻하지 않는다.', '',
              '| 학교급 | 목록화 | 상세 분석 초안 | 검토 완료 | 학생 반응 검증 |', '|---|---:|---:|---:|---:|']
    for level in ['초등학교', '중학교', '고등학교']:
        subset = [r for r in records if r['school_level'] == level]
        draft = sum(r['analysis_status'] == '초안' for r in subset)
        reviewed = sum(r['analysis_status'] in ['검토 완료', '학생 반응 검증'] for r in subset)
        validated = sum(r['analysis_status'] == '학생 반응 검증' for r in subset)
        output.append(f'| {level} | {len(subset)} | {draft} | {reviewed} | {validated} |')
    output += ['', '## 초등 영역별 상세 분석', '', '| 영역 | 전체 | 초안 | 미착수 |', '|---|---:|---:|---:|']
    for domain in COMMON_DOMAINS.values():
        subset = [r for r in records if r['school_level'] == '초등학교' and r['domain'] == domain]
        draft = sum(r['analysis_status'] == '초안' for r in subset)
        output.append(f'| {domain} | {len(subset)} | {draft} | {sum(r["analysis_status"] == "미착수" for r in subset)} |')
    output += ['', '## 다음 작업', '',
               '1. 전체 상세 초안의 수학적 논증과 교육과정 적용 범위를 영역별로 검토한다.',
               '2. 중고등 연결의 중간 개념과 성립 조건을 보강하고 대안 경로를 비교한다.',
               '3. 문헌의 원연구를 정독하여 자체 사고 분석과 연구 결과의 대응 범위를 확인한다.',
               '4. 가능한 경우 진단 질문에 대한 실제 학생 반응으로 분석을 수정한다.', '']
    output += ['전체 자료 보완의 최신 진행과 완료 조건: [전체 자료 보완 진행](../docs/전체자료보완진행.md). 내용 체계 항목의 자체 의미 대조, 원문 이미지 대조, 문헌 검토와 실제 검증을 구별해 관리한다.', '']
    (target_dir / '진행현황.md').write_text('\n'.join(output), encoding='utf-8')


if __name__ == '__main__':
    main()
