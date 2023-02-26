"""User model tests."""
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase
from sqlalchemy import exc

from models import db, User


os.environ['DATABASE_URL'] = "postgresql:///news"


# Now we can import app

from app import app
app.app_context().push()


db.drop_all()
db.create_all()


class UserModel(TestCase):
        """Test views for User."""

        def setUp(self):
            """Create test client, add sample data."""
            db.drop_all()
            db.create_all()

            u1 = User.signup(username="test1", email="email1@email.com", password="password")
            uid1 = 1111
            u1.id = uid1

            db.session.commit()

            u1 = User.query.get(uid1)

            self.u1 = u1
            self.uid1 = uid1
            self.client = app.test_client()

        def tearDown(self):
            res = super().tearDown()
            db.session.rollback()
            return res


        def test_user_model(self):
            """Does basic model work?"""

            u = User(
                email="test@test.com",
                username="testuser",
                password="HASHED_PASSWORD"
            )

            db.session.add(u)
            db.session.commit()

            # User should have no likes
            self.assertEqual(len(u.likes), 0)



        ####
        #
        # Signup Tests
        #
        ####
        def test_valid_signup(self):
            u_test = User.signup("testtesttest", "testtest@test.com", "password")
            uid = 99999
            u_test.id = uid
            db.session.commit()

            u_test = User.query.get(uid)
            self.assertIsNotNone(u_test)
            self.assertEqual(u_test.username, "testtesttest")
            self.assertEqual(u_test.email, "testtest@test.com")
            self.assertNotEqual(u_test.password, "password")
        
        ####
        #
        # Authentication Tests
        #
        ####
        def test_valid_authentication(self):
            u = User.authenticate(self.u1.username, "password")
            self.assertIsNotNone(u)
            self.assertEqual(u.id, self.uid1)
        
        def test_invalid_username(self):
            self.assertFalse(User.authenticate("badusername", "password"))

        def test_wrong_password(self):
            self.assertFalse(User.authenticate(self.u1.username, "badpassword"))




        




        

