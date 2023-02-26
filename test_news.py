"""User model tests."""
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase
from sqlalchemy import exc
from flask import g

from models import db, User, News, Author, Source, Category, User_Author, User_Category, User_Source
from author_functions import add_user_author
from sources_functions import add_source
from category import add_user_category
from user_functions import like
from api_test import search



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


        def test_search(self):
            """Does search work?"""

            search('Pepper')
            search('Pepper')
            # If the same item is searched twice, it should only be added to database once
            cats = Category.query.filter(Category.name == 'Pepper').all()
            self.assertEqual(len(cats), 1)
            authors = Author.query.all()
            sources = Source.query.all()

            # When the search function runs, the authors and source db should be populated 
            self.assertGreaterEqual(len(authors),1)
            self.assertGreaterEqual(len(sources),1)

            # No duplications of authors or sources in the database
            self.assertEqual(len(authors),len(set(authors)))
            self.assertEqual(len(sources),len(set(sources)))



        def test_user_author(self):
            """Testing Adding Author to Favorites"""

            u = User(
                email="test@test.com",
                username="testuser",
                password="HASHED_PASSWORD"
            )

            a = Author(name = 'John')

            db.session.add(u)
            db.session.add(a)
            db.session.commit()

            add_user_author(u.id,a.id)
            db.session.commit()

            ua = User_Author.query.get_or_404(1)

            self.assertEqual(ua.author_id, a.id)
            self.assertEqual(ua.user_id, u.id)


        def test_user_source(self):
            """Testing Adding Sources to Favorite"""

            u = User(
                email="test@test.com",
                username="testuser",
                password="HASHED_PASSWORD"
            )

            s = Source(name = 'ESPN')

            db.session.add(u)
            db.session.add(s)
            db.session.commit()

            add_source(u.id,s.id)

            us = User_Source.query.get_or_404(1)

            self.assertEqual(us.source_id, s.id)
            self.assertEqual(us.user_id, u.id)


        def test_user_category(self):
            """Testing Adding Category to Favorite"""

            u = User(
                email="test@test.com",
                username="testuser",
                password="HASHED_PASSWORD"
            )

            c = Category(name = 'Food')

            db.session.add(u)
            db.session.add(c)
            db.session.commit()

            g.user = User.query.get(1)


            add_user_category(g,c.id)
            db.session.commit()

            uc = User_Category.query.get_or_404(1)

            self.assertEqual(uc.category_id, c.id)
            self.assertEqual(uc.user_id, u.id)

        def test_user_like(self):
            """Testing Like"""

            u = User(
                email="test@test.com",
                username="testuser",
                password="HASHED_PASSWORD"
            )
            db.session.add(u)
            db.session.commit()

            g.user = User.query.get(1)
            search('Food')
            self.assertEqual(len(g.user.likes),0)

            news = News.query.all()

            like(g,news[0].id)
            self.assertEqual(len(g.user.likes),1)
            self.assertEqual(g.user.likes[0].title,news[0].title)










        


        


        




        




        

