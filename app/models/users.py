#* Import DB Controller
from flask import jsonify
from app.config.db_config import OracleConnect
from flask_jwt_extended import create_access_token

#Define the type and class of the model 
#Assign all the data to the new object
class User:
  #Initialize the object with all the data needed
  def __init__(self, allData):
    #Destructuring the object 
    Persona = allData["persona"]
    Usuario = allData["usuario"]
    Cliente = allData["cliente"]

    #Assing the values from the object to the model
    self.rut = Persona["rut"]
    self.name = Persona["nombre"]
    self.appat = Persona["appat"]
    self.apmat = Persona["apmat"]
    self.email = Persona["email"]
    self.direccion = Persona["direccion"]
    self.fono = Persona["fono"]
    self.celular = Persona["celular"]
    self.username = Usuario["username"]
    self.password = Usuario["password"]
    self.tipoCliente = Cliente["tipoCliente"]

  #* CREATE NEW USER 
  def createUser(self):
    sql = "INSERT INTO USUARIO (USUARIO, CLAVE_USER, ESTADO) VALUES (:1, :2, :3)"
    connection = OracleConnect.makeConn()

    try:
      cursor = connection.cursor()
      cursor.execute(sql, (self.username, self.password, 9))
      connection.commit()
    finally:
      if connection != "":
        connection.close()

class UserLogin:
  def __init__(self, userData):
    self.username = userData["username"]
    self.password = userData["password"]

  def makeLogin(self):
    sql = "SELECT * FROM USUARIO WHERE USUARIO = :usrName"
    connection = OracleConnect.makeConn()

    try:
      cursor = connection.cursor()
      cursor.execute(sql, usrName=self.username)
      fetchQuery = cursor.fetchall()
      result = fetchQuery[0] if len(fetchQuery) != 0 else fetchQuery

      #* Check if user and password are the same
      if result and result[1] == self.username and result[2] == self.password:

        #* Create access token
        access_token = create_access_token(identity=self.username)
        foundUser = {
          "id_usuario": result[0], 
          "username": result[1], 
          "estado_usuario": result[3], 
          "accessToken": access_token
        }

        #!-----
        #TODO: INSERT ACCESS TOKEN TO DB

        #* Return session_token with user data
        return jsonify(userLogin=foundUser), 200
      else:
        return jsonify({"err": "Invalid username or password"}), 401


    finally:
      if connection != "":
        connection.close()

