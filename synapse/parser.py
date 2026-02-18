"""
Parser for Synapse Programming Language
Builds an Abstract Syntax Tree (AST) from tokens
"""

from dataclasses import dataclass
from typing import List, Optional, Any
from synapse.lexer import Token, TokenType, Lexer


@dataclass
class ASTNode:
    """Base class for AST nodes"""
    pass


@dataclass
class Program(ASTNode):
    statements: List[ASTNode]


@dataclass
class PromptExpr(ASTNode):
    """Prompt execution expression"""
    content: ASTNode
    model: Optional[str] = None


@dataclass
class LLMCall(ASTNode):
    """Direct LLM invocation"""
    model: str
    prompt: ASTNode
    params: dict


@dataclass
class AsyncExpr(ASTNode):
    """Async expression"""
    body: ASTNode


@dataclass
class AwaitExpr(ASTNode):
    """Await expression"""
    expr: ASTNode


@dataclass
class StreamExpr(ASTNode):
    """Stream expression"""
    source: ASTNode


@dataclass
class VectorStore(ASTNode):
    """Vector store operation"""
    collection: str
    embedding: ASTNode


@dataclass
class VectorSearch(ASTNode):
    """Vector search operation"""
    collection: str
    query: ASTNode
    limit: Optional[int] = 10


@dataclass
class EmbedExpr(ASTNode):
    """Embedding expression"""
    content: ASTNode


@dataclass
class FunctionDef(ASTNode):
    name: str
    params: List[str]
    body: List[ASTNode]
    is_async: bool = False


@dataclass
class FunctionCall(ASTNode):
    name: str
    args: List[ASTNode]


@dataclass
class Assignment(ASTNode):
    name: str
    value: ASTNode


@dataclass
class BinaryOp(ASTNode):
    left: ASTNode
    operator: str
    right: ASTNode


@dataclass
class IfStatement(ASTNode):
    condition: ASTNode
    then_body: List[ASTNode]
    else_body: Optional[List[ASTNode]] = None


@dataclass
class ForLoop(ASTNode):
    variable: str
    iterable: ASTNode
    body: List[ASTNode]


@dataclass
class WhileLoop(ASTNode):
    condition: ASTNode
    body: List[ASTNode]


@dataclass
class ReturnStatement(ASTNode):
    value: Optional[ASTNode] = None


@dataclass
class Identifier(ASTNode):
    name: str


@dataclass
class Literal(ASTNode):
    value: Any


@dataclass
class ListLiteral(ASTNode):
    elements: List[ASTNode]


@dataclass
class DictLiteral(ASTNode):
    pairs: List[tuple]


class Parser:
    """Parses tokens into an AST"""
    
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0
    
    def current_token(self) -> Token:
        if self.pos >= len(self.tokens):
            return self.tokens[-1]
        return self.tokens[self.pos]
    
    def peek_token(self, offset: int = 1) -> Token:
        pos = self.pos + offset
        if pos >= len(self.tokens):
            return self.tokens[-1]
        return self.tokens[pos]
    
    def advance(self):
        self.pos += 1
    
    def skip_newlines(self):
        while self.current_token().type == TokenType.NEWLINE:
            self.advance()
    
    def expect(self, token_type: TokenType) -> Token:
        token = self.current_token()
        if token.type != token_type:
            raise SyntaxError(f"Expected {token_type}, got {token.type} at line {token.line}")
        self.advance()
        return token
    
    def parse(self) -> Program:
        statements = []
        self.skip_newlines()
        
        while self.current_token().type != TokenType.EOF:
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
            self.skip_newlines()
        
        return Program(statements)
    
    def parse_statement(self) -> Optional[ASTNode]:
        self.skip_newlines()
        token = self.current_token()
        
        if token.type == TokenType.FUNCTION:
            return self.parse_function()
        elif token.type == TokenType.ASYNC:
            return self.parse_async_statement()
        elif token.type == TokenType.IF:
            return self.parse_if_statement()
        elif token.type == TokenType.FOR:
            return self.parse_for_loop()
        elif token.type == TokenType.WHILE:
            return self.parse_while_loop()
        elif token.type == TokenType.RETURN:
            return self.parse_return()
        elif token.type == TokenType.IDENTIFIER:
            return self.parse_assignment_or_expr()
        else:
            return self.parse_expression()
    
    def parse_function(self) -> FunctionDef:
        is_async = False
        if self.current_token().type == TokenType.ASYNC:
            is_async = True
            self.advance()
        
        self.expect(TokenType.FUNCTION)
        name = self.expect(TokenType.IDENTIFIER).value
        
        self.expect(TokenType.LPAREN)
        params = []
        while self.current_token().type != TokenType.RPAREN:
            params.append(self.expect(TokenType.IDENTIFIER).value)
            if self.current_token().type == TokenType.COMMA:
                self.advance()
        self.expect(TokenType.RPAREN)
        
        self.skip_newlines()
        self.expect(TokenType.LBRACE)
        self.skip_newlines()
        
        body = []
        while self.current_token().type != TokenType.RBRACE:
            stmt = self.parse_statement()
            if stmt:
                body.append(stmt)
            self.skip_newlines()
        
        self.expect(TokenType.RBRACE)
        
        return FunctionDef(name, params, body, is_async)
    
    def parse_async_statement(self) -> ASTNode:
        self.expect(TokenType.ASYNC)
        
        if self.current_token().type == TokenType.FUNCTION:
            return self.parse_function()
        
        body = self.parse_expression()
        return AsyncExpr(body)
    
    def parse_if_statement(self) -> IfStatement:
        self.expect(TokenType.IF)
        self.expect(TokenType.LPAREN)
        condition = self.parse_expression()
        self.expect(TokenType.RPAREN)
        
        self.skip_newlines()
        self.expect(TokenType.LBRACE)
        self.skip_newlines()
        
        then_body = []
        while self.current_token().type != TokenType.RBRACE:
            stmt = self.parse_statement()
            if stmt:
                then_body.append(stmt)
            self.skip_newlines()
        
        self.expect(TokenType.RBRACE)
        
        else_body = None
        if self.current_token().type == TokenType.ELSE:
            self.advance()
            self.skip_newlines()
            self.expect(TokenType.LBRACE)
            self.skip_newlines()
            
            else_body = []
            while self.current_token().type != TokenType.RBRACE:
                stmt = self.parse_statement()
                if stmt:
                    else_body.append(stmt)
                self.skip_newlines()
            
            self.expect(TokenType.RBRACE)
        
        return IfStatement(condition, then_body, else_body)
    
    def parse_for_loop(self) -> ForLoop:
        self.expect(TokenType.FOR)
        self.expect(TokenType.LPAREN)
        variable = self.expect(TokenType.IDENTIFIER).value
        self.expect(TokenType.IN)
        iterable = self.parse_expression()
        self.expect(TokenType.RPAREN)
        
        self.skip_newlines()
        self.expect(TokenType.LBRACE)
        self.skip_newlines()
        
        body = []
        while self.current_token().type != TokenType.RBRACE:
            stmt = self.parse_statement()
            if stmt:
                body.append(stmt)
            self.skip_newlines()
        
        self.expect(TokenType.RBRACE)
        
        return ForLoop(variable, iterable, body)
    
    def parse_while_loop(self) -> WhileLoop:
        self.expect(TokenType.WHILE)
        self.expect(TokenType.LPAREN)
        condition = self.parse_expression()
        self.expect(TokenType.RPAREN)
        
        self.skip_newlines()
        self.expect(TokenType.LBRACE)
        self.skip_newlines()
        
        body = []
        while self.current_token().type != TokenType.RBRACE:
            stmt = self.parse_statement()
            if stmt:
                body.append(stmt)
            self.skip_newlines()
        
        self.expect(TokenType.RBRACE)
        
        return WhileLoop(condition, body)
    
    def parse_return(self) -> ReturnStatement:
        self.expect(TokenType.RETURN)
        
        if self.current_token().type in [TokenType.NEWLINE, TokenType.SEMICOLON]:
            return ReturnStatement(None)
        
        value = self.parse_expression()
        return ReturnStatement(value)
    
    def parse_assignment_or_expr(self) -> ASTNode:
        name = self.current_token().value
        self.advance()
        
        if self.current_token().type == TokenType.ASSIGN:
            self.advance()
            value = self.parse_expression()
            return Assignment(name, value)
        else:
            self.pos -= 1
            return self.parse_expression()
    
    def parse_expression(self) -> ASTNode:
        return self.parse_comparison()
    
    def parse_comparison(self) -> ASTNode:
        left = self.parse_additive()
        
        while self.current_token().type in [TokenType.EQUAL, TokenType.NOT_EQUAL, 
                                           TokenType.LESS_THAN, TokenType.GREATER_THAN]:
            op = self.current_token().value
            self.advance()
            right = self.parse_additive()
            left = BinaryOp(left, op, right)
        
        return left
    
    def parse_additive(self) -> ASTNode:
        left = self.parse_multiplicative()
        
        while self.current_token().type in [TokenType.PLUS, TokenType.MINUS]:
            op = self.current_token().value
            self.advance()
            right = self.parse_multiplicative()
            left = BinaryOp(left, op, right)
        
        return left
    
    def parse_multiplicative(self) -> ASTNode:
        left = self.parse_unary()
        
        while self.current_token().type in [TokenType.MULTIPLY, TokenType.DIVIDE]:
            op = self.current_token().value
            self.advance()
            right = self.parse_unary()
            left = BinaryOp(left, op, right)
        
        return left
    
    def parse_unary(self) -> ASTNode:
        return self.parse_primary()
    
    def parse_primary(self) -> ASTNode:
        token = self.current_token()
        
        # Prompt expression
        if token.type == TokenType.PROMPT:
            self.advance()
            self.expect(TokenType.LPAREN)
            content = self.parse_expression()
            self.expect(TokenType.RPAREN)
            return PromptExpr(content)
        
        # LLM call
        if token.type == TokenType.LLM:
            self.advance()
            self.expect(TokenType.DOT)
            model = self.expect(TokenType.IDENTIFIER).value
            self.expect(TokenType.LPAREN)
            prompt = self.parse_expression()
            self.expect(TokenType.RPAREN)
            return LLMCall(model, prompt, {})
        
        # Await expression
        if token.type == TokenType.AWAIT:
            self.advance()
            expr = self.parse_expression()
            return AwaitExpr(expr)
        
        # Stream expression
        if token.type == TokenType.STREAM:
            self.advance()
            self.expect(TokenType.LPAREN)
            source = self.parse_expression()
            self.expect(TokenType.RPAREN)
            return StreamExpr(source)
        
        # Embed expression
        if token.type == TokenType.EMBED:
            self.advance()
            self.expect(TokenType.LPAREN)
            content = self.parse_expression()
            self.expect(TokenType.RPAREN)
            return EmbedExpr(content)
        
        # Vector operations
        if token.type == TokenType.VECTOR:
            self.advance()
            self.expect(TokenType.DOT)
            
            # Handle both keyword and identifier for operation
            op_token = self.current_token()
            if op_token.type == TokenType.STORE:
                operation = "store"
                self.advance()
            elif op_token.type == TokenType.SEARCH:
                operation = "search"
                self.advance()
            elif op_token.type == TokenType.IDENTIFIER:
                operation = op_token.value
                self.advance()
            else:
                raise SyntaxError(f"Expected operation after 'vector.' at line {op_token.line}")
            
            if operation == "store":
                self.expect(TokenType.LPAREN)
                collection = self.expect(TokenType.STRING).value
                self.expect(TokenType.COMMA)
                embedding = self.parse_expression()
                self.expect(TokenType.RPAREN)
                return VectorStore(collection, embedding)
            elif operation == "search":
                self.expect(TokenType.LPAREN)
                collection = self.expect(TokenType.STRING).value
                self.expect(TokenType.COMMA)
                query = self.parse_expression()
                limit = 10
                if self.current_token().type == TokenType.COMMA:
                    self.advance()
                    limit = self.expect(TokenType.NUMBER).value
                self.expect(TokenType.RPAREN)
                return VectorSearch(collection, query, limit)
        
        # String
        if token.type == TokenType.STRING:
            self.advance()
            return Literal(token.value)
        
        # Number
        if token.type == TokenType.NUMBER:
            self.advance()
            return Literal(token.value)
        
        # Boolean
        if token.type == TokenType.BOOLEAN:
            self.advance()
            return Literal(token.value)
        
        # List literal
        if token.type == TokenType.LBRACKET:
            self.advance()
            elements = []
            while self.current_token().type != TokenType.RBRACKET:
                elements.append(self.parse_expression())
                if self.current_token().type == TokenType.COMMA:
                    self.advance()
            self.expect(TokenType.RBRACKET)
            return ListLiteral(elements)
        
        # Identifier (variable or function call)
        if token.type == TokenType.IDENTIFIER:
            name = token.value
            self.advance()
            
            # Function call
            if self.current_token().type == TokenType.LPAREN:
                self.advance()
                args = []
                while self.current_token().type != TokenType.RPAREN:
                    args.append(self.parse_expression())
                    if self.current_token().type == TokenType.COMMA:
                        self.advance()
                self.expect(TokenType.RPAREN)
                return FunctionCall(name, args)
            
            return Identifier(name)
        
        # Parenthesized expression
        if token.type == TokenType.LPAREN:
            self.advance()
            expr = self.parse_expression()
            self.expect(TokenType.RPAREN)
            return expr
        
        raise SyntaxError(f"Unexpected token {token.type} at line {token.line}")
