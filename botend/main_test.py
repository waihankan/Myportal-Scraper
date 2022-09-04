#!/usr/bin/python

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
         

@client.event
async def on_ready():
    print(
        f'{client.user} is connected to the following guild:\n'
    )

@client.event
async def on_message(message):
   if message.author == client.user:
      return

   elif message.content.lower().startswith("!helpbro"):
      embed = discord.Embed(
         title="Help Me Bro Commands",
         url = "https://i.imgur.com/wmDr0DU.png",
         description="List of commands for Help Me Bro",
         color=discord.Color.blue()
      )
      embed.set_author(name="Help Me Bro", url="https://i.imgur.com/wmDr0DU.png", icon_url="https://i.imgur.com/wmDr0DU.png")
      embed.set_thumbnail(url="https://i.imgur.com/wmDr0DU.png")
      embed.add_field(name="**!helpbro**", value="Display this help message", inline=False)
      embed.add_field(name="**!who**", value="`!whois <first and last name>`", inline=False)
      embed.add_field(name="**!grades**", value="`!dis_grade <instructor> <subj> <output_lines (optional)>`", inline=False)
      embed.add_field(name="**!grades**", value="`!dis_grade <instructor> <subj> <crse> <output_lines (optional)>`", inline=False)
      embed.add_field(name="**sch_find**", value="`!sch_find <term> <subj>`", inline=False)
      embed.add_field(name="**sch_find**", value="`!sch_find <term> <subj> <crse>`", inline=False)
      embed.set_footer(text="You can give me feedback by clicking on the link above")
      await message.channel.send(embed=embed)

   elif message.content.lower().startswith("!whois"):
      # !whois <instructor_name>
      # extract instructor name from message
      args = message.content.lower().split(";")
      prof = re.sub(r'!whois ', '', args[0])
      prof = re.sub(" +", ' ', prof)
      prof = prof.strip()
      response = bot.who_is(prof)
      embed = discord.Embed(
         title = f"Professor Information",
         url = "https://www.deanza.edu/directory/",
         color = discord.Color.blue()
      )
      for data in response:
         embed.add_field(name = f"{data[0]}  (Department: {data[1]})", value = f"Email: {data[2]}", inline = False)
      await message.channel.send(embed=embed)

   elif message.content.lower().startswith("!grades"):
      # !grades <instructor> 
      args = message.content.lower().split("--")
      if len(args) == 1:
         prof = re.sub(r'!grades ', '', args[0])
         prof = re.sub(" +", ' ', prof)
         prof = prof.strip()
         response = bot.prof_grade_info(prof)
         table = PrettyTable()
         table.field_names = ["Year", "Semester", "Professor", "Subject", "Course", "A", "B", "C", "D", "F", "W"]
         for data in response:
            table.add_row(data)
         await message.channel.send(f"```{table}```")

      elif len(args) == 3:
         subj = args[1].strip()
         crse = args[2].strip()
         crse = course_parser(crse)
         prof = re.sub(r'!grades ', '', args[0])
         prof = re.sub(" +", ' ', prof)
         prof = prof.strip()
         print(f"prof: {prof}, subj: {subj}, crse: {crse}")
         if prof == "":
            response = bot.prof_grade_info(subj, crse)  # find most A professor for a course (Easiest A)
         else:
            response = bot.prof_grade_info(prof, subj, crse)
         table = PrettyTable()
         table.field_names = ["Year", "Semester", "Professor", "Subject", "Course", "A", "B", "C", "D", "F", "W"]
         for data in response:
            table.add_row(data)
         await message.channel.send(f"```{table}```")

      else:
         await message.channel.send("Please use a valid command with the correct number of arguments")
     


   elif message.content.lower().startswith("!sch_find"):
      args = message.content.lower().split()
      if len(args) == 3:
         term = args[1]
         subj = args[2]
         await message.channel.send("two args")
     
      elif len(args) == 4:
         term = args[1]
         subj = args[2]
         crse = args[3]
         await message.channel.send("three args")
      else:
         await message.channel.send("Invalid number of arguments")

client.run(DISCORD_TOKEN)
