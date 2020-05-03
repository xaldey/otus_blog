from sqlalchemy import create_engine, Column, Integer, String, Text, Boolean, ForeignKey, Table, or_
from sqlalchemy.orm import relationship, sessionmaker, scoped_session, joinedload
from sqlalchemy.ext.declarative import declarative_base
import os


engine = create_engine('sqlite:///myblog.db')
Base = declarative_base(bind=engine)

session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)

# Переменная для сверки местоположения БД
expected_db_path = 'myblog.db'

# Make outer table for link within posts and tags
# both posts and tags are primary keys
posts_tags_table = Table(
    'tags_posts',
    Base.metadata,
    Column('post_id', Integer, ForeignKey('posts.id'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tags.id'), primary_key=True),
)


# make class for POSTS
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(30), nullable=False, unique=True)
    # make link from Post to User
    posts = relationship('Post', back_populates='user')

    def __repr__(self):
        return f'<User #{self.id} {self.username}>'


# make class for Post
class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    # user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    title = Column(String(40), nullable=False)
    text = Column(Text, nullable=False)
    is_published = Column(Boolean, nullable=False, default=False)
    # make link from Post to User and to Tags
    user = relationship(User, back_populates='posts')
    tags = relationship('Tag', secondary=posts_tags_table, back_populates='posts')

    def __repr__(self):
        return f'<Post #{self.id} by {self.user_id} {self.title}>'


# make class for Tags
class Tag(Base):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)
    # make link from Tag to Post
    posts = relationship('Post', secondary=posts_tags_table, back_populates='tags')

    def __repr__(self):
        return f'<Tag #{self.id} {self.name}>'


# Делаем проверку наличия БД в текущей папке
def is_base_exists():
    print("Проверим наличие БД")
    if os.path.isfile(expected_db_path) and os.path.exists(expected_db_path):
        print("База данных в наличии.")
    else:
        base_create()
        print("Базы данных не было. Теперь она создана.")


# Создаем базу и наполняем стандартным набором тегов
def base_create():
    Base.metadata.create_all()
    create_tables_and_tags()


# Создадим стартовый набор таблиц в БД
def create_tables_and_tags():
    print("-------------\nСоздание стартового набора таблиц БД")
    session = Session()
    standard_user: User = User(username='start_user')
    session.add(standard_user)
    session.flush(session)
    standard_tags = ('комедия', 'боевик', 'ужасы', 'мультфильм', 'документалка')
    for tag in standard_tags:
        tag = Tag(name=tag)
        session.add(tag)
        print("Тег", tag.name, "внесен в список тегов")
    print("-----------------Список тегов обновлен----------------")
    session.commit()
    session.close()
    print("Стандартный пользователь 'start_user' внесен в БД")


# Функция для проверки авторизации пользователя
def login_user():
    session = Session()
    print("Вытащим список всех существующих пользователей из БД перед логином.")
    query_users = session.query(User)
    print(query_users)
    existed_users = set(query_users)
    print("Список пользователей в БД перед логином:", existed_users)
    user_to_login = input("Укажите имя пользователя для вносимых постов:")
    if user_to_login in existed_users:
        print("Пользователь", user_to_login, "уже присутствует в БД.")
        print("(Из функции логина) Создаем посты пользователя", user_to_login)
        create_users_posts(user_to_login)
    else:
        print("Пользователя с именем", user_to_login, "в БД не существует.")
        print("Необходимо создать пользователя.")
        create_new_user(user_to_login)
    session.commit()
    session.close()


# Делаем функцию проверки наличия и добавления пользователя
def create_new_user(user_to_login):
    # Вытащим список всех существующих пользователей из БД
    session = Session()
    query_users = session.query(User)
    existed_users = set(query_users)
    print("Список пользователей в БД перед созданием нового пользователя:", existed_users)
    new_username = input("Введите имя пользователя: ")
    if new_username in existed_users:
        print("Пользователь с именем", new_username, "уже существует в БД. Выберите другое имя.")
        login_user(new_username)
    else:
        username = User(username=new_username)
        # adding user
        session.add(username)
        # flush session to get id of newly created user
        session.flush(session)
    print("Пользователь", new_username, "добавлен в БД.")
    session.commit()
    session.close()
    create_users_posts(new_username)


def create_users_posts(new_username):
    """
    make func to create users and posts
    :param new_username:
    :return:
    """
    session = Session()
    user = session.query(User).filter_by(username=new_username).first()
    print("Создаем посты от имени пользователя: ", user)
    print('------создаем посты-----')
    post1 = Post(user_id=user.id, title='Обзор фильма "Во все тяжкие"', text='Здесь находится большой текст-описание обзора фильма "Во все тяжкие"')
    post2 = Post(user_id=user.id, title='Обзор фильма "Гладиатор"', text='Здесь находится большой текст-описание обзора фильма "Гладиатор"')
    post3 = Post(user_id=user.id, title='Обзор фильма "Терминатор"', text='Здесь находится большой текст-описание обзора фильма "Терминатор"')
    post4 = Post(user_id=user.id, title='Обзор фильма "Мишки Гамми"', text='Здесь находится большой текст-описание обзора фильма "Мишки Гамми"')
    post5 = Post(user_id=user.id, title='Обзор фильма "Кремниевая долина"', text='Здесь находится большой текст-описание обзора фильма "Кремниевая долина"')
    session.add(post1)
    session.add(post2)
    session.add(post3)
    session.add(post4)
    session.add(post5)
    # Вносим данные в БД и закрываем сессию
    session.commit()
    user = session.query(User).filter_by(username=new_username).first()
    user_posts = session.query(Post).filter_by(user_id=user.id)
    user_posts = set(user_posts)
    print("-----------------Все посты добавлены----------------")
    for post in user_posts:
        print("Пост:", post,"- размещен пользователем: ",user)
    session.close()


# Показываем существующие теги
def show_existing_tags():
    session = Session()
    query_tags = session.query(Tag)
    tag = query_tags.first()
    tags = list(query_tags)
    print("-----------------Все существующие теги----------------")
    print(tags)
    #
    # query_filter_by_id = query_tags.filter(
    #     Tag.id > 2,
    # )
    # print("----Тег с id > 2----", query_filter_by_id)
    # # Фильтруем теги по содержанию
    # a_and_by_contains = query_filter_by_id.filter(
    #     Tag.name.contains('ком'),
    # )
    # print(a_and_by_contains)
    # print("----Все теги содержащие ком----")
    # print(a_and_by_contains.all())
    # print("----Все теги содержащие ком----")
    # # # Фильтрация тегов по требованию
    # # id > 2 & contains 'o'
    # q = query_tags.filter(
    #     or_(
    #         Tag.id > 2,
    #         Tag.name.contains('уж'),
    #     )
    # )
    # #
    # print(q)
    # print("----Все теги содержащие уж----")
    # print(q.all())
    # print("----Все теги содержащие уж----")
    # Closing session at the end of func
    session.close()


def add_tags_to_posts():
    """
    Adding tags for posts
        :return:
        """
    session = Session()
    tag = session.query(Tag).first()
    post: Post = session.query(Post).first()
    q_user = session.query(User.username).filter(User.id == 1)
    res_username = q_user.scalar()
    print('username:', res_username)
    print("----Все посты и их теги----", post, post.tags)


def show_join():
    """
        :return:
        """
    session = Session()

    q = session.query(
        User,
    ).join(
        Post,
        User.id == Post.user_id,
        ).filter(
        Post.title.contains('Гладиа')
    )


# make func for showing methods
def show_methods():
    session = Session()

    # q = session.query(Tag).filter(Tag.id == 1)
    # print(q)
    # print("-----111------Разобраться неясно, что отображает----------")
    # print(type(q))
    # print(list(q))
    # print("-----222------Разобраться неясно, что отображает----------")
    # print(q.all())
    # print("-----333------Разобраться неясно, что отображает----------")

    # Filter tags
    # q = session.query(Tag.name).filter(Tag.id.in_([1, 2, 4]))
    # print(q)
    # print("-----444------Разобраться неясно, что отображает----------")
    # print(type(q))
    # print("-----555------Разобраться неясно, что отображает----------")
    # # print(list(q))
    # res = q.all()
    # print([r for r, in res])
    # print("-----666------Разобраться неясно, что отображает----------")

    q_user = session.query(User.username).filter(User.id == 1)
    q_user = session.query(User.username).filter(User.id == 1)
    res_username = q_user.scalar()
    print('username:', res_username)
    print("-----888----------------")
    session.close()


def main():
    """
        :return:
        """
    is_base_exists()
    print("Залогинимся?")
    login_user()
    show_existing_tags()
    add_tags_to_posts()
    show_join()
    show_methods()


if __name__ == '__main__':
    main()
