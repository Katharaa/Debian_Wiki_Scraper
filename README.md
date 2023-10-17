Task 1 - Modernizing the Debian Wiki
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


How to Run the Script
---------------------

To run the script, follow these steps:

1.  Open a terminal.
2.  Navigate to the directory containing the script.
3.  Run the script with the following command,  where debian_wiki contains your python script


     python debian_wiki.py


Conclusion
----------

By following the steps outlined in this documentation, you can extract data from the News page and converting it to Markdown format.
