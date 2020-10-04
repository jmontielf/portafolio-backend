#* Import DB Controller
from app.config.db_config import OracleConnect

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

