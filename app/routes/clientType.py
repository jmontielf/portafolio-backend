from flask import request
from app.models.clientType import ClientType

def clientTypeRoutes(app):
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


    # clientTypesResponse = []
    # for ctype in allClientTypes:
    #   clientTypesResponse.append({"id": ctype[0], "name": ctype[1], "desc": ctype[2]})

    # json_format = json.dumps(clientTypesResponse) 

    # return json_format

    return allClientTypes






