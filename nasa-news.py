from selenium import webdriver
from bs4 import BeautifulSoup as bs
import urllib.parse
import requests
from pprint import pprint
import pandas as pd
import lxml


def scrape():
    # First Website Scraping
    BASE_URL = "https://mars.nasa.gov/news/"
    FILE = "nasa-news.txt"

    driver = webdriver.Firefox()
    driver.get(BASE_URL)
    html = driver.page_source
    driver.implicitly_wait(10)
    driver.close()

    with open(FILE, "w+", encoding="utf-8") as f:
        f.write(html)

    soup = bs(html, "html.parser")

    title_div_class = "content_title"
    desc_div_class = "article_teaser_body"

    article_title = soup.find("div", class_=title_div_class).text
    article_desc = soup.find("div", class_=desc_div_class).text

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
    dfs = pd.read_html(text, index_col=0)
    html_dfs = dfs[0].to_html()

    # Creates the dictionary with all scrapped values
    scraped_dic = {
        "Article Title": article_title,
        "Article Desc": article_desc,
        "Image URL": full_image_url,
        "Twitter": twitter,
        "Dataframe": html_dfs
    }

    return scraped_dic

scrape_dictionary = scrape()
pprint(scrape_dictionary)

