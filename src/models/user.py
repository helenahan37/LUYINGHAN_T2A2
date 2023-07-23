from init import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(200), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)
    # set default admin value to false
    is_admin = db.Column(db.Boolean, default=False)

    # add relationship to garden，refers to Garden model -user field, when user is deleted, all gardens will be deleted
    gardens = db.relationship(
        "Garden", back_populates="user", cascade="all, delete")

    # add relationship to comment, when user is deleted, all comments will be deleted
    comments = db.relationship(
        "Comment", back_populates="user", cascade="all, delete")
