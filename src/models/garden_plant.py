from init import db


class GardenPlant(db.Model):
    __tablename__ = "garden_plants"

    id = db.Column(db.Integer, primary_key=True)
    color = db.Column(db.String(), default="Green")
    position = db.Column(db.String(), nullable=False)
    size = db.Column(db.String(), default="Medium")

    garden_id = db.Column(db.Integer, db.ForeignKey(
        "gardens.id"), nullable=False)
    plant_id = db.Column(db.Integer, db.ForeignKey(
        "plants.id"), nullable=False)

    # extra attributes, garden and plant refers to Garden and Plant model
    garden = db.relationship(
        "Garden", back_populates="garden_plants")
    plant = db.relationship(
        "Plant", back_populates="garden_plants")
