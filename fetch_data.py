'''
   Send Post request to the server and fetch the data using cookies received from
   sel_scrape.py
'''
import requests
from cookies import Cookies


class FetchDataRequests():
   def __init__(self, term):
      self.filepath = f"database/html_archive/{term}.html"
      self.url = "https://ssb-prod.ec.fhda.edu/PROD/bwskfcls.P_GetCrse"
      self.headers = {"content-type": "application/x-www-form-urlencoded"}
      self.payload = f"term_in={term}&sel_subj=dummy&sel_subj=%25&SEL_CRSE=%25&SEL_TITLE=&BEGIN_HH=0&BEGIN_MI=0&BEGIN_AP=a&SEL_DAY=dummy&SEL_PTRM=dummy&END_HH=0&END_MI=0&END_AP=a&SEL_CAMP=dummy&SEL_SCHD=dummy&SEL_SESS=dummy&SEL_INSTR=dummy&SEL_INSTR=%25&SEL_ATTR=dummy&SEL_ATTR=%25&SEL_LEVL=dummy&SEL_LEVL=%25&SEL_INSM=dummy&sel_dunt_code=&sel_dunt_unit=&call_value_in=&rsts=dummy&crn=dummy&path=1&SUB_BTN=View%2BSections"
      self.status_code = None
      self.data = ""

   def fetch_data(self):
      my_cookies = Cookies()
      cookies = my_cookies.get_cookies("cookies/cookies.json")
      s = requests.Session()
      # Set the cookies fetched from the Selenium script
      for cookie in cookies:
         s.cookies.set(cookie['name'], cookie['value'])
      
      response = s.post(self.url, data=self.payload, headers=self.headers)
      self.status_code = response.status_code
      self.data = response.text

   def get_status_code(self):
      return self.status_code

   def get_data(self):
      return self.data

   def save_data(self):
      if self.status_code == 200:
         with open(self.filepath, "w") as file:
            file.write(self.data)
      else:
         print("Error: status code is not 200")
