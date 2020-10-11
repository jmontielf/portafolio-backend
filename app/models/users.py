#* Import DB Controller
from flask import jsonify
from app.config.db_config import OracleConnect
from flask_jwt_extended import create_access_token

#* Define the type and class of the model 
#* Assign all the data to the new object
class User:
  #* Initialize the object with all the data needed
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
  def createUser(self):
    sqlUsuario = "USUARIO_security.add_user"
    sqlPersona = "INSERT INTO PERSONA (RUT, NOMBRE, APPAT, APMAT, EMAIL, DIRECCION, FONO, CELULAR) VALUES (:1, :2, :3, :4, :5, :6, :7, :8)"
    sqlCliente = "INSERT INTO CLIENTE (ID_USUARIO, ID_PERSONA, ID_TIPOCLIENTE) VALUES ((SELECT ID_USUARIO FROM USUARIO WHERE USUARIO = :1), (SELECT ID_PERSONA FROM PERSONA WHERE RUT = :2), :3)"
    connection = OracleConnect.makeConn()

    try:
      cursor = connection.cursor()
      cursor.callproc(sqlUsuario, [self.username, self.password])
      cursor.execute(sqlPersona, (self.rut, self.name, self.appat, self.apmat, self.email, self.direccion, self.fono, self.celular))
      cursor.execute(sqlCliente, (self.username.upper(), self.rut, self.tipoCliente))

      connection.commit()
      return jsonify({"msg": "User created"}), 200
    except cx_Oracle.DatabaseError as e:
      errorObj, = e.args
      return jsonify({
        "err": "An error has ocurred",
        "Error Code": errorObj.code,
        "Error Message": errorObj.message
        }), 401
    finally:
      if connection != "":
        connection.close()

  #* UPDATE EXISTENT USER
  #TODO: Update the other tables
  def updateUser(self):
    sqlUsuario = "UPDATE USUARIO SET USUARIO = :1, CLAVE_USER = :2, ESTADO = :3 WHERE ID_USUARIO = :4"
    sqlPersona = "UPDATE PERSONA SET EMAIL = :1, DIRECCION = :2, FONO = :3, CELULAR = :4 WHERE ID_PERSONA = :5"
    sqlCliente = "UPDATE CLIENTE SET ID_TIPOCLIENTE = :1 WHERE ID_CLIENTE = :2"
    connection = OracleConnect.makeConn()

    # TODO: GET VALUES FOR PERSONA AND CLIENTE 
    try:
      cursor = connection.cursor()
      cursor.execute(sqlUsuario, (self.username, self.password, self.estado, self.id))
      # cursor.execute(sqlPersona, (self.rut, self.name, self.appat, self.apmat, self.email, self.direccion, self.fono, self.celular))
      # cursor.execute(sqlCliente, (self.username.upper(), self.rut, self.tipoCliente))
      connection.commit()
      return jsonify({"msg": "User updated"}), 200
    except cx_Oracle.DatabaseError as e:
      errorObj, = e.args
      return jsonify({
        "err": "An error has ocurred",
        "Error Code": errorObj.code,
        "Error Message": errorObj.message
        }), 401
    finally:
      if connection != "":
        connection.close()


#? Class defined to attemp user login
class UserLogin:
  def __init__(self, userData):
    self.username = userData["username"]
    self.password = userData["password"]

  #* ATTEMPT LOGIN TO THE APP
  # TODO: RETURN ALL THE DATA OF THE USER
  # TODO: RETURN VALUES FROM CLIENTE AND PERSONA TABLE
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
    except cx_Oracle.DatabaseError as e:
      errorObj, = e.args
      return jsonify({
        "err": "An error has ocurred",
        "Error Code": errorObj.code,
        "Error Message": errorObj.message
        }), 401
    finally:
      if connection != "":
        connection.close()

