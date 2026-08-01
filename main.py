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

        if result == "elma":
            await ctx.send("🍎 Elma bulundu!")
            print("Elma; zengin lif, C vitamini ve güçlü antioksidan içeriğiyle bağışıklıktan sindirime kadar tüm vücut sağlığını destekleyen şifalı bir meyvedir. Elma, kalp sağlığını korumaya yardımcı olur, kan şekeri seviyelerini düzenler ve kilo yönetimine katkıda bulunur. Ayrıca, elma kabuğu ve çekirdekleri de besin değeri açısından önemlidir.")
        elif result == "muz":
            await ctx.send("🍌 Muz bulundu!")
            print("Muz; potasyum, lif ve vitaminler açısından zengin bir meyvedir. Kalp sağlığını destekler, sindirimi iyileştirir ve enerji sağlar. Muz ayrıca ruh halini iyileştirebilir ve kas fonksiyonlarını destekler.")
        else:
            await ctx.send(f"Tahmin: {result}")

        # Dosyayı sil
        os.remove(file_name)

    except Exception as e:
        print(e)
        await ctx.send(f"Hata oluştu: {e}")


bot.run("bot tokeni ekleyin")
