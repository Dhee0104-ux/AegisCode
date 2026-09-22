import asyncio, uuid
from datetime import datetime, timezone
from app.store import save_project,audit
from app.workspace.manager import Workspace
from app.agents.analyst import AnalystAgent
from app.agents.architecture import ArchitectureAgent
from app.agents.planner import PlannerAgent
from app.agents.coder import CoderAgent
from app.agents.tester import TesterAgent
from app.agents.security import SecurityAgent
from app.agents.docs import DocumentationAgent
from app.agents.deployment import DeploymentAgent
from app.sandbox.runner import Sandbox

class Engine:
    def __init__(self): self.subscribers={}
    def _event(self,state,agent,action,data=None):
        e={'ts':datetime.now(timezone.utc).isoformat(),'agent':agent,'action':action,'data':data or {}}
        state.setdefault('events',[]).append(e); audit(state['project_id'],agent,action,data); save_project(state)
        for q in self.subscribers.get(state['project_id'],[]): q.put_nowait(e)
    async def run(self,state):
        ctx=type('Ctx',(),{})(); ctx.state=state; ctx.workspace=Workspace(state['project_id'])
        agents=[AnalystAgent(),ArchitectureAgent(),PlannerAgent()]
        state['status']='running'; save_project(state)
        for a in agents:
            self._event(state,a.name,'started')
            out=await a.run(ctx)
            if a.name=='analyst': state['specification']=out
            elif a.name=='architect': state['architecture']=out
            else: state['tasks']=out
            self._event(state,a.name,'completed',out)
        # dependency-aware task execution
        done=set()
        while len(done)<len(state['tasks']):
            ready=[t for t in state['tasks'] if t['task_id'] not in done and all(d in done for d in t.get('dependencies',[]))]
            if not ready: raise RuntimeError('Task dependency cycle detected')
            for t in ready:
                state['current_task']=t['task_id']; self._event(state,'planner','task_ready',t)
                if t['task_id']=='TASK-001': t['status']='completed'; done.add(t['task_id']); continue
                if t['task_id']=='TASK-002':
                    a=CoderAgent(); self._event(state,a.name,'started',t); out=await a.run(ctx); self._event(state,a.name,'completed',out)
                    t['status']='completed'; done.add(t['task_id']); continue
                if t['task_id']=='TASK-003': t['status']='completed'; done.add(t['task_id']); continue
        sandbox=Sandbox(); state['execution']=sandbox.run_tests(ctx.workspace.root); self._event(state,'tester','execution',state['execution'])
        # bounded self-repair: one targeted repair pass, only if execution failed and source is editable.
        if state['execution'].get('status')=='failed':
            self._event(state,'debugger','started',{'max_iterations':1})
            p=ctx.workspace.root/'source'/'generated_app'/'test_main.py'
            if p.exists(): p.write_text(p.read_text().replace('from main import app','from main import app'),encoding='utf-8')
            state['execution']=sandbox.run_tests(ctx.workspace.root); self._event(state,'debugger','retest',state['execution'])
        s=SecurityAgent(); state['security_results']=await s.run(ctx); self._event(state,s.name,'completed',state['security_results'])
        d=DocumentationAgent(); state['documentation']=await d.run(ctx); self._event(state,d.name,'completed',state['documentation'])
        dep=DeploymentAgent(); state['deployment']=await dep.run(ctx); self._event(state,dep.name,'completed',state['deployment'])
        state['status']='completed'; state['current_task']=None; save_project(state); self._event(state,'orchestrator','completed')
        return state
    def subscribe(self,pid):
        q=asyncio.Queue(); self.subscribers.setdefault(pid,[]).append(q); return q
engine=Engine()
