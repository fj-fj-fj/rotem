from collections.abc import Mapping


# created by Mike Graham [https://stackoverflow.com/a/2704866/13278413]
class FrozenDict(Mapping):
    """A frozendict is a read-only mapping.

    A key cannot be added nor removed,
    and a key is always mapped to the same value.
    """

    def __init__(self, *args, **kwargs):
        self._d = dict(*args, **kwargs)
        self._hash = None

    def __iter__(self):
        return iter(self._d)

    def __len__(self):
        return len(self._d)

    def __getitem__(self, key):
        return self._d[key]

    def __hash__(self):
        if self._hash is None:
            hash_ = 0
            for pair in self.items():
                hash_ ^= hash(pair)
            self._hash = hash_
        return self._hash


def frozendict(*args, **kwargs) -> FrozenDict:
    return FrozenDict(*args, **kwargs)
