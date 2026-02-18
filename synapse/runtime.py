"""
Runtime/Interpreter for Synapse Programming Language
Executes AST nodes with AI-native features
"""

import asyncio
from typing import Any, Dict, List, Optional
from synapse.parser import (
    ASTNode, Program, PromptExpr, LLMCall, AsyncExpr, AwaitExpr, 
    StreamExpr, VectorStore, VectorSearch, EmbedExpr, FunctionDef,
    FunctionCall, Assignment, BinaryOp, IfStatement, ForLoop, 
    WhileLoop, ReturnStatement, Identifier, Literal, ListLiteral
)


class ReturnValue(Exception):
    """Exception to handle return statements"""
    def __init__(self, value):
        self.value = value


class VectorDB:
    """Built-in vector database for storing and searching embeddings"""
    
    def __init__(self):
        self.collections: Dict[str, List[Dict]] = {}
    
    def store(self, collection: str, embedding: List[float], metadata: Dict = None):
        """Store an embedding in a collection"""
        if collection not in self.collections:
            self.collections[collection] = []
        
        self.collections[collection].append({
            'embedding': embedding,
            'metadata': metadata or {}
        })
    
    def search(self, collection: str, query_embedding: List[float], limit: int = 10) -> List[Dict]:
        """Search for similar embeddings using cosine similarity"""
        if collection not in self.collections:
            return []
        
        results = []
        for item in self.collections[collection]:
            similarity = self._cosine_similarity(query_embedding, item['embedding'])
            results.append({
                'embedding': item['embedding'],
                'metadata': item['metadata'],
                'similarity': similarity
            })
        
        results.sort(key=lambda x: x['similarity'], reverse=True)
        return results[:limit]
    
    @staticmethod
    def _cosine_similarity(a: List[float], b: List[float]) -> float:
        """Calculate cosine similarity between two vectors"""
        dot_product = sum(x * y for x, y in zip(a, b))
        norm_a = sum(x * x for x in a) ** 0.5
        norm_b = sum(x * x for x in b) ** 0.5
        
        if norm_a == 0 or norm_b == 0:
            return 0.0
        
        return dot_product / (norm_a * norm_b)


class LLMProvider:
    """Mock LLM provider for demonstration (in production, this would call real LLM APIs)"""
    
    @staticmethod
    async def call_llm(model: str, prompt: str, params: Dict = None) -> str:
        """Call an LLM model (mock implementation)"""
        await asyncio.sleep(0.1)  # Simulate API call
        return f"[LLM Response from {model}]: Processed prompt: {prompt[:50]}..."
    
    @staticmethod
    async def stream_llm(model: str, prompt: str, params: Dict = None):
        """Stream LLM response (mock implementation)"""
        response = f"[Streaming from {model}]: {prompt}"
        words = response.split()
        
        for word in words:
            await asyncio.sleep(0.05)
            yield word + " "
    
    @staticmethod
    def embed(content: str) -> List[float]:
        """Generate embeddings (mock implementation using simple hash-based approach)"""
        import hashlib
        
        hash_obj = hashlib.md5(content.encode())
        hash_bytes = hash_obj.digest()
        
        # Convert to normalized vector
        embedding = [float(b) / 255.0 for b in hash_bytes[:8]]
        norm = sum(x * x for x in embedding) ** 0.5
        if norm > 0:
            embedding = [x / norm for x in embedding]
        
        return embedding


class Runtime:
    """Runtime environment for executing Synapse programs"""
    
    def __init__(self):
        self.globals: Dict[str, Any] = {}
        self.vector_db = VectorDB()
        self.llm = LLMProvider()
    
    async def execute(self, node: ASTNode, env: Dict[str, Any] = None) -> Any:
        """Execute an AST node"""
        if env is None:
            env = self.globals
        
        if isinstance(node, Program):
            result = None
            for stmt in node.statements:
                result = await self.execute(stmt, env)
            return result
        
        elif isinstance(node, PromptExpr):
            content = await self.execute(node.content, env)
            model = node.model or "default"
            return await self.llm.call_llm(model, str(content))
        
        elif isinstance(node, LLMCall):
            prompt = await self.execute(node.prompt, env)
            return await self.llm.call_llm(node.model, str(prompt), node.params)
        
        elif isinstance(node, AsyncExpr):
            return await self.execute(node.body, env)
        
        elif isinstance(node, AwaitExpr):
            result = await self.execute(node.expr, env)
            if asyncio.iscoroutine(result):
                return await result
            return result
        
        elif isinstance(node, StreamExpr):
            source = await self.execute(node.source, env)
            
            if isinstance(source, PromptExpr):
                content = await self.execute(source.content, env)
                model = source.model or "default"
                
                results = []
                async for chunk in self.llm.stream_llm(model, str(content)):
                    results.append(chunk)
                return ''.join(results)
            
            return source
        
        elif isinstance(node, EmbedExpr):
            content = await self.execute(node.content, env)
            return self.llm.embed(str(content))
        
        elif isinstance(node, VectorStore):
            embedding = await self.execute(node.embedding, env)
            self.vector_db.store(node.collection, embedding)
            return True
        
        elif isinstance(node, VectorSearch):
            query = await self.execute(node.query, env)
            if not isinstance(query, list):
                query = self.llm.embed(str(query))
            return self.vector_db.search(node.collection, query, node.limit)
        
        elif isinstance(node, FunctionDef):
            env[node.name] = node
            return None
        
        elif isinstance(node, FunctionCall):
            func = env.get(node.name)
            if func is None:
                raise NameError(f"Function '{node.name}' is not defined")
            
            if isinstance(func, FunctionDef):
                args = [await self.execute(arg, env) for arg in node.args]
                
                local_env = env.copy()
                for param, arg in zip(func.params, args):
                    local_env[param] = arg
                
                try:
                    for stmt in func.body:
                        await self.execute(stmt, local_env)
                    return None
                except ReturnValue as ret:
                    return ret.value
            
            raise TypeError(f"'{node.name}' is not callable")
        
        elif isinstance(node, Assignment):
            value = await self.execute(node.value, env)
            env[node.name] = value
            return value
        
        elif isinstance(node, BinaryOp):
            left = await self.execute(node.left, env)
            right = await self.execute(node.right, env)
            
            if node.operator == '+':
                return left + right
            elif node.operator == '-':
                return left - right
            elif node.operator == '*':
                return left * right
            elif node.operator == '/':
                return left / right
            elif node.operator == '==':
                return left == right
            elif node.operator == '!=':
                return left != right
            elif node.operator == '<':
                return left < right
            elif node.operator == '>':
                return left > right
        
        elif isinstance(node, IfStatement):
            condition = await self.execute(node.condition, env)
            if condition:
                for stmt in node.then_body:
                    await self.execute(stmt, env)
            elif node.else_body:
                for stmt in node.else_body:
                    await self.execute(stmt, env)
            return None
        
        elif isinstance(node, ForLoop):
            iterable = await self.execute(node.iterable, env)
            for item in iterable:
                local_env = env.copy()
                local_env[node.variable] = item
                for stmt in node.body:
                    await self.execute(stmt, local_env)
            return None
        
        elif isinstance(node, WhileLoop):
            while await self.execute(node.condition, env):
                for stmt in node.body:
                    await self.execute(stmt, env)
            return None
        
        elif isinstance(node, ReturnStatement):
            if node.value:
                value = await self.execute(node.value, env)
                raise ReturnValue(value)
            raise ReturnValue(None)
        
        elif isinstance(node, Identifier):
            if node.name not in env:
                raise NameError(f"Variable '{node.name}' is not defined")
            return env[node.name]
        
        elif isinstance(node, Literal):
            return node.value
        
        elif isinstance(node, ListLiteral):
            return [await self.execute(elem, env) for elem in node.elements]
        
        return None
    
    def run(self, source: str) -> Any:
        """Parse and execute source code"""
        from synapse.lexer import Lexer
        from synapse.parser import Parser
        
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        
        parser = Parser(tokens)
        ast = parser.parse()
        
        return asyncio.run(self.execute(ast))
