from .token import Kind
from .errors import ParseError
from . import ast

PRECEDENCE={Kind.OR:1,Kind.AND:2,Kind.EQEQ:3,Kind.NE:3,Kind.LT:4,Kind.LE:4,Kind.GT:4,Kind.GE:4,Kind.PLUS:5,Kind.MINUS:5,Kind.STAR:6,Kind.SLASH:6,Kind.PERCENT:6}
class Parser:
    def __init__(self,tokens): self.t=tokens; self.i=0
    def cur(self): return self.t[self.i]
    def match(self,*ks):
        if self.cur().kind in ks: x=self.cur(); self.i+=1; return x
        return None
    def need(self,k,msg):
        x=self.match(k)
        if not x: raise ParseError(msg,self.cur().span)
        return x
    def type_name(self):
        return self.need(Kind.IDENT,"expected type name").text
    def parse(self):
        s=[]
        while self.cur().kind!=Kind.EOF: s.append(self.statement())
        return ast.Program(self.cur().span,s)
    def statement(self):
        if self.match(Kind.LET): return self.var_decl(False)
        if self.match(Kind.VAR): return self.var_decl(True)
        if self.match(Kind.FUNC): return self.func_decl()
        if self.match(Kind.IF): return self.if_stmt()
        if self.match(Kind.WHILE): return self.while_stmt()
        if self.match(Kind.RETURN): return self.return_stmt()
        if self.cur().kind==Kind.IDENT and self.t[self.i+1].kind==Kind.EQ:
            name=self.match(Kind.IDENT); self.match(Kind.EQ); v=self.expr(); self.match(Kind.SEMI); return ast.Assign(name.span,name.text,v)
        e=self.expr(); self.match(Kind.SEMI); return ast.ExprStmt(e.span,e)
    def var_decl(self,mutable):
        n=self.need(Kind.IDENT,"expected variable name")
        ann=self.type_name() if self.match(Kind.COLON) else None
        self.need(Kind.EQ,"expected '=' after variable name"); v=self.expr(); self.match(Kind.SEMI)
        return ast.Let(n.span,n.text,mutable,ann,v)
    def func_decl(self):
        n=self.need(Kind.IDENT,"expected function name"); self.need(Kind.LPAREN,"expected '('"); params=[]
        if self.cur().kind!=Kind.RPAREN:
            while True:
                p=self.need(Kind.IDENT,"expected parameter name")
                ann=self.type_name() if self.match(Kind.COLON) else None
                params.append(ast.Param(p.text,ann,p.span))
                if not self.match(Kind.COMMA): break
        self.need(Kind.RPAREN,"expected ')'")
        ret=self.type_name() if self.match(Kind.ARROW) else None
        return ast.Func(n.span,n.text,params,ret,self.block())
    def block(self):
        o=self.need(Kind.LBRACE,"expected '{'"); s=[]
        while self.cur().kind not in (Kind.RBRACE,Kind.EOF): s.append(self.statement())
        self.need(Kind.RBRACE,"expected '}'"); return ast.Block(o.span,s)
    def if_stmt(self):
        c=self.expr(); th=self.block(); other=None
        if self.match(Kind.ELSE): other=self.if_stmt() if self.match(Kind.IF) else self.block()
        if isinstance(other,ast.If): other=ast.Block(other.span,[other])
        return ast.If(c.span,c,th,other)
    def while_stmt(self): return ast.While(self.cur().span,self.expr(),self.block())
    def return_stmt(self):
        span=self.t[self.i-1].span
        if self.cur().kind in (Kind.SEMI,Kind.RBRACE): self.match(Kind.SEMI); return ast.Return(span,None)
        v=self.expr(); self.match(Kind.SEMI); return ast.Return(span,v)
    def expr(self,minp=0):
        left=self.unary()
        while self.cur().kind in PRECEDENCE and PRECEDENCE[self.cur().kind]>=minp:
            op=self.cur(); self.i+=1; right=self.expr(PRECEDENCE[op.kind]+1); left=ast.Binary(op.span,left,op.text,right)
        return left
    def unary(self):
        if self.cur().kind in (Kind.BANG,Kind.MINUS):
            op=self.cur(); self.i+=1; return ast.Unary(op.span,op.text,self.unary())
        return self.call()
    def call(self):
        e=self.primary()
        while self.match(Kind.LPAREN):
            args=[]
            if self.cur().kind!=Kind.RPAREN:
                while True:
                    args.append(self.expr())
                    if not self.match(Kind.COMMA): break
            self.need(Kind.RPAREN,"expected ')' after arguments"); e=ast.Call(e.span,e,args)
        return e
    def primary(self):
        t=self.cur(); self.i+=1
        if t.kind in (Kind.NUMBER,Kind.STRING): return ast.Literal(t.span,t.value)
        if t.kind==Kind.TRUE:return ast.Literal(t.span,True)
        if t.kind==Kind.FALSE:return ast.Literal(t.span,False)
        if t.kind==Kind.NULL:return ast.Literal(t.span,None)
        if t.kind in (Kind.IDENT,Kind.PRINT): return ast.Name(t.span,t.text)
        if t.kind==Kind.LPAREN:
            e=self.expr(); self.need(Kind.RPAREN,"expected ')'"); return e
        raise ParseError("expected expression",t.span)
