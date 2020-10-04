from app.config.db_config import OracleConnect

class TestController:
  def sayHello():
    c = OracleConnect.makeConn().cursor()
    c.execute('select * from USUARIO')
    for row in c:
        print (row[0], '-', row[1])
    c.close()

    return "Hello World from the test app!"

    