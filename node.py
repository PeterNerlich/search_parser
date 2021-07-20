from token import tok_name
from search_parser.search_tokenize import TokenInfo


def short_token(tok: TokenInfo) -> str:
    s = tok.string
    if s == '' or s.isspace():
        return tok_name[tok.type]
    else:
        return repr(s)


def alt_repr(x) -> str:
    if isinstance(x, TokenInfo):
        return short_token(x)
    else:
        return repr(x)

def pretty(x, indent=0, indent_step=2) -> str:
    if isinstance(x, TokenInfo):
        return short_token(x)
    elif isinstance(x, Node):
        return x.pretty(indent=indent, indent_step=indent_step)
    elif isinstance(x, list):
        tmp = [pretty(el, indent=indent+1, indent_step=indent_step) for el in x]
        if any([isinstance(el, Node) for el in x]) or any([len(el.split("\n")) > 1 for el in tmp]):
            return "[\n{}{}\n{}]".format(' '*(indent+1)*indent_step, ",\n{}".format(' '*(indent+1)*indent_step).join(tmp), ' '*indent*indent_step)
        else:
            return "[{}]".format(', '.join(tmp))
    else:
        return "\n{}".format(' '*indent*indent_step).join(repr(x).split("\n"))


class Node:

    def __init__(self, type, children):
        self.type = type
        self.children = children

    def __repr__(self):
        return f"Node({self.type}, [{', '.join(map(alt_repr, self.children))}])"
        #return "Node({}, [\n{}\n])".format(self.type, ",\n".join(map(lambda x: '  '+x, map(alt_repr, self.children))))
        #return self.pretty()
    
    def pretty(self, indent=0, indent_step=2):
        return "Node({}, {})".format(self.type, pretty(self.children, indent=indent, indent_step=indent_step))

    def __eq__(self, other):
        if not isinstance(other, Node):
            return NotImplemented
        return self.type == other.type and self.children == other.children
