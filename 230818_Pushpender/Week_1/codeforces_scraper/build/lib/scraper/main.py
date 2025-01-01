import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

def scrape_codeforces():
    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Uncomment this to run in headless mode
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    # Set up the Chrome Driver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # Access the Codeforces problemset page
        url = "https://codeforces.com/problemset"
        driver.get(url)

        # Locate the problem row by the title "2052M"
        problem_table = driver.find_element(By.CLASS_NAME, 'problems')  # Find the problems table
        problem_rows = problem_table.find_elements(By.TAG_NAME, 'tr')  # Get all rows

        # Iterate through the rows to find the target problem
        data = {}
        for row in problem_rows:
            title_element = row.find_element(By.CLASS_NAME, 'left')  # Find the left class element
            title_link = title_element.find_element(By.TAG_NAME, 'a')  # Get the anchor tag
            title_text = title_link.text.strip()  # Title (e.g., "2052M")

            # Check for the correct title
            if title_text == "2052M":
                href_link = title_link.get_attribute('href')  # Get href link
                data = {
                    "title": title_text,
                    "href": href_link
                }
                break  # Stop after finding the title

        # Print the JSON output
        if data:
            print(json.dumps(data, indent=4))  # Print the JSON nicely
        else:
            print("Problem not found.")

    finally:
        driver.quit()  # Ensure the browser is closed

if __name__ == "__main__":
    scrape_codeforces()
