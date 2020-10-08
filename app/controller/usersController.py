from flask import request
from app.models.users import (User, UserLogin)

#* Defines the routes for Users
#? Entry point of users route
def userController(app):
  @app.route("/users/")
  def greetUsers():
    return "Hello World from Users!"

  #? Route to create a new user
  @app.route("/users/add", methods=['POST'])
  def createUsers():
    requestBody = request.get_json()
    newUser = User(requestBody)
    newUser.createUser()
    
    #TODO: Return response of user created
    return "User Created!"

  #? Make login to the user 
  @app.route("/users/login", methods=['POST'])
  def makeLogin():
    loginBody = request.get_json()
    newLogin = UserLogin(loginBody)
    result = newLogin.makeLogin()
    return result
