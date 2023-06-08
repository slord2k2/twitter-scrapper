# Twitter Data Crawler

This project is a Python script that utilizes the Selenium library to crawl data from multiple Twitter profiles. It extracts information such as followers, following, tweets, likes, and retweets from the specified profiles.

## Files
The repository contains the following files:

   - app.py: The main Python script that implements the crawling functionality.
   - chromedriver.exe: The Chrome WebDriver executable required for Selenium automation.
   - requirements.txt: A file specifying the dependencies required to run the script.
   - usernames.txt: A text file where you can provide the usernames of the Twitter profiles to crawl.
    
## Installation

To use this script, follow these steps:
1. Clone the repository to your local machine using the command:
   '
   git clone https://github.com/slord2k2/twitter-scrapper 
   '
2. Download the Chrome WebDriver executable appropriate for your operating system
3. Place the downloaded chromedriver.exe file in the same directory as the app.py script.
4. Install the required dependencies by running the following command:
   '
   pip install -r requirements.txt 
   '
5. Place the usernames of the Twitter profiles you want to crawl in the usernames.txt file. Each username should be on a separate line.

Usage

To run the Twitter data crawler, execute the following command:
   ' 
   python app.py 
   '


Notes

   - The script utilizes Selenium and requires the chromedriver.exe file to be present in the same directory.
   - Make sure to have a stable internet connection while running the script.
   - If you encounter any issues or have any questions, feel free to reach out.
