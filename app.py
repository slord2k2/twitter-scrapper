import json
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains


def initialize_driver():
    """
    Initialize the Selenium web driver with the appropriate browser(preferred Chrome) and options.
    Returns:
        driver (webdriver.Chrome): The initialized web driver.
    """
    chromedriver_path = 'chromedriver.exe' #Path of chrome webdriver  # Set the path to the web driver for your preferred browser
    service = Service(chromedriver_path)
    driver = webdriver.Chrome(service=service)
    return driver


def login_twitter(driver, username, password):
    """
    Login to Twitter using the provided username and password.
    Args:
        driver (webdriver.Chrome): The web driver instance.
        username (str): Twitter username.
        password (str): Twitter password.
    """
    # Open the Twitter login page
    driver.get('https://twitter.com/login')

    # Wait until the username input field is present
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//input[@autocomplete="username" and @type="text"]')))
    username_input = driver.find_element(By.XPATH, '//input[@autocomplete="username" and @type="text"]')
    username_input.send_keys(username)

    # Click the 'Next' button to proceed to the password input field
    next_button = driver.find_element(By.XPATH, '//span[contains(text(), "Next")]')
    next_button.click()

    # Wait until the password input field is present
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//input[@autocomplete="current-password" and @type="password"]')))
    password_input = driver.find_element(By.XPATH, '//input[@autocomplete="current-password" and @type="password"]')
    password_input.send_keys(password)

    # Click the 'Log in' button to submit the login credentials
    login_button = driver.find_element(By.XPATH, '//span[contains(text(), "Log in")]')
    login_button.click()

    print('Successfully logged in to Twitter!')


def crawl_twitter_profiles(driver, username_list):
    """
    Crawl the Twitter profiles for the given list of usernames and extract desired information.
    Args:
        driver (webdriver.Chrome): The web driver instance.
        username_list (list): List of usernames to crawl.
    Returns:
        profile_data (list): List of profile information dictionaries.
    """
    profile_data = []

    for username in username_list:
        profile_url = 'https://twitter.com/' + username
        driver.get(profile_url)

        # Wait until the follower count element is present
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@class="css-1dbjc4n r-13awgt0 r-18u37iz r-1w6e6rj"]/div/a//span[@class="css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0"]')))

        # Create a dictionary to store profile information
        profile_info = {
            'username': username,
            'No. of followers': None,
            'No. of following': None,
            'tweets': None,
        }

        # Extract follower and following counts
        elements = driver.find_elements(By.XPATH, '//div[@class="css-1dbjc4n r-13awgt0 r-18u37iz r-1w6e6rj"]/div/a//span[@class="css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0"]')
        values = []
        for element in elements:
            value = element.text
            values.append(value)
        profile_info['No. of following'] = values[0]
        profile_info['No. of followers'] = values[2]

        # Extract the number of tweets
        elements = driver.find_elements(By.XPATH, '//div[@dir="ltr" and @class="css-901oao css-1hf3ou5 r-1bwzh9t r-37j5jr r-n6v787 r-16dba41 r-1cwl3u0 r-bcqeeo r-qvutc0"]')
        if elements:
            element = elements[0]  # Get the first WebElement from the list
            profile_info['tweets'] = element.text.split()[0]

        profile_data.append(profile_info)

    return profile_data

def tweets_data(driver, username):
    """
    Crawl and extract tweets data for a given Twitter username.
    Args:
        driver (webdriver.Chrome): The web driver instance.
        username (str): Twitter username.
    """
    profile_url = 'https://twitter.com/' + username
    driver.get(profile_url)

    # Wait until the tweet articles are present
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        (By.XPATH, "//article[@data-testid='tweet']")))

    # Initialize lists to store tweet data
    UserTags = []
    TimeStamps = []
    Tweets = []
    Replys = []
    reTweets = []
    Likes = []

    # Extract data for each tweet
    articles = driver.find_elements(
        By.XPATH, "//article[@data-testid='tweet']")
    for article in articles:
        # Extract user tag
        UserTag = driver.find_element(
            By.XPATH, "//div[@data-testid='User-Name']").text
        UserTags.append(UserTag)

        # Extract timestamp
        TimeStamp = driver.find_element(
            By.XPATH, '//time').get_attribute('datetime')
        TimeStamps.append(TimeStamp)

        # Extract tweet text
        Tweet = driver.find_element(
            By.XPATH, '//div[@data-testid="tweetText"]').text
        Tweets.append(Tweet)

        # Extract reply count
        Reply = driver.find_element(
            By.XPATH, '//div[@data-testid="reply"]').text
        Replys.append(Reply)

        # Extract retweet count
        reTweet = driver.find_element(
            By.XPATH, "//div[@data-testid='retweet']").text
        reTweets.append(reTweet)

        # Extract like count
        Like = driver.find_element(
            By.XPATH, '//div[@data-testid="like"]').text
        Likes.append(Like)

        # Store data in a DataFrame and save it as JSON
        try:
            existing_data = pd.read_json('tweets_live.json')
        except FileNotFoundError:
            existing_data = pd.DataFrame()

        df = pd.DataFrame(zip(UserTags, TimeStamps, Tweets, Replys, reTweets, Likes),
                          columns=['UserTags', 'TimeStamps', 'Tweets', 'Replys', 'reTweets', 'Likes'])
        combined_data = existing_data.append(df, ignore_index=True)
        combined_data.drop_duplicates(subset=['Tweets'], inplace=True)
        combined_data = combined_data.dropna(how='any')
        combined_data.to_json('tweets_live.json', orient='records')


def save_data_to_json(data, filename):
    """
    Save data to a JSON file.
    Args:
        data (list/dict): Data to be saved.
        filename (str): Name of the JSON file.
    """
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)
    print(f'Data saved to {filename}')


if __name__ == '__main__':
    # Twitter account credentials
    twitter_username = 'YOUR_TWITTER_USERNAME'
    twitter_password = 'YOUR_TWITTER_PASSWORD'

    # Read the usernames from the text file
    with open('usernames.txt', 'r') as file:
        username_list = [line.strip() for line in file]

    driver = initialize_driver()
    login_twitter(driver, twitter_username, twitter_password)

    # Crawl Twitter profiles
    crawled_data = crawl_twitter_profiles(driver, username_list)
    save_data_to_json(crawled_data, 'twitter_profiles.json')

    # Crawl and extract tweets data
    for username in username_list:
        tweets_data(driver, username)

    driver.quit()
