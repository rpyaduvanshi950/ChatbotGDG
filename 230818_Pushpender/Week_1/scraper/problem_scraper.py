import os
import json
from bs4 import BeautifulSoup
import requests

BASE_URL = "https://codeforces.com/problemset/problem/"


def scrape_problem(contest_id, problem_index):
    url = f"{BASE_URL}{contest_id}/{problem_index}"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch problem page: {url}")
        return

    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract relevant data
    title = soup.find('div', class_='title').text
    statement = soup.find('div', class_='problem-statement').text
    tags = [tag.text for tag in soup.find_all('span', class_='tag-box')]
    metadata = {
        "title": title,
        "tags": tags,
        "url": url
    }

    # Save data
    save_problem_data(contest_id, problem_index, statement, metadata)


def save_problem_data(contest_id, problem_index, statement, metadata):
    problem_dir = os.path.join('data', 'problems', f"{contest_id}_{problem_index}")
    os.makedirs(problem_dir, exist_ok=True)

    with open(os.path.join(problem_dir, 'statement.txt'), 'w') as file:
        file.write(statement)

    with open(os.path.join(problem_dir, 'metadata.json'), 'w') as file:
        json.dump(metadata, file, indent=4)
