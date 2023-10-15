from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import json
import pandas as pd
import markdown
import re

# Specify the path to the Firefox binary
firefox_binary_path = "/usr/bin/firefox"  # Replace with your Firefox binary path

# Configure Firefox options
firefox_options = webdriver.FirefoxOptions()
firefox_options.binary_location = firefox_binary_path

# Create a Firefox WebDriver instance
driver = webdriver.Firefox(options=firefox_options)

class DebianWiki:
    def __init__(self):
        self.base_url = 'https://wiki.debian.org/'
    
    # This function will create a dictionary to store the contents of the 1st page
    def create_dict(self):
        # Home page
        driver.get('https://wiki.debian.org/')
        print('Loading Debian Wiki.....')
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="content"]/div[2]/table/tbody/tr[2]/td[1]/p/a[1]')))
    
        # Click on the news link
        news = driver.find_element(By.XPATH, '//*[@id="content"]/div[2]/table/tbody/tr[2]/td[1]/p/a[1]')
        news.click()
        print('Loading news page.....')
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="content"]/ul[1]/li[1]/p/a')))
        
        d = {}
        
        # News
        news = driver.find_element(By.XPATH, '//*[@id="pagelocation"]/li/a')
        line = driver.find_element(By.XPATH, '//*[@id="content"]/p[4]')
        
        d[news.text] = line.text
        
        # General news
        general_news = driver.find_element(By.XPATH, '//*[@id="General_news"]')
        latest_news = driver.find_element(By.XPATH, '//*[@id="content"]/ul[1]/li[1]/p/a')
        debian_project_news = driver.find_element(By.XPATH, '//*[@id="content"]/ul[1]/li[2]/p/a[1]')
        debian_security_announce = driver.find_element(By.XPATH, '//*[@id="content"]/ul[1]/li[3]/p/a')
        
        d[general_news.text] = {}
        d[general_news.text][latest_news.text] = {}
        d[general_news.text][debian_project_news.text] = {}
        d[general_news.text][debian_security_announce.text] = {}
        
        # News for Debian contributors
        ndc = driver.find_element(By.XPATH, '//*[@id="News_for_Debian_contributors"]')
        a = driver.find_element(By.XPATH, '//*[@id="content"]/dl')
        b = a.find_elements(By.TAG_NAME, 'dt')
        c = a.find_elements(By.TAG_NAME, 'p')
        
        d[ndc.text] = {}
        for i, j in zip(b, c):
            d[ndc.text][i.text] = j.text
        
        return d
    
    # This function extracts all the latest news links
    def extract_all_links(self):
        # Home page
        driver.get('https://wiki.debian.org/')
        print('Loading Debian Wiki.....')
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="content"]/div[2]/table/tbody/tr[2]/td[1]/p/a[1]')))
    
        # Click on the news link
        news = driver.find_element(By.XPATH, '//*[@id="content"]/div[2]/table/tbody/tr[2]/td[1]/p/a[1]')
        news.click()
        print('Loading news page.....')
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="content"]/ul[1]/li[1]/p/a')))
    
    ###################################### LATEST NEWS #####################################
        # Click on the latest news link
        latest_news = driver.find_element(By.XPATH, '//*[@id="content"]/ul[1]/li[1]/p/a')
        latest_news.click()
        print('Loading latest news page.....')
        sleep(5)
    
        # Get the links of the various latest news
        a = driver.find_element(By.XPATH, '//*[@id="content"]/p[1]')
        b = a.find_elements(By.TAG_NAME, 'a')
        latest_news_links = []
        for i in range(0, len(b)):
            latest_news_links.append(b[i].get_attribute('href'))
        
        # Get back to the previous page
        driver.back()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="content"]/ul[1]/li[2]/p/a[1]')))
        
    ###################################### DEBIAN PROJECT NEWS #####################################
        # Click on the debian project news link
        debian_project_news = driver.find_element(By.XPATH, '//*[@id="content"]/ul[1]/li[2]/p/a[1]')
        debian_project_news.click()
        print('Loading debian project news page....')
        sleep(5)
        
        # Get the links of various debian project news
        a = driver.find_element(By.XPATH, '//*[@id="content"]/p[3]')
        b = a.find_elements(By.TAG_NAME, 'a')
        debian_project_news_links = []
        for i in range(0, len(b)):
            debian_project_news_links.append(b[i].get_attribute('href'))
        
        # Get back to the previous page
        driver.back()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="content"]/ul[1]/li[3]/p/a')))
        
    ###################################### DEBIAN SECURITY ANNOUNCE #####################################
        # Click on the debian security announce
        debian_security_announce = driver.find_element(By.XPATH, '//*[@id="content"]/ul[1]/li[3]/p/a')
        debian_security_announce.click()
        print('Loading debian security announce page....')
        sleep(5)
        
        # Get the links of various debian project news
        a = driver.find_element(By.XPATH, '//*[@id="content"]/p[11]')
        b = a.find_elements(By.TAG_NAME, 'a')
        debian_security_announce_links = []
        for i in range(0, len(b)):
            debian_security_announce_links.append(b[i].get_attribute('href'))
        
        return latest_news_links, debian_project_news_links, debian_security_announce_links
    
    # This helper function extracts all the news from the given latest_news_links, debian_project_news_link
    def extract_news_helper(self, links):
        dic = {}
    
        # Iterate through all links
        for i in range(0, len(links)):
            a = driver.get(links[i])
            print(f'Loading {i+1}th link....')
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="content"]')))
        
            b = driver.find_element(By.XPATH, '//*[@id="content"]')
        
            # Extracting the title
            title = b.find_element(By.TAG_NAME, 'h1').text
        
            # Extracting the news
            news_para = b.find_elements(By.TAG_NAME, 'p')
            l = []
            for i in range(0, len(news_para)):
                l.append(news_para[i].text)
            news = ' '.join(l)
        
            # Appending the title: news as keys: values pairs in dictionary
            dic[title] = news
        
        return dic
    
    # This function will specially extract news from security announce
    def extract_news_security_announce(self, links):
        dic = {}
        
        for i in range(0, len(links)):
            a = driver.get(links[i])
            print(f'Loading {i+1}th link....')
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="content"]')))
            
            b = driver.find_element(By.XPATH, '//*[@id="content"]')
            title = b.find_element(By.TAG_NAME, 'h2').text
            dic[title] = {}
            
            # Since the info on this page is in the form of a dict as well hence I will store it in dictionary format
            # The keywords are common in all pages
            # It can be also stored in a pandas dataframe
            c = b.find_element(By.XPATH, '//*[@id="content"]/dl')
            d = c.find_elements(By.TAG_NAME, 'dt')
            e = c.find_elements(By.TAG_NAME, 'dd')
            for i, j in zip(d, e):
                dic[title][i.text.split(':')[0]] = j.text
            
        return dic
    
    # Extracting all news
    def extract_news(self, latest_news_links, debian_project_news_links, debian_security_announce_links, dic):
        print('----Extracting all latest news-------')
        dic['General news']['Latest News'] = self.extract_news_helper(latest_news_links)
        
        print('-----Extracting all Debian project news-----')
        dic['General news']['Debian Project News'] = self.extract_news_helper(debian_project_news_links)
        
        print('-----Extracting all Debian security announce-----')
        dic['General news']['debian-security-announce'] = self.extract_news_security_announce(debian_security_announce_links)
        
        return dic
    #saving into a markdown file
    def save_to_markdown_file(self, data, filename):
        with open(filename, 'w', encoding='utf-8') as file:
            for section, content in data.items():
                file.write(f"## {section}\n\n")
                if isinstance(content, dict):
                    for subsection, subsection_content in content.items():
                        file.write(f"### {subsection}\n\n")
                        if isinstance(subsection_content, dict):
                            for subsubsection, subsubsection_content in subsection_content.items():
                                file.write(f"#### {subsubsection}\n\n")
                                if isinstance(subsubsection_content, str):  # Check if it's a string
                                    subsubsection_content = re.sub(r'~~(.*?)~~', r'\1', subsubsection_content)
                                    file.write(f"{subsubsection_content}\n\n")
                                else:
                                    # Handle other cases, e.g., it could be a list or other data
                                    file.write(f"Unknown content: {subsubsection_content}\n\n")
                        else:
                            if isinstance(subsection_content, str):  # Check if it's a string
                                subsection_content = re.sub(r'~~(.*?)~~', r'\1', subsection_content)
                                file.write(f"{subsection_content}\n\n")
                            else:
                                # Handle other cases if needed
                                file.write(f"Unknown content: {subsection_content}\n\n")
                else:
                    if isinstance(content, str):  # Check if it's a string
                        content = re.sub(r'~~(.*?)~~', r'\1', content)
                        file.write(f"{content}\n\n")
                    else:
                        # Handle other cases if needed
                        file.write(f"Unknown content: {content}\n\n")


# Define the filename for the markdown file
markdown_filename = "debian_wiki_data.md"

# Create an instance of the DebianWiki class
dw = DebianWiki()

# Extract the data
dic = dw.create_dict()
latest_news_links, debian_project_news_links, debian_security_announce_links = dw.extract_all_links()
dic = dw.extract_news(latest_news_links, debian_project_news_links, debian_security_announce_links, dic)

# Save the data to the markdown file
dw.save_to_markdown_file(dic, markdown_filename)


# Function to remove the strike through in the file
def remove_strike_through(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        content = file.read()


    content = re.sub(r'~(.*?)~', '', content, flags=re.DOTALL)

    content = re.sub(r'~(.*?)~', '', content)

    with open(filename, 'w', encoding='utf-8') as file:
        file.write(content)
# Remove lines and words within ~ and ~ from the markdown file
remove_strike_through(markdown_filename)

# Quit the driver
driver.quit()

print(f"Data has been saved to {markdown_filename}")

