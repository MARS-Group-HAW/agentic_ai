# HAW ICC configuration

The starter supports an **OpenAI-compatible chat/embedding endpoint** through `langchain-openai`.

Before the course starts, the instructor should provide:

- base URL,
- authentication method,
- chat model name(s),
- embedding model name(s),
- rate limits / quotas,
- whether tool calling is supported,
- whether structured outputs are supported,
- whether token usage metadata is returned.

Example `.env` configuration:

```text
LLM_PROVIDER=openai_compatible
LLM_BASE_URL=https://<ICC-ENDPOINT>/v1
LLM_API_KEY=<TOKEN-IF-REQUIRED>
LLM_MODEL=<MODEL>

EMBEDDING_PROVIDER=openai_compatible
EMBEDDING_BASE_URL=https://<ICC-ENDPOINT>/v1
EMBEDDING_API_KEY=<TOKEN-IF-REQUIRED>
EMBEDDING_MODEL=<EMBEDDING-MODEL>
```

## Compatibility rule

If ICC is not OpenAI-compatible, change **only the provider adapter** in `src/llm/factory.py` and keep the rest of the project independent of the concrete serving platform.

Do not distribute real access tokens through Git or course material.
