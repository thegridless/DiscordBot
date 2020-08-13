# Discord Bot # MAFIA
import typing
import discord
from discord.ext import commands  # подгрузка библиотек

TOKEN = 'NzQzMDc1MjE1MzEwODQ4MDAw.XzPYuQ.ksRcVxyBqRGXHWWZ6VemWNZCr5Q'  # токен бота

players =[] #массив игроков

bot = commands.Bot(command_prefix='!')  # инициализация преффикса


@bot.command(pass_context=True)  # разрешаем передавать агрументы
async def play(ctx):#функция для !play
    if(ctx.author.discriminator in players):
       await ctx.send("Вы уже в игре")
    else:
        players.append(ctx.author.discriminator);
        global pcounter #использование глобальной переменной pcounter
        await ctx.send("Игрок " + str(ctx.author) +" присоединился к игре \n" + "Количество игроков : " + str(len(players)))



@bot.command()  # правила игры
async def rules(ctx):
    await ctx.send('Правила игры в Мафию: https://www.eventnn.ru/articles/item/68/1029/')


bot.run(TOKEN)  # запуск бота//
