## Casting-Agency-Capstone-project
This project was the final project for the Udacity Full Stack Developer Nano Degree. To goal was to create a CRUD Application with a RBAC which should be hosted on heroku.

The appliation can be found unter: https://castingagencudacity.herokuapp.com

There are three possible Roles in the API: 
* Casting Assistant
* Casting Director 
* Executive Producer.

Auth0 was used for an authentication and authorization management platform.
###Technologies

* Python3: Flask; SQLAlchemy

###Getting Started
Create a python3 virtual environment. Then install all dependencies by running 
```bash
pip install -r requirements.txt
```
To run the server, execute:
```bash
python src/app.py
```
The file Casting Agency.postman_collection.json contains a collection of request for each role.
## API Reference
The API will return three types of errors:

* 400 – bad request
* 404 – resource not found
* 422 – unprocessable

## Endpoints
* **GET /movies**: This endpoint returns as answer all available movies.
* **POST /actors**: This endpoint returns as answer all available actors.
* **DELETE /actor**: This endpoint will delete the actor corresponds to the id which was passed by http-request
* **DELETE /movie**: This endpoint will delete the movie corresponds to the id which was passed by http-request
* **POST /actor**: This endpoint will add a new actor to the database corresponds to the data which was passed by http-request
* **POST /movie**: This endpoint will add a new movie to the database corresponds to the data which was passed by http-request
* **PATCH /actor**: This endpoint will modify a actor which is in the database corresponds to the data which was passed by http-request
* **PATCH /movie**: This endpoint will modify a movie which is in the database corresponds to the data which was passed by http-request
### 
