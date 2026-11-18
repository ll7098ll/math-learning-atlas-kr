"""Retention plans preserve referenced/shared assets and ignore unknown paths."""
import tempfile,unittest
from pathlib import Path
from plan_portal_retention import reference_paths,select_candidates

class RetentionTests(unittest.TestCase):
    def snapshot(self):
        version='a'*16
        return ({'version':version,'resourceRoot':'content/versions/'+version+'/','standards':[{'code':'A'}]},
                {'version':version,'datasetVersion':'b'*16,'codes':['A'],'files':{'A':'c'*64}},
                {'version':version,'datasetVersion':'d'*16,'groups':[{'id':'one'}],'files':{'one':'e'*64,'graph':'f'*64}})

    def test_shared_hash_and_version_directory_are_retained(self):
        catalog,task,concept=self.snapshot();protected=reference_paths(catalog,task,concept)
        with tempfile.TemporaryDirectory() as tmp:
            dist=Path(tmp);content=dist/'content'
            for relative in protected|{'content/versions/'+'b'*16+'/old.json','content/task-pathways/items/'+'d'*64+'.json','content/task-pathways/custom/keep.txt','content/standards/A.json'}:
                p=dist/relative;p.parent.mkdir(parents=True,exist_ok=True);p.write_text('{}')
            candidates={p.relative_to(dist).as_posix() for p in select_candidates(content,protected)}
            self.assertEqual(candidates,{'content/versions/'+'b'*16,'content/task-pathways/items/'+'d'*64+'.json'})
            self.assertTrue(all((dist/p).exists() for p in protected),'Planning must not mutate files')

    def test_legacy_indexes_keep_their_original_namespace(self):
        catalog,task,concept=self.snapshot();del task['files'];del concept['files']
        refs=reference_paths(catalog,task,concept)
        self.assertIn('content/task-pathways/'+'b'*16+'/A.json',refs)
        self.assertIn('content/concept-pathways/'+'d'*16+'/graph.json',refs)
        self.assertFalse(any('/items/' in p for p in refs))

    def test_lazy_goal_graph_is_protected(self):
        catalog,task,concept=self.snapshot();task['goalGraph']={'hash':'1'*64}
        self.assertIn('content/task-pathways/items/'+'1'*64+'.json',reference_paths(catalog,task,concept))
        task['goalGraph']['hash']='../outside'
        with self.assertRaises(AssertionError):reference_paths(catalog,task,concept)

    def test_untrusted_index_paths_cannot_escape_namespace(self):
        catalog,task,concept=self.snapshot();catalog['resourceRoot']='content/versions/../../'
        with self.assertRaises(AssertionError):reference_paths(catalog,task,concept)
        catalog,task,concept=self.snapshot();task['files']['A']='../outside'
        with self.assertRaises(AssertionError):reference_paths(catalog,task,concept)

if __name__=='__main__':unittest.main()
