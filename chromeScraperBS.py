import requests
from bs4 import BeautifulSoup
import pandas as pd

# Step 1: Open Agoda
url = 'https://www.agoda.com'
response = requests.get(url)

if response.status_code == 200:
    print("Opened Agoda...")
else:
    print("Failed to open Agoda. Exiting.")
    exit()

# Step 2: Locate Hotel
while True:
    try:
        search = input('Input name of hotel and location (i.e. <hotel name><space><location>): ')
        search = str(search)
        params = {'q': search}
        response = requests.get(url, params=params)
        soup = BeautifulSoup(response.content, 'html.parser')
        suggestion = soup.find('span', class_='Suggestion__categoryName_text', string='Property')
        if suggestion:
            suggestion.click()
        else:
            print('Your Selection is not a property, please check your spelling.')
            continue
    except Exception as e:
        print(f'An error occurred: {e}')
        break
    else:
        break

# Step 4: Search and click review box (skipping the part related to clicking buttons)

# Step 5: Transfer to new pop-up window (assuming you've clicked on a review)

# Step 6: Collect the review collection
reviews = []

while True:
    try:
        # Replace this part with the appropriate URL for reviews
        review_url = 'https://www.agoda.com/review-url'  # Update this with the actual review URL
        review_response = requests.get(review_url)
        review_soup = BeautifulSoup(review_response.content, 'html.parser')

        # Adjust the following code to match the structure of Agoda reviews page
        comment_review = review_soup.find_all('div', class_='Review-comment-body')
        for comment in comment_review:
            comment_text = comment.get_text(strip=True)
            print(comment_text)
            reviews.append(comment_text)
    except Exception as e:
        print(f'An error occurred: {e}')
        break

# Step 7: Collect the reviews (either Agoda or Booking.com)
print('Scraping.....')
reviews_url = 'https://www.agoda.com/reviews-url'  # Update this with the actual reviews URL
reviews_response = requests.get(reviews_url)
reviews_soup = BeautifulSoup(reviews_response.content, 'html.parser')

# Continue parsing and collecting reviews as needed...

# Step 8: Open Trip Advisor
print('Opening Trip Advisor')
tripadvisor_url = 'https://www.tripadvisor.com.ph'
tripadvisor_response = requests.get(tripadvisor_url)
tripadvisor_soup = BeautifulSoup(tripadvisor_response.content, 'html.parser')

# Continue with the remaining Trip Advisor code using BeautifulSoup...

# Closing the WebDriver since we're not using it in this translated version
# driver.close()

# Step 8: Open Trip Advisor (Continued)
print('Opening Trip Advisor')
tripadvisor_url = 'https://www.tripadvisor.com.ph'
tripadvisor_response = requests.get(tripadvisor_url)
tripadvisor_soup = BeautifulSoup(tripadvisor_response.content, 'html.parser')

# Continue with the remaining TripAdvisor code using BeautifulSoup...
# Add your code here to navigate through the TripAdvisor website, search for the hotel, and collect reviews.

# Assuming you have reached the page with hotel reviews, continue with the reviews collection part:

# Collect TripAdvisor Reviews
tripadvisor_reviews = []

while True:
    try:
        # Replace this part with the appropriate URL for TripAdvisor reviews
        tripadvisor_review_url = 'https://www.tripadvisor.com/review-url'  # Update this with the actual review URL
        tripadvisor_review_response = requests.get(tripadvisor_review_url)
        tripadvisor_review_soup = BeautifulSoup(tripadvisor_review_response.content, 'html.parser')

        # Adjust the following code to match the structure of TripAdvisor reviews page
        review_elements = tripadvisor_review_soup.find_all('div', class_='review-container')
        for review_element in review_elements:
            # Extract relevant information from the review element
            review_text = review_element.find('q', class_='IRsGHoPm').get_text(strip=True)
            review_date = review_element.find('span', class_='ratingDate')['title']
            # Add more extraction as needed

            # Print or store the extracted information
            print(f'Review: {review_text}')
            print(f'Review Date: {review_date}')
            # Add more print or storage as needed

            # Append the review to the list
            tripadvisor_reviews.append({'Review': review_text, 'Review Date': review_date})
    except Exception as e:
        print(f'An error occurred: {e}')
        break

# Optionally, you can save the TripAdvisor reviews to a CSV file or any other desired format.

# Close the TripAdvisor session
print('Closing TripAdvisor...')
# Add code to close the TripAdvisor session or browser if needed.

# End of the script
print('Script completed.')
