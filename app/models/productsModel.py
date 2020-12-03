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
    #self.desc = productData['desc']
    self.price = productData['price']
    self.quality = productData['quality']
    self.registerDate = productData['registerDate']
    #self.data = productData['data']
    #self.id_comerciante = productData['id_comerciante']
    self.stock = productData['stock']
    self.productType = productData['productType']

  def createProduct(self):
    sql = "INSERT INTO PRODUCTO (NOMBRE, PRECIO, CALIDAD, FEC_INGRESO, STOCK, TIPO_PRODUCTO) VALUES (:1, :2, :3, TO_DATE('2020-11-25 23:43:04', 'YYYY-MM-DD HH24:MI:SS'), :4, :5)"
    #"INSERT INTO "ADMIN_FERIA"."PRODUCTO" (NOMBRE, PRECIO, CALIDAD, FEC_INGRESO, STOCK, TIPO_PRODUCTO) 
    # VALUES ('PAPAYA', '$200', 'EXCELENTE', TO_DATE('2020-11-25 23:43:04', 'YYYY-MM-DD HH24:MI:SS'), '200', 'FRUTA')"
    
    connection = OracleConnect.makeConn()
    #? Attemp creation of new products
    try:
      cursor = connection.cursor()
      cursor.execute(sql, (self.name, self.price, self.quality, self.stock, self.productType))
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