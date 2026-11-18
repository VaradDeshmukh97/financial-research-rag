import argparse
from .index import build_index,read_index
from .retrieval import retrieve
from .generation import prompt_for,generate,check_citations

def main():
 p=argparse.ArgumentParser(description="Financial research RAG demo"); s=p.add_subparsers(dest="cmd",required=True)
 a=s.add_parser("index"); a.add_argument("--documents",required=True); a.add_argument("--output",required=True)
 b=s.add_parser("query"); b.add_argument("--index",required=True); b.add_argument("--question",required=True); b.add_argument("--top-k",type=int,default=4); b.add_argument("--ollama-model"); b.add_argument("--ollama-url",default="http://localhost:11434")
 x=p.parse_args()
 if x.cmd=="index": print(f"Indexed {build_index(x.documents,x.output)} chunks"); return
 passages=retrieve(x.question,read_index(x.index),x.top_k)
 if not passages: print("No relevant passages found."); return
 if not x.ollama_model:
  print("RETRIEVED EVIDENCE — no LLM generation requested\n")
  for item in passages: print(f"[{item['chunk_id']}] score={item['score']}\n{item['text']}\n")
 else:
  answer=generate(prompt_for(x.question,passages),x.ollama_model,x.ollama_url)
  print("DRAFT ANSWER\n"+answer+"\n\nCITATION CHECK\n"+str(check_citations(answer,passages)))
  print("\nAnalyst review is required; reference-ID validation does not prove factual correctness.")
if __name__=="__main__": main()
