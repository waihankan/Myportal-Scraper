import json
import requests


# s = requests.Session()
# for cookie in cookies:
#    s.cookies.set(cookie['name'], cookie['value'])

data = {
   "p_calling_proc": "P_CrseSearch",
   "p_term": "202321",
}

my_payload = {
   "term_in": "202322", 
   "sel_subj": "dummy",
   "sel_subj": "AFAM",
   "SEL_CRSE": "D010.", 
   "SEL_TITLE": "",
   "BEGIN_HH": "0",
   "BEGIN_MI": "0",
   "BEGIN_AP": "a",
   "SEL_DAY": "dummy",
   "SEL_PTRM": "dummy",
   "END_HH": "0",
   "END_MI": "0",
   "END_AP": "a",
   "SEL_CAMP": "dummy",
   "SEL_SCHD": "dummy",
   "SEL_SESS": "dummy",
   "SEL_INSTR": "dummy",
   "SEL_INSTR": "%",
   "SEL_ATTR": "dummy",
   "SEL_ATTR": "%",
   "SEL_LEVL": "dummy",
   "SEL_LEVL": "%",
   "SEL_INSM": "dummy",
   "sel_dunt_code": "",
   "sel_dunt_unit": "",
   "call_value_in": "",
   "rsts": "dummy",
   "crn": "dummy",
   "path": "1",
   "SUB_BTN": "View Sections",
}


unused_payload = {
   "rsts": "dummy",
   "crn": "dummy",
   "term_in": "202322",
   "sel_subj": "dummy",
   "sel_day": "dummy",
   "sel_schd": "dummy",
   "sel_insm": "dummy",
   "sel_camp": "dummy",
   "sel_levl": "dummy",
   "sel_sess": "dummy",
   "sel_instr": "dummy",
   "sel_ptrm": "dummy",
   "sel_attr": "dummy",
   "sel_subj": "ANTH",
   "sel_crse": "D001A",
   "sel_title": "",
   "sel_from_cred": "",
   "sel_to_cred": "",
   "sel_ptrm": "%",
   "begin_hh": "0",
   "begin_mi": "0",
   "end_hh": "0",
   "end_mi": "0",
   "begin_ap": "a",
   "end_ap": "a",
   "path": "1",
   "SUB_BTN": "View Sections"
}

new_payload='term_in=202322&sel_subj=dummy&sel_subj=ACCT&SEL_CRSE=D001A&SEL_TITLE=&BEGIN_HH=0&BEGIN_MI=0&BEGIN_AP=a&SEL_DAY=dummy&SEL_PTRM=dummy&END_HH=0&END_MI=0&END_AP=a&SEL_CAMP=dummy&SEL_SCHD=dummy&SEL_SESS=dummy&SEL_INSTR=dummy&SEL_INSTR=%25&SEL_ATTR=dummy&SEL_ATTR=%25&SEL_LEVL=dummy&SEL_LEVL=%25&SEL_INSM=dummy&sel_dunt_code=&sel_dunt_unit=&call_value_in=&rsts=dummy&crn=dummy&path=1&SUB_BTN=View%2BSections'
with open("cookies.json", "r") as file:
   cookies = json.load(file)

print (cookies)

headers = {'content-type': 'application/x-www-form-urlencoded', 'content-length': '398'}

s = requests.Session()
for cookie in cookies:
   s.cookies.set(cookie['name'], cookie['value'])

# response = s.post("https://ssb-prod.ec.fhda.edu/PROD/bwckgens.p_proc_term_date", data=data)
# print (response.text)
# print (s.cookies.get_dict())

url = "https://ssb-prod.ec.fhda.edu/PROD/bwskfcls.P_GetCrse"
response = s.post(url, data=new_payload, headers=headers)
# print(response.text)
print(response.status_code)



with open("requests.html", "w") as file:
   file.write(response.text)

