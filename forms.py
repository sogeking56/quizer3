from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, StringField, IntegerField, SubmitField, PasswordField, RadioField, SelectField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileRequired
class AddAds(FlaskForm):
    text= TextAreaField("რეკლამის ტექსტი", validators=[DataRequired()])
    img= FileField("სურათი", validators=[FileRequired()])
    submit= SubmitField("დამატება")

class  AddProducts(FlaskForm):
    name= StringField("პროდუქტის სახელი", validators=[DataRequired()])
    price= IntegerField("ფასი", validators=[DataRequired()])
    img= FileField("სურათი", validators=[FileRequired()])
    submit= SubmitField("დამატება")


class AddMain(FlaskForm):
    title= StringField("ქვიზის სახელი", validators=[DataRequired()])
    img= FileField("სურათი", validators=[FileRequired()])
    category = SelectField("კატეგორია",validators=[DataRequired()], choices=[("other", "სხვა"), ("physics", "ფიზიკა"), ("chemistry", "ქიმია"),
                                                 ("history", "ისტორია"),("liteture", "ლიტარატურა"),("math", "მათემათიკა ")])
    submit= SubmitField("დამატება")

class AddQuize_lem(FlaskForm):
    question = StringField("შკითხვა", validators=[DataRequired()])
    qans = StringField("სწორი პასუხი", validators=[DataRequired()])
    in1 = StringField("არასწორი პასუხი (სავალდებულო)", validators=[DataRequired()])
    in2 = StringField("არასწორი პასუხი (არა სავალდებულო)")
    in3 = StringField("არასწორი პასუხი (არა სავალდებულო")
    submit = SubmitField("დამატება და შემდეგ შეკიტხვაზე გადასვლა")

class Edit_main(FlaskForm):
    title = StringField("ქვიზის სახელი")
    img = FileField("სურათი")
    category = SelectField("კატეგორია", choices=[("other", "სხვა"), ("physics", "ფიზიკა"), ("chemistry", "ქიმია"),
                                        ("history", "ისტორია"),("liteture", "ლიტარატურა"),("math", "მათემათიკა ")])
    submit = SubmitField("დამატება")

class Edit_qelem(FlaskForm):
    question = StringField("შკითხვა",)
    qans = StringField("სწორი პასუხი",)
    in1 = StringField("არასწორი პასუხი")
    in2 = StringField("არასწორი პასუხი")
    in3 = StringField("არასწორი პასუხი")
    submit = SubmitField("დამატება და უკან დაბრუნება")

class Register(FlaskForm):
    name = StringField("სახელი", validators=[DataRequired()])
    password = PasswordField("შეიყვანეთ პაროლი", validators=[DataRequired()])
    submit = SubmitField("დარეგისტრირება")

class Login(FlaskForm):
    name = StringField("სახელი", validators=[DataRequired()])
    password = PasswordField("შეიყვანეთ პაროლი", validators=[DataRequired()])
    submit = SubmitField("დალოგინდი")

class View_Quiz(FlaskForm):
    answers = RadioField("rame", choices=[], validate_choice=False)
    submit = SubmitField("დაადასტურეთ პასუხი")