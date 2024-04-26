import discord
import mysql.connector
import random
import string
from datetime import datetime, timedelta
from discord.ext import commands

# Your Discord bot token (replace 'YOUR_BOT_TOKEN' with your actual bot token)
BOT_TOKEN = 'xxxxxxx'

# Create a Discord bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

# Color codes
cRed = 0XFF0000
cGreen = 0X00FF00
cMain = 0XFFF666

# Your database connection pool setup goes here
HOST = "xxxxxxx"
USER = "xxxxxxx"
PASSWORD = "xxxxxxx"
DATABASE = "xxxxxxx"

mydb = mysql.connector.connect(
  host=HOST,
  user=USER,
  password=PASSWORD,
  database=DATABASE
)

mycursor = mydb.cursor()

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

async def reconnect():
    global mydb
    mydb.disconnect()
    mydb = mysql.connector.connect(host=HOST, user=USER, passwd=PASSWORD, database=DATABASE)
    global mycursor
    mycursor = mydb.cursor()

async def check_user_products(current, new):
    for x in current:
        if x == new:
            return current
    return current+","+new


async def give_role(ctx, role):
    # Check if the command is invoked through direct messages
    if ctx.guild is None:
        try:
            # Fetch the guild object using the GUILD_ID
            guild = await bot.fetch_guild(0000000000000) # Replace this
            # Fetch the member object in the guild
            member = await guild.fetch_member(ctx.author.id)

            # Check if the user is a member of the guild
            if member:
                # Get the role object based on the role name
                role = discord.utils.get(guild.roles, name=f"{role}")  # Replace with the actual role name

                if role:
                    # Add the role to the member
                    await member.add_roles(role)
                    await ctx.send("Role added successfully!")
                else:
                    await ctx.send("Role not found.")
            else:
                await ctx.send("You are not a member of the guild.")
        except discord.errors.NotFound:
            await ctx.send("Guild not found. Make sure you have the correct GUILD_ID.")

def genkey():
    random.seed()
    characters = string.ascii_lowercase + string.digits

    groups = []
    for _ in range(3):
        group = ''.join(random.choice(characters) for _ in range(6))
        groups.append(group)

    license_key = f"prefix-{groups[0]}-{groups[1]}-{groups[2]}"

    return license_key


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Get the user ID of the message author
    user_id = message.author.id

    # Get the target channel
    target_channel = bot.get_channel(1137481109853184041)

    # Log every command received
    if message.content.startswith('!'):
        print(
            f"Command received: {message.content}, from {message.author} ({user_id}) in #{message.channel} | {message.guild}")
        await target_channel.send(
            f"Command received: `{message.content}`, from `{message.author}` (`{user_id}`) in `#{message.channel}` | `{message.guild}`")

    # Process commands normally
    await bot.process_commands(message)

# Command error handlers go here
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(embed=discord.Embed(title="Error",
                                           description="Command not found. Use !help for a list of available commands.",
                                           color=0xFF0000))
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(embed=discord.Embed(title="Error",
                                           description="Missing required argument. Use !help for command usage.",
                                           color=0xFF0000))
    else:
        # Handle other errors here
        await ctx.send(embed=discord.Embed(title="Error", description=f"{error}",
                                       color=0xFF0000))


@bot.command()
async def logs(ctx, command, output, color):

    channel = bot.get_channel(int(00000000)) # Replace this
    date_variable = datetime.now().strftime("[%d/%m/%Y | %H:%M:%S]")

    embed = discord.Embed(title="Logs", description=f"`{ctx.author}` appealed the command `{command}` in <#{ctx.channel.id}>",
                          color=color)
    embed.add_field(name="Output", value=f"{output}", inline=False)
    embed.set_footer(text=f"yoursite.com - {date_variable}")

    # Send the embed to the same channel where the command was invoked
    await channel.send(embed=embed)

# Your commands (decorated with @bot.command()) and the main logic for the bot go here

@bot.command()
async def help(ctx):
    # Create the embed object
    if isinstance(ctx.author, discord.Member) and ctx.author.roles:
        role = discord.utils.get(ctx.author.roles, name='Support')
        if role:
            embed = discord.Embed(title="Help", description="Bot prefix is `!`", color=0xffe433)
            embed.add_field(name="!help", value="You are already here", inline=False)
            embed.add_field(name="!claim [key]", value="Claim a subscription key", inline=False)
            embed.add_field(name="!sub", value="Returns your(only) subscription time", inline=False)
            embed.add_field(name="!gift [username] [key]", value="Gift someone subscription", inline=False)
            embed.add_field(name="!ping", value="Check if bot is online", inline=True)
            embed.add_field(name="----------Staff----------", value="", inline=False)
            embed.add_field(name="!gensub [days] [product]", value="Generate a subscription key", inline=False)
            embed.add_field(name="!gensubs [days] [product] [amount](only admin)", value="Generate subscription keys in bulk", inline=False)
            embed.add_field(name="!user [username]", value="Returns full information about a user", inline=False)
            embed.add_field(name="!resethwid [user]", value="Resets HWID for a specific user", inline=False)
            embed.add_field(name="!appversion", value="Returns the app version from database", inline=False)
            embed.add_field(name="!setappversion [version] (only admin)", value="Update the app version in database", inline=False)
            embed.set_footer(text="yoursite.com")
    else:
        embed = discord.Embed(title="Help", description="Bot prefix is `!`", color=0xffe433)
        embed.add_field(name="!help", value="You are already here", inline=False)
        embed.add_field(name="!claim [key]", value="Claim a subscription key", inline=False)
        embed.add_field(name="!sub", value="Returns your(only) subscription time", inline=False)
        embed.add_field(name="!gift [username] [key]", value="Gift someone subscription", inline=False)
        embed.add_field(name="!ping", value="Check if bot is online", inline=True)
        embed.set_footer(text="yoursite.com")

    # Send the embed to the same channel where the command was invoked
    await ctx.send(embed=embed)

# This is a general command for sending custom embeds in any channel you want

@bot.command()
@commands.has_any_role('Administrator')
async def sendembed(ctx):
    # Create the embed object

    embed = discord.Embed(title="Frequently Asked Questions (FAQ)", description="", color=cMain)
    embed.add_field(name="**1. Welcome to our serrver!**", value="Please read the rules channel.", inline=False)

    embed.set_footer(text="yoursite.com")

    # Send the embed to the same channel where the command was invoked
    await ctx.send(embed=embed)

@bot.command()
async def clearbot(ctx, amount: int):


    # Define a check function to filter bot messages
    def is_bot_message(message):
        return message.author.bot

    # Delete the specified number of bot messages
    deleted_count = 0
    async for message in ctx.channel.history(limit=None):
        if is_bot_message(message):
            await message.delete()
            deleted_count += 1
            if deleted_count >= amount:
                break

@bot.command()
async def ping(ctx):
    # Your existing ping command logic here
    await ctx.send(embed=discord.Embed(title="I'm alive, duh", description=f"Latency: {round(bot.latency * 1000)}ms",
                                       color=0xffe433))

@bot.command()
async def sub(ctx):
    await reconnect()

    query = f"SELECT * FROM users WHERE discord_name = %s"
    mycursor.execute(query, (ctx.author.name,))
    myresult = mycursor.fetchone()

    # Create the embed object
    embed = discord.Embed(title="User", color=cMain)
    embed.add_field(name="Your subscription will end on:", value=f"{myresult[5]}", inline=False)

    # Send the embed to the same channel where the command was invoked
    await ctx.send(embed=embed)

@bot.command()
@commands.has_any_role('Administrator')
async def setappversion(ctx, version):
    await reconnect()

    query = f"UPDATE cores SET version = '{version}'"
    mycursor.execute(query)

    # Create the embed object
    embed = discord.Embed(title="App", color=cMain)
    embed.add_field(name="Version updated", value=f"{version}", inline=False)
    mydb.commit()

    # Send the embed to the same channel where the command was invoked
    await ctx.send(embed=embed)

@bot.command()
@commands.has_any_role('Support', 'Administrator')
async def appversion(ctx):
    await reconnect()

    query = f"SELECT version FROM cores LIMIT 1"
    mycursor.execute(query)
    version = mycursor.fetchone()

    # Create the embed object
    embed = discord.Embed(title="App", color=cMain)
    embed.add_field(name="Current version", value=f"{version[0]}", inline=False)

    # Send the embed to the same channel where the command was invoked
    await ctx.send(embed=embed)

@bot.command()
async def claim(ctx, key):
    # Your existing claim command logic here
    if ctx.guild is not None:
        await ctx.send(embed=discord.Embed(title="Error",
                                           description=f"This command can be used only in through direct messages with bot !!!",
                                           color=cRed))
        await ctx.message.delete()
        return


    await reconnect()

    query = f"SELECT * FROM sub_keys WHERE license_key = '{key}'"
    mycursor.execute(query)
    myKey = mycursor.fetchone()

    if myKey is None:
        await ctx.send(
            embed=discord.Embed(title="Error", description=f"Invalid license key",
                                color=cRed))
        return

    myKey2 = myKey[1]
    myKeyProduct = myKey[2]
    myKeyTime = myKey[3]

    if myKeyProduct == 1:
        server_role = 'Membership'
    elif myKeyProduct == 2:
        server_role = 'Stage 2'
    elif myKeyProduct == 3:
        server_role = 'Stage 3'


    query = f"SELECT * FROM users WHERE discord_name = '{ctx.author.name}'"
    mycursor.execute(query)
    myUser = mycursor.fetchone()

    if myUser is None:
        # Add user in database
        date_variable = datetime.now()
        sub_time = date_variable + timedelta(days=myKeyTime)
        discord_id = ctx.author.id
        query = "INSERT INTO users (discord_name, discord_id, last_key, products, sub_time, role, created_date) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        val = (ctx.author.name, discord_id, key, myKeyProduct, sub_time, 1, date_variable)
        mycursor.execute(query, val)
        await give_role(ctx, server_role)
        await ctx.send(embed=discord.Embed(title="Success",
                                           description=f"Congratulations, you are now registered! {myKeyTime} "
                                                       f"days were added to your subscription",
                                           color=0xffe433))
        await logs(ctx, "!claim",
                   f"Account `{ctx.author.name}` created using the following {myKeyTime} days key `{key}`.",
                   cMain)

    else:
        #Add subscription to existing user
        myDiscordName = myUser[1]  # Column 1 from table
        if myDiscordName == ctx.author.name:
            if key == myKey2:
                date_variable = datetime.now()
                sub_time = date_variable + timedelta(days=myKeyTime)

                print(sub_time)
                final_products = await check_user_products(myUser[4], str(myKeyProduct))
                print(final_products)
                query = 'UPDATE users SET last_key = %s, sub_time = %s, products = %s WHERE discord_name = %s'
                query_del = f"DELETE FROM sub_keys WHERE license_key = '{key}'"
                val = (key, sub_time, final_products, ctx.author.name)
                mycursor.execute(query, val)
                mycursor.execute(query_del)

                await give_role(ctx, server_role)
                await ctx.send(embed=discord.Embed(title="Success",
                                                   description=f"You successfully claimed a {myKeyTime} days key",
                                                   color=0xffe433))
                await logs(ctx, "!claim",
                           f"`{ctx.author.name}` claimed the following {myKeyTime} days key `{key}`",
                           cMain)

    mydb.commit()


@bot.command()
@commands.has_any_role('Support', 'Administrator')
async def user(ctx, discord_name):
    await reconnect()

    query = f"SELECT * FROM users WHERE discord_name = '{discord_name}'"
    mycursor.execute(query)
    myresult = mycursor.fetchone()

    if myresult is None:
        await ctx.send(
            embed=discord.Embed(title="Error", description=f"Invalid discord name",
                                color=cRed))
        return

    print(myresult)
    # Create the embed object
    embed = discord.Embed(title="User", color=cMain)
    embed.add_field(name="User-ID", value=f"{myresult[0]}", inline=False)
    embed.add_field(name="Discord name/id", value=f"{myresult[1]} ({myresult[2]})", inline=False)
    embed.add_field(name="Last Key", value=f"{myresult[3]}", inline=False)
    embed.add_field(name="Stages", value=f"{myresult[4]}", inline=False)
    embed.add_field(name="Sub time", value=f"{myresult[5]}", inline=False)
    embed.add_field(name="Device (HWID)", value=f"{myresult[6]}", inline=False)
    embed.add_field(name="Role", value=f"{myresult[7]}", inline=False)
    embed.add_field(name="Creation date", value=f"{myresult[8]}", inline=False)
    embed.add_field(name="Ban reason", value=f"{myresult[9]}", inline=False)
    embed.set_footer(text="yoursite.com")

    # Send the embed to the same channel where the command was invoked
    await ctx.send(embed=embed)


@bot.command()
@commands.has_any_role('Support', 'Administrator')
async def gensub(ctx, days, product):

    if days in ["30", "60", "90"]:
        if product in ["1","2","3"]:
            date_variable = datetime.now()

            license_key = genkey()

            # Create the embed object
            embed = discord.Embed(title="License", color=0xffe433)
            embed.add_field(name=f"{days} Days - Stage {product}", value=f"{license_key}", inline=False)

            # Send the embed to the same channel where the command was invoked

            await reconnect()
            query = "INSERT INTO sub_keys (license_key, product, days, created_date, created_by) VALUES (%s, %s, %s, %s, %s)"
            val = (license_key, product, days, date_variable, ctx.author.name)
            mycursor.execute(query, val)
            mydb.commit()
            await ctx.send(embed=embed)
            await logs(ctx, "!gensub",
                       f"`{ctx.author.name}` generated the following {days} days key `{license_key}`",
                       cMain)
        else:
            await ctx.send(embed=discord.Embed(title="Error", description=
            f"Invalid stage, please use only 1, 2 and 3",
                                               color=0xFF0000))
    else:
        await ctx.send(embed=discord.Embed(title="Error", description=
        f"Invalid days input, please use only 30, 60 and 90",
        color=0xFF0000))


@bot.command()
@commands.has_any_role("Administrator")
async def gensubs(ctx, days, product, amount):

    await reconnect()
    date_variable = datetime.now()
    generatedKeys = ""

    if days in ["30", "60", "90"]:
        for x in range(int(amount)):
            license_key = genkey()
            generatedKeys += license_key + "\n"
            query = "INSERT INTO sub_keys (license_key, product, days, created_date, created_by) VALUES (%s, %s, %s, %s, %s)"
            val = (license_key, product, days, date_variable, ctx.author.name)
            mycursor.execute(query, val)

    mydb.commit()
    f = open(f"Stage{product}-{amount}keys.txt", "w")
    f.write(generatedKeys)
    f.close()
    await ctx.send(file=discord.File(f"Stage{product}-{amount}keys.txt"))



@bot.command()
@commands.has_any_role('Support', 'Administrator')
async def resethwid(ctx, discord_name):

    await reconnect()

    query = f"SELECT * FROM users WHERE discord_name = '{discord_name}'"
    mycursor.execute(query)
    myresult = mycursor.fetchone()

    if myresult is None:
        await ctx.channel.purge(limit=1)
        await ctx.send(
            embed=discord.Embed(title="Error", description=f"Invalid discord name",
                                color=cRed))
        return

    query = f"UPDATE users SET device = NULL WHERE discord_name = '{discord_name}'"
    mycursor.execute(query)

    # Create the embed object
    embed = discord.Embed(title="App", color=cMain)
    embed.add_field(name=f"Successfully resetted HWID for {discord_name}", value=f"", inline=False)
    mydb.commit()

    # Send the embed to the same channel where the command was invoked
    await ctx.send(embed=embed)

# Run the bot with your token
bot.run(BOT_TOKEN)
