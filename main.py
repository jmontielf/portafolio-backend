#* Main import of libraries
from flask import Flask
from flask_jwt_extended import JWTManager

#* Import all the routes of the app
from app.routes.routes import applicationRoutes

#* Create the instance of the app and pass the intance to the components of the app
app = Flask(__name__)
applicationRoutes(app)

#* Setup the Flask-JWT-Extended extension
#TODO: move the key of JWT to a secret file
#TODO: change key
app.config['JWT_SECRET_KEY'] = 'portfvirtual2020'
jwt = JWTManager(app)

#* Run the app server 
app.run(host='0.0.0.0')