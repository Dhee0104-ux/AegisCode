import json, sqlite3, threading
from pathlib import Path

DB = Path(__file__).resolve().parent.parent / 'aegiscode.db'
_lock = threading.Lock()

def init_db():
    with sqlite3.connect(DB) as c:
        c.execute('CREATE TABLE IF NOT EXISTS projects (id TEXT PRIMARY KEY, name TEXT, requirement TEXT, status TEXT, state_json TEXT)')
        c.execute('CREATE TABLE IF NOT EXISTS audit (id INTEGER PRIMARY KEY AUTOINCREMENT, project_id TEXT, ts TEXT DEFAULT CURRENT_TIMESTAMP, agent TEXT, action TEXT, payload TEXT)')

def save_project(state):
    with _lock, sqlite3.connect(DB) as c:
        c.execute('INSERT OR REPLACE INTO projects VALUES (?,?,?,?,?)', (state['project_id'],state['project_name'],state['requirement'],state['status'],json.dumps(state)))

def get_project(pid):
    with sqlite3.connect(DB) as c:
        r=c.execute('SELECT state_json FROM projects WHERE id=?',(pid,)).fetchone()
    return json.loads(r[0]) if r else None

def list_projects():
    with sqlite3.connect(DB) as c:
        rows=c.execute('SELECT id,name,status FROM projects ORDER BY rowid DESC').fetchall()
    return [{'project_id':a,'project_name':b,'status':d} for a,b,d in rows]

def audit(pid, agent, action, payload=None):
    with _lock, sqlite3.connect(DB) as c:
        c.execute('INSERT INTO audit(project_id,agent,action,payload) VALUES(?,?,?,?)',(pid,agent,action,json.dumps(payload or {})))

def get_audit(pid):
    with sqlite3.connect(DB) as c:
        rows=c.execute('SELECT id,ts,agent,action,payload FROM audit WHERE project_id=? ORDER BY id',(pid,)).fetchall()
    return [{'id':a,'ts':b,'agent':c,'action':d,'payload':json.loads(e or '{}')} for a,b,c,d,e in rows]
