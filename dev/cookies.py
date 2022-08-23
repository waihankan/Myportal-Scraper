import json


class Cookies():
   """
      Cookies that will handle handshake with the server 
      and save the new cookies to the file **kwargs handles the cookies set
      or get type
   """
   def __init__(self, **kwargs):
      self.cookies = kwargs.get('cookies', [])

   def save_new_cookies(self, filename):
      with open(filename, "w") as file:
         json.dump(self.cookies, file)

   def get_cookies(self, filename):
      with open(filename, "r") as file:
         cookies = json.load(file)
         return cookies

   def handle_cookies_handshake(self, filename, new_sess_id):
      with open(filename, "r") as file:
         cookies = json.load(file)
         for cookie in cookies:
            if cookie['name'] == "SESSID":
               cookie['value'] = new_sess_id
      self.save_cookies(filename)
