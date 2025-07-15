import os
import io
import threading
from flask import Flask, request, render_template, send_file, abort
from bot.obfuscator import obfuscate

# ✅ Load environment variables from .env
from dotenv import load_dotenv
load_dotenv()

# Discord bot setup
import discord

TOKEN = os.environ.get("DISCORD_BOT_TOKEN")
INTENTS = discord.Intents.default()
INTENTS.message_content = True

class VelonixBot(discord.Client):
    async def on_ready(self):
        print(f"[VelonixBot] Logged in as {self.user}")

    async def on_message(self, message):
        if message.author.bot:
            return
        if message.attachments:
            attachment = message.attachments[0]
            if not attachment.filename.lower().endswith(('.lua', '.txt')):
                await message.channel.send("⚠️ Please upload a valid `.lua` or `.txt` file.")
                return
            content = await attachment.read()
            code = content.decode('utf-8', errors='ignore')
            obf_code = obfuscate(code)
            buffer = io.BytesIO(obf_code.encode('utf-8'))
            await message.channel.send(
                content="✅ Obfuscated by **Velonix Team**.",
                file=discord.File(buffer, filename='Velonix_Obfuscated.lua')
            )

# Launch Discord bot in background thread
def start_discord_bot():
    if TOKEN:
        bot = VelonixBot(intents=INTENTS)
        bot.run(TOKEN)
    else:
        print("❌ DISCORD_BOT_TOKEN not set. Skipping bot startup.")

threading.Thread(target=start_discord_bot, daemon=True).start()

# Flask app
app = Flask(__name__, template_folder='templates')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/obfuscate', methods=['POST'])
def do_obfuscate():
    file = request.files.get('file')
    if not file or not file.filename.lower().endswith(('.lua', '.txt')):
        abort(400, "Invalid file type. Only .lua or .txt allowed.")
    
    src = file.read().decode('utf-8', errors='ignore')
    obf = obfuscate(src)
    
    buffer = io.BytesIO(obf.encode('utf-8'))
    return send_file(
        buffer,
        as_attachment=True,
        download_name='Velonix_Obfuscated.lua',
        mimetype='text/plain'
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
