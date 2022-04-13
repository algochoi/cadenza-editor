import importlib
import os

from pyteal import *

import sandbox_utils

# Temporary file suffix
count = 0
MAX_FILE_COUNT = 1000  # Store 1000 files at most in server


def application(pyteal: Expr) -> str:
    return compileTeal(pyteal, mode=Mode.Application, version=MAX_TEAL_VERSION)


# Naively sanitize user input code and raise exception if user is doing
# something suspicious.
def sanitize_code(user_code: str):
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
def process_pyteal(raw_pyteal: bytes) -> str:
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


def raw_compile(raw_pyteal: bytes):
    fname = process_pyteal(raw_pyteal)

    # Try compiling pyteal
    teal_code = ""
    try:
        mod_name = f"temp.{fname}"
        temp_pyteal = importlib.import_module(mod_name)
        teal_code = application(temp_pyteal.approval())
    except Exception as e:
        raise e

    # Try compiling TEAL
    try:
        client = sandbox_utils.create_algod_client()
        source_program = sandbox_utils.compile_program(client, teal_code)
    except Exception as e:
        raise e

    return teal_code, source_program
