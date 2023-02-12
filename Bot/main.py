import asyncio
import os
import discord
from discord.ext import commands
from help_cog import help_cog
from music_cog import music_cog



if __name__ == "__main__":
    bot = commands.Bot(command_prefix='!', intents=discord.Intents().all())
    bot.remove_command("help")
    bot.remove_command("play")

    #Função auxiliar da programação assonance
    async def on_ready():
        bot.add_cog(help_cog(bot))
        bot.add_cog(music_cog(bot))
    asyncio.run(on_ready())

    bot.run("SFASDASFSA")
