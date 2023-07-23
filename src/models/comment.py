from init import db


class Comment(db.Model):
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text, nullable=False)
    comment_date = db.Column(db.Date)

    # relates to user and garden table
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    garden_id = db.Column(db.Integer, db.ForeignKey(
        'gardens.id'), nullable=False)

    # provide the sqlalchemy relationship instead of database
    # refers to User model comment field
    user = db.relationship(
        "User", back_populates="comments")  # user in comments
    # refers to Garden model comment field
    garden = db.relationship(
        "Garden", back_populates="comments")  # garden in comments
