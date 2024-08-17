import requests
from bs4 import BeautifulSoup

def fetch_website_data(url):
    try:
        if not url.startswith('https://') and not url.startswith('http://'):
            url = 'https://' + url

        # Send a GET request to the URL
        response = requests.get(url, timeout=10)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Parse the content of the response using BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract text from the parsed HTML
            page_text = soup.get_text(separator=' ', strip=True)
            
            # Optionally, perform further cleaning on page_text here
            
            return page_text
        else:
            return f"Failed to retrieve the webpage: Status code {response.status_code}"
    except Exception as e:
        return f"An error occurred: {e}"

