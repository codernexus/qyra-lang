# Implementation status

## Working in 0.3 alpha

The source pipeline is `UTF-8 source -> lexer -> parser -> AST -> type checker -> bytecode -> VM`.

Static checking detects unknown names, duplicate declarations, immutable assignment, invalid conditions, argument count/type mismatches, invalid return types and unsupported operator combinations.

## Not yet implemented

Modules, user-defined types, generics, pattern matching, structured errors, collections, filesystem/JSON/HTTP libraries, package management, native code generation, WebAssembly, LSP and debugger.

No unimplemented component is represented by an empty directory.
