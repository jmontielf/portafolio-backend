from flask import request
from app.models.auctionModel import getAllAuctions, AuctionModel

def auctionsController(app):
  #? CREATE AUCTION
  @app.route("/auctions/create", methods=['POST'])
  def createAuction():
    requestBody = request.get_json()
    print(requestBody)
    auctionInstance = AuctionModel(requestBody["auction"])
    newAuction = auctionInstance.createAuction(requestBody["products"])
    return newAuction

  @app.route("/auctions", methods=['GET'])
  def getAllAuctions():
    getAuctions = getAllAuctions()
    return getAuctions

# ! TODO
#! CORREGIR CONSULTAS 
#! AGREGAR VENTA LOCAL - VENTA EXTRANJERA / DETALLE DE VENTAS
  @app.route("/auctions/update", methods=['POST'])
  def updateAuctions():
    return "1"

  @app.route("/auctions/delete", methods=['POST'])
  def deleteAuctions():
    return "2"

  @app.route("/auctions/disable", methods=['POST'])
  def disableAuctions():
    return "3"
