import pytest
from pyteal import *

import compile_pyteal


def test_compile_success():
    test_cases_good = [
        (
            b"from pyteal import *\n\n\ndef approval():\n    return Approve()\n",
            b"\x05\x81\x01C",
        ),
    ]
    for test in test_cases_good:
        output = compile_pyteal.raw_compile(test[0])
        assert output == test[1]


def test_compile_fail():
    test_cases_bad = [
        (b"asdf\n", NameError),
        (
            b"from pyteal import *\n\n\ndef reject():\n    return Approve()\n",
            AttributeError,
        ),
    ]
    for test in test_cases_bad:
        with pytest.raises(test[1]) as e:
            output = compile_pyteal.raw_compile(test[0])
