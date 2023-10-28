import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from markdownify import markdownify
import json 
import re
import os
import argparse


SCRIPT_DIR = os.path.dirname(__file__)

env = os.getenv('ENV') or "DEV"
print("ENV Set to:", env)
if env == "DEV":
    print("Scraping the maximum number of links set to 10 and years to 2")
elif env == "PROD":
    print("Scraping at maximum depth")


argParser = argparse.ArgumentParser()
argParser.add_argument("-i", "--input-list", help="Relative location of the input file containing the list of URLs and relative path")

args = argParser.parse_args()

def fetch_all_urls(url):
    """Returns an array of URL strings

    Goes through the passed-in URL and finds all links from it.
    """

    try:
        # Send an HTTP GET request to the URL
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content with BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find all the anchor (a) tags in the HTML
            links = soup.find_all('a')

            # Extract and return all URLs from the webpage
            urls = []
            for link in links:
                href = link.get('href')
                if href:
                    full_url = urljoin(url, href)
                    urls.append(full_url)
            return urls
        else:
            print("Failed to retrieve the webpage. Status code:", response.status_code)
    except requests.exceptions.RequestException as e:
        print("An error occurred:", e)

    # Return an empty list if there's an error or the URL is not valid
    return []

def get_urls_matching_pattern(url, pattern):
    """Returns an array of URL strings

    Fetches all URLs from a webpage and returns an array of URLs which matches the pattern
    """
    try:
        # Fetch all URLs from the given URL
        all_urls = fetch_all_urls(url)

        # Filter the URLs that match the specified pattern
        matching_urls = [full_url for full_url in all_urls if re.search(pattern, full_url)]
        # During testing only get the latest 2 years
        if (env == "DEV"):
            return matching_urls[:2]
        return matching_urls
    except requests.exceptions.RequestException as e:
        print("An error occurred:", e)

    # Return an empty list if there's an error
    return []


def is_valid_news_url(url, base_url):
    # Construct the regex pattern with the base_url
    pattern = re.escape(base_url)

    if base_url == "https://www.debian.org/News/weekly/":
        pattern += r'(\d{4}/\d{2}/|weekly/\d{4}/\d{2}/\d{2}/)'

    elif base_url == "https://www.debian.org/News/":
        pattern += r'(\d{4})/(\d{4})(\d{2})(\d{2})'

    elif base_url == "https://www.debian.org/security/":
        pattern += r'(\d{4}/[a-zA-Z0-9-]+)'

    pattern += r'$'

    # Use the constructed pattern to match the URL
    return bool(re.match(pattern, url))


def get_all_news_links_from_endpoints(news_endpoints, base_url):
    valid_news_url = []
    for endpoint in news_endpoints:
        all_links = fetch_all_urls(endpoint)
        for link in all_links:
            if (env == "DEV" and len(valid_news_url) > 10):
                return valid_news_url
            if is_valid_news_url(link, base_url):
                print("Got valid news URL:", link)
                valid_news_url.append(link)
            # else:
            #     print("Invalid URL:", link)
    return valid_news_url


def convert_relative_links_to_absolute(soup, base_url):
    """
    Returns an absolute link in string form

    Take input of a soup object and a base_url and returns all links in a webpage
    as abosulute links
    """
    # Find all anchor (a) tags in the HTML
    links = soup.find_all('a')

    # Convert relative links to absolute links
    for link in links:
        href = link.get('href')
        if href:
            full_url = urljoin(base_url, href)
            link['href'] = full_url

def extract_content_and_convert_to_markdown(url):
    """
    Returns a markdown string

    Accepts a URL, which has to be converted to markdown.
    By default, all the interested content lies inside a HTML div with the id 
    "content"
    """
    try:
        # Send an HTTP GET request to the URL
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content with BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')

            # Convert relative links to absolute links using the base URL
            convert_relative_links_to_absolute(soup, url)

            # Find the element with id="content" as it contains the interested content
            content_element = soup.find(id="content")

            # Check if the content_element is not None
            if content_element:
                # Convert HTML to markdown using markdownify
                markdown_content = markdownify(str(content_element))
                return markdown_content
            else:
                print("Element with id='content' not found on the webpage.")
        else:
            print("Failed to retrieve the webpage. Status code:", response.status_code)
    except requests.exceptions.RequestException as e:
        print("An error occurred:", e)

    return None

def write_markdown_to_file(markdown_content, file_path):
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(markdown_content)
        print(f"Markdown content saved to {file_path}")
    except Exception as e:
        print(f"Failed to save markdown content to {file_path}. Error: {str(e)}")


def create_file_name(url, base_url):
    # Check if the URL starts with the specified base_url
    if url.startswith(base_url):
        # Extract the content after the base_url
        last_part = url[len(base_url):]
        # Handle edge case for debian project news URLs
        if last_part[-1] == "/":
            last_part = last_part[:-1]

        return last_part + ".md"

    return None


URLs = {}
filename = "urls.json"
print("args", args.input_list)
if args.input_list == None:
    print("No input-list passed. Looking for default list urls.json...")
elif args.input_list and args.input_list.endswith(".json"):
    print("Using", args.input_list, "as input-list")
    filename = args.input_list
else:
    print("Passed in input-list is not a json file. Exiting...")
    exit()


try:
    # Try to open the file for reading
    with open(filename) as f:
        data = f.read()

    try:
        # Try to parse the JSON data
        URLs = json.loads(data)
        print(URLs)

    except json.JSONDecodeError as e:
        print("Error decoding JSON data:", e)

except FileNotFoundError:
    print(f"File '{filename}' not found.")

except IOError as e:
    print(f"An error occurred while reading the file: {e}")


for url in URLs:
    pattern = re.escape(url)
    pattern += r'\d{4}/$'
    prefix = url + "2023/"
    REL_PATH = URLs[url]
    print ("Processing URL:", url, "to", REL_PATH)
    year_news_endpoints = get_urls_matching_pattern(url, pattern)
    all_news_links = get_all_news_links_from_endpoints(year_news_endpoints, url)

    for link in all_news_links:
        md = extract_content_and_convert_to_markdown(link)
        write_markdown_to_file(md, os.path.join(SCRIPT_DIR, REL_PATH, create_file_name(link, url)))
