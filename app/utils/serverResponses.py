from .dbCodes import dbCodes
from flask import jsonify

serverErrors = {
  "STD": "Ha ocurrido un error al procesar la solicitud",
  "newUSR": "Ya existe un usuario con el {} ingresado",
  "noUSR": "El usuario no existe",
  "actionUSR": "Error al {} usuario",
  "AuctionErr": "Ha ocurrido un error al {} la subasta",
  "AuctionNotFound": "No existe una subasta con el ID proporcionado",
  "AuctionNotID": "Debe proporcionar un ID para ejecutar la acción"
}

serverSuccess = {
  "newUSR": "Usuario {} con éxito",
  "Auction": "Subasta {} con éxito"
}

def GetORAerrCode(errorObj):
  regexSearch = re.search("(ORA-\d\d\d\d)\w", errorObj.message)
  if regexSearch:
    return regexSearch.group(0)
  else:
    return None


def returnError(messageCode, stringVariable = ""):
  response = jsonify({
    "Error": serverErrors["STD"],
    "Message": serverErrors[messageCode].format(stringVariable)
  }), 400
  return response

def returnDBError(errorCode):
  response = jsonify({
    "Error": "Ha ocurrido un error al procesar la solicitud",
    "Message": "{} : {}".format(errorCode, dbCodes[errorCode])
  }), 400
  return response

def returnActionSuccess(messageCode, stringVariable):
  response = jsonify({
    "Message": serverSuccess[messageCode].format(stringVariable)
  }), 200

  return response
