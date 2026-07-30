import unittest
from qyra.api import run_source, compile_source
from qyra.errors import LexError, ParseError, RuntimeErrorQyra, TypeErrorQyra

class QyraTests(unittest.TestCase):
    def execute(self,src):
        out=[]; run_source(src,lambda *x: out.append(" ".join(map(str,x)))); return out
    def test_arithmetic(self): self.assertEqual(self.execute('print(2 + 3 * 4)'),['14'])
    def test_variables(self): self.assertEqual(self.execute('var x = 1; x = x + 4; print(x)'),['5'])
    def test_immutable(self):
        with self.assertRaises(TypeErrorQyra): run_source('let x=1; x=2')
    def test_function(self): self.assertEqual(self.execute('func add(a,b){return a+b} print(add(4,5))'),['9'])
    def test_if(self): self.assertEqual(self.execute('if 3 > 2 { print("yes") } else { print("no") }'),['yes'])
    def test_while(self): self.assertEqual(self.execute('var i=0; while i<3 { print(i); i=i+1 }'),['0','1','2'])
    def test_strings(self): self.assertEqual(self.execute('print("a" + "b")'),['ab'])
    def test_booleans(self): self.assertEqual(self.execute('print(true == false)'),['False'])
    def test_compile(self):
        main,funcs=compile_source('func f(){return 1} print(f())'); self.assertIn('f',funcs); self.assertGreater(len(main.code),1)
    def test_lex_error(self):
        with self.assertRaises(LexError): compile_source('@')
    def test_parse_error(self):
        with self.assertRaises(ParseError): compile_source('let = 1')
    def test_arity_error(self):
        with self.assertRaises(TypeErrorQyra): run_source('func f(a){return a} f()')
if __name__=='__main__': unittest.main()
