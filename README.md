# Synapse Programming Language

**Synapse** is an AI Native Programming Language that makes working with AI models, embeddings, and vector databases as natural as traditional programming.

## 🚀 Key Features

- **🤖 Prompt Execution as First-Class Feature** - Execute AI prompts directly in your code
- **🗄️ Built-in Vector DB Support** - Native vector database operations for semantic search
- **⚡ Native Async + Streaming** - Built-in async/await and streaming capabilities
- **🎯 Direct LLM Invocation** - Call any LLM model directly from your code

## Quick Example

```synapse
# Store documents with embeddings
doc = "Machine learning is a subset of AI"
vector.store("docs", embed(doc))

# Search semantically
query = "What is AI?"
results = vector.search("docs", embed(query), 5)

# Use prompts naturally
answer = prompt("Explain: " + results)

# Stream responses
response = stream(llm.gpt4("Write a story about AI"))
```

## Getting Started

```bash
# Run example programs
python3 -m synapse.cli examples/01_prompt_execution.syn
python3 -m synapse.cli examples/02_vector_db.syn
python3 -m synapse.cli examples/03_async_streaming.syn

# Run tests
python3 -m pytest tests/

# Or use unittest
python3 -m unittest tests/test_synapse.py
```

## Documentation

See [docs/README.md](docs/README.md) for complete documentation including:
- Language syntax
- AI-native constructs
- Built-in functions
- Examples and tutorials

## Project Structure

```
synapse/
├── __init__.py      # Package initialization
├── lexer.py         # Tokenizer
├── parser.py        # AST builder
├── runtime.py       # Interpreter with AI features
└── cli.py           # Command-line interface

examples/            # Example programs
tests/              # Test suite
docs/               # Documentation
```

## Language Features

### Prompt Execution
```synapse
result = prompt("What is artificial intelligence?")
```

### Vector Database
```synapse
embedding = embed("Your text")
vector.store("collection", embedding)
results = vector.search("collection", query_embedding, 10)
```

### Async & Streaming
```synapse
async fn processData() {
    result = await llm.gpt4("Process this")
    return result
}

streamed = stream(prompt("Generate content"))
```

### Direct LLM Calls
```synapse
response = llm.gpt4("Your prompt")
response = llm.claude("Another prompt")
```

## Contributing

Contributions welcome! This is an experimental language exploring AI-native programming paradigms.

## License

MIT License 
