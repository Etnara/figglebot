import discord
import selenium
import time
from discord.ext import tasks
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# User Variables
token = "Discord Bot Token"
channel_id = Channel ID
email = "Generation Esports Email"
password = "Generation Esports Password"

# Module Variables
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome("Path to ChromeDriver", options = options) 
options.add_argument("--headless")
client = discord.Client(intents = discord.Intents.all())

# Goto Generation Esports
driver.get("https://app.generationesports.com/")
time.sleep(15) # Wait for page to load

# Login
driver.find_element("id", "mat-input-0").send_keys(email)
driver.find_element("id", "mat-input-1").send_keys(password + Keys.RETURN)
time.sleep(15) # Wait for page to load

#
# Discord Functions
#

# Bot Ready
@client.event
async def on_ready():
    print(f"Bot logged in as {client.user}")
    match_alert.start() # Start Match Alert Loop

@tasks.loop(seconds = 3600)
async def match_alert():
    await client.wait_until_ready()

    # Goto Matches
    print("Checking for new matches...")
    try:
        global Time # Set Match Time as a global variable
        Time = driver.find_element("xpath", "/html/body/app-root/app-wrapper/div/mat-drawer-container/mat-drawer-content/div/div[1]/div/app-dashboard/div/div[2]/gene-card/mat-card/div[2]/single-elim-match-dashboard/div/div[3]/div[1]/span[1]").text
        driver.find_element("xpath", "/html/body/app-root/app-wrapper/div/mat-drawer-container/mat-drawer-content/div/div[1]/div/app-dashboard/div/div[2]/gene-card/mat-card/div[2]/single-elim-match-dashboard/div/div[3]/div[2]/div[2]/button").click()
        time.sleep(15) # Wait for page to load
    except:
        return

    # Get Team Names
    home = driver.find_element("xpath", "/html/body/app-root/app-wrapper/div/mat-drawer-container/mat-drawer-content/div/div[1]/div/app-edit-match-page/div[2]/div[3]/div/div/mat-accordion/mat-expansion-panel/div/div/div[1]/h4[1]/a").text
    away = driver.find_element("xpath", "/html/body/app-root/app-wrapper/div/mat-drawer-container/mat-drawer-content/div/div[1]/div/app-edit-match-page/div[2]/div[3]/div/div/mat-accordion/mat-expansion-panel/div/div/div[1]/h4[2]/a").text

    # Get Player Names
    homePlayers = []
    i = 1
    while True:
        try:
            homePlayers.append(driver.find_element("xpath", f"/html/body/app-root/app-wrapper/div/mat-drawer-container/mat-drawer-content/div/div[1]/div/app-edit-match-page/div[2]/div[6]/div[1]/mat-accordion/mat-expansion-panel/div/div/div/table/tbody/tr[{i}]/td[2]").text)
            i+=1
        except:
            break

    awayPlayers = []
    j = 1
    while True:
        try:
            awayPlayers.append(driver.find_element("xpath", f"/html/body/app-root/app-wrapper/div/mat-drawer-container/mat-drawer-content/div/div[1]/div/app-edit-match-page/div[2]/div[6]/div[2]/mat-accordion/mat-expansion-panel/div/div/table/tbody/tr[{j}]/td[2]").text)
            j+=1
        except:
            break

    # Format Player Names
    homePlayersList = ""
    for player in homePlayers:
        fPlayer = player.replace(" ", "%20")
        homePlayersList += f"[{player}](https://www.op.gg/summoners/na/{fPlayer})\n"

    awayPlayersList = ""
    for player in awayPlayers:
        fPlayer = player.replace(" ", "%20")
        awayPlayersList += f"[{player}](https://www.op.gg/summoners/na/{fPlayer})\n"

    # Print Match Info
    print(f"Match found: {home} vs {away}\n{Time}")
    print(f"{homePlayers}")
    print(f"{awayPlayers}")

    # Send Match Alert
    channel = client.get_channel(channel_id) # Channel ID
    embed = discord.Embed(title = f"{home} vs {away}", # Possibly add what game is being played
                          url = driver.current_url,
                          description = f"{Time}",
                          color = 0xFD82D7)
    embed.add_field(name = f"{home}", value = homePlayersList, inline = True)
    embed.add_field(name = f"{away}", value = awayPlayersList, inline = True)

    # If last message is the same don't send
    async for message in channel.history(limit = 1):
        if message.embeds[0].title == embed.title:
            print("No new matches found")
        else:
            await channel.send(embed = embed)

# Login to Discord
try:
    client.run(token)
except:
    print("Unable to Login to Discord")
    exit()
