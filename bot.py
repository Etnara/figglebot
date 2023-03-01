import discord

token = "Discord Bot Token"

client = discord.Client(intents = discord.Intents.all())

@client.event
async def on_ready():
    print(f"Bot logged in as {client.user}")

@client.event
async def on_message(message):
    if message.content.lower().startswith("test alert"):
        embed = discord.Embed(title = "{Home} vs {Away} in {Game}",
                              url = "https://www.example.com",
                              description = "{Date} at {Time}",
                              color = 0xFD82D7)
        await message.channel.send(embed = embed)

client.run(token)
