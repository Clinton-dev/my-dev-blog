from datetime import datetime
from flask import Flask, redirect, render_template,url_for, flash
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm

app = Flask(__name__)

app.config['SECRET_KEY']='a6f7c3788a7d8c742c822985818a41f8'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='user-default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    comments = db.relationship('Comments', backref='user', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    image_file = db.Column(db.String(20), nullable=False, default='blog-default.jpg')
    content = db.Column(db.Text, nullable=False)
    comments = db.relationship('Comments', backref='post', lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.content}', '{self.date_posted}')"

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


if __name__ == "__main__":
    app.run(debug=True)