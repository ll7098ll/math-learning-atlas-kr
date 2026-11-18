"""Immutable per-record objects so corpus additions reuse unchanged payloads."""
import hashlib
import json


def write_content_object(content,namespace,data):
    assert namespace in ('task-pathways','concept-pathways')
    encoded=json.dumps(data,ensure_ascii=False,separators=(',',':')).encode('utf-8')
    digest=hashlib.sha256(encoded).hexdigest()
    target=content/namespace/'items'/(digest+'.json')
    target.parent.mkdir(parents=True,exist_ok=True)
    if target.exists():
        assert target.read_bytes()==encoded,'Immutable content object differs: '+str(target)
    else:target.write_bytes(encoded)
    return digest
