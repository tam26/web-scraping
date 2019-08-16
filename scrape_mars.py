#Import Dependancies
import requests
import pandas as pd

from splinter import Browser
from bs4 import BeautifulSoup as bs

#Initialize Browser/Path to Chromedriver

def initial_browser():
    executable_path = {'executable_path': '/Users/tamaranajjar/Documents/BOOTCAMP/NUCHI201905DATA2/12-Web-Scraping-and-Document-Databases/Homework/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

#Initial Scrape

def scrape():
    browser = initial_browser()
    mars_data = {}

#Scrape News

def scrape_news():
    
    news_url = 'https://mars.nasa.gov/news/'

    browser.visit(news_url)
    news_soup = bs(browser.html, 'html.parser')

    news_list = news_soup.find('ul', class_='item_list')
    item_1 = news_list.find('li', class_='slide')

    news_title = item_1.find('div', class_='content_title').text
    news_p = item_1.find('div', class_='article_teaser_body').text

    mars_data['news_title'] = news_title
    mars_data['news_paragraph'] = news_p

    return news_title, news_p

#Scrape Facts Table

def scrape_facts_table():
    facts_url = 'https://space-facts.com/mars/'

    mars_table = pd.read_html(facts_url)
    mars_table_edit = mars_table[1]
    mars_table_mapping = {0: "Specifications", 1:"Measurements"}
    mars_facts = mars_table_edit.rename(columns = mars_table_mapping)

    mars_data['mars_facts'] = mars_facts

    return mars_facts.to_html('mars_facts.html', index=False)

#Scrape Image

def scrape_image():
    base_url = 'https://www.jpl.nasa.gov'
    image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

    browser.visit(image_url)
    browser.click_link_by_partial_text('FULL IMAGE')

    image_html = browser.html
    image = bs(image_html, 'html.parser').find('img', class_='fancybox-image')['src']

    featured_image = base_url + image
    
    mars_data['mars_image'] = featured_image
    
    return featured_image

#Scrape Weather

def scrape_weather():

    weather_url = 'https://twitter.com/marswxreport?lang=en'

    browser.visit(weather_url)
    weather_soup = bs(browser.html, 'html.parser')

    weather_tweet = weather_soup.find('p', class_='TweetTextSize').text
    
    mars_data['mars_weather'] = mars_facts

    return weather_tweet

#Scrape Hemispheres

def scrape_hemisphere():
    h_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

    browser.visit(h_url)
    h_pictures = []
    h_list = browser.find_by_css("a.product-item h3")

    for h in range(len(h_list)):
        h_dict = {}
        browser.find_by_css("a.product-item h3")[h].click()
        h_click = browser.find_link_by_text('Sample').first
        h_dict["title"] = browser.find_by_css("h2.title").text
        h_dict["image_url"] = h_click["href"]
        h_pictures.append(h_dict)
        browser.back()
    
    mars_data['mars_hemispheres'] = h_pictures

    return h_pictures