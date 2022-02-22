from pw.pw_cli import PasswordCommand
from pw.pw_config import get_test_config


c1 = "-s main"
c2 = "-n pytest -pw refactoring"
c3 = "-n guitar -kwargs 'brand=fender,model=stratocaster,string_gauge=0.10,amp=princeton_reverb'"
c4 = "-f guit -e"
c5 = "-n kafka -pw stream_processing -s test"


def test_get_password():
    args = "guitar"
    pw = PasswordCommand.main(args, get_test_config())
    assert isinstance(pw, str)


def test_get_password_from_section():
    args = "kafka --section test".split()
    pw = PasswordCommand.main(args, get_test_config())
    assert isinstance(pw, str)


def test_get_key():
    args = "pw guitar --key brand"
    pw = PasswordCommand.main(args, get_test_config())
    assert isinstance(pw, str)


def test_find():
    args = "pw -f kafka"
    pw = PasswordCommand.main(args, get_test_config())
    assert isinstance(pw, str)


if __name__ == "__main__":
    main()
