from datetime import datetime
import json
import flask
from flask import render_template, request, url_for, session,jsonify,abort,redirect
from models import User
from models import Book
app = flask.Flask("main")
app.secret_key = "1412002#"
 
#route for register screen
@app.route("/register",methods=["POST","GET"])
def register():
    session.pop("mail",None)
    if request.method =="POST":
        #get users data from the POST request when user submit Register form
        username = request.form['username']
        password = request.form['password']
        mail = request.form['email']
        message = User(username,"users.json",mail).add_user(password)
        
        #if there is error message, render the registeration page with the error message
        if message:
            return render_template("register.html",validation=message)
        
        session['mail'] = mail
        
        #redirect to home page after successful registeration
        return redirect(url_for("home"))
    return render_template("register.html",validation=None)



#-----------------------------------------------------------------------------------------------------



@app.route("/home")
def home():
    if "mail" not in session:
        return redirect("/")
    file_path = 'books.json'  
    categories = Book.get_unique_categories(file_path)
    return render_template('index.html', categories=categories)


#----------------------------------------------------------------------------------------------------
@app.route("/", methods = ["POST","GET"])
def login():
    type = None
    
    #if user is already logged in redirect them to home 
    if 'mail' in session:
        return redirect(url_for('home'))
    if request.method == "POST":
        mail = request.form["email"]
        password = request.form["password"]
        with open("users.json","r") as infile:
            users_data = json.load(infile)
        for user in users_data:
            if(user["email"] == mail and user["password"] == password):
                session["mail"] = mail
                if mail == "admin@admin.com":
                    type = "Admin"
                    return redirect(url_for("get_all_book",type = type))
                else:
                    return redirect(url_for("home",type = "User"))
    # if the mail and password don't match any user in database, show message to user 
        return render_template("login.html",validation = "Invalid mail or password, please try again.")
    return render_template("login.html",validation = None)



#--------------------------------------------------------------------------------------------------------------


@app.route('/category/<category_name>')
def category_books(category_name):
    file_name = 'books.json'  
    books = Book.get_specific_category_books( category_name,file_name)
    return render_template('all_books.html', category_name=category_name, books=books,type="User")

#--------------------------------------------------------------------------------------------------------------
@app.route('/allbooks')
def get_all_book():
    type = request.args.get("type")
    file_name = 'books.json'
    books = Book.create_books_from_json(file_name)
    print("we are here")
    book = books[0]
    print(book.title)
    return render_template('all_books.html',books=books,type = type,category_name = None)


#---------------------------------------------------------------------------------------------------------------

@app.route("/favourites")
def favourites():
    user_email = session.get('mail')
    if not user_email:
        return redirect(url_for('login'))
    with open("users.json", "r") as users_file:
        users_data = json.load(users_file)
    for user_data in users_data:
        if user_data["email"] == user_email:
            favorites = user_data.get("favorites", [])    
    return render_template('favourites.html',favourites=favorites)


#----------------------------------------------------------------------------------------------------------------

@app.route("/add_to_favourite/<book_id>", methods=["POST"])
def add_to_favourite(book_id):
    print("book id is " + str(book_id))
    user_mail = session.get("mail")
    if not user_mail:
        return redirect(url_for('login'))
    
    book = None
    with open("books.json", "r") as books_file:
        books_data = json.load(books_file)
    
    if "books" in books_data:
        books_data = books_data["books"]
    
    for book_data in books_data:
        if int(book_data["_id"]) == int(book_id):
            book = book_data
            print("book is here ")
            break
    
    if not book:
        return jsonify({"success": False, "message": "Book not found"})
    
    user = None
    with open("users.json", "r") as users_file:
        users_data = json.load(users_file)
    
    for user_data in users_data:
        if user_data["email"] == user_mail:
            user = user_data
            print(user)
            break
    
    if not user:
        return jsonify({"success": False, "message": "User not found"})
    
    favorites = user.get("favorites", [])
    fav_ids = [fav["_id"] for fav in favorites]
    print(fav_ids)
    
    if book_id not in fav_ids:
        # favorites.append({"_id": book["_id"], "title": book["title"]})
        favorites.append({"_id": book["_id"], "title": book["title"],"isbn": book["isbn"],
            "pageCount": book["pageCount"],
            "publishedDate": book["publishedDate"],
            "thumbnailUrl":book["thumbnailUrl"] ,
            "shortDescription":book["shortDescription"],
            "longDescription":   book["longDescription"],
            "status":book["status"],
            "authors": book["authors"],
            "categories": book["categories"]})
    
    user["favorites"] = favorites
    print(user["favorites"])
    
    with open("users.json", "w") as users_file:
        json.dump(users_data, users_file, indent=4)
    print("reached here")
    
    return jsonify({"success": True, "book_id": book_id})

#--------------------------------------------------------------------------------------------------
@app.route("/addBook", methods=["POST", "GET"])
def add_book():
    if request.method == "GET":
        return render_template("add_book.html")
    if request.method == "POST":
        try:
            with open("books.json", "r") as books_file:
                books_data = json.load(books_file)
        except (FileNotFoundError, json.JSONDecodeError):
            books_data = {"books": []}

        idx = 1
        if books_data['books']:
            idx = max(book['_id'] for book in books_data['books']) + 1

        published_date = request.form["publishedDate"]
        try:
            # Try to parse the date to ensure consistency
            parsed_date = datetime.strptime(published_date, '%Y-%m-%dT%H:%M')
            published_date = parsed_date.strftime('%Y-%m-%dT%H:%M:%S.%f%z')
        except ValueError:
            return "Invalid date format. Please use YYYY-MM-DDTHH:MM format."

        book = {
            "_id": idx,
            "title": request.form["title"],
            "isbn": request.form["isbn"],
            "pageCount": int(request.form["pageCount"]),
            "publishedDate": published_date,
            "thumbnailUrl": request.form["thumbnailUrl"],
            "shortDescription": request.form["shortDescription"],
            "longDescription": request.form["longDescription"],
            "status": request.form["status"],
            "authors": request.form["authors"].split(','),
            "categories": request.form["categories"].split(',')
        }

        books_data['books'].append(book)
        with open("books.json", 'w') as outfile:
            json.dump(books_data, outfile, indent=4)

        return redirect(url_for("get_all_book", type="Admin"))

#------------------------------------------------------------------------------
@app.route("/delete_book/<book_id>", methods=["POST"])
def delete_book(book_id):
    try:
        with open("books.json", "r") as books_file:
            books_data = json.load(books_file)
    except (FileNotFoundError, json.JSONDecodeError):
        return jsonify({"success": False, "message": "Error loading books data"}), 500

    book_to_delete = None
    for book in books_data["books"]:
        if int(book["_id"]) == int(book_id):
            print("Found book to delete")
            book_to_delete = book
            break

    if not book_to_delete:
        return jsonify({"success": False, "message": "Book not found"}), 404

    books_data["books"].remove(book_to_delete)

    try:
        with open("books.json", "w") as books_file:
            json.dump(books_data, books_file, indent=4)
    except Exception as e:
        return jsonify({"success": False, "message": f"Error saving books data: {e}"}), 500

    return jsonify({"success": True, "message": "Book deleted successfully"}), 200


#------------------------------------------------------------------------------------------------------------
@app.route("/edit_book/<book_id>",methods = ["POST","GET"])
def edit_book(book_id):
    book_to_edit = None
    if "method":
        print("reached heree")
        with open("books.json", "r") as books_file:
                books_data = json.load(books_file)
        for book in books_data["books"]:
            if int(book["_id"]) == int(book_id):
                book_to_edit = book
                print("book found" + str(book))
                break
        if not book_to_edit:
            print("book not found")
            return jsonify({"success": False, "message": "Book not found"}), 404
        return render_template('edit_book.html',book=book_to_edit)
    return render_template('edit_book.html',book=book_to_edit)


#---------------------------------------------------------------------------------------------------------------
@app.route("/cancel_edit")
def cancel_edit():
    return redirect(url_for("get_all_book", type="Admin"))
#---------------------------------------------------------------------------------------------------------------
@app.route("/edit_book_data",methods = ["POST"])
def edit_book_data():
    if request.method == "POST":
        book_id = request.form["bookId"]
        with open("books.json", "r") as books_file:
            books_data = json.load(books_file)
        for book in books_data["books"]:
            if int(book["_id"]) == int(book_id):
                book_to_edit = book
                book["title"] = request.form["title"]
                book["isbn"] = request.form["isbn"]
                book["thumbnailUrl"] = request.form["thumbnailUrl"]
                book["shortDescription"] = request.form["shortDescription"]
                book["longDescription"] = request.form["longDescription"]
                book["status"] = request.form["status"]
                book["authors"] = request.form["title"]
                book["authors"] = request.form["authors"].split(',')
                book["categories"] = request.form["categories"].split(',')
        with open("books.json", "w") as books_file:
            json.dump(books_data, books_file, indent=4)
        return redirect(url_for("get_all_book", type="Admin"))
    return redirect(url_for("get_all_book", type="Admin"))
