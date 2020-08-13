import ctx as ctx
import typing
import discord
from discord.ext import commands  # подгрузка библиотек

@main.bot.command(pass_context=True)  # разрешаем передавать агрументы
async def test(ctx, arg):  # создаем асинхронную фунцию бота
    await ctx.send(arg)  # отправляем обратно аргумент


@bot.command()
async def kekw(ctx,arg):
    await ctx.send('privet')