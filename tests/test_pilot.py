import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from qa import answer

def test_does_not_claim_verification():
    r = answer('Advaita Brahman')
    assert r['claims']
    assert r['verified'] is False
    assert all(c['status'] != 'verified' for c in r['claims'])

def test_unseen_question_reports_gap():
    r = answer('xyzzy quux blorb')
    assert not r['claims']
    assert 'Knowledge gap' in r['answer']

def test_school_filter():
    r = answer('liberation', school='Dvaita Vedānta')
    assert all(c['school'] == 'Dvaita Vedānta' for c in r['claims'])
