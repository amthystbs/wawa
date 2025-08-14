import discord
from discord.ext import commands
from discord import option
from dotenv import load_dotenv
import os
import json

load_dotenv()
token = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.all()
bot = commands.Bot(intents=intents)

file = open("wawa_data.json", "a")
file.close()

with open("wawa_data.json", "r+") as file:
    if not file.read(1):
        file.write("{}")

with open('wawa_data.json', 'r') as wawa_file:
    wawa_data = json.load(wawa_file)

def update_wawa_file(data):
    with open("wawa_data.json", "w") as wawa_data_file:
        wawa_data_file.write(json.dumps(data))

def update_data(channel_data):
    if not "nextWawa" in channel_data:
        channel_data["nextWawa"] = "a"

    if not "nextLetter" in channel_data:
        channel_data["nextLetter"] = "w"

    if not "last_user" in channel_data:
        channel_data["last_user"] = None

    if not "chain_length" in channel_data:
        channel_data["chain_length"] = 0

    if not "record" in channel_data:
        channel_data["record"] = 0

    if not "record_breaker" in channel_data:
        channel_data["record_breaker"] = None

    if not "correct_reaction" in channel_data:
        channel_data["correct_reaction"] = "✅"

    if not "new_record_reaction" in channel_data:
        channel_data["new_record_reaction"] = "🎉"

    if not "10_reaction" in channel_data:
        channel_data["10_reaction"] = "🔟"

    if not "100_reaction" in channel_data:
        channel_data["100_reaction"] = "💯"

    if not "wrong_reaction" in channel_data:
        channel_data["wrong_reaction"] = "❌"

    if not "wait_reaction" in channel_data:
        channel_data["wait_reaction"] = "⚠️"

@bot.event
async def on_message(message):
    global wawa_data

    if message.content == "":
        return

    if not message.content[0] in ["a","w","A","W"]:
        return

    if message.author == bot.user:
        return

    if str(message.channel.id) in wawa_data:
        channel_data = wawa_data[str(message.channel.id)]
        update_data(channel_data)

        try:
            wawa = str(message.content).lower()
            if message.author.id != channel_data["last_user"]:
                if wawa == channel_data["nextWawa"]:
                    channel_data["nextWawa"] = channel_data["nextLetter"] + channel_data["nextWawa"]
                    if channel_data["nextLetter"] == "a":
                        channel_data["nextLetter"] = "w"
                    else:
                        channel_data["nextLetter"] = "a"

                    channel_data["chain_length"] += 1
                    channel_data["last_user"] = message.author.id

                    if channel_data["chain_length"] > channel_data["record"] != 0:
                        if channel_data["new_record_reaction"]:
                            await message.add_reaction(channel_data["new_record_reaction"])
                    else:
                        if channel_data["correct_reaction"]:
                            await message.add_reaction(channel_data["correct_reaction"])

                    if channel_data["chain_length"] % 10 == 0 and channel_data["chain_length"] != 0:
                        if channel_data["10_reaction"]:
                            await message.add_reaction(channel_data["10_reaction"])

                    if channel_data["chain_length"] % 100 == 0 and channel_data["chain_length"] != 0:
                        if channel_data["100_reaction"]:
                            await message.add_reaction(channel_data["10_reaction"])

                    wawa_data[str(message.channel.id)] = channel_data
                    with open("wawa_data.json", "w") as wawa_file:
                        wawa_file.write(json.dumps(wawa_data))
                else:
                    channel_data["nextWawa"] = "a"
                    channel_data["nextLetter"] = "w"
                    channel_data["last_user"] = None
                    await message.add_reaction(channel_data["wrong_reaction"])
                    if channel_data["chain_length"] > channel_data["record"]:
                        channel_data["record"] = channel_data["chain_length"]
                        channel_data["record_breaker"] = message.author.mention
                        await message.channel.send(
                            f"New record! {message.author.mention} broke the chain at {channel_data["chain_length"]} letters! Restart at \"a\".\n\nIf you didn't type a wawa but still failed, it may be because your message started with a or w. Try to avoid those or put a character in front of your messages!")
                    else:
                        await message.channel.send(
                            f"{message.author.mention} broke the chain at {channel_data["chain_length"]} letters! Restart at \"a\".\n\nIf you didn't type a wawa but still failed, it may be because your message started with a or w. Try to avoid those or put a character in front of your messages!")

                    channel_data["chain_length"] = 0

                    wawa_data[str(message.channel.id)] = channel_data
                    update_wawa_file(wawa_data)
            else:
                if channel_data["wait_reaction"]:
                    await message.add_reaction(channel_data["wait_reaction"])
                await message.channel.send("You need friends to wawa!")
        except ValueError:
            pass
    await bot.process_commands(message)

@bot.slash_command(description = "Makes it so you can wawa in the current channel!")
async def enable_wawa(ctx):
    if not ctx.user.guild_permissions.administrator:
        return await ctx.response.send_message("You aren't an admin!")

    global wawa_data

    channel_data = {}
    update_data(channel_data)

    wawa_data[str(ctx.channel.id)] = channel_data
    update_wawa_file(wawa_data)

    await ctx.response.send_message("Wawa enabled!")

@bot.slash_command(description = "Deletes all wawa data in the current channel :(")
async def disable_wawa(ctx):
    if not ctx.user.guild_permissions.administrator:
        return await ctx.response.send_message("You aren't an admin!")

    global wawa_data

    del wawa_data[str(ctx.channel.id)]
    update_wawa_file(wawa_data)

    await ctx.response.send_message("Wawa disabled :(")


@bot.slash_command(description = "Displays record wawa length (and who broke it) in this channel")
async def show_record(ctx):
    global wawa_data
    channel_data = wawa_data[str(ctx.channel.id)]

    update_data(channel_data)

    if channel_data["record"] > 0:
        await ctx.respond(f"The record length wawa in this channel was {channel_data["record"]} letters long and {channel_data["record_breaker"]} was the one who broke the chain!")
    else:
        await ctx.respond("No record has been set in this channel yet! When someone ruins the wawa chain, it will be updated.")

@bot.slash_command(description = "Resets record in current channel")
async def reset_record(ctx):
    if not ctx.user.guild_permissions.administrator:
        return await ctx.response.send_message("You aren't an admin!")

    global wawa_data
    channel_data = wawa_data[str(ctx.channel.id)]

    channel_data["record"] = 0
    channel_data["record_breaker"] = None

    wawa_data[str(ctx.channel.id)] = channel_data
    update_wawa_file(wawa_data)

    await ctx.respond(f"Channel record data reset!")

@bot.slash_command(description = "Resets all wawa data in this channel")
async def reset_channel(ctx):
    if not ctx.user.guild_permissions.administrator:
        return await ctx.response.send_message("You aren't an admin!")

    global wawa_data

    channel_data = {}
    update_data(channel_data)

    wawa_data[str(ctx.channel.id)] = channel_data
    update_wawa_file(wawa_data)

    await ctx.respond(f"Channel wawa data reset!")

@bot.slash_command(description = "Resets the symbols the bot uses in reactions")
@option ("reaction", description="Choose what reaction's symbol to change", choices=["correct_reaction", "new_record_reaction", "10_reaction", "100_reaction", "wrong_reaction", "wait_reaction", "all"])
async def reset_reaction(ctx, reaction):
    if not ctx.user.guild_permissions.administrator:
        return await ctx.response.send_message("You aren't an admin!")

    global wawa_data
    channel_data = wawa_data[str(ctx.channel.id)]
    default_reactions = {"correct_reaction":"✅","new_record_reaction":"🎉","10_reaction":"🔟","100_reaction":"💯","wrong_reaction":"❌","wait_reaction":"⚠️"}

    if reaction in default_reactions:
        del channel_data[reaction]
    else:
        del channel_data["correct_reaction"]
        del channel_data["new_record_reaction"]
        del channel_data["10_reaction"]
        del channel_data["100_reaction"]
        del channel_data["wrong_reaction"]
        del channel_data["wait_reaction"]

    wawa_data[str(ctx.channel.id)] = channel_data
    update_wawa_file(wawa_data)

    await ctx.respond(f"Reset reaction(s)!")

@bot.slash_command(description = "Sets the symbols the bot uses in reactions")
@option("reaction", description="Choose what reaction's symbol to change", choices=["correct_reaction", "new_record_reaction", "10_reaction", "100_reaction", "wrong_reaction", "wait_reaction"])
@option("symbol", description = "Enter the emoji the bot should use for the chosen reaction", required = False)
async def set_reaction(ctx, reaction, symbol):
    if not ctx.user.guild_permissions.administrator:
        return await ctx.response.send_message("You aren't an admin!")

    global wawa_data
    channel_data = wawa_data[str(ctx.channel.id)]

    if symbol:
        channel_data[reaction] = str(symbol)
    else:
        channel_data[reaction] = None

    wawa_data[str(ctx.channel.id)] = channel_data
    update_wawa_file(wawa_data)

    await ctx.respond(f"Set reaction!")

@bot.slash_command(description = "Lists the reactions used in this channel")
async def list_reactions(ctx):
    global wawa_data
    channel_data = wawa_data[str(ctx.channel.id)]

    await ctx.respond(
        f"Correct Reaction: {channel_data["correct_reaction"]}\n"
        f"New Record Reaction: {channel_data["new_record_reaction"]}\n"
        f"10 Reaction: {channel_data["10_reaction"]}\n"
        f"100 Reaction: {channel_data["100_reaction"]}\n"
        f"Wrong Reaction: {channel_data["wrong_reaction"]}\n"
        f"Wait Reaction: {channel_data["wait_reaction"]}"
    )

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

bot.run(token)