from flask import Flask, render_template, request, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, Email, EqualTo, ValidationError
import re

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'

# Dummy user data
users = {
    "shane1": {
        "email": "shane1@example.com",
        "password": "Password1!"
    }
}

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=6, max=20)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6, max=20)])

    def validate_username(self, username):
        user = users.get(username.data)
        if user is None:
            raise ValidationError("Username does not exist. Please register.")

    def validate_password(self, password):
        user = users.get(self.username.data)
        if user is not None:
            if password.data != user['password']:
                raise ValidationError("Password is incorrect.")

@app.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session['username'] = form.username.data
        return redirect(url_for('home'))
    return render_template('login.html', form=form)

@app.route('/home')
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    return "Welcome to the homepage!"

if __name__ == '__main__':
    app.run(debug=True)