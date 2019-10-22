import discord
import random
import pandas as pd
from discord.ext import commands
import config

TOKEN = config.TOKEN

client = commands.Bot(command_prefix='!')


def d(x):
    return random.randint(1, x + 1)


@client.event
async def on_ready():
    print('Bot is ready.')


@client.event
async def on_message(message):
    if message.content.startswith('!hello'):
        channel = message.channel
        await channel.send('Hello, {.author.mention}'.format(message))

    if message.content.startswith('!deck13'):
        channel = message.channel
        card = random.randint(0, 13)
        df = pd.read_csv('deckofmanythings.csv')
        cardName = df['Playing Card'][card]
        cardDesc = df['Description'][card]
        await channel.send((
                                       "{0.author.mention}, you pull a card from the Deck of Many Things...\nYou have selected the " + cardName + ":\nThe Card of the " + cardDesc).format(
            message))

    if message.content.startswith('!deck22'):
        channel = message.channel
        card = random.randint(0, 22)
        df = pd.read_csv('deckofmanythings.csv')
        cardName = df['Playing Card'][card]
        cardDesc = df['Description'][card]
        await channel.send((
                                       "{0.author.mention}, you pull a card from the Deck of Many Things...\nYou have selected the " + cardName + ":\nThe Card of the " + cardDesc).format(
            message))

    if message.content.startswith('!roll'):
        channel = message.channel
        roll = str(message.content).split(' ')[1]
        numDice = int(roll.split('d')[0])
        diceVal = int(roll.split('d')[-1])
        diceResults = []
        total = 0
        if numDice > 100:
            await channel.send(
                ('{0.author.mention} That is too many dice!').format(message))
        elif diceVal > 1000:
            await channel.send(
                ('{0.author.mention} That die is too big!').format(message))
        else:
            while numDice > 0:
                diceResults.append(d(diceVal))
                numDice -= 1
            for x in diceResults:
                total += x
            if '+' in message.content:
                total += int(message.content[-1])
            elif '-' in message.content:
                total -= int(message.content[-1])
            else:
                total += 0

            await channel.send(
                ('{0.author.mention} Result: ' + str(total) + '\n' + '*' + str(diceResults) + '*').format(message))


client.run(TOKEN)
