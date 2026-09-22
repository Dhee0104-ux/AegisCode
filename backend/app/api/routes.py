import asyncio, uuid
from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect
from app.models.schemas import RequirementRequest
from app.store import get_project,list_projects,get_audit,save_project
from app.orchestration.engine import engine
router=APIRouter()

@router.get('/health')
def health(): return {'status':'ok','service':'aegiscode'}
@router.get('/projects')
def projects(): return list_projects()
@router.get('/projects/{pid}')
def project(pid):
    x=get_project(pid)
    if not x: raise HTTPException(404,'Project not found')
    return x
@router.get('/projects/{pid}/audit')
def audit_log(pid): return get_audit(pid)
@router.post('/projects')
async def create(req:RequirementRequest):
    pid=str(uuid.uuid4()); name=req.project_name or 'AegisCode Project'
    state={'project_id':pid,'project_name':name,'requirement':req.requirement,'status':'queued','specification':{},'architecture':{},'tasks':[],'current_task':None,'events':[],'test_results':{},'security_results':{},'deployment':{}}
    save_project(state); asyncio.create_task(engine.run(state)); return {'project_id':pid,'project_name':name,'status':'queued'}
@router.websocket('/ws/projects/{pid}')
async def ws(websocket:WebSocket,pid:str):
    await websocket.accept(); q=engine.subscribe(pid)
    try:
        state=get_project(pid)
        if state:
            for e in state.get('events',[]): await websocket.send_json(e)
        while True: await websocket.send_json(await q.get())
    except WebSocketDisconnect: pass
