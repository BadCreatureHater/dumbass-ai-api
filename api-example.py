import discord
from discord.ext import commands
import requests
import io

# Initialize bot with a command prefix
intents = discord.Intents.default()
intents.message_content = True  # Required to read the prompt from messages
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name} (ID: {bot.user.id})")
    print("------")

@bot.command(name="generate")
async def generate_image(ctx, *, prompt: str):
    """Generates an image from a text prompt using Pollinations AI."""
    # Notify the user that processing has started
    await ctx.send(f"🎨 Generating: '{prompt}'... Please wait.")

    # Clean the prompt for the URL structure
    encoded_prompt = requests.utils.quote(prompt)
    api_url = f"https://pollinations.ai{encoded_prompt}?width=1024&height=1024&enhanced=true"

    try:
        # Fetch the image data from the API
        response = requests.get(api_url, timeout=30)
        
        if response.status_code == 200:
            # Convert raw bytes into a file object Discord can read
            image_bytes = io.BytesIO(response.content)
            discord_file = discord.File(fp=image_bytes, filename="generated_image.png")
            
            # Send the image back to the exact same channel
            await ctx.send(file=discord_file)
        else:
            await ctx.send("❌ Failed to generate image. The API might be down.")
            
    except Exception as e:
        print(f"Error encountered: {e}")
        await ctx.send("❌ An error occurred while processing your request.")

# Run the bot
bot.run("YOUR_DISCORD_BOT_TOKEN")
bot.run(YOURTOKENTHERE)
