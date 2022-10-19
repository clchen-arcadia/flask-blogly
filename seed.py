"""Seed file to make """

from models import User, db
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