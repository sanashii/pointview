from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import ElementClickInterceptedException,WebDriverException, TimeoutException,NoSuchElementException
import time,pandas as pd,re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from urllib.request import urlopen
import requests
from bs4 import BeautifulSoup

# prereqs
chrome_options = Options()
prefs = {"profile.managed_default_content_settings.images": 2}
chrome_options.add_experimental_option("prefs", prefs)
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-popup-blocking")
chrome_options.add_experimental_option("useAutomationExtension", False)
chrome_options.add_argument("--proxy-server='direct://'")
chrome_options.add_argument("--proxy-bypass-list=*")
chrome_options.add_argument("--start-maximized")
#chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)

# Step 1: Open Agoda
url = 'https://www.agoda.com'
driver.get(url)
response = requests.get(url)
print(driver.title)

if response.status_code == 200:
    print("Opened Agoda...")
else:
    print("Failed to open Agoda. Exiting.")
    exit()

# ! NOTE: we have to wait for about 5 seconds bc there's a pop-up that appears
xpath_to_wait_for = './/div/button[@class="ab-close-button"]'
try:
    element = WebDriverWait(driver, 6).until(
        EC.presence_of_element_located((By.XPATH, xpath_to_wait_for))
    )
    print(f"Element with XPath '{xpath_to_wait_for}' is now present.")
    
    ActionChains(driver).move_to_element(element).perform()
    element.click()
    print("Closed the pop-up.")

except TimeoutException:
    print(f"Timed out waiting for element with XPath '{xpath_to_wait_for}' to appear.")

input("Press Enter to close the browser...")

# Close the WebDriver
driver.quit()
# #Step 2: Locate Hotel
# while True:
# 	try:
# 		driver.find_element_by_xpath('.//input[@class="SearchBoxTextEditor SearchBoxTextEditor--autocomplete"]').clear()
# 		search = input('Input name of hotel and location (i.e. <hotel name><space><location>):')
# 		search = str(search)
# 		driver.find_element_by_xpath('.//input[@class="SearchBoxTextEditor SearchBoxTextEditor--autocomplete"]').send_keys(search)
# 		WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,'.//span[@class="Suggestion__categoryName_text"][contains(., "Property")]')))
# 		driver.find_element_by_xpath('.//span[@class="Suggestion__categoryName_text"][contains(., "Property")]').click()
# 	except (NoSuchElementException,TimeoutException):
# 		print('Your Selection is not a propery, please check your spelling.')
# 		continue
# 	else:
# 		break

# # Step 6: Collect the review collection
# reviews = []

# while True:
#     try:
#         # Replace this part with the appropriate URL for reviews
#         review_url = 'https://www.agoda.com/review-url'  # Update this with the actual review URL
#         review_response = requests.get(review_url)
#         review_soup = BeautifulSoup(review_response.content, 'html.parser')

#         # Adjust the following code to match the structure of Agoda reviews page
#         comment_review = review_soup.find_all('div', class_='Review-comment-body')
#         for comment in comment_review:
#             comment_text = comment.get_text(strip=True)
#             print(comment_text)
#             reviews.append(comment_text)
#     except Exception as e:
#         print(f'An error occurred: {e}')
#         break

# # Step 7: Collect the reviews (either Agoda or Booking.com)
# print('Scraping Agoda reviews.....')
# reviews_url = 'https://www.agoda.com/reviews-url'  # Update this with the actual reviews URL
# reviews_response = requests.get(reviews_url)
# reviews_soup = BeautifulSoup(reviews_response.content, 'html.parser')

# # Continue parsing and collecting reviews as needed...

# # End of Agoda scraper
# print('Agoda scraping completed.')
