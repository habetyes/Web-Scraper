from bs4 import BeautifulSoup as bs
from splinter import Browser
import pymongo
import requests
import time
import pandas as pd

def init_browser():
    """ INITIALIZES BROWSER: THIS MAY NEED TO BE REPLACED WITH YOUR PATH TO CHROME DRIVER """
    executable_path = {"executable_path": 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    return browser

def mars_news():
    """ SCRAPES MARS NEWS SITE TO GRAB LATEST TITLE AND DESCRIPTION"""
    browser = init_browser()
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    time.sleep(1)
    html = browser.html
    soup = bs(html, 'html.parser')
    results = soup.find('div', class_ = 'content_title')
    news_title = results.text.lstrip()

    # # FIRST PARAGRAPH
    soup = bs(html, 'html.parser')
    results = soup.find('div', class_ = 'article_teaser_body')
    news_p = results.text.lstrip()
    browser.quit()
    return {'title': news_title, 'paragraph': news_p}

def mars_image():
    browser = init_browser()
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    # SEND BROWSER TO URL AND SLEEP TO LET PAGE FULLY LOAD
    browser.visit(url)
    time.sleep(1)
    html = browser.html
    soup = bs(html, 'html.parser')

    # CLICK ON PROMPTS WHICH WILL TAKE US TO THE PAGE WHICH HOUSES THE FULL SIZE IMAGE
    # Pause between each page to allow page to fully load
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(1)
    browser.click_link_by_partial_text('more info')
    time.sleep(1)

    # RE-READ HTML IN ORDER TO FIND ELEMENT
    html = browser.html
    soup = bs(html, 'html.parser')
    img_link = soup.find('figure', class_ = 'lede').find('a')['href']
    time.sleep(1)

    # SPLINTER DOCUMENTATION SHOWS HOW TO CLICK LINK BY HREF. PASS IN HREF (EXTRACTED ABOVE) TO SELECT CORRECT ONE
    browser.click_link_by_href(img_link)

    # CAPTURE FINAL IMAGE URL INTO VARIABLE
    featured_image_url = browser.url
    browser.quit()
    return(featured_image_url)

def mars_weather():
    browser = init_browser()
    url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')
    result = soup.find_all('div', class_='js-tweet-text-container')[0].text
    x = result.split('pic.twitter')[0]
    x
    mars_weather = x.split('\n')[1]
    browser.quit()
    return(mars_weather)

def mars_facts():
    browser = init_browser()
    url = 'https://space-facts.com/mars/'
    # SCRAPE TABLES WITH PANDAS AND WRITE TO HTML
    table = pd.read_html(url)
    df = table[0]
    df.columns = ['Metric', 'Measurement']
    df.set_index('Metric', inplace=True)
    html_table = df.to_html()
    browser.quit()
    return(html_table)

def mars_hemispheres():
    browser = init_browser()
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')
    images = soup.find_all('div', class_='item')

    # CAPTURE BASE URL TO APPEND HREF TO WITHIN LOOP
    base = url.split('/search')[0]
    hemisphere_image_urls = []

    for image in images:
    # empty dictionary which will be populated within each iteration
        mt_dict = {}
        
    # navigate to link page to capture appropriate link    
        link = image.a['href']
        image_link = base+link
    # send browser to page which contains appropriate link
        browser.visit(image_link)
        time.sleep(1)
    # re-read html
        html2 = browser.html
        soup2 = bs(html2, 'html.parser')
        title = soup2.find('h2', class_ ='title')
        title = title.text.lstrip()
        url2 = soup2.find('div', class_ = 'downloads').find('a')['href']
        mt_dict['title'] = title
        mt_dict['img_url'] = url2
        
    #Append dictionary of this iteration into list
        hemisphere_image_urls.append(mt_dict)
    browser.quit()    
    return(hemisphere_image_urls)

def scrape():
    mars_data = {
    "news_header": mars_news()['title'],
    "news_body": mars_news()['paragraph'],
    "featured_image": mars_image(),
    "tweet": mars_weather(),
    "table": mars_facts(),
    "hemisphere": mars_hemispheres()
    }

   
    # Return results
    return mars_data
