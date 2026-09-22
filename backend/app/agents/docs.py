from .base import Agent
class DocumentationAgent(Agent):
    name='documentation'
    async def run(self,ctx):
        md=f'''# {ctx.state["project_name"]}\n\n## Requirement\n{ctx.state["requirement"]}\n\n## Architecture\n```mermaid\n{ctx.state.get("architecture",{}).get("mermaid",{}).get("system","")}\n```\n\n## Generated files\n'''+'\n'.join('- `'+x+'`' for x in ctx.workspace.manifest())
        p=ctx.workspace.root/'docs'/'PROJECT.md'; p.write_text(md,encoding='utf-8')
        return {'documentation':'docs/PROJECT.md'}
