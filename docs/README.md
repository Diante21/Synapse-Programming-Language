# Synapse Programming Language

Synapse is an **AI Native Programming Language** designed to make working with AI models, embeddings, and vector databases as natural as traditional programming constructs.

## Features

### 🤖 Prompt Execution as First-Class Feature
Execute prompts directly in your code without boilerplate:
```synapse
result = prompt("What is artificial intelligence?")
```

### 🗄️ Built-in Vector DB Support
Native vector database operations for semantic search:
```synapse
embedding = embed("Your text here")
vector.store("collection", embedding)
results = vector.search("collection", query_embedding, 10)
```

### ⚡ Native Async + Streaming
Built-in async/await and streaming support:
```synapse
async fn processData() {
    result = await llm.gpt4("Process this data")
    return result
}

streamedResponse = stream(prompt("Generate a story"))
```

### 🎯 Direct LLM Invocation
Call any LLM model directly:
```synapse
response = llm.gpt4("Your prompt here")
response = llm.claude("Another prompt")
```

## Installation

```bash
# Clone the repository
git clone https://github.com/Diante21/Synapse-Programming-Language.git
cd Synapse-Programming-Language

# The language is implemented in Python
python3 -m synapse.cli examples/01_prompt_execution.syn
```

## Quick Start

### Hello World
```synapse
# hello.syn
greeting = prompt("Say hello to the world")
```

Run it:
```bash
python3 -m synapse.cli hello.syn
```

### Vector Search Example
```synapse
# Store documents
doc1 = "Machine learning is a subset of AI"
vector.store("docs", embed(doc1))

doc2 = "Deep learning uses neural networks"
vector.store("docs", embed(doc2))

# Search
query = "What is AI?"
results = vector.search("docs", embed(query), 2)
```

### Async Processing
```synapse
async fn analyze(text) {
    summary = await llm.gpt4("Summarize: " + text)
    return summary
}

result = await analyze("Long text here...")
```

## Language Syntax

### Variables
```synapse
x = 42
name = "Synapse"
flag = true
```

### Functions
```synapse
fn add(a, b) {
    return a + b
}

async fn fetchData(url) {
    data = await llm.gpt4("Fetch: " + url)
    return data
}
```

### Control Flow
```synapse
# If statements
if (x > 10) {
    y = prompt("X is large")
} else {
    y = prompt("X is small")
}

# For loops
for (item in items) {
    result = prompt("Process: " + item)
}

# While loops
while (condition) {
    # do something
}
```

### AI-Native Constructs

#### Prompts
```synapse
# Direct prompt execution
answer = prompt("Question here")

# With variable content
question = "What is " + topic + "?"
answer = prompt(question)
```

#### LLM Calls
```synapse
# Call specific models
gpt_response = llm.gpt4("Your prompt")
claude_response = llm.claude("Your prompt")
llama_response = llm.llama("Your prompt")
```

#### Embeddings
```synapse
# Create embeddings
text = "Some text to embed"
vector = embed(text)
```

#### Vector Database
```synapse
# Store embeddings
vector.store("collection_name", embedding)

# Search for similar embeddings
results = vector.search("collection_name", query_embedding, limit)
```

#### Streaming
```synapse
# Stream LLM responses
response = stream(prompt("Generate a long response"))
```

## Examples

Check out the `examples/` directory for more examples:
- `01_prompt_execution.syn` - Prompt execution basics
- `02_vector_db.syn` - Vector database operations
- `03_async_streaming.syn` - Async and streaming
- `04_llm_invocation.syn` - Direct LLM calls
- `05_complete_app.syn` - Complete application

## Architecture

Synapse consists of:
1. **Lexer** (`synapse/lexer.py`) - Tokenizes source code
2. **Parser** (`synapse/parser.py`) - Builds Abstract Syntax Tree
3. **Runtime** (`synapse/runtime.py`) - Executes the AST with AI features
4. **CLI** (`synapse/cli.py`) - Command-line interface

## Built-in Components

### Vector Database
- In-memory vector storage
- Cosine similarity search
- Multiple collections support

### LLM Provider
- Mock implementation for demonstration
- Easy to extend with real API calls
- Support for multiple models

### Embedding System
- Text to vector conversion
- Compatible with vector DB

## Future Enhancements

- Real LLM API integrations (OpenAI, Anthropic, etc.)
- Persistent vector database
- Type system
- Standard library
- Package manager
- IDE support
- Debugging tools

## Contributing

Contributions are welcome! This is an experimental language designed to explore AI-native programming paradigms.

## License

MIT License

## Author

Synapse Programming Language - An AI Native Programming Language
