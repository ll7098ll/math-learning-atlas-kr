"""Check that adding a revision preserves prior immutable object bytes."""
import tempfile
import unittest
from pathlib import Path
from content_objects import write_content_object


class ContentObjectTests(unittest.TestCase):
    def test_reuse_and_revision_preserve_previous_objects(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            first=write_content_object(root,'task-pathways',{'code':'A','conditions':['a','b']})
            unchanged=write_content_object(root,'task-pathways',{'code':'B','conditions':['c']})
            saved={p.name:p.read_bytes() for p in (root/'task-pathways/items').iterdir()}
            again=write_content_object(root,'task-pathways',{'code':'A','conditions':['a','b']})
            revised=write_content_object(root,'task-pathways',{'code':'A','conditions':['a','b','d']})
            self.assertEqual(first,again)
            self.assertNotEqual(first,revised)
            self.assertEqual(len(list((root/'task-pathways/items').iterdir())),3)
            for name,content in saved.items():self.assertEqual((root/'task-pathways/items'/name).read_bytes(),content)
            self.assertEqual(unchanged,write_content_object(root,'task-pathways',{'code':'B','conditions':['c']}))

    def test_existing_corruption_is_reported_without_overwrite(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);data={'code':'A','conditions':['required']}
            digest=write_content_object(root,'task-pathways',data)
            item=root/'task-pathways/items'/(digest+'.json')
            item.write_bytes(b'corrupted')
            with self.assertRaisesRegex(AssertionError,'Immutable content object differs'):
                write_content_object(root,'task-pathways',data)
            self.assertEqual(item.read_bytes(),b'corrupted')


if __name__=='__main__':unittest.main()
