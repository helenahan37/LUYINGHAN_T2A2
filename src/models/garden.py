from init import db


class Garden(db.Model):
    __tablename__ = "gardens"

    id = db.Column(db.Integer, primary_key=True)
    garden_name = db.Column(db.String(200), nullable=False, unique=True)
    creation_date = db.Column(db.Date)
    description = db.Column(db.Text)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # refer to User model -gardens field
    user = db.relationship("User", back_populates="gardens")

    # refer to GardenPlant model -garden field, when garden is deleted, delete all garden_plants related to that garden
    garden_plants = db.relationship(
        "GardenPlant",
        back_populates="garden", cascade="all, delete")

    # refer to comment model -garden field, when garden is deleted, delete all comments related to that garden
    comments = db.relationship(
        "Comment", back_populates="garden", cascade="all, delete")
