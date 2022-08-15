#! /usr/bin/python3
import requests
from cookies import Cookies

# s = requests.Session()
# for cookie in cookies:
#    s.cookies.set(cookie['name'], cookie['value'])

data = {
   "p_calling_proc": "P_CrseSearch",
   "p_term": "202321",
}

headers = {'content-type': 'application/x-www-form-urlencoded'}

new_payload='term_in=202222&sel_subj=dummy&sel_subj=CIS&SEL_CRSE=D022A&SEL_TITLE=&BEGIN_HH=0&BEGIN_MI=0&BEGIN_AP=a&SEL_DAY=dummy&SEL_PTRM=dummy&END_HH=0&END_MI=0&END_AP=a&SEL_CAMP=dummy&SEL_SCHD=dummy&SEL_SESS=dummy&SEL_INSTR=dummy&SEL_INSTR=%25&SEL_ATTR=dummy&SEL_ATTR=%25&SEL_LEVL=dummy&SEL_LEVL=%25&SEL_INSM=dummy&sel_dunt_code=&sel_dunt_unit=&call_value_in=&rsts=dummy&crn=dummy&path=1&SUB_BTN=View%2BSections'

# with open("cookies.json", "r") as file:
#    cookies = json.load(file)

my_cookies = Cookies()
cookies = my_cookies.get_cookies("cookies/cookies.json")



s = requests.Session()
for cookie in cookies:
   s.cookies.set(cookie['name'], cookie['value'])

# response = s.post("https://ssb-prod.ec.fhda.edu/PROD/bwckgens.p_proc_term_date", data=data)
# print (response.text)
# print (s.cookies.get_dict())

url = "https://ssb-prod.ec.fhda.edu/PROD/bwskfcls.P_GetCrse"
response = s.post(url, data=new_payload, headers=headers)
print(response.status_code)
print(s.cookies.get_dict())



with open("database/archive/work.html", "w") as file:
   file.write(response.text)

