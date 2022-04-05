from pyteal import *

import compile_pyteal

test_cases_good = [
    b"from pyteal import *\n\n\ndef approval():\n    return Approve()\n",
]
for test in test_cases_good:
    output = compile_pyteal.raw_compile(test)
    assert output.status == "200 OK"

test_cases_bad = [
    b"asdf\n",
    b"from pyteal import *\n\n\ndef reject():\n    return Approve()\n",
]
for test in test_cases_bad:
    output = compile_pyteal.raw_compile(test)
    assert output.status == "400 BAD REQUEST"
