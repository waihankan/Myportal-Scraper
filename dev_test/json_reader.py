import json
import os
cwd = os.getcwd()
# print(os.listdir(cwd))



# working read json file
f = open("cookies.json")
cookies = json.load(f)
for cookie in cookies:
   print(cookie)
   print("\n")

f.close()
for cookie in cookies:
   if cookie['name'] == "SESSID":
      cookie['value'] = "changed cookie session"

with open("read.json", "w") as file:
   json.dump(cookies, file)