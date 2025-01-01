from bs4 import BeautifulSoup
import requests
import os
import json
import logging
import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
logging.basicConfig(filename='logs/scraper.log', level=logging.INFO)

def log_message(message):
    logging.info(message)


def scrape_problem(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    title = soup.find('div', class_='title').text.strip()
    problem_statement = soup.find('div', class_='problem-statement').text.strip()

    time_limit = soup.find('div', class_='time-limit').text.strip()
    memory_limit = soup.find('div', class_='memory-limit').text.strip()

    tags = [tag.text.strip() for tag in soup.find_all('span', class_='tag-box')]

    problem_data = {
        'title': title,
        'statement': problem_statement,
        'time_limit': time_limit,
        'memory_limit': memory_limit,
        'tags': tags
    }
    return problem_data

def save_problem_data(problem_data, problem_id):
    problem_dir = './data/problems/'
    if not os.path.exists(problem_dir):
        os.makedirs(problem_dir)

    # Save problem statement as a text file
    with open(os.path.join(problem_dir, f'{problem_id}.txt'), 'w') as f:
        f.write(problem_data['statement'])

    # Save problem metadata as a JSON file
    with open(os.path.join(problem_dir, f'{problem_id}.json'), 'w') as f:
        json.dump(problem_data, f, indent=4)

def scrape_editorial(editorial_url):
    response = requests.get(editorial_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    editorial_content = soup.find('div', class_='ttypography').text.strip()

    for element in soup.find_all(['script', 'math']):
        element.decompose()

    return editorial_content

def process_editorial(editorial_content):
    return editorial_content


def rate_limit():
    time.sleep(random.uniform(1, 3))  # Random delay to mimic human-like behavior

def handle_request_error(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        rate_limit()
        return None


def main():
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)

    try:
        problem_urls = ['https://codeforces.com/problemset/problem/1000/A', '...']  # Example URLs

        for url in problem_urls:
            problem_data = scrape_problem(url)
            problem_id = url.split('/')[-1]
            save_problem_data(problem_data, problem_id)

            editorial_url = f'https://codeforces.com/contest/{problem_id}/editorial'
            editorial_content = scrape_editorial(editorial_url)
            editorial_content = process_editorial(editorial_content)
            save_editorial_data(editorial_content, problem_id)

            rate_limit()

    finally:
        driver.quit()


def save_editorial_data(editorial_content, problem_id):
    editorial_dir = './data/editorials/'
    if not os.path.exists(editorial_dir):
        os.makedirs(editorial_dir)

    with open(os.path.join(editorial_dir, f'{problem_id}.txt'), 'w') as f:
        f.write(editorial_content)
