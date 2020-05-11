from models.create_db import is_base_exists
from import_data import create_users_posts, show_existing_tags, add_tags_to_posts, show_join, show_methods, \
    show_posts_and_tags, show_posts_without_tags, show_all_posts_of_user


if __name__ == '__main__':
    is_base_exists()
    create_users_posts()
    show_existing_tags()
    add_tags_to_posts()
    show_join()
    show_methods()
    show_posts_and_tags()
    show_posts_without_tags()
    show_all_posts_of_user()

