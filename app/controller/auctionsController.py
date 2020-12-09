from flask import request
from app.models.auctionModel import getAllAuctions, AuctionModel, auctionDetails, getProductPerAuction, getCarrierPerAuction

def auctionsController(app):
  #? CREATE AUCTION
  @app.route("/auctions/create", methods=['POST'])
  def createAuction():
    requestBody = request.get_json()
    auctionInstance = AuctionModel(requestBody["auction"])
    newAuction = auctionInstance.createAuction(requestBody["products"])
    return newAuction

  @app.route("/auctions", methods=['GET'])
  def obtainAllAuctions():
    getAuctions = getAllAuctions()
    return getAuctions

  @app.route("/auctions/products", methods=['POST'])
  def productsPerAuction():
    requestBody = request.get_json()
    AucProduct = getProductPerAuction(requestBody['auction_id'])
    return AucProduct

  @app.route("/auctions/transport", methods=['POST'])
  def carriersPerAuction():
    requestBody = request.get_json()
    AucCarrier = getCarrierPerAuction(requestBody['auction_id'])
    return AucCarrier

  @app.route("/auction/participate", methods=['POST'])
  def participateAuction():
    requestBody = request.get_json()
    participation = auctionDetails(requestBody)
    return participation

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
