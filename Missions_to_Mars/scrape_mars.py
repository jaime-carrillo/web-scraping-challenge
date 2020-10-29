from bs4 import BeautifulSoup
import requests
import pandas as pd
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import time

def init_browser():
    executable_path = {"executable_path": ChromeDriverManager().install()}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    browser = init_browser()

    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)
    time.sleep(10)


    html = browser.html
# Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')


    li_slide = soup.find('li', class_ = 'slide')


    news_title = li_slide.find('div', class_ = 'content_title').a.text


    news_par = li_slide.find('div', class_ = 'article_teaser_body').text


    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    time.sleep(10)


    browser.links.find_by_partial_text("FULL IMAGE").click()


    browser.links.find_by_partial_text("more info").click()


    html = browser.html
# Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')


    img_href = soup.find("figure", class_ = "lede").a["href"]


    featured_image_url = 'https://www.jpl.nasa.gov' + img_href


    space_facts = pd.read_html("https://space-facts.com/mars/")[0]


    space_facts.columns = ["Description","Facts"]
    space_facts.set_index("Description", inplace = True)


    mars_facts = space_facts.to_html()


    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    time.sleep(10)


    hemisphere_images_url = []
    hemispheres = browser.find_by_css("a.product-item h3")
    for i in range (len(hemispheres)):
        data = {}
        browser.find_by_css("a.product-item h3")[i].click()
        data["image_url"] = browser.links.find_by_text("Sample").first["href"]
        data["title"] = browser.find_by_css("h2.title").text
        hemisphere_images_url.append(data)
        browser.back()


    browser.quit()

    return {
        "news_title": news_title,
        "news_par": news_par,
        "feature_image": featured_image_url,
        "mars_facts": mars_facts,
        "hemispheres": hemisphere_images_url
    }


