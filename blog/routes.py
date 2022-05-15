from flask import redirect, render_template,url_for, flash
from blog import app
from blog.forms import RegistrationForm, LoginForm
from blog.models import User, Post, Comment


blogs = [
    {
        "title":"First blog post",
        "content": "",
        "date_posted":"13-02-2021",
        "no_of_comments":30
    },
    {
        "title":"second blog post",
        "content": "",
        "date_posted":"25-04-2022",
        "no_of_comments":15
    },
    {
        "title":"third blog post",
        "content": "",
        "date_posted":"25-01-2022",
        "no_of_comments":1
    },
    {
        "title":"fourth blog post",
        "content": "",
        "date_posted":"25-01-2022",
        "no_of_comments":1
    },
    {
        "title":"fifth blog post",
        "content": "",
        "date_posted":"25-01-2022",
        "no_of_comments":1
    }
]

@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html", blogs=blogs)


@app.route("/login",methods=["POST","GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == "clintonwambugu@gmail.com" and form.password.data == "pass":
            flash(f'login successfully',"success")
            return redirect(url_for('home'))
        else:
            flash(f'login failed! Try again',"danger")
    return render_template('login.html', title="login",form=form)

@app.route("/register", methods=["POST","GET"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'user was created successfully',"success")
        return redirect(url_for('home'))
    return render_template('signup.html', title="signup",form=form)