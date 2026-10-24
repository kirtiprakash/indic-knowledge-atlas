"""Deterministic, source-aware retrieval baseline. No LLM and no fabricated quotes."""
import json
import re
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

def answer(question, school=None, limit=6):
    rows = json.loads((ROOT / 'data' / 'claims.json').read_text(encoding='utf8'))
    tokens = set(re.findall(r'[\wāīūṛśṣṇ]+', question.lower()))
    scored = []
    for row in rows:
        if school and row['school'] != school:
            continue
        hay = ' '.join([row['concept'], row['claim'], row['school'], *row['tags']]).lower()
        score = sum(1 for token in tokens if len(token) >= 3 and token in hay)
        if score:
            scored.append((score, row))
    scored.sort(key=lambda p: (-p[0], p[1]['id']))
    evidence = [row for _, row in scored[:limit]]
    return {'question': question, 'claims': evidence, 'verified': False,
            'answer': 'Candidate interpretations only; confirm the linked primary passages before relying on these claims.' if evidence
            else 'Knowledge gap: no matching candidate interpretation was found.'}
