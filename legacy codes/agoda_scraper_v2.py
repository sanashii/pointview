from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import ElementClickInterceptedException,WebDriverException, TimeoutException,NoSuchElementException
import time,pandas as pd
from random import randint
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions
from urllib.request import urlopen
import requests
import re
from bs4 import BeautifulSoup

import logging

# Suppressing "ERROR:device_event_log_impl.cc" messages
logging.getLogger('urllib3').setLevel(logging.ERROR)


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
chrome_options.add_argument("--ignore-certificate-errors")
#chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=chrome_options)
REVIEW_LEFT_SCORE_XPATH = './/div[@class="Review-comment-leftScore"]'

# function to switch to original tab (for multiple pages in 1 tab)
def switch_to_original_tab():
    all_tabs = driver.window_handles
    driver.switch_to.window(all_tabs[0])

# Function to handle page selection
def handle_page_selection():
    try:
        # Find the current page number
        current_page = driver.find_element(By.XPATH, './/span[@class="Typographystyled__TypographyStyled-sc-j18mtu-0 croywR kite-js-Typography Review-paginator-number Review-paginator-number--current"]').text
        current_page = int(current_page)

        # Click the right button to move to the next page
        right_button = driver.find_element(By.XPATH, './/i[@class="ficon ficon-24 ficon-carrouselarrow-right"]').click()

        # Wait for the next set of reviews to load
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, REVIEW_LEFT_SCORE_XPATH)))
        time.sleep(2)  # Add additional wait if necessary

        print(f"Moved from page {current_page} to the next page.")

    except NoSuchElementException:
        print("Page selection not found or reached the last page.")

# Function to save data to CSV
def to_csv(score_list, sentiments, identities, travel_type, room_type, stayed, comments, review_date, review_pages):
    # Creating DataFrames and saving to CSV
    for i in range(1, review_pages + 1):
        sentiments = pd.DataFrame(sentiments, columns=['sentiments'])
        identities = pd.DataFrame(identities, columns=['location'])
        travel_type = pd.DataFrame(travel_type, columns=['travel_type'])
        room_type = pd.DataFrame(room_type, columns=['room_type'])
        stayed = pd.DataFrame(stayed, columns=['stayed'])
        score = pd.DataFrame(score_list, columns=['score'])
        comments = pd.DataFrame(comments, columns=['comments'])
        review_date = pd.DataFrame(review_date, columns=['review_date'])
        comments['location'] = identities['location']
        comments['sentiments'] = sentiments['sentiments']
        comments['travel_type'] = travel_type['travel_type']
        comments['room_type'] = room_type['room_type']
        comments['stayed'] = stayed['stayed']
        comments['score'] = score['score']
        comments['review_date'] = review_date['review_date']
        comments.to_csv(search + " " + i + '.csv', index=False)
    print('Comments Saved...')

# Function to scrape Agoda reviews
def scrape_reviews():
    # Lists to store scraped data
    score_list = []
    sentiments = []
    identities = []
    travel_type = []
    room_type = []
    stayed = []
    comments = []
    review_date = []
    review_pages = 0

    # Infinite loop to iterate through reviews
    # while True:
    while review_pages < 5:  # Set a limit to the number of pages to scrape
        time.sleep(2)

        # Wait for the left score elements to be present
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, './/div[@class="{REVIEW_LEFT_SCORE_XPATH}"]')))

        print("Scraping reviews...")
        # Get the HTML content after the page has loaded
        page_source = driver.page_source

        # Use BeautifulSoup to parse the HTML content
        soup = BeautifulSoup(page_source, 'html.parser')

        # Extract data using BeautifulSoup
        for number in soup.select('.{REVIEW_LEFT_SCORE_XPATH}'):
            score_list.append(number.get_text(strip=True))

        for sent in soup.select('.Review-comment-leftScoreText'):
            sentiments.append(sent.get_text(strip=True))

        for date in soup.select('.Review-statusBar-date'):
            review_date.append(date.get_text(strip=True))

        for loc in soup.select('[Review-comment-reviewer data-info-type="reviewer-name"]'):
            loc = loc.get_text(strip=True).split("from")[1:]
            loc = ",".join(loc).strip(" ")
            identities.append(loc)

        for travel in soup.select('[Review-comment-reviewer data-info-type="group-name"]'):
            travel_type.append(travel.get_text(strip=True))

        for room in soup.select('[Review-comment-reviewer data-info-type="room-type"]'):
            room_text = room.get_text(strip=True)
            if room_text:
                room_type.append(room_text)
            else:
                room_type.append("N/A")  # placeholder if no room was specified

        for stay in soup.select('[data-info-type="stay-detail"]'):
            stayed.append(stay.get_text(strip=True))

        for comment in soup.select('.Review-comment-body'):
            comment = comment.get_text(strip=True).replace('\n', ',').replace('”,', ',')
            comments.append(comment)
            print(comment)

        try:
            # Click the "Dismiss" button to move to the next set of reviews
            driver.find_element(By.XPATH, './/*[@class="BackToSearch-dismissText"][contains(., "Dismiss")]').click()
            time.sleep(2)

        except (ElementClickInterceptedException, TimeoutException, NoSuchElementException, WebDriverException) as e:
            print(e)
            break
        review_pages += 1

    # calling the function to save data to csv
    to_csv(score_list, sentiments, identities, travel_type, room_type, stayed, comments, review_date, review_pages)


# Step 1: Open Agoda
time.sleep(10)
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
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, xpath_to_wait_for))
    )

    ActionChains(driver).move_to_element(element).perform()
    element.click()
    print("Closed the pop-up.")

except TimeoutException:
    print(f"Timed out waiting for element with XPath '{xpath_to_wait_for}' to appear.")

# Step 2: Locate hotel
while True:
	try:
		driver.find_element(By.XPATH, './/input[@class="SearchBoxTextEditor SearchBoxTextEditor--autocomplete"]').clear()
		search = input('Input hotel name & location:')
		search = str(search)
		driver.find_element(By.XPATH, './/input[@class="SearchBoxTextEditor SearchBoxTextEditor--autocomplete"]').send_keys(search)
		WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,'.//li[@class="Suggestion__subtext Suggestion__subtext__update"][contains(., "Property")]')))
		driver.find_element(By.XPATH, './/span[@class="Suggestion__categoryName_subtext"][contains(., "Property")]').click()
	except (NoSuchElementException,TimeoutException):
		print('Your selection is not a city, please check your spelling.')
		continue
	else:
		break

# Step 3: Search and click review box
time.sleep(2)
WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, './/div[@class="Box-sc-kv6pi1-0 sc-hlTvYk gGiMIZ eMcHMY IconBox IconBox--checkIn IconBox--focused IconBox--focussable"]')))
driver.find_element(By.XPATH, './/div[@class="Box-sc-kv6pi1-0 sc-hlTvYk gGiMIZ eMcHMY IconBox IconBox--checkIn IconBox--focused IconBox--focussable"]').click()
driver.find_element(By.XPATH, './/div/button[@class="Buttonstyled__ButtonStyled-sc-5gjk6l-0 iCZpGI Box-sc-kv6pi1-0 fDMIuA"]').click()
sleep(randint(1,5)) # random sleeping time between 1 to 6 seconds to mimic human behavior
print('Clicked on the review box...')

# Step 4: Transfer to new pop-up window (if needed)
if len(driver.window_handles) > 1:
    driver.switch_to.window(driver.window_handles[1])

# Step 4.1: Store the handle of the original tab
original_tab = driver.current_window_handle

# Step 5: Scrape reviews of the selected hotel
WebDriverWait(driver, 1000).until(EC.presence_of_element_located((By.XPATH, './/ol[@class="hotel-list-container"]')))
print('Hotel list is present...')

# Click on the first hotel link in the list
ordered_list_class = 'hotel-list-container'
hotel_link = driver.find_elements(By.XPATH, f'.//ol[@class="{ordered_list_class}"]/li/div/a')
hotel_link[0].click()

# Switch to the new tab
all_tabs = driver.window_handles
if len(all_tabs) > 1:
    new_tab = all_tabs[-1]
    driver.switch_to.window(new_tab)

try:
    WebDriverWait(driver, 100).until(EC.new_window_is_opened(all_tabs))
    print("Switched to the new tab successfully.")
except TimeoutException:
    print("Timed out waiting for the new tab to open.")

# Optionally adjust the wait time based on the actual loading times
try:
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, './/div[@class="ReviewScoreCompact__section"]')))
    print("New tab is fully loaded.")
except TimeoutException:
    print("Timed out waiting for the new tab to be fully loaded.")

hotel_name = driver.find_element(By.XPATH, './/div/p[@class="HeaderCerebrum__Name"]').text
print(f"Scraping reviews from {hotel_name}...")
scrape_reviews()

driver.close()
print('Scraping completed!')