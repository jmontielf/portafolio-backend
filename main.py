#* Main import of libraries
from flask import Flask

#* Import all the routes of the app
from app.routes.routes import applicationRoutes

#* Create the instance of the app and pass the intance to the components of the app
app = Flask(__name__)
applicationRoutes(app)

#* Run the app server 
app.run(host='0.0.0.0')