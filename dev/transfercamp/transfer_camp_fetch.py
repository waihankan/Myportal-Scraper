import requests

terms = ["2015", "2016", "2017", "2018", "2019"]



def _save_data(term, data):
   with open(f"./database/transfer_html_archive/{str(term)}.html", "w") as f:
      f.write(data)

for term in terms:
   url = f"https://transfercamp.com/de-anza-college-grade-distribution-{term}-{int(term)+1}/"
   response = requests.get(url)
   _save_data(term, response.text)
   print(f"Saved {term} data")
