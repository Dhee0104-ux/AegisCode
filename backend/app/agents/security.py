from .base import Agent
import re
class SecurityAgent(Agent):
    name='security'
    async def run(self,ctx):
        findings=[]
        for f in ctx.workspace.manifest():
            try:s=ctx.workspace.read(f)
            except:continue
            if re.search(r'(AKIA[0-9A-Z]{16}|sk-[A-Za-z0-9]{20,})',s): findings.append({'severity':'critical','file':f,'issue':'Possible hard-coded credential'})
            if 'subprocess' in s and 'shell=True' in s: findings.append({'severity':'high','file':f,'issue':'Potential shell injection surface'})
        return {'status':'completed','findings':findings,'summary':f'{len(findings)} finding(s)'}
