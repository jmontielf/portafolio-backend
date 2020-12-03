from flask import request
from app.models.contractsModel import ContractsModel, getAllContracts

def contractsController(app):
  #? Get all avaible products for create auction
  @app.route("/contracts", methods=['GET'])
  def getAllContracts():
    contracts = getAllContracts()
    return contracts

   
