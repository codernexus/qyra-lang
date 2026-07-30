import unittest
from qyra.api import compile_source, run_source
from qyra.errors import TypeErrorQyra, ParseError

class TypeTests(unittest.TestCase):
    def test_typed_function(self):
        out=[]; run_source('func add(a: Int, b: Int) -> Int { return a+b } print(add(2,3))', lambda *x:out.append(x))
        self.assertEqual(out,[(5,)])
    def test_annotation(self): compile_source('let x: Int = 3')
    def test_float_widen(self): compile_source('let x: Float = 3')
    def test_bad_annotation(self):
        with self.assertRaises(TypeErrorQyra): compile_source('let x: Int = "no"')
    def test_immutable_assignment(self):
        with self.assertRaises(TypeErrorQyra): compile_source('let x=1 x=2')
    def test_mutable_assignment(self): compile_source('var x=1 x=2')
    def test_unknown_name(self):
        with self.assertRaises(TypeErrorQyra): compile_source('print(missing)')
    def test_bad_condition(self):
        with self.assertRaises(TypeErrorQyra): compile_source('if 1 { print(1) }')
    def test_bad_return(self):
        with self.assertRaises(TypeErrorQyra): compile_source('func x() -> Int { return "x" }')
    def test_bad_arg(self):
        with self.assertRaises(TypeErrorQyra): compile_source('func x(a: Int)->Int{return a} print(x("x"))')
    def test_arity(self):
        with self.assertRaises(TypeErrorQyra): compile_source('func x(a: Int)->Int{return a} print(x())')
    def test_unknown_type(self):
        with self.assertRaises(TypeErrorQyra): compile_source('let x: Banana = 1')
    def test_bool_logic(self): compile_source('let x: Bool = true and false')
    def test_text_plus(self): compile_source('let x: Text = "a" + "b"')
    def test_numeric_mismatch(self):
        with self.assertRaises(TypeErrorQyra): compile_source('let x = 1 + "b"')

if __name__=='__main__': unittest.main()
