from flask import request
from app.models.productsModel import getAllAvailableProducts, ProductModel

def productsController(app):
  #? Get all avaible products for create auction
  @app.route("/products", methods=['GET'])
  def getAvailableProducts():
    products = getAllAvailableProducts()
    return products

  #! revisar con postman
  @app.route("/products/create", methods=['POST'])
  def createProduct():
    requestBody = request.get_json()
    productInstance = ProductModel(requestBody)
    newproduct = productInstance.createProduct()
    return newproduct
