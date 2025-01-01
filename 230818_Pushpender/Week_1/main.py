from scraper.problem_scraper import scrape_problem
from scraper.editorial_scraper import scrape_editorial

if __name__ == "__main__":
    # Specify the problem ID and index
    contest_id = 2052
    problem_index = 'M'

    # Scrape problem and editorial
    scrape_problem(contest_id, problem_index)
    scrape_editorial(contest_id, problem_index)
