from bs4 import BeautifulSoup as bs
import pymongo
import flask
from pprint import pprint
from flask import Flask, request, render_template, redirect
from nasa_scrape import scrape

app = Flask(__name__)

def mongo_query(query_name):
    client = pymongo.MongoClient('localhost', 27017)
    db = client['mars']
    collection = db['mars_data']
    col_objects = collection.find()
    for col_object in col_objects:
        return col_object[query_name]

@app.route("/scrape")
def call_scrape():
    client = pymongo.MongoClient('localhost', 27017)
    db = client['mars']
    collection = db['mars_data']
    if collection.count_documents() > 0:
        collection.drop()
    collection.insert_one(scrape())
    return redirect("/", code=302)


@app.route("/")
def home():
    client = pymongo.MongoClient('localhost', 27017)
    headline = mongo_query("article_title")
    content = mongo_query("article_desc")
    featured_image = mongo_query("image_url")
    twitter = mongo_query("twitter")
    facts = mongo_query("dataframe")
    return render_template("index.html", headline=headline, content=content, featured_image=featured_image, twitter=twitter, facts=facts)


if __name__ == "__main__":
    app.run()
