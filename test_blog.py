from main import User, Post, Tag
import pytest
import os.path
import datetime
import pathlib
import pytest

path = pathlib.Path(input('Введите адрес: '))
print(path.exists())  # True
print(path.is_file())  # True

# class TestBlog:
#     def is_base_exists(self):
#         """Проверка запуска теста"""
#         assert 1 == 1
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

