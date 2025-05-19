import json
import os
from datetime import datetime

class MailManager:
    def __init__(self):
        self.data_dir = os.path.join(os.path.dirname(__file__), 'data')
        os.makedirs(self.data_dir, exist_ok=True)
        
        self.accounts_file = os.path.join(self.data_dir, 'accounts.json')
        self.emails_file = os.path.join(self.data_dir, 'emails.json')
        
        self.load_data()

    def load_data(self):
        self.accounts = self._load_json(self.accounts_file)
        self.emails = self._load_json(self.emails_file)

    def _load_json(self, filepath):
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def save_account(self, username, account_data):
        self.accounts[username] = account_data
        with open(self.accounts_file, 'w') as f:
            json.dump(self.accounts, f, indent=4)

    def get_emails(self, email):
        return self.emails.get(email, [])

    def send_email(self, from_email, to_email, subject, body):
        if to_email not in self.emails:
            self.emails[to_email] = []
        
        email = {
            'from': from_email,
            'subject': subject,
            'body': body,
            'date': str(datetime.now()),
            'read': False
        }
        
        self.emails[to_email].append(email)
        self._save_json(self.emails_file, self.emails)
        return True

    def _save_json(self, filepath, data):
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=4)
