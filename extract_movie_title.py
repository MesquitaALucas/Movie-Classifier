from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time

# Set up Chrome WebDriver
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run Chrome in headless mode
chrome_service = Service('/path/to/chromedriver')  # Path to your chromedriver executable
driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

# Load Letterboxd list page
driver.get("https://letterboxd.com/deltanz/list/the-definitive-horror-list-based-on-deltanzs/")  # Your Letterboxd list URL
time.sleep(5)  # Let the page load, adjust the wait time as needed

# If login is required, you may need to add code to handle login here

# Scroll to the bottom of the page to load all movies
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)  # Adjust wait time as needed
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# Extract movie names
movie_elements = driver.find_elements(By.CLASS_NAME, "poster-list-item")
movie_names = [element.find_element(By.CLASS_NAME, "frame").get_attribute("data-target-link") for element in movie_elements]

# Print movie names
for name in movie_names:
    print(name)

# Quit WebDriver
driver.quit()
