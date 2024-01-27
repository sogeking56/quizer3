from ext import db, app, loginm
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class Points(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    point = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    quiz_id = db.Column(db.Integer)

class Quizelem(db.Model):
    quiz_id = db.Column(db.ForeignKey("Quiz_.id"))
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String)
    qans = db.Column(db.String)
    in1 = db.Column(db.String)
    in2 = db.Column(db.String)
    in3 = db.Column(db.String)

    quiz = db.relationship("Quiz", back_populates="quizelem")

class Quiz(db.Model):
    __tablename__ = "Quiz_"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    img = db.Column(db.String)
    category = db.Column(db.String)
    clicks = db.Column(db.Integer)
    quizelem = db.relationship("Quizelem", back_populates="quiz")

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    password = db.Column(db.String)
    role = db.Column(db.String)
    math = db.Column(db.Integer)
    physics = db.Column(db.Integer)
    chemistry = db.Column(db.Integer)
    geography = db.Column(db.Integer)
    history = db.Column(db.Integer)
    literature = db.Column(db.Integer)
    other = db.Column(db.Integer)

    def __init__ (self, name, password, math, physics, chemistry, history, geography, literature, other, role="guest"):
        self.name=name
        self.password=generate_password_hash(password)
        self.role=role
        self.math=math
        self.physics=physics
        self.chemistry=chemistry
        self.history=history
        self.geography=geography
        self.literature=literature
        self.other=other

    def check(self, password):
        return check_password_hash(self.password, password)
@loginm.user_loader
def load_user(index):
    return User.query.get(index)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

        admin = User(name= "god", password= "gaga123", role= "admin", math=0, physics=0, chemistry=0, history=0, geography=0, literature=0, other=0)
        db.session.add(admin)
        db.session.commit()
