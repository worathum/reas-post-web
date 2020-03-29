# -*- coding: utf-8 -*-

#INSTALL
'''
pip install selenium;
sudo apt-get install chromium-chromedriver
'''
#REF
'''
install google chrome stable https://askubuntu.com/questions/510056/how-to-install-google-chrome
install chromedriver https://makandracards.com/makandra/29465-install-chromedriver-on-linux
https://duo.com/decipher/driving-headless-chrome-with-python
https://www.guru99.com/selenium-python.html
https://medium.com/cs-note/web-crawling-by-using-selenium-python-3-4fff0bdb4c65
'''


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
#from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.common.keys import Keys

options = Options()
options.add_argument("--headless") # Runs Chrome in headless mode.
options.add_argument('--no-sandbox') # # Bypass OS security model
options.add_argument('start-maximized')
options.add_argument('disable-infobars')
options.add_argument("--disable-extensions")
driver = webdriver.Chrome(options=options)
driver.get("http://google.com/")


print ("Headless Chrome Initialized on Linux OS")
