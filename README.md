# T2A2 - API Webserver Project - Virtual Garden API

## Installation Instructions:

1. Clone the repository from GitHub

   ```
   git@github.com:helenahan37/LUYINGHAN_T2A2.git
   ```

2. Insure you have PostgreSQL installed and running on your terminal:

   ```
   open the terminal and run `psql`
   ```

3. Create a database called 'virtual_garden_db' in PostgreSQL

   ```
   CREATE DATABASE virtual_garden_db;
   ```

4. Create a role and set the password:

   ```
   CREATE USER vg_dev WITH PASSWORD '123456';
   ```

5. Grant all privileges on the database to the role:

   ```
   GRANT ALL PRIVILEGES ON DATABASE virtual_garden_db TO vg_dev;
   ```

6. Grant all privileges on the schema to the role

   ```
   GRANT ALL ON SCHEMA public TO vg_dev;
   ```

7. cd into 'src' folder and create a virtual environment and activate it:

   ```
   python3 -m venv .venv && source .venv/bin/activate
   ```

8. Rename the '.env.sample' file to '.env' file and add the following lines:

   ```
   DATABASE_URL="postgresql+psycopg2://vg_dev:123456@localhost:5432/virtual_garden_db"
   JWT_SECRET_KEY="secret"
   ```

9. Install the required packages:

   ```
   pip3 install -r requirements.txt
   ```

10. Run the following command to reset the database tables:

    ```
    flask db drop && flask db create && flask db seed
    ```

11. Run the application:

    ```
    flask run
    ```

## R1. Identification of the problem you are trying to solve by building this particular app.

The problem being addressed by building this particular app is the time and effort constraints that modern society poses on garden design and maintenance. Many individuals find it difficult to allocate enough time to plan and manage their real gardens effectively. Garden design requires careful consideration of plant selection, arrangement, and maintenance, which can be daunting and time-consuming for busy individuals. Additionally, lack of experience and knowledge about plants' attributes may lead to suboptimal garden designs and unsatisfactory outcomes.

To tackle this problem, the virtual garden API provides a solution that allows users to design and experiment with their dream gardens in a virtual environment. By offering a wide selection of plants and customization options, users can freely explore their creativity without the limitations of time and physical space. The virtual garden also serves as a valuable learning platform where users can gain insights into plant attributes, growth cycles, and watering requirements, empowering them to make informed decisions when managing their real gardens.

---

## R2. Why is it a problem that needs solving?

The need to solve this problem arises due to the increasing demands and constraints of modern life. Many people lead busy lifestyles, juggling work, family, and various responsibilities, leaving limited time and energy for hobbies like gardening. As a result, individuals may neglect their gardens or miss out on the joy of creating and tending to their green spaces. That's why I came up with this API, inspired by the virtual home design games I played during my childhood.

The virtual garden API addresses this problem by offering a convenient and accessible way for users to engage in garden design and cultivation without the need for physical labor. By providing a virtual environment, users can explore their passion for gardening and experiment with various design ideas, regardless of their busy schedules. The educational aspect of the API also empowers users to become more knowledgeable gardeners, making their real gardening experiences more rewarding and successful.

---

## R3. Why have you chosen this database system. What are the drawbacks compared to others?

I am utilizing PostgreSQL as my relational database system. PostgreSQL, often referred to as "Postgres," employs Structured Query Language (SQL) for data access and is highly suitable for integration with other tools. Its ability to handle data integrity and complex operations makes it an excellent choice for my needs.

One of the primary reasons I chose PostgreSQL is its ease of use and efficient data management in a relational database. It offers a wide range of key features, including high availability, fault tolerance, and compatibility with various data types. Its adherence to ACID (Atomicity, Consistency, Isolation, Durability) compliance ensures data integrity and consistency[^1].

Additionally, I chose PostgreSQL as my database because my program uses JSON data format. PostgreSQL provides extensive support and advantages for JSON data. It supports native JSON data type, allowing direct storage of JSON data in the database without the need for additional conversions or processing. This makes storing and retrieving JSON data more efficient and convenient.

PostgreSQL allows querying and indexing of JSON data, enabling searches and filtering based on various JSON fields. This empowers me to leverage the database's functionalities to optimize the query performance of JSON data[^2].

Moreover, PostgreSQL supports constraints and validation for JSON data, ensuring that the stored data adheres to the expected format and structure. This contributes to maintaining data integrity and consistency.

By choosing PostgreSQL, I can effectively manage and interact with JSON data, taking advantage of its native support and performance optimizations to enhance the functionality and reliability of my application.

##### Drawbacks[^3]:

PostgreSQL, being a community-driven open-source database management system, lacks centralized ownership, which has led to challenges in gaining widespread recognition despite its comprehensive features and comparability to other DBMS systems.

When aiming for speed improvements, PostgreSQL may require more effort than MySQL, as its focus lies on maintaining compatibility with existing systems.

While MySQL enjoys extensive support from many open-source applications, the same level of support may not always be available for PostgreSQL.

In performance metrics, PostgreSQL tends to be slightly slower than MySQL.

---

## R4. Identify and discuss the key functionalities and benefits of an ORM

#### Key functionalities of an ORM[^4]:

Abstraction of Database Interaction: ORM allows developers to interact with the database using their preferred programming language, abstracting away the need to write raw SQL queries.

Database Independence: With ORM, applications become independent of the underlying database management system, enabling easier migration to different databases.

Data Validation and Type Conversion: ORM provides mechanisms for data validation and type conversion, ensuring data integrity and consistency.

Relationship Management: ORM simplifies handling database relationships, representing them as object associations.

Code Reusability: ORM promotes code reusability, allowing developers to create generic database access methods.

#### Benefits of using an ORM[^5]:

Language Familiarity: Developers can use the programming language they are comfortable with, making development faster and more efficient.

Reduced Learning Curve: Developers do not need to learn different SQL syntaxes for each database, saving time and effort.

Simplified Data Manipulation: ORM allows easy manipulation of data, enabling developers to focus on code optimization and performance improvement.

Robust and Secure Connections: ORM handles necessary configurations and promotes secure application development with fewer coding interventions.

Wide Range of Choices: There are numerous ORM libraries available for different programming languages, providing flexibility in choosing the right one for specific business needs.

---

## R5. Document all endpoints for your API

### Welcome Page

- HTTP request: GET
- URL: localhost:8080
- Authentication required: No
- Required data: None
- Expected response data

![welcome](/docs/welcome.png)

### Auth Routes

#### CREATE a new user

- HTTP request: POST
- URL: localhost:8080/auth/register
- Authentication required: No
- Required data: user_name, email and password
- Expected response data

  - failed to provide required data
    ![register](/docs/register.png)
  - invalid input format
    ![register](/docs/register%20invalid%20input.png)
  - successfully registered
    ![register](/docs/success%20registered.png)

#### login as a registered user

- HTTP request: POST
- URL: localhost:8080/auth/login
- Authentication required: email and password
- Required data: email and password
- Expected response data

  - failed to provide required data
    ![login](/docs/login.png)
  - incorrect email or password
    ![login](/docs/incorrect%20login.png)
  - successfully logged in
    ![login](/docs/sucesslogin.png)

#### READ all users

###### only admin can get all users

- HTTP request: GET
- URL: localhost:8080/auth/user
- Authentication required: JWT token
- Required data: None
- Expected response data
  - failed to provide token
    ![login](/docs/login-failed_provide_jwt.png)
  - failed to provide admin token
    ![login](/docs/login_forbidden.png)
  - admin successfully logged in
    ![login](/docs/admin_login_success.png)

#### READ one users

###### only admin can get user by user_id

- HTTP request: GET
- URL: localhost:8080/auth/user/user_id
- Authentication required: JWT token
- Required data: user_id
- Expected response data
  - failed to provide token
    ![login](/docs/user-get-nojwt.png)
  - failed to provide admin token
    ![login](/docs/user-get-noadmintoken.png)
  - user_id not found
    ![login](/docs/user-get-useridnotfound.png)
  - user successfully found
    ![login](/docs/user-get-success.png)

#### UPDATE account info

###### only account owner and admin can update account info, only current admin can change is_admin status

- HTTP request: PUT or PATCH
- URL: localhost:8080/auth/user/user_id
- Authentication required: JWT token
- Required data: user_id, the account info you want to update
- Expected response data
  - failed to provide token
    ![login](/docs/login_failed_provide_token.png)
  - user_id not found
    ![login](/docs/login_useridnotfound.png)
  - login user is not the account owner or admin
    ![login](/docs/login_usernotowner.png)
  - user_name and email must be unique
    ![login](/docs/login_unique.png)
  - login user cannot change is_admin status
    ![login](/docs/login_failedchangeadmin.png)
  - account info successfully updated
    ![login](/docs/login_updatesuccess.png)
  - admin can change is_admin status
    ![login](/docs/login_adminupdate.png)

#### DELETE account

###### only account owner and admin can delete account

- HTTP request: DELETE
- URL: localhost:8080/auth/user/user_id
- Authentication required: JWT token
- Required data: user_id
- Expected response data
  - failed to provide token
    ![login](/docs/login-delete-failedprovidetoken.png)
  - user_id not found
    ![login](/docs/login-delete-idnotfound.png)
  - login user is not the account owner or admin
    ![login](/docs/login-delete-notaccountowner.png)
  - account successfully deleted
    ![login](/docs/login-delete-sucess.png)

## Garden Routes

#### EAD all gardens

###### any visitors can access

- HTTP request: GET
- URL: localhost:8080/garden
- Authentication required: No
- Required data: None
- Expected response data
  ![login](/docs/garden-getallgardens.png)

#### READ a garden by garden_id

###### any visitors can access

- HTTP request: GET
- URL: localhost:8080/garden/garden_id
- Authentication required: None
- Required data: garden_id
- Expected response data
  - garden_id successfully found
    ![login](/docs/garden-getallgardenbyid.png)
  - garden_id not found
    ![login](/docs/garden-idnotfound.png)

#### CREATE a new garden

###### only registered user can access, garden_name must be unique

- HTTP request: POST
- URL: localhost:8080/garden
- Authentication required: JWT token
- Required data: garden_name
- Expected response data

  - failed to provide token
    ![login](/docs/garden-post-missingjwt.png)
  - failed to provide garden_name
    ![login](/docs/garden-post-failedprovidename.png)
  - garden_name already exists
    ![login](/docs/garden-post-nameexists.png)
  - invalid input
    ![login](/docs/garden-post-invalidinput.png)
  - garden successfully created
    ![login](/docs/garden-post-success.png)

#### UPDATE garden

###### only garden owner or admin can update, garden_name must be unique

- HTTP request: PUT or PATCH
- URL: localhost:8080/garden/garden_id
- Authentication required: JWT token
- Required data: garden_id, garden info you want to update
- Expected response data
  - failed to provide token
    ![login](/docs/garden-update-failedprovidejwt.png)
  - garden_id not found
    ![login](/docs/garden-update-idnotfound.png)
  - login user is not the garden owner or admin
    ![login](/docs/garden-update-notowner.png)
  - garden_name already exists
    ![login](/docs/garden-update-nameexists.png)
  - garden successfully updated
    ![login](/docs/garden-post-updatesuccess.png)

#### DELETE garden

###### only garden owner or admin can delete

- HTTP request: DELETE
- URL: localhost:8080/garden/garden_id
- Authentication required: JWT token
- Required data: garden_id
- Expected response data
  - failed to provide token
    ![login](/docs/garden-delete-failedprovidejwt.png)
  - garden_id not found
    ![login](/docs/garden-delete-idnotfound.png)
  - login user is not the garden owner or admin
    ![login](/docs/garden-delete-notowner.png)
  - garden successfully deleted
    ![login](/docs/garden-delete-success.png)

### Plants Routes

#### READ all plants

###### any visitors can access

- HTTP request: GET
- URL: localhost:8080/plant
- Authentication required: No
- Required data: None
- Expected response data
  ![login](/docs/plant-get-allplants.png)

#### READ plant by id

###### any visitors can access

- HTTP request: GET
- URL: localhost:8080/plant/plant_id
- Authentication required: No
- Required data: plant_id
- Expected response data
  - plant_id not found
    ![login](/docs/plant-get-idnotfound.png)
  - plant_id successfully found
    ![login](/docs/plants-get-idfound.png)

#### CREATE new plant

###### only admin can access, plant_name must be unique

- HTTP request: GET
- URL: localhost:8080/plant/plant_id
- Authentication required: JWT token
- Required data: plant_id, plant name, genus
- Expected response data
  - failed to provide token
    ![login](/docs/plant-post-nojwt.png)
  - login user not admin
    ![login](/docs/plant-post-notadmin.png)
  - plant name not provided
    ![login](/docs/plant-post-notprovidename.png)
  - plant name already exists
    ![login](/docs/plant-post-nameexists.png)
  - plant successfully created
    ![login](/docs/plant-post-success.png)

#### UPDATE plant

###### only admin can access, plant_name must be unique

- HTTP request: PUT or PATCH
- URL: localhost:8080/plant/plant_id
- Authentication required: JWT token
- Required data: plant_id, plant info you want to update
- Expected response data
  - failed to provide token
    ![login](/docs/plant-update-nojwt.png)
  - login user not admin
    ![login](/docs/plant-update-notadmin.png)
  - plant id not find
    ![login](/docs/plant-update-notfoundid.png)
  - plant name already exists
    ![login](/docs/plant-update-nameexists.png)
  - invalid input
    ![login](/docs/plant-update-invalidinput.png)
  - plant successfully updated
    ![login](/docs/plant-post-success.png)

#### DELETE plant

###### only admin can access

- HTTP request: DELETE
- URL: localhost:8080/plant/plant_id
- Authentication required: JWT token
- Required data: plant_id
- Expected response data
  - failed to provide token
    ![login](/docs/plant-delete-nojwt.png)
  - login user not admin
    ![login](/docs/plant-delete-notadmin.png)
  - plant id not find
    ![login](/docs/plant-delete-notfoundid.png)
  - plant successfully deleted
    ![login](/docs/plant-delete-success.png)

### garden_plants Routes

#### READ garden_plants by garden_id

###### all visitors can get garden_plants from any garden

- HTTP request: GET
- URL: localhost:8080/garden/garden_id/garden_plants
- Authentication required: No
- Required data: garden_id
- Expected response data
  - garden_id not found
    ![login](/docs/gardenplants-get-idnotfound.png)
  - garden_id successfully found but no garden_plants in this garden
    ![login](/docs/gardenplants-get-noplants.png)
  - garden_plants successfully found
    ![login](/docs/gardenplants-get-success.png)

#### CREATE garden_plants by garden_id and plant_id

###### only garden owner and admin can create garden_plant, garden_plant position must be unique in a garden

- HTTP request: POST
- URL: localhost:8080/garden/garden_id/plant/plant_id
- Authentication required: JWT token
- Required data: garden_id, plant_id, position
- Expected response data
  - failed to provide token
    ![login](/docs/gp-post-nojwt.png)
  - garden_id not found
    ![login](/docs/gp-post-gardenidnotfound.png)
  - not garden owner or admin
    ![login](/docs/gp-post-notowner.png)
  - plant_id not found
    ![login](/docs/gp-post-plantidnotfound.png)
  - garden_plants successfully created
    ![login](/docs/gp-post-success.png)
  - invalid input
    ![login](/docs/gp-post-invalidinput1.png)
    ![login](/docs/gp-post-invalidinput2.png)
  - position already exists
    ![login](/docs/gp-post-positionexists.png)

#### UPDATE garden_plants by garden_id and garden_plant_id

###### only garden owner or admin can update garden_plant, position must be unique in a garden

- HTTP request: PUT or PATCH
- URL: localhost:8080/garden/garden_id/garden_plant_id
- Authentication required: JWT token
- Required data: garden_id, garden_plant_id, the garden_plant info you want to update
- Expected response data
  - failed to provide token
    ![login](/docs/gp-update-nojwt.png)
  - garden_id not found
    ![login](/docs/gp-update-gardenidnotfound.png)
  - garden_plant_id not found
    ![login](/docs/gp-update-gardenplantidnotfound.png)
  - invalid input
    ![login](/docs/gp-update-invalidinput1.png)
  - updated position already exists
    ![login](/docs/gp-update-positionexists.png)
  - not garden owner or admin
    ![login](/docs/gp-update-notowner.png)
  - garden_plants successfully updated
    ![login](/docs/gp-update-success.png)

#### DELETE garden_plants by garden_id and garden_plant_id

###### only garden owner and admin can delete garden_plant

- HTTP request: DELETE
- URL: localhost:8080/garden/garden_id/garden_plant_id
- Authentication required: JWT token
- Required data: garden_id, garden_plant_id
- Expected response data
  - failed to provide token
    ![login](/docs/gp-delete-nojwt.png)
  - garden_id not found
    ![login](/docs/gp-delete-gardenidnotfound.png)
  - garden_plant_id not found
    ![login](/docs/gp-delete-gardenplantidnotfound.png)
  - not garden owner or admin
    ![login](/docs/gp-delete-notowner.png)
  - garden_plant successfully deleted
    ![login](/docs/gp-delete-success.png)

### Comments Routes

#### POST a new comment by garden_id

###### only login user can post a new comment by garden id

- HTTP request: POST
- URL: localhost:8080/garden/garden_id/comment
- Authentication required: JWT token
- Required data: garden_id, message
- Expected response data
  - failed to provide token
    ![login](/docs/comment-post-nojwt.png)
  - garden_id not found
    ![login](/docs/comment-post-gardenidnotfound.png)
  - invalid input
    ![login](/docs/comment-post-invalidinput.png)
    ![login](/docs/comment-post-invalidinput1.png)
  - comment successfully posted
    ![login](/docs/comment-post-success.png)

#### READ all comments by garden_id

###### only login user can read all comments by garden id

- HTTP request: GET
- URL: localhost:8080/garden/garden_id/comment
- Authentication required: JWT token
- Required data: garden_id
- Expected response data
  - failed to provide token
    ![login](/docs/comment-get-nojwt.png)
  - garden_id not found
    ![login](/docs/comment-get-gardenidnotfound.png)
  - no comments found
    ![login](/docs/comment-get-nocomment.png)
  - comments successfully found
    ![login](/docs/comment-get-success.png)

#### UPDATE comment by garden_id and comment_id

###### only login comment owner or admin can update comment by comment id

- HTTP request: PUT or PATCH
- URL: localhost:8080/garden/garden_id/comment/comment_id
- Authentication required: JWT token
- Required data: garden_id, comment_id, message
- Expected response data

  - failed to provide token
    ![login](/docs/comment-update-nojwt.png)
  - garden_id not found
    ![login](/docs/comment-update-gardenidnotfound.png)
  - comment_id not found in garden_id
    ![login](/docs/comment-update-commentidnotfound.png)
  - not comment owner or admin
    ![login](/docs/comment-update-notowner.png)
  - invalid input
    ![login](/docs/comment-update-invalidinput.png)
    ![login](/docs/comment-update-invalidinput1.png)
  - comment successfully updated
    ![login](/docs/comment-update-success.png)

#### DELETE comment by garden_id and comment_id

###### only login comment owner or admin can delete comment by comment id

- HTTP request: DELETE
- URL: localhost:8080/garden/garden_id/comment/comment_id
- Authentication required: JWT token
- Required data: garden_id, comment_id
- Expected response data
  - failed to provide token
    ![login](/docs/comment-delete-nojwt.png)
  - garden_id not found
    ![login](/docs/comment-delete-gardenidnotfound.png)
  - comment_id not found in garden_id
    ![login](/docs/comment-delete-commentidnotfound.png)
  - not comment owner or admin
    ![login](/docs/comment-delete-notowner.png)
  - comment successfully deleted
    ![login](/docs/comment-delete-success.png)

---

## R6. An ERD for your app

![ERD](/docs/ERD.png)

## R7. Detail any third party services that your app will use

- **Flask**: Flask is a micro web framework written in Python. It is used to build web applications and APIs. I am using Flask to build my API.
- **SQLAlchemy**: SQLAlchemy is an open-source SQL toolkit and object-relational mapper for Python. It designed for efficient and high-performing database access. I am using SQLAlchemy to interact with my PostgreSQL database.
- **Marshmallow**: Marshmallow is an ORM/ODM/framework-agnostic library for converting complex datatypes to and from native Python datatypes. I am using Marshmallow to serialize and deserialize my SQLAlchemy models.
- **Flask-Bcrypt**: Flask-Bcrypt is a Flask extension that provides bcrypt hashing utilities for my application. I am using Flask-Bcrypt to hash passwords for user authentication.
- **Flask-JWT-Extended**: Flask-JWT-Extended is a Flask extension that provides JSON Web Token (JWT) support for my application. I am using Flask-JWT-Extended to generate and verify JWT tokens for user authentication.
- **PostgreSQL**: PostgreSQL is a free and open-source relational database management system. I am using PostgreSQL to store and manage my application's data.
- **psycopg2-binary**: psycopg2-binary is a PostgreSQL database adapter for Python. I am using psycopg2-binary to connect my application to PostgreSQL.
- **Werkzeug**: Werkzeug is a comprehensive WSGI web application library. I am using Werkzeug to handle HTTP requests and responses for my application.

## R8. Describe your projects models in terms of the relationships they have with each other

In relational databases, relationships define how different tables are connected to each other. There are several types of relationships, such as one-to-one, one-to-many, and many-to-many. These relationships help establish the connections between records in different tables and enable efficient data retrieval and manipulation.

In Flask, SQLAlchemy is a widely used Object-Relational Mapping (ORM) library. It allows users to define their database models using Python classes and handles the communication between their Python code and the underlying database. SQLAlchemy also supports defining relationships between these models, which are then translated into the corresponding database relationships.

My application has five models: User, Garden, Plant, GardenPlant and comment. The relationships between these models are as follows:

**User Model:**

```python
class User(db.Model):
 __tablename__ = 'users'

 id = db.Column(db.Integer, primary_key=True)
 user_name = db.Column(db.String(100), nullable=False, unique=True)
 email = db.Column(db.String(200), nullable=False, unique=True)
 password = db.Column(db.String(), nullable=False)
 is_admin = db.Column(db.Boolean, default=False)

 gardens = db.relationship(
     "Garden", back_populates="user", cascade="all, delete")

 comments = db.relationship(
     "Comment", back_populates="user", cascade="all, delete")
```

In this model, the gardens attribute establishes a one-to-many relationship with the Garden model. The "back_populates" argument is used to specify the corresponding attribute in the Garden model, which is "user." This allows easy bidirectional navigation between User and Garden objects.

Similarly, the comments attribute establishes another one-to-many relationship with the Comment model, with the "back_populates" argument set to "user."

When users are deleted, the "cascade" argument ensures that all associated gardens and comments are also deleted.

**Plant Model:**

```python
class Plant(db.Model):
    __tablename__ = "plants"

    id = db.Column(db.Integer, primary_key=True)
    plant_name = db.Column(db.String(100), nullable=False, unique=True)
    genus = db.Column(db.String(100), nullable=False)
    watering = db.Column(db.String, default="Frequent")
    growth_rate = db.Column(db.String, default="High")

    garden_plants = db.relationship(
        "GardenPlant",
        back_populates="plant", cascade="all, delete"
    )
```

The garden_plants attribute create a relationship in the Plant model with the GardenPlant model. Specifically, it establishes a one-to-many relationship, allowing a Plant object to have multiple GardenPlant objects, while each GardenPlant object belongs to only one Plant object. The "back_populates" specifies the name of the attribute in the GardenPlant model that establishes the reverse relationship with the Plant model.

When plants are deleted, the "cascade" argument ensures that all associated garden_plants are also deleted.

**Garden Model:**

```python
class Garden(db.Model):
    __tablename__ = "gardens"

    id = db.Column(db.Integer, primary_key=True)
    garden_name = db.Column(db.String(200), nullable=False, unique=True)
    creation_date = db.Column(db.Date)
    description = db.Column(db.Text)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    user = db.relationship("User", back_populates="gardens")

    garden_plants = db.relationship(
        "GardenPlant",
        back_populates="garden", cascade="all, delete")

    comments = db.relationship(
        "Comment", back_populates="garden", cascade="all, delete")
```

In this model, the user attribute establishes a many-to-one relationship with the User model. The "back_populates" argument points to the corresponding attribute in the User model. Every garden belongs to a single user.

The garden_plants attribute defines a one-to-many relationship with the GardenPlant model, with the "back_populates" argument set to "garden."

Similarly, the comments attribute establishes another one-to-many relationship with the Comment model, with the "back_populates" argument set to "garden."

When gardens are deleted, the "cascade" argument ensures that all associated garden_plants and comments are also deleted.

**GardenPlant Model:**

```python

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

    garden = db.relationship(
        "Garden", back_populates="garden_plants")
    plant = db.relationship(
        "Plant", back_populates="garden_plants")
```

The garden attribute establishes a many-to-one relationship with the Garden model, with the "back_populates" argument set to "garden_plants." Every garden_plant belongs to a single garden.
Similarly, the plant attribute establishes a many-to-one relationship with the Plant model, with the "back_populates" argument set to "garden_plants." Every garden_plant belongs to a single plant.

**Comment Model:**

```python
class Comment(db.Model):
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text, nullable=False)
    comment_date = db.Column(db.Date)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    garden_id = db.Column(db.Integer, db.ForeignKey(
        'gardens.id'), nullable=False)

    user = db.relationship(
        "User", back_populates="comments")

    garden = db.relationship(
        "Garden", back_populates="comments")

```

The user attribute establishes a many-to-one relationship with the User model, with the "back_populates" argument set to "comments." Every comment belongs to a single user. Similarly, the garden attribute establishes a many-to-one relationship with the Garden model, with the "back_populates" argument set to "comments." Every comment belongs to a single garden.

## R9. Discuss the database relations to be implemented in your application

In my application, I have implemented the following database relationships:

**One-to-many relationship between User and Garden models:**

Each User can have multiple Gardens, but each Garden belongs to only one User. This is represented by the user_id as a foreign key in the Garden model, referencing the primary key id in the User model.

**One-to-many relationship between User and Comment models:**

Each User can have multiple Comments, but each Comment belongs to only one User. This is represented by the user_id as a foreign key in the Comment model, referencing the primary key id in the User model.

**One-to-many relationship between Comment and Garden models:**

Each Garden can have multiple Comments, but each Comment belongs to only one Garden. This is represented by the garden_id as a foreign key in the Comment model, referencing the primary key id in the Garden model.

**Many-to-many relationship between User and Garden models through the Comment model (Join table):**

A Comment acts as a join table between User and Garden models, establishing a many-to-many relationship.
A User can be associated with multiple Gardens through their comments, and a Garden can be associated with multiple Users through their comments.
This is achieved by having user_id and garden_id as foreign keys in the Comment model, referencing the primary keys in the User and Garden models, respectively.

**One-to-many relationship between Garden and GardenPlant models:**

Each Garden can have multiple GardenPlants, but each GardenPlant belongs to only one Garden. This is represented by the garden_id as a foreign key in the GardenPlant model, referencing the primary key id in the Garden model.

**One-to-many relationship between Plant and GardenPlant models:**

Each Plant can have multiple GardenPlants, but each GardenPlant belongs to only one Plant. This is represented by the plant_id as a foreign key in the GardenPlant model, referencing the primary key id in the Plant model.

**Many-to-many relationship between Garden and Plant models through the GardenPlant model (Join table):**

The GardenPlant model acts as a join table between Garden and Plant models, establishing a many-to-many relationship.

A Garden can be associated with multiple Plants through the GardenPlants, and a Plant can be associated with multiple Gardens through the GardenPlants.
This is achieved by having garden_id and plant_id as foreign keys in the GardenPlant model, referencing the primary keys in the Garden and Plant models, respectively.

**User Model:**

In the User model, the user_name and email fields are required to be unique, ensuring that no two users can have the same user_name or email in the database. Fields formats are enforced through validation rules specified in the schema.

To maintain data integrity, the is_admin field is set to False by default when a user is registered. This design prevents ordinary users from changing their is_admin status and gaining administrative privileges.

During user registration, the password is securely hashed using bcrypt, ensuring that passwords are stored securely in the database.

For user authentication, user needs to verify the provided email and password combination. This method ensures that the entered credentials match the hashed password stored in the database, allowing authenticated users to access the system.

Upon successful login, the user receives a JWT (JSON Web Token) that serves as an authentication token.

**Garden Model:**

In the Garden model, the garden_name field is required to be unique, ensuring that no two gardens can have the same garden_name in the database. Fields format is enforced through validation rules specified in the schema. Creation_date is set to the current date and description is set to null if not provided.

**Plant Model:**

In the Plant model, the plant_name field is required to be unique and cannot be null, ensuring that no two plants can have the same plant_name in the database. Fields format is enforced through validation rules specified in the schema. Genus is also required and cannot be null. Watering and growth_rate are set to default values if not provided. The validate for watering and growth_rate are set to only accept the provided values.

**GardenPlant Model:**

In the GardenPlant model, the position field is mandatory and cannot be left empty. Each specific garden allows only one unique garden_plant to be placed in a particular position. This means that within a single garden, no two garden_plants can occupy the same position.

The color and size fields are equipped with default values, which are utilized if no values are provided during the creation of a garden_plant object. For the color, size, and position fields, the validation has been set up to accept only predefined values.

**Comment Model:**

In the Comment model, the message field is mandatory and cannot be left empty and the format validation has been applied in schema. The comment_date field is set to the current date.

## R10. Describe the way tasks are allocated and tracked in your project

I am using Trello to track my project. I have created a Trello board with the following lists:
project planning, models, schemas, controller, endpoints, testing and error handling, bug fix, D.R.Y code, and readme file.

I have also created multiple cards for each list that needs to be completed. Each card is assigned to a list based on the stage of the project. For example, the "project planning" list contains cards related to project planning, such as "create ERD" and "finalise ERD." The "models" list contains cards related to creating database models, such as "create User model" and "create Garden model."

By assigning tasks to specific lists, I can track the progress of each task from its initial stage to completion. This allows me to monitor the overall progress of the project and see what needs to be done next.

Trello Board: [Link](https://trello.com/b/kkaIJSVf/virtualgarden-api)

![Trello](/docs/Trello/trello1.png)
![Trello](/docs/Trello/trello4.png)
![Trello](/docs/Trello/trello6.png)

---

## Reference List

[^1]: "What is PostgreSQL?", _EDUCBA_, Retrieved 21th July 2023, https://www.educba.com/what-is-postgresql/
[^2]: "PostgreSQL and JSON – How to Use JSON Data in PostgreSQL", _freecodecamp_, Retrieved 21th July 2023, https://www.freecodecamp.org/news/postgresql-and-json-use-json-data-in-postgresql/
[^3]: "What is PostgreSQL? Introduction, Advantages & Disadvantages", _guru99_, Retrieved 21th July 2023, https://www.guru99.com/introduction-postgresql.html
[^4]: "What is ORM?", _EDUCBA_, Retrieved 21th July 2023, https://www.educba.com/what-is-orm/
[^5]: "What is an ORM and Why You Should Use it", _bitsrc_, Retrieved 21th July 2023, https://blog.bitsrc.io/what-is-an-orm-and-why-you-should-use-it-b2b6f75f5e2a
