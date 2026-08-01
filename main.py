import discord
from discord.ext import commands
from model import get_class
import os

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="$", intents=intents)


@bot.event
async def on_ready():
    print(f"{bot.user} olarak giriş yapıldı!")


@bot.command()
async def hello(ctx):
    await ctx.send(f"Merhaba! Ben {bot.user}.")


@bot.command()
async def check(ctx):
    try:
        # Dosya kontrolü
        if len(ctx.message.attachments) == 0:
            await ctx.send("Bir resim eklemeyi unuttun.")
            return

        attachment = ctx.message.attachments[0]
        file_name = attachment.filename

        # Dosyayı kaydet
        await attachment.save(file_name)

        await ctx.send("Resim alındı, kontrol ediliyor...")

        # Tahmin yap
        result = get_class(
            model_path="keras_model.h5",
            labels_path="labels.txt",
            image_path=file_name
        )
