# Import dependecies
from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
from webdriver_manager.chrome import ChromeDriverManager
import requests
import pandas as pd

#define scrape function
def scrape():
    #Set up for splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser("chrome", **executable_path, headless=False)

    #visit the mars news site
    url = "https://redplanetscience.com/"
    browser.visit(url)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    #get the title and paragraph
    news_title = soup.find('div', class_='content_title').text.strip()
    news_p = soup.find('div', class_='article_teaser_body').text.strip()
    
    #visit the mars image site
    url = "https://spaceimages-mars.com/"
    browser.visit(url)
    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")
    #get the image url
    relative_image_path = soup.find_all('img')[1]["src"]
    image_url = url + relative_image_path
    
    #mars facts
    url = 'https://galaxyfacts-mars.com/'
    #read the tables
    tables = pd.read_html(url)
    df = tables[0]
    html_table = df.to_html(classes=["table-striped","table"])

    #mars hemisphere   
    url = "https://marshemispheres.com"
    browser.visit(url)
    mars_hemi = []
    for i in range(4):
        browser.find_by_css("a.product-item img")[i].click()
        hemi= {"img_url":browser.find_by_text("Sample")[0]["href"], "title": browser.find_by_css("h2.title").text}
        mars_hemi.append(hemi)
        browser.back()
   

    mars_data = {
        "news_title": news_title,
        "news_paragraph": news_p,
        "featured_img": image_url,
        "info_tables": html_table,
        "hemi_list": mars_hemi
    }
    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data

