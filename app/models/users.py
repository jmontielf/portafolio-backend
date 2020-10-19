#* Import DB Controller
import re
import cx_Oracle
from flask import jsonify
from app.utils.dbCodes import dbCodes
from app.config.db_config import OracleConnect
from flask_jwt_extended import create_access_token
from app.utils.serverResponses import returnError, returnActionSuccess, returnDBError

#* Define the type and class of the model 
#* Assign all the data to the new object
class User:
  #* Initialize the object with all the data needed
  def __init__(self, allData):
    #Destructuring the object 
    if allData:
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
    #? Queries to check if user exist before insert
    sqlCheckUser = "SELECT ID_USUARIO FROM USUARIO WHERE USUARIO = :usrName"
    sqlCheckRUT = "SELECT ID_PERSONA FROM PERSONA WHERE RUT = :usrRUT"
    #? Make connection with the DB
    connection = OracleConnect.makeConn()
    try:
        cursor = connection.cursor()
        #? Check if user exist
        cursor.execute(sqlCheckUser, usrName=self.username.upper())
        fetchedQuery = cursor.fetchall()
        if fetchedQuery:
          #? Check if RUT exist  
          cursor.execute(sqlCheckRUT, usrRUT=self.rut)
          fetchedQuery = cursor.fetchall()
          if fetchedQuery:
            #? Do inserts 
            cursor.callproc(sqlUsuario, [self.username, self.password])
            cursor.execute(sqlPersona, (self.rut, self.name, self.appat, self.apmat, self.email, self.direccion, self.fono, self.celular))
            cursor.execute(sqlCliente, (self.username.upper(), self.rut, self.tipoCliente))
            connection.commit()
            return returnActionSuccess("newUSR", "creado")
          else:
            #* RETURN ERROR BY RUT
            return returnError("newUSR", "rut")
        else:
          #* RETURN ERROR BY USERNAME
          return returnError("newUSR", "nombre de usuario")
    except cx_Oracle.DatabaseError as e:
      errorObj, = e.args
      regexSearch = GetORAerrCode(errorObj)
      if regexSearch:
        errorCode = regexSearch.group(0)
        return returnDBError(errorCode)
      else:
        return returnError("actionUSR", "crear")
    finally:
      if connection != "":
        connection.close()

  #* UPDATE EXISTENT USER
  #TODO: Update the other tables
  #TODO: SEPARATE USUARIO, PERSONA AND CLIENTE IN DIFFERENT QUERIES
  def updateUser(self):
    sqlUsuario = "UPDATE USUARIO SET USUARIO = :1, CLAVE_USER = :2, ESTADO = :3 WHERE ID_USUARIO = :4"
    sqlPersona = "UPDATE PERSONA SET EMAIL = :1, DIRECCION = :2, FONO = :3, CELULAR = :4 WHERE RUT = :5"
   # sqlCliente = "UPDATE CLIENTE SET ID_TIPOCLIENTE = :1 WHERE ID_CLIENTE = :2"
    sqlCheckUser = "SELECT ID_USUARIO FROM USUARIO WHERE USUARIO = :usrName"

    connection = OracleConnect.makeConn()

    # TODO: GET VALUES FOR CLIENTE 
    try:
      cursor = connection.cursor()

      cursor.execute(sqlCheckUser, usrName=self.username.upper())
      fetchedQuery = cursor.fetchall()

      if fetchedQuery:
        cursor.execute(sqlUsuario, (self.username, self.password, self.estado, self.id))
        cursor.execute(sqlPersona, (self.email, self.direccion, self.fono, self.celular, self.rut))
        #cursor.execute(sqlCliente, (self.username.upper(), self.rut, self.tipoCliente))
        connection.commit()
        return returnActionSuccess("newUSR", "actualizado")
      else:
        return returnError("noUSR")
    except cx_Oracle.DatabaseError as e:
      errorObj, = e.args
      regexSearch = GetORAerrCode(errorObj)
      if regexSearch:
        errorCode = regexSearch.group(0)
        return returnDBError(errorCode)
    finally:
      if connection != "":
        connection.close()

  #? Listar usuarios (Get users)
  def getAllUsers(self):
    sql = "SELECT USR.USUARIO, USR.CLAVE_USER, USR.ESTADO, USR.ID_USUARIO, CLT.ID_TIPOCLIENTE, PRS.RUT, PRS.NOMBRE, PRS.APPAT, PRS.APMAT, PRS.EMAIL, PRS.DIRECCION, PRS.FONO, PRS.CELULAR FROM USUARIO USR JOIN CLIENTE CLT ON USR.ID_USUARIO = CLT.ID_USUARIO JOIN PERSONA PRS ON CLT.ID_PERSONA = PRS.ID_PERSONA"
    connection = OracleConnect.makeConn()

    try:
      cursor = connection.cursor()
      cursor.execute(sql)
      fetchQuery = cursor.fetchall()

      if len(fetchQuery) > 0:
        foundUsers = []
        for row in fetchQuery:
          #* Create an object with the results and update the main array
          userObject = {
            'USUARIO': row[0],
            'CLAVE_USER': row[1],
            'ESTADO': row[2],
            'ID_USUARIO': row[3],
            'ID_TIPOCLIENTE': row[4],
            'RUT': row[5],
            'NOMBRE': row[6],
            'APPAT': row[7],
            'APMAT': row[8],
            'EMAIL': row[9],
            'DIRECCION': row[10],
            'FONO': row[11],
            'CELULAR': row[12]
          }
          #* Append the object to the user array
          foundUsers.append(userObject)

        #* Return array with the users
        return jsonify(foundUsers), 200
      else:
        return jsonify({"err": "Failed to fetch the users"}), 400
    except cx_Oracle.DatabaseError as e:
        errorObj, = e.args
        return jsonify({
          "err": "An error has ocurred",
          "Error Code": errorObj.code,
          "Error Message": errorObj.message
          }), 400
    finally:
      if connection != "":
        connection.close()

  #? ELIMINAR USUARIO (Desactivar estado)
  def disableUser(self, opt):
    sql = "UPDATE USUARIO SET ESTADO = 0 WHERE USUARIO = :1 AND CLAVE_USER = :2"
    connection = OracleConnect.makeConn()

    try:
      cursor = connection.cursor()
      cursor.execute(sql, (opt['username'], opt['password']))
      connection.commit()
      return jsonify({"msg": "User disabled"}), 200
    except cx_Oracle.DatabaseError as e:
      errorObj, = e.args
      return jsonify({
        "err": "An error has ocurred",
        "Error Code": errorObj.code,
        "Error Message": errorObj.message
        }), 400
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
        return jsonify({"err": "Invalid username or password"}), 400
    except cx_Oracle.DatabaseError as e:
      errorObj, = e.args
      return jsonify({
        "err": "An error has ocurred",
        "Error Code": errorObj.code,
        "Error Message": errorObj.message
        }), 400
    finally:
      if connection != "":
        connection.close()

