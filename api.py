from flask import Flask,request
import glob
import json
app = Flask(__name__)
app.debug = True

PATH_TO_BOOKS = "/root/api/books/"

book_list = glob.glob(PATH_TO_BOOKS+"*.txt")

import pymongo
client = pymongo.MongoClient()
book_places = client.fastread.bookplace

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/book_names')
def book_names():
    uid = request.args.get("uid")
    ls = []
    for book in book_list:
        one = book_places.find_one({"book":book,"uid":uid})
        if one:
            one.pop("uid")
            ls.append(one)
        else:
            ls.append({"book":book,"word":0})
    return json.dumps({"books":ls})

@app.route('/get_book', methods=["POST"])
def get_book():
    book = request.args.get("book")

    print "The book is: "+book
    if book in book_list:
        f = open(book, "r")
        book = f.read().split(" ")
        book = filter(None, book)
        return str(book)
    else:
        return "Book not found"

@app.route("/set_my_place", methods=["POST"])
def set_my_place():
    book = request.args.get("book")
    uid = request.args.get("uid")
    word = int(request.args.get("word"))
    a = book_places.update({"book":book,"uid":uid},{"book":book,"uid":uid,"word":word},upsert=True)
    return str(a)


@app.route("/get_my_place", methods=["POST"])
def get_my_place():
    book = request.args.get("book")
    uid = request.args.get("uid")

    return str(book_places.find_one({"book":book,"uid":uid}))


if __name__ == '__main__':
    app.run()
