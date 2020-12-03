from flask import request
from app.models.productsModel import getAllAvailableProducts, ProductModel

def productsController(app):
  #? Get all avaible products for create auction
  @app.route("/products", methods=['GET'])
  def getAvailableProducts():
    products = getAllAvailableProducts()
    return products
