from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer, ForeignKey, Table, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, scoped_session, joinedload
from sqlalchemy.orm.session import sessionmaker

engine = create_engine('sqlite3://myblog.db', echo=True)
Base = declarative_base()
Base.metadata.create_all(engine)

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
    username = Column(String, nullable=False)
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
    session = sessionmaker(bind=engine)
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


def main():
    create_users_posts


if __name__ == '__main__':
    main()
