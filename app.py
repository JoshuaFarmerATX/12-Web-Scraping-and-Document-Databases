from bs4 import BeautifulSoup as bs
import pymongo
import flask
from pprint import pprint
from flask import Flask, request, render_template, redirect
from nasa_scrape import scrape

app = Flask(__name__)


def mongo_query(query_name):
    client = pymongo.MongoClient("mongodb://heroku_5cvvmm4p:9r8tct8g2btpdrc1bm539aq0ea@ds161335.mlab.com:61335/heroku_5cvvmm4p", 27017)
    db = client["mars"]
    collection = db["mars_data"]
    col_objects = collection.find()
    for col_object in col_objects:
        return col_object[query_name]


def mongo_hemisphere_query(query_name, index_number):
    client = pymongo.MongoClient("mongodb://heroku_5cvvmm4p:9r8tct8g2btpdrc1bm539aq0ea@ds161335.mlab.com:61335/heroku_5cvvmm4p", 27017)
    db = client["mars"]
    collection = db["mars_data"]
    col_objects = collection.find()
    for col_object in col_objects:
        return col_object["hemisphere"][index_number][query_name]


@app.route("/scrape")
def call_scrape():
    client = pymongo.MongoClient("mongodb://heroku_5cvvmm4p:9r8tct8g2btpdrc1bm539aq0ea@ds161335.mlab.com:61335/heroku_5cvvmm4p", 27017)
    db = client["mars"]
    collection = db["mars_data"]
    if collection.count() > 0:
        collection.drop()
    collection.insert_one(scrape())
    return redirect("/", code=302)


@app.route("/")
def home():
    client = pymongo.MongoClient("mongodb://heroku_5cvvmm4p:9r8tct8g2btpdrc1bm539aq0ea@ds161335.mlab.com:61335/heroku_5cvvmm4p", 27017)
    headline = mongo_query("article_title")
    content = mongo_query("article_desc")
    featured_image = mongo_query("image_url")
    twitter = mongo_query("twitter")
    facts = mongo_query("dataframe")
    hem_one_title = mongo_hemisphere_query("title", 0)
    hem_two_title = mongo_hemisphere_query("title", 1)
    hem_three_title = mongo_hemisphere_query("title", 2)
    hem_four_title = mongo_hemisphere_query("title", 3)
    hem_one_img = mongo_hemisphere_query("img_url", 0)
    hem_two_img = mongo_hemisphere_query("img_url", 1)
    hem_three_img = mongo_hemisphere_query("img_url", 2)
    hem_four_img = mongo_hemisphere_query("img_url", 3)

    return render_template(
        "index.html",
        headline=headline,
        content=content,
        featured_image=featured_image,
        twitter=twitter,
        facts=facts,
        hem_one_title=hem_one_title,
        hem_two_title=hem_two_title,
        hem_three_title=hem_three_title,
        hem_four_title=hem_four_title,
        hem_one_img=hem_one_img,
        hem_two_img=hem_two_img,
        hem_three_img=hem_three_img,
        hem_four_img=hem_four_img,
    )


if __name__ == "__main__":
    app.run()
