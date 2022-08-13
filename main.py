#!/usr/bin/python3
from sel_scrape import Scraper

# def main():
with Scraper(close_window=True) as bot:
   bot.land_page()
   bot.login()
   bot.registration()
   bot.print_cookies()





# if __name__ == '__main__':
#    main()