#!/usr/bin/python3
from sel_scrape import Scraper
from cookies import Cookies
from fetch_data import FetchDataRequests
import time

# def main():
with Scraper(close_window=True) as bot:
   bot.land_page()
   bot.login()
   bot.registration()
   bot.click_on_class()
   my_cookies = Cookies(cookies = bot.fetch_cookies())
   my_cookies.save_new_cookies("cookies/cookies.json")
   

# if __name__ == '__main__':
#    main()