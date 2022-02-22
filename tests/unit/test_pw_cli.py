import pyperclip

from pw.pw_cli import PasswordCommand
from pw.pw_config import get_test_config


c1 = "-s main"
c2 = "-n pytest -pw refactoring"
c3 = "-n guitar -kwargs brand=fender,model=stratocaster,string_gauge=0.10,amp=princeton_reverb"
c4 = "-f guit -e"
c5 = "-n kafka -pw stream_processing -s test"


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


if __name__ == "__main__":
    main()
