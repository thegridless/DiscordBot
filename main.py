# Discord Bot # MAFIA
import discord
import random
import asyncio
import time
import ffmpeg
from discord.ext import commands  # подгрузка библиотек
from discord.utils import get

TOKEN = 'NzQzMDc1MjE1MzEwODQ4MDAw.XzPYuQ.ksRcVxyBqRGXHWWZ6VemWNZCr5Q'  # токен бота

# players = []  # массив игроков
# mafia = []
# p_pl = []  # массив игроков, которых выставили на голосование
sounds = [10] # массив звуков
sounds[0]="sounds/пушка.mp3" # пути к звукам

global g
bot = commands.Bot(command_prefix='!')  # инициализация преффикса

games = {}

class Game:
    def __init__(self):
        self.players = []
        self.mafia = []
        self.p_pl = []


@bot.command(pass_context=True)  # разрешаем передавать агрументы
async def play(ctx):  # функция для !play
    if ctx.guild.id not in games:
        games[ctx.guild.id] = Game()
    
    if ctx.author.voice == None:
        await ctx.send(ctx.author.mention + ", зайди в голосовой канал!!")
    else:
        if ctx.author in games[ctx.guild.id].players:
            await ctx.send(str(ctx.author) + ", вы уже в игре")
        else:
            games[ctx.guild.id].players.append(ctx.author)
            embed = discord.Embed(
                description=str(ctx.author.mention) + " присоединился к игре",
                colour=discord.Colour.blue()
            )
            embed.set_footer(text='Хорошей игры')
            embed.set_image(url='https://2ch.hk/b/arch/2020-07-07/src/224156532/15940650663840.png')
            embed.add_field(name="Количество участников: ", value=str(len(games[ctx.guild.id].players)), inline=True)
            embed.add_field(name='Список участников', value=','.join([str(elem.mention) for elem in games[ctx.guild.id].players]), inline=False)
            await ctx.send(embed=embed)

    g = ctx.message.guild.id

# функция для того чтобы покинуть игру
@bot.command()
async def leave(ctx):
    # условие для проверки учатсвует ли игрок в некст игре
    if ctx.author in [ctx.guild.id].players:
        [ctx.guild.id].players.remove(ctx.author)
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



    # if voice and voice.is_connected():
    #     await voice.move_to(channel_voice)
    # else:
    #     voice = await channel_voice.connect()

    # перемещение юзеров
    for element in games[ctx.guild.id].players:
        await element.move_to(channel_voice)
        # await element.edit(mute=True)

    await t_rand(ctx)
    await roles(ctx)  # выдача ролей
    # await asyncio.sleep(10)
    #РАСКОМЕНТИТЬ
    await game(ctx)
    await golosovanie(ctx)
    await asyncio.sleep(5)
    #await playSound(ctx, _source=sounds[0])


@bot.command()
async def stop(ctx):  # функция для удаления каналов
    # await asyncio.sleep(5)
    await channel_voice.delete()
    await channel_text.delete()


# @bot.command()
# async def left(ctx):  # функция для выхода из voice канала
#     c = ctx.message.author.voice.channel
# #     voice = get(bot.voice_clients, guild=ctx.guild)
# #     if voice and voice.is_connected():
# #         await voice.disconnect()


async def roles(ctx):  # рабочая отправляет в лс кто ты есть на самом деле
    global acab_random
    global doctor_random
    global don_random
    f = 0
    global maf
    maf = []
    m_count = len(games[ctx.guild.id].players) / 3
    round(m_count)
    while f < m_count:
        jke = random.randint(0, len(games[ctx.guild.id].players) - 1)
        if jke in maf:
            f -= 1
        else:
            maf.append(jke)
        f += 1
    maf.sort()

    don_random = random.choice(maf)
    user1 = bot.get_user(games[ctx.guild.id].players[don_random].id)
    await user1.send('Ваша роль - Дон.')

    # выдача роли полицая
    acab_random = random.randint(0, len(games[ctx.guild.id].players) - 1)
    while acab_random in maf:
        acab_random = random.randint(0, len(games[ctx.guild.id].players) - 1)
        break

    user2 = bot.get_user(games[ctx.guild.id].players[acab_random].id)
    await user2.send('Ваша роль - Комиссар.')

    doctor_random = random.randint(0, len(games[ctx.guild.id].players) - 1)
    while doctor_random in maf or doctor_random == acab_random:
        doctor_random = random.randint(0, len(games[ctx.guild.id].players) - 1)
        break

    user3 = bot.get_user(games[ctx.guild.id].players[doctor_random].id)
    await user3.send('Ваша роль - Доктор.')

    j = 0
    for i in range(len(games[ctx.guild.id].players)):
        if i == maf[j]:
            if i == don_random:
                continue
            else:
                user = bot.get_user(games[ctx.guild.id].players[i].id)
                await user.send('Ваша роль - Мафия.')
                if j < len(maf) - 1:
                    j += 1
        else:
            if i == acab_random or i == doctor_random:
                continue
            else:
                user = bot.get_user(games[ctx.guild.id].players[i].id)
                await user.send('Ваша роль - Мирный житель.')
    # выдача роли дона


async def t_rand(ctx):
    global d, d_list
    d = {}
    for i in games[ctx.guild.id].players:
        jke = random.randint(1, len(games[ctx.guild.id].players))
        while jke in d.keys():
            jke = random.randint(1, len(games[ctx.guild.id].players))
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
    embed1.add_field(name='Номера:', value='\n'.join([str(i) + " - " + str(d[i].mention) for i in d_list]),
                     inline=False)
    await channel_text.send(embed=embed1)
    # print(d)


async def game(ctx):
    await channel_text.send("Игра началась!!!")

    for i in d_list:

        choice = False

        await channel_text.send("Игрок " + str(i) + " - " + str(d[
                                                                    i].mention) + ". Ваша минута!\nЕсли вы хотите выставить игрока на голосование напишите его номер в данный чат.")
        t_end = time.time() + 10
        while time.time() < t_end:
            try:
                msg = await bot.wait_for('message', timeout=10.0)
            except asyncio.TimeoutError:
                break

            s = msg.content
            if s.isdigit() == False:
                await channel_text.send("Напишите существующий номер")
            elif msg.author != d[i]:
                await channel_text.send("Сейчас не ваша минута")
            elif int(s) <= len(games[ctx.guild.id].players) and int(s) > 0 and msg.channel == channel_text:
                if (int(s) in games[ctx.guild.id].p_pl):
                    await channel_text.send("Этот игрок уже выставлен")
                else:
                    await channel_text.send("Вы выставили игрока " + str(msg.content) + " на голосование!")
                    if choice == False:
                        games[ctx.guild.id].p_pl.append(int(s))
                        choice = True
                    else:
                        games[ctx.guild.id].p_pl.pop()
                        games[ctx.guild.id].p_pl.append(int(s))

            else:
                await channel_text.send("Напишите существующий номер")

    embed_p = discord.Embed(
        title="Выставленые игроки на голосование",
        description="Голосование проходит в порядке выстовления игроков",
        colour=discord.Colour.blue()
    )
    embed_p.set_footer(text='Хорошей игры')
    # embed_p.set_image(url='https://2ch.hk/b/arch/2020-07-07/src/224156532/15940650663840.png')
    embed_p.add_field(name='Номера:', value='\n'.join([str(i) + " - " + str(d[i].mention) for i in games[ctx.guild.id].p_pl]),
                      inline=False)
    await channel_text.send(embed=embed_p)

# функция воспроизведения звуков
async def playSound(ctx, _source):
    voice.play(discord.FFmpegPCMAudio(executable="C:/ffmpeg/bin/ffmpeg.exe", source=_source))

# проверочная команда для воспроизведения
@bot.command()
async def ps(ctx):
    voice.play(discord.FFmpegPCMAudio(executable="C:/ffmpeg/bin/ffmpeg.exe", source=sounds[0]))


async def golosovanie(ctx):
    global g_list
    g_list = [] #список игроков которые отправили сообщение
    p_pl1 = {} #словарь номинированных с количеством голосов
    print(games[ctx.guild.id].p_pl)

    for i in range(len(games[ctx.guild.id].p_pl)):
        await channel_text.send("Игрок " + str(games[ctx.guild.id].p_pl[i]) + " - " + games[ctx.guild.id].players[games[ctx.guild.id].p_pl[i]-1].mention + ". Ваша минута!\n Попробуй оправдаться, мудазвон")
        await asyncio.sleep(5)

    global msg, pg_users, ma

    for i in range(len(games[ctx.guild.id].p_pl)):
        await channel_text.send('Голосуем за игрока '+ str(games[ctx.guild.id].p_pl[i]) + " - " + games[ctx.guild.id].players[games[ctx.guild.id].p_pl[i]-1].mention + ", если считаете, что он мафия, напишите плюсик")
        t_end = time.time() + 10
        while time.time() < t_end:
            try:
                msg = await bot.wait_for('message', timeout=10.0)
                s = msg.content
                ma = ctx.message.author
                print(ma)

                if s != '+':
                    await channel_text.send(ma.mention + " Напишите плюсик")
                elif ma not in g_list:
                    g_list.append(ma)
                else:
                    continue
            except asyncio.TimeoutError:
                break

            # #я хз так ли это работает
            # s = msg.content
            # ma = ctx.message.author
            # print (ma)
            #
            # if s != '+':
            #     await channel_text.send(ma.mention + " Напишите плюсик")
            # elif ma not in g_list:
            #     g_list.append(ma)
            # else:
            #     continue

        await channel_text.send('За исключение игрока '+ str(games[ctx.guild.id].p_pl[i]) + " - " + games[ctx.guild.id].players[games[ctx.guild.id].p_pl[i]-1].mention + 'проголосвало ' + str(len(g_list)) + ' человек(а)')




        p_pl1.update({len(g_list): games[ctx.guild.id].p_pl[i]})




#
# #берем ключи сортируем и по наибольшему ключу вычисляем кикнутого
#     p = list(p_pl1.keys())
#     p.sort()
#     key = p.pop()
#     yo = p_pl1.get(key)
#     channel_text.send('Игрок '+yo.mention+' покидает игру')

async def check(ctx,number):
    user = bot.get_user(games[ctx.guild.id].players[number].id)
    await user.send('Отправьте номер для проверки, у вас есть 10 секунд')

    t_end = time.time() + 10
    while time.time() < t_end:
        try:
            msg = await bot.wait_for('message', timeout=10.0)
        except asyncio.TimeoutError:
            break

        s = msg.content

    if not s.isdigit():
        await channel_text.send("Напишите существующий номер")

    if number == don_random:
        if s == acab_random:
            await user.send("Роль игрока под номером" + s + "- Коммисар.")
        elif s == doctor_random:
            await user.send("Роль игрока под номером" + s + "- Доктор.")
        else:
            await user.send("Роль игрока под номером" + s + "- Мирный житель.")

    if number == acab_random:
        if s in maf:
            await user.send("Роль игрока под номером" + s + "- Мафия.")
        elif s == don_random:
            await user.send("Роль игрока под номером" + s + "- Дон.")
        else:
            await user.send("Роль игрока под номером" + s + "- Не мафия.")
    # если че тут маньяка добавить ещё



bot.run(TOKEN)  # запуск бота//
