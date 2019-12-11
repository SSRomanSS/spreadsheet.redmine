import os

REDMINE_URL = 'http://localhost:3000/'
USERNAME = 'admin'
PASSWORD = 'admin'
SCOPE = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
KEY_FILE = os.path.dirname(os.path.abspath(__file__)) + os.sep + 'secret_key.json'
