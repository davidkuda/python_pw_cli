import json
import datetime


class SecretsDataJSONClient:
    def __init__(self, creds_dir: str, creds_file_path: str):
        self.creds_dir = creds_dir
        self.creds_file_path = creds_file_path
        self.pw_dict = self.get_pws_from_json_file()
        self.create_backup()

    def get_pws_from_json_file(self):
        """Loads json data into python to retrieve passwords that are stored as key value pairs."""
        with open(self.creds_file_path) as pws:
            return json.load(pws)

    def create_backup(self):
        """Create a backup of the dictionary with the passwords."""
        now = datetime.datetime.now().isoformat()
        pretty_now = now.split('.')[0].replace(':', '.')
        with open(f'{self.creds_dir}/.backups/{pretty_now}', 'w') as pw_file_json:
            json.dump(self.pw_dict, pw_file_json)

    def save_dict_to_file(self):
        with open(self.creds_file_path, 'w') as pw_file_json:
            json.dump(self.pw_dict, pw_file_json)
