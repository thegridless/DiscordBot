# Discord Bot # MAFIA
import typing
import discord
import random
from discord.ext import commands  # подгрузка библиотек

TOKEN = 'NzQzMDc1MjE1MzEwODQ4MDAw.XzPYuQ.ksRcVxyBqRGXHWWZ6VemWNZCr5Q'  # токен бота

players = []  # массив игроков
mafia = []
# m_count = len(players) / 3.5  # формула для расчета количества членов мафии в игре
# round(m_count)
m_count = 1

bot = commands.Bot(command_prefix='!')  # инициализация преффикса


@bot.command(pass_context=True)  # разрешаем передавать агрументы
async def play(ctx):  # функция для !play
    if (ctx.author in players):
        await ctx.send(str(ctx.author) + ", вы уже в игре")
    else:
        players.append(ctx.author)
        # global pcounter  # использование глобальной переменной pcounter
        # await ctx.send("Игрок " + str(ctx.author.mention) + " присоединился к игре \n" + "Количество игроков : " + str(len(players)))
        # await ctx.send("Список текущих игроков: ")
        # for element in players:
        #     await ctx.send(element)

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
    if (ctx.author.mention in players):
        players.remove(ctx.author.mention)
        await ctx.send(str(ctx.author.mention) + ", вы покинули следующую игру")
    else:
        await ctx.send(str(ctx.author.mention) + ", вы не участвуете в следующей игре")


@bot.command()  # правила игры
async def rules(ctx):
    await ctx.send('Правила игры в Мафию: https://www.eventnn.ru/articles/item/68/1029/')


# берем из списка в зависимости от количества m_count челов и отдаем им роль мафии а остальным даем мирных
@bot.command()  # сообщение в лс кто я
async def start(ctx):
    guild = ctx.message.guild
    channel = guild.create_voice_channel('Мафиозники')
    # await guild.create_voice_channel('Мафиозники')
    for element in players:
        # берем id каждого юзера написавшего !play
        user = bot.get_user(element.id)
        # отправляем ему роль
        await user.send("говна кусок")
        # await ctx.move_member(element, channel)


@bot.command()
async def mafiap(ctx): #рабочая отправляет в лс кто ты есть на самом деле
    f = 0
    while f < m_count:
        maf = random.randint(0, len(players))
        f += 1
    i = 0
    for i in range(len(players)):
        if i == maf:
            user = bot.get_user(players[maf].id)
            await user.send('ты мафия ')
        else:
            user = bot.get_user(players[i].id)
            await user.send('ты мирный ')



bot.run(TOKEN)  # запуск бота//
