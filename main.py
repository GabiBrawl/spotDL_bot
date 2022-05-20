from http import client
from time import sleep
import discord
import os
import ctypes
from discord_slash import SlashCommand
from discord.ext import commands
from env import *
import random
from spotdl import Spotdl


bot = commands.Bot(command_prefix=PREFIX, description="A random bot doing nothing here.")
cp = "!!" #command prefix
ctypes.windll.kernel32.SetConsoleTitleW("Discord Bot logs&more")
slash = SlashCommand(bot, sync_commands=True)

@bot.event
async def on_ready():
    print('\n-------------------------- Logged in as {0.user} --------------------------\n\n'.format(bot))

@slash.slash(name="spotdl", description="Use spotDL within discord")
async def spotdl(ctx, songname, output:str):
    if not output in OFS:
        await ctx.send(f'<@{ctx.author.id}>' + ' spotDL only supports mp3, flac, opus, m4a, wav and ogg output formats.')
        return
    with open('songname.txt', 'w') as f:
        f.write('"' + songname + '"')
    with open('outputextension.txt', 'w') as f:
        f.write(output)
    await ctx.send('Processing request... One moment please...')
    print('\nSong Downloader Started...' + '\nTriggeredBy: ' + f'@{ctx.author}\n' + 'SongName: ' + songname + '\nSongOutput: ' + output)
    spotdl = Spotdl(client_id=SCID, client_secret=SCSECRET, output_format=output, save_file=output, overwrite='skip', print_errors=True)
    songs = spotdl.search(str(songname))
    spotdl.download_songs(songs)
    sns = output + songs
    await ctx.send(file=discord.File(sns))
    print(sns)
    print("Done!")
    return
    


@bot.command(pass_context=True)
@discord.ext.commands.has_any_role('Bot_Perms')
async def r(message):
    role = discord.utils.find(lambda r: r.name == 'Member', message.guild.roles)
    if role in message.author.roles:
            await message.channel.send('Resetting...')
            print('Reset Request accepted by ' + f'@{message.author}')
            os.system("python main.py")
            exit()
    else:
        print('Reset Request Refused. Sent by ' + f'@{message.author}\n')
        await message.channel.send(f'<@{message.author.id}>' + ', you are not authorized to run that command.')

    
@bot.command(pass_context=True)
async def clear(ctx, amount:str):
    if amount == 'all':
        await ctx.channel.purge()
    else:
        await ctx.channel.purge(limit=(int(amount) + 1))


@bot.command(pass_context=True)
async def h(ctx):
    print(f'\n@{ctx.author}' + " asked to show help." )
    embed = discord.Embed(
        name=ctx.author.display_name,
        icon_url=ctx.author.avatar_url,
        title="Gabiii Commands help",
        description="All available commands for Gabiii BOT",
        color=0xFF5733
    )
    embed.add_field(
        name="React to the last message in the channel with random emoji",
        value=" -If you use this command while replying to someone, the bot will react to the message you're replying to! \n\n " + PREFIX + "e [amount 1-20]\n",
        inline=False
        )
    embed.add_field(
        name="Shutdown bot",
        value="!!s",
        inline=True
        )
    embed.add_field(
        name="Reset bot, to apply changes",
        value="!!r",
        inline=True
        )
    msg = await ctx.send(embed=embed)

@bot.command(pass_context=True)
async def e(ctx, qtty:int=1, *arg):
    print(f'\n@{ctx.author}' + " asked for a random reaction." )
    await ctx.channel.purge(limit=(1)) #delete the command message
    reference = ctx.message.reference
    if qtty > 20:
        await ctx.channel.send('Maximum value is 20. You asked for ' + str(qtty))
        return
    if reference == None:
        for x in range(qtty):
            emoji = random.choice(EMOJI_LIST)
            async for ctx.message in ctx.channel.history(limit=(1)):
                await ctx.message.add_reaction( #add the reaction(s)
                    str(emoji)
                )
        channel = ctx.channel
        msg = await channel.fetch_message(ctx.message.id)
        print("Successfully reacted with " + str(qtty) + " emoji for " + f"@{ctx.author}")
        return
    else:
        channel = ctx.channel
        msg = await channel.fetch_message(ctx.message.id)
        for x in range(qtty):
            emoji = random.choice(EMOJI_LIST)
            await msg.add_reaction(
                str(emoji)
            )
        print("Successfully reacted with " + str(qtty) + " emoji for " + f"@{ctx.author}" + ", to message sent by " + f"@{msg.author.name}")
        return



@bot.command(pass_context=True)
async def roll_dice(message):
    dice = [1, 2, 3, 4, 5, 6]
    print(f'\n@{message.author}' + " asked to roll the dice." )
    dice_value = random.choice(dice)
    await message.channel.send('The dice gave you a: ' + str(dice_value))


@bot.command(pass_context=True)
@discord.ext.commands.has_any_role('Bot_Perms')
async def alive(ctx, msg:str=1):
    await ctx.channel.purge(limit=(1)) #delete the command message
    reference = ctx.message.reference
    if msg == 1:
        await ctx.channel.send('You have to type double quotes and insert your text in there after the command. (ie: !!alive "your text here")')
    role = discord.utils.find(lambda r: r.name == 'Member', ctx.guild.roles)
    if any(word in msg for word in BWFILTER):
        await ctx.channel.send(f"{ctx.author.mention}" + ", bad words aren't allowed in here ma boy/gurl")
        return
    else:
        if role in ctx.author.roles:
            if reference == None:
                print(f'\n@{ctx.author}' + " prompted me to print '" + msg + "'")
                await ctx.channel.send(msg)
            else:
                repl = await ctx.channel.fetch_message(ctx.message.reference.message_id)
                print(f'\n@{ctx.author}' + " prompted me to print '" + msg + "', while replying to " + f'@{repl.author}')
                await repl.reply(msg)
        else:
            print(f'\n@{ctx.author}' + " prompted me to print '" + msg + "', but the command got denied.")
            await ctx.channel.send("No, I'm not in the mood of saying that. (:")


bot.run(TOKEN, bot=True, reconnect=True)
