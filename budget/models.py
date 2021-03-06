import datetime

from flask_login import UserMixin

from budget import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(60), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    buys = db.relationship('Buy', backref='author', lazy=True)

    def __repr__(self):
        return f'{self.__class__.__name__}({self.id}, {self.username})'


class Buy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    desc = db.Column(db.String(), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.date.today())
    price = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(120), nullable=False, default='سایر')
    tags = db.Column(db.String())
    image = db.Column(db.String())

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

    def __repr__(self):
        return f'{self.__class__.__name__}({self.id}, {self.desc}, {self.category}' \
               f'{self.tags}, {self.image}, {self.date.today()})'
