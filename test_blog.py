from main import User, Post, Tag
import sqlite3
import os.path
import datetime
import pathlib
import pytest

expected_db_path = 'myblog.db'
path = ''


def is_file_exists():
    path = pathlib.Path(input('Введите имя файла БД: '))
    print('Сравним', path,'и', expected_db_path)

    if (path.is_file() and path.exists()):
        print('Файл', path,'в наличии.')
        if str(path) == str(expected_db_path):
            print('И это правильный и рабочий файл! :)')
        elif str(path) != str(expected_db_path):
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
            pytest.param('myblog.db', 'myblog.db')
        ]
    )
    def test_is_file_exists(self, args, expected_result):
        # path_db = 'test_blog.py'
        if str(args) == str(pathlib.Path(args)):
            print('Файл с указанным именем', args, 'в наличии!')
        else:
            print('Указанного файла', args, 'нет на диске!')

    def test_file_correct(self):
        path_db = 'myblog.db'
        if str(path_db) == str(expected_db_path):
            print('Имя файла', path_db, 'верно!')
        else:
            print('Имя файла', path_db, 'неверно!')

    def test_connect_to_db(self):
        path = 'myblog.db'
        if path == expected_db_path:
            conn = sqlite3.connect(path)
            cursor = conn.cursor()
            cursor.execute("SELECT title FROM posts WHERE posts.id = 1")
            results = cursor.fetchall()
            print(results)
        else:
            print('Подключение к БД не удалось!')


#     def test_is_posts_exists(self, args):
#         pass
#
#     def test_is_tags_exists(self, args):
#         pass


if __name__ == '__main__':
    TestBlog
