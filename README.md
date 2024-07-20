# BOOKY
BOOKY is a website where users can navigate through books library, different books categories, and add books to thier favourites list.
- What does it do?
"This is a web project in which users can navigate through book library, and Admins have a dashboard where they can add, delete, or modify any book"
- What is the "new feature" which you have implemented that
we haven't seen before?
 "Reading from json files, passing values to routes and use them, deleting from file, and using jinja to display elments"
## Prerequisites
Did you add any additional modules that someone needs to
install (for instance anything in Python that you `pip
install-ed`)?
List those here (if any).
* Python: Install Python from the original website python.org
* Flask: Install flask using pip (python's package installer). by running the following command: `pip install flask`
* Jinja in Visual Studio Code: Ensure you have Visual Studio Code installed. Jinja is a templating engine used by Flask, and it should be integrated into Visual Studio Code by default when you have the Python extension installed.
## Project Checklist
- [x] It is available on GitHub.
- [x] It uses the Flask web framework.
- [x] It uses at least one module from the Python Standard
Library other than the random module.
 Please provide the name of the module you are using in your
app.
 - Module name: json and datetime
- [x] It contains at least one class written by you that has
both properties and methods. It uses `__init__()` to let the
class initialize the object's attributes (note that
`__init__()` doesn't count as a method). This includes
instantiating the class and using the methods in your app.
Please provide below the file name and the line number(s) of
at least one example of a class definition in your code as
well as the names of two properties and two methods.
 - File name for the class definition: models.py
 - Line number(s) for the class definition: line 4 for User class definition and line 60 for Book class definition:
 - Name of two properties: username and email in User class, title and short_description in Book class
 - Name of two methods: add_user and delete_user in User class, get_unique_categories and get_specific_category_books in Book class
 - File name and line numbers where the methods are used: models.py, lines 12,35, 120, 130.
- [x] It makes use of JavaScript in the front end and uses the
localStorage of the web browser.
- [x] It uses modern JavaScript (for example, let and const
rather than var).
- [x] It makes use of the reading and writing to the same file
feature.
- [x] It contains conditional statements. Please provide below
the file name and the line number(s) of at least
one example of a conditional statement in your code.
 - File name: main.py
 - Line number(s): 67, 71, 127, 147, 158
- [x] It contains loops. Please provide below the file name
and the line number(s) of at least
 one example of a loop in your code.
 - File name: main.py
 - Line number(s): 66, 126, 157, 206
- [x] It lets the user enter a value in a text box at some
point.
 This value is received and processed by your back end
Python code.
- [x] It doesn't generate any error message even if the user
enters a wrong input.
- [x] It is styled using your own CSS.
- [x] The code follows the code and style conventions as
introduced in the course, is fully documented using comments
and doesn't contain unused or experimental code.
 In particular, the code should not use `print()` or
`console.log()` for any information the app user should see.
Instead, all user feedback needs to be visible in the
browser.
- [x] All exercises have been completed as per the
requirements and pushed to the respective GitHub repository.
