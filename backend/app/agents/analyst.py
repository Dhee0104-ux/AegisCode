import re
from .base import Agent
class AnalystAgent(Agent):
    name='analyst'
    async def run(self, ctx):
        req=ctx.state['requirement']; ai=await self.llm('Return only JSON for software requirement analysis. Keys: project_name,functional_requirements,non_functional_requirements,users,apis,database,authentication,integrations,technology_constraints,deployment_requirements,ambiguities.',req)
        if ai: return ai
        low=req.lower(); name=ctx.state['project_name']
        db='PostgreSQL' if 'postgres' in low else ('MySQL' if 'mysql' in low else 'SQLite')
        auth='JWT' if 'jwt' in low else ('OAuth2' if 'oauth' in low else 'none')
        apis=[]
        if 'crud' in low: apis=['GET /items','POST /items','GET /items/{id}','PUT /items/{id}','DELETE /items/{id}']
        return {'project_name':name,'functional_requirements':[x.strip() for x in re.split(r'[,.]\s*',req) if x.strip()][:12], 'non_functional_requirements':['testability','security','containerized deployment'],'users':['Administrator','Authenticated User'],'apis':apis,'database':{'engine':db},'authentication':{'type':auth},'integrations':[],'technology_constraints':['FastAPI' if 'fastapi' in low else 'Python'],'deployment_requirements':['Docker'],'ambiguities':[]}
