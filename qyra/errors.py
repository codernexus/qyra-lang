from dataclasses import dataclass

@dataclass
class Span:
    line: int
    column: int
    length: int = 1

class QyraError(Exception):
    code = "QY0000"
    def __init__(self, message: str, span: Span | None = None, hint: str | None = None):
        super().__init__(message)
        self.message, self.span, self.hint = message, span, hint

    def render(self, source: str, filename: str = "<input>") -> str:
        head = f"error[{self.code}]: {self.message}"
        if not self.span:
            return head
        lines = source.splitlines() or [""]
        line = lines[self.span.line - 1] if 0 < self.span.line <= len(lines) else ""
        pointer = " " * max(self.span.column - 1, 0) + "^" * max(self.span.length, 1)
        out = [head, "", f"  --> {filename}:{self.span.line}:{self.span.column}", "   |", f"{self.span.line:>3} | {line}", f"   | {pointer}"]
        if self.hint:
            out += ["   |", f"help: {self.hint}"]
        return "\n".join(out)

class LexError(QyraError): code = "QY1001"
class ParseError(QyraError): code = "QY2001"
class TypeErrorQyra(QyraError): code = "QY3001"
class CompileError(QyraError): code = "QY3101"
class RuntimeErrorQyra(QyraError): code = "QY4001"
