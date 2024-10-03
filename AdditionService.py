from zato.server.service import Service
import logging


class AdditionService(Service):
    def handle(self):
        try:
            num_1 = self.request.payload.get("num_1")
            num_2 = self.request.payload.get("num_2")

            logging.info(f"Received request : {self.request.payload}")

            if num_1 and num_2:
                result = num_1 + num_2
                self.response.payload = {"result": result}
                self.response.status_code = 200
            else:
                self.response.payload = {
                    "error": "Missing one or both numbers"
                }
                self.response.status_code = 400

            logging.info(f"Sent response : {self.response.payload}")
        except Exception as e:
            self.response.payload = {"error": str(e)}
            logging.error(f"Error occurred: {str(e)}")
            self.response.status_code = 500
