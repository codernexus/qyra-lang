from dataclasses import dataclass
from enum import Enum, auto
from .errors import Span

class Kind(Enum):
    EOF=auto(); IDENT=auto(); NUMBER=auto(); STRING=auto()
    LET=auto(); VAR=auto(); FUNC=auto(); RETURN=auto(); IF=auto(); ELSE=auto(); WHILE=auto(); TRUE=auto(); FALSE=auto(); NULL=auto(); PRINT=auto()
    LPAREN=auto(); RPAREN=auto(); LBRACE=auto(); RBRACE=auto(); COMMA=auto(); SEMI=auto(); COLON=auto(); ARROW=auto()
    PLUS=auto(); MINUS=auto(); STAR=auto(); SLASH=auto(); PERCENT=auto(); BANG=auto(); EQ=auto(); EQEQ=auto(); NE=auto(); LT=auto(); LE=auto(); GT=auto(); GE=auto(); AND=auto(); OR=auto()

@dataclass
class Token:
    kind: Kind
    text: str
    value: object
    span: Span
