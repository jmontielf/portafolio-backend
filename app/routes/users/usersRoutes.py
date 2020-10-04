from flask import request
from app.models.users import User

#* Defines the routes for Users
#? Entry point of users route
def userRoutes(app):
  @app.route("/users/")
  def greetUsers():
    return "Hello World from Users!"

#? Route to create a new user
#TODO: call the model, insert data to model
#TODO: create insert to DB with data and func from the model
  @app.route("/users/add", methods=['POST'])
  def createUsers():
    requestBody = request.get_json()

    newUser = User(requestBody)
    newUser.createUser()

    return "User Created!"