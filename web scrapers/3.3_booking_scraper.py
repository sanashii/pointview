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
from selenium.common.exceptions import StaleElementReferenceException

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

# Function to scrape Booking reviews
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
    review_pages = 1

    # Infinite loop to iterate through reviews
    # while True:
    while review_pages <= 5:  #! FOR TESTING ONLY - maximum number of review pages you want to scrape
        time.sleep(2)

        # Wait for the left score elements to be present
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, './/div[@class="{REVIEW_LEFT_SCORE_XPATH}"]')))

        print(f"Scraping reviews from page {review_pages}...")
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
                room_type.append("N/A") # placeholder if no room was specified


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

            # Handle the page selection
            handle_page_selection()
            review_pages += 1

        except (ElementClickInterceptedException, TimeoutException, NoSuchElementException, WebDriverException) as e:
            print(e)
            break

     # calling the function to save data to csv
    to_csv(score_list, sentiments, identities, travel_type, room_type, stayed, comments, review_date, review_pages)

    # Close the current tab
    driver.close()

    # Switch back to the original tab
    driver.switch_to.window(original_tab)
    
# Step 1: Open Booking.com
url = 'https://www.booking.com/'
driver.get(url)
response = requests.get(url)
print(driver.title)

if response.status_code == 200:
    print("Opened Booking.com...")
else:
    print("Failed to open Booking.com. Exiting.")
    exit()

# ! NOTE: we have to wait for about 5 seconds bc there's a pop-up that appears
pop_up = 0
xpath_to_wait_for = './/div/button[@class="a83ed08757 c21c56c305 f38b6daa18 d691166b09 ab98298258 deab83296e f4552b6561"]' # path for pop up close button
try:
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, xpath_to_wait_for))
    )
    
    ActionChains(driver).move_to_element(element).perform()
    element.click()
    pop_up = 1
    print("Closed the pop-up.")

except TimeoutException:
    print(f"Timed out waiting for element with XPath '{xpath_to_wait_for}' to appear.")

# Step 2: Locate city
while True:
    try:    
        search = input('Input city location: ')
        search = str(search)
        print(search)
        
        # Enter the new search query
        driver.find_element(By.XPATH, './/div/div/div/input[@class="eb46370fe1"]').send_keys(search)
        
        # Wait for the dropdown menu to appear
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, './/ul/li[@class="be14df8bfb"]')))
        
        # Click on the first suggestion in the dropdown menu
        driver.find_element(By.XPATH,'.//ul/li/div[@class="d7430561e2"]').click()
        
    except (NoSuchElementException, TimeoutException):
        print('Your selection is not a city, please check your spelling.')
        continue
    else:
        break


#Step 3: Search and click review box
time.sleep(2)
button = driver.find_element(By.XPATH, './/div/button[@class="a83ed08757 c21c56c305 a4c1805887 f671049264 d2529514af c082d89982 cceeb8986b"]')
driver.execute_script("arguments[0].scrollIntoView(true);", button) # scrolling to bypass calendar overlay
button.click()

# # Wait for the calendar overlay to appear
# try:
#     calendar_overlay = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, './/div/nav[@class="d48f1af7a3 e74a369bda d3ce2af2cd"]')))
#     # Calculate the check-out date (current date + 1 day for overnight stay)
#     check_out_date = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%d")
#     check_in_date = int(check_out_date) - 1  # Convert to integer

#     # Click on the check-out date in the calendar overlay
#     driver.find_element(By.XPATH, f'.//div/nav[@class="d48f1af7a3 e74a369bda d3ce2af2cd"]//td[text()="{check_in_date}"]').click()
#     driver.find_element(By.XPATH, f'.//div/nav[@class="d48f1af7a3 e74a369bda d3ce2af2cd"]//td[text()="{check_out_date}"]').click()

#     button.click()
# except TimeoutException:
#     print("Calendar overlay did not appear within the specified time.")


sleep(randint(1,5)) # random sleeping time between 1 to 6 seconds to mimic human behavior

# Step 4: Transfer to new pop-up window (if needed)
if len(driver.window_handles) > 1:
    driver.switch_to.window(driver.window_handles[1])
    
# Step 4.1: Store the handle of the original tab
original_tab = driver.current_window_handle

# Step 5: looping through pages of lists of hotels
WebDriverWait(driver, 1000).until(EC.presence_of_element_located((By.XPATH, './/div[@class="d4924c9e74"]')))
print('Hotel list is present...')

# another pop up check if ever it wont show up during startup
try:
    if(pop_up == 0):
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, xpath_to_wait_for))
        )
        
        ActionChains(driver).move_to_element(element).perform()
        element.click()
        pop_up = 1
        print("Closed the pop-up.")

except TimeoutException:
    print(f"Timed out waiting for element with XPath '{xpath_to_wait_for}' to appear.")
    
'''
max_pages = driver.find_element(By.XPATH, './/ol/li/button[@class="a83ed08757 a2028338ea"]').text  # Set the maximum number of pages you want to scrape
# # Use regular expression to extract the number
# match = re.search(r'Page \d+ out of (\d+)', max_pages)

# # Check if the pattern was found
# if match:
#     total_pages = int(match.group(1))
'''
max_pages = 1  #! FOR TESTING ONLY - Set the maximum number of pages you want to scrape

for page in range(1, max_pages + 1):
    hotel_list_class = 'bcbf33c5c3' # its not an ol but an array of divs
    hotel_links = driver.find_elements(By.XPATH, f'.//div[@class="{hotel_list_class}"]//a')

    print(f"Found {len(hotel_links)} hotel links on page {page}.")

    for hotel_link in hotel_links:
        time.sleep(5)
        # Simulate opening link in a new tab
        hotel_link.send_keys(Keys.CONTROL + Keys.RETURN)

        time.sleep(2)  # Add a delay to ensure the new tab has opened

        # Switch to the newly opened tab
        all_tabs = driver.window_handles
        new_tab = all_tabs[-1]
        driver.switch_to.window(new_tab)

        hotel_name_element = driver.find_element(By.XPATH, './/div/h2[@class="d2fee87262 pp-header__title"]')
        hotel_name = hotel_name_element.text
        print(f"Switched to the new tab with URL: {driver.current_url}, Hotel name: {hotel_name}")

        # Clicking the review tab
        driver.find_element(By.XPATH, './/div/ul/li/a/span/div/span[contains(text(), "Guest reviews")]').click()
        print('Clicked on the review tab...')
        WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, './/div/div[@class="sliding-panel-widget-content review_list_block one_col"]')))
        print(f"Scraping reviews from {hotel_name}...")
        # scrape_reviews()

#             driver.close()  # Close the new tab
            
#             driver.switch_to.window(original_tab)
#         else:
#             print("No new tab found. Unable to switch.")

#     # Step 10: Navigate to the next page
#     next_page_button_id = 'paginationNext'
#     next_page_button = driver.find_element(By.XPATH, f'.//ol[@class="{next_page_button_id}"]').click()
#     time.sleep(2)  # Add a delay to ensure the new page has loaded


# # After processing all hotel links, switch back to the original tab
# driver.switch_to.window(original_tab)
# print('Scraping completed!')