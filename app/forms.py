from tkinter.tix import Select
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo, Optional

class LoginForm(FlaskForm):
    username = StringField(label="Username", validators=[DataRequired()])
    password = PasswordField(label="Password", validators=[DataRequired()])
    remember_me = BooleanField(label="Remember Me")
    submit = SubmitField(label="Log In")

class SignUpForm(FlaskForm):
    username = StringField(label="Username", validators=[DataRequired()])
    password = PasswordField(label="Password", validators=[DataRequired(), Length(min=8, max=25)])
    confirm = PasswordField(label="Confirm Password", validators=[DataRequired(), EqualTo('password')])
    first_name = StringField(label="First Name", validators=[DataRequired()])
    last_name = StringField(label="Last Name", validators=[DataRequired()])
    submit = SubmitField(label="Submit")

class TodosForm(FlaskForm):
    title = StringField(label="Title", validators=[DataRequired()])
    description = TextAreaField(label="Description", validators=[DataRequired()])
    status = SelectField(label="Status", choices=[(1, "Complete"), (0, "In progress")])
    priority = SelectField(label="Priority Level", choices=["Low", "High"])
    submit = SubmitField(label="Submit")