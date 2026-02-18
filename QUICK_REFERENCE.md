# Synapse Quick Reference Guide

## Installation & Usage

```bash
# Run a Synapse program
python3 -m synapse.cli program.syn

# Execute code directly
python3 -m synapse.cli -c 'result = prompt("Hello")'

# Run tests
python3 -m unittest tests.test_synapse

# Run demo
python3 demo.py
```

## Syntax Cheat Sheet

### Variables
```synapse
x = 42
name = "Synapse"
flag = true
list = [1, 2, 3]
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
# If-else
if (x > 10) {
    y = 1
} else {
    y = 0
}

# For loop
for (item in items) {
    result = process(item)
}

# While loop
while (condition) {
    # do something
}
```

## AI-Native Features

### Prompts
```synapse
# Execute a prompt
answer = prompt("What is AI?")

# Prompts in expressions
summary = prompt("Summarize: " + text)
```

### LLM Calls
```synapse
# Call specific models
gpt_response = llm.gpt4("Your prompt")
claude_response = llm.claude("Your prompt")
llama_response = llm.llama("Your prompt")
```

### Embeddings
```synapse
# Generate embedding
vec = embed("Text to embed")

# Use in expressions
embedding = embed(doc1 + " " + doc2)
```

### Vector Database
```synapse
# Store an embedding
vector.store("collection_name", embedding)

# Search for similar vectors
results = vector.search("collection_name", query_embedding, 10)

# Results include similarity scores
for (result in results) {
    # Each result has: embedding, metadata, similarity
}
```

### Async & Streaming
```synapse
# Async function
async fn process(text) {
    result = await llm.gpt4(text)
    return result
}

# Await
data = await process("some text")

# Stream responses
streamed = stream(prompt("Generate a story"))
```

## Common Patterns

### RAG Pattern
```synapse
# Store documents
docs = ["Doc 1 content", "Doc 2 content", "Doc 3 content"]
for (doc in docs) {
    vector.store("knowledge", embed(doc))
}

# Query
user_question = "What is the answer?"
relevant = vector.search("knowledge", embed(user_question), 3)

# Generate answer with context
answer = llm.gpt4("Context: " + relevant + "\nQuestion: " + user_question)
```

### Async Data Processing
```synapse
async fn processDocument(doc) {
    summary = await llm.gpt4("Summarize: " + doc)
    embedding = embed(summary)
    vector.store("summaries", embedding)
    return summary
}

# Process multiple documents
docs = ["Doc 1", "Doc 2", "Doc 3"]
for (doc in docs) {
    summary = await processDocument(doc)
}
```

### Semantic Search Pipeline
```synapse
# Index documents
documents = ["AI is transforming tech", "ML learns from data"]
for (doc in documents) {
    vector.store("docs", embed(doc))
}

# Search
query = "technology transformation"
matches = vector.search("docs", embed(query), 5)

# Process results
for (match in matches) {
    response = prompt("Explain: " + match)
}
```

## Data Types

- **Number**: `42`, `3.14`
- **String**: `"hello"`, `'world'`
- **Boolean**: `true`, `false`
- **List**: `[1, 2, 3]`, `["a", "b"]`
- **Embedding**: List of floats from `embed()`

## Operators

- **Arithmetic**: `+`, `-`, `*`, `/`
- **Comparison**: `==`, `!=`, `<`, `>`
- **Assignment**: `=`

## Comments

```synapse
# This is a single-line comment
```

## Built-in Functions

| Function | Description | Example |
|----------|-------------|---------|
| `prompt(text)` | Execute AI prompt | `prompt("What is AI?")` |
| `embed(text)` | Generate embedding | `embed("some text")` |
| `llm.model(text)` | Call LLM model | `llm.gpt4("prompt")` |
| `vector.store(col, vec)` | Store vector | `vector.store("docs", vec)` |
| `vector.search(col, q, n)` | Search vectors | `vector.search("docs", qvec, 10)` |
| `stream(expr)` | Stream response | `stream(prompt("text"))` |
| `await expr` | Await async | `await asyncFunc()` |

## Example Programs

See the `examples/` directory:
- `01_prompt_execution.syn` - Basic prompts
- `02_vector_db.syn` - Vector operations
- `03_async_streaming.syn` - Async features
- `04_llm_invocation.syn` - LLM calls
- `05_complete_app.syn` - Full application

## Error Handling

Currently, errors are raised as Python exceptions. Future versions will include try/catch syntax.

## Tips

1. **Start simple**: Begin with basic prompts and variables
2. **Use vector search**: Great for semantic similarity
3. **Async for I/O**: Use async functions for LLM calls
4. **Stream long responses**: Use `stream()` for better UX
5. **Test incrementally**: Test features one at a time

## More Information

- Full docs: `docs/README.md`
- Language spec: `docs/SPECIFICATION.md`
- Implementation: `IMPLEMENTATION_SUMMARY.md`
