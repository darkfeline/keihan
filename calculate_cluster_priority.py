import csv
import sys
from typing import NamedTuple


class TabDialect(csv.excel_tab):
    lineterminator = '\n'


def main(argv):
    obs = load_obs(sys.stdin)
    rules = Rules(obs)
    wrong = True
    while wrong:
        wrong = not all(rules.learn(o.cluster, o.form) for o in obs)
    rules.normalize()
    writer = csv.writer(sys.stdout, dialect=TabDialect())
    writer.writerows(rules[letter] for letter in sorted(rules))


def load_obs(f):
    reader = csv.reader(sys.stdin, dialect='excel-tab')
    # Skip header
    next(reader)
    return [Observation(*row) for row in reader]


class Observation(NamedTuple):
    cluster: str
    form: str


class Rules:
    _forms: 'Dict[str, str]'
    _priorities: 'Dict[str, int]'

    def __init__(self, obs: 'Iterable[Observation]'):
        self._forms = _base_forms(obs)
        self._priorities = {letter: 1 for letter in self._forms}

    def __iter__(self):
        return iter(self._forms)

    def __getitem__(self, k):
        """Return Rule for letter or cluster."""
        if len(k) == 1:
            return Rule(k, self._forms[k], self._priorities[k])
        dominant_letter = max(k, key=lambda l: self._priorities[l])
        return self[dominant_letter]

    def learn(self, cluster, form) -> bool:
        """Adjust learned rules to match the actual cluster form.

        Return True if our rule is right.
        """
        dominant_rule = self[cluster]
        if dominant_rule.form == form:
            return True
        letters_with_form = [letter for letter in cluster
                             if self[letter].form == form]
        self._priorities[letters_with_form[0]] = dominant_rule.priority + 1

    def normalize(self):
        self._priorities = _normalize_priorities(self._priorities)


class Rule(NamedTuple):
    letter: str
    form: str
    priority: int


def _base_forms(obs: 'Iterable[Observation]'):
    forms = {}
    for o in obs:
        if len(set(o.cluster)) == 1:
            forms[o.cluster[0]] = o.form
    return forms


def _normalize_priorities(mapping: 'Dict[Any, int]'):
    """Normalize priorities.

    >>> normalize_priorities({'a': 2, 'b': 4}) == {'a': 1, 'b': 2}
    True
    """
    priorities = sorted(set(mapping.values()))
    replacement_map = {old: new for new, old in enumerate(priorities, start=1)}
    return {k: replacement_map[old_priority]
            for k, old_priority in mapping.items()}


if __name__ == '__main__':
    sys.exit(main(sys.argv))
