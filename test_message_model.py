"""Message model tests."""


import os
from unittest import TestCase
from sqlalchemy import exc
from models import db, User, Message, Follows, Likes

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"
from app import app
db.create_all()

class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""
        db.drop_all()
        db.create_all()

        self.uid = 99999
        u = User.signup("tester", "tester@test.com", "password", None)
        
        u.id = self.uid
        db.session.commit()

        self.u = User.query.get(self.uid)
        self.client = app.test_client()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_message_model(self):
        """Does basic model work?"""
        
        message = Message(text="test message", user_id=self.uid)

        db.session.add(message)
        db.session.commit()
        
        self.assertEqual(len(self.u.messages), 1)
        self.assertEqual(self.u.messages[0].text, "test message")

    def test_message_likes(self):
        message1 = Message(
            text="test message",
            user_id=self.uid
        )

        message3 = Message(
            text="second test message",
            user_id=self.uid 
        )

        uid = 11111
        u = User.signup("tester2", "tester2@test.com", "password", None)
        u.id = uid
        db.session.add_all([message1, message3, u])
        db.session.commit()

        u.likes.append(message1)

        db.session.commit()

        likes = Likes.query.filter(Likes.user_id == uid).all()
        self.assertEqual(len(likes), 1)
        self.assertEqual(likes[0].message_id, message1.id)


        