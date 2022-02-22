import pyperclip

from pw.pw_cli import PasswordCommand
from pw.pw_config import get_test_config


def test_get_password():
    _test_clipboard("guitar", "pink_floyd")


def test_get_password_from_section():
    _test_clipboard("kafka --section test", "stream_processing")


def test_get_key():
    _test_clipboard("guitar -k brand", "fender")


def test_find():
    _test_clipboard("-f kaf", "stream_processing")


def _test_clipboard(args: str, expected_value: str):
    PasswordCommand.main(args.split(), get_test_config())
    actual_value = pyperclip.paste()
    assert actual_value == expected_value
