from enum import unique
import random
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import string
import pymysql
pymysql.install_as_MySQLdb()
db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.Text(), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now())
    bookmarks = db.relationship('Bookmark', backref="user") #bookmark와 user의 relationship을 양방향으로 설정
    #backref로 인해 user.id, bookmark.user_id 모두 참조 가능 (한쪽에만 backref를 선언하면 다른쪽에도 자동으로 backref 생성 적용 됨)

    def generate_short_characters(self):
        characters=string.digits+string.ascii_letters # flask shell에서 import string 후 string.digits, string.ascii_letters 입력하면 무슨 값들인지 확인 가능
        picked_chars=random.choices(characters, k=3) # flask shell에서 import random 후 random.choices(string.ascii_letters, k=3)

        link=self.query.filter_by(short_url=picked_chars).first()

        if link:
            self.generate_short_characters()
        else: 
            return picked_chars

    def __init__(self,**kwargs): #**kwargs는 keyword arguments의 약자로 파라미터의 이름을 같이 보낼 수 있고 dictionary 형태로 저장된다. (*args는 튜플형태로 저장됨)
        super().__init__(**kwargs) # ex) func(name="aa", age="20"), 출력값={'age':'} => **kwargs라는 딕셔너리를 만들고 그 안에 name, age값을 넣는다고 보면 된다.

    def __repr__(self) -> str: #reference method
        return 'User>>> {self.username}' #representation of our model class 
    
    class Bookmark(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        body = db.Column(db.Text, nullable=True)
        url = db.Column(db.Text, nullable=False)
        short_url = db.Column(db.String(3), nullable=True)
        visits=db.Column(db.Integer, default=0)
        user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
        created_at = db.Column(db.DateTime, default=datetime.now())
        updated_at = db.Column(db.DateTime, default=datetime.now())
