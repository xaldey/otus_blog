from main import User, Post, Tag
import pytest
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
    def is_base_exists(self):
        path_db = 'myblog.db'
        assert path_db == expected_db_path
#
#     def test_db_contains(self, args, expected_result):
#         pass
#
#     def test_is_user_exsists(self, args):
#         pass
#
#     def test_is_posts_exsists(self, args):
#         pass
#
#     def test_is_tags_exsists(self, args):
#         pass


if __name__ == '__main__':
    TestBlog
    is_file_exists()
