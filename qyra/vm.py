from dataclasses import dataclass
from .bytecode import Op
from .errors import RuntimeErrorQyra
@dataclass
class Binding: value:object; mutable:bool
class VM:
    def __init__(self,main,functions,output=print): self.main=main; self.functions=functions; self.output=output; self.globals={}
    def run(self): return self.exec(self.main,{})
    def exec(self,fn,locals_):
        stack=[]; ip=0
        while ip<len(fn.code):
            ins=fn.code[ip]; ip+=1; op=ins.op
            if op==Op.CONST: stack.append(fn.constants[ins.arg])
            elif op==Op.LOAD:
                if ins.arg in locals_: stack.append(locals_[ins.arg].value)
                elif ins.arg in self.globals: stack.append(self.globals[ins.arg].value)
                else: raise RuntimeErrorQyra(f"unknown name '{ins.arg}'")
            elif op==Op.DEFINE:
                name,mut=ins.arg; target=self.globals if fn.name=="<main>" else locals_; target[name]=Binding(stack.pop(),mut)
            elif op==Op.STORE:
                b=locals_.get(ins.arg) or self.globals.get(ins.arg)
                if not b: raise RuntimeErrorQyra(f"unknown variable '{ins.arg}'")
                if not b.mutable: raise RuntimeErrorQyra(f"cannot assign to immutable variable '{ins.arg}'")
                b.value=stack.pop()
            elif op==Op.POP:
                if stack: stack.pop()
            elif op==Op.PRINT:
                n=ins.arg
                vals=stack[-n:] if n else []
                if n:
                    del stack[-n:]
                self.output(*vals)
            elif op==Op.NEG: stack.append(-stack.pop())
            elif op==Op.NOT: stack.append(not stack.pop())
            elif op in (Op.ADD,Op.SUB,Op.MUL,Op.DIV,Op.MOD,Op.EQ,Op.NE,Op.LT,Op.LE,Op.GT,Op.GE):
                b=stack.pop(); a=stack.pop(); f={Op.ADD:lambda:a+b,Op.SUB:lambda:a-b,Op.MUL:lambda:a*b,Op.DIV:lambda:a/b,Op.MOD:lambda:a%b,Op.EQ:lambda:a==b,Op.NE:lambda:a!=b,Op.LT:lambda:a<b,Op.LE:lambda:a<=b,Op.GT:lambda:a>b,Op.GE:lambda:a>=b}[op]; stack.append(f())
            elif op==Op.JUMP: ip=ins.arg
            elif op==Op.JUMP_IF_FALSE:
                if not stack.pop(): ip=ins.arg
            elif op==Op.CALL:
                name,n=ins.arg
                if name not in self.functions: raise RuntimeErrorQyra(f"unknown function '{name}'")
                f=self.functions[name]
                args=stack[-n:] if n else []
                if n:
                    del stack[-n:]
                if len(args)!=len(f.params): raise RuntimeErrorQyra(f"function '{name}' expects {len(f.params)} arguments, got {len(args)}")
                frame={p:Binding(v,True) for p,v in zip(f.params,args)}; stack.append(self.exec(f,frame))
            elif op==Op.RETURN: return stack.pop() if stack else None
            elif op==Op.HALT: return stack[-1] if stack else None
        return None
