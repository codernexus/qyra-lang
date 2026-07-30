from .token import Token, Kind
from .errors import Span, LexError

KEYWORDS = {
    "let":Kind.LET,"var":Kind.VAR,"func":Kind.FUNC,"return":Kind.RETURN,"if":Kind.IF,"else":Kind.ELSE,"while":Kind.WHILE,
    "true":Kind.TRUE,"false":Kind.FALSE,"null":Kind.NULL,"print":Kind.PRINT,"and":Kind.AND,"or":Kind.OR,
}

class Lexer:
    def __init__(self, source:str): self.s=source; self.i=0; self.line=1; self.col=1
    def peek(self,n=0):
        j=self.i+n
        return self.s[j] if j<len(self.s) else "\0"
    def advance(self):
        c=self.peek(); self.i+=1
        if c=="\n": self.line+=1; self.col=1
        else: self.col+=1
        return c
    def token(self,k,text,value,line,col): return Token(k,text,value,Span(line,col,max(len(text),1)))
    def scan(self):
        out=[]
        while self.i<len(self.s):
            c=self.peek()
            if c in " \r\t\n": self.advance(); continue
            if c=="/" and self.peek(1)=="/":
                while self.peek() not in ("\n","\0"): self.advance()
                continue
            line,col=self.line,self.col
            if c.isalpha() or c=="_":
                start=self.i
                while self.peek().isalnum() or self.peek()=="_": self.advance()
                text=self.s[start:self.i]; out.append(self.token(KEYWORDS.get(text,Kind.IDENT),text,text,line,col)); continue
            if c.isdigit():
                start=self.i
                while self.peek().isdigit(): self.advance()
                if self.peek()=="." and self.peek(1).isdigit():
                    self.advance()
                    while self.peek().isdigit(): self.advance()
                text=self.s[start:self.i]; val=float(text) if "." in text else int(text); out.append(self.token(Kind.NUMBER,text,val,line,col)); continue
            if c=='"':
                self.advance(); chars=[]
                while self.peek() not in ('"','\0'):
                    if self.peek()=="\\":
                        self.advance(); esc=self.advance(); chars.append({"n":"\n","t":"\t","r":"\r",'"':'"',"\\":"\\"}.get(esc,esc))
                    else: chars.append(self.advance())
                if self.peek()=="\0": raise LexError("unterminated string",Span(line,col),"close the string with a double quote")
                self.advance(); text=self.s[self.i-len(chars)-2:self.i]; out.append(self.token(Kind.STRING,text,"".join(chars),line,col)); continue
            two=c+self.peek(1)
            pairs={"==":Kind.EQEQ,"!=":Kind.NE,"<=":Kind.LE,">=":Kind.GE,"->":Kind.ARROW}
            if two in pairs: self.advance(); self.advance(); out.append(self.token(pairs[two],two,two,line,col)); continue
            singles={"(":Kind.LPAREN,")":Kind.RPAREN,"{":Kind.LBRACE,"}":Kind.RBRACE,",":Kind.COMMA,";":Kind.SEMI,":":Kind.COLON,"+":Kind.PLUS,"-":Kind.MINUS,"*":Kind.STAR,"/":Kind.SLASH,"%":Kind.PERCENT,"!":Kind.BANG,"=":Kind.EQ,"<":Kind.LT,">":Kind.GT}
            if c in singles: self.advance(); out.append(self.token(singles[c],c,c,line,col)); continue
            raise LexError(f"unexpected character {c!r}",Span(line,col),"remove it or use a supported token")
        out.append(Token(Kind.EOF,"",None,Span(self.line,self.col,1)))
        return out
