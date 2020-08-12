##########################
# Author : Sushant Moon
# Date : 11 August 2020
##########################


from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys

import logging
import argparse
from datetime import datetime


class Sel(object):
    def __init__(self):
        # self.driver = webdriver.Firefox(executable_path="/usr/bin/geckodriver")
        self.driver = webdriver.Chrome(
            executable_path="/home/lorenzo/geckodriver/Chrome/chromedriver_linux64/chromedriver"
        )

        # self.driver = webdriver.PhantomJS()
        # self.driver.set_window_size(1120, 550)
        # self.driver.implicitly_wait(30) #### commention as we are using
        self.verificationErrors = []
        self.accept_next_alert = True
        logging.info("Selenium Object Initialized")
        super().__init__()

    def __del__(self):
        self.driver.close()
        self.driver.quit()
        logging.info("Cleaned and Deleted the Selenium Webdriver Instance")


class DiceCrawler(Sel):
    def __init__(self, detailed_html):
        self.base_url = "https://www.dice.com/"
        self.TIMEOUT = 30  ### seconds
        self.fileName = detailed_html
        self.wait = None
        super().__init__()

    def __del__(self):
        super().__del__()
        logging.info("Deleting the DiceCrawler Object")

    def extractDetailsFromDiceLinks(self, jobLinks):
        dfile = open(self.fileName, 'w')
        for position, jobLink in enumerate(jobLinks, start=1):
            print(10*"*" + "  "+str(position)+"  " + 10*"*")
            print(jobLink)

            logging.info("Crawling #{}: {}".format(position, jobLink))

            # open tab
            self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.CONTROL + 't')
            # You can use (Keys.COMMAND + 't') on OSX and (Keys.CONTROL + 't') on other OSs

            self.driver.get(jobLink)
            self.wait.until(
                EC.visibility_of_element_located(
                    (By.ID, "jobdescSec")
                )
            )
            heading_1 = self.driver.find_element(By.ID, "jt").text
            heading_2 = self.driver.find_element(
                            By.CSS_SELECTOR,
                            ".location"
                        ).get_attribute("innerHTML")
            data = self.driver.find_element(By.ID, "jobdescSec")

            print(
                "<h2>#{position}<a href={link}>{jobTitle} - {location}</a></h2>".format(
                    position=position,
                    link=jobLink,
                    jobTitle=heading_1,
                    location=heading_2
                ),
                file=dfile
            )
            # print(data.get_attribute("innerHTML"))
            print(data.get_attribute("innerHTML"), file=dfile)
            print("\n\n", file=dfile)

            # close tab
            self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.CONTROL + 'w')

            print(20*"*")
        dfile.close()

    def crawl(self, job, location):
        self.driver.get(self.base_url)
        self.wait = WebDriverWait(
                self.driver,
                self.TIMEOUT                    # for AJAX to load
            )
        try:
            self.wait.until(
                EC.presence_of_element_located(
                    (By.ID, 'searchInput-div')
                )
            )
        except TimeoutException:
            print("Loading took too much time!")
            return

        currentTime = datetime.now()
        logging.info("Crawling starting ...")

        logging.info("Inputting job search string : {job}".format(job=job))
        jobTitleInput = self.driver.find_element(By.XPATH, "//input[@placeholder='Job title, skills or company']")
        jobTitleInput.send_keys(job)

        logging.info("Inputting location search string : {location}".format(location=location))
        jobTitleInput = self.driver.find_element(By.XPATH, "//input[@placeholder='Location (zip, city, state)']")
        jobTitleInput.send_keys(location)

        submitButton = self.driver.find_element(By.ID, 'submitSearch-button')
        submitButton.click()

        self.wait.until(
                EC.element_to_be_clickable(
                    (By.ID, "jobAlertSaveButton")
                )
            )

        logging.info("Extracting Job Links.")
        results = self.driver.find_elements(By.XPATH, "//a[@data-cy='card-title-link']")
        jobLinks = []
        for r in results:
            jobLink = r.get_attribute('href')
            jobLinks.append(jobLink)
            logging.debug("Obtained Link : {}".format(jobLink))

        self.extractDetailsFromDiceLinks(jobLinks)


def main(job, location, detailed_html):
    crawler = DiceCrawler(detailed_html)
    crawler.crawl(job, location)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Crawling Dice.com for job postings'
    )
    parser.add_argument('--job', help='Job Title', required=True)
    parser.add_argument('--location', help='Location (Zip, City, State)', required=True)
    parser.add_argument(
        '--detailed_html',
        default="dice-job-listings.html",
        help='Name of the file where the details should go.(Optional, filetype = html only)'
    )

    args = parser.parse_args()

    location = args.location
    job = args.job
    detailedHTML = args.detailed_html

    logging.basicConfig(
        level=logging.INFO,
        filename='DiceCrawler-' + datetime.now().strftime(
            "%m-%d-%Y_%H-%M-%S"
        ) + '.log',
        format='[%(levelname)s] (%(threadName)-10s) %(asctime)s : %(message)s',
        datefmt='%m/%d/%Y %I:%M:%S %p'
    )

    main(job, location, detailedHTML)
    logging.info("Exting the code")
