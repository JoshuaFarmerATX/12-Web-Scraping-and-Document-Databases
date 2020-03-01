from bs4 import BeautifulSoup as bs
import pymongo
import flask
from pprint import pprint
from flask import Flask, request, render_template, redirect
from nasa_scrape import scrape

def call_scrape():    
    client = pymongo.MongoClient("mongodb://heroku_5cvvmm4p:9r8tct8g2btpdrc1bm539aq0ea@ds161335.mlab.com:61335/heroku_5cvvmm4p", 27017)
    db = client["mars"]
    collection = db["mars_data"]
    if collection.count() > 0:
        collection.drop()
    collection.insert_one(scrape())
    return redirect("/", code=302)