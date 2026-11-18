from collections import Counter
import math,re

def tokens(text:str)->list[str]: return re.findall(r"[a-z0-9]+",text.lower())

def retrieve(question:str,chunks:list[dict],top_k:int=5)->list[dict]:
 if top_k<1: raise ValueError("top_k must be positive")
 q=tokens(question); docs=[tokens(x["text"]) for x in chunks]; n=len(docs)
 if not n or not q: return []
 df=Counter()
 for doc in docs: df.update(set(doc))
 avg=sum(map(len,docs))/n; results=[]
 for item,doc in zip(chunks,docs):
  freq=Counter(doc); score=0.0
  for term in set(q):
   tf=freq[term]
   if not tf: continue
   idf=math.log(1+(n-df[term]+0.5)/(df[term]+0.5))
   score+=idf*(tf*2.5)/(tf+1.5*(0.25+0.75*len(doc)/max(avg,1)))
  if score>0: results.append({**item,"score":round(score,6)})
 return sorted(results,key=lambda x:x["score"],reverse=True)[:top_k]
