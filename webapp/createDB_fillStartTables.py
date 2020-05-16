from webapp.models.create_db import base_create
from webapp.models.import_data import create_users_posts, show_existing_tags, add_tags_to_posts, show_join, show_methods, \
    show_posts_and_tags, show_posts_without_tags, show_all_posts_of_user
from webapp.config import EXPECTED_DB_PATH
import os


# Делаем проверку наличия БД в нужном месте
def is_base_exists():
    print("Проверим наличие БД")
    if os.path.isfile(EXPECTED_DB_PATH) and os.path.exists(EXPECTED_DB_PATH):
        print("База данных в наличии.")
    else:
        base_create()
        create_users_posts()
        show_existing_tags()
        add_tags_to_posts()
        show_join()
        show_methods()
        show_posts_and_tags()
        show_posts_without_tags()
        show_all_posts_of_user()


if __name__ == '__main__':
    is_base_exists()


