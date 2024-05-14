from db.database import *
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime


class Post(Base):
    __tablename__ = "post"  # 기본적으로 테이블 이름은 자동으로 정의되지만 이 처럼 명시적으로 정할 수 있다.

    id = Column(Integer, primary_key=True)
    post_key = Column(String(30), unique=True)
    post_write_date = Column(DateTime, default=datetime.now)

    def __init__(self, post_key):
        self.post_key = post_key
        # self.post_write_date = post_write_date


class Blog(Base):
    __tablename__ = "blog"

    postId = Column(Integer, primary_key=True)
    url = Column(String(300), unique=True)
    status = Column(Integer)

    def __init__(self, postId, url, status):
        self.postId = postId
        self.url = url
        self.status = status


# # 데이터베이스 생성
# init_db()
