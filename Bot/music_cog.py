import discord
import nextcord as nextcord
from discord import client
from discord.ext import commands
from unicodedata import name
from youtube_dl import YoutubeDL



class music_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.isplaying = False
        self.ispausing = True

        self.music_queue = []
        self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                               'options': '-vn'}

        self.vc = None

    #Funcão de busca do programa
    def search(self, item):

        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            try:
                info = ydl.extract_info("ytsearch:%s" % item, download=False)['entries'][0]

            except Exception:
                return False

        return {'source': info['formats'][0]['url'], 'title': info['title']}

    def playnext(self):

        if len(self.music_queue) > 0:
            self.isplaying = True
            m_url = self.music_queue[0][0]['source']

            self.music_queue.pop(0)
            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.playnext())
        else:
            self.isplaying = False

    async def playmusic(self, ctx):
        if len(self.music_queue) > 0:
            self.isplaying = True
            m_url = self.music_queue[0][0]['source']

            if self.vc is None or not self.vc.is_connected():
                self.vc = await self.music_queue[0][1].connect()

                if self.vc is None:
                    await ctx.send("Não pude me conectar ao voice channel Kuwata tsuno wovalai")
                    return
                else:
                    await self.vc.move_to(self.music_queue[0][1])

                self.music_queue.pop(0)
                self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.playnext())

        else:
            self.isplaying = True

    @commands.command(name='play', help='Tells the bot to join the voice channel')
    async def play(self, ctx, *args):
        query = "".join(args)
        voice_channel = ctx.author.voice.channel

        if voice_channel is None:
            await ctx.send("Conecte-se em um canal de voz.")

        else:
            song = self.search(query)
            if type(song) == type(True):
                await ctx.send("Could not download the song.")

            else:
                await ctx.send("Música adicionada. Eu sei que...")
                self.music_queue.append([song, voice_channel])

                if self.isplaying is False:
                    await self.playmusic(ctx)
        self.bot.add_command(self.play)


    @commands.command(name="pause", help="Pausa o som tocado.")
    async def pause(self, ctx, *args):
        if self.isplaying:
            self.isplaying = False
            self.ispausing = True
            self.vc.pause()

        elif self.ispausing:
            self.isplaying = True
            self.ispausing = False
            self.vc.resume()

    @commands.command(name="resume", aliases=["re"], help="Volta a tocar a música")
    async def resume(self, ctx, *args):
        if self.ispausing:
            self.isplaying = True
            self.ispausing = False
            self.vc.resume()

    @commands.command(name="skip", aliases=["s"], help="Skipa o som atual")
    async def skip(self, ctx, *args):
        if self.vc is not None and self.vc:
            self.vc.stop()
            await self.playmusic(ctx)

    @commands.command(name="queue", aliases=["q"], help="Mostra a queue")
    async def queue(self, ctx, *args):
        retval = ""

        for i in range(0, len(self.music_queue)):
            if i > 4: break
            retval += self.music_queue[i][0]['title'] + "/n"

        if retval != "":
            await ctx.send(retval)

        else:
            await ctx.send("Sem música na queie")

    @commands.command(name="blackrose", aliases=["br"], help="Limpa a queue e desconecta o bot (até chamar ele dnv)")
    async def blackrose(self, ctx, *args):

        if self.vc is not None and self.isplaying:
            self.vc.stop()
        self.music_queue = []
        await ctx.send("Queue Limpa")

    @commands.command(name="leave", aliases=["disconnect", "l", "disc"], help="Desconecta o bot")
    async def leave(self, ctx):
        self.isplaying = False
        self.ispausing = False
        await self.vc.disconnect()




