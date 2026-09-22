from .base import Agent

class CoderAgent(Agent):
    name='coder'
    async def run(self,ctx):
        w=ctx.workspace
        files={
            'generated_app/main.py': '''from fastapi import FastAPI\napp=FastAPI(title="Generated AegisCode App")\n\n@app.get("/health")\ndef health():\n    return {"status":"ok"}\n''',
            'generated_app/test_main.py': '''from fastapi.testclient import TestClient\nfrom main import app\n\ndef test_health():\n    assert TestClient(app).get("/health").status_code == 200\n''',
            'generated_app/requirements.txt': 'fastapi==0.115.6\nhttpx==0.28.1\npytest==8.3.4\n',
            'generated_app/Dockerfile': '''FROM python:3.12-slim\nWORKDIR /app\nCOPY requirements.txt .\nRUN pip install --no-cache-dir -r requirements.txt\nCOPY . .\nUSER 65532:65532\nCMD ["uvicorn","main:app","--host","0.0.0.0","--port","8000"]\n''',
            '.github/workflows/ci.yml': '''name: ci\non: [push, pull_request]\njobs:\n  test:\n    runs-on: ubuntu-latest\n    steps:\n      - uses: actions/checkout@v4\n      - uses: actions/setup-python@v5\n        with:\n          python-version: '3.12'\n      - run: pip install -r generated_app/requirements.txt\n      - run: cd generated_app && pytest -q\n'''
        }
        for p,c in files.items():
            w.write(p,c)
        return {'files':list(files),'changes':len(files)}
