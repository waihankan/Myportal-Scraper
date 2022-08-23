'''
   Send POST request to the server and fetch the data using cookies received from
   sel_scrape.py
'''

from cookies import Cookies
from sel_scrape import Scraper
import requests
import time

# Change Database filepath here
HTML_FILEPATH = "./database/html_archive/"

class FetchDataRequests():
   def __init__(self, sleeptime=10):
      self.fetched_cookies = Cookies(cookies = Scraper().fetch_cookies())
      self.fetched_cookies.save_new_cookies("cookies/cookies.json")
      self.filepath = ""
      self.url = "https://ssb-prod.ec.fhda.edu/PROD/bwskfcls.P_GetCrse"
      self.headers = {"content-type": "application/x-www-form-urlencoded"}
      self.payload = ""
      self.status_code = None
      self.data = ""
      self.sleeptime = sleeptime
      self.terms = [
         "202322", "202312",
         "202242", "202232", "202222", "202212",
         "202142", "202132", "202122", "202112",
         "202042", "202032", "202022", "202012",
         "201942", "201932", "201922", "201912",
         "201842", "201832", "201822", "201812",
         "201742", "201732", "201722", "201712",
         "201642", "201632", "201622", "201612",
         "201542", "201532", "201522", "201512",
         "201442", "201432", "201422", "201412",
         "201342", "201332", "201322", "201312",
         "201242", "201232", "201222", "201212",
         "201142", "201132", "201122", "201112",
      ]

   def _update_payload(self, term):
      self.payload = f"term_in={term}&sel_subj=dummy&sel_subj=%25&SEL_CRSE=%25&SEL_TITLE=&BEGIN_HH=0&BEGIN_MI=0&BEGIN_AP=a&SEL_DAY=dummy&SEL_PTRM=dummy&END_HH=0&END_MI=0&END_AP=a&SEL_CAMP=dummy&SEL_SCHD=dummy&SEL_SESS=dummy&SEL_INSTR=dummy&SEL_INSTR=%25&SEL_ATTR=dummy&SEL_ATTR=%25&SEL_LEVL=dummy&SEL_LEVL=%25&SEL_INSM=dummy&sel_dunt_code=&sel_dunt_unit=&call_value_in=&rsts=dummy&crn=dummy&path=1&SUB_BTN=View%2BSections"
   
   def _update_filepath(self, term):
      self.filepath = f"{HTML_FILEPATH}{term}.html"

   def _get_data(self):
      return self.data

   def _fetch_data(self, term):
      my_cookies = Cookies()
      cookies = my_cookies.get_cookies("cookies/cookies.json")
      self._update_payload(term)
      s = requests.Session()
      # Set the cookies fetched from the Selenium script
      for cookie in cookies:
         s.cookies.set(cookie['name'], cookie['value'])
      
      response = s.post(self.url, data=self.payload, headers=self.headers)
      self.status_code = response.status_code
      self.data = response.text

   def _save_data(self, term):
      if self.status_code == 200:
         self._update_filepath(term)
         with open(self.filepath, "w") as file:
            file.write(self.data)
      else:
         print("Error: status code is not 200")
         
   def archive_one_term(self, term):
         self._fetch_data(term)
         self._save_data(term)
         print(f"Saved data for term {term} | Status code: {self.status_code} | Sleeptime: {self.sleeptime} seconds")
         time.sleep(self.sleeptime)

   def archive_all_past_terms(self):
      for term in self.terms:
         self.archive_one_term(term)
