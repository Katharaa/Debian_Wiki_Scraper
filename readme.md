
Debian Wiki Scraper (Task for outreachy)
====================================

Table of Contents
-----------------

*   [System Requirements](#system-requirements)
*   [Installation](#installation)
    *   [Python Installation](#python-installation)
    *   [Creating a Virtual Environment](#creating-a-virtual-environment)
    *   [Library Dependencies](#library-dependencies)
        *   [Requirements.txt File](#requirements-txt-file)
        *   [Using requirements.txt](#using-requirements-txt)
*   [How to Run the Script](#how-to-run-the-script)
*   [Comment Options](#comment-options)
*   [Project Milestone](#project-milestone)
*   [Conclusion](#conclusion)

System Requirements
-------------------

Before proceeding, ensure your system meets the following prerequisites:

*   Python (version I'm using [Python 3.11.6](https://www.python.org/downloads/))
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
    
Installing pip: 

If pip is not already installed in your virtual environment, you can install it using the following command:

    python -m ensurepip --default-pip

### Library Dependencies

You can manage the required Python libraries using a `requirements.txt` file for easy installation and version control.

I have attached the `requirements.txt` file, and you can install the libraries by running the following command:

    
    pip install -r requirements.txt
    

This will install the specified libraries and their required versions, making it easier to manage and share dependencies for your project.

How to Run the Script
---------------------

To run the script, follow these steps:

1.  Open a terminal.
2.  Navigate to the directory containing the script.
3.  Run the script with the following command, where `debian_wiki` contains your python script:

    
    python debian-wiki.py -i urls.json
    

Comment Options
---------------

You can use the script with the following comment options:

*   `python debian_wiki.py -h`: Display the help message and available options.
*   `python debian_wiki.py -i <input_file>`: Execute the script with an input file containing a list of URLs and relative paths for saving Markdown files. If no input file is provided, the script will look for a default input file named `urls.json` in the project directory. You can customize the input data with this option.

### Environment (Customizable)

The script operates in two environments, which can be customized using the `ENV` environment variable:

*   **Development (DEV)**: In this environment, the script limits the number of matched URLs to the latest 2 years. This environment is suitable for testing and development.
*   **Production (PROD)**: In the production environment, no limitations are imposed, allowing the script to scrape without constraints.

To set the environment, you can use the `ENV` environment variable in the command. For example:

ENV=DEV python debian_wiki.py -i urls.json

ENV=PROD python debian_wiki.py -i urls.json

The choice of environment affects the behavior of the script, particularly the number of years for scraping and the number of matched URLs. You can select the appropriate environment based on your specific use case.

Project Milestone
-----------------

*   \[x\] Create functions to extract news content from various sections on the Debian Wiki.
*   \[x\] Extract content from the general news section, latest news, Debian project news, and security announcements.
*   \[x\] Organize the extracted data into a structured dictionary format.
*   \[x\] Implement a function to save the parsed data to a Markdown file.
*   \[x\] Modify the script to extract and save news data from different years into separate files, for better organization and easier access to historical news.
*   \[ \] Containerization of the entire web scraping project.

Conclusion
----------

In this project, we set out to modernize the Debian Wiki by developing a web scraping script that extracts news content from various sections on the Debian Wiki and converts it into Markdown format. This project represents a significant step in improving the accessibility and usability of the Debian Wiki's valuable news articles.