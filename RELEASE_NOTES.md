# Qyra 0.3.0-alpha

This alpha adds a static checking pass before bytecode generation.

Implemented and tested:
- explicit type annotations for variables;
- typed function parameters and return values;
- local type inference;
- checks for unknown names and types;
- immutable assignment diagnostics;
- argument count and argument type checks;
- return type checks;
- Boolean condition checks;
- numeric and text operator checks;
- bytecode generation and execution after successful checking.

This release still uses the Python bootstrap implementation and is not production-ready.
