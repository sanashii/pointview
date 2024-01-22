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
from selenium.webdriver.firefox.options import Options
from urllib.request import urlopen
#Step 1 Call Browser
chrome_options = webdriver.ChromeOptions()
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
driver = webdriver.Chrome(chrome_options=chrome_options)

#Step 2: Open Agoda
driver.get('https://www.agoda.com')
print ("Opened Agoda...")
time.sleep(2)
element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,'.//div[@class="IconBox IconBox--autocomplete"]')))
ActionChains(driver).move_to_element(element).perform()
element.click()
#Step 3: Locate Hotel
while True:
	try:
		driver.find_element_by_xpath('.//input[@class="SearchBoxTextEditor SearchBoxTextEditor--autocomplete"]').clear()
		search = input('Input name of hotel and location (i.e. <hotel name><space><location>):')
		search = str(search)
		driver.find_element_by_xpath('.//input[@class="SearchBoxTextEditor SearchBoxTextEditor--autocomplete"]').send_keys(search)
		WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,'.//span[@class="Suggestion__categoryName_text"][contains(., "Property")]')))
		driver.find_element_by_xpath('.//span[@class="Suggestion__categoryName_text"][contains(., "Property")]').click()
	except (NoSuchElementException,TimeoutException):
		print('Your Selection is not a propery, please check your spelling.')
		continue
	else:
		break

'''#Step 4: Search and click review box
time.sleep(2)
WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,'.//div[@class="IconBox IconBox--checkIn IconBox--focused"]')))
driver.find_element_by_xpath('.//div[@class="IconBox IconBox--checkIn IconBox--focused"]').click()
driver.find_element_by_xpath('.//button[@class="btn Searchbox__searchButton Searchbox__searchButton--active"]').click()
element = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,'.//div[@class="LazyLoad is-visible"]')))
element.click()
driver.close()
time.sleep(2)

#Step 5: Transfer to new pop-up window
driver.switch_to_window(driver.window_handles[0])

#Step 6: Collect the review collection (either from Agoda or Booking.com)
WebDriverWait(driver, 1000).until(EC.presence_of_element_located((By.XPATH,'.//span[@class="Review-tab Review-tab--active"]')))
element = driver.find_element_by_xpath('.//span[@class="Review-tab Review-tab--active"]')
driver.execute_script("arguments[0].scrollIntoView();", element)
i = element.text
print('Scraping.....')
score_list = []
sentiments = []
identities = []
travel_type = []
room_type = []
stayed = []
comments = []
review_date = []
while True:
	time.sleep(2)
	WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH,'.//div[@class="Review-comment-leftScore"]')))
	time.sleep(2)
	WebDriverWait(driver, 100).until(EC.visibility_of_element_located((By.XPATH,'.//div[@class="Review-comment-leftScore"]')))
	ActionChains(driver).move_to_element(element).perform()
	time.sleep(1)
	score = driver.find_elements_by_xpath('.//div[@class="Review-comment-leftScore"]')
	for number in score:
		score_list.append(number.text)
	WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH,'.//div[@class="Review-comment-leftScoreText"]')))
	sentiment = driver.find_elements_by_xpath('.//div[@class="Review-comment-leftScoreText"]')
	for sent in sentiment:
		sentiments.append(sent.text)
	WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH,'.//span[@class="Review-statusBar-date "]')))
	date_review= driver.find_elements_by_xpath('.//span[@class="Review-statusBar-date "]')
	for date in date_review:
		review_date.append(date.text)
	WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH,'.//*[@data-info-type="reviewer-name"]')))
	location =  driver.find_elements_by_xpath('.//*[@data-info-type="reviewer-name"]')
	for loc in location:
		loc = loc.text
		loc = loc.split("from")
		loc = loc[1:]
		loc = ",".join(loc)
		loc = loc.strip(" ")
		identities.append(loc)
	WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH,'.//*[@data-info-type="group-name"]')))
	trav_type = driver.find_elements_by_xpath('.//*[@data-info-type="group-name"]')
	for travel in trav_type:
		travel_type.append(travel.text)
	time.sleep(2)
	rooM_type = driver.find_elements_by_xpath('.//*[@data-info-type="room-type"]')
	for room in rooM_type:
		room_type.append(room.text)
	time.sleep(2)
	stayed_detail = driver.find_elements_by_xpath('.//*[@data-info-type="stay-detail"]')
	for stay in stayed_detail:
		stayed.append(stay.text)
	time.sleep(2)
	comment_review = driver.find_elements_by_xpath('.//div[@class="Review-comment-body"]')
	for comment in comment_review:
		comment = comment.text
		comment = comment.replace('\n',',')
		comment = comment.replace('”,',',')
		print(comment)
		comments.append(comment)
	try:
		driver.find_element_by_xpath('.//*[@class="BackToSearch-dismissText"][contains(., "Dismiss")]').click()
		time.sleep(2)
		WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH,'.//*[@class="ficon ficon-24 ficon-carrouselarrow-right"]')))
		time.sleep(2)
		WebDriverWait(driver, 100).until(EC.visibility_of_element_located((By.XPATH,'.//*[@class="ficon ficon-24 ficon-carrouselarrow-right"]')))
		element = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH,'.//*[@class="ficon ficon-24 ficon-carrouselarrow-right"]')))
		ActionChains(driver).move_to_element(element).perform()
		time.sleep(5)
		element.click()
		time.sleep(2)
	except (ElementClickInterceptedException,TimeoutException,NoSuchElementException,WebDriverException) as e:
		print(e)
		break


sentiments = pd.DataFrame(sentiments, columns=['sentiments'])
identities = pd.DataFrame(identities, columns=['location'])
travel_type = pd.DataFrame(travel_type, columns=['travel_type'])
room_type = pd.DataFrame(room_type, columns=['room_type'])
stayed = pd.DataFrame(stayed, columns=['stayed'])
score = pd.DataFrame(score_list, columns=['score'])
comments = pd.DataFrame(comments, columns=['comments'])
review_date = pd.DataFrame(review_date, columns=['review_date'])
comments['location']=identities['location']
comments['sentiments']=sentiments['sentiments']
comments['travel_type']=travel_type['travel_type']
comments['room_type']=room_type['room_type']
comments['stayed']=stayed['stayed']
comments['score']=score['score']
comments['review_date']=review_date['review_date']
comments.to_csv(search+" "+i+'.csv',index=False)
print('Comments Saved...')

#Step 7 collect the reviews (either Agoda or Booking.com)
print('Scrapping.....')
WebDriverWait(driver, 500).until(EC.presence_of_element_located((By.XPATH,'.//span[@class="NavBar__menulink--active"][contains(., "Reviews")]')))
time.sleep(2)
WebDriverWait(driver, 500).until(EC.visibility_of_element_located((By.XPATH,'.//span[@class="NavBar__menulink--active"][contains(., "Reviews")]')))
element = WebDriverWait(driver, 500).until(EC.element_to_be_clickable((By.XPATH,'.//span[@class="NavBar__menulink--active"][contains(., "Reviews")]')))
ActionChains(driver).move_to_element(element).perform()
time.sleep(5)
element.click()
score_list = []
sentiments = []
identities = []
travel_type = []
room_type = []
stayed = []
comments = []
review_date = []
time.sleep(2)
WebDriverWait(driver, 500).until(EC.presence_of_element_located((By.XPATH,'.//span[contains(@class,"Review-tab ")]')))
time.sleep(2)
WebDriverWait(driver, 500).until(EC.visibility_of_element_located((By.XPATH,'.//span[contains(@class,"Review-tab ")]')))
element = WebDriverWait(driver, 500).until(EC.element_to_be_clickable((By.XPATH,'.//span[contains(@class,"Review-tab ")]')))
ActionChains(driver).move_to_element(element).perform()
time.sleep(5)
element.click()
time.sleep(2)
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,'.//*[@class="Review-tab Review-tab--active"]')))
time.sleep(2)
WebDriverWait(driver, 100).until(EC.visibility_of_element_located((By.XPATH,'.//*[@class="Review-tab Review-tab--active"]')))
element = driver.find_element_by_xpath('.//*[@class="Review-tab Review-tab--active"]')
driver.execute_script("arguments[0].scrollIntoView();", element)
i = element.text
while True:
	time.sleep(1)
	score = driver.find_elements_by_class_name("Review-comment-leftScore")
	for number in score:
		score_list.append(number.text)
	time.sleep(1)<CNTD(Order ID (Orders))>
Order Count

<MONTH(Return Date)>
Month of Order Date
	sentiment = driver.find_elements_by_xpath('.//div[@class="Review-comment-leftScoreText"]')
	for sent in sentiment:
		sentiments.append(sent.text)
	time.sleep(1)
	date_review= driver.find_elements_by_xpath('.//span[@class="Review-statusBar-date "]')
	for date in date_review:
		review_date.append(date.text)
	time.sleep(1)
	location =  driver.find_elements_by_xpath('.//*[@data-info-type="reviewer-name"]')
	for loc in location:
		loc = loc.text
		loc = loc.split("from")
		loc = loc[1:]
		loc = ",".join(loc)
		loc = loc.strip(" ")
		identities.append(loc)
	time.sleep(1)
	trav_type = driver.find_elements_by_xpath('.//*[@data-info-type="group-name"]')
	for travel in trav_type:
		travel_type.append(travel.text)
	time.sleep(1)
	rooM_type = driver.find_elements_by_xpath('.//*[@data-info-type="room-type"]')
	for room in rooM_type:
		room_type.append(room.text)
	time.sleep(1)
	stayed_detail = driver.find_elements_by_xpath('.//*[@data-info-type="stay-detail"]')
	for stay in stayed_detail:
		stayed.append(stay.text)
	time.sleep(1)
	comment_review = driver.find_elements_by_xpath('.//div[@class="Review-comment-body"]')
	for comment in comment_review:
		comment = comment.text
		comment = comment.replace('\n',',')
		comment = comment.replace('”,',',')
		comments.append(comment)
		print(comment)
	try:
		driver.find_element_by_xpath('.//*[@class="BackToSearch-dismissText"][contains(., "Dismiss")]').click()
		WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH,'.//span[@class="Review-paginator-numbers"]')))
		element = WebDriverWait(driver, 100).until(EC.visibility_of_element_located((By.XPATH,'.//span[@class="Review-paginator-numbers"]')))
		ActionChains(driver).move_to_element(element).perform()
		time.sleep(2)
		WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH,'.//*[@class="ficon ficon-24 ficon-carrouselarrow-right"]')))
		time.sleep(2)
		WebDriverWait(driver, 100).until(EC.visibility_of_element_located((By.XPATH,'.//*[@class="ficon ficon-24 ficon-carrouselarrow-right"]')))
		time.sleep(2)
		element = WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.XPATH,'.//*[@class="ficon ficon-24 ficon-carrouselarrow-right"]')))
		ActionChains(driver).move_to_element(element).perform()
		time.sleep(5)
		element.click()
		time.sleep(2)
	except (TimeoutException,NoSuchElementException,WebDriverException) as e: #,ElementClickInterceptedException,) as e:
		print(e)
		break

sentiments = pd.DataFrame(sentiments, columns=['sentiments'])
identities = pd.DataFrame(identities, columns=['location'])
travel_type = pd.DataFrame(travel_type, columns=['travel_type'])
room_type = pd.DataFrame(room_type, columns=['room_type'])
stayed = pd.DataFrame(stayed, columns=['stayed'])
score = pd.DataFrame(score_list, columns=['score'])
comments = pd.DataFrame(comments, columns=['comments'])
review_date = pd.DataFrame(review_date, columns=['review_date'])
comments['location']=identities['location']
comments['sentiments']=sentiments['sentiments']
comments['travel_type']=travel_type['travel_type']
comments['room_type']=room_type['room_type']
comments['stayed']=stayed['stayed']
comments['score']=score['score']
comments['review_date']=review_date['review_date']
comments.to_csv(search+" "+i+'.csv',index=False)
print('Comments Saved...')'''

#Step 8: Open Trip-Advisor
print('Opening Trip Advisor')
driver.get('https://www.tripadvisor.com.ph')
time.sleep(5)

while True:
	try:
			WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH,'.//div[contains(@class,"overlays-pieces-CloseX__close--3jowQ overlays-pieces-CloseX__inverted--3ADoB")]')))
			
			WebDriverWait(driver, 100).until(EC.visibility_of_element_located((By.XPATH,'.//div[contains(@class,"overlays-pieces-CloseX__close--3jowQ overlays-pieces-CloseX__inverted--3ADoB")]')))
			element = WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.XPATH,'.//div[contains(@class,"overlays-pieces-CloseX__close--3jowQ overlays-pieces-CloseX__inverted--3ADoB")]')))
			ActionChains(driver).move_to_element(element).perform()
			
			element.click()
	except (NoSuchElementException, TimeoutException) as e:
		break


WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,'.//span[contains(@class,"brand-global-nav-action-search-Search__label--3Fbaz")]')))

WebDriverWait(driver, 100).until(EC.visibility_of_element_located((By.XPATH,'.//span[contains(@class,"brand-global-nav-action-search-Search__label--3Fbaz")]')))
element = WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.XPATH,'.//span[contains(@class,"brand-global-nav-action-search-Search__label--3Fbaz")]')))
ActionChains(driver).move_to_element(element).perform()

element.click()

WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,'.//input[contains(@id,"mainSearch")]')))

WebDriverWait(driver, 100).until(EC.visibility_of_element_located((By.XPATH,'.//input[contains(@id,"mainSearch")]')))
element = WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.XPATH,'.//input[contains(@id,"mainSearch")]')))
ActionChains(driver).move_to_element(element).perform()

element.click()

driver.find_element_by_xpath('.//input[contains(@id,"mainSearch")]').send_keys(search)
element = WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.XPATH,'.//*[contains(@id,"SEARCH_BUTTON")]')))
element.click()

#wait for the review count element to show up
WebDriverWait(driver, 100).until(EC.visibility_of_element_located((By.XPATH,'.//a[contains(@class,"review_count")]')))

# return to the review count
time.sleep(6)
element = WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.XPATH,'.//a[contains(@class,"review_count")]')))
ActionChains(driver).move_to_element(element).perform()
time.sleep(8)
element.click()

driver.close()

#Transfer to new pop up window
driver.switch_to_window(driver.window_handles[0])
WebDriverWait(driver, 100).until(EC.visibility_of_element_located((By.XPATH,'.//span[contains(@class,"reviewCount")]')))
element = WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.XPATH,'.//span[contains(@class,"reviewCount")]')))
ActionChains(driver).move_to_element(element).perform()
time.sleep(5)
element.click()

#Collect Comments
score_list = []
travel_type = []
stayed = []
comments = []
reviews = []
review_date = []
#user_loc = []
print('Initiating Collection')

while True:
	time.sleep(5)
	#Looking for the Tab Review & More
	WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH,'.//*[contains(@data-tab,"TABS_REVIEWS")]')))
	element = driver.find_element_by_xpath('.//*[contains(@data-tab,"TABS_REVIEWS")]')
	time.sleep(8)
	element.location_once_scrolled_into_view
	container = driver.find_elements_by_xpath('.//*[contains(@data-tab,"TABS_REVIEWS")]')
	print('Looking Into Review-Container')
	for item in container:
		try:
			#Looking into the container where the reviews are...
			element = driver.find_element_by_xpath('.//div[contains(@class,"ui_card hotels-hotel-review-community-content-Card__card--2dqMT section")]')
			driver.execute_script("arguments[0].scrollIntoView();", element)
			# Click the Read More Tab
			print('Expanding Comment Box')
			time.sleep(2)
			WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH,'.//span[contains(@class,"hotels-hotel-review-community-content-review-list-parts-ExpandableReview__cta--3_zOW")][contains(., "Read more")]')))
			WebDriverWait(driver, 100).until(EC.visibility_of_element_located((By.XPATH,'.//span[contains(@class,"hotels-hotel-review-community-content-review-list-parts-ExpandableReview__cta--3_zOW")][contains(., "Read more")]')))
			element = WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.XPATH,'.//span[contains(@class,"hotels-hotel-review-community-content-review-list-parts-ExpandableReview__cta--3_zOW")][contains(., "Read more")]')))
			ActionChains(driver).move_to_element(element).perform()
			element.click()
		except (WebDriverException) as e:
			continue

		try:
			# Remove Hotel Admin Reply
			driver.execute_script("[...document.querySelectorAll('.mgrRspnInLine')].map(el => el.parentNode.removeChild(el))")
			driver.execute_script("[...document.querySelectorAll('.hotels-hotel-review-about-with-photos-Reviews__bubbleRating--1dCQB')].map(el => el.parentNode.removeChild(el))")
			time.sleep(10)
			# retrieve bubble rating
			WebDriverWait(item, 100).until(EC.presence_of_element_located((By.XPATH,'//span[contains(@class,"ui_bubble_rating bubble_")]')))

			WebDriverWait(item, 100).until(EC.visibility_of_element_located((By.XPATH,'//span[contains(@class,"ui_bubble_rating bubble_")]')))
			rating = item.find_elements_by_xpath('//span[contains(@class,"ui_bubble_rating bubble_")]')
			time.sleep(2)
			for i in rating:
				rate = i.get_attribute("class")
				rate = str(rate)
				rate = rate[-2:]
				print('Rate')
				print(rate)
				print('---------------------------------------------------------------------------')
				score_list.append(rate)
			# retrieve container with date of stay
			time.sleep(2)
			print('Collecting Date Stayed')
			stay = driver.find_elements_by_xpath('.//div[contains(@class,"hotels-review-list-parts-EventDate__event_date--1agCM")]')
			for i in stay:			
				stayed = i.text
				print('stayed')
				print(stayed)
				print('---------------------------------------------------------------------------')
				stayed = stayed.split(': ')
				stayed.append(stayed[1])
			# retrieve travel type
			travel = driver.find_elements_by_xpath('.//div[contains(@class,"hotels-review-list-parts-TripType__trip_type--l3cTB")]')
			for i in travel:
				type_travel = i.text
				print('Travel Type')
				print(type_travel)
				print('---------------------------------------------------------------------------')
				type_travel = type_travel.split(': ')
				travel_type.append(type_travel[1])
			# Retrieve  Title Comment
			WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH,'.//*[contains(@class,"hotels-hotel-review-community-content-review-list-parts-ReviewTitle__reviewTitleText--2vGeO")]')))
			summary = driver.find_elements_by_xpath('.//*[contains(@class,"hotels-hotel-review-community-content-review-list-parts-ReviewTitle__reviewTitleText--2vGeO")]')
			for i in summary:
				comment = i.text
				print('comment')
				print(comment)
				print('---------------------------------------------------------------------------')
				comments.append(comment)
			#WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH,'.//*[contains(@class,"userLoc")]')))
			#loc = driver.find_elements_by_xpath('.//*[contains(@class,"userLoc")]')
			#for i in loc:
				#loc = i.text
				#print('location')
				#print(loc)
				#print('---------------------------------------------------------------------------')
				#user_loc.append(loc)
			WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH,'.//div[contains(@class,"hotels-hotel-review-community-content-review-list-parts-ReviewCardHeader__padding--WNQp_")]')))
			rating_date = driver.find_elements_by_xpath('.//div[contains(@class,"hotels-hotel-review-community-content-review-list-parts-ReviewCardHeader__padding--WNQp_")]')
			#rating_date = driver.find_elements_by_xpath('.//div[@class,"social-member-MemberEventOnObjectBlock__item--27qCT"]')
			for i in rating_date:			
				#date = i.get_attribute("title")
				#date = str(date)
				date = i.text
				print('Date')
				print(date)
				print('---------------------------------------------------------------------------')
				review_date.append(date)
			WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH,'.//q[contains(@class,"hotels-hotel-review-community-content-review-list-parts-ExpandableReview__reviewText--1OjOL")]')))
			review = driver.find_elements_by_css_selector(".hotels-hotel-review-community-content-review-list-parts-ExpandableReview__reviewText--1OjOL")
			for i in review:
				review = i.text
				print('Review')
				print(review)
				print('---------------------------------------------------------------------------')
				reviews.append(review)
		except (NoSuchElementException,TimeoutException) as e:
			continue
	try:
		time.sleep(5)
		WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH,'.//*[contains(@class,"ui_button nav next primary_dark ")]')))
		time.sleep(5)
		WebDriverWait(driver, 100).until(EC.visibility_of_element_located((By.XPATH,'.//*[contains(@class,"ui_button nav next primary_dark ")]')))
		element = WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.XPATH,'.//*[contains(@class,"ui_button nav next primary_dark ")]')))
		ActionChains(driver).move_to_element(element).perform()
		time.sleep(5)
		element.click()
		time.sleep(5)
	except (ElementClickInterceptedException,NoSuchElementException,TimeoutException,WebDriverException) as e:
		print(e)
		break
	except Exception as e:
		print (e)
		break

travel_type = pd.DataFrame(travel_type, columns=['travel_type'])
stayed = pd.DataFrame(stayed, columns=['stayed'])
score = pd.DataFrame(score_list, columns=['score'])
comments = pd.DataFrame(comments, columns=['short_phrase'])
review = pd.DataFrame(reviews, columns=['comment'])
review_date = pd.DataFrame(review_date, columns=['review_date'])
#user_loc = pd.DataFrame(user_loc, columns=['location'])
review['short_phrase']=comments['short_phrase']
review['travel_type']=travel_type['travel_type']
review['stayed']=stayed['stayed']
#review['location']=user_loc['location']
review['score']=score['score']
review['review_date']=review_date['review_date']
review.to_csv(search+' tripadvisor.csv',index=False)
print('Comments Saved....')
driver.close()
