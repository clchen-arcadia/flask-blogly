from unittest import TestCase

from app import app, db
from models import DEFAULT_IMAGE_URL, User, connect_db

# Let's configure our app to use a different database for tests
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///blogly_test"

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

connect_db(app)
db.create_all()


class UserViewTestCase(TestCase):
    """Test views for users."""

    def setUp(self):
        """Create test client, add sample data."""

        # As you add more models later in the exercise, you'll want to delete
        # all of their records before each test just as we're doing with the
        # User model below.
        User.query.delete()

        self.client = app.test_client()

        test_user = User(
            first_name="test_first_one",
            last_name="test_last_one",
            image_url=None,
        )

        second_user = User(
            first_name="test_first_two",
            last_name="test_last_two",
            image_url=None,
        )

        db.session.add_all([test_user, second_user])
        db.session.commit()

        # We can hold onto our test_user's id by attaching it to self (which is
        # accessible throughout this test class). This way, we'll be able to
        # rely on this user in our tests without needing to know the numeric
        # value of their id, since it will change each time our tests are run.
        self.user_id = test_user.id

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()

    def test_list_users(self):
        """Tests route to page of list all users"""

        with self.client as c:
            resp = c.get("/users")
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("test_first_one", html)
            self.assertIn("test_last_one", html)

    def test_get_edit_user(self):
        """Tests route to get edit user form page"""

        with self.client as c:
            resp = c.get(f"/users/{self.user_id}/edit")
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("test_first_one", html)
            self.assertIn("test_last_one", html)

    def test_post_edit_user(self):
        """Tests route to edit user and its redirect"""

        with self.client as c:

            resp_post = c.post(
                f"/users/{self.user_id}/edit",
                data = {
                    "first-name": "test_edit_new_first",
                    "last-name": "test_edit_new_last",
                    "image-url": "test_edit_new_image"
                }
            )

            self.assertEqual(resp_post.status_code, 302)

            self.assertEqual(resp_post.location, f"/users/{self.user_id}")

            resp_new = c.get(resp_post.location)
            html = resp_new.get_data(as_text=True)

            self.assertIn("test_edit_new_first", html)
            self.assertIn("test_edit_new_last", html)

    def test_create_new_user(self):
        """Tests route to create new user and redirect to users list page"""

        with self.client as c:
            resp_post = c.post(
                "/users/new",
                data = {
                    "first-name": "test_new_first_name",
                    "last-name": "test_new_last_name",
                    "image-url": "test_new_img_url"
                }
            )

            self.assertEqual(resp_post.status_code, 302)

            resp_redirect = c.get(resp_post.location)
            html = resp_redirect.get_data(as_text=True)

            self.assertIn("test_new_first_name", html)
            self.assertIn("test_new_last_name", html)

    def test_delete_user(self):
        """Tests route to delete a user and redirect"""

        with self.client as c:
            resp_post = c.post(
                f"/users/{self.user_id}/delete",
            )

        self.assertEqual(resp_post.status_code, 302)

        resp_new = c.get("/users")
        self.assertEqual(resp_new.status_code, 200)

        test_get = db.session.query(self.user_id)
        print("---------TESTGET-------------", test_get)


        # proposed tests to check that the deleted user's name is no longer shown
        html = resp_new.get_data(as_text=True)
        self.assertNotIn("test_first_one", html)
        self.assertNotIn("test_last_one", html)

#date time?

#what do we have to check? front end? backend? db? all three?
#do we even have to test everything? what is reserved for unit testing

#what's the diff with db.session.query vs Post.query or User.query
#which one is better etc
