"""Blogly application."""

from flask import Flask, request, redirect, render_template
from models import db, connect_db, User

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
    """Presents the home page to the user"""

    #for now, redirect to users page

    return redirect("/users")


# @app.post("/")
# def


@app.get("/users")
def display_users():
    """Display the users page"""

    users = User.query.all()
    return render_template(
        "users.html",
        title="Users",
        users=users
    )

@app.get('/users/new')
def display_new_user():
    """Displays the form for a new user"""

    return render_template(
        "new_user.html",
        title='Create New User'

    )

@app.post('/users/new')
def create_new_user():
    """Handles form submission for a new user"""

    print('YOU GOT HERE ------')

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

    return redirect('/')

@app.get('/users/<int:user_id>')
def display_user_info(user_id):
    """Display user info page"""

    user = User.query.get(user_id)

    return render_template(
        'user_page.html',
        user=user
    )
