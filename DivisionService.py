from zato.server.service import Service
import logging


class DivisionService(Service):
    def handle(self):
        try:
            numerator = self.request.payload.get("numerator", 1)
            denominator = self.request.payload.get("denominator", 1)

            logging.info(f"Received request : {self.request.payload}")

            result = numerator / denominator
            self.response.payload = {"result": result}

            logging.info(f"Sent response : {self.response.payload}")
        except ZeroDivisionError:
            self.response.payload = {"error": "Cannot divide by zero"}
            logging.error("Division by zero error")
            self.response.status_code = 400
