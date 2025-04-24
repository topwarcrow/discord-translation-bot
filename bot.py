import threading
import socket
import os  # ← すでにあるはずだけど念のため

PORT = int(os.environ.get("PORT", 10000))  # ← ここを追加

def dummy_server():
    s = socket.socket()
    s.bind(('', PORT))  # ← 固定値10000からPORT変数に変更
    s.listen(1)
    while True:
        conn, addr = s.accept()
        conn.close()

threading.Thread(target=dummy_server, daemon=True).start()

import discord
from discord.ext import commands
from googletrans import Translator
import os
TOKEN = os.getenv("TOKEN")

JAPANESE_CHANNEL_ID = 1364961133940838512
ENGLISH_CHANNEL_ID = 1364960893493973092

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

translator = Translator()

@bot.event
async def on_ready():
    print(f"{bot.user.name} 起動完了！")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if message.channel.id == JAPANESE_CHANNEL_ID:
        result = translator.translate(message.content, src="ja", dest="en")
        target_channel = bot.get_channel(ENGLISH_CHANNEL_ID)
        await target_channel.send(f"{message.author.display_name}: {result.text}")

    elif message.channel.id == ENGLISH_CHANNEL_ID:
        result = translator.translate(message.content, src="en", dest="ja")
        target_channel = bot.get_channel(JAPANESE_CHANNEL_ID)
        await target_channel.send(f"{message.author.display_name}: {result.text}")

    await bot.process_commands(message)

bot.run(TOKEN)
