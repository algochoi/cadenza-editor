import importlib

from flask import Response
from pyteal import *

import sandbox_utils

# Temporary file suffix
count = 0


def application(pyteal: Expr) -> str:
    return compileTeal(pyteal, mode=Mode.Application, version=MAX_TEAL_VERSION)


# Creates a temp PyTeal file and saves to temp folder.
def process_pyteal(raw_pyteal: bytes) -> str:
    global count
    decoded = raw_pyteal.decode("utf-8")
    fname = f"temp_pyteal_{count}"
    count += 1
    with open(f"temp/{fname}.py", "w") as f:
        f.write(decoded)
    return fname


def raw_compile(raw_pyteal: bytes):
    fname = process_pyteal(raw_pyteal)

    # Try compiling pyteal
    teal_code = ""
    try:
        mod_name = f"temp.{fname}"
        temp_pyteal = importlib.import_module(mod_name)
        teal_code = application(temp_pyteal.approval())
    except Exception as e:
        return Response("Bad Approval program; could not compile PyTeal", status=400)

    # Try compiling TEAL
    try:
        client = sandbox_utils.create_algod_client()
        source_program = sandbox_utils.compile_program(client, teal_code)
    except Exception as e:
        return Response("Bad Approval program; could not compile TEAL", status=400)

    return Response(f"Compilation successful: {source_program}", status=200)
