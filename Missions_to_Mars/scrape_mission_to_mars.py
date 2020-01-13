
def scrape():

        # Dependencies
    from bs4 import BeautifulSoup
    import requests
    import os
    import pymongo
    from splinter import Browser
    import time
    import pandas as pd

    

    # # NASA Mars News
    # Scrape the NASA Mars News Site and collect the latest News Title and Paragraph Text. Assign the text to variables that you can reference later.

    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    url_mars = 'https://mars.nasa.gov/news/'
    browser.visit(url_mars)
    html_MARS = browser.html
    soup_MARS = BeautifulSoup(html_MARS, "html.parser")

    #Title text of latest article
    NASAMarsNews_latest_title = soup_MARS.find("div", class_ = "content_title").text.strip()

    #Print text of Paragraph of latest article
    NASAMarsNews_latest_paragraph = soup_MARS.find("div", class_ = "article_teaser_body").text.strip()



    # # JPL Mars Space Images - Featured Image
    # Visit the url for JPL Featured Space Image here.
    # Use splinter to navigate the site and find the image url for the current Featured Mars Image and assign the url string to a variable called featured_image_url.
    # Make sure to find the image url to the full size .jpg image.
    # Make sure to save a complete url string for this image.


    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    url_JPL = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url_JPL)


    browser.click_link_by_partial_text("FULL IMAGE")
    #Let's make them not suspicious I'm a robot, put the search to sleep
    time.sleep(5)

    # Keep scraping/searching, go to "More Info" of that image
    browser.click_link_by_partial_text("more info")

    # Parse the HTML where you just arrived with Beautiful Soup
    html_JPL = browser.html
    soup_JPL = BeautifulSoup(html_JPL, "html.parser")

    featuredImage = soup_JPL.find('figure', class_='lede').a["href"]
    featuredImage = f'https://jpl.nasa.gov{featuredImage}'


    # # Mars Weather
    # Visit the Mars Weather twitter account here and scrape the latest Mars weather tweet from the page. Save the tweet text for the weather report as a variable called mars_weather.

    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    url_TW = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url_TW)

    # Parse the HTML where you just arrived with Beautiful Soup
    html_TW = browser.html
    soup_TW = BeautifulSoup(html_TW, "html.parser")

    # Extract latest tweet
    tweet_container = soup_TW.find_all('div', class_="js-tweet-text-container")

    # Loop through latest tweets and find the tweet that has weather information
    for tweet in tweet_container: 
        mars_weather = tweet.find('p').text
        if 'sol' and 'pressure' in mars_weather:
            print(mars_weather)
            break
        else: 
            pass

    tuit = tweet.text.strip()


    # # Mars Facts
    # Visit the Mars Facts webpage here and use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
    # Use Pandas to convert the data to a HTML table string.

    url_mars_table = 'https://space-facts.com/mars/'
    mars_table = pd.read_html(url_mars_table)

    mars_facts = mars_table[0]

    NewColumns = {0: "Characteristics", 1:"Figures"}
    mars_facts = mars_facts.rename(columns=NewColumns)
    mars_facts.head(3)
    mars_facts_HTML_table = mars_facts.to_html("Mars-Facts-Table.html")


    # # Mars Hemispheres
    # Visit the USGS Astrogeology site here to obtain high resolution images for each of Mar's hemispheres.
    # You will need to click each of the links to the hemispheres in order to find the image url to the full resolution image.
    # Save both the image url string for the full resolution hemisphere image, and the Hemisphere title containing the hemisphere name. Use a Python dictionary to store the data using the keys img_url and title.
    # Append the dictionary with the image url string and the hemisphere title to a list. This list will contain one dictionary for each hemisphere.

    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    hemisphere =[]
    hemisphere_list=['Cerberus','Schiaparelli','Syrtis','Valles']
    for hemi in hemisphere_list:
        hemispheres={}
        url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(url)
        html = browser.html
        soup = BeautifulSoup(html,'html.parser')
        browser.click_link_by_partial_text(hemi)
        html = browser.html
        soup = BeautifulSoup(html,'html.parser')
        hemispheres['image']=soup.find('a',target="_blank")['href']
        hemispheres['title']=soup.find('h2',class_="title").text
        hemisphere.append(hemispheres)


    # In the scrape_mars.py, the scrape function is to be moved above all operations

        mars_data = {}
        mars_data["news_title"] = NASAMarsNews_latest_title
        mars_data["news_paragraph"] = NASAMarsNews_latest_paragraph
        mars_data["featured_image"] = featuredImage
        mars_data["weather"] = tuit
        mars_data["mars_facts_table"] = mars_facts_HTML_table
        mars_data["hemispheres"] = hemisphere
        
        return mars_data

