from sqlalchemy import create_engine, Column, Integer, ForeignKey, Table
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from webapp.config import SQLALCHEMY_DATABASE_URI


engine = create_engine(SQLALCHEMY_DATABASE_URI)
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)


class Base:
    @declared_attr
    def __tablename__(self):
        return f"myapp_{self.__name__.lower()}"

    id = Column(Integer, primary_key=True)


Base = declarative_base(bind=engine, cls=Base)


# Создаем базу и наполняем стандартным набором тегов
def base_create():
    Base.metadata.create_all(engine)
    print("Базы данных не было. Теперь она создана.")


posts_tags_table = Table(
        'tags_posts',
        Base.metadata,
        Column('post_id', Integer, ForeignKey('posts.id'), primary_key=True),
        Column('tag_id', Integer, ForeignKey('tags.id'), primary_key=True),
    )


def main():
    base_create()


if __name__ == '__main__':
    main()
