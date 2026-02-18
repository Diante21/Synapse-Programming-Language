#!/usr/bin/env python3
"""
Demonstration of Synapse Programming Language Features
This script shows all AI-native features in action
"""

from synapse.runtime import Runtime


def demo_section(title):
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def main():
    print("\n🚀 Synapse Programming Language - AI Native Demo\n")
    
    runtime = Runtime()
    
    # Demo 1: Prompt Execution
    demo_section("1. Prompt Execution as First-Class Feature")
    code1 = '''
greeting = prompt("Say hello")
'''
    print("Code:")
    print(code1)
    print("Output:")
    runtime.run(code1)
    print(f"Result: {runtime.globals['greeting']}")
    
    # Demo 2: Vector Database
    demo_section("2. Built-in Vector Database Support")
    code2 = '''
# Embed and store documents
doc1 = "Machine learning uses algorithms"
vec1 = embed(doc1)
vector.store("knowledge", vec1)

doc2 = "AI helps automate tasks"
vec2 = embed(doc2)
vector.store("knowledge", vec2)

# Search for similar content
query = "automation with AI"
results = vector.search("knowledge", embed(query), 2)
'''
    print("Code:")
    print(code2)
    print("\nOutput:")
    runtime2 = Runtime()
    runtime2.run(code2)
    print(f"Found {len(runtime2.globals['results'])} similar documents")
    for i, result in enumerate(runtime2.globals['results']):
        print(f"  {i+1}. Similarity: {result['similarity']:.4f}")
    
    # Demo 3: Direct LLM Invocation
    demo_section("3. Direct LLM Invocation")
    code3 = '''
response = llm.gpt4("Explain neural networks")
'''
    print("Code:")
    print(code3)
    print("\nOutput:")
    runtime3 = Runtime()
    runtime3.run(code3)
    print(f"LLM Response: {runtime3.globals['response']}")
    
    # Demo 4: Async Functions
    demo_section("4. Native Async + Streaming")
    code4 = '''
async fn processData(text) {
    result = await llm.gpt4(text)
    return result
}

output = await processData("Process this data")
'''
    print("Code:")
    print(code4)
    print("\nOutput:")
    runtime4 = Runtime()
    runtime4.run(code4)
    print(f"Async Result: {runtime4.globals['output']}")
    
    # Demo 5: Complete AI Application
    demo_section("5. Complete AI Application")
    code5 = '''
# Process and store documents with embeddings
docs = ["AI is transforming industries", "Machine learning learns patterns"]
for (doc in docs) {
    vec = embed(doc)
    vector.store("documents", vec)
}

# Semantic search
query_text = "industry transformation"
matches = vector.search("documents", embed(query_text), 1)

# Generate response
answer = prompt("Summarize the findings")
'''
    print("Code:")
    print(code5)
    print("\nOutput:")
    runtime5 = Runtime()
    runtime5.run(code5)
    print(f"Processed {len(runtime5.globals['docs'])} documents")
    print(f"Found {len(runtime5.globals['matches'])} matches")
    print(f"Answer: {runtime5.globals['answer']}")
    
    # Feature Summary
    demo_section("Feature Summary")
    print("""
✅ Prompt Execution - Execute AI prompts as native operations
✅ Vector Database - Built-in semantic search and storage
✅ Direct LLM Calls - Call any model directly (gpt4, claude, llama)
✅ Async/Await - Native asynchronous programming support
✅ Streaming - Stream LLM responses for real-time output
✅ Embeddings - Generate and work with text embeddings
✅ Functions - Define and call functions (sync and async)
✅ Control Flow - If/else, for loops, while loops
✅ Variables - Dynamic typing with multiple data types

🎯 Synapse makes AI programming as natural as traditional coding!
    """)
    
    print("\n" + "=" * 60)
    print("  Demo Complete!")
    print("=" * 60 + "\n")


if __name__ == '__main__':
    main()
