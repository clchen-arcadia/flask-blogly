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
    """Presents the home page to the user"""#not true right now

    #for now, redirect to users page

    return redirect("/users")


@app.get("/users")
def display_users():
    """Display the users page"""

    users = User.query.all()#order by is advisable
    return render_template(
        "users.html",
        title="Users",
        users=users
    )

@app.get('/users/new')
def display_new_user():#function name more better
    """Displays the form for a new user"""

    return render_template(
        "new_user.html",#same for html name
        title='Create New User'

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

    user = User.query.get(user_id)#get_or_404 is better here

    # posts = Post.query.all() #TODO: get by foreign key

    return render_template(
        'user_page.html',
        user=user
    )

@app.get('/users/<int:user_id>/edit')
def edit_user_info(user_id):#fn name picky
    """Display edit user page"""

    user = User.query.get(user_id)#get_or_404

    return render_template(
        'user_edit.html',#same here
        title='Edit a User',
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
