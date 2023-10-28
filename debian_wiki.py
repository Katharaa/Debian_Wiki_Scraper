import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from markdownify import markdownify
import re
import os


SCRIPT_DIR = os.path.dirname(__file__)


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
        return matching_urls[:2]
        #return matching_urls
    except requests.exceptions.RequestException as e:
        print("An error occurred:", e)

    # Return an empty list if there's an error
    return []


def is_valid_date_url(url, base_url):
    # Construct the regex pattern with the base_url
    pattern = re.escape(base_url) + r'(\d{4})/(\d{4})(\d{2})(\d{2})(\d+)?$'

    # Use the constructed pattern to match the URL
    match = re.match(pattern, url)

    if match:
        year, full_year, month, day, extra_info = match.groups()
        if (
            year == full_year
            and re.match(r'^(0[1-9]|1[0-2])$', month)
            and re.match(r'^(0[1-9]|[12][0-9]|3[01])$', day)
        ):
            return True
    return False



def get_all_news_links_from_endpoints(news_endpoints, base_url):
    valid_news_url = []
    for endpoint in news_endpoints:
        all_links = fetch_all_urls(endpoint)
        for link in all_links:
            if is_valid_date_url(link, base_url):
                print("Got valid news URL:", link)
                valid_news_url.append(link)
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
    pattern = re.escape(base_url) + r'(\d{4})/(\d{4})(\d{2})(\d{2})(\d+)?$'
    match = re.search(pattern, url)
    if match:
        year, full_year, month, day, extra_info = match.groups()
        formatted_date = f"{year}/{day}-{month}"
        if extra_info:
            formatted_date += f"-{extra_info}"
        return f"{formatted_date}.md"
    return None

url = "https://www.debian.org/News/"
pattern = r'https://www.debian.org/News/\d{4}/$'
base_url = "https://www.debian.org/News/"
OUTPUT_DIR = "news" 

year_news_endpoints = get_urls_matching_pattern(url, pattern)
all_news_links = get_all_news_links_from_endpoints(year_news_endpoints, url)

for link in all_news_links:
    md = extract_content_and_convert_to_markdown(link)
    formatted_date = create_file_name(link, base_url)
    if formatted_date:
        folder_path = os.path.join(SCRIPT_DIR, OUTPUT_DIR, formatted_date.split("/")[0])
        os.makedirs(folder_path, exist_ok=True)
        file_path = os.path.join(folder_path, formatted_date.split("/")[1])
        write_markdown_to_file(md, file_path)
        
        
        
        
        

