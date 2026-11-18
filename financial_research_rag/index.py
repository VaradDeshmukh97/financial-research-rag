import json
from pathlib import Path
from .chunking import load_documents

def build_index(documents:str,output:str)->int:
 chunks=load_documents(documents); path=Path(output); path.parent.mkdir(parents=True,exist_ok=True)
 with path.open("w",encoding="utf-8") as f:
  for c in chunks: f.write(json.dumps(c.to_dict(),ensure_ascii=False)+"\n")
 return len(chunks)

def read_index(path:str)->list[dict]:
 p=Path(path)
 if not p.exists(): raise FileNotFoundError(p)
 return [json.loads(line) for line in p.read_text(encoding="utf-8").splitlines() if line.strip()]
