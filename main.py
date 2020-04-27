from sqlalchemy import create_engine, Column, Integer, String, Text, Boolean, ForeignKey, Table, or_
from sqlalchemy.orm import relationship, sessionmaker, scoped_session, joinedload
from sqlalchemy.ext.declarative import declarative_base
import pathlib

engine = create_engine('sqlite:///myblog.db')
Base = declarative_base(bind=engine)

session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)


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
    username = Column(String(30), nullable=False)
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


# make func to create users and posts
def create_users_posts():
    session = Session()
    # make User from class User
    user = User(username='editor')
    # adding user
    session.add(user)
    # flush session to get id of newly created user
    session.flush(session)
    # make some posts for user
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
    session.close()


# create standard tags in DB
def create_standard_tags():
    session = Session()
    # Сделать механизм противодействия дублирования тегов
    # Сначала выберем все теги из БД
    query_tags = session.query(Tag)
    existed_tags = set(query_tags)
    # print(existed_tags)
    print(type(existed_tags))
    # for tag in existed_tags:
    #     print(tag)
    #     print(type(tag))
    standard_tags = ('комедия', 'боевик', 'ужасы', 'мультфильм', 'документалка')
    for tag_candidate in standard_tags:
        existed_tags.add(tag_candidate)
    print(existed_tags)
    # all_tags = existed_tags + standard_tags
    for tag_candidate in standard_tags:
        if tag_candidate in existed_tags:
            print('Тег"',tag_candidate,'" уже содержится в БД.')
        else:
            tag_candidate = Tag(name=tag_candidate)
            session.add(tag_candidate)
    # for tag in standard_tags:
    #     print(tag)
    #     print(type(tag))
    #     tag = Tag(name=tag)
    #     session.add(tag)
    session.commit()
    session.close()


# Показываем существующие теги
def show_existing_tags():
    session = Session()

    query_tags = session.query(Tag)
    # Show first tag
    tag = query_tags.first()
    # print(tag)
    # print(tag.posts)
    # tags = query_tags.all()
    tags = list(query_tags)
    print(tags)

    # query_filter_by_id = query_tags.filter(
    #     Tag.id > 2,
    # )
    # # print(query_filter_by_id)
    # # print(query_filter_by_id.all())
    # # Фильтруем теги по содержанию
    # a_and_by_contains = query_filter_by_id.filter(
    #     Tag.name.contains('g'),
    # )
    # # print(a_and_by_contains)
    # # print(a_and_by_contains.all())
    # # Фильтрация тегов по требованию
    # # id > 2 & contains 'o'
    # q = query_tags.filter(
    #     or_(
    #         Tag.id > 2,
    #         Tag.name.contains('o'),
    #     )
    # )
    # #
    # print(q)
    # print(q.all())
    # Closing session at the end of func
    session.close()


# Adding tags for posts
def add_tags_to_posts():
    """
        :return:
        """
    session = Session()

    tag = session.query(Tag).first()
    post: Post = session.query(Post).first()
    # post.tags.append(tag)
    #
    # session.commit()

    print(post, post.tags)
    # print(tag, tag.posts)


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
        # Post.title.contains('flask')
        Post.tags.any(Tag.id == 1)
    )
    print(q)
    print(q.all())


# make func for showing methods
def show_methods():
    session = Session()

    # q = session.query(Tag).filter(Tag.id == 1)
    # print(q)
    # # print(type(q))
    # print(list(q))
    # print(q.all())

    # Filter tags
    # q = session.query(Tag.name).filter(Tag.id.in_([1, 2, 4]))
    # print(q)
    # print(type(q))
    # # print(list(q))
    # res = q.all()
    # print([r for r, in res])

    # q_user = session.query(User.username).filter(User.id == 1)
    # user = q_user.one()
    # print(user)
    #
    # res_username = q_user.scalar()
    # print('username:', res_username)
    session.close()


# Делаем проверку наличия БД в текущей папке
path_to_db = pathlib.Path('myblog.db')
# print(path_to_db.exists())  # True
# print(path_to_db.is_file())  # True

def main():
    """
        :return:
        """
    if not path_to_db:
        Base.metadata.create_all()
        create_users_posts()
    create_standard_tags()
    show_existing_tags()
    add_tags_to_posts()
    show_join()
    show_methods()


if __name__ == '__main__':
    main()
