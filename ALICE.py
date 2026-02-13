import discord
from discord.ext import commands
from dotenv import load_dotenv

import logging
import os
import api_methods

def ALICE():
    #Necessary setup for discord.py
    load_dotenv()
    token = os.getenv('DISCORD_TOKEN')

    handler = logging.FileHandler(filename='./discord.log', encoding='utf-8', mode='w')
    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True

    bot = commands.Bot(command_prefix='!', intents=intents)
    role="Red"


    @bot.event
    async def on_ready():
        print(f"We are ready to go in, {bot.user.name}")

    @bot.event
    async def on_member_join(member):
        await member.send(f"{bot.user.name} acknowledged {member.name} joining!")    
    

    @bot.event
    async def on_message(message):
        #Don't reply to yourself
        if message.author == bot.user:
            return
        
        if "i hate alice" in message.content.lower():
            await message.delete()
            await message.channel.send(f"{message.author.mention}, that's mean :(")

        if "mustikkapiirakka" in message.content.lower():
            await message.channel.send(f"{message.author.mention} I need to eat Mustikkapiirakka with you {message.author.display_name} PLS PLS PLS PLS!!!1!!!!!!!!!!!")
        
        await bot.process_commands(message)

    @bot.command()
    async def sako(ctx):
        await ctx.send(f"Sako makes some pretty neat rifles {ctx.author.display_name}!")

    @bot.command()
    async def red(ctx):
        role_given = discord.utils.get(ctx.guild.roles, name=role)
        if role_given:
            await ctx.author.add_roles(role_given)
            await ctx.send(f"{ctx.author.display_name} is now given {role_given}")
        else:
            await ctx.send(f"Error: Role does not exist")

    @bot.command()
    async def redRemove(ctx):
        role_given = discord.utils.get(ctx.guild.roles, name=role)
        if role_given:
            await ctx.author.remove_roles(role_given)
            await ctx.send(f"{ctx.author.display_name} is now losing {role_given}")
        else:
            await ctx.send(f"Error: Role does not exist")

    @bot.command()
    async def dm(ctx, *, msg):
        await ctx.author.send(f"You said '{msg}'")

    @bot.command()
    async def reply(ctx):
        await ctx.reply("Replying to message")

    @bot.command()
    async def badapple(ctx):
        await ctx.send(file=discord.File("./BadApple.mp4", filename="BadApple.mp4"))#, embed=embed)

    #Access Randomfox API to display an image of a random fox
    @bot.command()
    async def fox(ctx):
        await api_methods.fox_api(ctx)
        
    #Access Safebooru's API and pull a random Furina image
    @bot.command()
    async def furina(ctx):
        await api_methods.furina_api(ctx)

    #Access Safebooru's API and pull a random Hu Tao image
    @bot.command()
    async def hutao(ctx):
        await api_methods.hu_tao_api(ctx)


    bot.run(token, log_handler=handler, log_level=logging.DEBUG)


if __name__ == "__main__":
    ALICE()