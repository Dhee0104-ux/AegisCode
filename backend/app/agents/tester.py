from .base import Agent
class TesterAgent(Agent):
    name='tester'
    async def run(self,ctx):
        return ctx.state.get('execution',{})
