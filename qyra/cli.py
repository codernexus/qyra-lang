import argparse, json, sys
from pathlib import Path
from .api import compile_source, run_source
from .errors import QyraError
from .bytecode import Op
from . import __version__

def main(argv=None):
    p=argparse.ArgumentParser(prog="qyra"); p.add_argument("--version",action="version",version=__version__)
    sub=p.add_subparsers(dest="cmd",required=True)
    for name in ("run","check","bytecode"):
        q=sub.add_parser(name); q.add_argument("file")
    a=p.parse_args(argv); path=Path(a.file); src=path.read_text(encoding="utf-8")
    try:
        if a.cmd=="run": run_source(src)
        else:
            main_code, funcs=compile_source(src)
            if a.cmd=="check": print(f"OK: {path} ({len(main_code.code)} instructions, {len(funcs)} functions)")
            else:
                for i,ins in enumerate(main_code.code): print(f"{i:04} {ins.op.name:<14} {ins.arg!r}")
    except QyraError as e:
        print(e.render(src,str(path)),file=sys.stderr); return 1
    return 0
if __name__=="__main__": raise SystemExit(main())
