#* Import OracleDB library for connection
import cx_Oracle

#* Create connection Class
class OracleConnect:
  #* Define function to stablish the connection
  def makeConn():
    # TODO: SAVE THIS CONFIG FILE IN A SECURE FILE
    connectionInfo = {
      'hostName': '35.208.121.134',
      'portNumber': '1521',
      'serviceName': 'xe',
      'username': 'ADMIN_FERIA',
      'password': '123',
    }

    #* Create DSN (Data Source Name) / TNS (Transparent Network Substrate), this are protocol from Oracle to stablish the connection with the db
    #* Create connection 
    dsn_tns = cx_Oracle.makedsn(connectionInfo['hostName'], connectionInfo['portNumber'], service_name=connectionInfo['serviceName'])
    conn = cx_Oracle.connect(user=connectionInfo['username'], password=connectionInfo['password'], dsn=dsn_tns) 

    #* Return the connection object
    return conn


