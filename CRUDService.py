"""
Exercice
--------
service: gestion utilisateur
- création utilisateur (nom, prénom, adresse, age, fonction, etc...)
- suppression utilisateur 
- get all list utilisateurs
- une connexion channel relier à ton service pour un appel externe

Nous n'avons pas de bd pour insérer les info mais crée une variable dans votre code 
"""

from zato.server.service import Service

# Global variable to store users
users = {}


class CRUDService(Service):
    # Handle GET request - Get List of User
    def handle_GET(self):
        self.logger.info("Retrieving all users.")
        self.response.payload = {"users": list(users.values())}
        self.logger.info("I was invoked via GET")

    # Handle POST request - Create User
    def handle_POST(self):
        self.logger.info("Creating a new user.")

        name = self.request.payload.get("name", "")
        firstname = self.request.payload.get("firstname", "")
        address = self.request.payload.get("address", "")
        age = self.request.payload.get("age", 0)
        function = self.request.payload.get("function", "")

        # Validate required fields
        if not (name and firstname and address and function):
            self.response.payload = {"error": "Missing required fields"}
            self.response.status_code = 400
            self.logger.warning("Missing required fields in user creation")
            return

        # Validate age
        if not isinstance(age, int) or int(age) <= 0:
            self.response.payload = {
                "error": "Age must be an integer and greater than 0"
            }
            self.response.status_code = 400
            self.logger.warning(f"Invalid age provided : {age}")
            return

        # Create user
        user = {
            "name": name,
            "firstname": firstname,
            "address": address,
            "age": age,
            "function": function
        }

        # Use the user's name as a key in the users dictionary
        if name in users:
            self.response.payload = {"error": "User already exists"}
            self.response.status_code = 409
            return

        users[name] = user

        self.response.payload = {
            "message": "User created successfully",
            "user": user,
        }
        self.response.status_code = 201
        self.logger.info(f"User {user['name']} created")
        self.logger.info("I was invoked via POST")

    # Handle PUT request - Update User Informations
    def handle_PUT(self):
        self.logger.info("Updating user information by specifying username")

        name = self.request.payload.get("name", "")
        if not name:
            self.response.payload = {"error": "Username is required"}
            self.response.status_code = 400
            return

        user = users.get(name)
        user.update({
            "firstname": self.request.payload.get("firstname", user["firstname"]),
            "address": self.request.payload.get("address", user["address"]),
            "age": self.request.payload.get("age", user["age"]),
            "function": self.request.payload.get("function", user["function"])
        })
        users[name] = user

        self.response.payload = {
            "message": "User information updated successfully",
            "user": user
        }
        self.response.status_code = 200

        self.logger.info("I was invoked via PUT")

    # Handle DELETE request - Delete User
    def handle_DELETE(self):
        self.logger.info("Deleting user by specifying username")

        name = self.request.payload.get("name", "")

        if name not in users:
            self.response.payload = {"error": "User not found"}
            self.response.status_code = 404
            return

        del users[name]
        self.response.payload = {
            "message": f"User {name} deleted successfully"
        }
        self.response.status_code = 200
        self.logger.info(f"User {name} deleted")
        self.logger.info("I was invoked via DELETE")
