import tempfile,unittest
from pathlib import Path
from financial_research_rag.chunking import split_text
from financial_research_rag.index import build_index,read_index
from financial_research_rag.retrieval import retrieve
from financial_research_rag.generation import check_citations

class TestRAG(unittest.TestCase):
 def test_split_limit(self): self.assertTrue(all(len(x)<=150 for x in split_text("paragraph about finance. "*30,150)))
 def test_retrieval_and_citations(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(__file__).parents[1]; target=str(Path(d)/"index.jsonl")
   build_index(str(root/"data/documents"),target); docs=read_index(target)
   found=retrieve("Northstar revenue in 2024",docs,3); self.assertTrue(found); self.assertIn("northstar",found[0]["document_id"])
   self.assertTrue(check_citations(f"Revenue increased [{found[0]['chunk_id']}].",found)["all_citations_in_context"])
if __name__=="__main__": unittest.main()
