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
sounds = [10]  # массив звуков
sounds[0] = "sounds/пушка.mp3"  # пути к звукам

global g
bot = commands.Bot(command_prefix='!')  # инициализация преффикса

games = {}


class Game:
    def __init__(self):
        self.players = []  # массив игркоов хранится ctx.author
        self.maf = []  # массив с номерами мафий хранится int(рандомные числа)
        self.p_pl = []  # массив с номерами выстваленных на голосование игроков
        self.d = {}  # словарь с игроками хранится {рандомный номер : ctx.author}
        self.d_list = {}  # отсортированный массив с номерами игроков
        self.p_pl1 = {}  # словарь хранится {кол-во голосов : номер игрока}
        self.g_list = []  # массив с проголосовавшими игроками
        self.end_of_game = False
        self.embed = 0
        self.embed1 = 0
        self.embed_p = 0
        self.acab_random = 0
        self.don_random = 0
        self.sherif = 0

@bot.command(pass_context=True)  # разрешаем передавать агрументы
async def play(ctx):  # функция для !play
    if ctx.guild.id not in games:
        games[ctx.guild.id] = Game()

    if ctx.author.voice == None:
        await ctx.send(ctx.author.mention + ", зайди в голосовой канал!!")
    else:
        if ctx.author in games[ctx.guild.id].players:
            await ctx.send(str(ctx.author.mention) + ", вы уже в игре")
        else:
            games[ctx.guild.id].players.append(ctx.author)
            games[ctx.guild.id].embed = discord.Embed(
                description=str(ctx.author.mention) + " присоединился к игре",
                colour=discord.Colour.blue()
            )
            games[ctx.guild.id].embed.set_footer(text='Хорошей игры')
            games[ctx.guild.id].embed.set_image(url='https://2ch.hk/b/arch/2020-07-07/src/224156532/15940650663840.png')
            games[ctx.guild.id].embed.add_field(name="Количество участников: ", value=str(len(games[ctx.guild.id].players)), inline=True)
            games[ctx.guild.id].embed.add_field(name='Список участников',
                            value=','.join([str(elem.mention) for elem in games[ctx.guild.id].players]), inline=False)
            await ctx.send(embed=games[ctx.guild.id].embed)

    g = ctx.message.guild.id


# функция для того чтобы покинуть игру
@bot.command()
async def leave(ctx):
    # условие для проверки участвует ли игрок в некст игре
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

    await t_rand(ctx) #создается словарь d
    await roles(ctx)  # выдача ролей
    # РАСКОМЕНТИТЬ
    await game(ctx)
    if len(games[ctx.guild.id].p_pl)!=0:
        await golosovanie(ctx)
    # await playSound(ctx, _source=sounds[0])


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

    f = 0
    m_count = len(games[ctx.guild.id].players) / 3
    round(m_count)
    while f < m_count:
        jke = random.randint(0, len(games[ctx.guild.id].players) - 1)
        user = bot.get_user(games[ctx.guild.id].players[jke].id)
        if user in games[ctx.guild.id].maf:
            f -= 1
        else:
            games[ctx.guild.id].maf.append(user)
        f += 1
    # maf.sort()

    games[ctx.guild.id].don_random = random.choice(games[ctx.guild.id].maf)
    # user1 = bot.get_user(games[ctx.guild.id].players[don_random].id)
    await games[ctx.guild.id].don_random.send('Ваша роль - Дон.')

    # выдача роли полицая
    games[ctx.guild.id].acab_random = random.randint(0, len(games[ctx.guild.id].players) - 1)
    games[ctx.guild.id].sherif = bot.get_user(games[ctx.guild.id].players[games[ctx.guild.id].acab_random].id)
    while games[ctx.guild.id].sherif in games[ctx.guild.id].maf:
        games[ctx.guild.id].acab_random = random.randint(0, len(games[ctx.guild.id].players) - 1)
        games[ctx.guild.id].sherif = bot.get_user(games[ctx.guild.id].players[games[ctx.guild.id].acab_random].id)
        break

    # user2 = bot.get_user(games[ctx.guild.id].players[acab_random].id)
    await games[ctx.guild.id].sherif.send('Ваша роль - Комиссар.')

    # doctor_random = random.randint(0, len(games[ctx.guild.id].players) - 1)
    # while doctor_random in maf or doctor_random == acab_random:
    #     doctor_random = random.randint(0, len(games[ctx.guild.id].players) - 1)
    #     break
    #
    # user3 = bot.get_user(games[ctx.guild.id].players[doctor_random].id)
    # await user3.send('Ваша роль - Доктор.')

    j = 0
    for i in games[ctx.guild.id].players:
        if i == games[ctx.guild.id].maf[j]:
            if i == games[ctx.guild.id].don_random:
                continue
            else:
                # user = bot.get_user(games[ctx.guild.id].players[i].id)
                await i.send('Ваша роль - Мафия.')
                if j < len(games[ctx.guild.id].maf) - 1:
                    j += 1
        else:
            if i == games[ctx.guild.id].sherif: # or i == doctor_random:
                continue
            else:
                # user = bot.get_user(games[ctx.guild.id].players[i].id)
                await i.send('Ваша роль - Мирный житель.')
    # выдача роли дона


async def t_rand(ctx):
    for i in games[ctx.guild.id].players:
        jke = random.randint(1, len(games[ctx.guild.id].players))
        while jke in games[ctx.guild.id].d.keys():
            jke = random.randint(1, len(games[ctx.guild.id].players))
        games[ctx.guild.id].d.update({jke: i})
    games[ctx.guild.id].d_list = list(games[ctx.guild.id].d.keys())
    games[ctx.guild.id].d_list.sort()
    # for i in d_list:
    #     await channel_text.send(str(i) + " - " + str(d[i].mention))
    games[ctx.guild.id].embed1 = discord.Embed(
        title='Номера игроков',
        description="Игра начнется через 30 секунд",
        colour=discord.Colour.blue()
    )
    games[ctx.guild.id].embed1.set_footer(text='Хорошей игры')
    games[ctx.guild.id].embed1.set_image(url = 'https://2ch.hk/b/arch/2020-07-07/src/224156532/15940650663840.png')
    games[ctx.guild.id].embed1.add_field(name = 'Номера:', value = '\n'.join(
        [str(i) + " - " + str(games[ctx.guild.id].d[i].mention) for i in games[ctx.guild.id].d_list]),
                     inline=False)
    await channel_text.send(embed=games[ctx.guild.id].embed1)
    # print(d)


async def game(ctx):
    await channel_text.send("Игра началась!!!")

    for i in games[ctx.guild.id].d_list:

        choice = False

        await channel_text.send("Игрок " + str(i) + " - " + str(games[ctx.guild.id].d[
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
            elif msg.author != games[ctx.guild.id].d[i]:
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

    if len(games[ctx.guild.id].p_pl)==0:
        games[ctx.guild.id].embed_p = discord.Embed(
            title="На голосование не было выставлено ни одного игрока",
            colour=discord.Colour.blue()
        )
        games[ctx.guild.id].embed_p.set_footer(text='Хорошей игры')
        await channel_text.send(embed=games[ctx.guild.id].embed_p)
    else:
        games[ctx.guild.id].embed_p = discord.Embed(
            title="Выставленые игроки на голосование",
            description="Голосование проходит в порядке выстовления игроков",
            colour=discord.Colour.blue()
        )
        games[ctx.guild.id].embed_p.set_footer(text='Хорошей игры')
        # embed_p.set_image(url='https://2ch.hk/b/arch/2020-07-07/src/224156532/15940650663840.png')
        games[ctx.guild.id].embed_p.add_field(name='Номера:', value='\n'.join(
            [str(i) + " - " + str(games[ctx.guild.id].d[i].mention) for i in games[ctx.guild.id].p_pl]),
                          inline=False)
        await channel_text.send(embed=games[ctx.guild.id].embed_p)


# функция воспроизведения звуков
async def playSound(ctx, _source):
    voice.play(discord.FFmpegPCMAudio(executable="C:/ffmpeg/bin/ffmpeg.exe", source=_source))


# проверочная команда для воспроизведения
@bot.command()
async def ps(ctx):
    voice.play(discord.FFmpegPCMAudio(executable="C:/ffmpeg/bin/ffmpeg.exe", source=sounds[0]))


async def golosovanie(ctx):
    for i in range(len(games[ctx.guild.id].p_pl)):
        await channel_text.send("Игрок " + str(games[ctx.guild.id].p_pl[i]) + " - " + games[ctx.guild.id].d[
            games[ctx.guild.id].p_pl[i]].mention + ". Ваша минута!\n Оправдывайся")
        await asyncio.sleep(5)


    for i in range(len(games[ctx.guild.id].p_pl) - 1):
        await channel_text.send(
            'Голосуем за игрока ' + str(games[ctx.guild.id].p_pl[i]) + " - " + games[ctx.guild.id].d[
                games[ctx.guild.id].p_pl[i]].mention + ", если считаете, что он мафия, напишите плюсик")
        t_end = time.time() + 10
        counter = 0
        while time.time() < t_end:
            try:
                msg = await bot.wait_for('message', timeout=10.0)
                s = msg.content
                if s != '+':
                    await channel_text.send(str(msg.author.mention) + ", напишите плюсик")
                elif msg.author in games[ctx.guild.id].g_list:
                    await channel_text.send(str(msg.author.mention) + ", вы уже голосовали!!!")
                else:
                    games[ctx.guild.id].g_list.append(msg.author)
                    counter += 1
            except asyncio.TimeoutError:
                break

        await channel_text.send(
            'За исключение игрока ' + str(games[ctx.guild.id].p_pl[i]) + " - " + games[ctx.guild.id].d[
                games[ctx.guild.id].p_pl[i]].mention + 'проголосовало ' + str(counter) + ' человек(а)')
        games[ctx.guild.id].p_pl1.update({counter: games[ctx.guild.id].p_pl[i]})

    nonvoted = len(games[ctx.guild.id].d_list) - len(games[ctx.guild.id].g_list)  # не проголосовавшие
    games[ctx.guild.id].p_pl1.update({nonvoted: games[ctx.guild.id].p_pl[-1]})

    # берем ключи сортируем и по наибольшему ключу вычисляем кикнутого

    p = list(games[ctx.guild.id].p_pl1.keys())
    p.sort()
    # key - максимальное кло-во голосов
    key = p.pop()
    yo = games[ctx.guild.id].p_pl1[key]
    await channel_text.send('Игрок ' + games[ctx.guild.id].d[yo].mention + ' покидает игру')
    del games[ctx.guild.id].d[yo]


async def night(ctx):
    for i in games[ctx.guild.id].maf:
        await i.send(embed=games[ctx.ctx.guild.id].embed)
        await i.send("Отправьте номер игрока, которого хотите убить")
    await games[ctx.guild.id].sherif.send(embed=games[ctx.ctx.guild.id].embed)
    # try:
    #     msg = await bot.wait_for('message', timeout=20.0)
    # except asyncio.TimeoutError:



async def check(ctx, number):
    user = bot.get_user(games[ctx.guild.id].d_list[number].id)
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

    if number == games[ctx.guild.id].don_random:
        if s == games[ctx.guild.id].acab_random:
            await user.send("Роль игрока под номером" + s + "- Коммисар.")
        # elif s == doctor_random:
        #     await user.send("Роль игрока под номером" + s + "- Доктор.")
        else:
            await user.send("Роль игрока под номером" + s + "- Мирный житель.")

    if number == games[ctx.guild.id].acab_random:
        if s in games[ctx.guild.id].maf:
            await user.send("Роль игрока под номером" + s + "- Мафия.")
        elif s == games[ctx.guild.id].don_random:
            await user.send("Роль игрока под номером" + s + "- Дон.")
        else:
            await user.send("Роль игрока под номером" + s + "- Не мафия.")
    # если че тут маньяка добавить ещё


bot.run(TOKEN)  # запуск бота//
