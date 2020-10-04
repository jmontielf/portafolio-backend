#* Import the subroutes of the application
from app.routes.users.usersRoutes import userRoutes
from app.routes.test.test import testRoutes
from app.routes.clientType import clientTypeRoutes

#* Unify all the routes and export it to the main.py
def applicationRoutes(app):
  userRoutes(app)
  testRoutes(app)
  clientTypeRoutes(app)