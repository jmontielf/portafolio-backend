#* Import the subroutes of the application
from app.controller.usersController import userController
from app.controller.clientTypeController import clientTypeController
from app.controller.auctionsController import auctionsController

#* Unify all the routes and export it to the main.py
def applicationRoutes(app):
  #? Entrypoint app
  @app.route("/")
  def main():
    return "Welcome from Portfvirtual API"

  #* From route calls to controllers and models
  #? Routes and controller for the users
  userController(app)
  #? Routes and controller for client type
  clientTypeController(app)
  #? Routes and controller for auctions
  auctionsController(app)