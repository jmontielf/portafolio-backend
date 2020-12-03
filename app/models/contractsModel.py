#* Import DB Controller
import cx_Oracle
from flask import jsonify
from app.utils.dbCodes import dbCodes
from app.config.db_config import OracleConnect
from app.utils.serverResponses import returnError, returnActionSuccess, returnDBError, GetORAerrCode

class ContractsModel:
  def __init__(self, contractInfo):
    self.file = contractInfo
    self.startDate = contractInfo
    self.endDate = contractInfo
    self.status = contractInfo
    self.id_person = contractInfo

  def createContract(self):
    return "Contract created"

  def updateContract(self):
  return "Contract updated"

  def deleteContract(self):
    return "Contract deleted"

def getAllContracts(self):
    return "All contracts json"
