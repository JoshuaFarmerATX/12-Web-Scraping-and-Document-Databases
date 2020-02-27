from bs4 import BeautifulSoup as bs
import pymongo
import flask
from pprint import pprint
from flask import Flask, request, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == '__main__':
    app.run()