from sqlalchemy import create_engine, Column, Integer, String, Text, Boolean, ForeignKey, Table, or_
from sqlalchemy.orm import relationship, sessionmaker, scoped_session, joinedload
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///myblog.db')
Base = declarative_base(bind=engine)

session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)


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
    print("-*-" * 20)
    print("show_existing_tags():")
    print("-*-" * 20)
    session = Session()

    q_tags = session.query(Tag)
    tag = q_tags.first()
    print("tag = q_tags.first()", tag)
    print(tag.posts)
    tags1 = q_tags.all()
    tags2 = list(q_tags)
    print("tags1 = q_tags.all()",tags1)
    print("tags2 = list(q_tags)",tags2)


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
    print("-*-" * 20)
    print("add_tags_to_posts():")
    print("-*-" * 20)
    session = Session()

    tag = session.query(Tag).first()
    post: Post = session.query(Post).first()
    # post.tags.append(tag)
    #
    # session.commit()
    print(post, post.tags)
    print(tag, tag.posts)


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
        Post.title.contains('тяжкие')
        # Post.tags.any(Tag.id == 1)
    )
    print("Post.title.contains('тяжкие')", q)
    print("Post.title.contains('тяжкие')", q.all())


def show_methods():
    print("show_methods():")

    session = Session()

    q = session.query(Tag).filter(Tag.id == 1)
    print(q)
    print(type(q))
    print(list(q))
    print(q.all())

    q = session.query(Tag.name).filter(Tag.id.in_([1, 2, 4]))
    print(q)
    print(type(q))
    # print(list(q))
    res = q.all()
    print([r for r, in res])

    q_user = session.query(User.username).filter(User.id == 1)
    user = q_user.one()
    print(user)

    res_username = q_user.scalar()
    print('username:', res_username)


def main():
    Base.metadata.create_all()
    create_users_posts()
    create_start_tags()
    show_existing_tags()
    add_tags_to_posts()
    show_join()
    show_methods()


if __name__ == '__main__':
    main()
