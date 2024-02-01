import requests
from bs4 import BeautifulSoup

# Step 8: Open Trip Advisor
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

# End of TripAdvisor scraper
print('TripAdvisor scraping completed.')
