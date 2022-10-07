from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

#driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))


driver = webdriver.Chrome("C:\\Users\\дом.DESKTOP-A3U9TO1\\DataspellProjects\\moretech_prokhodilimimo\\chromedriver\\chromedriver.exe")
driver.get("https://www.google.com")