from flask import Flask, request, jsonify
from sqlalchemy import exists
from components.BookDetails import Book
from components.Author import Author
from __main__ import db, app

"""
This file will contain all the routes with their functions. Make sure to add a
separator for your own section.

It is easier to maintain and check for conflicts if all the routes are in a
single file, make sure you are naming each function uniquely.
"""


# ******************** [4] Book Details ********************
@app.route("/admin/books", methods=["POST"])
def addBook():
    """Handles adding a book to the database"""
    # Fetch the POST request's fields
    Name = request.json["Name"]
    Description = request.json["Description"]
    Price = request.json["Price"]
    Author = request.json["Author"]
    Genre = request.json["Genre"]
    Pub = request.json["Publisher"]
    Year = request.json["YearPublished"]
    Sold = request.json["Sold"]

    # Check if the book exists in the DB
    duplicate = db.session.query(exists().where(Book.Name == Name)).scalar()

    if duplicate:
        return jsonify("Book name is already in the database")

    # Create new book with fetched fields
    new_book = Book(Name, Description, Price, Author, Genre, Pub, Year, Sold)

    # Only add book if it's unique
    db.session.add(new_book)
    db.session.commit()

    # Return new_book as json
    return new_book.product_schema.jsonify(new_book)


@app.route("/admin/books", methods=["GET"])
def getBooks():
    """Returns a json with all the books in the database"""
    # Query
    all_books = Book.query.all()

    result = Book.products_schema.dump(all_books)

    # Returns all the DB items as json
    return jsonify(result)


@app.route("/authors", methods=["GET"])
def getAuthors():
    """Returns a json with all the books in the database"""
    # Query
    all_authors = Author.query.all()

    result = Author.products_schema.dump(all_authors)

    # Returns all the DB items as json
    return jsonify(result)


@app.route("/admin/createAuthor", methods=["POST"])
def createAuthor():
    """Handles adding an author to the database"""
    # Fetch the POST request's fields
    FName = request.json["FirstName"]
    LName = request.json["LastName"]
    Biography = request.json["Biography"]
    Publisher = request.json["Publisher"]

    # Check if the book exists in the DB
    dupFName = db.session.query(exists().where(Author.FirstName == FName)).scalar()
    dupLName = db.session.query(exists().where(Author.LastName == LName)).scalar()

    if dupFName and dupLName:
        return jsonify("Author is already in the database.")

    # Create new book with fetched fields
    new_author = Author(FName, LName, Biography, Publisher)

    # Only add book if it's unique
    db.session.add(new_author)
    db.session.commit()

    # Return new_book as json
    return new_author.product_schema.jsonify(new_author)


@app.route("/books/<ISBN>", methods=["GET"])
def getBookByISBN(ISBN):
    """Returns the book requested by the specific ISBN route"""
    book = Book.query.get(ISBN)

    if book is None:
        return jsonify(None)

    return Book.product_schema.jsonify(book)


@app.route("/books/author/<AUTHOR>", methods=["GET"])
def getBooksByAuthor(AUTHOR):
    """Retrieve a list of books associated with an author"""
    # Get all books
    all_books = Book.query.all()

    # Append the book's name if its author was specified on the URL
    byAuthor = [book.Name for book in all_books if book.Author == AUTHOR]

    # Check that the author has books in the database. If no books are found
    # by the author, return a json message saying so, and suggest authors.
    all_authors = Author.products_schema.dump(Author.query.all())
    if len(byAuthor) == 0:
        return jsonify(
            "No books written by this author in the database.",
            "Here is a list of authors recorded: ",
            all_authors,
        )

    # Returns all the DB items as json
    return jsonify(byAuthor)


# ******************** [4] Book Details ********************
# Create a Product

@app.route('/rating/<book>',methods=['POST'])
def add_rating(book):
    book = request.json['book']
    name = request.json['name']
    rate = request.json['rate']
    comment = request.json['comment']

    new_rating = Rating(book, name, rate, comment)

    db.session.add(new_rating)
    db.session.comit()

    return new_rating.product_schema.jsonify(new_rating)

# Get All product
@app.route('/product/',methods=['GET'])
def  get_product():
    all_product = Product.query.all()
    result = products_schema.dump(all_products)
    return jsonify(result.data)

# write a rate to Product
@app.route('/product/<rate>',methods=['PUT'])
def rate_product(rate):


    id = request.json['id']
    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    qty = request.json['qty']

    product.id = id
    product.name = name
    product.description = description
    product.price =price
    product.qty =qty

    product = Product.query.get(rate)

    db.session.comit()

    return product_schema.jsonify(product)

# write a rate to Product

@app.route('/product/<rate>',methods=['PUT'])
def rate_product(rate):


    id = request.json['id']
    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    qty = request.json['qty']



    product.id = id
    product.name = name
    product.description = description
    product.price =price
    product.qty =qty
    product = Product.query.get(rate)

    db.session.comit()

    return product_schema.jsonify(product)

@app.route('/product/<id>',menthods =['DELETE'])
def delete_product(id):
    product = Product.query.get(id)
    return product_schema.jsonify(product)
