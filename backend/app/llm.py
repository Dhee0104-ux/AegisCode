import os, json, httpx

async def complete_json(system: str, user: str):
    key=os.getenv('LLM_API_KEY')
    if not key: return None
    base=os.getenv('LLM_BASE_URL','https://api.openai.com/v1').rstrip('/')
    model=os.getenv('LLM_MODEL','gpt-4.1-mini')
    payload={'model':model,'messages':[{'role':'system','content':system},{'role':'user','content':user}], 'temperature':0.1, 'response_format':{'type':'json_object'}}
    async with httpx.AsyncClient(timeout=90) as client:
        r=await client.post(base+'/chat/completions',json=payload,headers={'Authorization':f'Bearer {key}'})
        r.raise_for_status(); return json.loads(r.json()['choices'][0]['message']['content'])
