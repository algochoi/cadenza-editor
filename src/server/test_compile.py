import pytest

import compile_pyteal


def test_compile_success():
    test_cases_good = [
        (
            """
from pyteal import *
router = Router(
    "Cadenza test",
    BareCallActions(
        no_op=OnCompleteAction(action=Approve(), call_config=CallConfig.ALL),
        # clear_state=OnCompleteAction.call_only(Approve()),
    ),
)
            """,
            b'\x07 \x01\x001\x1b"\x12@\x00\x01\x001\x19"\x12@\x00\x01\x00\x81\x01C',
        ),
    ]
    for test in test_cases_good:
        _, output, _ = compile_pyteal.compile_pyteal(test[0])
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
        with pytest.raises(test[1]):
            _, _, _ = compile_pyteal.compile_pyteal(test[0])
