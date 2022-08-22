#!/usr/bin/python3
from sel_scrape import Scraper
from cookies import Cookies
from fetch_data import FetchDataRequests
import time


with Scraper(close_window=True) as bot:
   bot.land_page()
   bot.login()
   bot.registration()
   bot.click_on_class()
   my_cookies = Cookies(cookies = bot.fetch_cookies())
   my_cookies.save_new_cookies("cookies/cookies.json")

terms = ["202322", "202312",
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

for term in terms:
   print(f"Fetching data for term {term}")
   fetcher = FetchDataRequests(term)
   fetcher.fetch_data()
   print(fetcher.get_status_code())
   fetcher.save_data()
   print("Sleeping for 20 seconds . . . . . \n\n")
   time.sleep(20)

# if __name__ == '__main__':
#    main()