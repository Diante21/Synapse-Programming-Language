"""
Lexer for Synapse Programming Language
Tokenizes source code into tokens for parsing
"""

import re
from enum import Enum, auto
from dataclasses import dataclass
from typing import List, Optional, Any


class TokenType(Enum):
    # Keywords
    PROMPT = auto()
    ASYNC = auto()
    AWAIT = auto()
    STREAM = auto()
    LLM = auto()
    VECTOR = auto()
    EMBED = auto()
    SEARCH = auto()
    STORE = auto()
    FUNCTION = auto()
    RETURN = auto()
    IF = auto()
    ELSE = auto()
    FOR = auto()
    IN = auto()
    WHILE = auto()
    
    # Literals
    STRING = auto()
    NUMBER = auto()
    BOOLEAN = auto()
    IDENTIFIER = auto()
    
    # Operators
    ASSIGN = auto()
    PLUS = auto()
    MINUS = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    EQUAL = auto()
    NOT_EQUAL = auto()
    LESS_THAN = auto()
    GREATER_THAN = auto()
    ARROW = auto()
    
    # Delimiters
    LPAREN = auto()
    RPAREN = auto()
    LBRACE = auto()
    RBRACE = auto()
    LBRACKET = auto()
    RBRACKET = auto()
    COMMA = auto()
    SEMICOLON = auto()
    COLON = auto()
    DOT = auto()
    
    # Special
    NEWLINE = auto()
    EOF = auto()


@dataclass
class Token:
    type: TokenType
    value: Any
    line: int
    column: int


class Lexer:
    """Tokenizes Synapse source code"""
    
    KEYWORDS = {
        'prompt': TokenType.PROMPT,
        'async': TokenType.ASYNC,
        'await': TokenType.AWAIT,
        'stream': TokenType.STREAM,
        'llm': TokenType.LLM,
        'vector': TokenType.VECTOR,
        'embed': TokenType.EMBED,
        'search': TokenType.SEARCH,
        'store': TokenType.STORE,
        'fn': TokenType.FUNCTION,
        'return': TokenType.RETURN,
        'if': TokenType.IF,
        'else': TokenType.ELSE,
        'for': TokenType.FOR,
        'in': TokenType.IN,
        'while': TokenType.WHILE,
        'true': TokenType.BOOLEAN,
        'false': TokenType.BOOLEAN,
    }
    
    def __init__(self, source: str):
        self.source = source
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens: List[Token] = []
    
    def current_char(self) -> Optional[str]:
        if self.pos >= len(self.source):
            return None
        return self.source[self.pos]
    
    def peek_char(self, offset: int = 1) -> Optional[str]:
        pos = self.pos + offset
        if pos >= len(self.source):
            return None
        return self.source[pos]
    
    def advance(self):
        if self.pos < len(self.source) and self.source[self.pos] == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        self.pos += 1
    
    def skip_whitespace(self):
        while self.current_char() and self.current_char() in ' \t\r':
            self.advance()
    
    def skip_comment(self):
        if self.current_char() == '#':
            while self.current_char() and self.current_char() != '\n':
                self.advance()
    
    def read_string(self) -> str:
        quote = self.current_char()
        self.advance()
        result = ''
        
        while self.current_char() and self.current_char() != quote:
            if self.current_char() == '\\':
                self.advance()
                if self.current_char() == 'n':
                    result += '\n'
                elif self.current_char() == 't':
                    result += '\t'
                elif self.current_char() == '\\':
                    result += '\\'
                elif self.current_char() == quote:
                    result += quote
                else:
                    result += self.current_char()
                self.advance()
            else:
                result += self.current_char()
                self.advance()
        
        self.advance()  # Skip closing quote
        return result
    
    def read_number(self) -> float:
        result = ''
        has_dot = False
        
        while self.current_char() and (self.current_char().isdigit() or self.current_char() == '.'):
            if self.current_char() == '.':
                if has_dot:
                    break
                has_dot = True
            result += self.current_char()
            self.advance()
        
        return float(result) if has_dot else int(result)
    
    def read_identifier(self) -> str:
        result = ''
        
        while self.current_char() and (self.current_char().isalnum() or self.current_char() == '_'):
            result += self.current_char()
            self.advance()
        
        return result
    
    def tokenize(self) -> List[Token]:
        while self.current_char():
            self.skip_whitespace()
            
            if not self.current_char():
                break
            
            # Skip comments
            if self.current_char() == '#':
                self.skip_comment()
                continue
            
            line = self.line
            column = self.column
            
            # Newline
            if self.current_char() == '\n':
                self.tokens.append(Token(TokenType.NEWLINE, '\n', line, column))
                self.advance()
                continue
            
            # Strings
            if self.current_char() in '"\'':
                value = self.read_string()
                self.tokens.append(Token(TokenType.STRING, value, line, column))
                continue
            
            # Numbers
            if self.current_char().isdigit():
                value = self.read_number()
                self.tokens.append(Token(TokenType.NUMBER, value, line, column))
                continue
            
            # Identifiers and keywords
            if self.current_char().isalpha() or self.current_char() == '_':
                value = self.read_identifier()
                token_type = self.KEYWORDS.get(value, TokenType.IDENTIFIER)
                
                if value in ['true', 'false']:
                    self.tokens.append(Token(token_type, value == 'true', line, column))
                else:
                    self.tokens.append(Token(token_type, value, line, column))
                continue
            
            # Two-character operators
            if self.current_char() == '=' and self.peek_char() == '=':
                self.tokens.append(Token(TokenType.EQUAL, '==', line, column))
                self.advance()
                self.advance()
                continue
            
            if self.current_char() == '!' and self.peek_char() == '=':
                self.tokens.append(Token(TokenType.NOT_EQUAL, '!=', line, column))
                self.advance()
                self.advance()
                continue
            
            if self.current_char() == '-' and self.peek_char() == '>':
                self.tokens.append(Token(TokenType.ARROW, '->', line, column))
                self.advance()
                self.advance()
                continue
            
            # Single-character tokens
            char_tokens = {
                '=': TokenType.ASSIGN,
                '+': TokenType.PLUS,
                '-': TokenType.MINUS,
                '*': TokenType.MULTIPLY,
                '/': TokenType.DIVIDE,
                '<': TokenType.LESS_THAN,
                '>': TokenType.GREATER_THAN,
                '(': TokenType.LPAREN,
                ')': TokenType.RPAREN,
                '{': TokenType.LBRACE,
                '}': TokenType.RBRACE,
                '[': TokenType.LBRACKET,
                ']': TokenType.RBRACKET,
                ',': TokenType.COMMA,
                ';': TokenType.SEMICOLON,
                ':': TokenType.COLON,
                '.': TokenType.DOT,
            }
            
            if self.current_char() in char_tokens:
                self.tokens.append(Token(char_tokens[self.current_char()], self.current_char(), line, column))
                self.advance()
                continue
            
            # Unknown character
            raise SyntaxError(f"Unknown character '{self.current_char()}' at line {line}, column {column}")
        
        self.tokens.append(Token(TokenType.EOF, None, self.line, self.column))
        return self.tokens
