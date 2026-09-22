import subprocess, json, time, os
from pathlib import Path
class Sandbox:
    def __init__(self,image='python:3.12-slim'): self.image=image
    def run_tests(self,root):
        root=Path(root); start=time.time()
        if not self._docker(): return {'status':'sandbox_unavailable','exit_code':None,'stdout':'','stderr':'Docker daemon unavailable. No host execution performed.','duration_ms':int((time.time()-start)*1000),'timed_out':False}
        cmd=['docker','run','--rm','--network','none','--cpus','1','--memory','512m','--pids-limit','128','--read-only','--tmpfs','/tmp:rw,noexec,nosuid,size=128m','-v',f'{root}/source/generated_app:/app:ro','-w','/app',self.image,'sh','-lc','python -m pip install --no-cache-dir -r requirements.txt >/tmp/install.log 2>&1 && pytest -q']
        try:
            p=subprocess.run(cmd,capture_output=True,text=True,timeout=180)
            return {'status':'passed' if p.returncode==0 else 'failed','exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr,'duration_ms':int((time.time()-start)*1000),'timed_out':False}
        except subprocess.TimeoutExpired as e:
            return {'status':'failed','exit_code':124,'stdout':e.stdout or '','stderr':e.stderr or 'timeout','duration_ms':180000,'timed_out':True}
    def _docker(self):
        try:return subprocess.run(['docker','info'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=5).returncode==0
        except Exception:return False
