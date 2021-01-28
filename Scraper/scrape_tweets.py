import time
import csv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import SessionNotCreatedException
from webdriver_manager.chrome import ChromeDriverManager
from os import path

#  ----------------------  GLOBAL VARIABLES  ----------------------
scraped_elements_count = 0
scraped_elements = []
scroll_max = int(input('Enter the scroll count to determine the tweet count(1 scroll is average 8 - 13 tweets):'))
scroll_delay = int(input('Enter the delay duration after each scroll to load the new tweets: '))


# ----------------------  EXCEPTION CLASS  ----------------------

class NotFoundError(Exception):
    # Throw when something can't be found
    pass


class CsvWriteError(Exception):
    # Throw if there is any problem while writing the CSV file
    pass


class DriverPathError(Exception):
    # Throw if the selenium driver location is wrong
    pass


#  ----------------------   FUNCTIONS  ----------------------
def run_browser():
    # driver_path = 'C:\\bin\\chromedriver.exe' 
    if path.exists('selenium_driver_path.txt'):  # after the first initialization you dont have to enter the driver path all the time
        with open('selenium_driver_path.txt','r') as file:
            driver_path = file.read()
    else:    # if file is not created, create and save the driver path for the next runs
        driver_path = input('Please enter the selenium driver path here: ')
        with open('selenium_driver_path.txt','w') as file:
            file.write(driver_path)
    if path.exists(driver_path):
        try:
            web_browser = webdriver.Chrome(executable_path=driver_path)
        except (RuntimeError):
                print('There is a problem while running webdriver. Please check driver path\n')
        except SessionNotCreatedException:
            print('Selenium web driver version is not updated. Updating...')
            web_browser = webdriver.Chrome(ChromeDriverManager().install())
    else:
        raise FileNotFoundError('Selenium Web Driver is not found. Please check driver path')
                    
    return web_browser

def scroll_page():
    last_height = browser.execute_script('return document.body.scrollHeight')
    browser.execute_script(
        'window.scrollTo(0,document.body.scrollHeight);')  # scroll and wait for loading of the new tweets
    time.sleep(scroll_delay)
    new_height = browser.execute_script('return document.body.scrollHeight')

    if last_height == new_height:  # means we are at the bottom of the page thus we cannot scroll down anymore
        return
    else:  # means we continue to scroll down
        last_height = new_height


def scrape_data():
    global scraped_elements_count
    page_source = browser.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    tweets_container = soup.find_all("div", attrs={"data-testid": "tweet"})

    try:
        tweets_container[0]
    except IndexError:
        raise NotFoundError(
            'No elements found. Probably scraping started before loading the web page.\nPlease increase waiting time')
    for element in tweets_container:
        author = element.find("div", attrs={
            'class': 'css-901oao css-bfa6kz r-111h2gw r-18u37iz r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo '
                     'r-qvutc0'}).get_text().strip()
        tweet_date = element.find("a", attrs={
                    'class': 'css-4rbku5 css-18t94o4 css-901oao r-111h2gw r-1loqt21 r-1q142lx r-1qd0xha r-a023e6 r-16dba41 \
                        r-ad9z0x r-bcqeeo r-3s2u2q r-qvutc0'})
        tweet_text = element.find('div', attrs={
            'class': 'css-901oao r-jwli3a r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0'}) \
            .get_text().strip()
        tweet_comments = element.find('div', attrs={'data-testid': 'reply'}).get_text().strip()
        tweet_retweets = element.find('div', attrs={'data-testid': 'retweet'}).get_text().strip()
        tweet_likes = element.find('div', attrs={'data-testid': 'like'}).get_text().strip()

        tweet_stats = {
            'author': author,
            'date': '-' if tweet_date is None else tweet_date.string,
            'text': tweet_text.replace(',', '').replace('\n', ' '),
            'comment': '0' if not tweet_comments else tweet_comments,
            'retweet': '0' if not tweet_retweets else tweet_retweets,
            'like': '0' if not tweet_likes else tweet_likes
        }

        if tweet_stats not in scraped_elements:  # eliminate if there are duplicates
            scraped_elements.append(tweet_stats)
            scraped_elements_count = scraped_elements_count + 1
            # print("\n***********************************\nTweet:" + str(scrapedElementCount) + "\n" + tweetText)
        else:
            continue


def check_if_page_loaded():
    page_source = browser.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    tweet = soup.find_all('div', attrs={'data-testid': 'tweet'})

    if not tweet:
        return False
    else:
        return True


def export_to_csv_file(source_data):
    try:
        file = open('tweets.csv', "w", encoding="utf-8")
        writer = csv.writer(file)
        writer.writerow(('Author', 'Date', 'Text', 'Comment', 'Retweet', 'Like'))  # header row
        for data in source_data:
            writer.writerow(
                (data['author'], data['date'], data['text'], data['comment'], data['retweet'], data['like']))
    except CsvWriteError:
        print('An error occurred while writing the file.')
    finally:
        file.close()


# ----------------------  MAIN FUNCTION  ----------------------

# search key => 'request for startup'
search_key = input('Enter the keyword to search on Twitter: '). \
    replace(' ', '%20')  # replace spaces with "%20" for twitterUrl
source_url = 'https://twitter.com/search?q=' + search_key + '&src=typed_query&f=live'  # for latest tweets

browser = run_browser()
browser.delete_all_cookies()  # to prevent blocking
browser.get(source_url)  # navigate to destination site

current_time = 0
max_waiting_time = 30
while not check_if_page_loaded():
    print('\n----- Web page is not loaded yet waiting for another 1 second -----\n')
    time.sleep(1)
    current_time += 1
    if current_time == max_waiting_time:
        print("Page could not be loaded. Check your internet connection.")
        browser.close()
        break

if current_time < max_waiting_time:
    print('\n----- Web page loaded successfully ! -----\n')
    # get everything about tweets
    for i in range(scroll_max):
        scrape_data()
        scroll_page()

    export_to_csv_file(scraped_elements)
    print(f'\n----- {scraped_elements_count} Tweets Exported To CSV File ! -----\n')
    browser.close()

    # for index in range(15):
    #    print('{0}.Tweet:\n{1}\n'.format(str(index + 1), str(scraped_elements[index])))
