from flask import request
from app.models.clientType import ClientType

def clientTypeController(app):
  @app.route("/client-type/add", methods=['POST'])
  def createClientType():
    requestBody = request.get_json()
    newClientType = ClientType(requestBody)
    newClientType.createClientType()

    return "response"


  @app.route("/client-type/", methods=['GET'])
  def getAllClientType():
    initialData = {"name": "aaa", "desc": "aaa"}
    clientType = ClientType(initialData)
    allClientTypes = clientType.getAllClientTypes()

    return allClientTypes






