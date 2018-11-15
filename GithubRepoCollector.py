#!/usr/bin/python3
"""
Usage:
  GithubRepoCollector.py --help
  GithubRepoCollector.py (--github_user=<github_user>)

Options:
  --github_user=<github_user>    Github user to scrub for projects ex: my4andle
"""

import requests
import concurrent.futures

from docopt import docopt
from bs4 import BeautifulSoup


def load_page(url: str):
    """
    Load a page with BeautifulSoup.

    Args:
        url:    The url to load
    
    Returns:
        BeautifulSoup html
    """
    print("Loading page: {}".format(url))
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    return soup

def find_pagination_max(soup_html):
    """
    Find the page range from pagination html.
    
    Args:
        soup_html: The html from the base page loaded which may contain pagination
    
    Returns:
        Either the max pagination integer or None
    """
    print("Finding pagination max")
    a_refs = soup_html.select('.pagination a')
    pages = []
    for ref in a_refs:
        num_str = ref.get_text()
        try:
            num_int = int(num_str)
            pages.append(num_int)
        except:
            pass
    try:
        page_max = max(pages)
        return page_max
    except:
        return None

def generate_page_list(github_user: str, page_count: int):
    """
    Based on the page count and user, generate a list of repository pages.

    Args:
        github_user:    Github user account
        page_count:     The max pagination integer
    
    Returns:
        A list of repository pages for the given user
    """
    print("Generating pagination page list using count of: {}".format(page_count))
    page_url = "https://github.com/{}?page=".format(github_user)
    # preload with base page for simplicity
    page_list = []
    for p in range(1, int(page_count) + 1):
        page_list.append(page_url + str(p))
    print(page_list)
    return page_list

def generate_git_urls(page):
    """
    Generate a list of git repository urls to be later cloned by the user.

    Args:
        page_list:  A list of repository pages to anylize
    
    Returns:
        A list of git urls that can be cloned
    """
    base_url = "https://github.com"
    repos = []
    soup_html = load_page(page)
    for repo in soup_html.find_all('a', itemprop="name codeRepository"):
        if repo.text:
            repos.append(base_url + repo['href'] + ".git")
    return repos

def generate_git_urls_concurrent(page_list: list):
    """
    Concurrently find repositories for a list of given github pages.

    Args:
        page_list:  List of repository pages to scrub for repositories

    Returns:
        A list of lists
    """
    print("Concurrently finding repositories")
    results_list = []
    with concurrent.futures.ProcessPoolExecutor(max_workers=10) as pool:
        results = {pool.submit(generate_git_urls, page): page for page in page_list}
        for future in concurrent.futures.as_completed(results):
            if future.result():
                results_list.append(future.result())
    return results_list

def main():
    """
    Orchestrate the chaos.
    """
    opts = docopt(__doc__)
    github_user = opts["--github_user"]
    base_user_url = "https://github.com/{}?tab=repositories".format(github_user)
    soup_html = load_page(base_user_url)
    page_max = find_pagination_max(soup_html)
    if page_max:
        page_urls = generate_page_list(github_user, page_max)
    else:
        page_urls = [base_user_url]
    clone_urls = generate_git_urls_concurrent(page_urls)
    with open("{}_git_urls.log".format(github_user), "w+") as file:
        for urllist in clone_urls:
            for line in urllist:
                file.write(line + "\n")

if __name__ == '__main__':
    main()
