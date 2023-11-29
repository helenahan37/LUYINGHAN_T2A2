API Webserver Project - Virtual Garden API

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
   CREATE USER <user_name> WITH PASSWORD '<password>';
   ```

5. Grant all privileges on the database to the role:

   ```
   GRANT ALL PRIVILEGES ON DATABASE virtual_garden_db TO <user_name>;
   ```

6. Grant all privileges on the schema to the role

   ```
   GRANT ALL ON SCHEMA public TO <user_name>;
   ```

7. cd into 'src' folder and create a virtual environment and activate it:

   ```
   python3 -m venv .venv && source .venv/bin/activate
   ```

8. Rename the '.env.sample' file to '.env' file and add the following lines:

   ```
   DATABASE_URL="postgresql+psycopg2://<user_name>:<password>@localhost:5432/virtual_garden_db"
   JWT_SECRET_KEY="<secret_key>"
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


The problem being addressed by building this particular app is the time and effort constraints that modern society poses on garden design and maintenance. Many individuals find it difficult to allocate enough time to plan and manage their real gardens effectively. Garden design requires careful consideration of plant selection, arrangement, and maintenance, which can be daunting and time-consuming for busy individuals. Additionally, lack of experience and knowledge about plants' attributes may lead to suboptimal garden designs and unsatisfactory outcomes.

To tackle this problem, the virtual garden API provides a solution that allows users to design and experiment with their dream gardens in a virtual environment. By offering a wide selection of plants and customization options, users can freely explore their creativity without the limitations of time and physical space. The virtual garden also serves as a valuable learning platform where users can gain insights into plant attributes, growth cycles, and watering requirements, empowering them to make informed decisions when managing their real gardens.

---


## Rend points for API

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

## ERD 

![ERD](/docs/ERD.png)

## Detail of third party services

- **Flask**: Flask is a micro web framework written in Python. It is used to build web applications and APIs. I am using Flask to build my API.
- **SQLAlchemy**: SQLAlchemy is an open-source SQL toolkit and object-relational mapper for Python. It designed for efficient and high-performing database access. I am using SQLAlchemy to interact with my PostgreSQL database.
- **Marshmallow**: Marshmallow is an ORM/ODM/framework-agnostic library for converting complex datatypes to and from native Python datatypes. I am using Marshmallow to serialize and deserialize my SQLAlchemy models.
- **Flask-Bcrypt**: Flask-Bcrypt is a Flask extension that provides bcrypt hashing utilities for my application. I am using Flask-Bcrypt to hash passwords for user authentication.
- **Flask-JWT-Extended**: Flask-JWT-Extended is a Flask extension that provides JSON Web Token (JWT) support for my application. I am using Flask-JWT-Extended to generate and verify JWT tokens for user authentication.
- **PostgreSQL**: PostgreSQL is a free and open-source relational database management system. I am using PostgreSQL to store and manage my application's data.
- **psycopg2-binary**: psycopg2-binary is a PostgreSQL database adapter for Python. I am using psycopg2-binary to connect my application to PostgreSQL.
- **Werkzeug**: Werkzeug is a comprehensive WSGI web application library. I am using Werkzeug to handle HTTP requests and responses for my application.


## Reference List

[^1]: "What is PostgreSQL?", _EDUCBA_, Retrieved 21th July 2023, https://www.educba.com/what-is-postgresql/
[^2]: "PostgreSQL and JSON – How to Use JSON Data in PostgreSQL", _freecodecamp_, Retrieved 21th July 2023, https://www.freecodecamp.org/news/postgresql-and-json-use-json-data-in-postgresql/
[^3]: "What is PostgreSQL? Introduction, Advantages & Disadvantages", _guru99_, Retrieved 21th July 2023, https://www.guru99.com/introduction-postgresql.html
[^4]: "What is ORM?", _EDUCBA_, Retrieved 21th July 2023, https://www.educba.com/what-is-orm/
[^5]: "What is an ORM and Why You Should Use it", _bitsrc_, Retrieved 21th July 2023, https://blog.bitsrc.io/what-is-an-orm-and-why-you-should-use-it-b2b6f75f5e2a
