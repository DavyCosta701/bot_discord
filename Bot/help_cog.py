from multiprocessing.connection import Client

import discord
from discord.ext import commands

class help_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.help_message = """
        
        Comandos
        !help - Mostra ajuda 
        !p <Musica> - Toca a música atual. Aliases = play
        !pause - Pausa o player, volta a tocar se o player estiver pausado
        !re - Volta a tocar a música
        !skip - Dá skip na música
        !blackrose - Para a música e limpa a queue. Aliases = br
        !leave - Manda o bot pastar
        
        """

        self.text_channel_text = []

    @commands.Cog.listener()
    async def on_ready(self):
        for guild in self.bot.guilds:
            for channel in guild.text_channels:
                self.text_channel_text.append(channel)

    async def send_to_all(self, msg):
        for text_channel in self.text_channel_text:
            await text_channel.send(msg)

    @commands.command(name= "help", help= "Ajuda")
    async def help(self, ctx):
        await ctx.send(self.help_message)






