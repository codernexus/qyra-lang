from dataclasses import dataclass
from enum import Enum, auto
class Op(Enum):
    CONST=auto(); LOAD=auto(); DEFINE=auto(); STORE=auto(); POP=auto(); PRINT=auto(); NEG=auto(); NOT=auto(); ADD=auto(); SUB=auto(); MUL=auto(); DIV=auto(); MOD=auto(); EQ=auto(); NE=auto(); LT=auto(); LE=auto(); GT=auto(); GE=auto(); JUMP=auto(); JUMP_IF_FALSE=auto(); CALL=auto(); RETURN=auto(); HALT=auto()
@dataclass
class Ins: op:Op; arg:object=None
@dataclass
class FunctionCode: name:str; params:list; code:list; constants:list
