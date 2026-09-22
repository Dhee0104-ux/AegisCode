from dataclasses import dataclass
from app.llm import complete_json

@dataclass
class AgentContext:
    state: dict
    workspace: object

class Agent:
    name='base'
    async def run(self, ctx): raise NotImplementedError
    async def llm(self, system, user): return await complete_json(system,user)
