# Synapse Language Specification

## Version 0.1.0

## Overview

Synapse is an AI-native programming language designed to make AI operations first-class citizens in the language.

## Keywords

### AI Operations
- `prompt` - Execute an AI prompt
- `llm` - Direct LLM model invocation
- `embed` - Generate text embeddings
- `vector` - Vector database operations
- `stream` - Stream responses

### Async Operations
- `async` - Define async functions
- `await` - Wait for async operations

### Control Flow
- `fn` - Function definition
- `if` / `else` - Conditional execution
- `for` / `in` - Iteration
- `while` - Loop
- `return` - Return value

## Data Types

### Primitives
- `Number` - Integer or floating point
- `String` - Text enclosed in `"` or `'`
- `Boolean` - `true` or `false`
- `List` - `[elem1, elem2, ...]`
- `Vector` - Embedding vector (list of floats)

### AI Types
- `Prompt` - AI prompt result
- `Embedding` - Vector embedding
- `Stream` - Streaming response

## Syntax

### Variables
```synapse
name = value
x = 42
text = "hello"
flag = true
```

### Functions
```synapse
fn functionName(param1, param2) {
    # function body
    return value
}

# Async functions
async fn asyncFunction(param) {
    result = await someOperation()
    return result
}
```

### Control Flow
```synapse
# If-else
if (condition) {
    # then branch
} else {
    # else branch
}

# For loop
for (item in collection) {
    # loop body
}

# While loop
while (condition) {
    # loop body
}
```

### AI Operations

#### Prompt Execution
```synapse
result = prompt("Your prompt here")
```

#### LLM Invocation
```synapse
response = llm.modelName("Your prompt")
# Examples: llm.gpt4(), llm.claude(), llm.llama()
```

#### Embeddings
```synapse
vector = embed("Text to embed")
```

#### Vector Database
```synapse
# Store embedding
vector.store("collection_name", embedding)

# Search for similar vectors
results = vector.search("collection_name", query_vector, limit)
```

#### Streaming
```synapse
streamed = stream(prompt("Generate long response"))
```

### Operators

#### Arithmetic
- `+` Addition
- `-` Subtraction
- `*` Multiplication
- `/` Division

#### Comparison
- `==` Equal
- `!=` Not equal
- `<` Less than
- `>` Greater than

#### Assignment
- `=` Assignment

### Comments
```synapse
# This is a comment
```

## Built-in Functions

### AI Functions
- `prompt(text)` - Execute AI prompt
- `embed(text)` - Generate embedding
- `stream(expr)` - Stream response

### Vector DB Functions
- `vector.store(collection, embedding)` - Store embedding
- `vector.search(collection, query, limit)` - Search vectors

### LLM Functions
- `llm.gpt4(prompt)` - Call GPT-4
- `llm.claude(prompt)` - Call Claude
- `llm.llama(prompt)` - Call Llama
- (Extensible to any model)

## Grammar

```
program         ::= statement*
statement       ::= function_def | async_stmt | if_stmt | for_loop | 
                   while_loop | return_stmt | assignment | expression
function_def    ::= ["async"] "fn" IDENTIFIER "(" params ")" "{" statement* "}"
async_stmt      ::= "async" (function_def | expression)
if_stmt         ::= "if" "(" expression ")" "{" statement* "}" ["else" "{" statement* "}"]
for_loop        ::= "for" "(" IDENTIFIER "in" expression ")" "{" statement* "}"
while_loop      ::= "while" "(" expression ")" "{" statement* "}"
return_stmt     ::= "return" [expression]
assignment      ::= IDENTIFIER "=" expression
expression      ::= comparison
comparison      ::= additive (("==" | "!=" | "<" | ">") additive)*
additive        ::= multiplicative (("+" | "-") multiplicative)*
multiplicative  ::= unary (("*" | "/") unary)*
unary           ::= primary
primary         ::= prompt_expr | llm_call | await_expr | stream_expr |
                   embed_expr | vector_op | literal | identifier | 
                   function_call | list | "(" expression ")"
prompt_expr     ::= "prompt" "(" expression ")"
llm_call        ::= "llm" "." IDENTIFIER "(" expression ")"
await_expr      ::= "await" expression
stream_expr     ::= "stream" "(" expression ")"
embed_expr      ::= "embed" "(" expression ")"
vector_op       ::= "vector" "." ("store" | "search") "(" arguments ")"
function_call   ::= IDENTIFIER "(" arguments ")"
literal         ::= STRING | NUMBER | BOOLEAN
list            ::= "[" [expression ("," expression)*] "]"
```

## Future Extensions

### Planned Features
- Type system
- Error handling (try/catch)
- Modules and imports
- Standard library
- Real-time collaboration
- Distributed execution
- Model fine-tuning support
- RAG (Retrieval Augmented Generation) primitives

### Potential Syntax
```synapse
# Type annotations
fn add(a: Number, b: Number) -> Number {
    return a + b
}

# Error handling
try {
    result = llm.gpt4("prompt")
} catch (error) {
    # handle error
}

# Imports
import vector_utils
import llm_helpers

# RAG pattern
context = vector.search("knowledge", embed(query), 5)
answer = llm.gpt4("Context: " + context + "\nQuestion: " + query)
```

## Implementation Notes

The current implementation is in Python and includes:
- Lexer for tokenization
- Recursive descent parser for AST generation
- Async-capable interpreter
- Mock LLM provider (easily extendable to real APIs)
- In-memory vector database with cosine similarity

This specification is subject to change as the language evolves.
