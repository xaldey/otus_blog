import os

basedir = os.path.abspath(os.path.dirname(__file__))
SECRET_KEY="jhsdajusgduyaygfshfgjadbvnxcbvhgdesftgyg"
DEBUG=True
# Переменная для сверки местоположения БД
EXPECTED_DB_PATH = 'myapp_myblog.db'
DECOR = ' #' * 15
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, EXPECTED_DB_PATH)
SQLALCHEMY_TRACK_MODIFICATIONS = False