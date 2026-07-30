<p align="center">
  <img src="assets/qyra-brand-concept.png" alt="Qyra preliminary logo" width="480">
</p>

# Qyra 0.3.0-alpha.1

Qyra is an experimental statically checked programming language project founded by **Трифон Ярослав Васильович (Nexu_scoder)**.

This public alpha contains a working lexer, parser, AST, primitive type checker, bytecode compiler and stack virtual machine. It is suitable for experimentation, education and compiler development. It is **not production-ready**.

## Implemented

- source lexer with line and column positions;
- recursive-descent parser with expression precedence;
- abstract syntax tree;
- primitive static types: `Int`, `Float`, `Bool`, `Text`, `Void`, `Any`;
- local type inference;
- typed parameters and return values;
- immutable `let` and mutable `var`;
- functions, `return`, `if`, `else`, `while`;
- arithmetic, comparisons and boolean operations;
- Qyra bytecode compiler;
- stack virtual machine;
- CLI commands: `run`, `check`, `bytecode`;
- stable diagnostic codes for implemented checks;
- 27 automated tests;
- CI configuration for Windows, Linux and macOS.

## Example

```qyra
func add(a: Int, b: Int) -> Int {
    return a + b
}

let project: Text = "Qyra"
let answer: Int = add(20, 22)
print(project, answer)
```

## Install and run

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e .
qyra check examples/typed.qy
qyra run examples/typed.qy
qyra bytecode examples/typed.qy
```

Run tests:

```bash
python -m unittest discover -s tests -v
```

## Project status

The current bootstrap requires Python 3.10+. Native compilation, modules, collections, structures, enums, traits, generics, `Option`, `Result`, async/await, package management, production database drivers and sandboxing are not implemented.

See [STATUS.md](docs/STATUS.md), [ARCHITECTURE.md](docs/ARCHITECTURE.md), [ROADMAP.md](docs/ROADMAP.md), [INSTALL.md](INSTALL.md) and [PUBLISHING.md](PUBLISHING.md).

## Leadership

Founder and Lead Language Designer: **Трифон Ярослав Васильович**  
Developer alias: **Nexu_scoder**

## License

Apache License 2.0. The preliminary name and logo must be reviewed before trademark use.
