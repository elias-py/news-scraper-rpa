import logging
import re
import time
import calendar

from tqdm import tqdm
import pandas as pd
from RPA.Browser.Selenium import Selenium
from SeleniumLibrary.errors import ElementNotFound
from datetime import datetime

browser_lib = Selenium()

logging.basicConfig(level=logging.INFO)

money_regex = re.compile(r'\$\d{1,3}(,\d{3})*(\.\d{1,2})?|\d+\s(dollars|USD)')

class ExtractNewsInfo:

    URL = "https://nytimes.com"

    def __init__(self, search_phrase: str, section: str, months: int) -> None:
        self.search_phrase = search_phrase
        self.section = section
        self.months = int(months)

        self.titles = []
        self.descriptions = []
        self.dates = []
        self.money = []
        self.img_srcs = []
        self.searched_phrase_in_title = []
        self.searched_phrase_in_description = []

    def extract_info(self):
        try:
            self._open_the_website(self.URL)
            self._search_for(self.search_phrase)
            self._select_section(self.section)
            self._select_latest_news()
            time.sleep(0.5)
            self._show_more_info_if_necessary()
            self._extract_data()

            self._write_to_excel()
        finally:
            browser_lib.close_all_browsers()

    def _open_the_website(self, url: str) -> None:
        logging.info("Opening the website...")
        browser_lib.open_available_browser(url)

    def _search_for(self, term: str) -> None:
        logging.info("Entering phrase on search input field...")
        search_button = (
            '//*[@id="app"]/div[2]/div[2]/header/section[1]/div[1]/div[2]/button'
        )
        search_input = '//*[@id="app"]/div[2]/div[2]/header/section[1]/div[1]/div[2]/div/form/div/input'

        browser_lib.click_button(search_button)
        browser_lib.input_text(search_input, term)
        browser_lib.press_keys(search_input, "ENTER")

    def _select_section(self, section: str) -> None:
        logging.info("Selecting section...")
        section_button = (
            '//*[@id="site-content"]/div/div[1]/div[2]/div/div/div[2]/div/div/button'
        )
        browser_lib.click_button_when_visible(section_button)
        browser_lib.select_checkbox(f"//input[@type='checkbox'][starts-with(@value, '{section}')]")

    def _select_latest_news(self) -> None:
        logging.info("Selecting latest news...")
        newest_option = (
            '//*[@id="site-content"]/div/div[1]/div[1]/form/div[2]/div/select/option[2]'
        )
        browser_lib.click_element(newest_option)

    def _show_more_info_if_necessary(self) -> None:
        logging.info("Clicking on show more...")

        BASE_XPATH = '//*[@id="site-content"]/div/div[2]/div[1]/ol/li'
        len_elements = browser_lib.get_element_count(BASE_XPATH)


        current_last_month = browser_lib.get_text(
            f'{BASE_XPATH}[{len_elements}]/div/span').split('.')[0]
        end_month = self._get_month_name(datetime.now().month, self.months)

        while current_last_month != end_month:
            show_more_button = '//*[@id="site-content"]/div/div[2]/div[2]/div/button'
            browser_lib.click_button_when_visible(show_more_button)
            len_elements = browser_lib.get_element_count(BASE_XPATH)
            current_last_month = browser_lib.get_text(
                f'{BASE_XPATH}[{len_elements}]/div/span').split('.')[0]


    def _extract_data(self):
        logging.info("Extracting data...")
        BASE_XPATH = '//*[@id="site-content"]/div/div[2]/div[1]/ol/li'

        len_elements = browser_lib.get_element_count(BASE_XPATH)

        for i in tqdm(range(1, len_elements+1)):
            current_month_is_the_flag_month = self._check_current_month(
                i, BASE_XPATH)

            if current_month_is_the_flag_month:
                break
            try:
                current_title = browser_lib.get_text(
                    f'{BASE_XPATH}[{i}]/div/div/div/a/h4')
                current_date = browser_lib.get_text(
                    f'{BASE_XPATH}[{i}]/div/span')
                current_description = browser_lib.get_text(
                    f'{BASE_XPATH}[{i}]/div/div/div/a/p[1]')
                img_src = browser_lib.get_element_attribute(
                    f'{BASE_XPATH}[11]/div/div/figure/div/img', 'src')

                self.titles.append(current_title)
                self.dates.append(current_date)
                self.descriptions.append(current_description)
                self.searched_phrase_in_title.append(
                    current_title.lower().count(self.search_phrase.lower()))
                self.searched_phrase_in_description.append(
                    current_description.lower().count(self.search_phrase.lower()))
                self.img_srcs.append(img_src)

                if money_regex.search(current_title) \
                    or money_regex.search(current_description):
                    self.money.append(True)
                else:
                    self.money.append(False)
            except ElementNotFound:
                pass

    def _write_to_excel(self) -> None:
        logging.info("Writing to excel...")
        data = {
            "title": [title for title in self.titles],
            "description": [description for description in self.descriptions],
            "date": [date for date in self.dates],
            "has_money": [mon for mon in self.money],
            "phrase_in_title": [p for p in self.searched_phrase_in_title],
            "phrase_in_description": [p for p in self.searched_phrase_in_description],
            "picture_filename": [pic for pic in self.img_srcs]
        }

        df = pd.DataFrame(data)

        writer = pd.ExcelWriter("./output/file.xlsx", engine="openpyxl")
        df.to_excel(writer, index=False, sheet_name="Sheet1")
        writer.save()

    def _get_month_name(self, current_month:  int, months_back: int) -> str:
        if months_back == 0:
            months_back = 1

        result_month = current_month - months_back
        if result_month <= 0:
            result_month = result_month + 12

        return calendar.month_abbr[result_month]

    def _check_current_month(self, index: int, BASE_XPATH: str) -> bool:
        month_to_stop = self._get_month_name(datetime.now().month, self.months)

        try:
            current_month_iterating = browser_lib.get_text(
                f'{BASE_XPATH}[{index}]/div/span'
            ).split('.')[0]

            if current_month_iterating == month_to_stop:
                return True
        except ElementNotFound:     # This is for empty line items
            return False