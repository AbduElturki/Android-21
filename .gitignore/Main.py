import discord
import asyncio
import random
import pickle
import os
import time

#TODO: seperate this file into different modules.
#TODO: Remove pickle and just use database.



#Check if the role is in the file

def role_exists(role,list):
    roles = []
    for x in list:
        roles.append(x.name.lower())
    if role.lower() in roles:
        return True
    else:
        return False

#Get role object from the picke file.

def get_role(name,list):
    for x in list:
        if name.lower() == x.name.lower():
            return x
    sys.exit(1)

welcome = 'Hello, I\'m Android 21! the offical University of Bristol Computer Gaming Society bot. Please make sure to read #server_info channel for rules and information about the society. check #announcements to keep upto date with our socials. If you are first year assign yourself with @Fresher role in #roles. Otherwise, assign yourself appropriate so people know what game you play. Finally, introduce yourself in #introduction and make friends! have fun!'

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_member_join(member):
    await client.send_message(member, welcome)

@client.event
async def on_message(message):
    #TODO seperate server messages and private messages commands
    #For testing welcome message.
    if message.content.startswith('!testwelcome'):
        await client.send_message(message.author, welcome)

    #TODO Make this committee/admin only command
    elif message.content.startswith('!addgame'):
        if not os.path.isfile("game_file.pk1"):
            games = []
        else:
            with open("game_file.pk1","rb") as game_file:
                games = pickle.load(game_file)
        if not role_exists(message.content[9:],message.server.roles):
            await client.create_role(message.server, name=message.content[9:])
        else:
            if get_role(message.content[9:],message.server.roles) in games:
                await client.send_message(message.channel, 'The game is already in the list')
            else:
                games.append(get_role(message.content[9:],message.server.roles))
                await client.send_message(message.channel, message.content[9:] + ' has been added')
        with open("game_file.pk1", "wb") as game_file:
            pickle.dump(games, game_file)


    elif message.content.startswith('!checkgames'):
        if not os.path.isfile("game_file.pk1"):
            await client.send_message(message.channel, 'no games added.')
        else:
            with open("game_file.pk1","rb") as game_file:
                games = pickle.load(game_file)
                print(len(games))
                if len(games) == 0:
                    await client.send_message(message.channel, 'no games added')
                else:
                    for x in games:
                        await client.send_message(message.channel, str(x.name))

    #Give role to the user, and making sure it is done in a channel named role.
    elif message.content.startswith('!give') and message.channel.name == "role":
        if not os.path.isfile("game_file.pk1"):
            await client.send_message(message.channel, message.author.mention + ", game not found.")
        else:
            with open("game_file.pk1","rb") as game_file:
                games = pickle.load(game_file)
                if role_exists(message.content[6:],message.server.roles):
                    if role_exists(message.content[6:],message.author.roles):
                        await client.send_message(message.channel, message.author.mention + ", you already got have the role silly.")
                    elif get_role(message.content[6:],message.server.roles) in games:
                        await client.add_roles(message.author, get_role(message.content[6:], message.server.roles))
                        await client.send_message(message.channel, message.author.mention + ", the role has been added.")
                    else:
                        await client.send_message(message.channel, message.author.mention + ", oh no silly boy, you can\'t have this role.")
                else:
                    await client.send_message(message.channel, message.author.mention + ", game not found.")

    #remove a role for the user.
    elif message.content.startswith('!remove'):
        if not os.path.isfile("game_file.pk1"):
            await client.send_message(message.channel, message.author.mention + ", that role can't be removed.")
        else:
            with open("game_file.pk1","rb") as game_file:
                games = pickle.load(game_file)
                print(message.content[8:])
                if role_exists(message.content[8:],message.server.roles):
                    if not role_exists(message.content[6:],message.author.roles):
                        await client.send_message(message.channel, message.author.mention + ", you don't have this role silly.")
                    elif get_role(message.content[8:],message.server.roles) in games:
                        await client.remove_roles(message.author, get_role(message.content[8:], message.server.roles))
                        await client.send_message(message.channel, message.author.mention + ", the role has been removed.")
                    else:
                        await client.send_message(message.channel, message.author.mention + ", oh no silly kid, you can\'t remove this role.")
                else:
                    await client.send_message(message.channel, message.author.mention + ", that role can't be removed.")

    #Deletes the messages in role channel
    #TODO Have a message made by the bot that lists roles in alphabetical order.
    if message.channel.name == "role":
        time.sleep(5)
        await client.delete_message(message)



client.run('Mzc2Mzg3NTc0ODQ1MDE0MDMx.DN9p9w.AnQZF2P1oLolLW_6izvYkvLQA3U')
