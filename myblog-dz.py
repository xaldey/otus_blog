from sqlalchemy import create_engine, Column, Integer, String, Text, Boolean, ForeignKey, Table, or_
from sqlalchemy.orm import relationship, sessionmaker, scoped_session, joinedload
from sqlalchemy.ext.declarative import declarative_base
import os

engine = create_engine('sqlite:///myblog.db')
Base = declarative_base(bind=engine)

session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)

# Переменная для сверки местоположения БД
EXPECTED_DB_PATH = 'myblog.db'
decor = ' #' * 15

posts_tags_table = Table(
    'tags_posts',
    Base.metadata,
    Column('post_id', Integer, ForeignKey('posts.id'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tags.id'), primary_key=True),
)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(30), nullable=False)

    posts = relationship('Post', back_populates='user')

    def __repr__(self):
        return f'<User #{self.id} {self.username}>'


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    # user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    title = Column(String(40), nullable=False)
    text = Column(Text, nullable=False)
    is_published = Column(Boolean, nullable=False, default=False)

    user = relationship(User, back_populates='posts')
    tags = relationship('Tag', secondary=posts_tags_table, back_populates='posts')

    def __repr__(self):
        return f'<Post #{self.id} by {self.user_id} {self.title}>'


class Tag(Base):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True)
    name = Column(String(10), nullable=False)

    posts = relationship('Post', secondary=posts_tags_table, back_populates='tags')

    def __repr__(self):
        return f'<Tag #{self.id} {self.name}>'


# Делаем проверку наличия БД в текущей папке
def is_base_exists():
    print("Проверим наличие БД")
    if os.path.isfile(EXPECTED_DB_PATH) and os.path.exists(EXPECTED_DB_PATH):
        print("База данных в наличии.")
    else:
        base_create()


# Создаем базу и наполняем стандартным набором тегов
def base_create():
    Base.metadata.create_all()
    create_users_posts()
    print("Базы данных не было. Теперь она создана.")


def create_users_posts():
    session = Session()

    user = User(username='otus')
    session.add(user)
    session.flush(session)

    print("Создаем посты от имени пользователя: ", user)
    print('------создаем посты-----')
    post1 = Post(user_id=user.id, title='Обзор фильма "Во все тяжкие"',
                 text='Здесь находится большой текст-описание обзора фильма "Во все тяжкие"')
    post2 = Post(user_id=user.id, title='Обзор фильма "Гладиатор"',
                 text='Здесь находится большой текст-описание обзора фильма "Гладиатор"')
    post3 = Post(user_id=user.id, title='Обзор фильма "Терминатор"',
                 text='Здесь находится большой текст-описание обзора фильма "Терминатор"')
    post4 = Post(user_id=user.id, title='Обзор фильма "Мишки Гамми"',
                 text='Здесь находится большой текст-описание обзора фильма "Мишки Гамми"')
    post5 = Post(user_id=user.id, title='Обзор фильма "Кремниевая долина"',
                 text='Здесь находится большой текст-описание обзора фильма "Кремниевая долина"')
    session.add(post1)
    session.add(post2)
    session.add(post3)
    session.add(post4)
    session.add(post5)

    session.commit()
    session.close()
    create_start_tags()


def create_start_tags():
    session = Session()
    standard_tags = ('комедия', 'боевик', 'ужасы', 'мультфильм', 'документалка')
    for tag in standard_tags:
        tag = Tag(name=tag)
        session.add(tag)
        print("Тег", tag.name, "внесен в список тегов")
    print("-----------------Список тегов обновлен----------------")
    session.commit()
    session.close()


def show_existing_tags():
    print(decor)
    print("Все имеющиеся теги")
    session = Session()
    q_tags = session.query(Tag)
    tag = q_tags.first()
    print("(Первый тег) tag = q_tags.first()", tag)
    print("Теги к постам", tag.posts)
    tags1 = q_tags.all()
    tags2 = list(q_tags)
    print("Все теги методом .all()",tags1)


    # q_f_by_id = q_tags.filter(
    #     Tag.id > 2,
    # )
    # print(q_f_by_id)
    # print(q_f_by_id.all())
    #
    # a_and_by_contains = q_f_by_id.filter(
    #     Tag.name.contains('g'),
    # )
    # print(a_and_by_contains)
    # print(a_and_by_contains.all())
    #
    # q = q_tags.filter(
    #     or_(
    #         Tag.id > 2,
    #         Tag.name.contains('o'),
    #     )
    # )
    #
    # print(q)
    # print(q.all())

    session.close()


def add_tags_to_posts():
    """
    :return:
    """
    print(decor)
    print("Добавляем теги к постам:")
    session = Session()

    tag = session.query(Tag).first()
    post: Post = session.query(Post).first()
    post.tags.append(tag)

    # tag_war = session.query(Tag.name).filter(
    #     Tag.name.contains("боевик")
    # )
    # post_first: Post = session.query(Post).first()
    # post_first.tags.append(tag_war)
    session.commit()
    print("Пост -", post, "с тегом -", post.tags)
    print("Тег -", tag,"к посту -", tag.posts)
    session.close()


def show_join():
    """
    :return:
    """
    print(decor)
    print("Разбираем join")
    session = Session()

    query_user_join = session.query(
        User,
    ).join(
        Post,
        User.id == Post.user_id,
    ).filter(
        Post.title.contains('Гамми')
        # Post.tags.any(Tag.id == 1)
    )
    # print("Post.title.contains('тяжкие')", query_join)
    print("Post.title.contains('Гамми')", query_user_join.all())


def show_methods():
    print("Разбираем методы")

    session = Session()

    query_first_tag = session.query(Tag).filter(Tag.id == 1)
    # print("Первый тег:", query_first_tag)
    # print("Тип:", type(query_first_tag))
    print("Список первого тега через list", list(query_first_tag))
    print("Список первого тега через .all",query_first_tag.all())

    # query_tag = q_tags.filter(
        #     or_(
        #         Tag.id > 2,
        #         Tag.name.contains('o'),
        #     )
        # )
    query_tag = session.query(Tag.name).filter(
        Tag.name.contains("боевик")
    )
    # print("Tag.name.contains(тяжкие) - ", query_tag)

    print("Tag.name.contains(боевик) .all ", query_tag.all())
    # print(type(query_tag))
    # print(list(q))
    # res = q.all()
    # print([r for r, in res])

    q_user = session.query(User.username).filter(User.id == 1)
    user = q_user.one()
    print("User.id == 1 ->", user)

    # Берем первого пользователя из запроса
    res_username = q_user.scalar()
    print('username:', res_username)


def main():
    is_base_exists()
    show_existing_tags()
    add_tags_to_posts()
    show_join()
    show_methods()


if __name__ == '__main__':
    main()
