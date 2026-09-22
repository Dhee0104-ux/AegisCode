from pathlib import Path
import json
class Workspace:
    def __init__(self,pid):
        self.root=Path(__file__).resolve().parents[2]/'projects'/pid
        for d in ['source','tests','docs','build','logs','artifacts']: (self.root/d).mkdir(parents=True,exist_ok=True)
    def write(self,rel,content):
        p=(self.root/'source'/rel).resolve(); p.parent.mkdir(parents=True,exist_ok=True)
        if self.root/'source' not in p.parents: raise ValueError('path escape')
        p.write_text(content,encoding='utf-8'); return str(p.relative_to(self.root))
    def read(self,rel): return ((self.root/'source'/rel).resolve()).read_text(encoding='utf-8')
    def manifest(self): return [str(p.relative_to(self.root/'source')) for p in (self.root/'source').rglob('*') if p.is_file()]
