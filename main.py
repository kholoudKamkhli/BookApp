#importing mecessary modules
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
    #empty the session first
    session.pop("mail",None)
    if request.method =="POST":
        #get users data from the POST request when user submit Register form
        username = request.form['username']
        password = request.form['password']
        mail = request.form['email']
        #create User instance and call add_user method of the User class to add user to databse
        message = User(username,"users.json",mail).add_user(password)
        
        #if there is error message, render the registeration page with the error message
        if message:
            return render_template("register.html",validation=message)
        
        session['mail'] = mail
        
        #redirect to home page after successful registeration
        return redirect(url_for("home"))
    return render_template("register.html",validation=None)



#-----------------------------------------------------------------------------------------------------


#route for the home page
@app.route("/home")
def home():
    file_path = 'books.json'  
    # get the books'unique categories to show them to the user
    categories = Book.get_unique_categories(file_path)
    # render the index.html page and pass the obtained categories to it
    return render_template('index.html', categories=categories)


#----------------------------------------------------------------------------------------------------
#route for login page
@app.route("/", methods = ["POST","GET"])
def login():
    #type to save the type of the user either admin or normal user
    type = None
    #if user is already logged in redirect them to home 
    if 'mail' in session:
        return redirect(url_for('home'))
    if request.method == "POST":
        # get the mail and password from the login form data
        mail = request.form["email"]
        password = request.form["password"]
        # open the json file to read the users data
        with open("users.json","r") as infile:
            users_data = json.load(infile)
        # loop over the saved users in users.json to check whether the user exists or not
        for user in users_data:
            if(user["email"] == mail and user["password"] == password):
                # if user is found, save the mail in the session
                session["mail"] = mail
                #check whether the mail entered is admin mail
                if mail == "admin@admin.com":
                    type = "Admin"
                    # if the user is admin, redirect him to books page
                    return redirect(url_for("get_all_book",type = type))
                else:
                    # if user is normal user, redirect him to home page
                    return redirect(url_for("home",type = "User"))
    # if the mail and password don't match any user in database, show message to user 
        return render_template("login.html",validation = "Invalid mail or password, please try again.")
    # render the login page if the method is get
    return render_template("login.html",validation = None)



#--------------------------------------------------------------------------------------------------------------

# getting the books that belong to specific category
@app.route('/category/<category_name>')
def category_books(category_name):
    #check if user was not already signed in, redirect them to sign in page 
    if "mail" not in session:
        return redirect("/")
    file_name = 'books.json'  
    # using the class Book's method to get specific category books
    books = Book.get_specific_category_books( category_name,file_name)
    return render_template('all_books.html', category_name=category_name, books=books,type="User")

#--------------------------------------------------------------------------------------------------------------
# getting all books
@app.route('/allbooks')
def get_all_book():
    #check if user was not already signed in, redirect them to sign in page 
    if "mail" not in session:
        return redirect("/")
    type = request.args.get("type")
    print(type)
    file_name = 'books.json'
    books = Book.create_books_from_json(file_name)
    return render_template('all_books.html',books=books,type = type,category_name = None)


#---------------------------------------------------------------------------------------------------------------
# getting the user's favourite books
@app.route("/favourites")
def favourites():
    #check if user was not already signed in, redirect them to sign in page 
    if "mail" not in session:
        return redirect("/")
    # if user not logged in, redirect to login page
    user_email = session.get('mail')
    if not user_email:
        return redirect(url_for('login'))
    # read user's file
    with open("users.json", "r") as users_file:
        users_data = json.load(users_file)
    # get the logged in in users favourites list
    for user_data in users_data:
        if user_data["email"] == user_email:
            favorites = user_data.get("favorites", [])    
    return render_template('favourites.html',favourites=favorites)


#----------------------------------------------------------------------------------------------------------------
# adding specific book to users favourites
@app.route("/add_to_favourite/<book_id>", methods=["POST"])
def add_to_favourite(book_id):
    user_mail = session.get("mail")
    if not user_mail:
        return redirect(url_for('login'))
    
    book = None
    with open("books.json", "r") as books_file:
        books_data = json.load(books_file)
    # get the book's data
    if "books" in books_data:
        books_data = books_data["books"]
    for book_data in books_data:
        if int(book_data["_id"]) == int(book_id):
            book = book_data
            break
    # if book not found return error 
    if not book:
        return jsonify({"success": False, "message": "Book not found"})
    # get the user's data
    user = None
    with open("users.json", "r") as users_file:
        users_data = json.load(users_file)
    for user_data in users_data:
        if user_data["email"] == user_mail:
            user = user_data
            break
    # handle that the user's data may not exist
    if not user:
        return jsonify({"success": False, "message": "User not found"})
    # get the user's favourite list
    favorites = user.get("favorites", [])
    # get user's favourite books ids
    fav_ids = [fav["_id"] for fav in favorites]
    # if the book not in the user's favourite list, add it
    if book_id not in fav_ids:
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
    
    with open("users.json", "w") as users_file:
        json.dump(users_data, users_file, indent=4)    
    return jsonify({"success": True, "book_id": book_id})

#--------------------------------------------------------------------------------------------------
# admin's functionality to add book to database
@app.route("/addBook", methods=["POST", "GET"])
def add_book():
    #check if user was not already signed in, redirect them to sign in page 
    if "mail" not in session:
        return redirect("/")
    if session.get("mail")!="admin@admin.com":
        return redirect("/")
    if request.method == "GET":
        return render_template("add_book.html")
    if request.method == "POST":
        try:
            with open("books.json", "r") as books_file:
                books_data = json.load(books_file)
        except (FileNotFoundError, json.JSONDecodeError):
            books_data = {"books": []}
        # get the maximum id in the database and add one to be the id of the added book
        idx = 1
        if books_data['books']:
            idx = max(book['_id'] for book in books_data['books']) + 1

        published_date = request.form["publishedDate"]
        #parsing the date to be consistent 
        try:
            parsed_date = datetime.strptime(published_date, '%Y-%m-%dT%H:%M')
            published_date = parsed_date.strftime('%Y-%m-%dT%H:%M:%S.%f%z')
        except ValueError:
            return "Invalid date format. Please use YYYY-MM-DDTHH:MM format."
        #create book 
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
#admin's function to delete a book from the database
@app.route("/delete_book/<book_id>", methods=["POST"])
def delete_book(book_id):
    #check if user was not already signed in, redirect them to sign in page 
    if "mail" not in session:
        return redirect("/")
    if session.get("mail")!="admin@admin.com":
        return redirect("/")
    try:
        # reading the books json file
        with open("books.json", "r") as books_file:
            books_data = json.load(books_file)
    except (FileNotFoundError, json.JSONDecodeError):
        return jsonify({"success": False, "message": "Error loading books data"}), 500
    #loop over the books to get the book to be deleted
    book_to_delete = None
    for book in books_data["books"]:
        if int(book["_id"]) == int(book_id):
            book_to_delete = book
            break
    # return error if the book doesn't exist
    if not book_to_delete:
        return jsonify({"success": False, "message": "Book not found"}), 404
    # remove the book from the books json file
    books_data["books"].remove(book_to_delete)
    # write the data back to file after modification
    try:
        with open("books.json", "w") as books_file:
            json.dump(books_data, books_file, indent=4)
    except Exception as e:
        return jsonify({"success": False, "message": f"Error saving books data: {e}"}), 500
    # removing the book if exists in user's favourites
    with open("users.json", "r") as users_file:
            users_data = json.load(users_file)
    for user in users_data:
        if book_to_delete in user["favorites"]:
            user["favorites"].remove(book_to_delete)
    with open("users.json", "w") as users_file:
            json.dump(users_data, users_file, indent=4)
    return jsonify({"success": True, "message": "Book deleted successfully"}), 200


#------------------------------------------------------------------------------------------------------------
# admin functionality get specific book data to edit it
@app.route("/edit_book/<book_id>",methods = ["POST","GET"])
def edit_book(book_id):
    if "mail" not in session:
        return redirect("/")
    book_to_edit = None
    if "method":
        # open books file to read books' data
        with open("books.json", "r") as books_file:
                books_data = json.load(books_file)
        for book in books_data["books"]:
            if int(book["_id"]) == int(book_id):
                book_to_edit = book
                break
        # if book not found, return error
        if not book_to_edit:
            return jsonify({"success": False, "message": "Book not found"}), 404
        return render_template('edit_book.html',book=book_to_edit)
    return render_template('edit_book.html',book=book_to_edit)


#---------------------------------------------------------------------------------------------------------------
# handle admin's cancel edit
@app.route("/cancel_edit")
def cancel_edit():
    
    return redirect(url_for("get_all_book", type="Admin"))
#---------------------------------------------------------------------------------------------------------------
# handle the editted book data
@app.route("/edit_book_data",methods = ["POST"])
def edit_book_data():
    if "mail" not in session:
        return redirect("/")
    
    if request.method == "POST":
        # get the book to be editted id 
        book_id = request.form["bookId"]
        with open("books.json", "r") as books_file:
            books_data = json.load(books_file)
        #search for the book in the json file
        for book in books_data["books"]:
            if int(book["_id"]) == int(book_id):
                # modify the book's data with the new data
                book["title"] = request.form["title"]
                book["isbn"] = request.form["isbn"]
                book["thumbnailUrl"] = request.form["thumbnailUrl"]
                book["shortDescription"] = request.form["shortDescription"]
                book["longDescription"] = request.form["longDescription"]
                book["status"] = request.form["status"]
                book["authors"] = request.form["title"]
                book["authors"] = request.form["authors"].split(',')
                book["categories"] = request.form["categories"].split(',')
        #rewrite to the file
        with open("books.json", "w") as books_file:
            json.dump(books_data, books_file, indent=4)
        return redirect(url_for("get_all_book", type="Admin"))
    return redirect(url_for("get_all_book", type="Admin"))

#------------------------------------------------------------------------------------------
@app.route("/logout")
def logout():
    session.pop("mail",None)
    return render_template("login.html")