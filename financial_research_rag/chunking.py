from pathlib import Path
from dataclasses import asdict,dataclass
import re

@dataclass(frozen=True)
class Chunk:
 chunk_id:str; document_id:str; source_file:str; chunk_number:int; text:str
 def to_dict(self): return asdict(self)

def split_text(text:str,max_chars:int=900)->list[str]:
 if max_chars<100: raise ValueError("max_chars must be at least 100")
 paras=[re.sub(r"\s+"," ",p).strip() for p in re.split(r"\n\s*\n",text) if p.strip()]
 output=[]; current=""
 for para in paras:
  if len(para)>max_chars:
   if current: output.append(current); current=""
   words=para.split(); part=""
   for word in words:
    candidate=(part+" "+word).strip()
    if len(candidate)>max_chars and part: output.append(part); part=word
    else: part=candidate
   if part: output.append(part)
  else:
   candidate=(current+"\n"+para).strip()
   if current and len(candidate)>max_chars: output.append(current); current=para
   else: current=candidate
 if current: output.append(current)
 return output

def load_documents(directory:str,max_chars:int=900)->list[Chunk]:
 root=Path(directory)
 if not root.exists(): raise FileNotFoundError(root)
 chunks=[]
 for path in sorted(root.rglob("*.txt")):
  doc_id=path.stem
  for n,text in enumerate(split_text(path.read_text(encoding="utf-8"),max_chars),1):
   chunks.append(Chunk(f"{doc_id}#chunk_{n}",doc_id,str(path.relative_to(root)),n,text))
 return chunks
