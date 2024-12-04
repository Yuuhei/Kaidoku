import discord
import base64
import datetime

intents = discord.Intents.default()
intents.members = True

kaidoku = discord.Client(intents=intents)

allowed_channel_id = YOUR_CHANNEL_ID

@kaidoku.event
async def on_ready():
    print(f"Heyo, {kaidoku.user.name} here! Script loaded and ready to rock!")
    await kaidoku.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="I'm broke | >decode"))

@kaidoku.event
async def on_message(message):
    if message.author == kaidoku.user:
        return

    if message.content.startswith('>decode'):
        print(f"[{datetime.datetime.now()}] Command used by {message.author}: {message.content}")
        if message.channel.id != allowed_channel_id:
            await message.reply(f"Oof! This command can only be used in <#{allowed_channel_id}>!")
            return

        encoded_string = message.content.replace('>decode', '').strip()

        if not encoded_string:
            await message.add_reaction('❌')
            await message.reply(f"I can't understand the string that you sent, please provide a valid Base64 string/URL.")
            return

        if len(encoded_string) % 4 != 0:
            encoded_string += "=" * (4 - len(encoded_string) % 4)
        try:
            decoded_string = base64.b64decode(encoded_string).decode('utf-8')
        except:
            await message.add_reaction('❌')
            encoded_string = encoded_string.rstrip("=")
            await message.reply(f"I can't understand the string that you sent, please check your Base64 string/URL before sending it to me.\nUnable to parse: {encoded_string}")
            return

        try:
            await message.author.send(f"Heyo! I barely made in here 😫\n \nBy the way, here is the decoded Base64 link: {decoded_string}")
        except discord.errors.Forbidden:
            await message.add_reaction('❌')
            await message.reply(f"{message.author.mention}, I can't send you a DM, **please enable __Direct Messages__ on Privacy Settings on this server!**")
            return

        await message.add_reaction('✅')
        await message.reply(f"Done decoding! Please check your DM, I already sent the decoded Base64 URL there.\nIf you didn't received a DM from me, **please enable __Direct Messages__ on Privacy Settings for this server!**")


kaidoku.run('YOUR_BOT_TOKEN')
