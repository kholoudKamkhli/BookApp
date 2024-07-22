import json
from datetime import datetime
# creating Book class to handle Book data
class Book:
    def __init__(self, _id, title, isbn, page_count, published_date, thumbnail_url, short_description, long_description, status, authors, categories):
        self._id = _id
        self.title = title
        self.isbn = isbn
        self.page_count = page_count
        self.published_date = published_date
        self.thumbnail_url = thumbnail_url
        self.short_description = short_description
        self.long_description = long_description
        self.status = status
        self.authors = authors
        self.categories = categories
    
    #creating class methods that will be used in the backend 
    @classmethod
    #create list of objects of books and return them
    def create_books_from_json(cls, file_name):
        books = []
        try:
            with open(file_name, 'r') as infile:
                books_data = json.load(infile)
        except (FileNotFoundError, json.JSONDecodeError):
            books_data = {"books": []}  
        for book_data in books_data['books']:
            published_date_data = book_data['publishedDate']
            
            # create book instance  
            book = cls(
                _id=book_data['_id'],
                title=book_data['title'],
                isbn=book_data.get('isbn', ''),  
                page_count=book_data.get('pageCount', 0),  
                published_date=published_date_data,
                thumbnail_url=book_data.get('thumbnailUrl', ''),
                short_description=book_data.get('shortDescription', ''),
                long_description=book_data.get('longDescription', ''),
                status=book_data.get('status', ''),
                authors=book_data.get('authors', []),
                categories=book_data.get('categories', [])
            )
            # add the book instance to the list 
            books.append(book)
        # return the list
        return books
    # method to get the unique categories of the books
    @classmethod
    def get_unique_categories(cls, file_name):
        categories = set()
        books = cls.create_books_from_json(file_name)
        for book in books:
            for category in book.categories:
                if category != "":
                    categories.add(category)
        return categories
    # method to get books that belong to specific category
    @classmethod
    def get_specific_category_books(cls, specified_category, file_name):
        category_books = set()
        books = cls.create_books_from_json(file_name)
        for book in books:
            for category in book.categories:
                if category == specified_category:
                    category_books.add(book)
        return category_books
