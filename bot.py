import discord
import selenium
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# User Variables
token = "Discord Bot Token"
email = "Generation Esports Email"
password = "Generation Esports Password"

# Module Variables
client = discord.Client(intents = discord.Intents.all())
driver = webdriver.Chrome("Path to ChromeDriver")

# Goto Generation Esports
driver.get("https://app.generationesports.com/")

# Login
time.sleep(5) # Wait for page to load
driver.find_element("id", "mat-input-0").send_keys(email)
driver.find_element("id", "mat-input-1").send_keys(password + Keys.RETURN)

# Loop to check for new matches
while True:
    print("Checking for new matches...")
    time.sleep(60) # Wait 60 seconds

#
# Discord Functions
#

# Bot Ready
@client.event
async def on_ready():
    print(f"Bot logged in as {client.user}")

# Match Alert
@client.event
async def on_message(message):
    if message.content.lower().startswith("test alert"):
        embed = discord.Embed(title = "{Home} vs {Away} in {Game}",
                              url = "https://www.example.com",
                              description = "{Date} at {Time}",
                              color = 0xFD82D7)
        embed.add_field(name = "{Home Team}", value = "[Player 1](https://www.example.com)\n [Player 2](https://www.example.com)\n [Player 3](https://www.example.com)\n [Player 4](https://www.example.com)\n [Player 5](https://www.example.com)", inline = True)
        embed.add_field(name = "{Away Team}", value = "[Player 1](https://www.example.com)\n [Player 2](https://www.example.com)\n [Player 3](https://www.example.com)\n [Player 4](https://www.example.com)\n [Player 5](https://www.example.com)", inline = True)   
        await message.channel.send(embed = embed)

client.run(token)
