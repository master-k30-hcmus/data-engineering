from .repository import RepoCrawler

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

import re
import time

class TopicCrawler(RepoCrawler):
    def __init__(self):
        super().__init__()
        self.base_url = 'https://github.com/topics'
        self.query_params = 'o=desc&s=updated'  # sort by recently updated

    def crawl(self):
        soup = self.make_soup(url=self.base_url)
        page_source = soup.prettify()

        # fetch popular topics
        topics = self.find_by_xpath(page_source, '//*[@id="js-pjax-container"]/div[4]/div[2]//ul/li/a/@title')
        topics = [t.replace("Topic: ", "") for t in topics]
        all_repos = []
        for topic in topics:
            repos = self._parse_topic_page(topic)
            all_repos.extend(repos)
            break
        return all_repos

    def _parse_topic_page(self, topic: str):
        topic_url = f'{self.base_url}/{topic}?{self.query_params}'
        print(topic_url)
        chrome_options = webdriver.ChromeOptions() 
        chrome_options.add_argument("start-maximized")
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

        driver.get(topic_url)

        while True:
            try:
                WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="js-pjax-container"]/div[2]/div[2]/div/div[1]/form/button'))).click()
                time.sleep(3)
            except TimeoutException:
                print("No more LOAD MORE RESULTS button to be clicked")
                break
        print("Complete")
        time.sleep(10)
        page_source = driver.page_source
        driver.quit()
        soup = BeautifulSoup(page_source, 'lxml')
        links = soup.find_all('h3', class_ = "f3 color-text-secondary text-normal lh-condensed")
        topics_info = soup.find_all('h2', class_ ='h3 color-text-secondary')
        topic_info = topics_info[0].text.replace(",","")
        num_repo = re.findall(r'\d+', topic_info)
        print("Number of repo in this topic:", num_repo[0])
        repos = []

        count = 0
        for link in links:
            if count == 10:
                break
            repo_raw = link.text.replace(" ", "")
            repo_raw = repo_raw.replace("\n", "")
            repo_raw = re.split('/', repo_raw)
            link_repo = f'https://github.com/{repo_raw[0]}/{repo_raw[1]}'
            print("Repo need to prase: ",link_repo)
            repo = self.parse_repo(link_repo)
            if repo:
                repo.update({"topic": topic})
                repos.append(repo)
            count = count + 1
        return repos