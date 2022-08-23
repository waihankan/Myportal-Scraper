import sys
sys.path.insert(0, "/home/selenium/")
import credentials
from credentials import username, password, PORTAL_URL
from xpaths import *
from selenium import webdriver
from selenium.webdriver.common.by import By


class Scraper(webdriver.Chrome):
   """ This class is a helper class responsible for getting cookies """
   def __init__(self, close_window=True):
      super(Scraper, self).__init__()
      self.close_window = close_window
      self.maximize_window()
      self.implicitly_wait(5)
   
   def __exit__(self, exc_type, exc_value, traceback):
      if self.close_window:
         self.quit()

   def _land_page(self):
      self.get(PORTAL_URL)

   def _login(self):
      # print(f"username = {username}")
      # print(f"password = {password}")
      user_input = self.find_element(By.XPATH, user_xpath)
      password_input = self.find_element(By.XPATH, password_xpath)
      user_input.send_keys(username)
      password_input.send_keys(password)
      submit_but = self.find_element(By.XPATH, credentials_submit_xpath)
      submit_but.click()
      print("successfully login")

   # go to registration page to fetch cookies
   def _registration(self):
      print("accessing apps . . .")
      app_icon = self.find_element(By.XPATH, register_icon_xpath)
      self.execute_script("arguments[0].click();", app_icon)

      # search for classes
      class_schedule_link = self.find_element(By.XPATH, class_schedule_xpath)
      class_schedule_link.click()
      self.close()  # close myportal tab
      self.switch_to.window(self.window_handles[0])

      select_fall2022 = self.find_element(By.XPATH, fall2022_xpath)
      select_fall2022.click()

      submit_but = self.find_element(By.XPATH, terms_submit_xpath)
      submit_but.click()

   def _click_on_class(self):
      self.find_element(By.XPATH, sample_class_xpath).click()
      self.find_element(By.XPATH, course_search_xpath).click()
      self.find_element(By.XPATH, '/html/body/div[3]/table[2]/tbody/tr[3]/td[3]/form/input[30]').click()

   def _fetch_cookies(self):
      return self.get_cookies()
   
   def fetch_cookies(self):
      self._land_page()
      self._login()
      self._registration()
      self._click_on_class()
      return self._fetch_cookies()
      