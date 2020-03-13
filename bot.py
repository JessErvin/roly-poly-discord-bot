'''
This is roly-poly, a simple dice rolling bot I made for Discord.
It can also say hello or draw a card from the Deck of Many Things
'''

import discord
import random
import pandas as pd
from discord.ext import commands
import config

TOKEN = config.token

client = commands.Bot(command_prefix='!')


def d(x):
    return random.randint(1, x)


@client.event
async def on_ready():
    print('Bot is ready.')


@client.event
async def on_message(message):  # Say Hi to the bot!
    if message.content.startswith('!hello'):
        channel = message.channel
        await channel.send('Hello, {.author.mention}!'.format(message))

    if message.content.startswith('!deck13'):  # pick a card from the 13 card version of the deck of many things
        channel = message.channel
        card = random.randint(0, 13)
        df = pd.read_csv('deckofmanythings.csv')
        cardName = df['Playing Card'][card]
        cardDesc = df['Description'][card]
        await channel.send((
                "{0.author.mention}, you pull a card from the Deck of Many Things...\nYou have "
                "selected the " + cardName + ":\nThe Card of the " + cardDesc).format(
            message))

    if message.content.startswith('!deck22'):  # pick a card from the 22 card version of the deck of many things
        channel = message.channel
        card = random.randint(0, 22)
        df = pd.read_csv('deckofmanythings.csv')
        cardName = df['Playing Card'][card]
        cardDesc = df['Description'][card]
        await channel.send((
                '{0.author.mention}, you pull a card from the Deck of Many Things...\nYou have selected the ' + cardName + ':\nThe Card of the ' + cardDesc).format(
            message))

        #TODO: KEEP TRACK OF USER DECK csv? add !reset command

    if message.content.startswith('!roll'):  # roll some dice & add modifiers
        channel = message.channel
        roll = str(message.content).split(' ')[1]
        roll = roll.split('+')[0]
        roll = roll.split('-')[0]
        numDice = int(roll.split('d')[0])
        diceVal = int(roll.split('d')[-1])
        diceResults = []
        total = 0
        try:
            if numDice > 100:  # setting limits to avoid timing out
                await channel.send(
                    '{0.author.mention} That is too many dice!'.format(message))
            elif diceVal > 1000:
                await channel.send(
                    '{0.author.mention} That die is too big!'.format(message))
            else:
                while numDice > 0:
                    diceResults.append(d(diceVal))
                    numDice -= 1
                for x in diceResults:
                    total += x
                if '+' in message.content:
                    total += int(str(message.content).split('+')[-1])
                elif '-' in message.content:
                    total -= int(str(message.content).split('-')[-1])
                else:
                    total += 0

                await channel.send(
                    ('{0.author.mention} Result: ' + str(total) + '\n' + '*' + str(diceResults) + '*').format(message))
        except:
            await channel.send(
                "I'm sorry, {0.author.mention} I don't understand, Try typing !commands to see what I can do".format(
                    message))

    if message.content.startswith('!commands'):  # returns a list of possible commands
        channel = message.channel
        await channel.send((
            'Hello, {0.author.mention}! Here is a list of what I can do:\n__**!roll #d# + #**__ - This rolls your '
            'chosen number of dice with your chosen number of sides. You can also add or subtract a modifier! '
            '\n     *Examples: !roll 1d20, !roll 2d6 + 8, !roll 2d4 - 1*\n__**!deck13**__ - This will pull a card from '
            'the 13 card version of the Deck of Many Things\n__**!deck22**__ - This will pull a card from the full 22 '
            'card version of the Deck of Many Things\n__**!commands**__ - This will repeat this message!\n     *Details '
            'on the Deck of Many Things can be found here: '
            'https://www.dndbeyond.com/magic-items/deck-of-many-things*'.format(message)))


client.run(TOKEN)
