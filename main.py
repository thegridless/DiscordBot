# Discord Bot # MAFIA
import discord
import random
import asyncio
from abc import ABC
import time
from discord.ext import commands  # подгрузка библиотек
from discord.utils import get

class MyABC(ABC):
    pass

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
    # не забыть раскоментить
    guild = ctx.message.guild
    global channel_voice
    channel_voice = await guild.create_voice_channel('Мафиозники')
    global channel_text
    channel_text = await guild.create_text_channel('Мафиозники')
    # подключение бота к каналу
    global voice

    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel_voice)
    else:
        voice = await channel_voice.connect()

    await voice.disconnect()

    if voice and voice.is_connected():
        await voice.move_to(channel_voice)
    else:
        voice = await channel_voice.connect()
    # перемещение юзеров
    # for element in players:
    #     await element.move_to(channel)
        # await element.edit(mute=True)

    await t_rand()
    await roles()  # выдача ролей
    # await asyncio.sleep(10)
    await game(ctx)


@bot.command()
async def stop(ctx):  # функция для удаления каналов
    await asyncio.sleep(5)
    await channel_voice.delete()
    await channel_text.delete()


# @bot.command()
# async def left(ctx):  # функция для выхода из voice канала
#     c = ctx.message.author.voice.channel
# #     voice = get(bot.voice_clients, guild=ctx.guild)
# #     if voice and voice.is_connected():
# #         await voice.disconnect()


async def roles():  # рабочая отправляет в лс кто ты есть на самом деле
    global acab_random
    global doctor_random
    global don_random
    f = 0
    maf = []
    m_count = len(players) / 3
    round(m_count)
    while f < m_count:
        jke = random.randint(0, len(players) - 1)
        if jke in maf:
            f -= 1
        else:
            maf.append(jke)
        f += 1
    maf.sort()

    don_random = random.choice(maf)
    user1 = bot.get_user(players[don_random].id)
    await user1.send('Ваша роль - Дон.')

    # выдача роли полицая
    acab_random = random.randint(0, len(players) - 1)
    while acab_random in maf:
        acab_random = random.randint(0, len(players) - 1)
        break

    user2 = bot.get_user(players[acab_random].id)
    await user2.send('Ваша роль - Комиссар.')

    doctor_random = random.randint(0, len(players) - 1)
    while doctor_random in maf or doctor_random==acab_random:
        doctor_random = random.randint(0, len(players) - 1)
        break

    user3 = bot.get_user(players[doctor_random].id)
    await user3.send('Ваша роль - Доктор.')


    j = 0
    for i in range(len(players)):
        if i == maf[j]:
            if i == don_random:
                continue
            else:
                user = bot.get_user(players[i].id)
                await user.send('Ваша роль - Мафия.')
                if j < len(maf) - 1:
                    j += 1
        else:
            if i == acab_random or i == doctor_random:
                continue
            else:
                user = bot.get_user(players[i].id)
                await user.send('Ваша роль - Мирный житель.')
    # выдача роли дона


async def t_rand():
    global d, d_list
    d = {}
    for i in players:
        jke = random.randint(1, len(players))
        while jke in d.keys():
            jke = random.randint(1, len(players))
        d.update({jke: i})
    d_list = list(d.keys())
    d_list.sort()
    # for i in d_list:
    #     await channel_text.send(str(i) + " - " + str(d[i].mention))
    embed1 = discord.Embed(
        title='Номера игроков',
        description="Игра начнется через 30 секунд",
        colour=discord.Colour.blue()
    )
    embed1.set_footer(text='Хорошей игры')
    embed1.set_image(url='https://2ch.hk/b/arch/2020-07-07/src/224156532/15940650663840.png')
    embed1.add_field(name='Номера:', value='\n'.join([str(i) + " - " + str(d[i].mention) for i in d_list]), inline=False)
    await channel_text.send(embed=embed1)
    # print(d)


async def game(ctx):
    await channel_text.send("Игра началась!!!")

    def check(m):
        temp = m.content
        if temp.isdigit() == False:
            return False
        if int(temp)<=len(players) and int(temp)>0 and m.author== d[i] and m.channel==channel_text:
            return True
        else:
            return False

    for i in d_list:
        await channel_text.send("Игрок " + str(i) + " - " + str(d[i].mention) +". Ваша минута!\nЕсли вы хотите выставить игрока на голосование напишите его номер в данный чат.")
        t_end = time.time() + 60
        while time.time() < t_end:
            msg = await bot.wait_for('message',check=check)
            if check==False:
                await channel_text.send("Напишите существующий номер!!!")
            else:
                await channel_text.send("Вы выставили игрока " + str(msg.content) + " на голосование!")


bot.run(TOKEN)  # запуск бота//
