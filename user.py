import json
from datetime import datetime

class User:
    def __init__(self, username, file_name, email):
        self.username = username
        self.email = email
        self.file_name = file_name
        self.date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Add user to database function
    def add_user(self, password):
        # Check if file exists and initialize if empty
        try:
            with open(self.file_name, 'r') as infile:
                users_data = json.load(infile)
        except (FileNotFoundError, json.JSONDecodeError):
            users_data = []

        # Loop over existing users to check if email already exists
        for user in users_data:
            if user["email"] == self.email:
                return "The mail is already taken."
        
        # Create new user to add to the database
        user = {"email": self.email, "password": password, "username": self.username, "date": self.date, "favorites": []}
        users_data.append(user)
        
        # Open file in write mode to modify it
        with open(self.file_name, 'w') as outfile:
            json.dump(users_data, outfile, indent=4)
        return None
    
    # Delete user from database
    def delete_user(self):
        # Open the database file containing users info
        try:
            with open(self.file_name, 'r') as infile:
                users_data = json.load(infile)
        except (FileNotFoundError, json.JSONDecodeError):
            users_data = []

        # Update users_data to contain all users except the existing user
        new_users_data = [user for user in users_data if user["email"] != self.email]
        
        # Open database file in write mode to modify its content
        with open(self.file_name, 'w') as outfile:
            json.dump(new_users_data, outfile, indent=4)
        return None
    
    
    def add_to_fav(self,book):
        self.favorites.append(book)
        return None
    
    
