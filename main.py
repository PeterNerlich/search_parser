#!/usr/bin/env python3.8

import argparse
import os
import sys
from tokenize import generate_tokens

from search_parser.tokenizer import Tokenizer
from search_parser.generator3 import check, generate
from search_parser.visualizer import Visualizer

argparser = argparse.ArgumentParser()
argparser.add_argument("grammar", nargs="?", help="Grammar file (search.gram)")
argparser.add_argument("-r", "--regen", action="store_true", help="Regenerate grammar")
argparser.add_argument("-o", "--output", help="Output file (search.py)")
argparser.add_argument("-c", "--classname", help="Output class name (SearchParser)")
argparser.add_argument("-v", "--visualize", action="store_true", help="Use visualizer")
argparser.add_argument("-b", "--backup", action="store_true", help="Use old grammar parser")


def main():
    args = argparser.parse_args()
    file = args.grammar
    if not file:
        if args.regen:
            file = "search_parser/grammar.gram"
        else:
            file = "search_parser/search.gram"
    outfile = args.output
    if not outfile:
        head, tail = os.path.split(file)
        base, ext = os.path.splitext(tail)
        if base == "grammar":
            base += "parser"
        outfile = os.path.join(head, base + ".py")
    classname = args.classname

    if args.backup:
        from search_parser.grammar import GrammarParser
    else:
        from search_parser.grammarparser import GrammarParser

    print("Reading", file, file=sys.stderr)
    with open(file) as f:
        tokengen = generate_tokens(f.readline)
        vis = None
        if args.visualize:
            vis = Visualizer()
        try:
            tok = Tokenizer(tokengen, vis)
            p = GrammarParser(tok)
            grammar = p.start()
            if vis:
                vis.done()
        finally:
            if vis:
                vis.close()

    if not grammar:
        if tok.tokens:
            last = tok.tokens[-1]
            print(f"Line {last.start[0]}:")
            print(last.line)
            print(" "*last.start[1] + "^")
        sys.exit("SyntaxError")

    print(repr(grammar))
    print(str(grammar))

    if not classname:
        classname = grammar.metas_dict.get("class")
        if not classname:
            tail = os.path.basename(file)
            base, ext = os.path.splitext(tail)
            classname = base.title() + "Parser"

    errors = check(grammar)
    if errors:
        sys.exit(f"Detected {errors} errors")

    print("Writing class", classname, "to", outfile, file=sys.stderr)
    with open(outfile, "w") as stream:
        generate(grammar, classname, stream)


if __name__ == '__main__':
    main()
