import os
import json
import datetime


class SecretsDataJSONClient:
    def __init__(self, creds_dir_path: str, creds_file_name: str):
        self.creds_dir_path = creds_dir_path
        self.creds_file_name = creds_file_name
        self.creds_file_path = os.path.join(creds_dir_path, creds_file_name)
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
        backup_path = os.path.join(self.creds_dir_path, ".backups", pretty_now)
        with open(f'{backup_path}', 'w') as pw_file_json:
            json.dump(self.pw_dict, pw_file_json)

    def save_dict_to_file(self):
        with open(self.creds_file_path, 'w') as pw_file_json:
            json.dump(self.pw_dict, pw_file_json)
