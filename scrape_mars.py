# import dependendies
from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd
import time

# function to setup a browser object before scraping with splinter
def init_browser():
    executable_path = {'executable_path': 'c:\Chromedriver\chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

# function to scrape mars data
def scrape_info():
    browser = init_browser()

   # scrape NASA Mars News for title and teaser of latest news article
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    time.sleep(1)
    html = browser.html
    soup = BeautifulSoup(html, 'lxml')

    news_title = soup.find(class_='image_and_description_container').find(class_='content_title').find('a').text
    news_p = soup.find(class_='image_and_description_container').find(class_='article_teaser_body').text

    # scrape JPL Mars featured image url
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    time.sleep(1)
    html = browser.html
    soup = BeautifulSoup(html, 'lxml')

    img_url = 'https://www.jpl.nasa.gov'+soup.find('article')['style'].split("'")[-2]

    # scrape the Mars Weather twitter account for the latest tweet about Mars weather
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    time.sleep(1)
    html = browser.html
    soup = BeautifulSoup(html, 'lxml')
    
    tweet = soup.find('li',class_='js-stream-item stream-item stream-item').find('p').text.split('pic')[0]

    # scrape the Space Facts page for Mars info, using Pandas
    url = 'https://space-facts.com/mars/'

    # get the second of two tables
    dfs = pd.read_html(url)
    dfs[1].columns=['Description','Value']
    facts_html = dfs[1].to_html(index=False)

    # scape USGS astrogeoloy site for images of Mars's hemispheres
    hemispheres = ['Valles Marineris Hemisphere','Cerberus Hemisphere','Schiaparelli Hemisphere','Syrtis Major Hemisphere']
    hemisphere_image_urls = []
    
    for hemi in hemispheres:
        url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(url)
        browser.click_link_by_partial_text(hemi)
        html = browser.html
        soup = BeautifulSoup(html, 'lxml')
        hemisphere_image_urls.append({'title':hemi,'img_url':'https://astrogeology.usgs.gov'+ soup.find('img', class_='wide-image')['src']})
   
    # store all the scraped data in a dictionary
    mars_data = {
        'news_title':news_title,
        'news_p':news_p,
        'img_url':img_url,
        'tweet':tweet,
        'facts_html':facts_html,
        'hemisphere_image_urls':hemisphere_image_urls}

    # close the browser after scraping
    browser.quit()

    # return results
    return mars_data