from . import ast
from .bytecode import Op,Ins,FunctionCode
from .errors import CompileError
class Compiler:
    def __init__(self): self.code=[]; self.const=[]; self.functions={}
    def emit(self,op,arg=None): self.code.append(Ins(op,arg)); return len(self.code)-1
    def patch(self,i,arg): self.code[i].arg=arg
    def c(self,v): self.const.append(v); return len(self.const)-1
    def compile(self,p):
        for s in p.statements: self.stmt(s)
        self.emit(Op.HALT); return FunctionCode("<main>",[],self.code,self.const),self.functions
    def stmt(self,n):
        if isinstance(n,ast.Let): self.expr(n.value); self.emit(Op.DEFINE,(n.name,n.mutable))
        elif isinstance(n,ast.Assign): self.expr(n.value); self.emit(Op.STORE,n.name)
        elif isinstance(n,ast.ExprStmt): self.expr(n.expr); self.emit(Op.POP)
        elif isinstance(n,ast.Block):
            for s in n.statements:self.stmt(s)
        elif isinstance(n,ast.If):
            self.expr(n.cond); jf=self.emit(Op.JUMP_IF_FALSE,None); self.stmt(n.then); j=self.emit(Op.JUMP,None); self.patch(jf,len(self.code));
            if n.otherwise:self.stmt(n.otherwise)
            self.patch(j,len(self.code))
        elif isinstance(n,ast.While):
            start=len(self.code); self.expr(n.cond); jf=self.emit(Op.JUMP_IF_FALSE,None); self.stmt(n.body); self.emit(Op.JUMP,start); self.patch(jf,len(self.code))
        elif isinstance(n,ast.Func):
            sub=Compiler();
            for s in n.body.statements: sub.stmt(s)
            sub.emit(Op.CONST,sub.c(None)); sub.emit(Op.RETURN)
            self.functions[n.name]=FunctionCode(n.name,[p.name for p in n.params],sub.code,sub.const)
        elif isinstance(n,ast.Return):
            if n.value:self.expr(n.value)
            else:self.emit(Op.CONST,self.c(None))
            self.emit(Op.RETURN)
        else: raise CompileError(f"unsupported statement {type(n).__name__}",n.span)
    def expr(self,n):
        if isinstance(n,ast.Literal): self.emit(Op.CONST,self.c(n.value))
        elif isinstance(n,ast.Name): self.emit(Op.LOAD,n.name)
        elif isinstance(n,ast.Unary): self.expr(n.expr); self.emit(Op.NEG if n.op=="-" else Op.NOT)
        elif isinstance(n,ast.Binary):
            self.expr(n.left); self.expr(n.right); mp={"+":Op.ADD,"-":Op.SUB,"*":Op.MUL,"/":Op.DIV,"%":Op.MOD,"==":Op.EQ,"!=":Op.NE,"<":Op.LT,"<=":Op.LE,">":Op.GT,">=":Op.GE,"and":Op.MUL,"or":Op.ADD}; self.emit(mp[n.op])
        elif isinstance(n,ast.Call):
            for a in n.args:self.expr(a)
            if isinstance(n.callee,ast.Name) and n.callee.name=="print": self.emit(Op.PRINT,len(n.args)); self.emit(Op.CONST,self.c(None))
            elif isinstance(n.callee,ast.Name): self.emit(Op.CALL,(n.callee.name,len(n.args)))
            else: raise CompileError("only named functions can be called",n.span)
        else: raise CompileError(f"unsupported expression {type(n).__name__}",n.span)
