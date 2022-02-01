import discord, os
from discord.ext import commands, tasks
from discord_components import *
from quran import ayaat, search_ayaat
from trivia import gen_question
from TorD import get_dare, get_truth
from random import randint, choice
import json, requests

#./install.bash

SERVER = 710346112086704239

bot = commands.Bot(command_prefix='!')

DiscordComponents(bot)


mention = lambda user_id: f"<@!{user_id}>"
convert_id = lambda mention: mention[3:-1]

async def real_member(user_id):

  await bot.wait_until_ready()
  guild = bot.get_guild(SERVER)
  member = await guild.fetch_member(user_id)

  if member:
    return True
  
  return False

@bot.event
async def on_ready():

  await bot.wait_until_ready()
  guild = bot.get_guild(SERVER)

  channel = discord.utils.get(guild.text_channels, name="general")

  await channel.send("Salam brothers, I'm back online! :mosque: ")
  
@bot.command(name="search_ayaat")
async def quran_search(ctx):

  content = ctx.message.content.split()[1:]

  msg = await ctx.channel.send(f'Searching for Ayaat **[{content[0]}]** ..... :mag_right::face_with_monocle: ')

  search_ayaat(content[0])

  await msg.delete()
  await ctx.channel.send(file=discord.File('ayaat.jpg'))
  os.remove('ayaat.jpg')

@bot.command(name="haram")
async def haram_rater(ctx):

  content = ctx.message.content.split()[1:]
  
  user_id = convert_id(content[0]) if content else ctx.message.author.id

  num = randint(0,100)
  role = discord.utils.get(ctx.guild.roles, name="Sussy Baka")
  
  member = await ctx.guild.fetch_member(user_id)

  if not member: return

  if role in member.roles: num = 100
  
  if int(user_id) == bot.user.id: num = 0

  embedVar = discord.Embed(title="Haram R8r 2000", description=f"\n{mention(user_id)} is **{num}%** haram :gay_pride_flag:", color=0xFF00FF)
  
  await ctx.channel.send(embed=embedVar)

@bot.command(name="trivia")
async def trivia(ctx):

  question, answer, options = gen_question()

  buttons = [Button(style=ButtonStyle.blue, label=opt) for opt in options]

  embedVar = discord.Embed(title="Trivia", description=question, color=0xE69138)

  await ctx.channel.send(embed=embedVar,components=buttons)

  response = None

  while True:
    response = await bot.wait_for("button_click", timeout = 180)
    if response.user == ctx.message.author and response.component.label in options:
      break

  if response.channel == ctx.channel:

    res = f"Correct! :white_check_mark:  **{response.component.label}** was the right answer!" if response.component.label == answer else f"Incorrect! :x: __{answer}__ was the right answer! You guessed **{response.component.label}**."
    
    await ctx.channel.send(res)

@bot.command(name="dare")
async def dare(ctx):

  content = ctx.message.content.split()[1:]
  
  user_id = convert_id(content[0]) if content else ctx.message.author.id
   
  guild = bot.get_guild(SERVER)
  
  member = await guild.fetch_member(user_id)

  if not member:
    return


  embedVar = discord.Embed(title="Dare", description=f"\n {get_dare()}  {mention(user_id)}", color=0x552E12)
  
  await ctx.channel.send(embed=embedVar)

@bot.command(name="truth")
async def truth(ctx):

  content = ctx.message.content.split()[1:]
  
  user_id = convert_id(content[0]) if content else ctx.message.author.id
   
  guild = bot.get_guild(SERVER)
  
  member = await guild.fetch_member(user_id)

  if not member:
    return


  embedVar = discord.Embed(title="Truth", description=f"\n {get_truth()}  {mention(user_id)}", color=0x552E12)
  
  await ctx.channel.send(embed=embedVar)

@tasks.loop(hours=24)

async def daily_ayaat():

  await bot.wait_until_ready()

  verse, v_num = ayaat()
  

  guild = bot.get_guild(SERVER)

  embedVar = discord.Embed(title=f"Daily Ayaat [{v_num}]", description=verse, color=0x40FFCC)
  
  channel = discord.utils.get(guild.text_channels, name="daily-wisdom")

  await channel.send(embed=embedVar)

daily_ayaat.start()

@bot.command(name="coinflip")
async def coinflip(ctx):
  
  coinfaces = [
    "https://media.discordapp.net/attachments/617115357072850994/868738674106462208/tails.PNG","https://media.discordapp.net/attachments/617115357072850994/868738560520515604/heads.PNG"
    ]
    
  await ctx.channel.send(choice(coinfaces))

@bot.command(name="ask")
async def magic_ball(ctx):

  content = ctx.message.content.split()[1:]

  data = json.loads(requests.get('https://8ball.delegator.com/magic/JSON/Will%20I%20ever%20give%20you%20up%3F').text)

  embedVar = discord.Embed(title=' '.join(content), description=data['magic']['answer'], color=0xFFCCAA)

  await ctx.channel.send(embed=embedVar)

@bot.command(name="joke")
async def joke(ctx):

  joke = None
  delivery = None
  data = json.loads(requests.get('https://v2.jokeapi.dev/joke/Any').text)

  try: 
    joke = data['setup']
    delivery = data['delivery']
  except KeyError: 
    joke =  ''
    delivery = data['joke']

  embedVar = discord.Embed(title=joke, description=delivery, color=0x9900FF)

  await ctx.channel.send(embed=embedVar)

bot.run("ODY4NTQ1Mjk3NzA4NjQ2NDUx.YPxN1w.RnhJg21Nny7PLW_PCvw-omSOdVU")
#bot.loop.create_task()
