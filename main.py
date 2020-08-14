# Discord Bot # MAFIA
import typing
import discord
import random
from discord.ext import commands  # подгрузка библиотек

TOKEN = 'NzQzMDc1MjE1MzEwODQ4MDAw.XzPYuQ.ksRcVxyBqRGXHWWZ6VemWNZCr5Q'  # токен бота

players = []  # массив игроков


m_count = len(players) / 3.5  # формула для расчета количества членов мафии в игре

bot = commands.Bot(command_prefix='!')  # инициализация преффикса


@bot.command(pass_context=True)  # разрешаем передавать агрументы
async def play(ctx):  # функция для !play
    if (ctx.author.mention in players):
        await ctx.send(str(ctx.author.mention) + ", вы уже в игре")
    else:
        players.append(ctx.author.mention)
        # global pcounter  # использование глобальной переменной pcounter
        # await ctx.send("Игрок " + str(ctx.author.mention) + " присоединился к игре \n" + "Количество игроков : " + str(len(players)))
        # await ctx.send("Список текущих игроков: ")
        # for element in players:
        #     await ctx.send(element)


        embed = discord.Embed(
            title=ctx.author.mention,
            colour=discord.Colour.blue()
        )

        embed.set_footer(text='Хорошей игры')
        embed.set_image(url='https://2ch.hk/b/arch/2020-07-07/src/224156532/15940650663840.png')
        embed.set_thumbnail(url='https://2ch.hk/b/arch/2020-07-07/src/224156532/15940650663840.png')
        embed.add_field(name="Количетсво участников: ",value=str(len(players)),inline=True)
        embed.add_field(name='Список участников',value=str(players),inline=False)

        await ctx.send(embed=embed)

#функция для того чтобы покинуть игру
@bot.command()
async def leave(ctx):
    #условие для проверки учатсвует ли игрок в некст игре
    if (ctx.author.mention in players):
        players.remove(ctx.author.mention)
        await ctx.send(str(ctx.author.mention) + ", вы покинули следующую игру")
    else:
        await ctx.send(str(ctx.author.mention)+", вы не участвуете в следующей игре")


@bot.command()  # правила игры
async def rules(ctx):
    await ctx.send('Правила игры в Мафию: https://www.eventnn.ru/articles/item/68/1029/')

#берем из списка в зависимости от количества m_count челов и отдаем им роль мафии а остальным даем мирных
@bot.command()  # сообщение в лс кто я
async def ready(ctx):
   await ctx.author.send("говна кусок")

bot.run(TOKEN)  # запуск бота//
