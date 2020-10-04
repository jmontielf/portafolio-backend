from app.controller.test.testController import TestController

def testRoutes(app):
  # Testing routes
  @app.route("/test/")
  def greetTest():
    return TestController.sayHello()
  