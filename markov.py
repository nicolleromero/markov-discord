"""A Markov chain generator that can tweet random messages."""

import os
import discord
import re
import sys
import random
from pprint import pprint


def open_and_read_file():
    """Takes any number of text files and turns
    the files' contents into one string of text.
    """

    contents = ''

    for text in range(2, len(sys.argv)):
        contents += open(str(sys.argv[text])).read()

    return contents.strip()


def make_chains():
    """Take input text as string; return dictionary of Markov chains.

    A chain will be a key that consists of a tuple of (word1, word2)
    and the value would be a list of the word(s) that follow those two
    words in the input text.

    For example:

        >>> chains = make_chains("hi there mary hi there juanita")

    Each bigram (except the last) will be a key in chains:

        >>> sorted(chains.keys())
        [('hi', 'there'), ('mary', 'hi'), ('there', 'mary')]

    Each item in chains is a list of all possible following words:

        >>> chains[('hi', 'there')]
        ['mary', 'juanita']

        >>> chains[('there','juanita')]
        [None]
    """

    chains = {}

    # Open the file and turn it into one long string
    contents = open_and_read_file()

    # Creates a list of individual words
    words_list = re.split('\s+', contents)

    # n is for the n-gram and is passed in as the second argument
    n = int(sys.argv[1])

    for idx, word in enumerate(words_list[:-n]):
        ngram = tuple(words_list[idx: (idx + n)])
        next_word = words_list[idx + n]

        values = chains.setdefault(ngram, [])
        values.append(next_word)

    return chains


def make_text():
    """Return text from chains."""

    # Get a Markov chain
    chains = make_chains()
    chain_keys = list(chains.keys())

    # Randomly choose a word; must start with a capital letter
    while True:
        try:
            phrase = random.choice(chain_keys)
            phrase_list = chains[phrase]
            random_word = random.choice(phrase_list)

            if random_word and random_word[0].isupper():
                break

        except:
            break

    words = [random_word]
    phrase = (*phrase[1:], random_word)

  # Continue adding words using random selection
    while True:
        try:
            random_word = random.choice(chains[phrase])
            words.append(random_word)
            phrase = (*phrase[1:], random_word)

            # Breaks if the message is > 100 words and it ends with a period
            if words[-1][-1] == '.' and len(words) > 100:
                break

        except:
            # Breaks if chain gets to the end (random selection results in error)
            break

    return " ".join(words)


"""Connecting to bot on Discord"""

client = discord.Client()


@client.event
async def on_ready():
    print(f'Successfully connected! Logged in as {client.user}.')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content:
        await message.channel.send(make_text())


client.run(os.environ['DISCORD_TOKEN'])
