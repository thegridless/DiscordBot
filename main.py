# Discord Bot # MAFIA
import typing
import discord
import random
from discord.ext import commands  # подгрузка библиотек
from discord.utils import get

TOKEN = 'NzQzMDc1MjE1MzEwODQ4MDAw.XzPYuQ.ksRcVxyBqRGXHWWZ6VemWNZCr5Q'  # токен бота

players = []  # массив игроков
mafia = []

bot = commands.Bot(command_prefix='!')  # инициализация преффикса


@bot.command(pass_context=True)  # разрешаем передавать агрументы
async def play(ctx):  # функция для !play
    if ctx.author in players:
        await ctx.send(str(ctx.author) + ", вы уже в игре")
    else:
        players.append(ctx.author)
        embed = discord.Embed(
            description=str(ctx.author.mention) + " присоединился к игре",
            colour=discord.Colour.blue()
        )
        embed.set_footer(text='Хорошей игры')
        embed.set_image(url='https://2ch.hk/b/arch/2020-07-07/src/224156532/15940650663840.png')
        embed.add_field(name="Количество участников: ", value=str(len(players)), inline=True)
        embed.add_field(name='Список участников', value=','.join([str(elem.mention) for elem in players]), inline=False)
        await ctx.send(embed=embed)


# функция для того чтобы покинуть игру
@bot.command()
async def leave(ctx):
    # условие для проверки учатсвует ли игрок в некст игре
    if ctx.author in players:
        players.remove(ctx.author)
        await ctx.send(str(ctx.author.mention) + ", вы покинули следующую игру")
    else:
        await ctx.send(str(ctx.author.mention) + ", вы не участвуете в следующей игре")


@bot.command()  # правила игры
async def rules(ctx):
    await ctx.send('Правила игры в Мафию: https://www.eventnn.ru/articles/item/68/1029/')


# берем из списка в зависимости от количества m_count челов и отдаем им роль мафии а остальным даем мирных
@bot.command()  # начало игры
async def start(ctx):
    guild = ctx.message.guild
    channel = await guild.create_voice_channel('Мафиозники')
    # подключение бота к каналу
    global voice
    c = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()

    await voice.disconnect()

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
    # перемещение юзеров
    for element in players:
        await element.move_to(channel)
# мут   await element.edit(mute=True)
    await mafiap()  # выдача ролей


# @bot.command()
# async def left(ctx):  # функция для выхода из voice канала
#     c = ctx.message.author.voice.channel
#     voice = get(bot.voice_clients, guild=ctx.guild)
#     if voice and voice.is_connected():
#         await voice.disconnect()


async def mafiap():  # рабочая отправляет в лс кто ты есть на самом деле
    f = 0
    maf = []
    m_count = len(players) / 2
    round(m_count)
    while f < m_count:
        jke = random.randint(0, len(players) - 1)
        if jke in maf:
            f -= 1
        else:
            maf.append(jke)
        f += 1
    maf.sort()
    i = 0
    j = 0
    for i in range(len(players)):
        if i == maf[j]:
            user = bot.get_user(players[i].id)
            await user.send('ты мафия ')
            if j < len(maf):
                j += 1
        else:
            user = bot.get_user(players[i].id)
            await user.send('ты мирный ')


bot.run(TOKEN)  # запуск бота//
