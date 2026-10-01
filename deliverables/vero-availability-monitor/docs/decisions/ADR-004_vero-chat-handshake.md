# ADR-004: Vero Chat checked by MCP handshake, token from an environment variable
Status: accepted (3.0.0)

Context: Vero Chat is an MCP server; a `tools/call` runs an agent that can take minutes. The `initialize` handshake
proves the endpoint and the token work without any model call. Tokens must never be stored in config or Git.
Decision: the optional `chat` check sends `initialize` only; the bearer token is read from the environment variable
named in `chat.token_env` (default `VERO_CHAT_TOKEN`) at run time.
Consequences: free and fast; it does not prove the Chat agent can answer (secondary check: its failure only degrades).
