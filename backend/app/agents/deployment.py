from .base import Agent
class DeploymentAgent(Agent):
    name='deployment'
    async def run(self,ctx):
        compose='''services:\n  app:\n    build: ./generated_app\n    ports: ["8000:8000"]\n'''
        p=ctx.workspace.root/'source'/'docker-compose.generated.yml'; p.write_text(compose,encoding='utf-8')
        return {'docker_compose':'source/docker-compose.generated.yml','ci':'source/.github/workflows/ci.yml'}
