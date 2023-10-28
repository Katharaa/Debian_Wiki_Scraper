import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from markdownify import markdownify
import re
import os


script_dir = os.path.dirname(__file__)

def fetch_all_urls(url):
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


def is_valid_date_url(url):
    # Use regular expression to match the pattern
    match = re.match(r'https://www.debian.org/News/(\d{4})/(\d{4})(\d{2})(\d{2})$', url)
    if match:
        year, full_year, month, day = match.groups()
        if year == full_year and re.match(r'^(0[1-9]|1[0-2])$', month) and re.match(r'^(0[1-9]|[12][0-9]|3[01])$', day):
            return True
    return False


def get_all_news_links_from_endpoints(news_endpoints):
    valid_news_url = []
    for endpoint in news_endpoints:
        all_links = fetch_all_urls(endpoint)
        for link in all_links:
            if is_valid_date_url(link):
                print("Got valid news URL:", link)
                valid_news_url.append(link)
    return valid_news_url




def convert_relative_links_to_absolute(soup, base_url):
    # Find all anchor (a) tags in the HTML
    links = soup.find_all('a')

    # Convert relative links to absolute links
    for link in links:
        href = link.get('href')
        if href:
            full_url = urljoin(base_url, href)
            link['href'] = full_url

def extract_content_and_convert_to_markdown(url):
    try:
        # Send an HTTP GET request to the URL
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content with BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')

            # Convert relative links to absolute links using the base URL
            convert_relative_links_to_absolute(soup, url)

            # Find the element with id="content"
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

def create_file_name(url, output_dir):
    if url.startswith("https://www.debian.org/News/"):
        last_part = url[len("https://www.debian.org/News/"):]

        # Reformat the date part to "DD-MM"
        parts = last_part.split("/")
        if len(parts) >= 2 and all(part.isdigit() for part in parts[:2]):
            year = parts[0]
            date = parts[1][:8]  
            formatted_date = f"{date[6:8]}-{date[4:6]}"  
            
            year_dir = os.path.join(output_dir, year)
            os.makedirs(year_dir, exist_ok=True)
            file_path = os.path.join(year_dir, formatted_date + ".md")
            return file_path

url = "https://www.debian.org/News/"
pattern = r'https://www.debian.org/News/\d{4}/$'
year_news_endpoints = get_urls_matching_pattern(url, pattern)
all_news_links = get_all_news_links_from_endpoints(year_news_endpoints)
output_dir = os.path.join(script_dir, "news")

for link in all_news_links:
    md = extract_content_and_convert_to_markdown(link)
    file_path = create_file_name(link, output_dir)
    if file_path:
        write_markdown_to_file(md, file_path)
