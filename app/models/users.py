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
    self.fono = Persona["fono"]
    self.name = Persona["nombre"]
    self.appat = Persona["appat"]
    self.apmat = Persona["apmat"]
    self.email = Persona["email"]
    self.celular = Persona["celular"]
    self.username = Usuario["username"]
    self.password = Usuario["password"]
    self.direccion = Persona["direccion"]
    self.tipoCliente = Cliente["tipoCliente"]
    self.id = Usuario["id_usuario"] if hasattr(Usuario, 'id_usuario') == True else ""
    self.estado = Usuario["estado_usuario"] if hasattr(Usuario, 'estado_usuario') == True else ""

  #* CREATE NEW USER 
  #TODO: INSERT INTO OTHER TABLES
  def createUser(self):
    # sql = "INSERT INTO USUARIO (USUARIO, CLAVE_USER, ESTADO) VALUES (:1, :2, :3)"
    connection = OracleConnect.makeConn()

    try:
      cursor = connection.cursor()
      cursor.callproc("USUARIO_security.add_user", [self.username, self.password])
      # cursor.execute(sql, (self.username, self.password, 9))
      connection.commit()
      return jsonify({"msg": "User created"}), 200
    finally:
      if connection != "":
        connection.close()

  #* UPDATE EXISTENT USER
  #TODO: Update the other tables
  def updateUser(self):
    sql = "UPDATE USUARIO SET USUARIO = :1, CLAVE_USER = :2, ESTADO = :3 WHERE ID_USUARIO = :4"
    connection = OracleConnect.makeConn()

    try:
      cursor = connection.cursor()
      cursor.execute(sql, (self.username, self.password, self.estado, self.id))
      connection.commit()
      return jsonify({"msg": "User updated"}), 200
    finally:
      if connection != "":
        connection.close()


#? Class defined to attemp user login
class UserLogin:
  def __init__(self, userData):
    self.username = userData["username"]
    self.password = userData["password"]

  #* ATTEMPT LOGIN TO THE APP
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

