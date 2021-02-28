import json


def get_pws_from_json_file(file_path):
    """Loads json data into python to retrieve passwords that are stored as key value pairs."""
    with open(file_path) as pws:
        return json.load(pws)


def my_exchandler(type, value, traceback):
    """Set 'sys.excepthook' to myexchandler to avoid traceback.
     Credits: https://stackoverflow.com/questions/38598740/raising-errors-without-traceback
    """
    print(value)
