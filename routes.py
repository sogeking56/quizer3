import random

from flask import render_template, redirect, url_for
from os import path
from flask_login import login_user, logout_user, login_required, current_user
from ext import app, db
from models import Quizelem, Quiz, User, Points
from forms import AddMain, AddQuize_lem, Edit_main, Edit_qelem, Register, Login, View_Quiz
from random import shuffle

@app.route("/")
@login_required
def home():
    quizes=Quiz.query.order_by(Quiz.clicks.desc()).all()
    exist = True
    if current_user:
        if current_user.math == max(current_user.math, current_user.physics, current_user.chemistry, current_user.history, current_user.geography, current_user.literature, current_user.other): quizes2 = Quiz.query.order_by(Quiz.clicks.desc()).filter(Quiz.category == "math" ).all()
        if current_user.physics == max(current_user.math, current_user.physics, current_user.chemistry, current_user.history, current_user.geography, current_user.literature, current_user.other): quizes2 = Quiz.query.order_by(Quiz.clicks.desc()).filter(Quiz.category == "physics" ).all()
        if current_user.chemistry == max(current_user.math, current_user.physics, current_user.chemistry, current_user.history, current_user.geography, current_user.literature, current_user.other): quizes2 = Quiz.query.order_by(Quiz.clicks.desc()).filter(Quiz.category == "chemistry" ).all()
        if current_user.history == max(current_user.math, current_user.physics, current_user.chemistry, current_user.history, current_user.geography, current_user.literature, current_user.other): quizes2 = Quiz.query.order_by(Quiz.clicks.desc()).filter(Quiz.category == "history" ).all()
        if current_user.geography == max(current_user.math, current_user.physics, current_user.chemistry, current_user.history, current_user.geography, current_user.literature, current_user.other): quizes2 = Quiz.query.order_by(Quiz.clicks.desc()).filter(Quiz.category == "geography" ).all()
        if current_user.literature == max(current_user.math, current_user.physics, current_user.chemistry, current_user.history, current_user.geography, current_user.literature, current_user.other): quizes2 = Quiz.query.order_by(Quiz.clicks.desc()).filter(Quiz.category == "literature" ).all()
        if current_user.other == max(current_user.math, current_user.physics, current_user.chemistry, current_user.history, current_user.geography, current_user.literature, current_user.other): quizes2 = Quiz.query.order_by(Quiz.clicks.desc()).filter(Quiz.category == "other" ).all()
        del quizes2[3:]
        if current_user.math + current_user.physics + current_user.chemistry + current_user.history + current_user.geography + current_user.literature + current_user.other == 0:
            exist = False
    return render_template("mainQ.html", quizzes=quizes, quizzes2=quizes2, exist=exist)
@app.route("/category/<string:category>")
@login_required
def category(category):
    quiz = Quiz.query.filter(Quiz.category == category).all()
    return render_template("mainQ.html", quizzes=quiz)

@app.route("/add_quiz", methods=["GET", "POST"])
@login_required
def add_quiz():
    form = AddMain()
    if form.validate_on_submit():
        new_quiz = Quiz(title=form.title.data, img=form.img.data.filename, category=form.category.data, clicks=0)
        db.session.add(new_quiz)
        db.session.commit()

        file_dir = path.join(app.root_path, "static", form.img.data.filename)
        form.img.data.save(file_dir)
        return redirect("/add_quizelem")
    return render_template("add_quiz.html", form=form)

@app.route("/add_quizelem", methods=["GET", "POST"])
@login_required
def add_elem():
    form = AddQuize_lem()
    if form.validate_on_submit():
        new_quizelem = Quizelem(quiz_id=len(Quiz.query.all()), question=form.question.data, qans=form.qans.data, in1=form.in1.data, in2=form.in2.data, in3=form.in3.data,)
        db.session.add(new_quizelem)
        db.session.commit()
        return redirect("/add_quizelem")
    return render_template("add_quizelem.html", form=form)

@app.route("/start_quiz/<int:index>", methods=["GET", "POST"])
@login_required
def start_quiz(index):
    points = 0
    exist = True
    form = View_Quiz()
    quiz=Quiz.query.filter(Quiz.id == index).first()
    quiz_elem = Quizelem.query.filter(Quizelem.quiz_id == index).first()
    answers = [quiz_elem.qans, quiz_elem.in1, quiz_elem.in2, quiz_elem.in3]
    new_points = Points(user_id = current_user.id, quiz_id = index, point = 0)
    answers = list(filter(None, answers))
    random.shuffle(answers)
    form.answers.choices = answers
    if form.validate_on_submit():
        if quiz.category == "math": current_user.math += 1
        if quiz.category == "physics": current_user.physics += 1
        if quiz.category == "chemistry": current_user.chemistry += 1
        if quiz.category == "history": current_user.history += 1
        if quiz.category == "geography": current_user.geography += 1
        if quiz.category == "literature": current_user.literature += 1
        if quiz.category == "other": current_user.other += 1
        quiz.clicks += 1
        if form.answers.data == quiz_elem.qans:
            new_points.point += 1
            db.session.add(new_points)
            db.session.commit()
        return redirect(url_for("quiz", index=index, qid=quiz_elem.id +1))
    return render_template("start_quiz.html", form = form, quiz_elem = quiz_elem)


@app.route("/quiz/<int:index>/<int:qid>", methods=["GET", "POST"])
def quiz(index, qid):
    exist = True
    form = View_Quiz()
    quiz_elem = Quizelem.query.filter(Quizelem.quiz_id == index, Quizelem.id == qid).first()
    point = Points.query.filter(Points.user_id == current_user.id, Points.quiz_id == index).all()
    point = point[-1]
    answers = [quiz_elem.qans, quiz_elem.in1, quiz_elem.in2, quiz_elem.in3]
    random.shuffle(answers)
    answers = list(filter(None, answers))
    form.answers.choices = answers
    if not Quizelem.query.filter(Quizelem.quiz_id == index, Quizelem.id == qid + 1).first():
        exist = False

    if form.validate_on_submit():
        if form.answers.data == quiz_elem.qans :
            point.point +=1
            db.session.commit()
        if not Quizelem.query.filter(Quizelem.quiz_id == index, Quizelem.id == qid + 1).first():
            return redirect(url_for("result", index=index))
        return redirect(url_for("quiz", index=index, qid=quiz_elem.id + 1))
    return render_template("quiz.html", quiz_elem=quiz_elem, form=form)

@app.route("/result/<int:index>")
def result(index):
    classpoint = Points.query.filter(Points.user_id == current_user.id, Points.quiz_id == index).all()
    point = classpoint[-1]
    point = point.point
    return render_template("result.html", point = point)


@app.route("/delete/<int:index>")
def delete (index):
    if current_user.role != "admin":
        return redirect("/")
    quiz_elem = Quizelem.query.filter(Quizelem.quiz_id == index).all()
    quiz=Quiz.query.get(index)
    for qel in quiz_elem:
       db.session.delete(qel)
    db.session.delete(quiz)
    db.session.commit()
    return redirect("/")


@app.route("/edit_main/<int:index>", methods=["GET", "POST"])
def edit_main(index):
    if current_user.role != "admin":
        return redirect("/")
    quiz = Quiz.query.get(index)
    form = Edit_main(title=quiz.title, category=quiz.category)
    if form.validate_on_submit():
        quiz.title = form.title.data
        quiz.category = form.category.data
        if form.img.data:
            quiz.img=form.img.data.filename
            file_dir = path.join(app.root_path, "static", form.img.data.filename)
            form.img.data.save(file_dir)
        db.session.commit()
        return redirect("/")
    return render_template("add_quiz.html", form=form)

@app.route("/edit_page/<int:index>")
def edit_qelem(index):
    if current_user.role != "admin":
        return redirect("/")
    quiz_elem = Quizelem.query.filter(Quizelem.quiz_id == index).all()
    return render_template("edit_page.html", quiz_elem=quiz_elem)

@app.route("/edit_qelem/<int:qindex>/<int:index>", methods=["GET", "POST"])
def edit_elem(qindex, index):
    if current_user.role != "admin":
        return redirect("/")
    quiz_elems = Quizelem.query.filter(Quizelem.quiz_id == qindex).all()
    for quiz_elem in quiz_elems:
        if quiz_elem.id == index:
            qelem=quiz_elem
            break
    form = Edit_qelem(question=qelem.question, qans=qelem.qans, in1=qelem.in1, in2=qelem.in2, in3=qelem.in3,)
    if form.validate_on_submit():
        qelem.question = form.question.data
        qelem.qans = form.qans.data
        qelem.in1 = form.in1.data
        qelem.in2 = form.in2.data
        qelem.in3 = form.in3.data

        db.session.commit()
        return redirect("/")
    return render_template("add_quizelem.html", form=form)

@app.route("/Register", methods=["GET", "POST"])
def register():
    form = Register()
    exists = False
    user_all=User.query.all()
    if form.validate_on_submit():
        for user1 in user_all:
            if user1.name == form.name.data:
                exists = True
        if not exists:
            user = User(name=form.name.data, password=form.password.data, role="guest", math=0, physics=0, chemistry=0,
                        history=0, geography=0, literature=0, other=0)
            db.session.add(user)
            db.session.commit()
        return redirect("/")
    return render_template("register.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = Login()
    if form.validate_on_submit():
        user = User.query.filter(User.name == form.name.data).first()
        if user and user.check(form.password.data):
            login_user(user)
            return redirect("/")
    return render_template("login.html", form=form)

@app.route("/log_out")
def logout():
    logout_user()
    return redirect("/")

