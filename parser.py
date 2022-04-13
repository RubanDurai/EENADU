from typing import List
from bs4 import BeautifulSoup
import logging
import json
import time
from datetime import date, timedelta

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options    

from utils import Editions

logger = logging.getLogger(__name__)

class eenaduParser:

    def __init__(self, cookies: str, date: str = None):
        self.driver = None
        self._data: str = None
        self._links = []
        self.edition = None
        self.cookies = cookies
        self.date: str = date
        if self.date is None:
            self.date = self._get_today_date()
            logger.info("date is not set, using today's date %s!", self.date)

        ff_options = Options()
        ff_options.add_argument('--headless')
        self.driver = webdriver.Firefox(options=ff_options)
        self.driver.get("https://epaper.eenadu.net")
        self._inject_cookies()

    def _extract_images(self):
        soup = BeautifulSoup(self._data, "lxml")

        page_selector = soup.find("div", {"class": "owl-stage-outer"})
        page_images = page_selector.find_all("img")

        for page in page_images:
            #jpg is image background, png is text layer
            self._links.append((page.attrs["xhighres"], page.attrs["xhighres"].replace("hr.jpg", "hr.png")))
        logger.info("total links = %d | pages = %d", len(self._links), len(self._links) / 2)

    def _get_today_date(self):
        today = date.today()
        if time.localtime().tm_hour < 6:
            logger.warn("localtime.hour < 6: going back 1 day!")
            today = today - timedelta(days=1)
        return today.strftime("%d/%m/%Y")

    def _inject_cookies(self):
        logger.info("reading cookies from %s.", self.cookies)
        f = open(self.cookies, "r")
        data = json.loads(f.read())
        f.close()

        for k,v in data.items():
            if k == "changeddate":
                self.driver.add_cookie({"name": k, "value": "{}".format(self.date)})
            else:
                self.driver.add_cookie({"name": k, "value": v})


    def _run_mitigation(self):
        try:
            self.driver.find_element(By.ID, "btn_close_slow_net").click()
        except:
            pass

        try:
            self.driver.find_element(By.CLASS_NAME, "izooto-optin--cta-later").click()
        except:
            pass

    def get_edition(self, edition: Editions):

        self.edition = edition
        logger.info("requested edition: %s", self.edition.name)

        E: List = self.driver.find_elements(By.CLASS_NAME, "ep_ed_img")
        logger.debug("front page banners: %d", len(E))
        
        match edition:
            case Editions.TELANGANA:
                E[2].click()
            case Editions.ANDHRAPRADESH:
                E[0].click()
            case Editions.HYDERABAD:
                E[1].click()
            case Editions.SUNDAY:
                self.driver.find_element(By.ID, "span_SundayMagazine").click()
        
        logger.info("sleeping for 5 second!")
        time.sleep(5)

        self._run_mitigation()
        self._data = self.driver.execute_script("return document.body.innerHTML")           
        self._extract_images()
        self.driver.close()

    def get_links(self):
        return self._links

    def gen_filename(self) -> str:
        return "eenadu_{date}_{edition}.pdf".format(date=self.date.replace("/", "-"), edition=self.edition.name)