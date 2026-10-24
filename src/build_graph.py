"""Build an RDF dataset from explicitly labelled candidate claims.

IMPORTANT: candidate claims are not verified evidence. A real deployment must
review source locations, licensing and attribution before marking them verified.
"""
import json
from pathlib import Path
from urllib.parse import quote
from rdflib import Graph, Namespace, Literal, RDF, RDFS, URIRef

ROOT = Path(__file__).resolve().parents[1]
ICKO = Namespace('https://example.org/icko/')
EX = Namespace('https://example.org/indic-data/')

def build():
    graph = Graph()
    graph.parse(ROOT / 'data' / 'ontology.ttl', format='turtle')
    graph.bind('icko', ICKO)
    graph.bind('ex', EX)
    for record in json.loads((ROOT / 'data' / 'claims.json').read_text(encoding='utf8')):
        claim = EX[record['id']]
        school = EX['school/' + quote(record['school'], safe='')]
        concept = EX['concept/' + quote(record['concept'], safe='')]
        graph.add((claim, RDF.type, ICKO.Claim))
        graph.add((claim, ICKO.attributedToSchool, school))
        graph.add((claim, ICKO.aboutConcept, concept))
        graph.add((claim, ICKO.claimText, Literal(record['claim'])))
        graph.add((claim, ICKO.evidenceStatus, Literal(record['status'])))
        graph.add((school, RDF.type, ICKO.SchoolOfThought))
        graph.add((school, RDFS.label, Literal(record['school'])))
        graph.add((concept, RDF.type, ICKO.Concept))
        graph.add((concept, RDFS.label, Literal(record['concept'])))
        # We do not assert supportedBy while evidence is unverified.
    output = ROOT / 'data' / 'pilot_graph.ttl'
    graph.serialize(destination=str(output), format='turtle')
    return graph

if __name__ == '__main__':
    g = build()
    print(f'Wrote {len(g)} RDF triples to data/pilot_graph.ttl')
