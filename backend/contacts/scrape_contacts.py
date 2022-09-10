#!/usr/bin/python
import requests
import pandas as pd
import sqlite3 as sql

# Global variables
HTML_FILEPATH = "./database/contacts_html_archive/contacts.html"
DATABASE_FILEPATH = "./database/main_database.db"

# Create the database connection
conn = sql.connect(DATABASE_FILEPATH)
cur = conn.cursor()

def scrape_contacts():
      # Get the contacts from the website
      URL = "https://www.deanza.edu/directory/"
      response = requests.get(URL)
      with open(HTML_FILEPATH, "w") as f:
         f.write(response.text)

def extract_contacts():
      # Read the contacts from the file with pandas table
      df = pd.read_html(HTML_FILEPATH)
      return df[0]


def insert_phone_number(name, phone):
   cur.execute(
   """
      UPDATE deanza_instructors
      SET Phone_Number = ?
      WHERE Name = ?
   """, (phone, name))
   conn.commit()


def insert_contacts():
   df = extract_contacts()
   for row in df.itertuples():
      insert_phone_number(getattr(row, "Name"), getattr(row, "Phone"))

if __name__ == "__main__":
   # scrape_contacts()   # Uncomment this line to scrape the contacts from the website
   insert_contacts()   # Uncomment this line to insert the contacts into the database
