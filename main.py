from flask import Flask, render_template, jsonify, request, redirect, url_for
import json
import routes  

app = Flask(__name__)
app.secret_key = "1412002#"

# Register routes
app.add_url_rule('/register', 'register', routes.register, methods=["POST", "GET"])
app.add_url_rule('/home', 'home', routes.home)
app.add_url_rule('/', 'login', routes.login, methods=["POST", "GET"])
app.add_url_rule('/category/<category_name>', 'category_books', routes.category_books)
app.add_url_rule('/allbooks', 'get_all_book', routes.get_all_book)
app.add_url_rule('/favourites', 'favourites', routes.favourites)
app.add_url_rule('/add_to_favourite/<book_id>', 'add_to_favourite', routes.add_to_favourite, methods=["POST"])
app.add_url_rule('/addBook', 'add_book', routes.add_book, methods=["POST", "GET"])
app.add_url_rule('/delete_book/<book_id>', 'delete_book', routes.delete_book, methods=["POST"])
app.add_url_rule('/edit_book/<book_id>', 'edit_book', routes.edit_book, methods=["POST", "GET"])
app.add_url_rule('/cancel_edit', 'cancel_edit', routes.cancel_edit)
app.add_url_rule('/edit_book_data', 'edit_book_data', routes.edit_book_data, methods=["POST"])
app.add_url_rule('/logout', 'logout', routes.logout)
app.add_url_rule('/allbooks/search', 'search', routes.search, methods=["POST"])

if __name__ == "__main__":
    app.run(debug=True)