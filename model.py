from app import db

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120))
    password = db.Column(db.String(200))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    body = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    ##pub_date = db.Column(db.DateTime)

    def __init__(self, title, body, usr): ## pub_date = None):
        self.title = title
        self.body = body
        self.user_id = usr
        ##if pub_date is None:
        ##    pub_date = datetime.utcnow()
        ##self.pub_date = pub_date