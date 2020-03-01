from bs4 import BeautifulSoup as bs
import pymongo
import flask
from pprint import pprint
from flask import Flask, request, render_template
# from nasa_scrape import scrape
import requests

def my_fun(index_number, query_name):
    client = pymongo.MongoClient("localhost", 27017)
    db = client["mars"]
    collection = db["mars_data"]
    col_objects = collection.find()
    for col_object in col_objects:
        return col_object["hemisphere"][index_number][query_name]

print(my_fun(0, "title"))



# BASE_URL = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

# html = requests.get(BASE_URL).text

# soup = bs(html, "html.parser")

# the_list = soup.find_all("a", class_="itemLink product-item")
# hemisphere_list = []
# for item in the_list:
#     hemisphere_list.append("https://astrogeology.usgs.gov" + item['href'])

# hemisphere_dict = []
# for link in hemisphere_list:
#     new_base = link
#     new_html = requests.get(new_base).text
#     new_soup = bs(new_html, "html.parser")
#     hemisphere_dict.append({
#         "title": new_soup.find("h2", class_="title").text,
#         "img_url": "https://astrogeology.usgs.gov" + (new_soup.find("img", class_="wide-image")['src'])
#         })

# pprint(hemisphere_dict)