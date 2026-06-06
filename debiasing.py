import hashlib


import random
from math import prod

import numpy as np


def bits(bit_num: int = 1000) -> str:
    return "".join(f"{random.randint(0, 1)}" for _ in range(bit_num))


def onesFraction(bitString: str) -> float:
    ones = "".join(char for char in bitString if char == "1")
    return len(ones) / len(bitString)


def pileUpBias(k: int = 8) -> float:
    return prod([onesFraction(bits()) for _ in range(k)])


def vonNeumannDebias(bitString: str) -> str:
    pairs = [bitString[i : i + 2] for i in range(0, len(bitString), 2)]
    debiased = ""
    for i in range(len(pairs)):
        if pairs[i] == "10":
            debiased += "1"
        elif pairs[i] == "01":
            debiased += "0"
    return debiased


def entropy(bitString: str) -> float:
    p0 = bitString.count("0") / len(bitString)
    p1 = bitString.count("1") / len(bitString)
    result = p0 * np.log2(p0) + p1 * np.log2(p1)
    return result * -1


def pack_bits_to_bytes(bitString: str) -> bytes:
    out = bytearray()
    for i in range(0, len(bitString), 8):
        v = 0
        for b in bitString[i : i + 8]:
            v = (v << 1) | int(b)
        out.append(v)
    return bytes(out)


def hash_condition(bitString: str) -> tuple[bytes, str]:
    digest = hashlib.sha256(pack_bits_to_bytes(bitString)).digest()
    seed_bits = []
    for byte in digest:
        for j in range(7, -1, -1):
            seed_bits.append((byte >> j) & 1)
    seed = "".join(f"{bit}" for bit in seed_bits)
    return digest, seed


if __name__ == "__main__":
    debiased = vonNeumannDebias(bits())
    print(f"Debiased BitString: {onesFraction(debiased)}")
    print(f"Entropy: {entropy(debiased)}")
    digest, seed = hash_condition(bits())
    print(f"Seed: {seed}")
