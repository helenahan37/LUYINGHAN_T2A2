from init import db


class Plant(db.Model):
    __tablename__ = "plants"

    id = db.Column(db.Integer, primary_key=True)
    plant_name = db.Column(db.String(100), nullable=False, unique=True)
    genus = db.Column(db.String(100), nullable=False)
    watering = db.Column(db.String, default="Frequent")
    growth_rate = db.Column(db.String, default="High")

    # add relationship to GardenPlant model, when plant is deleted, all garden_plants will be deleted
    garden_plants = db.relationship(
        "GardenPlant",
        back_populates="plant", cascade="all, delete"
    )
