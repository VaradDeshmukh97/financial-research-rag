# Financial Research RAG

An inspectable retrieval-augmented generation workflow for financial research documents. It chunks local text files, retrieves relevant passages using a lightweight BM25-style ranker, and can optionally pass the evidence to a locally hosted Ollama model.

**All documents and company information are synthetic. This is a portfolio demonstration, not a production research assistant.**

## Run

Requires Python 3.10+ and no third-party Python packages.

```bash
python -m financial_research_rag.cli index --documents data/documents --output outputs/index.jsonl
python -m financial_research_rag.cli query --index outputs/index.jsonl --question "What drove Northstar's revenue growth?"
```

Evidence-only retrieval is the default. To generate a draft answer, start Ollama locally, pull a model, then add `--ollama-model llama3.2` to the query command. The default endpoint is `http://localhost:11434`; override with `--ollama-url`.

## Design

- Chunking preserves document ID, file name and chunk number.
- Retrieval is independent of generation; no LLM call is made by default.
- Prompting restricts the model to supplied passages and asks for exact chunk references.
- A citation-reference check confirms that cited IDs came from the retrieved context. It does **not** prove factual correctness or entailment.
- Analyst review remains necessary.

## Architecture

`Documents → Chunking → Local index → Retrieval → Evidence → Optional local LLM → Draft + citation check → Analyst review`

## Limitations

No OCR, table extraction, embeddings, reranker, user-level access control or production evaluation harness is included. Do not use confidential client material without a separate security and data-handling review.
