#!/usr/bin/env python3
"""
Synapse Programming Language CLI
"""

import sys
import argparse
from synapse.runtime import Runtime


def main():
    parser = argparse.ArgumentParser(description='Synapse Programming Language Interpreter')
    parser.add_argument('file', nargs='?', help='Synapse source file to execute')
    parser.add_argument('-c', '--code', help='Execute code directly')
    parser.add_argument('-v', '--version', action='version', version='Synapse 0.1.0')
    
    args = parser.parse_args()
    
    runtime = Runtime()
    
    if args.code:
        try:
            result = runtime.run(args.code)
            if result is not None:
                print(result)
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
    elif args.file:
        try:
            with open(args.file, 'r') as f:
                source = f.read()
            result = runtime.run(source)
            if result is not None:
                print(result)
        except FileNotFoundError:
            print(f"Error: File '{args.file}' not found", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print("Synapse Programming Language v0.1.0")
        print("Usage: synapse <file> or synapse -c '<code>'")


if __name__ == '__main__':
    main()
