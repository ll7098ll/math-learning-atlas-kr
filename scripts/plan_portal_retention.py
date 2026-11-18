"""Plan reversible archival of old static copies; never move/delete assets here."""
from pathlib import Path,PurePosixPath
import argparse,hashlib,json,re,subprocess

ROOT=Path(__file__).resolve().parents[1]
SITE=ROOT.parent if ROOT.name=='research' else ROOT/'tmp/pathways-release'

def reference_paths(catalog,task,concept):
    paths=set()
    resource=catalog.get('resourceRoot','')
    assert re.fullmatch(r'content/versions/[a-f0-9]{16}/',resource),'Missing or unsafe version root'
    paths.add(resource+'hierarchy.json')
    paths.update(resource+'relations/'+s['code']+'.json' for s in catalog['standards'])
    for namespace,index,keys in [('task-pathways',task,task['codes']),('concept-pathways',concept,[g['id'] for g in concept['groups']]+['graph'])]:
        assert index['version']==catalog['version']
        if 'files' in index:
            assert set(keys)==set(index['files'])
            for key in keys:
                digest=index['files'][key]
                assert re.fullmatch(r'[a-f0-9]{64}',digest),'Unsafe object hash'
                paths.add(f'content/{namespace}/items/{digest}.json')
        else:
            version=index['datasetVersion'];assert re.fullmatch(r'[a-f0-9]{16}',version)
            for key in keys:
                assert '/' not in key and '\\' not in key and key not in ('.','..')
                paths.add(f'content/{namespace}/{version}/{key}.json')
    if task.get('goalGraph'):
        digest=task['goalGraph']['hash']
        assert re.fullmatch(r'[a-f0-9]{64}',digest),'Unsafe goal graph object hash'
        paths.add(f'content/task-pathways/items/{digest}.json')
    assert all('..' not in PurePosixPath(p).parts for p in paths)
    return paths

def select_candidates(content,protected):
    """Only known version folders or content-addressed object files qualify."""
    root=content.parent
    candidates=[]
    for namespace in ['versions','task-pathways','concept-pathways']:
        parent=content/namespace
        if not parent.exists():continue
        for path in parent.iterdir():
            relative=path.relative_to(root).as_posix()
            if path.is_dir() and re.fullmatch(r'[a-f0-9]{16}',path.name):
                if not any(p.startswith(relative+'/') for p in protected):candidates.append(path)
            elif path.is_dir() and path.name=='items':
                for item in path.iterdir():
                    if item.is_file() and re.fullmatch(r'[a-f0-9]{64}\.json',item.name) and item.relative_to(root).as_posix() not in protected:candidates.append(item)
    relative_candidates=[c.relative_to(root).as_posix() for c in candidates]
    assert not any(p==candidate or p.startswith(candidate+'/') for p in protected for candidate in relative_candidates)
    return sorted(candidates)

def verify_paths(site,paths):
    for relative in paths:
        path=site/'dist'/relative
        assert path.is_file(),'Protected resource missing: '+relative
        if '/items/' in relative:
            assert hashlib.sha256(path.read_bytes()).hexdigest()==path.stem,'Protected object changed: '+relative

def make_plan(site,history,keep=5):
    assert history['cursor'] is None and keep>=2
    versions=sorted(history['items'],key=lambda v:v['version_number'],reverse=True)
    assert len({v['version_number'] for v in versions})==len(versions)
    assert all(v['has_archive'] for v in versions),'Saved rollback archives must exist'
    protected=set();snapshots=[]
    def add(catalog,task,concept,label):
        refs=reference_paths(catalog,task,concept);verify_paths(site,refs);protected.update(refs)
        snapshots.append(dict(label=label,catalog_version=catalog['version'],task_dataset=task['datasetVersion'],concept_dataset=concept['datasetVersion'],references=len(refs)))
    current=lambda name:json.loads((site/'dist/content'/name).read_text(encoding='utf-8'))
    add(current('catalog.json'),current('task-pathways-index.json'),current('concept-pathways-index.json'),'working_source')
    for version in versions[:keep]:
        def read(name):
            p=subprocess.run(['git','show',version['commit_sha']+':dist/content/'+name],cwd=site,capture_output=True)
            assert p.returncode==0,p.stderr
            return json.loads(p.stdout.decode('utf-8'))
        add(read('catalog.json'),read('task-pathways-index.json'),read('concept-pathways-index.json'),'saved_'+str(version['version_number']))
    moves=[]
    for path in select_candidates(site/'dist/content',protected):
        files=list(path.rglob('*')) if path.is_dir() else [path]
        files=[p for p in files if p.is_file()]
        moves.append(dict(path=path.relative_to(site/'dist').as_posix(),files=len(files),bytes=sum(p.stat().st_size for p in files)))
    return dict(policy='working_source_and_latest_5_saved_versions',keep_saved_versions=keep,saved_versions_audited=len(versions),retained_saved_versions=versions[:keep],snapshots=snapshots,protected_paths=sorted(protected),moves=moves,archive_files=sum(m['files'] for m in moves),archive_bytes=sum(m['bytes'] for m in moves),recovery='Older saved versions retain their Sites rollback archive; local static copies are moved reversibly outside the source checkout.')

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--site-dir',type=Path,default=SITE);parser.add_argument('--verify-only',action='store_true');args=parser.parse_args()
    out=ROOT/'data/portal_asset_retention.json'
    if args.verify_only:
        plan=json.loads(out.read_text(encoding='utf-8'));verify_paths(args.site_dir,plan['protected_paths'])
        current=json.loads((args.site_dir/'dist/content/task-pathways-index.json').read_text(encoding='utf-8'))
        assert current['datasetVersion']==plan['snapshots'][0]['task_dataset'],'Re-plan retention after source changes'
        print(json.dumps(dict(status='pass',retained_snapshots=len(plan['snapshots']),protected_paths=len(plan['protected_paths']))));return
    history=json.loads((ROOT/'data/portal_saved_versions.json').read_text(encoding='utf-8'))
    plan=make_plan(args.site_dir,history)
    out.write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:plan[k] for k in ['policy','saved_versions_audited','archive_files','archive_bytes']}))

if __name__=='__main__':main()
