import os
import json
import requests
import secrets
from PIL import Image
from flask import abort, redirect, render_template,url_for, flash, request
from blog import app, db, bcrypt
from blog.forms import RegistrationForm, LoginForm, UpdateProfileForm, PostForm, CommentForm
from blog.models import User, Post, Comment, Quote
from flask_login import login_required, login_user, current_user, logout_user

def get_quote():
    quote_url = 'http://quotes.stormconsultancy.co.uk/random.json'
    req = requests.get(quote_url)
    data = json.loads(req.content)
    quote = Quote(data["quote"],data["author"])
    return quote

@app.route("/")
@app.route("/home")
def home():
    quote = get_quote()
    print(quote)
    blogs = Post.query.all()
    return render_template("index.html", blogs=blogs, rand_quote=quote)


@app.route("/login",methods=["POST","GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash('Login successful. Happy blogging', 'success')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email or password', 'danger')
    return render_template('login.html', title="login",form=form)

@app.route("/register", methods=["POST","GET"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pass = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_pass)
        db.session.add(user)
        db.session.commit()
        flash(f'User signup successful please login',"success")
        return redirect(url_for('login'))
    return render_template('signup.html', title="signup",form=form)

@app.route("/logout")
def logout():
    logout_user()
    flash('User logout successful','success')
    return redirect('login')

def save_picture(form_pic):
    random_hex = secrets.token_hex(8)
    _f_name,f_ext = os.path.splitext(form_pic.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile-pic', picture_fn)

    output_size = (125,125)
    i = Image.open(form_pic)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn

@app.route("/profile", methods=["POST","GET"])
@login_required
def profile():
    form = UpdateProfileForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    img_file = url_for('static', filename='profile-pic/' + current_user.image_file)
    return render_template('profile.html', title="profile", user_img=img_file, form=form)

@app.route("/post/new", methods=["POST","GET"])
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data,user_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        flash('Blog post created successfully!', 'success')
        return redirect(url_for('home'))
    return render_template("create_post.html", title="new blog post", form=form, legend="Create a post")

@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    comments = Comment.query.filter_by(post_id=post.id)
    img_file = url_for('static', filename='images/' + post.image_file)
    return render_template("post.html", title=post.title,post=post,img_file=img_file, comments=comments)

def save_blogpicture(form_pic):
    random_hex = secrets.token_hex(8)
    _f_name,f_ext = os.path.splitext(form_pic.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/images', picture_fn)

    form_pic.save(picture_path)
    return picture_fn


@app.route("/post/<int:post_id>/update", methods=["POST","GET"])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()

    if form.validate_on_submit():
        print(form.content.data)
        if form.picture.data:
            picture_file = save_blogpicture(form.picture.data)
            post.image_file = picture_file
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Blog updated successfully!', 'success')
        return redirect(url_for('post',post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data=post.content
    return render_template("create_post.html", title="update post", form=form, legend="Update post")

@app.route("/post/<int:post_id>/delete", methods=["POST",'GET'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
            abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Blog post deleted successfully!','success')
    return redirect(url_for('home'))

@app.route("/post/<int:post_id>/comment/new", methods=["POST","GET"])
@login_required
def create_comment(post_id):
    post = Post.query.get_or_404(post_id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(content=form.content.data,user_id=current_user.id, post_id=post.id)
        db.session.add(comment)
        db.session.commit()
        flash('Comment posted successfully!', 'success')
        return redirect(url_for('post',post_id=post.id))
    return render_template("create_comment.html", title="post a comment", form=form, legend="Post a comment")

@app.route("/comment/<int:comment_id>/delete", methods=["POST",'GET'])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    if comment.post.author != current_user:
            abort(403)
    db.session.delete(comment)
    db.session.commit()
    flash('Comment deleted successfully!','success')
    return redirect(url_for('post', post_id=comment.post.id))

