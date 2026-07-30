# Архитектура Qyra Bootstrap 0.2

1. `lexer.py` преобразует UTF-8 исходник в токены с line/column spans.
2. `parser.py` строит AST recursive descent + precedence climbing.
3. `compiler.py` компилирует AST в стековый bytecode.
4. `vm.py` исполняет bytecode в изолированной Qyra VM.
5. `cli.py` предоставляет run/check/bytecode.

Bootstrap не выполняет Python-код пользователя и не использует `eval`/`exec`.
