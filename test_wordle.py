import pytest
from wordle import score

@pytest.mark.parametrize('guess,word,pattern', [
    ('stair', 'guard', 'sta*ir?'),
    ('other', 'stair', 'ot*her*'),
    ('stars', 'stair', 's*t*a*r?s'),
    ('memes', 'extra', 'me?mes')
    ])
def test_score(guess, word, pattern):
    assert score(guess, word) == pattern
