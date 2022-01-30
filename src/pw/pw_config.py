from dataclasses import dataclass
import os
from configparser import ConfigParser


@dataclass
class PWConfig:
    creds_dir: str
    creds_file_name: str
    encryption_key: str


def get_test_config():
    return PWConfig(
        creds_dir="tests/resources",
        creds_file_name="test_data.json",
        encryption_key=b"-HOFu-mIaxeVAdRMANMlTxvLF0Ihm5ncW3zOOZprX-U=",
    )


def get_prod_config():
    raise NotImplementedError()
