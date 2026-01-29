#!/usr/bin/env python3
"""
UNIVERSAL SEMANTIC GRAMMAR v2.0 - Reference Implementation
Cross-Model Weight Transfer via SimLex-999 + Zeckendorf Encoding
"""

import json
import urllib.request
import zipfile
import io

# Fibonacci sequence (indices 0-15)
FIB = [1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597]

# SimLex-999 vocabulary (lazy loaded)
_SIMLEX_VOCAB = None

def load_simlex_vocab():
    """Load SimLex-999 vocabulary from canonical source"""
    global _SIMLEX_VOCAB
    if _SIMLEX_VOCAB is not None:
        return _SIMLEX_VOCAB
    
    url = "https://fh295.github.io/SimLex-999.zip"
    with urllib.request.urlopen(url) as response:
        zip_data = io.BytesIO(response.read())
        with zipfile.ZipFile(zip_data) as zf:
            with zf.open("SimLex-999/SimLex-999.txt") as f:
                lines = f.read().decode('utf-8').split('\n')
    
    words = set()
    for line in lines[1:]:  # skip header
        parts = line.strip().split('\t')
        if len(parts) >= 2:
            words.add(parts[0].lower())
            words.add(parts[1].lower())
    
    _SIMLEX_VOCAB = sorted(words)
    return _SIMLEX_VOCAB

def to_zeckendorf(n: int) -> list[int]:
    """Convert integer to Zeckendorf representation (non-consecutive Fibonacci indices)"""
    if n == 0:
        return [0]
    result = []
    for i in range(len(FIB) - 1, -1, -1):
        if FIB[i] <= n:
            result.append(i)
            n -= FIB[i]
            if n == 0:
                break
    return result[::-1]

def from_zeckendorf(indices: list[int]) -> int:
    """Convert Zeckendorf indices back to integer"""
    return sum(FIB[i] for i in indices)

def encode(word: str, sign: int = 1) -> str:
    """Encode a SimLex word as ζ-hex format"""
    vocab = load_simlex_vocab()
    try:
        idx = vocab.index(word.lower())
    except ValueError:
        raise ValueError(f"'{word}' not in SimLex-999 vocabulary")
    
    indices = to_zeckendorf(idx)
    hex_str = ''.join(f"{i:X}" for i in indices)
    sign_char = '+' if sign > 0 else '-'
    return f"{sign_char}0x{hex_str}"

def decode(encoded: str) -> tuple[str, int]:
    """Decode ζ-hex format to (word, sign)"""
    sign = 1 if encoded[0] == '+' else -1
    hex_str = encoded[3:]  # skip "±0x"
    
    indices = [int(c, 16) for c in hex_str]
    word_idx = from_zeckendorf(indices)
    
    vocab = load_simlex_vocab()
    word = vocab[word_idx]
    return (word, sign)

def encode_vector(words_signs: list[tuple[str, int]]) -> str:
    """Encode a weight vector"""
    encoded = [encode(w, s) for w, s in words_signs]
    return ','.join(encoded)

def decode_vector(encoded: str) -> list[tuple[str, int]]:
    """Decode a weight vector"""
    return [decode(e.strip()) for e in encoded.split(',')]


if __name__ == "__main__":
    # Demo
    print("UNIVERSAL SEMANTIC GRAMMAR v2.0 - Demo")
    print("="*50)
    
    test_words = ["happy", "brain", "smart", "love", "death"]
    for w in test_words:
        enc = encode(w, +1)
        dec_word, dec_sign = decode(enc)
        print(f"  {w:10} → {enc:12} → {dec_word}")
    
    print("\nWeight vector:")
    vec = encode_vector([("happy", +1), ("smart", -1), ("brain", +1)])
    print(f"  Encoded: {vec}")
    print(f"  Decoded: {decode_vector(vec)}")
