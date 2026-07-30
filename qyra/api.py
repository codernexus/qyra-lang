from .lexer import Lexer
from .parser import Parser
from .compiler import Compiler
from .typecheck import TypeChecker
from .vm import VM

def compile_source(source:str):
    tokens=Lexer(source).scan(); tree=Parser(tokens).parse(); TypeChecker().check(tree); return Compiler().compile(tree)

def run_source(source:str, output=print):
    main, funcs=compile_source(source); return VM(main,funcs,output).run()
