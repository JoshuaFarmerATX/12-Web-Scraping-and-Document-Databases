from bs4 import BeautifulSoup as bs
import pymongo
import flask
from pprint import pprint
from flask import Flask, request, render_template
from nasa_scrape import scrape

client = pymongo.MongoClient('localhost', 27017)
db = client['mars']
collection = db['mars_data']
col_objects = collection.find()
for col_object in col_objects:
    print(col_object['article_title'])