"""Blogly application."""

from flask import Flask, request, redirect, render_template
from models import db, connect_db, User, Post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

from flask_debugtoolbar import DebugToolbarExtension
app.config['SECRET_KEY'] = "SECRET!"
debug = DebugToolbarExtension(app)


@app.get("/")
def display_home_page():
    """Presents the home page to the user"""#not true right now

    #for now, redirect to users page

    return redirect("/users")


@app.get("/users")
def display_users():
    """Display the users page"""

    users = User.query.all()#order by is advisable
    return render_template(
        "users.html",
        users=users
    )

@app.get('/users/new')
def display_new_user():#function name more better
    """Displays the form for a new user"""

    return render_template(
        "new_user.html",#same for html name

    )

@app.post('/users/new')
def create_new_user():
    """Handles form submission for a new user"""

    data = request.form
    print(data, 'this is data')

    first_name = data.get('first-name')
    last_name = data.get('last-name')
    image_url = data.get('image-url')

    image_url = image_url if image_url else None

    new_user = User(
        first_name=first_name,
        last_name=last_name,
        image_url=image_url
    )

    db.session.add(new_user)

    db.session.commit()

    return redirect('/users')

@app.get('/users/<int:user_id>')
def display_user_info(user_id):
    """Display user info page"""

    user = User.query.get_or_404(user_id)
    posts = Post.query.filter_by(user_id = user.id)

    return render_template(
        'user_page.html',
        posts=posts,
        user=user
    )

@app.get('/users/<int:user_id>/edit')
def edit_user_info(user_id):#fn name picky
    """Display edit user page"""

    user = User.query.get(user_id)#get_or_404

    return render_template(
        'user_edit.html',#same here
        user=user
    )

@app.post('/users/<int:user_id>/edit')
def save_user_info(user_id):
    """ Save user edit"""

    user = User.query.get(user_id)#again here

    data = request.form

    first_name = data.get('first-name')
    last_name = data.get('last-name')
    image_url = data.get('image-url')#detect empty string here for placeholder!
    #making it None doesnt work here either! default statement isnt triggered
    #db error? whatever it is it doesnt trigger default statement

    user.first_name = first_name
    user.last_name = last_name
    user.image_url = image_url


    db.session.commit()

    return redirect(f'/users/{user.id}')


@app.post('/users/<int:user_id>/delete')
def delete_user(user_id):
    """ Delete user profile """

    User.query.filter_by(id=user_id).delete()

    db.session.commit()

    return redirect('/')

@app.get('/posts/<int:post_id>')
def show_post_page(post_id):
    """ Show Post Page """

    post = Post.query.get_or_404(post_id)
    user_id = post.user_id

    return render_template(
        'post_page.html',
        post=post,
        user_id=user_id
    )

@app.get('/users/<int:user_id>/posts/new')
def display_form_new_post(user_id):
    """Display page for form to create new post"""

    user = User.query.get_or_404(user_id)

    return render_template(
        'new_post_form.html',
        user=user
    )

@app.post('/users/<int:user_id>/posts/new')
def submit_new_post(user_id):
    """Function handles submission of new post and redirects"""

    user = User.query.get_or_404(user_id)

    data = request.form
    title = data.get('post-title')
    content = data.get('post-content')

    new_post = Post(title=title, content=content, user_id=user_id)

    db.session.add(new_post)

    db.session.commit()

    return redirect(f"/users/{user_id}")

@app.get('/posts/<int:post_id>/edit')
def show_edit_post_form(post_id):
    """Function displays form to edit a post"""

    post = Post.query.get_or_404(post_id)

    return render_template(
        'edit_post_form.html',
        post=post
    )

@app.post('/posts/<int:post_id>/edit')
def handle_edit_post(post_id):
    """Function handles an edit post form submit"""

    post = Post.query.get_or_404(post_id)

    data = request.form

    title = data.get('post-title')
    content = data.get('post-content')

    post.title = title
    post.content = content

    db.session.commit()

    return redirect(f'/posts/{post_id}')
