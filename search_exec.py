#!/usr/bin/env python3.8

import argparse
import os
import sys
from io import StringIO

from search_parser.search_tokenize import generate_tokens
from search_parser.tokenizer import Tokenizer
from search_parser.generator3 import check, generate
from search_parser.visualizer import Visualizer
from search_parser.search import SearchParser

argparser = argparse.ArgumentParser()
argparser.add_argument("program", nargs="*", help="Program to parse")
argparser.add_argument("-v", "--visualize", action="store_true", help="Use visualizer")


def main():
    args = argparser.parse_args()
    file = StringIO(' '.join(args.program))
    
    tokengen = generate_tokens(file.readline)
    vis = None
    if args.visualize:
        vis = Visualizer()
    try:
        tok = Tokenizer(tokengen, vis)
        p = SearchParser(tok)
        program = p.start()
        if vis:
            vis.done()
    finally:
        if vis:
            vis.close()

    if not program:
        if tok.tokens:
            last = tok.tokens[-1]
            print(f"Line {last.start[0]}:")
            print(last.line)
            print(" "*last.start[1] + "^")
        sys.exit("SyntaxError")

    print(repr(program))
    print(str(program))


if __name__ == '__main__':
    main()
