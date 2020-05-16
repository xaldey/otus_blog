import sqlite3
import pathlib
import pytest
from webapp.config import EXPECTED_DB_PATH


def is_file_exists():
    path = pathlib.Path(input('Введите имя файла БД: '))
    print('Сравним', path,'и', EXPECTED_DB_PATH)

    if path.is_file() and path.exists():
        print('Файл', path,'в наличии.')
        if str(path) == str(EXPECTED_DB_PATH):
            print('И это правильный и рабочий файл! :)')
        elif str(path) != str(EXPECTED_DB_PATH):
            print('Только вот программа о нем ничего не знает.')
            print('Возможно он не был создан нативным инструментом.')
        else:
            print('Неясно, как ты сюда попал :)')
    else:
        print('Файла с именем', path,'не обнаружено.')


class TestBlog:

    @pytest.mark.parametrize(
        'args, expected_result',
        [
            pytest.param('test_blog.py', 'wrong_file.py'),
            pytest.param('models/myblog.db', 'models/myblog.db')
        ]
    )
    def test_is_file_exists(self, args, expected_result):
        # path_db = 'test_blog.py'
        if str(args) == str(pathlib.Path(args)):
            print('Файл с указанным именем', args, 'в наличии!')
        else:
            print('Указанного файла', args, 'нет на диске!')

    def test_file_correct(self):
        path_db = 'webapp/models/myblog.db'
        if str(path_db) == str(EXPECTED_DB_PATH):
            print('Имя файла', path_db, 'верно!')
        else:
            print('Имя файла', path_db, 'неверно!')

    def test_connect_to_db(self):
        path = 'webapp/models/myblog.db'
        if path == EXPECTED_DB_PATH:
            conn = sqlite3.connect(path)
            cursor = conn.cursor()
            cursor.execute("SELECT title FROM posts WHERE posts.id = 1")
            results = cursor.fetchall()
            print(results)
        else:
            print('Подключение к БД не удалось!')


if __name__ == '__main__':
    TestBlog
