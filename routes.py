import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from flaskblog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
#from flaskblog.relation_extraction import relExtra

dummy_data={
    'nodes': [
    {'name': "Adam"},
    {'name': "Bob"},
    {'name': "Carrie"},
    {'name': "Donovan"},
    {'name': "Edward"},
    {'name': "Felicity"},
    {'name': "George"},
    {'name': "Hannah"},
    {'name': "Iris"},
    {'name': "Jerry"}
    ],
    'edges': [
    {'source': 0, 'target': 1,'label':"friend"},
    {'source': 0, 'target': 2,'label':"student"},
    {'source': 0, 'target': 3,'label':"lover"},
    {'source': 0, 'target': 4,'label':"old friend"},
    {'source': 1, 'target': 5,'label':"killed by"},
    {'source': 2, 'target': 5,'label':"classmates"},
    {'source': 3, 'target': 4,'label':"teacher"},
    {'source': 5, 'target': 8,'label':"teacher"},
    {'source': 5, 'target': 9,'label':"teacher"},
    {'source': 6, 'target': 7,'label':"teacher"},
    {'source': 7, 'target': 8,'label':"teacher"},
    {'source': 8, 'target': 9,'label':"teacher"}
    ]
    }

data = {
    'nodes':[
        {"name": "Mr.Wargrave"},
        {"name": "Constance Culmington"},
        {"name": "Vera Claythrone"},
        {"name": "Nancy Owen"},
        {"name": "Philip Lombard"},
        {"name": "Mr. Issac Morris"},
        {"name": "Ms. Emily Brent"},
        {"name": "General MacArthur"},
        {"name": "Mr. U.N.Owen"},
        {"name": "Dr. Armstrong"},
        {"name": "Mr. and Mrs. Rogers"},
        {"name": "Mr. Blore"},
        {"name": "Unknown"}
    ],
    "edges":[
        {"source": 0,"target": 1,"label": "invited by"},
        {"source": 2,"target": 3, "label":"offered job by"},
        {"source": 4,"target": 5,"label": "work for"},
        {"source": 6,"target": 12,"label": "invited by"},
        {"source": 7,"target": 8,"label": "old cronies"},
        {"source": 9,"target": 8,"label": "doctor of"},
        {"source": 10,"target": 12,"label": "offered by"},
        {"source": 11,"target": 12,"label": "hired by"}
    ]
}

@app.route("/")
@app.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts)

@app.route("/userhome/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('user_posts.html', posts=posts, user=user)



@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            page = request.args.get('page', 1, type=int)
            user = User.query.filter_by(username=user.username).first_or_404()
            posts = Post.query.filter_by(author=user) \
                .order_by(Post.date_posted.desc()) \
                .paginate(page=page, per_page=5)
            return render_template('user_posts.html', posts=posts, user=user)
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)


@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your project has been created!', 'success')
        return redirect(url_for('post', post_id=post.id))
    return render_template('create_post.html', title='New Post',
                           form=form, legend='New Post')


@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    #r = relExtra(post.content)
    return render_template('post.html', title=post.title, post=post,relation = data)


@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('The diagram is generated as below.', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')


@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(author=current_user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    flash('Your project has been deleted!', 'success')
    return render_template('user_posts.html', posts=posts, user=current_user)

"""
@app.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('user_posts.html', posts=posts, user=user)
"""