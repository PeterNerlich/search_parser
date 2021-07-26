# This is @generated code; do not edit!

#from token import ENDMARKER, NAME, NEWLINE, NUMBER, STRING

from search_parser.search_token import ENDMARKER, WORD, NEWLINE, NUMBER, STRING
from search_parser.memo import memoize, memoize_left_rec, no_memoize
from search_parser.node import Node
from search_parser.parser import Parser

# Grammar for searching for protocols or general annotated documents

from typing import Union
from functools import reduce
from bson import SON
from mongoengine.queryset.visitor import Q, QCombination

def acc_text(*acc):
    """
    Merge all fulltext pieces into one single fulltext query (can only be used once)
    and returned it combined with whatever else queries there are.
    """
    text = []
    query = None
    for x in acc:
        if isinstance(x, (Q, QCombination)):
            if query:
                query &= x
            else:
                query = x
        elif isinstance(x, list):
            text.extend(x)
        else:
            raise ValueError("neither Q nor list!\n  {}: {}\n  ( {} )".format(type(x), x, repr(acc)))
    if len(text) > 0:
        q_text = Q(__raw__={"$text": SON({"$search": ' '.join(text)})})
        if query:
            query &= q_text
        else:
            query = q_text
    return query

def negate(atom: Union[Q, QCombination]) -> Union[Q, QCombination]:
    if isinstance(atom, QCombination):
        atom.operation = atom.OR if atom.operation == atom.AND else atom.AND
        for i in range(len(atom.children)):
            atom.children[i] = negate(atom.children[i])
    elif isinstance(atom, Q):
        for k, v in atom.query.items():
            if '$not' in v:
                atom.query[k] = v['$not']
            else:
                atom.query[k] = {'$not': v}
    else:
        raise ValueError('atom neither Q nor QCombination: {}: {}'.format(type(atom), repr(atom)))
    return atom

class SearchParser(Parser):

    @memoize
    def start(self):
        self.show_rule('start', [['expr', 'ENDMARKER']])
        pos = self.mark()
        if (True
            and self.show_index(0, 0)
            and (expr := self.expr()) is not None
            and self.show_index(0, 1)
            and (endmarker := self.expect(ENDMARKER)) is not None
        ):
            self.show_index(0, 0, 2)
            retval = expr
            if retval is not None:
                return retval
        self.reset(pos)
        self.show_index(0, 0, 0)
        return None

    @memoize
    def expr(self):
        self.show_rule('expr', [['term_or_text', 'term_or_text*']])
        pos = self.mark()
        if (True
            and self.show_index(0, 0)
            and (term_or_text := self.term_or_text()) is not None
            and self.show_index(0, 1)
            and (acc := self.loop(False, self.term_or_text)) is not None
        ):
            self.show_index(0, 0, 2)
            retval = acc_text ( term_or_text , * acc )
            if retval is not None:
                return retval
        self.reset(pos)
        self.show_index(0, 0, 0)
        return None

    @memoize
    def term_or_text(self):
        self.show_rule('term_or_text', [['term'], ['fulltext']])
        pos = self.mark()
        if (True
            and self.show_index(0, 0)
            and (term := self.term()) is not None
        ):
            self.show_index(0, 0, 1)
            retval = term
            if retval is not None:
                return retval
        self.reset(pos)
        if (True
            and self.show_index(1, 0)
            and (fulltext := self.fulltext()) is not None
        ):
            self.show_index(1, 0, 1)
            retval = fulltext
            if retval is not None:
                return retval
        self.reset(pos)
        self.show_index(0, 0, 0)
        return None

    @memoize
    def term(self):
        self.show_rule('term', [['and_'], ['or_'], ['atom']])
        pos = self.mark()
        if (True
            and self.show_index(0, 0)
            and (and_ := self.and_()) is not None
        ):
            self.show_index(0, 0, 1)
            retval = and_
            if retval is not None:
                return retval
        self.reset(pos)
        if (True
            and self.show_index(1, 0)
            and (or_ := self.or_()) is not None
        ):
            self.show_index(1, 0, 1)
            retval = or_
            if retval is not None:
                return retval
        self.reset(pos)
        if (True
            and self.show_index(2, 0)
            and (atom := self.atom()) is not None
        ):
            self.show_index(2, 0, 1)
            retval = atom
            if retval is not None:
                return retval
        self.reset(pos)
        self.show_index(0, 0, 0)
        return None

    @memoize
    def and_(self):
        self.show_rule('and_', [['atom', '_synthetic_rule_0+']])
        pos = self.mark()
        if (True
            and self.show_index(0, 0)
            and (atom := self.atom()) is not None
            and self.show_index(0, 1)
            and (acc := self.loop(True, self._synthetic_rule_0)) is not None
        ):
            self.show_index(0, 0, 2)
            retval = reduce ( lambda a , b : a & b , acc , atom )
            if retval is not None:
                return retval
        self.reset(pos)
        self.show_index(0, 0, 0)
        return None

    @memoize
    def or_(self):
        self.show_rule('or_', [['atom', '_synthetic_rule_1+']])
        pos = self.mark()
        if (True
            and self.show_index(0, 0)
            and (atom := self.atom()) is not None
            and self.show_index(0, 1)
            and (acc := self.loop(True, self._synthetic_rule_1)) is not None
        ):
            self.show_index(0, 0, 2)
            retval = reduce ( lambda a , b : a | b , acc , atom )
            if retval is not None:
                return retval
        self.reset(pos)
        self.show_index(0, 0, 0)
        return None

    @memoize
    def atom(self):
        self.show_rule('atom', [['not_'], ['keyval'], ["'('", 'term', "')'"]])
        pos = self.mark()
        if (True
            and self.show_index(0, 0)
            and (not_ := self.not_()) is not None
        ):
            self.show_index(0, 0, 1)
            retval = not_
            if retval is not None:
                return retval
        self.reset(pos)
        if (True
            and self.show_index(1, 0)
            and (keyval := self.keyval()) is not None
        ):
            self.show_index(1, 0, 1)
            retval = keyval
            if retval is not None:
                return retval
        self.reset(pos)
        if (True
            and self.show_index(2, 0)
            and self.expect('(') is not None
            and self.show_index(2, 1)
            and (term := self.term()) is not None
            and self.show_index(2, 2)
            and self.expect(')') is not None
        ):
            self.show_index(2, 0, 3)
            retval = term
            if retval is not None:
                return retval
        self.reset(pos)
        self.show_index(0, 0, 0)
        return None

    @memoize
    def not_(self):
        self.show_rule('not_', [["':'", "'not'", 'atom']])
        pos = self.mark()
        if (True
            and self.show_index(0, 0)
            and self.expect(':') is not None
            and self.show_index(0, 1)
            and self.expect('not') is not None
            and self.show_index(0, 2)
            and (atom := self.atom()) is not None
        ):
            self.show_index(0, 0, 3)
            retval = negate ( atom )
            if retval is not None:
                return retval
        self.reset(pos)
        self.show_index(0, 0, 0)
        return None

    @memoize
    def keyval(self):
        self.show_rule('keyval', [["':'", 'WORD', 'value']])
        pos = self.mark()
        if (True
            and self.show_index(0, 0)
            and self.expect(':') is not None
            and self.show_index(0, 1)
            and (word := self.expect(WORD)) is not None
            and self.show_index(0, 2)
            and (value := self.value()) is not None
        ):
            self.show_index(0, 0, 3)
            retval = Q ( ** {word . string : value} )
            if retval is not None:
                return retval
        self.reset(pos)
        self.show_index(0, 0, 0)
        return None

    @memoize
    def value(self):
        self.show_rule('value', [['WORD'], ['STRING'], ['NUMBER'], ['list']])
        pos = self.mark()
        if (True
            and self.show_index(0, 0)
            and (word := self.expect(WORD)) is not None
        ):
            self.show_index(0, 0, 1)
            retval = word . string
            if retval is not None:
                return retval
        self.reset(pos)
        if (True
            and self.show_index(1, 0)
            and (string := self.expect(STRING)) is not None
        ):
            self.show_index(1, 0, 1)
            retval = string . string
            if retval is not None:
                return retval
        self.reset(pos)
        if (True
            and self.show_index(2, 0)
            and (number := self.expect(NUMBER)) is not None
        ):
            self.show_index(2, 0, 1)
            retval = float ( number . string )
            if retval is not None:
                return retval
        self.reset(pos)
        if (True
            and self.show_index(3, 0)
            and (list := self.list()) is not None
        ):
            self.show_index(3, 0, 1)
            retval = list
            if retval is not None:
                return retval
        self.reset(pos)
        self.show_index(0, 0, 0)
        return None

    @memoize
    def list(self):
        self.show_rule('list', [["'['", 'value', '_synthetic_rule_2*', "']'"]])
        pos = self.mark()
        if (True
            and self.show_index(0, 0)
            and self.expect('[') is not None
            and self.show_index(0, 1)
            and (value := self.value()) is not None
            and self.show_index(0, 2)
            and (acc := self.loop(False, self._synthetic_rule_2)) is not None
            and self.show_index(0, 3)
            and self.expect(']') is not None
        ):
            self.show_index(0, 0, 4)
            retval = [ value ] + acc
            if retval is not None:
                return retval
        self.reset(pos)
        self.show_index(0, 0, 0)
        return None

    @memoize
    def fulltext(self):
        self.show_rule('fulltext', [['_synthetic_rule_3+']])
        pos = self.mark()
        if (True
            and self.show_index(0, 0)
            and (text := self.loop(True, self._synthetic_rule_3)) is not None
        ):
            self.show_index(0, 0, 1)
            retval = text
            if retval is not None:
                return retval
        self.reset(pos)
        self.show_index(0, 0, 0)
        return None

    @memoize
    def _synthetic_rule_0(self):
        self.show_rule('_synthetic_rule_0', [["':'", "'and'", 'atom']])
        pos = self.mark()
        if (True
            and self.show_index(0, 0)
            and self.expect(':') is not None
            and self.show_index(0, 1)
            and self.expect('and') is not None
            and self.show_index(0, 2)
            and (atom := self.atom()) is not None
        ):
            self.show_index(0, 0, 3)
            retval = atom
            if retval is not None:
                return retval
        self.reset(pos)
        self.show_index(0, 0, 0)
        return None

    @memoize
    def _synthetic_rule_1(self):
        self.show_rule('_synthetic_rule_1', [["':'", "'or'", 'atom']])
        pos = self.mark()
        if (True
            and self.show_index(0, 0)
            and self.expect(':') is not None
            and self.show_index(0, 1)
            and self.expect('or') is not None
            and self.show_index(0, 2)
            and (atom := self.atom()) is not None
        ):
            self.show_index(0, 0, 3)
            retval = atom
            if retval is not None:
                return retval
        self.reset(pos)
        self.show_index(0, 0, 0)
        return None

    @memoize
    def _synthetic_rule_2(self):
        self.show_rule('_synthetic_rule_2', [["','", 'value']])
        pos = self.mark()
        if (True
            and self.show_index(0, 0)
            and self.expect(',') is not None
            and self.show_index(0, 1)
            and (value := self.value()) is not None
        ):
            self.show_index(0, 0, 2)
            retval = value
            if retval is not None:
                return retval
        self.reset(pos)
        self.show_index(0, 0, 0)
        return None

    @memoize
    def _synthetic_rule_3(self):
        self.show_rule('_synthetic_rule_3', [['STRING'], ['NUMBER'], ['WORD']])
        pos = self.mark()
        if (True
            and self.show_index(0, 0)
            and (string := self.expect(STRING)) is not None
        ):
            self.show_index(0, 0, 1)
            retval = string . string
            if retval is not None:
                return retval
        self.reset(pos)
        if (True
            and self.show_index(1, 0)
            and (number := self.expect(NUMBER)) is not None
        ):
            self.show_index(1, 0, 1)
            retval = number . string
            if retval is not None:
                return retval
        self.reset(pos)
        if (True
            and self.show_index(2, 0)
            and (word := self.expect(WORD)) is not None
        ):
            self.show_index(2, 0, 1)
            retval = word . string
            if retval is not None:
                return retval
        self.reset(pos)
        self.show_index(0, 0, 0)
        return None

# The end.
