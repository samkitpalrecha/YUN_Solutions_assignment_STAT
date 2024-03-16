from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
import time

# For headless mode i.e, If you don't need a visible browser window
options = Options()
options.add_argument("--headless")

# define the chrome webdriver that we are using for the webscraping purpose
driver = webdriver.Chrome(options = options)

# we will be doing a google search for the task
driver.get("https://www.google.com/")

# find the search bar and search the required search query
search_bar = driver.find_element(By.CSS_SELECTOR, ".gLFyf")
search_query = "'Reliance Industries latest news'"
search_bar.send_keys(search_query)
search_bar.send_keys(Keys.RETURN)

try:
    # Wait for search results to load
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div#main > div > div > div")))
    print("Search results loaded successfully")

    # Scroll down to potentially load more results
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)  # Give time for additional content to load after scroll

    # Find news results container
    news_results = driver.find_element(By.ID, "main")

    # Extract links from news results
    anchors = news_results.find_elements(By.TAG_NAME, "a")
    cleaned_news_urls = []
    for anchor in anchors:
        url = anchor.get_attribute("href")
        if url and ("google" not in url and "quora" not in url):
            cleaned_news_urls.append(url)
    print("Extracted and filtered URLs")

    # Remove duplicates
    cleaned_news_urls = set(cleaned_news_urls)
    cleaned_news_urls = list(cleaned_news_urls)

    print(f"Found {len(cleaned_news_urls)} unique URLs")
        
except TimeoutException:
    print("Timeout waiting for search results to load")

finally:
    driver.quit()
    print("Browser closed")


def extract_text(url):
    try:
        driver.get(url)
        text = driver.find_element(By.TAG_NAME, 'body').text
        return {'source': url, 'text': text}
    except TimeoutException:
        print(f"Timeout waiting for {url} to load")
        return None 
    except Exception as e:
        print(f"Error processing {url}: {e}")
        return None 


data = []

driver = webdriver.Chrome(options=options)  # Create a single browser instance

for url in cleaned_news_urls:
    extracted_data = extract_text(url)
    if extracted_data:  # Only append if data was successfully extracted
        data.append(extracted_data)

driver.quit()  # Close the browser instance

print(f"Successfully Extracted data for {len(data)} URLs")

with open("data.txt", "w", encoding="utf-8") as f:
  for item in data:
    f.write(f"{item}\n")  # Add newline character for each item

