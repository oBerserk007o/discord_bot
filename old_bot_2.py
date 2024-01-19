import os
import discord
import random

db = []

client = discord.Client()
secret_token = os.environ['TOKEN']
forbidden_words = [
    "rawr",
    "nuzzles",
    "nuzzle",
    "rubbies",
    "UwU",
    "OwO",
    "uwu",
    "owo",
    "Owo",
    "owO",
    "Uwu",
    "uwU"
]
responses = [
    "Warning! You have said a punishable word! Becareful next time, or else...",
    "...",
    "Ehm ehm, is that an inapropriate word I see here?"
]


@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))


def add_forbidden_words(word):
    if "word" in db.keys():
        words = db["words"]
        words.append(word)
        db["words"] = words
    else:
        db["words"] = word


def delete_forbidden_words(index):
    words = db["words"]
    if len(words) > index:
        del words[index]
        db["words"] = words


options = forbidden_words
if "word" in db.keys():
    options = options + db["word"]


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    msg = message.content

    if msg.startswith("%testcommand"):
        await message.channel.send(
            "*bip bip* </>Test command recieved</>, *bup beep* <script>sending reply...<script/>")

        await message.channel.send("Message='Hello!'")

    if msg.startswith("%list"):
        await message.channel.send(options)

    if msg.startswith("%stop"):
        await message.channel.send("Stopping bot...")
        await client.close()
        print("Stopping bot...")

    if any(word in msg for word in options):
        await message.channel.send(random.choice(responses))

    if msg.startswith("%addword"):
        words = msg.split("%addword ", 1)[1]
        add_forbidden_words(words)
        try:
            await message.channel.send("New word " + str(words) + " added to list")
        except:
            await message.channel.send("Please enter a word, not a number (cause it ruins my code :c)")

    if msg.startswith("%delword"):
        words = []
        if "words" in db.keys():
            try:
                index = int(int(msg.split("%delword ", 1)[1]))
                print("index=" + str(index))
            except:
                await message.channel.send("Please enter a number (the number of the index of the word in the list)")
            delete_forbidden_words(int(index))
            words = db["words"]
        await message.channel.send(words)


client.run(secret_token)