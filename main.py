# Discord Bot # название

import discord
from discord.ext import commands  # подгрузка библиотек

TOKEN = 'NzQzMDc1MjE1MzEwODQ4MDAw.XzPYuQ.ksRcVxyBqRGXHWWZ6VemWNZCr5Q'  # токен бота

pcounter = 1 #количество игроков написавших !play

bot = commands.Bot(command_prefix='!')  # инициализация преффикса


@bot.command(pass_context=True)  # разрешаем передавать агрументы
async def play(ctx):#функция для !play
    global pcounter #использование глобальной переменной pcounter
    await ctx.send("Number of players " + str(pcounter))
    pcounter = pcounter + 1


bot.run(TOKEN)  # запуск бота//
