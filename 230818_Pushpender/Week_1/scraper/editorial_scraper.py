from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import os

BASE_URL = "https://codeforces.com/problemset/problem/"


def scrape_editorial(contest_id, problem_index):
    url = f"{BASE_URL}{contest_id}/{problem_index}/editorial"
    options = Options()
    options.add_argument('--headless')  # Run browser in headless mode
    driver = webdriver.Chrome(options=options)

    try:
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        content = soup.find('div', class_='editorial-content').text

        # Save editorial
        save_editorial_data(contest_id, problem_index, content)
    finally:
        driver.quit()


def save_editorial_data(contest_id, problem_index, content):
    editorial_dir = os.path.join('data', 'problems', f"{contest_id}_{problem_index}")
    os.makedirs(editorial_dir, exist_ok=True)

    with open(os.path.join(editorial_dir, 'editorial.txt'), 'w') as file:
        file.write(content)
