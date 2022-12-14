from optparse import OptionGroup
from credentials import username, password, PORTAL_URL
from xpaths import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(options=options)


class Scraper():
   """ This class is a helper class responsible for getting cookies """
   def __init__(self, close_window=True):
      self.close_window = close_window
      driver.maximize_window()
      driver.implicitly_wait(5)
   
   def __exit__(self, exc_type, exc_value, traceback):
      if self.close_window:
         driver.quit()

   def _land_page(self):
      driver.get(PORTAL_URL)

   def _login(self):
      user_input = driver.find_element(By.XPATH, user_xpath)
      password_input = driver.find_element(By.XPATH, password_xpath)
      user_input.send_keys(username)
      password_input.send_keys(password)
      submit_but = driver.find_element(By.XPATH, credentials_submit_xpath)
      submit_but.click()
      print("successfully login")

   # go to registration page to fetch cookies
   def _registration(self):
      print("accessing apps . . .")
      app_icon = driver.find_element(By.XPATH, register_icon_xpath)
      driver.execute_script("arguments[0].click();", app_icon)

      # search for classes
      class_schedule_link = driver.find_element(By.XPATH, class_schedule_xpath)
      class_schedule_link.click()
      driver.close()  # close myportal tab
      driver.switch_to.window(driver.window_handles[0])

      select_fall2022 = driver.find_element(By.XPATH, fall2022_xpath)
      select_fall2022.click()

      submit_but = driver.find_element(By.XPATH, terms_submit_xpath)
      submit_but.click()

   def _click_on_class(self):
      driver.find_element(By.XPATH, sample_class_xpath).click()
      driver.find_element(By.XPATH, course_search_xpath).click()
      driver.find_element(By.XPATH, '/html/body/div[3]/table[2]/tbody/tr[3]/td[3]/form/input[30]').click()

   def _fetch_cookies(self):
      return driver.get_cookies()
   
   def fetch_cookies(self):
      self._land_page()
      self._login()
      self._registration()
      self._click_on_class()
      return self._fetch_cookies()
      