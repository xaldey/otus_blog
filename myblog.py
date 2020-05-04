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
    print("(Первый тег) .first()", tag)
    print("Теги к постам", tag.posts)
    tags1 = q_tags.all()
    for tag in tags1:
        print("Все теги методом .all()", tag)
    session.close()


def add_tags_to_posts():
    print(decor)
    print("Добавляем теги к постам:")
    session = Session()
    # Назначим первый тег первому посту
    tag = session.query(Tag).first()
    post: Post = session.query(Post).first()
    post.tags.append(tag)

    # Назначим тег содержащий "боевик" посту содержащему "Гладиатор"
    post_war = session.query(Post).filter(Post.title.contains('Гладиатор')).one()
    tag_war = session.query(Tag).filter(Tag.name.contains('боевик')).one()
    post_war.tags.append(tag_war)
    session.commit()
    print("Пост -", post, "с тегом -", post.tags)
    print("Тег -", tag,"к посту -", tag.posts)
    print("Пост -", post_war, "с тегом -", post_war.tags)
    print("Тег -", tag_war, "к посту -", tag_war.posts)
    session.close()


def show_join():
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
    )
    print("Post.title.contains('Гамми')", query_user_join.all())
    session.close()


def show_methods():
    print(decor)
    print("Разбираем методы")
    session = Session()
    query_first_tag = session.query(Tag).filter(Tag.id == 1)
    print("Список первого тега через list", list(query_first_tag))
    print("Список первого тега через .all",query_first_tag.all())
    query_tag = session.query(Tag.name).filter(
        Tag.name.contains("боевик")
    )
    print("Tag.name.contains(боевик) .all ", query_tag.all())
    q_user = session.query(User.username).filter(User.id == 1)
    user = q_user.one()
    print("User.id == 1 ->", user)
    # Берем первого пользователя из запроса
    res_username = q_user.scalar()
    print('username:', res_username)
    session.close()


def show_posts_and_tags():
    session = Session()
    query_posts = session.query(Post)
    # query_tags = session.query(Tag)
    query_posts = query_posts.all()
    print("Вывести все посты и их теги:")
    for post in query_posts:
        print(post, post.tags)
    session.close()


def show_posts_without_tags():
    session = Session()
    query_posts = session.query(Post)
    # query_tags = session.query(Tag)
    query_posts = query_posts.all()
    print("Вывести все посты без тегов:")
    for post in query_posts:
        if post.tags:
            pass
        else:
            print(post)
    session.close()


def main():
    is_base_exists()
    show_existing_tags()
    add_tags_to_posts()
    show_join()
    show_methods()
    show_posts_and_tags()
    show_posts_without_tags()


if __name__ == '__main__':
    main()
