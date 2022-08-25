import re
from digger import Digger

DATABASE_FILEPATH = "./database/test2.db"

def main():
   digger = Digger(DATABASE_FILEPATH)
   instructor = input("Enter instructor name: ")
   subj = input("Enter subject: ")
   crse = input("Enter course number: ")
   results = digger.waitlist_viewer(instructor, subj, crse)
   for result in results:
      print(result)

def test():
   digger = Digger(DATABASE_FILEPATH)
   term = input("Enter term: ")
   subj = input("Enter subject: ")
   crse = input("Enter course number: ")
   results = digger.schedule_finder(term, subj, crse)
   # crn = input("Enter CRN: ")
   # results = digger.search_by_crn(term, crn)
   for result in results:
      print(result)

def test_term():
   digger  = Digger(DATABASE_FILEPATH)
   term = input("Enter term: ")
   result = digger.term_parser(term)
   print(result)

def test_course_parser():
   digger = Digger(DATABASE_FILEPATH)
   course = input("Enter course: ")
   result = digger.course_parser(course)
   print(result)

def test_course_parser(original_function):
   def wrapper(*args, **kwargs):
      print("Input validation test")
      print("Input: ", args[0], args[1])
      return original_function(*args, **kwargs)
   return wrapper

@test_course_parser
def course_parser(crse):
   if(len(crse) > 5):
      return "Invalid course number"

   elif(len(crse) == 5):
      return crse

   elif(len(crse) < 5):
      if(len(crse) == 1):
         return f"D00{crse}."
      elif(len(crse) == 2 and not crse.isdigit()):
         return f"D00{crse}"
      elif(len(crse) == 2 and crse.isdigit()):
         return f"D0{crse}."
      elif(len(crse) == 3 and not crse.isdigit()):
         return f"D0{crse}"
      elif(len(crse) == 3 and crse.isdigit()):
         return f"D{crse}."
      elif(len(crse) == 4):
         return f"D{crse}"





if __name__ == "__main__":
   # print(course_parser("22c", "22b"))
   print(Digger(DATABASE_FILEPATH).waitlist_viewer("", "EWRT", "D002."))