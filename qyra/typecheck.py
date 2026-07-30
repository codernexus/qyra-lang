from dataclasses import dataclass
from . import ast
from .errors import TypeErrorQyra

BUILTINS={"Int","Float","Bool","Text","Void","Any"}
@dataclass
class Symbol:
    type:str
    mutable:bool

class TypeChecker:
    def __init__(self):
        self.scopes=[{}]; self.functions={}; self.current_return=None
    def error(self,msg,node,hint=None): raise TypeErrorQyra(msg,node.span,hint)
    def define(self,name,sym,node):
        if name in self.scopes[-1]: self.error(f"name '{name}' is already defined",node)
        self.scopes[-1][name]=sym
    def lookup(self,name,node):
        for scope in reversed(self.scopes):
            if name in scope:return scope[name]
        self.error(f"unknown name '{name}'",node,"declare it before use")
    def check(self,p):
        for s in p.statements:
            if isinstance(s,ast.Func):
                if s.name in self.functions:self.error(f"function '{s.name}' is already defined",s)
                for param in s.params:
                    if param.annotation and param.annotation not in BUILTINS:self.error(f"unknown type '{param.annotation}'",s)
                if s.return_type and s.return_type not in BUILTINS:self.error(f"unknown type '{s.return_type}'",s)
                self.functions[s.name]=s
        for s in p.statements:self.stmt(s)
        return p
    def compatible(self,expected,actual): return expected==actual or expected=="Any" or actual=="Any" or (expected=="Float" and actual=="Int")
    def stmt(self,n):
        if isinstance(n,ast.Let):
            actual=self.expr(n.value); expected=n.annotation or actual
            if n.annotation and n.annotation not in BUILTINS:self.error(f"unknown type '{n.annotation}'",n)
            if not self.compatible(expected,actual):self.error(f"expected {expected}, found {actual}",n)
            self.define(n.name,Symbol(expected,n.mutable),n)
        elif isinstance(n,ast.Assign):
            sym=self.lookup(n.name,n)
            if not sym.mutable:self.error(f"cannot assign to immutable variable '{n.name}'",n,"declare it with var")
            actual=self.expr(n.value)
            if not self.compatible(sym.type,actual):self.error(f"expected {sym.type}, found {actual}",n)
        elif isinstance(n,ast.ExprStmt): self.expr(n.expr)
        elif isinstance(n,ast.Block):
            self.scopes.append({})
            for s in n.statements:self.stmt(s)
            self.scopes.pop()
        elif isinstance(n,ast.If):
            if self.expr(n.cond)!="Bool":self.error("if condition must be Bool",n.cond)
            self.stmt(n.then)
            if n.otherwise:self.stmt(n.otherwise)
        elif isinstance(n,ast.While):
            if self.expr(n.cond)!="Bool":self.error("while condition must be Bool",n.cond)
            self.stmt(n.body)
        elif isinstance(n,ast.Func):
            old=self.current_return; self.current_return=n.return_type or "Any"; self.scopes.append({})
            for p in n.params:self.define(p.name,Symbol(p.annotation or "Any",True),n)
            for s in n.body.statements:self.stmt(s)
            self.scopes.pop(); self.current_return=old
        elif isinstance(n,ast.Return):
            if self.current_return is None:self.error("return outside function",n)
            actual="Void" if n.value is None else self.expr(n.value)
            if not self.compatible(self.current_return,actual):self.error(f"expected return type {self.current_return}, found {actual}",n)
    def expr(self,n):
        if isinstance(n,ast.Literal):
            if n.value is None:return "Any"
            if isinstance(n.value,bool):return "Bool"
            if isinstance(n.value,int):return "Int"
            if isinstance(n.value,float):return "Float"
            return "Text"
        if isinstance(n,ast.Name):
            if n.name=="print":return "Any"
            return self.lookup(n.name,n).type
        if isinstance(n,ast.Unary):
            t=self.expr(n.expr)
            if n.op=="!":
                if t!="Bool":self.error("operator ! requires Bool",n)
                return "Bool"
            if t not in ("Int","Float"):self.error("unary - requires a number",n)
            return t
        if isinstance(n,ast.Binary):
            a,b=self.expr(n.left),self.expr(n.right)
            if n.op in ("and","or"):
                if a!="Bool" or b!="Bool":self.error(f"operator {n.op} requires Bool operands",n)
                return "Bool"
            if n.op in ("==","!="):return "Bool"
            if n.op in ("<","<=",">",">="):
                if a not in ("Int","Float","Text") or b not in ("Int","Float","Text"):self.error("comparison requires compatible values",n)
                return "Bool"
            if n.op=="+" and a==b=="Text":return "Text"
            if "Any" in (a,b): return "Any"
            if a not in ("Int","Float") or b not in ("Int","Float"):self.error(f"operator {n.op} requires numeric operands",n)
            return "Float" if "Float" in (a,b) or n.op=="/" else "Int"
        if isinstance(n,ast.Call):
            if not isinstance(n.callee,ast.Name):self.error("only named functions can be called",n)
            if n.callee.name=="print":
                for a in n.args:self.expr(a)
                return "Void"
            f=self.functions.get(n.callee.name)
            if not f:self.error(f"unknown function '{n.callee.name}'",n)
            if len(n.args)!=len(f.params):self.error(f"function '{f.name}' expects {len(f.params)} arguments, got {len(n.args)}",n)
            for arg,param in zip(n.args,f.params):
                actual=self.expr(arg); expected=param.annotation or "Any"
                if not self.compatible(expected,actual):self.error(f"argument '{param.name}' expects {expected}, found {actual}",arg)
            return f.return_type or "Any"
        self.error(f"cannot infer type of {type(n).__name__}",n)
