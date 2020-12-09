#* Import DB Controller
import cx_Oracle
from flask import jsonify
from app.utils.dbCodes import dbCodes
from app.config.db_config import OracleConnect
from app.utils.serverResponses import returnError, returnActionSuccess, returnDBError, GetORAerrCode
import json

class ProductModel:
  def __init__(self, productData):
    self.name = productData['name']
    self.desc = productData['desc']
    self.price = productData['price']
    self.quality = productData['quality']
    self.registerDate = productData['registerDate']
    self.id_comerciante = productData['id_comerciante']
    self.stock = productData['stock']
    self.productType = productData['productType']

  def createProduct(self):
    sql = "INSERT INTO PRODUCTO (NOMBRE, DESCRIPCION, PRECIO, CALIDAD, FEC_INGRESO, ID_COMERCIANTE, STOCK, TIPO_PRODUCTO) VALUES (:1, :2, :3, :4, :5, :6, :7, :8)"
    
    connection = OracleConnect.makeConn()
    #? Attemp creation of new products
    try:
      cursor = connection.cursor()
      cursor.execute(sql, (self.name, self.desc, self.price, self.quality, self.registerDate, self.id_comerciante, self.stock, self.productType))
      connection.commit()
      return returnActionSuccess("Producto", "creado")
    except cx_Oracle.DatabaseError as e:
        errorObj, = e.args
        regexSearch = GetORAerrCode(errorObj)
        if regexSearch:
          errorCode = regexSearch.group(0)
          return returnDBError(errorCode)
        else:
          return returnError("ProductErr", "crear")
    finally:
      if connection != "":
          connection.close()
    
    return "created"

def getAllAvailableProducts():
  sql = "SELECT DISTINCT NOMBRE FROM PRODUCTO ORDER BY NOMBRE ASC"
  connection = OracleConnect.makeConn()

  try:
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    productList = []

    if len(result) > 0:
      for product in result:
        productList.append(product[0])
      return jsonify(productList), 200
    else:
      return jsonify({"err": "Failed to fetch the products"}), 400

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

#? Call this function from insert auction
def productsPerAuction(details):
  products = details['products']
  auctionID = details['idLastAuction']
  sql = 'INSERT INTO SUB_OFERTA (ID_SUBASTA, ID_PRODUCTO) VALUES (:1, :2)'

  for product in products:
    connection = OracleConnect.makeConn()
      #? Attempt association of products and auctions
    try:
      cursor = connection.cursor()
      cursor.execute(sql, (auctionID, product["productID"]))
      connection.commit()
      print("Ascociar ok!")
    except cx_Oracle.DatabaseError as e:
        errorObj, = e.args
        regexSearch = GetORAerrCode(errorObj)
        if regexSearch:
          errorCode = regexSearch.group(0)
          print("Error again")
        else:
          print("Error al asociar productos")
    finally:
      if connection != "":
          connection.close()
      