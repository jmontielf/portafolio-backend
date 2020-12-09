from flask import request
from app.models.auctionModel import getAllAuctions, AuctionModel, auctionDetails, getProductPerAuction, getCarrierPerAuction, getAuctionWinner, auctionUpdate

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

  @app.route("/auctions/participate", methods=['POST'])
  def participateAuction():
    requestBody = request.get_json()
    participation = auctionDetails(requestBody)
    return participation

  @app.route("/auctions/winner", methods=['POST'])
  def auctionWinner():
    requestBody = request.get_json()
    getWinner = getAuctionWinner(requestBody)
    return getWinner

  @app.route("/auction/update", methods=['POST'])
  def updateAuction():
    requestBody = request.get_json()
    updated = auctionUpdate(requestBody)
    return updated