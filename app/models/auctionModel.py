#* Import DB Controller
import cx_Oracle
from flask import jsonify
from app.utils.dbCodes import dbCodes
from app.config.db_config import OracleConnect
from app.utils.serverResponses import returnError, returnActionSuccess, returnDBError, GetORAerrCode
from app.models.productsModel import ProductModel, productsPerAuction

class AuctionModel:
  def __init__(self, requestData):
    self.value = requestData['value']
    self.desc = requestData['desc']
    self.startDate = requestData['startDate']
    self.endDate = requestData['endDate']
    self.client_id = requestData['clientID']
    self.auctionType = requestData['auctionType']
    self.city = requestData['city']
    self.country = requestData['country']
    self.address = requestData['address']

  #* CREATE NEW AUCTION
  def createAuction(self, productData):
    sqlNewAuction = "INSERT INTO SUBASTA (VALOR, DESCRIPCION, ESTADO, FEC_INICIO, FEC_TERMINO, ID_CLIENTE, TIPO_SUBASTA, CIUDAD, PAIS, DIRECCION) VALUES (:1, :2, :3, :4, :5, :6, :7, :8, :9, :10)"
    sqlGetLastAuctionID = "SELECT ID_SUBASTA FROM (SELECT * FROM SUBASTA ORDER BY ID_SUBASTA DESC) WHERE ROWNUM = 1"

    connection = OracleConnect.makeConn()
    #? Attemp creation of new auction
    try:
      cursor = connection.cursor()
      cursor.execute(sqlNewAuction, (self.value, self.desc, 1, self.startDate, self.endDate, self.client_id, self.auctionType, self.city, self.country, self.address))
      connection.commit()

      #? FETCH ID FROM LAST INSERT
      cursor = connection.cursor()
      cursor.execute(sqlGetLastAuctionID)
      fetchSub = cursor.fetchall()

      if(fetchSub and fetchSub[0][0]):
        details = {
          "idLastAuction": fetchSub[0][0],
          "products": productData
        }
        productsPerAuction(details)

      return returnActionSuccess("Auction", "creada")
    except cx_Oracle.DatabaseError as e:
        errorObj, = e.args
        regexSearch = GetORAerrCode(errorObj)
        if regexSearch:
          errorCode = regexSearch.group(0)
          return returnDBError(errorCode)
        else:
          return returnError("AuctionErr", "crear")
    finally:
      if connection != "":
          connection.close()

  #!* UPDATE AUCTION
  def updateAuction(self):
    sqlCheckSubasta = "SELECT ID_SUBASTA WHERE ID_SUBASTA = :idSubasta"
    sqlSubasta = "UPDATE SUBASTA SET VALOR = :1, DESCRIPCION = :2, ID_TRANSPORTISTA = :3, ESTADO = :4, FEC_INICIO = :5, FEC_TERMINO = :6 WHERE ID_SUBASTA = :7"
    connection = OracleConnect.makeConn()

    try:
      if len(self.id_subasta) > 0:
        #? Create an instance of the cursor
        cursor = connection.cursor()
        #? Check if the auction exist and fetch results
        cursor.execute(sqlCheckSubasta, idSubasta = self.id_subasta)
        fetchSub = cursor.fetchall()
        if len(fetchSub) > 0:
          #? Update values of the auction
          cursor.execute(sqlSubasta, (self.value, self.desc, self.id_trans, self.status, self.startData, self.endDate, self.id_subasta))
          connection.commit()
          return returnActionSuccess("Auction", "actualizada")
        else:
          # Return error no auction found
          return returnError("AuctionNotFound")
      else:
        # Return error no id given 
          return returnError("AuctionNotID")
    except cx_Oracle.DatabaseError as e:
        errorObj, = e.args
        regexSearch = GetORAerrCode(errorObj)
        if regexSearch:
          errorCode = regexSearch.group(0)
          return returnDBError(errorCode)
    finally:
      if connection != "":
        connection.close()

  #* DELETE AUCTION
  def deleteAuction(self):
    sqlCheckSubasta = "SELECT ID_SUBASTA WHERE ID_SUBASTA = :idSubasta"
    sqlSubasta = "DELETE FROM SUBASTA WHERE ID_SUBASTA = :1"
    connection = OracleConnect.makeConn()

    try:
      if len(self.id_subasta) > 0:
        #? Create an instance of the cursor
        cursor = connection.cursor()
        #? Check if the auction exist and fetch results
        cursor.execute(sqlCheckSubasta, idSubasta = self.id_subasta)
        fetchSub = cursor.fetchall()
        if len(fetchSub) > 0:
          #? Update values of the auction
          cursor.execute(sqlSubasta, (self.id_subasta))
          connection.commit()
          return returnActionSuccess("Auction", "eliminada")
        else:
          # Return error no auction found
          return returnError("AuctionNotFound")
      else:
        # Return error no id given 
          return returnError("AuctionNotID")
    except cx_Oracle.DatabaseError as e:
        errorObj, = e.args
        regexSearch = GetORAerrCode(errorObj)
        if regexSearch:
          errorCode = regexSearch.group(0)
          return returnDBError(errorCode)
    finally:
      if connection != "":
        connection.close()

  #* DISABLE AUCTION
  def disableAuction(self):
    sqlCheckSubasta = "SELECT ID_SUBASTA WHERE ID_SUBASTA = :idSubasta"
    sqlSubasta = "UPDATE SUBASTA SET ESTADO = :1 WHERE ID_SUBASTA = :2"
    connection = OracleConnect.makeConn()

    try:
      if len(self.id_subasta) > 0:
        #? Create an instance of the cursor
        cursor = connection.cursor()
        #? Check if the auction exist and fetch results
        cursor.execute(sqlCheckSubasta, idSubasta = self.id_subasta)
        fetchSub = cursor.fetchall()
        if len(fetchSub) > 0:
          #? Update values of the auction
          cursor.execute(sqlSubasta, (self.status, self.id_subasta))
          connection.commit()
          return returnActionSuccess("Auction", "desactivada")
        else:
          # Return error no auction found
          return returnError("AuctionNotFound")
      else:
        # Return error no id given 
          return returnError("AuctionNotID")
    except cx_Oracle.DatabaseError as e:
        errorObj, = e.args
        regexSearch = GetORAerrCode(errorObj)
        if regexSearch:
          errorCode = regexSearch.group(0)
          return returnDBError(errorCode)
    finally:
      if connection != "":
        connection.close()

#* GET ALL AUCTIONS
def getAllAuctions():
  sqlGetAll = "SELECT * FROM SUBASTA"
  # Query with joins
  #sqlGetAll = "SELECT SU.ID_SUBASTA, SU.VALOR, SU.DESCRIPCION, SU.ID_TRANSPORTISTA, SU.ESTADO, SU.FEC_INICIO, SU.FEC_TERMINO FROM SUBASTA SU"
  connection = OracleConnect.makeConn()
  try:
    cursor = connection.cursor()
    cursor.execute(sqlGetAll)
    fetchQuery = cursor.fetchall()

    if len(fetchQuery) > 0:
      #do something
      foundAuctions = []
      for row in fetchQuery:
        auctionObj = {
          'ID_SUBASTA': row[0],
          'DESCRIPCION': row[1],
          'ID_TRANSPORTISTA': row[2],
          'ESTADO': row[3],
          'FEC_INICIO': row[4],
          'FEC_TERMINO': row[5]
        }
        #? Append object to the array
        foundAuctions.append(auctionObj)
      #? Return array with all auctions objects
      return jsonify(foundAuctions), 200
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


#* Transport goes into the auction
def auctionDetails(auctionDetails):
  aucValue = auctionDetails['value']
  aucTransport = auctionDetails['transport_type']
  aucIDCarrier = auctionDetails['id_transportista']
  aucIDAuction = auctionDetails['id_subasta']
  sqlInsertCarrier = "INSERT INTO DETALLE_SUBASTA (OFERTA, TRANSPORTE_TIPO, ID_TRANSPORTISTA, ID_SUBASTA, GANADORA) VALUES (:1, :2, :3, :4, 0)"
  #? Make connection
  connection = OracleConnect.makeConn()
  try:
    cursor = connection.cursor()
    cursor.execute(sqlInsertCarrier, (aucValue, aucTransport, aucIDCarrier, aucIDAuction))
    connection.commit()
    return returnActionSuccess("Participation")
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
