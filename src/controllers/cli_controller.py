from flask import Blueprint
from init import db, bcrypt
from models.user import User
from models.garden import Garden
from models.plant import Plant
from models.comment import Comment
from models.garden_plant import GardenPlant
from datetime import date

db_commands = Blueprint("db", __name__)


# create tables
@db_commands.cli.command("create")
def create_db():
    db.create_all()
    print("Tables Created")


# drop tables
@db_commands.cli.command("drop")
def drop_db():
    db.drop_all()
    print("Tables dropped")


# seed tables
@db_commands.cli.command("seed")
def seed_db():
    users = [
        User(
            user_name="Admin1",
            email="admin@admin.com",
            password=bcrypt.generate_password_hash("admin123").decode("utf-8"),
            is_admin=True
        ),
        User(
            user_name="User1",
            email="user1@email.com",
            password=bcrypt.generate_password_hash("user1pw").decode("utf-8")
        ),
        User(
            user_name="User2",
            email="user2@email.com",
            password=bcrypt.generate_password_hash("user2pw").decode("utf-8")
        ),
    ]

    db.session.add_all(users)

    gardens = [
        Garden(
            garden_name="Garden1",
            description="This is garden1 description",
            creation_date=date.today(),
            user=users[1]
        ),
        Garden(
            garden_name="Garden2",
            description="This is garden2 description",
            creation_date=date.today(),
            user=users[2]
        ),
    ]
    db.session.add_all(gardens)

    plants = [
        Plant(
            plant_name="Cascade Maple",
            genus="Acer Japonicum",
            watering="Average",
            growth_rate="Low"
        ),
        Plant(
            plant_name="Fraser Fir",
            genus="Abies Fraseri",
            watering="Frequent",
            growth_rate="Moderate"
        ),
        Plant(
            plant_name="Sea Buckthorn",
            genus="Hippophae Rhamnoides",
            watering="Frequent",
            growth_rate="High"
        ),
        Plant(
            plant_name="Summer Mimosa",
            genus="Albizia Julibrissin",
            watering="Average",
            growth_rate="Moderate"
        ),
        Plant(
            plant_name="Ginkgo",
            genus="Ginkgo Biloba",
            watering="Frequent",
            growth_rate="Moderate"
        ),
        Plant(
            plant_name="Limelight Hydrangea",
            genus="Hydrangea Paniculata",
            watering="Frequent",
            growth_rate="High"
        ),
        Plant(
            plant_name="Tuliptree",
            genus="Liriodendron Tulipifera",
            watering="Average",
            growth_rate="High"
        ),
        Plant(
            plant_name="Marilyn Magnolia",
            genus="Magnolia",
            watering="Average",
            growth_rate="High"
        ),
        Plant(
            plant_name="Azalea",
            genus="Rhododendron",
            watering="Average",
            growth_rate="Low"
        ),
    ]
    db.session.add_all(plants)

    garden_plants = [
        GardenPlant(
            color="Green",
            position="North",
            size="Small",
            garden=gardens[0],
            plant=plants[3]
        ),
        GardenPlant(
            color="White",
            position="South",
            size="Large",
            garden=gardens[0],
            plant=plants[1]
        ),
        GardenPlant(
            color="Red",
            position="East",
            size="Medium",
            garden=gardens[1],
            plant=plants[4]
        ),
        GardenPlant(
            color="Rainbow",
            position="NorthWest",
            size="Large",
            garden=gardens[1],
            plant=plants[2]
        ),
        GardenPlant(
            color="Yellow",
            position="Center",
            size="Small",
            garden=gardens[1],
            plant=plants[2]
        ),
    ]

    db.session.add_all(garden_plants)

    comments = [
        Comment(
            message="This is comment1",
            comment_date=date.today(),
            user=users[1],
            garden=gardens[0]
        ),
        Comment(
            message="This is comment2",
            comment_date=date.today(),
            user=users[1],
            garden=gardens[0]
        ),
        Comment(
            message="This is comment3",
            comment_date=date.today(),
            user=users[2],
            garden=gardens[0]
        ),
        Comment(
            message="This is comment4",
            comment_date=date.today(),
            user=users[1],
            garden=gardens[1]
        ),
    ]
    db.session.add_all(comments)

    db.session.commit()

    print("Tables seeded")
