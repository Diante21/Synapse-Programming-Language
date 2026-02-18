"""
Tests for Synapse Programming Language
"""

import unittest
import asyncio
from synapse.lexer import Lexer, TokenType
from synapse.parser import Parser
from synapse.runtime import Runtime


class TestLexer(unittest.TestCase):
    """Test the lexer"""
    
    def test_keywords(self):
        source = "prompt async await stream llm vector embed"
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        
        self.assertEqual(tokens[0].type, TokenType.PROMPT)
        self.assertEqual(tokens[1].type, TokenType.ASYNC)
        self.assertEqual(tokens[2].type, TokenType.AWAIT)
        self.assertEqual(tokens[3].type, TokenType.STREAM)
        self.assertEqual(tokens[4].type, TokenType.LLM)
        self.assertEqual(tokens[5].type, TokenType.VECTOR)
        self.assertEqual(tokens[6].type, TokenType.EMBED)
    
    def test_literals(self):
        source = '"hello" 42 3.14 true false'
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        
        self.assertEqual(tokens[0].type, TokenType.STRING)
        self.assertEqual(tokens[0].value, "hello")
        self.assertEqual(tokens[1].type, TokenType.NUMBER)
        self.assertEqual(tokens[1].value, 42)
        self.assertEqual(tokens[2].type, TokenType.NUMBER)
        self.assertEqual(tokens[2].value, 3.14)
        self.assertEqual(tokens[3].type, TokenType.BOOLEAN)
        self.assertEqual(tokens[3].value, True)
        self.assertEqual(tokens[4].type, TokenType.BOOLEAN)
        self.assertEqual(tokens[4].value, False)
    
    def test_operators(self):
        source = "+ - * / == != < > ="
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        
        self.assertEqual(tokens[0].type, TokenType.PLUS)
        self.assertEqual(tokens[1].type, TokenType.MINUS)
        self.assertEqual(tokens[2].type, TokenType.MULTIPLY)
        self.assertEqual(tokens[3].type, TokenType.DIVIDE)
        self.assertEqual(tokens[4].type, TokenType.EQUAL)
        self.assertEqual(tokens[5].type, TokenType.NOT_EQUAL)
        self.assertEqual(tokens[6].type, TokenType.LESS_THAN)
        self.assertEqual(tokens[7].type, TokenType.GREATER_THAN)
        self.assertEqual(tokens[8].type, TokenType.ASSIGN)
    
    def test_identifiers(self):
        source = "x my_var _private"
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        
        self.assertEqual(tokens[0].type, TokenType.IDENTIFIER)
        self.assertEqual(tokens[0].value, "x")
        self.assertEqual(tokens[1].type, TokenType.IDENTIFIER)
        self.assertEqual(tokens[1].value, "my_var")
        self.assertEqual(tokens[2].type, TokenType.IDENTIFIER)
        self.assertEqual(tokens[2].value, "_private")


class TestParser(unittest.TestCase):
    """Test the parser"""
    
    def test_assignment(self):
        source = 'x = 42'
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        self.assertEqual(len(ast.statements), 1)
        from synapse.parser import Assignment
        self.assertIsInstance(ast.statements[0], Assignment)
    
    def test_prompt_expr(self):
        source = 'result = prompt("test")'
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        self.assertEqual(len(ast.statements), 1)
        from synapse.parser import Assignment, PromptExpr
        stmt = ast.statements[0]
        self.assertIsInstance(stmt, Assignment)
        self.assertIsInstance(stmt.value, PromptExpr)
    
    def test_function_def(self):
        source = 'fn add(a, b) { return a + b }'
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        self.assertEqual(len(ast.statements), 1)
        from synapse.parser import FunctionDef
        self.assertIsInstance(ast.statements[0], FunctionDef)
        self.assertEqual(ast.statements[0].name, "add")
        self.assertEqual(len(ast.statements[0].params), 2)


class TestRuntime(unittest.TestCase):
    """Test the runtime"""
    
    def test_basic_arithmetic(self):
        runtime = Runtime()
        result = runtime.run('x = 5 + 3')
        self.assertEqual(runtime.globals['x'], 8)
    
    def test_variable_assignment(self):
        runtime = Runtime()
        runtime.run('name = "Synapse"')
        self.assertEqual(runtime.globals['name'], "Synapse")
    
    def test_function_call(self):
        runtime = Runtime()
        source = '''
fn double(x) {
    return x * 2
}
result = double(21)
'''
        runtime.run(source)
        self.assertEqual(runtime.globals['result'], 42)
    
    def test_embedding(self):
        runtime = Runtime()
        source = 'vec = embed("test")'
        runtime.run(source)
        
        self.assertIsInstance(runtime.globals['vec'], list)
        self.assertTrue(len(runtime.globals['vec']) > 0)
    
    def test_vector_operations(self):
        runtime = Runtime()
        source = '''
vec = embed("test document")
vector.store("docs", vec)
results = vector.search("docs", vec, 1)
'''
        runtime.run(source)
        results = runtime.globals['results']
        
        self.assertIsInstance(results, list)
        self.assertEqual(len(results), 1)
    
    def test_if_statement(self):
        runtime = Runtime()
        source = '''
x = 10
if (x > 5) {
    y = 1
} else {
    y = 0
}
'''
        runtime.run(source)
        self.assertEqual(runtime.globals['y'], 1)


class TestAIFeatures(unittest.TestCase):
    """Test AI-specific features"""
    
    def test_prompt_execution(self):
        runtime = Runtime()
        source = 'result = prompt("test")'
        runtime.run(source)
        
        self.assertIn('result', runtime.globals)
        self.assertIsInstance(runtime.globals['result'], str)
    
    def test_llm_call(self):
        runtime = Runtime()
        source = 'response = llm.gpt4("test")'
        runtime.run(source)
        
        self.assertIn('response', runtime.globals)
        self.assertIsInstance(runtime.globals['response'], str)
    
    def test_async_function(self):
        runtime = Runtime()
        source = '''
async fn process(text) {
    result = llm.gpt4(text)
    return result
}
output = await process("hello")
'''
        runtime.run(source)
        
        self.assertIn('output', runtime.globals)
        self.assertIsInstance(runtime.globals['output'], str)


if __name__ == '__main__':
    unittest.main()
