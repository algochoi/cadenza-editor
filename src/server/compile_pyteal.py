import base64
import importlib
import os
from typing import Tuple, Union

from algosdk.v2client import algod
from pyteal import MAX_TEAL_VERSION, Expr, Mode, Router, compileTeal

import sandbox_utils

# Temporary file suffix
count = 0
MAX_FILE_COUNT = 1000  # Store 1000 files at most in server


# Old way of compiling pyteal through the approval() entry method.
def application(pyteal_code: Expr) -> str:
    return compileTeal(pyteal_code, mode=Mode.Application, version=MAX_TEAL_VERSION)


# Newer way of compiler pyteal through the Router object.
# TODO: Allow users to optionally use router to compile contracts.
def compile_router(router: Router) -> str:
    approval_program, _, _ = router.compile_program(version=MAX_TEAL_VERSION)
    return approval_program


# Naively sanitize user input code and raise exception if user is doing
# something suspicious.
def sanitize_code(user_code: str) -> None:
    bad_commands = [
        " os.",
        " sys.",
        " subprocess.",
        " asyncio.",
        "exec(",
        "eval(",
        " logging.",
        " code.",
        "_xxsubinterpreters.",
        "_testcapi.",
        ".__",
    ]

    for command in bad_commands:
        if command in user_code:
            print(f"User attemped to use: {command}")
            raise Exception("Sorry, we don't support that command!")


# Creates a temp PyTeal file and saves to temp folder.
def process_pyteal(raw_pyteal: Union[str, bytes]) -> str:
    global count
    decoded = raw_pyteal
    if isinstance(raw_pyteal, bytes):
        decoded = raw_pyteal.decode("utf-8")
    fname = f"temp_pyteal_{count%MAX_FILE_COUNT}"
    count += 1

    # Sanitize input, and if bad, raise exception
    sanitize_code(decoded)

    # Create temp directory (mkdir -p)
    try:
        os.mkdir("temp")
    except:
        # Swallow error if temp dir already exists
        pass

    with open(f"temp/{fname}.py", "w") as f:
        f.write(decoded)
    return fname


def compile_raw_pyteal(raw_pyteal: bytes) -> bytes:
    source_code = raw_pyteal.decode("utf-8")
    return compile_pyteal(source_code)[1]


def compile_program(client: algod.AlgodClient, source_code: str) -> bytes:
    compile_response = client.compile(source_code)
    return base64.b64decode(compile_response["result"])


def compile_pyteal(pyteal_code: str) -> Tuple[str, bytes]:
    fname = process_pyteal(pyteal_code)

    # Try compiling pyteal
    teal_code = ""
    try:
        mod_name = f"temp.{fname}"
        temp_pyteal = importlib.import_module(mod_name)
        teal_code = compile_router(temp_pyteal.router)
    except Exception as e:
        raise e

    # Try compiling TEAL
    try:
        client = sandbox_utils.create_algod_client()
        source_program = compile_program(client, teal_code)
    except Exception as e:
        raise e

    return teal_code, source_program
