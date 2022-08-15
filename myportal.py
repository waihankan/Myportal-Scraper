from selenium import webdriver
import requests
import json


# def get_cookies():
#     cookies = {}
#     selenium_cookies = driver.get_cookies()
#     for cookie in selenium_cookies:
#         cookies[cookie['name']] = cookie['value']
#     return cookies
   
# def get_posts():
#    cookies = get_cookies()
#    response = requests.get("https://myportal.fhda.edu", cookies=cookies)
#    # time.sleep(5)
#    return response.text

driver = webdriver.Chrome()
driver.maximize_window()
url = "https://myportal.fhda.edu"
driver.get(url)
# time.sleep(3)

campus_id = driver.find_element_by_id("username")
password = driver.find_element_by_id("password")
submit = driver.find_element_by_id("btn-eventId-proceed")


driver.implicitly_wait(6)
campus_id.send_keys("20504061")
password.send_keys("waihankan")
submit.click()

# reg = driver.find_element_by_css_selector(
#    'div[data-content-id="app.studentreg"]'
# )

search = driver.find_element_by_class_name("form-control")
search.send_keys("student registration")

go_button = driver.find_element_by_css_selector('button[type="button"]')
go_button.click()

reg = driver.find_element_by_css_selector('div[data-content-id="app.studentreg"]')
label = reg.find_element_by_class_name("myapps-item-label")
label.click()


container = driver.find_elements_by_class_name("mb-2")
for item in container:
   link = item.find_element_by_tag_name("a")
   if (str(link.get_attribute("innerHTML")).strip() == "Searchable Schedule of Classes"):
      link.click()

# reg = driver.find_element_by_class_name("myapps-appicon-studentreg")
# reg.click()
driver.switch_to.window(driver.window_handles[1])
selection = driver.find_element_by_css_selector('select[name="p_term"]')
fall_2022 = selection.find_element_by_css_selector('option[value="202322"]')
fall_2022.click()
submit = driver.find_element_by_xpath("/html/body/div[3]/form/input[2]")
submit.click()






cookies = driver.get_cookies()
# print request cookies
print(json.dumps(cookies, indent =4))
print("\n")
s = requests.Session()
for cookie in cookies:
    s.cookies.set(cookie['name'], cookie['value'])

data = {
   "p_calling_proc": "P_CrseSearch",
   "p_term": "202322"
}

response = s.post("https://ssb-prod.ec.fhda.edu/PROD/bwckgens.p_proc_term_date", data=data)
# print (response.text)

print("Response Cookies")
print(response.cookies.get_dict())


with open ("index.html", "w") as file:
   file.write(response.text)



