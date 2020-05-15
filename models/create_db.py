from sqlalchemy import create_engine, Column, Integer, ForeignKey, Table
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base, declared_attr
import os


engine = create_engine('sqlite:///models/myapp_myblog.db')

session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)

# Переменная для сверки местоположения БД
EXPECTED_DB_PATH = 'models/myapp_myblog.db'
decor = ' #' * 15


class Base:
    @declared_attr
    def __tablename__(self):
        return f"myapp_{self.__name__.lower()}"

    id = Column(Integer, primary_key=True)


Base = declarative_base(bind=engine, cls=Base)


posts_tags_table = Table(
    'tags_posts',
    Base.metadata,
    Column('post_id', Integer, ForeignKey('posts.id'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tags.id'), primary_key=True),
)


# Делаем проверку наличия БД в текущей папке
def is_base_exists():
    print("Проверим наличие БД")
    if os.path.isfile(EXPECTED_DB_PATH) and os.path.exists(EXPECTED_DB_PATH):
        print("База данных в наличии.")
    else:
        base_create()


# Создаем базу и наполняем стандартным набором тегов
def base_create():
    Base.metadata.create_all(engine)
    print("Базы данных не было. Теперь она создана.")


def main():
    is_base_exists()


if __name__ == '__main__':
    main()
