#!/usr/bin/python3
from sel_scrape import Scraper
from cookies import Cookies

def main():
   fetched_cookies = Cookies(cookies = Scraper().fetch_cookies())
   fetched_cookies.save_new_cookies("cookies/cookies.json")
   
if __name__ == '__main__':
   main()