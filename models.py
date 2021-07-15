"""SQLAlchemy models for Badger Group Reminder App"""

from datetime import datetime
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()

##Connect to database
def connect_db(app):
    """Connect this database to provided Flask app.
    You should call this in your Flask app.
    """

    db.app = app
    db.init_app(app)


##Models
class User(db.Model):
    """User model"""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.Text, nullable=False, unique=True)

    phone_number = db.Column(db.Text, nullable=False, unique=True)

    password = db.Column(db.Text, nullable=False)

    messages = db.relationship('Message')


    ##Methods for User class
    def __repr__(self):
            return f"<User #{self.id}: {self.username}, {self.phone_number}>"

    @classmethod
    def signup(cls, username, email, password, image_url):
        """Sign up user.
        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            email=email,
            password=hashed_pwd,
            image_url=image_url,
        )

        db.session.add(user)
        return user

    @classmethod
    def signup(cls, username, phone_number, password):
        """Sign up user.
        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            phone_number=phone_number,
            password=hashed_pwd,
        )

        db.session.add(user)
        return user
    
    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.
        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.
        If can't find matching user (or if password is wrong), returns False.
        """

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False

class Message(db.Model):
    """Message model"""

    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='cascade'))

    text = db.Column(db.String(300), nullable=False)

    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

    queued_time = db.Column(db.DateTime, nullable=False)

    user = db.relationship('User')

    queued = db.Column(db.Boolean, nullable=False, default=True)


class Badger(db.Model):
    """Relationship between message sender recipient model"""
    
    __tablename__ = 'badgers'

    id = db.Column(db.Integer, primary_key=True)

    message_id = db.Column(db.Integer, db.ForeignKey('messages.id', ondelete='cascade'))

    sender_user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='cascade'), primary_key=True)
    
    recipient_number = db.Column(db.String, nullable=False)

class PhoneNum(db.Model):
    """Phone Numbers"""

    __tablename_ = 'phone_numbers'

    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, nullable=False)
    cc = db.Column(db.Integer, nullable=False)


#class Queued_Message(db.Model):
#    """Queue model"""
#
#    __tablename__ = 'queued_messages'
#
#    id = db.Column(db.Integer, primary_key=True)
#
#    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='cascade'))
#
#    message_id = db.Column(db.Integer, db.ForeignKey('messages.id', ondelete='cascade'))
#
#    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())



##In Production##
#class Verified_Number(db.Model):
#    """Phone Number model"""
#
#    __tablename__ = 'verified_numbers'
#
#    id = db.Column(db.Integer, primary_key=True)
#
#    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='cascade'))
#
#    phone_number = db.Column(db.Text, nullable=False, unique=True)

