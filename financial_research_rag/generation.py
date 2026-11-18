import json,re
from urllib.request import Request,urlopen
from urllib.error import URLError

def prompt_for(question:str,passages:list[dict])->str:
 evidence="\n\n".join(f"[{p['chunk_id']}]\n{p['text']}" for p in passages)
 return f"""You are assisting a financial research analyst. Answer only from the evidence below. Do not add unsupported facts or assumptions. If evidence is insufficient, say so. Cite material factual statements using exact reference IDs in square brackets. Do not invent references.\n\nQUESTION:\n{question}\n\nEVIDENCE:\n{evidence}"""

def generate(prompt:str,model:str,base_url:str)->str:
 url=base_url.rstrip("/")+"/api/generate"; data=json.dumps({"model":model,"prompt":prompt,"stream":False}).encode()
 req=Request(url,data=data,headers={"Content-Type":"application/json"},method="POST")
 try:
  with urlopen(req,timeout=120) as response: result=json.loads(response.read().decode())
 except URLError as exc: raise RuntimeError(f"Cannot reach Ollama at {url}; is it running?") from exc
 answer=result.get("response","").strip()
 if not answer: raise RuntimeError("Ollama returned an empty response")
 return answer

def check_citations(answer:str,passages:list[dict])->dict:
 allowed={p["chunk_id"] for p in passages}; cited=set(re.findall(r"\[([A-Za-z0-9_.#-]+)\]",answer))
 unknown=sorted(cited-allowed)
 return {"cited_ids":sorted(cited),"unknown_ids":unknown,"has_citations":bool(cited),"all_citations_in_context":bool(cited) and not unknown}
