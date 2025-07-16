import discord
import io
import os
from bot.obfuscator import obfuscate

# Load .env if token isn't already set
if "DISCORD_BOT_TOKEN" not in os.environ:
    from dotenv import load_dotenv
    load_dotenv()

TOKEN = os.environ.get("DISCORD_BOT_TOKEN")
print("[DEBUG] Loaded token:", "Yes" if TOKEN else "No")

if not TOKEN or not TOKEN.strip():
    raise RuntimeError("DISCORD_BOT_TOKEN is missing or empty")

INTENTS = discord.Intents.default()
INTENTS.message_content = True

class VelonixBot(discord.Client):
    async def on_ready(self):
        print(f'[VelonixBot] Logged in as {self.user} (ID: {self.user.id})')

    async def on_message(self, message):
        if message.author.bot:
            return
        if message.attachments:
            attachment = message.attachments[0]
            if not attachment.filename.lower().endswith(('.lua', '.txt')):
                return await message.channel.send("⚠️ Please provide a `.lua` or `.txt` file.")
            content = await attachment.read()
            src = content.decode('utf-8', errors='ignore')
            obf = obfuscate(src)
            buf = io.BytesIO(obf.encode())
            await message.channel.send(
                content="✅ Obfuscated by **Velonix Team**.",
                file=discord.File(buf, filename="Velonix_Obfuscated.lua")
            )

    async def on_error(self, event_method, *args, **kwargs):
        import traceback
        print(f"[ERROR] in event: {event_method}")
        traceback.print_exc()

if __name__ == '__main__':
    VelonixBot(intents=INTENTS).run(TOKEN)
