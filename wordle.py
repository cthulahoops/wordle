from dataclasses import dataclass
from collections import Counter
from math import log
import re
# import pytest

with open("/usr/share/dict/words", encoding='utf-8') as fh:
    words = fh.read().splitlines()

words = [w for w in words if re.match(r'^[a-z]{5}$', w)]

@dataclass
class Pattern:
    regex: str
    exclude: set
    require: Counter

    @classmethod
    def from_string(cls, pattern_string):
        pattern = re.findall('[a-z][*?]?', pattern_string)
        parts = ['.' for _ in range(5)]
        exclude = set()
        require = Counter()

        for (i, place) in enumerate(pattern):
            letter = place[0]
            marker = place[-1]

            if marker == '*':
                parts[i] = letter
                require[letter] += 1
            elif marker == '?':
                parts[i] = f'[^{letter}]'
                require[letter] += 1
            else:
                exclude.add(letter)

        return cls(regex='^' + ''.join(parts) + '$', exclude=exclude, require=require)

    def match(self, word):
        if not re.match(self.regex, word):
            return False

        counts = Counter(word)

        for letter, count in counts.items():
            if count < self.require[letter]:
                return False

        for letter in self.exclude:
            if counts[letter] > self.require[letter]:
                return False

        return True

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

def guess_counts(guess, possibilities):
    return Counter(score(guess, word) for word in possibilities)

def guess_entropy(guess, possibilities):
    return sum([x * log(x) for x in guess_counts(guess, possibilities).values()])

def filter_possibilities(pattern, words):
    pattern = Pattern.from_string(pattern)
    return [w for w in words if pattern.match(w)]

def recommend_guess(possibilities):
    scored_guesses = []
    for potential_guess in words:
        entropy = guess_entropy(potential_guess, possibilities)
        scored_guesses.append((entropy, -(potential_guess in possibilities), potential_guess))

    (entropy, _, recommendation) = min(scored_guesses)
    print(guess_counts(recommendation, possibilities))

    scored_guesses.sort()

    print(scored_guesses[:10])

    print(entropy, recommendation)

    return recommendation

def main():
    remaining_possibilities = words

    guess = 'tares'

    while len(remaining_possibilities) > 1:
        print("I recommend: ", guess)

        pattern = input('Result? ')
        remaining_possibilities = filter_possibilities(pattern, remaining_possibilities)
        guess = recommend_guess(remaining_possibilities)

    print("The answer is: ", remaining_possibilities[0])

if __name__ == '__main__':
    main()
