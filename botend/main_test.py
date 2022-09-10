#!/usr/bin/python3

import discord
import regex as re
from credentials import DISCORD_TOKEN
from digger import Digger
from prettytable import PrettyTable


intents = discord.Intents.default()
intents.message_content = True
intents.members = True
client = discord.Client(intents=intents)
DATABASE_FILEPATH = "./database/test2.db"
bot = Digger(DATABASE_FILEPATH)


def course_parser(crse):
   """ Parse the course string into subject and course number """
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

def term_parser(term):
   code = ""
   term = re.split(r'(\d+)', term)
   quarter = term[0].lower()
   year = f"20{term[1]}"
   if quarter == "winter":
      code = f"{year}32"
   elif quarter == "spring":
      code = f"{year}42"
   elif quarter == "summer":
      code = f"{int(year) + 1}12"
   elif quarter == "fall":
      code = f"{int(year) + 1}22"
   else:
      exit("Invalid term")
   return code


@client.event
async def on_ready():
    print(f'{client.user} is connected to the following guild:\n')

@client.event
async def on_message(message):
   if message.author == client.user:
      return

   elif message.content.lower().startswith("!help"):
      embed = discord.Embed(
         title="I am -- a bot for De Anza College course information",
         url = "https://i.imgur.com/wmDr0DU.png",
         description="Some Commands I can do:",
         color=discord.Color.blue()
      )
      embed.set_author(name="Just Wanna Graduate", url="https://i.imgur.com/wmDr0DU.png", icon_url="https://i.imgur.com/wmDr0DU.png")
      embed.set_thumbnail(url="https://i.imgur.com/wmDr0DU.png")
      embed.add_field(name="**!help**", value="Display This Help Message", inline=False)
      embed.add_field(name="**Professor Information**", value="`!whois prof_name`", inline=False)
      embed.add_field(name="**Easiest Professor (According to the grade distribution)**", value="`!easy --CIS --22C`", inline=False)
      embed.add_field(name="**Waitlist Information**", value="`!waitlist --prof --MATH --1A`", inline=False)
      embed.add_field(name="**Grade Distribution**", value="`!grades --prof_name --ACCT`\n`!grades --prof_name --PHIL --8`", inline=False)
      embed.add_field(name="**Check Class Schedule**", value="`!find --winter22 --CIS`\n`!find --spring22 --ACCT --1A`\n`!find --fall22 --{CRN}`", inline=False)
      embed.set_footer(text="💭 Please contact if you want to volunteer to help me improve!")
      await message.channel.send(embed=embed)

   elif message.content.lower().startswith("!whois"):
      """ !whois professor_name"""
      args = message.content.lower().split("--")
      prof = re.sub(r'!whois ', '', args[0])
      prof = re.sub(" +", ' ', prof)
      prof = prof.strip()
      response = bot.who_is(prof)
      if response:
         embed = discord.Embed(
            title = f"Professor Information",
            url = "https://www.deanza.edu/directory/",
            color = discord.Color.blue()
         )
         for data in response:
            embed.add_field(name = f"{data[0]}  (Department: {data[1]})", value = f"Email: {data[2]}\n Phone: {data[3]}", inline = False)
         embed.set_footer(text = 
         """💡 !grades --prof_name --subject --course_number  ->  grade distribution for a specific course\n💡 !grades --prof_name  ->  general grade distribution of the professor
         """)

      else:
         embed = discord.Embed(
            title = f"No Results Found",
            description="Please use: `!whois first_name last_name` or `!whois last_name` or `!whois first_name`",
            color=discord.Color.blue()
         )
         embed.add_field(name="Examples:", value="➡ **!whois Delia Garbacea**\n➡ **!whois Usha**", inline=True)
         embed.set_footer(text="Thank you for using me 😀")
      await message.channel.send(embed=embed)

   elif message.content.lower().startswith("!grades"):
      """ !grades --prof_first_and_last_name """
      args = message.content.lower().split("--")
      if len(args) == 2:
         """ !grades --professor"""
         prof = args[1].strip()
         response = bot.prof_grade_info(prof)
         if response:
            table = PrettyTable()
            table.field_names = ["Year", "Semester", "Professor", "Subject", "Course", "A", "B", "C", "D", "F", "W"]
            for data in response:
               table.add_row(data)
            await message.channel.send(f"```{table}```\n💡 *Use* `!whois first_name last_name` *to get the professor's email and phone number*")
         else:
            embed = discord.Embed(
            title = "No Results Found",
            description="Please use: `!grades --prof_name --subject --course_number` or `!grades --prof_name`",
            color=discord.Color.blue()
            )
            embed.add_field(name="Examples:", value="➡ **!grades --delia --CIS --22A**\n➡ **!grades --delia**", inline=True)
            embed.set_footer(text="Thank you for using me 😀")
            await message.channel.send(embed = embed)

      elif len(args) == 4:
         """ !grades --prof_first_and_last_name --subject --course_number """
         prof = args[1].strip()
         subj = args[2].strip()
         crse = args[3].strip()
         crse = course_parser(crse)
         response = bot.prof_grade_info(prof, subj, crse)
         if response:
            table = PrettyTable()
            table.field_names = ["Year", "Semester", "Professor", "Subject", "Course", "A", "B", "C", "D", "F", "W"]
            for data in response:
               table.add_row(data)
            await message.channel.send(f"```{table}```\n💡 *Use* `!whois first_name last_name` *to get the professor's email and phone number*")
         else:
            embed = discord.Embed(
            title = "No Results Found",
            description="Please use: `!grades --prof_name --subject --course_number` or `!grades --prof_name`",
            color=discord.Color.blue()
            )
            embed.add_field(name="Examples:", value="➡ **!grades --delia --CIS --22A**\n➡ **!grades --delia**", inline=True)
            embed.set_footer(text="Thank you for using me 😀")
            await message.channel.send(embed = embed)
      else:
         embed = discord.Embed(
         title = "Invalid Command",
         description="Please use: `!grades --prof_name --subject --course_number` or `!grades --prof_name`",
         color=discord.Color.blue()
         )
         embed.add_field(name="Examples:", value="➡ **!grades --delia --CIS --22A**\n➡ **!grades --delia**", inline=True)
         embed.set_footer(text="Thank you for using me 😀")
         await message.channel.send(embed = embed)
      
   elif message.content.lower().startswith("!easy"):
      """ !easy --subject --course_number """

      args = message.content.lower().split("--")
      if len(args) == 3:
         subj = args[1].strip()
         crse = args[2].strip()
         crse = course_parser(crse)
         response = bot.prof_grade_info(subj, crse)  # find most A professor for a course (Easiest A)
         if response:
            table = PrettyTable()
            table.field_names = ["Year", "Semester", "Professor", "Subject", "Course", "A", "B", "C", "D", "F", "W"]
            for data in response:
               table.add_row(data)
            await message.channel.send(f"""
            ```{table}```\n💡 *Use* `!grades prof_name --subject --course_number` *to see grade distribution for a specific course*\n💡 *Use* `!grades prof_name` *for general grade distribution of the professor*
            """)
         else:
            embed = discord.Embed(
               title = f"No Results Found",
               description="Please make sure the course name and the course number are correct",
               color=discord.Color.blue()
            )
            embed.add_field(name="Examples:", value="➡ **!easy --CIS --22A**\n➡ **!easy --ACCT --1A**", inline=True)
            embed.set_footer(text="Thank you for using me 😀")
            await message.channel.send(embed = embed)

      else:
         embed = discord.Embed(
         title = "Invalid Command",
         description="Please use: `!easy --subject --course_number`",
         color=discord.Color.blue()
         )
         embed.add_field(name="Examples:", value="➡ **!easy --CIS --22A**\n➡ **!easy --ACCT --1A**", inline=True)
         embed.set_footer(text="Thank you for using me 😀")
         await message.channel.send(embed = embed)

   elif message.content.lower().startswith("!find"):
      """ 
         !find --term --subject
         !find --term --subject --course_number
         !find --term --crn
      """
      args = message.content.lower().split("--")
      if len(args) == 3:
         term = term_parser(args[1].strip())
         if args[2].isdigit() and len(args[2]) == 5:
            """ !find --term --crn """
            crn = args[2].strip()
            response = bot.search_by_crn(term=term, crn=crn)
            if response:
               table = PrettyTable()
               table.field_names = ["CRN", "Subject", "Course", "Rem", "WLRem", "Instructor", "Days", "Time"]
               for data in response:
                  table.add_row(data)
               await message.channel.send(f"```{table}```")
            else:
               embed = discord.Embed(
                  title = f"No Results Found",
                  description="Please make sure the CRN is correct",
                  color=discord.Color.blue()
               )
               embed.add_field(name="Examples:", value="➡ **!find --summer22**\n➡ **!find --2020 --CIS --22A**", inline=True)
               embed.set_footer(text="Thank you for using me 😀")
               await message.channel.send(embed = embed)


         elif args[2].isalpha():
            """ !find --term --subject """
            subj = args[2].strip()
            response = bot.search_by_term_subj(term=term, subj=subj)
            if response:
               table = PrettyTable()
               table.field_names = ["CRN", "Subject", "Course", "Rem", "WLRem", "Instructor", "Days", "Time"]
               for index, data in enumerate(response):
                  table.add_row(data)
                  if index % 15 == 0 and index != 0 or index == len(response) - 1:
                     await message.channel.send(f"```{table}```")
                     table.clear_rows()   
            else:
               embed = discord.Embed(
                  title = f"No Results Found",
                  description="Please use `!find --term --subject` or `!find --term --subject --course_number` or `!find --term --crn`",
                  color=discord.Color.blue()
               )
               embed.add_field(name="Examples:", value="➡ **!find --summer22 --cis --22C**\n➡ **!find --winter22 --CIS --22A**", inline=True)
               embed.set_footer(text="Thank you for using me 😀")
               await message.channel.send(embed = embed)

         else:
            embed = discord.Embed(
               title = f"No Results Found",
               description="Please make sure the CRN is correct",
               color=discord.Color.blue()
            )
            embed.add_field(name="Examples:", value="➡ **!find --summer22**\n➡ **!find --2020 --CIS --22A**", inline=True)
            embed.set_footer(text="Thank you for using me 😀")
            await message.channel.send(embed = embed)

     
      elif len(args) == 4:
         """ !find --term --subject --course_number """

         term = term_parser(args[1].strip())
         subj = args[2].strip()
         crse = course_parser(args[3].strip())
         response = bot.search_by_term_subj_crse(term=term, subj=subj, crse=crse)
         if response:
            table = PrettyTable()
            table.field_names = ["CRN", "Subject", "Course", "Rem", "WLRem", "Instructor", "Days", "Time"]
            for index, data in enumerate(response):
               table.add_row(data)
               if index % 15 == 0 and index != 0 or index == len(response) - 1:
                  await message.channel.send(f"```{table}```")
                  table.clear_rows()   
         else:
            embed = discord.Embed(
               title = f"No Results Found",
               description="Please use `!find --term --subject` or `!find --term --subject --course_number` or `!find --term --crn`",
               color=discord.Color.blue()
            )
            embed.add_field(name="Examples:", value="➡ **!find --summer22 --cis --22C**\n➡ **!find --winter22 --CIS --22A**", inline=True)
            embed.set_footer(text="Thank you for using me 😀")
            await message.channel.send(embed = embed)


      else:
         embed = discord.Embed(
            title = f"Invalid Command",
            description="Please use `!find --term --subject` or `!find --term --subject --course_number` or `!find --term --crn`",
            color=discord.Color.blue()
         )
         embed.add_field(name="Examples:", value="➡ **!find --summer22 --00000**\n➡ **!find --winter20 --CIS**\n➡**!find --fall22 --CIS --22C**", inline=True)
         embed.set_footer(text="Thank you for using me 😀")
         await message.channel.send(embed = embed)

   elif message.content.lower().startswith("!waitlist"):
      args = message.content.lower().split("--")
      response = []
      if len(args) == 3:
         """ !waitlist --professor --subject """
         prof = args[1].strip()
         subj = args[2].strip()
         response = bot.waitlist_viewer_prof(prof, subj)
      elif len(args) == 4:
         """ !waitlist --professor --subject --course_number """
         prof = args[1].strip()
         subj = args[2].strip()
         crse = course_parser(args[3].strip())
         response = bot.waitlist_viewer_crse(instructor=prof, subj=subj, crse=crse)
      else:
         embed = discord.Embed(
            title = f"Invalid Command",
            description="Please use `!waitlist --professor --subject --course_number`",
            color=discord.Color.blue()
         )
         embed.add_field(name="Examples:", value="➡ **!waitlist --Oldham --CIS --22B**", inline=True)
         embed.set_footer(text="Thank you for using me 😀")
         await message.channel.send(embed = embed)

      if response:
         table = PrettyTable()
         table.field_names = ["Terms", "Subject", "Course", "Act", "Rem", "WLRem", "Instructor", "Location"]
         for data in response:
            table.add_row(data)
         await message.channel.send(f"```{table}\n💡 Negative numbers under 'Rem' represents the number of accepted Waitlisted students.```")

      else:
         embed = discord.Embed(
            title = f"No Results Found",
            description="Please use `!waitlist --professor --subject --course_number`",
            color=discord.Color.blue()
         )
         embed.add_field(name="Examples:", value="➡ **!waitlist --Delia --CIS --22A**", inline=True)
         embed.set_footer(text="Thank you for using me 😀")
         await message.channel.send(embed = embed)

client.run(DISCORD_TOKEN)
