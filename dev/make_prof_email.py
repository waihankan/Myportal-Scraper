import regex as re

prof_list = [
   "Ann C. Lee-Yen",
   "Fatemeh S. Zarghami",
   "Sherwood Harrington",
   "Mia A. Breen",
   "Stephen J. Hurst",
   "Terrance Brown",
   "Michael M. Gough",
   "Lakshmamma Venkata",
   "Theodore C. Ellis",
   "Chris C. Kwak",
   "Lydia R. Botsford",
   "Lauri B. Hammond",
   "Jacquelyn R. McClure",
   "Meghan C. Kensler",
   "Terry R. Ellis",
   "Mallory K. Lawlor",
   "Eugene N. Lindenbaum",
   "Isaiah O. Nengo"
]


def email_generator(full_name_with_middle_initial):
      full_name = re.sub(r"\s\w*.\s", " ", full_name_with_middle_initial)
      first_name = full_name.split()[0]
      last_name = full_name.split()[1]
      first_email_name = re.sub(r"-", "", first_name).lower()
      last_email_name = re.sub(r"-", "", last_name).lower()
      print(f"Email: {last_email_name}{first_email_name}@deanza.edu")


if __name__ == "__main__":
   for prof in prof_list:
      email_generator(prof)