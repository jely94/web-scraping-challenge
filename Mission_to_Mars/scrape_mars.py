# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import time
from selenium.webdriver.chrome.options import Options  

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    options = Options()
    options.add_argument('--no-sandbox') # Bypass OS security model

    executable_path = {'executable_path': '../chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False, chrome_options=options)
    news_title, news_paragraph = scrape_mars_news(browser)    

# Create dictionary to hold Mars info to be imported into Mongo
    mars_info = {
    'news_title': news_title,
    'news_p': news_p,
    'nasa_photo': nasa_photo,
    'mars_facts_table': mars_facts_table,
    'hemisphere_image_urls': hemisphere_image_urls
    }
    browser.quit()
    return mars_info

# Nasa Mars News Scrape
def scrape_mars_news(browser):

        # Navigate to the NASA Mars News Site
        url = 'https://mars.nasa.gov/news/'
        browser.visit(url)

        # HTML object
        html = browser.html
        # Parse HTML with Beautiful Soup
        soup = BeautifulSoup(html, 'html.parser')

        # Find the first headline title and assign to a variable
        nasa_header = soup.find('li', class_='slide')
        news_title = nasa_header.find('div', class_='content_title').text

        # Find the first headline paragraph and assign to a variable
        news_p = nasa_header.find('div', class_='article_teaser_body').text

        # Add to mars_info dictionary
        # mars_info['news_title'] = news_title
        # mars_info['news_p'] = news_p

        return news_title, news_p


# NASA Featured Image Scrape
def scrape_feat_image(browser):

        # Navigate to the JPL Images Site and click to get the full image
        url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
        base_url = 'https://www.jpl.nasa.gov'
        browser.visit(url)
        browser.find_by_id('full_image').click()
        browser.links.find_by_partial_text('more info').click()
        time.sleep(1)

        # HTML object
        html = browser.html
        # Parse HTML with Beautiful Soup
        soup = BeautifulSoup(html, 'html.parser')

        # Assign image path to variable
        nasa_photo = soup.find('img', class_='main_image')['src']

        return nasa_photo

# Mars Facts Scrape
def scape_mars_facts(browser):

        # Use Pandas to scrape Mars facts data
        tables = pd.read_html('https://space-facts.com/mars/')

        # Convert 1st table to dataframe
        mars_df = tables[0]

        # Name columns and reset index
        mars_df.columns=['Description', 'Value']
        mars_facts_table = mars_df.to_html(table_id="html_tbl_css",justify='left',index=False)

        return mars_facts_table

# Mars Hemisphere Scrape
def scrape_mars_hemispheres(browser):

        # Navigate to the astrogeology site to get hemisphere images
        url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(url)

        # HTML object
        html = browser.html

        # Parse HTML with Beautiful Soup
        soup = BeautifulSoup(html, 'html.parser')

        # Retreive all items that contain mars hemispheres information
        items = soup.find_all('div', class_='item')

        # Create empty list for hemisphere urls 
        hemisphere_image_urls = []

        # Assign the main url to variable
        hemispheres_url = 'https://astrogeology.usgs.gov'

        # Loop through items
        for i in items: 
            # Store the hemisphere title
            title = i.find('h3').text
    
            # Assign the link to the full image to a variable
            img_url = i.find('a', class_='itemLink product-item')['href']
    
            # Navigate to the link by combining the two urls
            browser.visit(hemispheres_url + img_url)
    
            # HTML Object 
            img_html = browser.html
    
            # Parse HTML with Beautiful Soup for every individual hemisphere information website 
            soup = BeautifulSoup(img_html, 'html.parser')
    
            # Assign the  full image source to a variable 
            full_img_url = hemispheres_url + soup.find('img', class_='wide-image')['src']
    
            # Append the retreived information into a list of dictionaries 
            hemisphere_image_urls.append({"title" : title, "img_url" : full_img_url})

        return hemisphere_image_urls


