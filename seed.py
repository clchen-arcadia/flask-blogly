"""Seed file to make """

from models import User, Post, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# Add users
alan = User(first_name='Alan', last_name='Alda')
joel = User(first_name='Joel', last_name='Burton')
jane = User(first_name='Jane', last_name='Smith')

# Add new users to session
db.session.add(alan)
db.session.add(joel)
db.session.add(jane)

# commit session
db.session.commit()

# Sample posts
post_1 = Post(title='First Post', content='test post please ignore', user_id=2)
post_2 = Post(title='Second Post', content='test post please ignore', user_id=2)
post_3 = Post(title='Third Post', content='test post please ignore', user_id=2)

# Add new posts to session
db.session.add(post_1)
db.session.add(post_2)
db.session.add(post_3)

# commit session
db.session.commit()