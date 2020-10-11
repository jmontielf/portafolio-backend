from flask import request
from app.models.clientType import ClientType

def clientTypeController(app):
  @app.route("/client-type/add", methods=['POST'])
  def createClientType():
    requestBody = request.get_json()

    print(requestBody["name"])

    newClientType = ClientType(requestBody)
    newClientType.createClientType()

    return "response"


  @app.route("/client-type/", methods=['GET'])
  def getAllClientType():
    initialData = {"name": "aaa", "desc": "aaa"}
    clientType = ClientType(initialData)
    allClientTypes = clientType.getAllClientTypes()

    # Enable Access-Control-Allow-Origin
    #allClientTypes.headers.add("Access-Control-Allow-Origin", "*")

    return allClientTypes






