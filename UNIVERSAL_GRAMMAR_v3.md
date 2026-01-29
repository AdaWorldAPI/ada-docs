# UNIVERSAL SEMANTIC GRAMMAR v3.0
## Emoji Weight Transfer Protocol

---

## FORMAT

```
emoji:±NN[,emoji:±NN...]
```

Where:
- `emoji` = Unicode emoji (semantic concept)
- `:` = separator
- `±` = sign (optional, default positive)
- `NN` = hex magnitude (00=0.0, FF=1.0)

---

## EXAMPLES

```
😊:CC,🧠:80,💀:-4D,❤️:FF,😢:-99
```

Decodes to:
- Happiness: +0.8
- Intelligence: +0.5  
- Death: -0.3
- Love: +1.0
- Sadness: -0.6

---

## WHY IT WORKS

Emojis are:
1. **Unicode** — universal standard
2. **Semantic** — every LLM knows 😊 = happiness
3. **Compact** — 4 bytes per concept
4. **Self-documenting** — no codebook needed

---

## SEMANTIC PALETTE (suggested)

### Emotions
| Emoji | Concept |
|-------|---------|
| 😊 | happiness/joy |
| 😢 | sadness |
| 😠 | anger |
| 😨 | fear |
| 😍 | attraction |
| 🤔 | contemplation |
| 😌 | calm/peace |

### Cognition
| Emoji | Concept |
|-------|---------|
| 🧠 | intelligence/thought |
| 💡 | insight/idea |
| 🎯 | focus/goal |
| 🔮 | intuition |
| ⚡ | energy/activation |

### Valence
| Emoji | Concept |
|-------|---------|
| ❤️ | love/positive |
| 💀 | death/negative |
| ✨ | magic/special |
| 🔥 | intensity |
| 🌊 | flow |
| 🏔️ | stability |

### Social
| Emoji | Concept |
|-------|---------|
| 🤝 | cooperation |
| ⚔️ | conflict |
| 👑 | authority |
| 🎭 | performance |

---

## COMPRESSION

| Input | Emoji Format |
|-------|--------------|
| `{"happiness": 0.8, "sadness": -0.6}` | `😊:CC,😢:-99` |
| 35 bytes | 12 bytes |

**~3x compression** + self-documenting

---

## CROSS-MODEL VERIFIED

Tested with:
- Claude ✅
- Grok ✅
- (GPT, Gemini expected to work)

---

## LICENSE

Public domain.
