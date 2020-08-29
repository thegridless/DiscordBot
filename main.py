# Discord Bot # MAFIA
import discord
import random
import asyncio
import time
import ffmpeg
from discord.ext import commands  # подгрузка библиотек
from discord.utils import get
import collections
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
        self.embed3 = 0
        self.embed_p = 0
        self.acab_random = 0
        self.don_random = 0
        self.sherif = 0
        self.mafia_kill = {} #{маф или дон: номер игрока кот хочет убить}
        self.kill = 0 #номер игрока, кот убивают
        self.m_kills = [] #вспомогательный массив
        self.s_check = 0 #номер проверяемого игрока шерифом
        self.d_check = 0 #номер проверяемого игрока доном
        self.pm = [] #массив мафии, где хранятся мафии кот написали кого убить
        self.max_g = 0 #максимальное кол-во голосов за одного игрока
        self.ravg = False
        self.dopravg = False
        self.channel_text = 0 #текстовый канал
        self.channel_voice = 0#Голосовой канал
        self.f = 0 # счетчик
        self.m_count = 0 #кол-во мафии
        self.jke = 0 #рандом
        self.t_end = 0
        self.counter = 0
        self.nonvoted = 0 #оставшиеся голоса
        self.i = 0
        self.pmcheck = False
        self.embednight = 0 #embed отправляемый ночью активным ролям
        self.n = 0 #ещё одна рандомная переменная
        self.d_sort = []
        self.key = 0
        self.value = 0
        self.msg = 0
        self.item = 0
        self.count = 0
        self.pause = False
        self.mode = 1
        self.embedmode = 0
        self.doc_random = 0
        self.doc = 0
        self.d_h = 0
        self.dochill = False

@bot.event
async def on_guild_join(guild):
    category = guild.categories[0]
    channel = category.channels[0]
    await channel.send("Привет я МафияБот.\nМой префикс - !\nВы можете посмотреть список команд, написав !help")
    # await g.text_channels[0].send("Привет я МафияБот.\nМой префикс - !\nВы можете посмотреть список команд, написав !help")


@bot.command(pass_context=True)
async def pause(ctx):
    # games[ctx.guild.id].pause = True
    await ctx.send("Для снятия паузы напишите !unpause")
    while True:
        games[ctx.guild.id].msg = await bot.wait_for('message')
        # if games[ctx.guild.id].msg.author in games[ctx.guild.id].players:
        if games[ctx.guild.id].msg.content=="unpause" or games[ctx.guild.id].msg.content=="!unpause":
            break


@bot.command(pass_context=True)
async def mode(ctx):
    games[ctx.guild.id].embedmode = discord.Embed(
        title='Режимы игры',
        description='Текущий режим ' + str(games[ctx.guild.id].mode),
        colour=discord.Colour.blue()
    )
    games[ctx.guild.id].embedmode.add_field(name="1", value="Шериф",inline=True)
    games[ctx.guild.id].embedmode.add_field(name="2", value="Шериф + Доктор",inline=False)
    await ctx.send(embed=games[ctx.guild.id].embedmode)
    await ctx.send("Напишите номер режима, который хотите выбрать")
    games[ctx.guild.id].msg = await bot.wait_for('message')
    if  games[ctx.guild.id].msg.content=='1':
        games[ctx.guild.id].mode = 1
        await ctx.send("Вы выбрали первый режим")
    elif games[ctx.guild.id].msg.content=='2':
        games[ctx.guild.id].mode = 1
        await ctx.send("Вы выбрали второй режим")



@bot.command(pass_context=True)  # разрешаем передавать агрументы
async def play(ctx):  # функция для !play
    if ctx.guild==None:
        await ctx.send("Отправляйте сообщения в текстовые каналы сервера")
    else:
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
                games[ctx.guild.id].embed.set_image(url='https://sun9-8.userapi.com/2iogxkZ27p6BBF7F3x03OnAlEL7aMnLcZfwwRA/_C7vA75DVAE.jpg')
                games[ctx.guild.id].embed.add_field(name="Лидер лобби",value=str(games[ctx.guild.id].players[0].mention))
                games[ctx.guild.id].embed.add_field(name="Количество участников: ", value=str(len(games[ctx.guild.id].players)), inline=True)
                games[ctx.guild.id].embed.add_field(name='Список участников',
                                value=','.join([str(games[ctx.guild.id].i.mention) for games[ctx.guild.id].i in games[ctx.guild.id].players]), inline=False)
                await ctx.send(embed=games[ctx.guild.id].embed)



# функция для того чтобы покинуть игру
@bot.command()
async def leave(ctx):
    # условие для проверки участвует ли игрок в некст игре
    if ctx.author in games[ctx.guild.id].players:
        games[ctx.guild.id].players.remove(ctx.author)
        await ctx.send(str(ctx.author.mention) + ", вы покинули следующую игру")
    else:
        await ctx.send(str(ctx.author.mention) + ", вы не участвуете в следующей игре")


@bot.command()  # правила игры
async def rules(ctx):
    await ctx.send('Правила игры в Мафию: https://www.eventnn.ru/articles/item/68/1029/')


# берем из списка в зависимости от количества m_count челов и отдаем им роль мафии а остальным даем мирных
@bot.command()  # начало игры
async def start(ctx):
    if ctx.guild==None:
        await ctx.send("Отправляйте сообщения в текстовые каналы сервера")
    elif len(games[ctx.guild.id].players)<4:
        await ctx.send("Недостаточно игроков")
    else:
        if ctx.message.author == games[ctx.guild.id].players[0]:
            # не забыть раскоментить
            guild = ctx.message.guild
            games[ctx.guild.id].channel_voice = await guild.create_voice_channel('Мафиозники')
            games[ctx.guild.id].channel_text = await guild.create_text_channel('Мафиозники')
            # # подключение бота к каналу
            # global voice
            #
            # voice = get(bot.voice_clients, guild=ctx.guild)
            #
            # if voice and voice.is_connected():
            #     await voice.move_to(games[ctx.guild.id].channel_voice)
            # else:
            #     voice = await games[ctx.guild.id].channel_voice.connect()
            #
            # # if voice and voice.is_connected():
            # #     await voice.move_to(channel_voice)
            # # else:
            # #     voice = await channel_voice.connect()

            # перемещение юзеров
            for games[ctx.guild.id].i in games[ctx.guild.id].players:
                await games[ctx.guild.id].i.move_to(games[ctx.guild.id].channel_voice)
                await games[ctx.guild.id].i.edit(mute=True)

            await t_rand(ctx) #создается словарь d
            await roles(ctx)  # выдача ролей

            while games[ctx.guild.id].end_of_game==False:
                await game(ctx)
                if len(games[ctx.guild.id].p_pl)!=0 and len(games[ctx.guild.id].p_pl)!=1:
                    await golosovanie(ctx)
                await night(ctx)

            await games[ctx.guild.id].channel_text.send(file=discord.File('igraz.jpg'))
            if len(games[ctx.guild.id].maf)==0:
                await games[ctx.guild.id].channel_text.send("Игра закончена победой мирный!!!")
                await games[ctx.guild.id].channel_text.send(file=discord.File('mirp.jpg'))
            else:
                await games[ctx.guild.id].channel_text.send("Игра закончена победой мафии!!!")
                await games[ctx.guild.id].channel_text.send(file=discord.File('mafp.jpg'))
            await games[ctx.guild.id].channel_text.send("Через 10 секунд каналы удалятся")
            await asyncio.sleep(10)
            await stop(ctx)
            del games[ctx.guild.id]
        else:
            await ctx.send("Только лидер лобби может начать игру")


async def stop(ctx):  # функция для удаления каналов
    # await asyncio.sleep(5)
    await games[ctx.guild.id].channel_voice.delete()
    await games[ctx.guild.id].channel_text.delete()


# @bot.command()
# async def left(ctx):  # функция для выхода из voice канала
#     c = ctx.message.author.voice.channel
# #     voice = get(bot.voice_clients, guild=ctx.guild)
# #     if voice and voice.is_connected():
# #         await voice.disconnect()


async def roles(ctx):  # рабочая отправляет в лс кто ты есть на самом деле

    games[ctx.guild.id].m_count = len(games[ctx.guild.id].players) / 2.5
    games[ctx.guild.id].m_count = round(games[ctx.guild.id].m_count)
    while games[ctx.guild.id].f < games[ctx.guild.id].m_count:
        games[ctx.guild.id].jke = random.randint(0, len(games[ctx.guild.id].players) - 1)
        games[ctx.guild.id].i = bot.get_user(games[ctx.guild.id].players[games[ctx.guild.id].jke].id)
        if games[ctx.guild.id].i in games[ctx.guild.id].maf:
            games[ctx.guild.id].f -= 1
        else:
            games[ctx.guild.id].maf.append(games[ctx.guild.id].i)
        games[ctx.guild.id].f += 1
    # maf.sort()
    games[ctx.guild.id].don_random = random.choice(games[ctx.guild.id].maf)
    # user1 = bot.get_user(games[ctx.guild.id].players[don_random].id)
    await games[ctx.guild.id].don_random.send('Ваша роль - Дон.')


    # выдача роли шерифа
    games[ctx.guild.id].acab_random = random.randint(0, len(games[ctx.guild.id].players) - 1)
    games[ctx.guild.id].sherif = bot.get_user(games[ctx.guild.id].players[games[ctx.guild.id].acab_random].id)
    while games[ctx.guild.id].sherif in games[ctx.guild.id].maf:
        games[ctx.guild.id].acab_random = random.randint(0, len(games[ctx.guild.id].players) - 1)
        games[ctx.guild.id].sherif = bot.get_user(games[ctx.guild.id].players[games[ctx.guild.id].acab_random].id)


    await games[ctx.guild.id].sherif.send('Ваша роль - Комиссар.')

    # выдача роли доктора
    if games[ctx.guild.id].mode==2:
        games[ctx.guild.id].doc_random = random.randint(0, len(games[ctx.guild.id].players) - 1)
        games[ctx.guild.id].doc = bot.get_user(games[ctx.guild.id].players[games[ctx.guild.id].doc_random].id)
        while games[ctx.guild.id].doc in games[ctx.guild.id].maf and games[ctx.guild.id].doc!=games[ctx.guild.id].sherif:
            games[ctx.guild.id].doc_random = random.randint(0, len(games[ctx.guild.id].players) - 1)
            games[ctx.guild.id].doc = bot.get_user(games[ctx.guild.id].players[games[ctx.guild.id].doc_random].id)

        await games[ctx.guild.id].doc.send('Ваша роль - Доктор.')

    for games[ctx.guild.id].i in games[ctx.guild.id].players:
        if games[ctx.guild.id].i in games[ctx.guild.id].maf:
            if games[ctx.guild.id].i == games[ctx.guild.id].don_random:
                continue
            else:
                await games[ctx.guild.id].i.send('Ваша роль - Мафия.')
        else:
            if games[ctx.guild.id].i == games[ctx.guild.id].sherif: # or i == doctor_random:
                continue
            else:
                # user = bot.get_user(games[ctx.guild.id].players[i].id)
                await games[ctx.guild.id].i.send('Ваша роль - Мирный житель.')

    # список всей мафии
    games[ctx.guild.id].embed3 = discord.Embed(
        colour=discord.Colour.red()
    )
    games[ctx.guild.id].embed3.add_field(name="Дон:", value=games[ctx.guild.id].don_random.mention)
    games[ctx.guild.id].embed3.add_field(name='Список участников, играющих за мафию:\n',
                                         value=','.join([str(games[ctx.guild.id].i.mention) for games[ctx.guild.id].i in
                                                         games[ctx.guild.id].maf]),
                                         inline=False)
    for games[ctx.guild.id].i in games[ctx.guild.id].maf:

        await games[ctx.guild.id].i.send(embed=games[ctx.guild.id].embed3)

        # if games[ctx.guild.id].i == games[ctx.guild.id].don_random:
        #     await games[ctx.guild.id].i.send(embed=games[ctx.guild.id].embed3)
        # else:
        #     await games[ctx.guild.id].i.send(embed=games[ctx.guild.id].embed3)
        #     await games[ctx.guild.id].i.send("Игрок " + games[ctx.guild.id].don_random.mention + " играет роль Дона.")






async def t_rand(ctx):
    for games[ctx.guild.id].i in games[ctx.guild.id].players:
        games[ctx.guild.id].jke = random.randint(1, len(games[ctx.guild.id].players))
        while games[ctx.guild.id].jke in games[ctx.guild.id].d.keys():
            games[ctx.guild.id].jke = random.randint(1, len(games[ctx.guild.id].players))
        games[ctx.guild.id].d.update({games[ctx.guild.id].jke: games[ctx.guild.id].i})
    games[ctx.guild.id].d_list = list(games[ctx.guild.id].d.keys())
    games[ctx.guild.id].d_list.sort()
    games[ctx.guild.id].d_sort = list(games[ctx.guild.id].d.keys())
    games[ctx.guild.id].d_sort.sort()
    # for i in d_list:
    #     await channel_text.send(str(i) + " - " + str(d[i].mention))
    # print(d)


async def game(ctx):

    games[ctx.guild.id].g_list = []
    games[ctx.guild.id].p_pl = []

    if len(games[ctx.guild.id].d_list)-len(games[ctx.guild.id].maf)<=len(games[ctx.guild.id].maf) or len(games[ctx.guild.id].maf)==0:
        games[ctx.guild.id].end_of_game=True
    else:
        games[ctx.guild.id].embed1 = discord.Embed(
            title='Номера игроков',
            description="Игра начнется через 30 секунд",
            colour=discord.Colour.blue()
        )
        games[ctx.guild.id].embed1.set_footer(text='Хорошей игры')
        games[ctx.guild.id].embed1.set_image(url='https://sun9-42.userapi.com/qZnD6a3I1utr_oFnA4JqsRvR1_BRpXEqvZtNiQ/vq_6YNzaXfA.jpg')
        games[ctx.guild.id].embed1.add_field(name='Номера:', value='\n'.join(
            [str(games[ctx.guild.id].i) + " - " + str(games[ctx.guild.id].d[games[ctx.guild.id].i].mention) for
             games[ctx.guild.id].i in games[ctx.guild.id].d_sort]),
                                             inline=False)
        await games[ctx.guild.id].channel_text.send(embed=games[ctx.guild.id].embed1)
        await games[ctx.guild.id].channel_text.send("Начинается день.")
        for games[ctx.guild.id].i in games[ctx.guild.id].d_list:

            choice = False

            await games[ctx.guild.id].channel_text.send("Игрок " + str(games[ctx.guild.id].i) + " - " + str(games[ctx.guild.id].d[games[ctx.guild.id].i].mention) + ". Ваша минута!\nЕсли вы хотите выставить игрока на голосование напишите его номер в данный чат.")
            await games[ctx.guild.id].d[games[ctx.guild.id].i].edit(mute=False)
            games[ctx.guild.id].t_end = time.time() + 10
            while time.time() < games[ctx.guild.id].t_end:
                try:
                    games[ctx.guild.id].msg = await bot.wait_for('message', timeout=10.0)
                except asyncio.TimeoutError:
                    break

                if games[ctx.guild.id].msg.content.isdigit() == False:
                    await games[ctx.guild.id].channel_text.send("Напишите существующий номер")
                elif games[ctx.guild.id].msg.author != games[ctx.guild.id].d[games[ctx.guild.id].i]:
                    await games[ctx.guild.id].channel_text.send(str(games[ctx.guild.id].msg.author.mention) + ", сейчас не ваша минута")
                elif int(games[ctx.guild.id].msg.content) <= len(games[ctx.guild.id].players) and int(games[ctx.guild.id].msg.content) > 0 and games[ctx.guild.id].msg.channel == games[ctx.guild.id].channel_text:
                    if (int(games[ctx.guild.id].msg.content) in games[ctx.guild.id].p_pl):
                        await games[ctx.guild.id].channel_text.send("Этот игрок уже выставлен")
                    else:
                        await games[ctx.guild.id].channel_text.send("Вы выставили игрока " + str(games[ctx.guild.id].msg.content) + " на голосование!")
                        if choice == False:
                            games[ctx.guild.id].p_pl.append(int(games[ctx.guild.id].msg.content))
                            choice = True
                        else:
                            games[ctx.guild.id].p_pl.pop()
                            games[ctx.guild.id].p_pl.append(int(games[ctx.guild.id].msg.content))

                else:
                    await games[ctx.guild.id].channel_text.send("Напишите существующий номер")

            await games[ctx.guild.id].d[games[ctx.guild.id].i].edit(mute=True)
        if len(games[ctx.guild.id].p_pl)==0:
            games[ctx.guild.id].embed_p = discord.Embed(
                title="На голосование не было выставлено ни одного игрока",
                colour=discord.Colour.blue()
            )
            games[ctx.guild.id].embed_p.set_footer(text='Хорошей игры')
            await games[ctx.guild.id].channel_text.send(embed=games[ctx.guild.id].embed_p)
        elif len(games[ctx.guild.id].p_pl)==1:
            await games[ctx.guild.id].channel_text.send("На голосование выставлен один игрок.\nГолосование не проводится")
        else:
            games[ctx.guild.id].embed_p = discord.Embed(
                title="Выставленые игроки на голосование",
                description="Голосование проходит в порядке выставления игроков",
                colour=discord.Colour.blue()
            )
            games[ctx.guild.id].embed_p.set_footer(text='Хорошей игры')
            games[ctx.guild.id].embed_p.set_image(url='https://sun9-32.userapi.com/J2G-yCllpa0zB8FA5XM4VeB_ASxo8R_DdqRb_A/g7osq1fmND4.jpg')
            games[ctx.guild.id].embed_p.add_field(name='Номера:', value='\n'.join(
                [str(games[ctx.guild.id].i) + " - " + str(games[ctx.guild.id].d[int(games[ctx.guild.id].i)].mention) for games[ctx.guild.id].i in games[ctx.guild.id].p_pl]),
                              inline=False)
            await games[ctx.guild.id].channel_text.send(embed=games[ctx.guild.id].embed_p)

    games[ctx.guild.id].n = games[ctx.guild.id].d_list.pop(0)
    games[ctx.guild.id].d_list.append(games[ctx.guild.id].n)

# функция воспроизведения звуков
# async def playSound(ctx, _source):
#     voice.play(discord.FFmpegPCMAudio(executable="C:/ffmpeg/bin/ffmpeg.exe", source=_source))


# проверочная команда для воспроизведения
# @bot.command()
# async def ps(ctx):
#     voice.play(discord.FFmpegPCMAudio(executable="C:/ffmpeg/bin/ffmpeg.exe", source=sounds[0]))


async def golosovanie(ctx):
    if games[ctx.guild.id].end_of_game==True:
        pass
    else:
        print(games[ctx.guild.id].p_pl)
        while games[ctx.guild.id].ravg==False:
            for games[ctx.guild.id].i in range(len(games[ctx.guild.id].p_pl)):
                await games[ctx.guild.id].channel_text.send("Игрок " + str(games[ctx.guild.id].p_pl[games[ctx.guild.id].i]) + " - " + games[ctx.guild.id].d[
                    games[ctx.guild.id].p_pl[games[ctx.guild.id].i]].mention + ". Ваша минута!\n Оправдывайся")
                await games[ctx.guild.id].d[games[ctx.guild.id].p_pl[games[ctx.guild.id].i]].edit(mute=False)
                games[ctx.guild.id].t_end = time.time() + 10
                while time.time() < games[ctx.guild.id].t_end:
                    pass
                await games[ctx.guild.id].d[games[ctx.guild.id].p_pl[games[ctx.guild.id].i]].edit(mute=True)


            for games[ctx.guild.id].i in range(len(games[ctx.guild.id].p_pl) - 1):
                await games[ctx.guild.id].channel_text.send(
                    'Голосуем за игрока ' + str(games[ctx.guild.id].p_pl[games[ctx.guild.id].i]) + " - " + games[ctx.guild.id].d[
                        games[ctx.guild.id].p_pl[games[ctx.guild.id].i]].mention + ", если считаете, что он мафия, напишите плюсик")
                games[ctx.guild.id].t_end = time.time() + 10
                while time.time() < games[ctx.guild.id].t_end:
                    try:
                        games[ctx.guild.id].msg  = await bot.wait_for('message', timeout=10.0)
                        if games[ctx.guild.id].msg.author in games[ctx.guild.id].d.values():
                            if games[ctx.guild.id].msg.content  != '+':
                                await games[ctx.guild.id].channel_text.send(str(games[ctx.guild.id].msg.author.mention) + ", напишите плюсик")
                            elif games[ctx.guild.id].msg.author in games[ctx.guild.id].g_list:
                                await games[ctx.guild.id].channel_text.send(str(games[ctx.guild.id].msg.author.mention) + ", вы уже голосовали!!!")
                            else:
                                games[ctx.guild.id].g_list.append(games[ctx.guild.id].msg.author)
                                games[ctx.guild.id].counter += 1
                        elif games[ctx.guild.id].msg.author == "MafiaBot#0059":
                            pass
                        else:
                            await ctx.send("Вы не участвуете в этой игре")
                    except asyncio.TimeoutError:
                        break

                await games[ctx.guild.id].channel_text.send(
                    'За исключение игрока ' + str(games[ctx.guild.id].p_pl[games[ctx.guild.id].i]) + " - " + games[ctx.guild.id].d[
                        games[ctx.guild.id].p_pl[games[ctx.guild.id].i]].mention + 'проголосовало ' + str(games[ctx.guild.id].counter) + ' человек(а)')
                games[ctx.guild.id].p_pl1.update({games[ctx.guild.id].p_pl[games[ctx.guild.id].i]:games[ctx.guild.id].counter })

            games[ctx.guild.id].nonvoted = len(games[ctx.guild.id].d_list) - len(games[ctx.guild.id].g_list)  # не проголосовавшие
            games[ctx.guild.id].p_pl1.update({games[ctx.guild.id].p_pl[-1]: games[ctx.guild.id].nonvoted})

            # берем ключи сортируем и по наибольшему ключу вычисляем кикнутого

            games[ctx.guild.id].max_g = max(list(games[ctx.guild.id].p_pl1.values()))



            for games[ctx.guild.id].key,games[ctx.guild.id].value in games[ctx.guild.id].p_pl1.items():
                if  games[ctx.guild.id].max_g==games[ctx.guild.id].value:
                    games[ctx.guild.id].p_pl.append(games[ctx.guild.id].key)


            if len(games[ctx.guild.id].p_pl)>1:
                if games[ctx.guild.id].dopravg==True:
                    await games[ctx.guild.id].channel_text.send("Игру покидают два игрока")
                    for games[ctx.guild.id].i in games[ctx.guild.id].p_pl:
                        await games[ctx.guild.id].channel_text.send(
                            'Игрок ' + games[ctx.guild.id].d[games[ctx.guild.id].i].mention + ' покидает игру')
                        if games[ctx.guild.id].d[games[ctx.guild.id].i] in games[ctx.guild.id].maf:
                            games[ctx.guild.id].maf.remove(games[ctx.guild.id].d[games[ctx.guild.id].i])
                        del games[ctx.guild.id].d[games[ctx.guild.id].i]
                        if len(games[ctx.guild.id].d) - len(games[ctx.guild.id].maf) <= len(
                                games[ctx.guild.id].maf) or len(
                                games[ctx.guild.id].maf) == 0:
                            games[ctx.guild.id].end_of_game = True
                        games[ctx.guild.id].d_list.remove(games[ctx.guild.id].i)
                    break
                games[ctx.guild.id].dopravg=True
                await games[ctx.guild.id].channel_text.send("Переголосование")
            else:
                games[ctx.guild.id].ravg = True

        if(games[ctx.guild.id].dopravg!=True):
            await games[ctx.guild.id].channel_text.send(
                'Игрок ' + games[ctx.guild.id].d[games[ctx.guild.id].p_pl[0]].mention + ' покидает игру')
            #последняя минута игрока

            await games[ctx.guild.id].channel_text.send(games[ctx.guild.id].d[games[ctx.guild.id].p_pl[0]].mention + ", ваша последняя минута.")
            await games[ctx.guild.id].d[games[ctx.guild.id].p_pl[0]].edit(mute=False)
            games[ctx.guild.id].t_end = time.time() + 10
            while time.time() < games[ctx.guild.id].t_end:
                pass
            await games[ctx.guild.id].d[games[ctx.guild.id].p_pl[0]].edit(mute=True)


            if games[ctx.guild.id].d[games[ctx.guild.id].p_pl[0]] in games[ctx.guild.id].maf:
                games[ctx.guild.id].maf.remove(games[ctx.guild.id].d[games[ctx.guild.id].p_pl[0]])
            del games[ctx.guild.id].d[games[ctx.guild.id].p_pl[0]]
            if len(games[ctx.guild.id].d) - len(games[ctx.guild.id].maf) <= len(games[ctx.guild.id].maf) or len(
                    games[ctx.guild.id].maf) == 0:
                games[ctx.guild.id].end_of_game = True
            games[ctx.guild.id].d_list.remove(games[ctx.guild.id].p_pl[0])
            games[ctx.guild.id].d_sort.remove(games[ctx.guild.id].p_pl[0])




async def night(ctx):
    games[ctx.guild.id].p_pl = []
    games[ctx.guild.id].g_list = []
    games[ctx.guild.id].p_pl1 = {}
    if games[ctx.guild.id].end_of_game==True:
        pass
    else:

        games[ctx.guild.id].embednight = discord.Embed(
            title='Номера игроков',
            colour=discord.Colour.blue()
        )
        games[ctx.guild.id].embednight.set_footer(text='Хорошей игры')
        games[ctx.guild.id].embednight.set_image(url='https://2ch.hk/b/arch/2020-07-07/src/224156532/15940650663840.png')
        games[ctx.guild.id].embednight.add_field(name='Номера:', value='\n'.join(
            [str(games[ctx.guild.id].i) + " - " + str(games[ctx.guild.id].d[games[ctx.guild.id].i].mention) for
             games[ctx.guild.id].i in games[ctx.guild.id].d_sort]),
                                             inline=False)
        await games[ctx.guild.id].channel_text.send("Наступает ночь\nМафия и шериф получат сообщения в лс")
        await games[ctx.guild.id].channel_text.send(file=discord.File('zas.jpg'))

        #убийство мафии
        for games[ctx.guild.id].i in games[ctx.guild.id].maf:
            if games[ctx.guild.id].i in games[ctx.guild.id].d.values():
                await games[ctx.guild.id].i.send(file=discord.File('mafpr.jpg'))
                await games[ctx.guild.id].i.send(embed=games[ctx.guild.id].embednight)
                await games[ctx.guild.id].i.send("Отправьте номер игрока, которого хотите убить")

        #ждем сообщения от мафии

        # games[ctx.guild.id].t_end = time.time() + 15
        while games[ctx.guild.id].pmcheck==False:
            try:
                games[ctx.guild.id].msg = await bot.wait_for('message')
                if games[ctx.guild.id].msg.author not in games[ctx.guild.id].maf:
                    pass
                elif games[ctx.guild.id].msg.author not in games[ctx.guild.id].d.values():
                    await games[ctx.guild.id].msg.author.send("Вы мертвы")
                elif games[ctx.guild.id].msg.content.isdigit() == False:
                    await games[ctx.guild.id].msg.author.send("Напишите существующий номер")
                elif int(games[ctx.guild.id].msg.content) not in games[ctx.guild.id].d.keys():
                    await games[ctx.guild.id].msg.author.send("Напишите существующий номер")
                elif games[ctx.guild.id].msg.author in games[ctx.guild.id].pm:
                    await games[ctx.guild.id].msg.author.send("Вы уже сделали свой выбор")
                # проверяем кто отправил сообщение
                else:
                    games[ctx.guild.id].pm.append(games[ctx.guild.id].msg.author)
                    if games[ctx.guild.id].msg.author == games[ctx.guild.id].don_random:
                        games[ctx.guild.id].mafia_kill.update({games[ctx.guild.id].msg.author: games[ctx.guild.id].msg.content})
                        await games[ctx.guild.id].msg.author.send("Вы выбрали игрока под номером " + games[ctx.guild.id].msg.content)
                    else:
                        games[ctx.guild.id].mafia_kill.update({games[ctx.guild.id].msg.author: games[ctx.guild.id].msg.content})
                        await games[ctx.guild.id].msg.author.send("Вы выбрали игрока под номером " + games[ctx.guild.id].msg.content)
                if len(games[ctx.guild.id].pm) == len(games[ctx.guild.id].maf):
                    games[ctx.guild.id].pmcheck=True
            except asyncio.TimeoutError:
                for games[ctx.guild.id].i in games[ctx.guild.id].maf:
                    await games[ctx.guild.id].i.send("Ваше время закончилось")

        games[ctx.guild.id].pmcheck=False
        games[ctx.guild.id].m_kills = games[ctx.guild.id].mafia_kill.values()
        games[ctx.guild.id].m_kills = [games[ctx.guild.id].item for games[ctx.guild.id].item,games[ctx.guild.id].count in collections.Counter(games[ctx.guild.id].m_kills).items() if games[ctx.guild.id].count > 1]

        if len(games[ctx.guild.id].m_kills)==0 or len(games[ctx.guild.id].m_kills)==2:
            if games[ctx.guild.id].don_random in games[ctx.guild.id].d.values():
                games[ctx.guild.id].kill = games[ctx.guild.id].mafia_kill[games[ctx.guild.id].don_random]
            else:
                games[ctx.guild.id].kill = games[ctx.guild.id].mafia_kill[next(iter(games[ctx.guild.id].mafia_kill))]
        else:
            games[ctx.guild.id].kill = games[ctx.guild.id].m_kills[0]

        games[ctx.guild.id].pm = []
        games[ctx.guild.id].mafia_kill={}
        games[ctx.guild.id].m_kills = []
        for games[ctx.guild.id].i in games[ctx.guild.id].maf:
            if games[ctx.guild.id].i in games[ctx.guild.id].d.values():
                await games[ctx.guild.id].i.send(file=discord.File('mafz.jpg'))

        #проверка шерифа

        if games[ctx.guild.id].sherif not in games[ctx.guild.id].d.values():
            pass
        else:
            await games[ctx.guild.id].sherif.send(file=discord.File('shpr.jpg'))
            await games[ctx.guild.id].sherif.send(embed=games[ctx.guild.id].embednight)
            await games[ctx.guild.id].sherif.send("Отправьте номер игрока, которого хотите проверить")
            games[ctx.guild.id].t_end = time.time() + 15
            while games[ctx.guild.id].pmcheck==False:
                try:
                    games[ctx.guild.id].msg = await bot.wait_for('message', timeout=15.0)

                    if games[ctx.guild.id].msg.author!=games[ctx.guild.id].sherif:
                        pass
                    elif games[ctx.guild.id].msg.content.isdigit() == False:
                        await games[ctx.guild.id].msg.author.send("Напишите существующий номер")
                    elif int(games[ctx.guild.id].msg.content) not in games[ctx.guild.id].d.keys():
                        await games[ctx.guild.id].msg.author.send("Напишите существующий номер")
                    else:
                        games[ctx.guild.id].s_check = int(games[ctx.guild.id].msg.content)
                        games[ctx.guild.id].pmcheck = True

                        if games[ctx.guild.id].d[games[ctx.guild.id].s_check] in games[ctx.guild.id].maf:
                            await games[ctx.guild.id].sherif.send("Он мафия")
                            break
                        else:
                            await games[ctx.guild.id].sherif.send("Он не мафия")
                            break

                except asyncio.TimeoutError:
                    await games[ctx.guild.id].sherif.send("Ваше время закончилось")
            games[ctx.guild.id].pmcheck = False
            await games[ctx.guild.id].sherif.send(file=discord.File('shz.jpg'))
        #проверка дона
        if games[ctx.guild.id].don_random not in games[ctx.guild.id].d.values():
            pass
        else:
            await games[ctx.guild.id].don_random.send(file=discord.File('dpr.jpg'))
            await games[ctx.guild.id].don_random.send(embed=games[ctx.guild.id].embednight)
            await games[ctx.guild.id].don_random.send("Отправьте номер игрока, которого хотите проверить")


            games[ctx.guild.id].t_end = time.time() + 15
            while games[ctx.guild.id].pmcheck==False:
                try:

                    games[ctx.guild.id].msg = await bot.wait_for('message')

                    if games[ctx.guild.id].msg.author!=games[ctx.guild.id].don_random:
                        pass
                    if games[ctx.guild.id].msg.content.isdigit() == False:
                        await games[ctx.guild.id].don_random.send("Напишите существующий номер")
                    elif int(games[ctx.guild.id].msg.content) not in games[ctx.guild.id].d.keys():
                        await games[ctx.guild.id].don_random.send("Напишите существующий номер")
                    else:
                        games[ctx.guild.id].d_check = int(games[ctx.guild.id].msg.content)
                        games[ctx.guild.id].pmcheck = True
                        if games[ctx.guild.id].d[games[ctx.guild.id].d_check]==games[ctx.guild.id].sherif:
                            await games[ctx.guild.id].don_random.send("Он шериф")
                            break
                        else:
                            await games[ctx.guild.id].don_random.send("Он не шериф")
                            break

                except asyncio.TimeoutError:
                    await games[ctx.guild.id].don_random.send("Ваше время закончилось")

            games[ctx.guild.id].pmcheck = False
            await games[ctx.guild.id].don_random.send(file=discord.File('dz.jpg'))
            if games[ctx.guild.id].mode == 2:
            # хилл дока
                if games[ctx.guild.id].doс not in games[ctx.guild.id].d.values():
                    pass
                else:
                    await games[ctx.guild.id].doс.send(file=discord.File('docpr.jpg'))
                    await games[ctx.guild.id].doс.send(embed=games[ctx.guild.id].embednight)
                    await games[ctx.guild.id].doс.send("Отправьте номер игрока, которого хотите полечить")

                    games[ctx.guild.id].t_end = time.time() + 15
                    while games[ctx.guild.id].dochill == False:

                        games[ctx.guild.id].msg = await bot.wait_for('message')

                        if games[ctx.guild.id].msg.author != games[ctx.guild.id].doс:
                            pass
                        if games[ctx.guild.id].msg.content.isdigit() == False:
                            await games[ctx.guild.id].doс.send("Напишите существующий номер")
                        elif int(games[ctx.guild.id].msg.content) not in games[ctx.guild.id].d.keys():
                            await games[ctx.guild.id].doс.send("Напишите существующий номер")
                        else:
                            games[ctx.guild.id].d_h = int(games[ctx.guild.id].msg.content)
                            games[ctx.guild.id].dochill = True
                            if games[ctx.guild.id].d[games[ctx.guild.id].d_h] == games[ctx.guild.id].kill:
                                await games[ctx.guild.id].doс.send("Вы полечили игрока " + str(games[ctx.guild.id].d[games[ctx.guild.id].d_h]))

                    games[ctx.guild.id].dochill = False
                    await games[ctx.guild.id].doc.send(file=discord.File('docz.jpg'))
        #убираем убитого из игры

        if games[ctx.guild.id].mode == 2:
            if games[ctx.guild.id].d[games[ctx.guild.id].d_check] == games[ctx.guild.id].kill:
                await games[ctx.guild.id].channel_text.send("Начинается новый день\nВсе живы")
            else:
                await games[ctx.guild.id].channel_text.send("Начинается новый день\nИгрок " + str(
                    games[ctx.guild.id].d[int(games[ctx.guild.id].kill)].mention) + " был убит")
                # last minute of chelik

                await games[ctx.guild.id].channel_text.send(
                    games[ctx.guild.id].d[int(games[ctx.guild.id].kill)].mention + ", ваша последняя минута.")
                await games[ctx.guild.id].d[int(games[ctx.guild.id].kill)].edit(mute=False)
                games[ctx.guild.id].t_end = time.time() + 10
                while time.time() < games[ctx.guild.id].t_end:
                    pass
                await games[ctx.guild.id].d[int(games[ctx.guild.id].kill)].edit(mute=True)

                if games[ctx.guild.id].d[int(games[ctx.guild.id].kill)] in games[ctx.guild.id].maf:
                    games[ctx.guild.id].maf.remove(games[ctx.guild.id].d[int(games[ctx.guild.id].kill)])

                del games[ctx.guild.id].d[int(games[ctx.guild.id].kill)]
                games[ctx.guild.id].d_list.remove(int(games[ctx.guild.id].kill))
                games[ctx.guild.id].d_sort.remove(int(games[ctx.guild.id].kill))
        else:
            await games[ctx.guild.id].channel_text.send("Начинается новый день\nИгрок " + str(games[ctx.guild.id].d[int(games[ctx.guild.id].kill)].mention) + " был убит" )
            #last minute of chelik

            await games[ctx.guild.id].channel_text.send(games[ctx.guild.id].d[int(games[ctx.guild.id].kill)].mention + ", ваша последняя минута.")
            await games[ctx.guild.id].d[int(games[ctx.guild.id].kill)].edit(mute=False)
            games[ctx.guild.id].t_end = time.time() + 10
            while time.time() < games[ctx.guild.id].t_end:
                pass
            await games[ctx.guild.id].d[int(games[ctx.guild.id].kill)].edit(mute=True)


            if games[ctx.guild.id].d[int(games[ctx.guild.id].kill)] in games[ctx.guild.id].maf:
                games[ctx.guild.id].maf.remove(games[ctx.guild.id].d[int(games[ctx.guild.id].kill)])

            del games[ctx.guild.id].d[int(games[ctx.guild.id].kill)]
            games[ctx.guild.id].d_list.remove(int(games[ctx.guild.id].kill))
            games[ctx.guild.id].d_sort.remove(int(games[ctx.guild.id].kill))




bot.run(TOKEN)  # запуск бота//
