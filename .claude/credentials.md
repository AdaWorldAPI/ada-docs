# Credentials

## GitHub
```
GITHUB_TOKEN=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
```

## Jina AI
```
JINA_API_KEY=jina_b7b1d172a2c74ad2a95e2069d07d8bb9TayVx4WjQF0VWWDmx4xl32VbrHAc
```

## Upstash Redis

### Primary (persistent)
```
UPSTASH_REDIS_URL=https://upright-jaybird-27907.upstash.io
UPSTASH_REDIS_TOKEN=AW0DAAIncDI5YWE1MGVhZGU2YWY0YjVhOTc3NDc0YTJjMGY1M2FjMnAyMjc5MDc
```

### Secondary (ram_expansion)
```
UPSTASH_REDIS_URL2=https://massive-seahorse-9089.upstash.io
UPSTASH_REDIS_TOKEN2=ASOBAAImcDJkZjczM2RhM2RjNDc0MGNiYjE1MjMxNmM0ZGRkYmM3OHAyOTA4OQ
```

### Admin Key
```
UPSTASH_ADMIN_KEY=6375b738-859c-49b0-ba62-3db5f4ccd7de
```

## Neo4j
```
NEO4J_URI=neo4j+s://7e137e6e.databases.neo4j.io
NEO4J_USER=neo4j
NEO4J_PASSWORD=O-EXvpDXZBoIIH9SvmCiXobcGcMt81oEgmpS405hs1o
```

## OpenAI
```
OPENAI_API_KEY=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
```

## xAI (Grok)
```
XAI_API_KEY=xai-g3WcFfAaWXT2sHbANbpngsLfdOCSBMnZYUqQ7RdI8RTfyfsCtFWydwK3OtD8T3Cpzywid7T5jgzRQpkS
```

## Hugging Face
```
HF_TOKEN=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
```

## ElevenLabs
```
ELEVENLABS_API_KEY=sk_78a6ec2b473eb96ab9c4f2b74482d5ea1a85f7ca39c62626
```

## Replicate
```
REPLICATE_API_TOKEN=r8_UTKqtBxsrcxpspBYJDlyNsSNNWc3YpP2RGRvD
```

## Railway
```
RAILWAY_API_KEY_1=696c05cb-5b23-4a94-9eba-2917ef064bb0
RAILWAY_API_KEY_2=527fd4d6-e801-43e0-9a22-736a2a069801
RAILWAY_PROJECT_ADARAIL=87a274c8-87d2-44b7-84a9-f51210d0c1d9
RAILWAY_PROJECT_TOKEN=a87fed68-6e48-45d4-ad9c-42ec9e5e2fac
RAILWAY_OAUTH_TOKEN=16bb666b-c84e-450c-a976-41d7000ee85d
```

## PiAPI
```
PIAPI_KEY=51b3fbbbc72ac6a5a2ac5d341c007633b9b3d87416a54bb6bede294c79791db9
```

## Legnext (Midjourney)
```
LEGNEXT_API_KEY=bcd01f2332d4ca42f626b93bc83858128c10924b17be6f51cc8d9480ad645471
```

## Cursor
```
CURSOR_API_KEY=key_5416578d439445aa5be96ee8aea5fca422393a8b5f6f4ff6d746d3048aa832b8
```

---

## Usage

### In Python
```python
import os
from dotenv import load_dotenv

load_dotenv('.claude/credentials.env')

github_token = os.getenv('GITHUB_TOKEN')
jina_key = os.getenv('JINA_API_KEY')
```

### In Bash
```bash
source .claude/credentials.env
curl -H "Authorization: token $GITHUB_TOKEN" ...
```

### Direct Load
```python
# Quick inline for Claude Code
CREDS = {
    "github": "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",
    "jina": "jina_b7b1d172a2c74ad2a95e2069d07d8bb9TayVx4WjQF0VWWDmx4xl32VbrHAc",
    "upstash": {
        "url": "https://upright-jaybird-27907.upstash.io",
        "token": "AW0DAAIncDI5YWE1MGVhZGU2YWY0YjVhOTc3NDc0YTJjMGY1M2FjMnAyMjc5MDc"
    }
}
```
