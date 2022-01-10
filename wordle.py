from dataclasses import dataclass
from collections import Counter
from math import log
import re
# import pytest

words = open("/usr/share/dict/words").read().splitlines()

words = [w for w in words if re.match(r'^[a-z]{5}$', w)]

@dataclass
class Pattern:
    regex: str
    exclude: set
    require: set

    @classmethod
    def from_string(cls, pattern_string):
        pattern = re.findall('[a-z][*?]?', pattern_string)
        parts = ['.' for _ in range(5)]
        exclude = set()
        require = set()

        for (i, place) in enumerate(pattern):
            letter = place[0]
            marker = place[-1]

            if marker == '*':
                parts[i] = letter
                require.add(letter)
            elif marker == '?':
                parts[i] = f'[^{letter}]'
                require.add(letter)
            else:
                exclude.add(letter)

            for x in require:
                if x in exclude:
                    exclude.remove(x)
        return cls(regex='^' + ''.join(parts) + '$', exclude=exclude, require=require)

    def match(self, word):
        return re.match(self.regex, word) and all(x in word for x in self.require) and not any(x in word for x in self.exclude)

def score(guess, word):
    assert len(guess) == len(word)
    used = set()
    exact = set()
    for (idx, (guess_letter, word_letter)) in enumerate(zip(guess, word)):
        if guess_letter == word_letter:
            used.add(idx)
            exact.add(idx)

    wrong_place = set()
    for (guess_idx, guess_letter) in enumerate(guess):
        if guess_idx in exact:
            continue
        for (word_idx, word_letter) in enumerate(word):
            if word_letter == guess_letter and word_idx not in used:
                used.add(word_idx)
                wrong_place.add(guess_idx)

    result = []
    for (idx, letter) in enumerate(guess):
        result.append(letter)
        if idx in exact:
            result.append('*')
        elif idx in wrong_place:
            result.append('?')
    return ''.join(result)

def mean(values):
    return sum(values) / len(values)

def guess_entropy(guess, possibilities):
    counts = Counter(score(guess, word) for word in possibilities)
    return mean([log(x) for x in counts.values()])

def filter_possibilities(pattern, words):
    pattern = Pattern.from_string(pattern)
    return [w for w in words if pattern.match(w)]

def main():
    remaining_possibilities = words

    for pattern in ['he?ar*t', 'mu*sic']:
        remaining_possibilities = filter_possibilities(pattern, remaining_possibilities)

    print(remaining_possibilities)

    if len(remaining_possibilities) == 1:
        return

    scored_guesses = []
    for potential_guess in words:
        entropy = guess_entropy(potential_guess, remaining_possibilities)
        scored_guesses.append((entropy, potential_guess))

    (entropy, recommendation) = min(scored_guesses)

    print(entropy, recommendation)

    # new_pattern = score(recommendation, answer)

    # pattern = Pattern.from_string(new_pattern)
    # potential_words = [w for w in remaining_possibilities if pattern.match(w)]

    # print(potential_words)


if __name__ == '__main__':
    main()
