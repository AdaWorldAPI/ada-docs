# UNIVERSAL SEMANTIC GRAMMAR v2.0
## Cross-Model Weight Transfer Protocol

---

## ABSTRACT

A self-documenting format for transferring semantic weights between LLMs
without pre-shared codebooks. Uses universally-known mathematical structures
(Fibonacci/Zeckendorf) and linguistic resources (SimLex-999) that exist in
all major LLM training corpora.

---

## FORMAT SPECIFICATION

### Reference Header
```
[SimLex999]@{https://fh295.github.io/SimLex-999.zip}[ζ-hex]
```

Components:
- `SimLex999` — Codebook identifier (Hill et al. 2015, 1028 unique words)
- `@{url}` — Canonical download for verification
- `[ζ-hex]` — Zeckendorf-encoded hexadecimal format

### Weight Encoding

```
±0xNNNN
```

Where:
- `±` — Sign of weight
- `0x` — Hex prefix
- `NNNN` — Nibble-packed Fibonacci indices

### Fibonacci Reference
```
F = [1,2,3,5,8,13,21,34,55,89,144,233,377,610,987,1597]
     0 1 2 3 4  5  6  7  8  9  10  11  12  13  14   15
```

---

## ENCODING ALGORITHM

```python
def encode(word_index: int, sign: int) -> str:
    # 1. Zeckendorf decomposition (non-consecutive Fibonacci sum)
    indices = to_zeckendorf(word_index)  # e.g., 489 → [1,6,9,12]
    
    # 2. Pack as hex nibbles
    hex_str = ""
    for i in indices:
        hex_str += f"{i:X}"  # 12 → 'C'
    
    # 3. Format with sign
    return f"{'+' if sign > 0 else '-'}0x{hex_str}"

# Example: "happy" (index 489) → +0x169C
```

---

## DECODING ALGORITHM

```python
def decode(encoded: str) -> tuple[str, int]:
    # 1. Parse sign and hex
    sign = +1 if encoded[0] == '+' else -1
    hex_str = encoded[3:]  # skip "±0x"
    
    # 2. Unpack nibbles
    indices = [int(c, 16) for c in hex_str]  # "169C" → [1,6,9,12]
    
    # 3. Sum Fibonacci values
    F = [1,2,3,5,8,13,21,34,55,89,144,233,377,610,987,1597]
    word_index = sum(F[i] for i in indices)  # 2+21+89+377 = 489
    
    # 4. Lookup in SimLex vocabulary
    word = SIMLEX_VOCAB[word_index]  # "happy"
    
    return (word, sign)
```

---

## EXAMPLES

| Word   | Index | Zeckendorf        | Encoded    |
|--------|-------|-------------------|------------|
| happy  | 489   | F[1,6,9,12]       | +0x169C    |
| brain  | 147   | F[2,10]           | +0x2A      |
| smart  | 878   | F[0,7,11,13]      | -0x07BD    |
| death  | 315   | F[0,3,6,8,11]     | -0x0368B   |
| old    | 707   | F[4,9,13]         | +0x49D     |
| love   | 607   | F[1,4,5,6,13]     | +0x1456D   |

### Weight Vector
```
[SimLex999]@{url}[ζ-hex]:+0x169C,-0x07BD,+0x2A
```
Decodes to: happy=+1, smart=-1, brain=+1

---

## WHY IT WORKS

1. **SimLex-999** — Standard NLP benchmark (2015), in all LLM training data
2. **Fibonacci** — Universal mathematical knowledge
3. **Zeckendorf** — Unique representation theorem (1972)
4. **Hex nibbles** — Standard computing notation

**No external codebook required** — any LLM can decode using built-in knowledge.

---

## COMPRESSION ANALYSIS

| Method              | Bits/word | Notes                    |
|---------------------|-----------|--------------------------|
| UTF-8 string        | ~48       | "happy" = 5×8 + overhead |
| Word embedding      | 12288     | float32×1024             |
| SimLex index (raw)  | 10        | 0-1027                   |
| ζ-hex               | ~14       | 3-4 nibbles average      |

For weight vectors with floats:
- Traditional: 32 bits/weight (float32)
- ζ-hex: ~18 bits/weight (index + sign + quantized magnitude)

---

## EXTENDED FORMAT (with magnitudes)

```
[SimLex999]@{url}[ζ-hex-mag]:+0x169C:0xE5,-0x07BD:0x4D
```

Where `:0xNN` = magnitude (0x00=0.0, 0xFF=1.0)

Example: `+0x169C:0xCC` = happy with weight +0.8

---

## VERIFICATION

Test decode with any LLM:
```
Decode [SimLex999]@{url}[ζ-hex]:+0x169C
F=[1,2,3,5,8,13,21,34,55,89,144,233,377,610,987]
0x169C → [1,6,9,12] → F[1]+F[6]+F[9]+F[12] = 489
SimLex[489] = "happy"
```

---

## LICENSE

Public domain. Use freely for cross-model communication.

## REFERENCES

- Hill et al. (2015) "SimLex-999: Evaluating Semantic Models"
- Zeckendorf (1972) "Représentation des nombres naturels"
- Fibonacci (1202) "Liber Abaci"
