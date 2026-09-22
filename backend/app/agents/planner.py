from .base import Agent
class PlannerAgent(Agent):
    name='planner'
    async def run(self,ctx):
        ai=await self.llm('Return JSON object with tasks array. Each task: task_id,title,description,dependencies,files_to_create,files_to_modify,acceptance_criteria,status. Make tasks dependency-aware.',str(ctx.state['architecture']))
        if ai and ai.get('tasks'): return ai['tasks']
        return [
          {'task_id':'TASK-001','title':'Initialize project','description':'Create backend, frontend and project metadata.','dependencies':[],'files_to_create':['README.md','.gitignore'],'files_to_modify':[],'acceptance_criteria':['Workspace exists'],'status':'pending'},
          {'task_id':'TASK-002','title':'Create application scaffold','description':'Create generated sample application and tests.','dependencies':['TASK-001'],'files_to_create':['generated_app/main.py','generated_app/test_main.py'],'files_to_modify':[],'acceptance_criteria':['App imports','Tests pass'],'status':'pending'},
          {'task_id':'TASK-003','title':'Add container configuration','description':'Create Dockerfile and CI configuration.','dependencies':['TASK-002'],'files_to_create':['generated_app/Dockerfile','.github/workflows/ci.yml'],'files_to_modify':[],'acceptance_criteria':['Docker build definition exists'],'status':'pending'}]
