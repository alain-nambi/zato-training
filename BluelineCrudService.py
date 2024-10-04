from zato.server.service import Service
import uuid

# Global variable to store users
users = {}


class BluelineCrudService(Service):
    name = "blueline.crud.service"

    def log_and_respond(self, message, status_code, payload=None):
        """Helper method to log and set the response payload."""
        self.logger.info(message)
        self.response.payload = payload or {}
        self.response.status_code = status_code

    def handle_GET(self):
        self.log_and_respond(
            message="Retrieving all users.",
            status_code=200,
            payload={"users": list(users.values())}
        )

    def handle_POST(self):
        self.logger.info("Creating a new user.")

        name = self.request.payload.get("name")
        firstname = self.request.payload.get("firstname")
        address = self.request.payload.get("address")
        age = self.request.payload.get("age", 0)
        function = self.request.payload.get("function")
        email = self.request.payload.get("email")

        # Validate required fields
        if not all([name, firstname, address, function, email]):
            return self.log_and_respond(
                message="Missing required fields in user creation",
                status_code=400,
                payload={"error": "Missing required fields"}
            )

        # Validate age
        if not isinstance(age, int) or age <= 0:
            return self.log_and_respond(
                message="Invalid age provided.",
                status_code=400,
                payload={"error": "Age must be an integer and greater than 0"}
            )

        # Normalize email to lowercase for consistency
        email = email.lower()

        # Check if user already exists
        if any(user["email"] == email for user in users.values()):
            return self.log_and_respond(
                message=f"User with email : ${email} already exists",
                status_code=409,
                payload={"error": f"User with email : {email} already exists"}
            )

        # Generate random ID
        ID = str(uuid.uuid4()).split("-")[-1]

        # Create user
        user = {
            "ID": ID,
            "name": name,
            "firstname": firstname,
            "address": address,
            "age": age,
            "function": function,
            "email": email,
        }

        # Store user with ID as the unique key
        users[ID] = user
        self.log_and_respond(
            message="User created successfully",
            status_code=201,
            payload={
                "message": "User created successfully", "user": user
            }
        )

    def handle_PUT(self):
        self.logger.info("Updating user information by specifying ID")

        ID = self.request.payload.get("ID")
        if not ID:
            return self.log_and_respond(
                message="ID is required",
                status_code=400,
                payload={"error": "ID is required"}
            )

        user = users.get(ID)
        if not user:
            return self.log_and_respond(
                message="User not found",
                status_code=404,
                payload={"error": "User not found"}
            )

        # Update user information with provided values or keep existing ones
        user.update({
            "name": self.request.payload.get("name", user["name"]),
            "firstname": self.request.payload.get(
                "firstname", user["firstname"]
            ),
            "address": self.request.payload.get("address", user["address"]),
            "age": self.request.payload.get("age", user["age"]),
            "function": self.request.payload.get("function", user["function"]),
            "email": self.request.payload.get("email", user["email"])
        })

        self.log_and_respond(
            message="User information updated successfully",
            status_code=200,
            payload={
                "message": "User information updated successfully",
                "user": user
            }
        )

    def handle_DELETE(self):
        self.logger.info("Deleting user by specifying ID")

        ID = self.request.payload.get("ID")
        if ID not in users:
            return self.log_and_respond(
                "User not found", 404, {"error": "User not found"}
            )

        del users[ID]
        self.log_and_respond(
            message=f"User with ID: {ID} deleted successfully",
            status_code=200,
            payload={"message": f"User with ID: {ID} deleted successfully"}
        )
