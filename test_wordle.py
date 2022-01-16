import pytest
from wordle import score, Pattern

@pytest.mark.parametrize('guess,word,pattern', [
    ('stair', 'guard', 'sta*ir?'),
    ('other', 'stair', 'ot*her*'),
    ('stars', 'stair', 's*t*a*r?s'),
    ('memes', 'extra', 'me?mes')
    ])
def test_score(guess, word, pattern):
    assert score(guess, word) == pattern

@pytest.mark.parametrize('pattern,word', [
    ('p*a*n?i?c', 'pains'),
    ('buzzy', 'soils'),
    ('climb?', 'baddy'),
    ('wade?d', 'beens'),
])
def test_matches(pattern, word):
    pattern = Pattern.from_string(pattern)
    assert pattern.match(word)

@pytest.mark.parametrize('pattern,word', [
    ('p*a*n?i?c', 'panda'),
    ('buzzy', 'zebra'),
    ('glade*', 'seven'),
    ('pa*n*da', 'manga'),
    ('clams?', 'rides'),
    ('ta?r?es?', 'bobby'),
])
def test_excludes(pattern, word):
    pattern = Pattern.from_string(pattern)
    assert not pattern.match(word)
