from selenium import webdriver
from bs4 import BeautifulSoup as bs
import urllib.parse
import requests
import json
from pprint import pprint
import pandas as pd
import lxml


def scrape():
    # Nasa News Scrape
    URL = "https://mars.nasa.gov/api/v1/news_items/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    response = requests.get(URL).json()
    article_title = response["items"][0]["title"]
    article_desc = response["items"][0]["description"]

    # This begins script for the image URL
    IMG_URL = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"

    IMG_HTML = requests.get(IMG_URL).text

    img_soup = bs(IMG_HTML, "html.parser")
    image = img_soup.find("img", class_="thumb")["src"]
    full_image_url = "https://www.jpl.nasa.gov" + image

    # This begins the script for the twitter scrapping
    TWITTER_URL = "https://twitter.com/marswxreport?lang=en"
    TWITTER_HTML = requests.get(TWITTER_URL).text

    TWITTER_SOUP = bs(TWITTER_HTML, "html.parser")
    twitter = TWITTER_SOUP.find("p", class_="TweetTextSize").text

    # This is the Pandas DF scrape
    r = requests.get("http://space-facts.com/mars/")
    text = r.text
    dfs = pd.read_html(text)
    html_dfs = dfs[0].rename(columns={0: "name", 1: "value"}).to_dict(orient="records")

    # This section is the hemisphere scrape
    BASE_URL = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

    html = requests.get(BASE_URL).text

    soup = bs(html, "html.parser")
    base_two = "https://astrogeology.usgs.gov/" + (soup.find("a", class_="itemLink product-item")['href'])
    html_two = requests.get(base_two).text
    soup_two = bs(html_two, "html.parser")

    hemisphere_dict = {
        "title": soup_two.find("h2", class_="title").text,
        "img_url": "https://astrogeology.usgs.gov" + (soup_two.find("img", class_="wide-image")['src'])
    }

    # Creates the dictionary with all scrapped values
    scraped_dic = {
        "article_title": article_title,
        "article_desc": article_desc,
        "image_url": full_image_url,
        "twitter": twitter,
        "dataframe": html_dfs,
        "hemisphere": hemisphere_dict
    }

    return scraped_dic

scrape_dictionary = scrape()
pprint(scrape_dictionary)

