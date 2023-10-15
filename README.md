Task 1 - Modernizing the Debian Wiki
====================================


Task Description
----------------

In Task 1, we aim to modernize the Debian Wiki by developing a simple script that performs the following actions:

1.  Read the content from the News page in the Debian Wiki.
2.  Parse the data to extract meaningful information.
3.  Write the parsed content to a file in Markdown format.

Table of Contents
-----------------

*   [System Requirements](#system-requirements)
*   [Installation](#installation)
    *   [Python Installation](#python-installation)
    *   [Creating a Virtual Environment](#creating-a-virtual-environment)
    *   [Library Dependencies](#library-dependencies)
        *   [Requirements.txt File](#requirements-txt-file)
        *   [Using requirements.txt](#using-requirements-txt)
*   [Script Code Explanation](#script-code-explanation)
*   [How to Run the Script](#how-to-run-the-script)
*   [Conclusion](#conclusion)

System Requirements
-------------------

Before proceeding, ensure your system meets the following prerequisites:

*   You need to have Firefox and the GeckoDriver installed.
*   Python (version I'm using [Python 3.11.6])
*   An internet connection for downloading dependencies :)
*   I'm using Debian Unstable Version

Installation
------------

### Python Installation

If Python is not already installed on your system, you can download it from the [official Python website](https://www.python.org/downloads/).

### Creating a Virtual Environment

We recommend working within a virtual environment to manage project dependencies. You can create a virtual environment using the following command:

    python -m venv myenv

Activate the virtual environment:

    source myenv/bin/activate  

### Library Dependencies

You can manage the required Python libraries using a \`requirements.txt\` file for easy installation and version control.

I have attached the requirements.txt file, you can install the libraries by running the following command:

    
    pip install -r requirements.txt
    

This will install the specified libraries and their required versions, making it easier to manage and share dependencies for your project.

Script Code Explanation
-----------------------

Here's an explanation of the key parts of the Python script:

    
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
    def remove_lines_and_words_within_tilde(filename):
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read()
    
        # Remove lines within ~ and ~
        content = re.sub(r'~(.*?)~', '', content, flags=re.DOTALL)
    
        # Remove words within ~ and ~
        content = re.sub(r'~(.*?)~', '', content)
    
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(content)
    
    # Remove strike through from the markdown file
    remove_lines_and_words_within_tilde(markdown_filename)
    
    # Quit the driver
    driver.quit()
    
    print(f"Data has been saved to {markdown_filename}")
    
    

How to Run the Script
---------------------

To run the script, follow these steps:

1.  Open a terminal.
2.  Navigate to the directory containing the script.
3.  Run the script with the following command,  where debian_wiki.py is your python script




     python debian_wiki.py


Conclusion
----------

By following the steps outlined in this documentation, you will get a markdown file ("debian_wiki_data.md") which contains the extracted data from the debian-wiki News page.
