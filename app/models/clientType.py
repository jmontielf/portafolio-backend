from app.config.db_config import OracleConnect
import json

class ClientType:
  def __init__(self, clientType):
    self.name = clientType["name"]
    self.desc = clientType["desc"]

  #*CREATE NEW CLIENT TYPE
  def createClientType(self):
    sql = "INSERT INTO TIPO_CLIENTE (NOMBRE_TIPO, DESCRIPCION_TIPO) VALUES (:1, :2)"
    connection = OracleConnect.makeConn()
    #? Attempt to insert all the data 
    try:
      cursor = connection.cursor()
      cursor.execute(sql, (self.name, self.desc))
      connection.commit()
    finally:
      if connection != "":
        connection.close()
  
  #*GET ALL CLIENTS TYPES 
  def getAllClientTypes(self):
    sql = "SELECT * FROM TIPO_CLIENTE"
    connection = OracleConnect.makeConn()
    #? Attempt to fetch all the data 
    try:
      clientTypesResponse = []
      cursor = connection.cursor()
      cursor.execute(sql)
      results = cursor.fetchall()
      #? Create the object in order to store the data
      for ctype in results:
        clientTypesResponse.append({"id": ctype[0], "name": ctype[1], "desc": ctype[2]})
      #? Convert the object to JSON and return it
      json_format = json.dumps(clientTypesResponse) 
      return json_format
    finally:
      if connection != "":
        connection.close()
