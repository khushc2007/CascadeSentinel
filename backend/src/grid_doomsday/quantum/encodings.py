from __future__ import annotations
from itertools import combinations
from math import comb


def _validate(n: int, k: int) -> None:
    if n < 0 or k < 0 or k > n:
        raise ValueError("require n >= 0 and 0 <= k <= n")


def valid_bitstrings(n: int, k: int) -> tuple[str, ...]:
    _validate(n, k)
    return tuple("".join("1" if i in selected else "0" for i in range(n)) for selected in combinations(range(n), k))


def dicke_dimension(n: int, k: int) -> int:
    _validate(n, k)
    return comb(n, k)


def encode_index(index: int, n: int, k: int) -> str:
    states = valid_bitstrings(n, k)
    if index < 0 or index >= len(states):
        raise IndexError("Dicke basis index out of range")
    return states[index]


def decode_index(bits: str) -> int:
    if any(bit not in "01" for bit in bits):
        raise ValueError("bits must contain only 0 and 1")
    return valid_bitstrings(len(bits), bits.count("1")).index(bits)

