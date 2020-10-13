from flask import request
from app.models.users import (User, UserLogin)

#* Defines the routes for Users
#? Entry point of users route
def userController(app):
  @app.route("/users/")
  def greetUsers():
    return "Hello World from Users!"

  #? Route to get all users
  @app.route("/users/get-all", methods=['GET'])
  def getAllUsers():
    allUsers = User(allData=False)
    request = allUsers.getAllUsers()
    return request

  #? Route to create a new user
  @app.route("/users/add", methods=['POST'])
  def createUsers():
    requestBody = request.get_json()
    newUser = User(requestBody)
    createUser = newUser.createUser()
    return createUser

  #? Route to update an existent user
  @app.route("/users/update", methods=['POST'])
  def updateUser():
    requestBody = request.get_json()
    newUser = User(requestBody)
    updateUser = newUser.updateUser()
    return updateUser

  #? Make login to the user 
  @app.route("/users/login", methods=['POST'])
  def makeLogin():
    loginBody = request.get_json()
    newLogin = UserLogin(loginBody)
    result = newLogin.makeLogin()
    return result
