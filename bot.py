import discord
import asyncio
import re
from time import gmtime, strftime
from parseAPI import Data, load

with open('../pros_token.txt', 'r') as discord_file:
    DISCORD_TOKEN = discord_file.read()[:-2]
print(DISCORD_TOKEN, end=';\n')

prefix = "$"
client = discord.Client()
color = discord.Color(15452014)
base = "https://pros.cs.purdue.edu/"
tutorial = base + "tutorials/"
api = base + "api/#"
data = load()

def reContains(regex, string):
    return bool(re.search(regex, string))

@client.event
@asyncio.coroutine
def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------\n')
    yield from client.send_message(client.get_channel("315552571823489024"), "Connected at " + strftime("%Y-%m-%d %H:%M:%S", gmtime()))

@client.event
@asyncio.coroutine
def on_message(message):
    global data, prefix, client, base, tutorial, api
    content = message.content[1:]
    if message.content[0] == prefix:
        result = ""
        if content.startswith("api "):
            c = content[4:]
            tdata = None
            for i in range(len(data)):
                if data[i].access == c.lower():
                    tdata = data[i]
            if tdata == None:
                result = "Not found"
            else:
                result = ""
                link = "**[PROS API Reference](" + tdata.link + ")**"
                params = ""
                if len(tdata.params) > 0:
                    for param in tdata.params:
                        paramm = param.split(" ")
                        params += "`" + paramm.pop(0) + ":` " + " ".join(paramm).strip() + "\n"
                em = discord.Embed(title=tdata.group, description=link, color=color)
                if tdata.typec.lower() == "function":
                    em.add_field(name="Declaration", value="```Cpp\n" + tdata.extra + " " + tdata.name + "\n```")
                    em.add_field(name="Description", value=tdata.description)
                    if len(tdata.params) > 0:
                        em.add_field(name="Parameters", value=params)
                    if tdata.returns is not "":
                        em.add_field(name="Returns", value = tdata.returns)
                elif tdata.typec.lower() == "macro":
                    em.add_field(name="Declaration", value="```Cpp\n#define " + tdata.name + " " + tdata.extra + "\n```")
                    em.add_field(name="Description", value=tdata.description)
                if em != None:
                    yield from client.send_message(message.channel, embed=em)
        elif content.startswith("tutorial "):
            c = content[9:]
            result = "<" + tutorial + c + ">"
        elif content.startswith("f "):
            c = content[2:].lower()
            matches = []
            for d in data:
                if reContains(c, d.access) or reContains(c, d.description.lower()):
                    if len(d.name) > 1 and len(d.description) > 1:
                        matches.append(d)
            em = discord.Embed(title="Matches for `" + c + "`", color=color)
            for m in range(len(matches)):
                fname = "`" + matches[m].extra + " " + matches[m].name + "`"
                if matches[m].typec == "macro":
                    fname = "`#define " + matches[m].name + matches[m].extra + "`"
                flink = "*[link](" + matches[m].link + ")*"
                fdes = flink + "\n" + matches[m].description
                em.add_field(name=fname, value=fdes)
            if len(matches) is 0:
                em.add_field(name="None Found")
            yield from client.send_message(message.channel, embed=em)
        if result != None and result != "":
            yield from client.send_message(message.channel, result)
    data = load()

client.run(DISCORD_TOKEN)
