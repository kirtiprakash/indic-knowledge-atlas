# Indic Knowledge Atlas (Indic-KG-RAG pilot)

An **independent research prototype** inspired by the architecture of [SPARQL-LLM](https://github.com/sib-swiss/sparql-llm). This is **not** an official Infinity Foundation product, and is **not** trained on or connected to Infinity Foundation's private corpus.

## What works now

- Responsive GitHub Pages-ready frontend in `docs/` with queries, school filtering, a conceptual ontology diagram, citation leads, knowledge-gap warnings and local integrity tests.
- Deterministic retrieval baseline (`src/qa.py`), explicit candidate claims (`data/claims.json`).
- OWL/RDF ontology (`data/ontology.ttl`) and graph generator (`src/build_graph.py`).
- Regression smoke tests (`tests/test_pilot.py`) and GitHub Actions CI.

**Integrity boundary:** All six sample doctrinal statements are illustrative and unverified. References are leads for future verification, **not** validated passage citations. The pilot neither fabricates quotations nor claims expert-reviewed SOT fidelity.

## Local quick start

```bash
python -m pip install -r requirements.txt
python src/build_graph.py
python -m pytest -q
cd docs
python -m http.server 8000
```

Open http://localhost:8000 . Python 3.10+ recommended.

## GitHub Pages

1. Create a new GitHub repository and upload this project, preserving `docs/` at repository root.
2. Open **Settings → Pages**.
3. Select **Deploy from a branch**, branch `main`, directory `/docs`, then Save.
4. The website will appear at `https://YOUR_USERNAME.github.io/YOUR_REPOSITORY/` once GitHub deploys it.

The browser app deliberately makes no calls to external LLMs, so it can be hosted on static GitHub Pages. Full RAG/GraphRAG requires a backend and licensed source corpus.

## Next implementation milestones

1. Acquire permissioned source files and record editions, translations, page/time offsets and licenses.
2. Human-review candidate interpretations and attach exact, passage-level source evidence.
3. Add OpenSearch/BM25 + multilingual embeddings and reranking.
4. Use SPARQL-LLM's `SparqlExamplesLoader`, `SparqlVoidShapesLoader`, `validate_sparql_with_void` with a deployed RDF endpoint.
5. Add query routing for text RAG, SPARQL and multi-hop GraphRAG, with an API-hosted model.
6. Evaluate claim support, attribution, doctrinal fidelity, multi-turn robustness, adversarial resilience and cost with qualified reviewers.

## Ethical and scholarly safeguards

Never equate conceptual similarity with ontological identity, never merge schools' doctrines without attribution, and never present incomplete/review-pending claims as verified. Include dissenting interpretations, edition and translation differences, and calibrated abstention.

## License

MIT for this prototype code. Third-party source materials retain their respective rights.
