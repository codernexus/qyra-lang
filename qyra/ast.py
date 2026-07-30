from dataclasses import dataclass
from .errors import Span

@dataclass
class Node: span: Span
@dataclass
class Program(Node): statements:list
@dataclass
class Literal(Node): value:object
@dataclass
class Name(Node): name:str
@dataclass
class Unary(Node): op:str; expr:Node
@dataclass
class Binary(Node): left:Node; op:str; right:Node
@dataclass
class Call(Node): callee:Node; args:list
@dataclass
class Let(Node): name:str; mutable:bool; annotation:str|None; value:Node
@dataclass
class Assign(Node): name:str; value:Node
@dataclass
class ExprStmt(Node): expr:Node
@dataclass
class Block(Node): statements:list
@dataclass
class If(Node): cond:Node; then:Block; otherwise:Block|None
@dataclass
class While(Node): cond:Node; body:Block
@dataclass
class Param: name:str; annotation:str|None; span:Span
@dataclass
class Func(Node): name:str; params:list; return_type:str|None; body:Block
@dataclass
class Return(Node): value:Node|None
