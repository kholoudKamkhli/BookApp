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
    
    
#----------------------------------------------------------------------------------------------------------------
# # app/models.py

# import json
# from datetime import datetime

# class Book:
#     def __init__(self, _id, title, isbn, page_count, published_date, thumbnail_url, short_description, long_description, status, authors, categories):
#         self._id = _id
#         self.title = title
#         self.isbn = isbn
#         self.page_count = page_count
#         self.published_date = datetime.strptime(published_date, '%Y-%m-%dT%H:%M:%S.%f%z') if published_date else None
#         self.thumbnail_url = thumbnail_url
#         self.short_description = short_description
#         self.long_description = long_description
#         self.status = status
#         self.authors = authors
#         self.categories = categories

#     @classmethod
#     def create_books_from_json(cls, file_name):
#         books = []
#         try:
#             with open(file_name, 'r') as infile:
#                 books_data = json.load(infile)
#         except (FileNotFoundError, json.JSONDecodeError):
#             books_data = []
#         for book_data in books_data['books']:
#             book = cls(
#                 _id=book_data['_id'],
#                 title=book_data['title'],
#                 isbn=book_data.get('isbn', ''),  
#                 page_count=book_data.get('pageCount', 0),  
#                 published_date=book_data['publishedDate']['$date'] if 'publishedDate' in book_data else None,
#                 thumbnail_url=book_data.get('thumbnailUrl', ''),
#                 short_description=book_data.get('shortDescription', ''),
#                 long_description=book_data.get('longDescription', ''),
#                 status=book_data.get('status', ''),
#                 authors=book_data.get('authors', []),
#                 categories=book_data.get('categories', [])
#             )
#             books.append(book)
#         return books

#     @classmethod
#     def get_unique_categories(cls, file_name):
#         categories = set()
#         books = cls.create_books_from_json(file_name)
#         for book in books:
#             for category in book.categories:
#                 if category != "":
#                     categories.add(category)
#                 if category == "S":
#                     print(book._id)
#         return categories
#     @classmethod
#     def get_specific_category_books(cls, specified_category,file_name):
#         category_books = set()
#         books = cls.create_books_from_json(file_name)
#         for book in books:
#             for category in book.categories:
#                 if category == specified_category:
#                     category_books.add(book)
#         return category_books
# import json
# from datetime import datetime

# class Book:
#     def __init__(self, _id, title, isbn, page_count, published_date, thumbnail_url, short_description, long_description, status, authors, categories):
#         self._id = _id
#         self.title = title
#         self.isbn = isbn
#         self.page_count = page_count
#         self.published_date = datetime.strptime(published_date, '%Y-%m-%dT%H:%M:%S.%f%z') if published_date else None
#         self.thumbnail_url = thumbnail_url
#         self.short_description = short_description
#         self.long_description = long_description
#         self.status = status
#         self.authors = authors
#         self.categories = categories

#     @classmethod
#     def create_books_from_json(cls, file_name):
#         books = []
#         try:
#             with open(file_name, 'r') as infile:
#                 books_data = json.load(infile)
#         except (FileNotFoundError, json.JSONDecodeError):
#             books_data = {"books": []}  # Initialize with empty structure if file is empty or malformed
#         for book_data in books_data['books']:
#             published_date = None
#             if 'publishedDate' in book_data:
#                 published_date_data = book_data['publishedDate']
#                 if isinstance(published_date_data, dict) and '$date' in published_date_data:
#                     published_date = published_date_data['$date']
#                 elif isinstance(published_date_data, str):
#                     published_date = published_date_data
#             book = cls(
#                 _id=book_data['_id'],
#                 title=book_data['title'],
#                 isbn=book_data.get('isbn', ''),  
#                 page_count=book_data.get('pageCount', 0),  
#                 published_date=published_date,
#                 thumbnail_url=book_data.get('thumbnailUrl', ''),
#                 short_description=book_data.get('shortDescription', ''),
#                 long_description=book_data.get('longDescription', ''),
#                 status=book_data.get('status', ''),
#                 authors=book_data.get('authors', []),
#                 categories=book_data.get('categories', [])
#             )
#             books.append(book)
#         return books

#     @classmethod
#     def get_unique_categories(cls, file_name):
#         categories = set()
#         books = cls.create_books_from_json(file_name)
#         for book in books:
#             for category in book.categories:
#                 if category != "":
#                     categories.add(category)
#         return categories

#     @classmethod
#     def get_specific_category_books(cls, specified_category, file_name):
#         category_books = set()
#         books = cls.create_books_from_json(file_name)
#         for book in books:
#             for category in book.categories:
#                 if category == specified_category:
#                     category_books.add(book)
#         return category_books

import json
from datetime import datetime

class Book:
    def __init__(self, _id, title, isbn, page_count, published_date, thumbnail_url, short_description, long_description, status, authors, categories):
        self._id = _id
        self.title = title
        self.isbn = isbn
        self.page_count = page_count
        self.published_date = self.parse_date(published_date)
        self.thumbnail_url = thumbnail_url
        self.short_description = short_description
        self.long_description = long_description
        self.status = status
        self.authors = authors
        self.categories = categories

    def parse_date(self, date_str):
        date_formats = ['%Y-%m-%dT%H:%M:%S.%f%z', '%Y-%m-%dT%H:%M', '%Y-%m-%dT%H:%M:%S.%f']
        for fmt in date_formats:
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                continue
        return None

    @classmethod
    def create_books_from_json(cls, file_name):
        books = []
        try:
            with open(file_name, 'r') as infile:
                books_data = json.load(infile)
        except (FileNotFoundError, json.JSONDecodeError):
            books_data = {"books": []}  
        for book_data in books_data['books']:
            published_date = ""
            if 'publishedDate' in book_data:
                published_date_data = book_data['publishedDate']
                if isinstance(published_date_data, dict) and '$date' in published_date_data:
                    published_date = published_date_data['$date']
                elif isinstance(published_date_data, str):
                    published_date = published_date_data
                
            book = cls(
                _id=book_data['_id'],
                title=book_data['title'],
                isbn=book_data.get('isbn', ''),  
                page_count=book_data.get('pageCount', 0),  
                published_date=published_date,
                thumbnail_url=book_data.get('thumbnailUrl', ''),
                short_description=book_data.get('shortDescription', ''),
                long_description=book_data.get('longDescription', ''),
                status=book_data.get('status', ''),
                authors=book_data.get('authors', []),
                categories=book_data.get('categories', [])
            )
            books.append(book)
        return books

    @classmethod
    def get_unique_categories(cls, file_name):
        categories = set()
        books = cls.create_books_from_json(file_name)
        for book in books:
            for category in book.categories:
                if category != "":
                    categories.add(category)
        return categories

    @classmethod
    def get_specific_category_books(cls, specified_category, file_name):
        category_books = set()
        books = cls.create_books_from_json(file_name)
        for book in books:
            for category in book.categories:
                if category == specified_category:
                    category_books.add(book)
        return category_books
