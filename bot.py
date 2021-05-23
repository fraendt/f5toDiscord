import discord
from discord.ext.commands import Bot
from discord.ext.commands.errors import MissingRequiredArgument
import os
from dotenv import load_dotenv
import collector

load_dotenv()

try:
    with open('anchors.txt') as f:
        anchors = f.readlines()
except:
    anchors = []

client = Bot(command_prefix="!")

@client.command(name='embed', description='embed test', help='embed test')
async def embeded(ctx):
    embed=discord.Embed(title="top text",
                        description="bottom text",
                        color=0xFF5733)
    await ctx.send(embed=embed)

@client.command(name='echo', description='echo', help='echo')
async def echo(ctx, message=''):
    if message=='':
        return
    await ctx.send(message)

@client.command(name='where')
async def echo(ctx):
    global w
    w=ctx
    await ctx.send(ctx.channel)

@client.command(name='anchor', description='send f5bot messages here')
async def anchor(ctx, keyword='*'): # for lack of a better adjective
    global anchors
    channel = ctx.channel.id
    if channel not in anchors:
        anchors.append(channel)
        await ctx.send('anchored')
    else:
        await ctx.send('bruh channel already anchored')

@client.command(name="test", description="test", help="test")
async def test(ctx):
    await ctx.send('W')

@client.command(name='check', description='check inbox', help='check inbox')
async def check_mail(ctx):
    res = collector.check_inbox()
    recipients = anchors
    if ctx.channel.id not in recipients:
        recipients.append(ctx.channel.id)
    if len(res) == 0:
        embed=discord.Embed(title="sorry bruh",
                        description="theres nothing",
                        color=0xFF5733)
        await ctx.send(embed=embed)
        return
    for i in res:
        parsed = collector.parse(i)
        for keyword, head, link, location in parsed:
            embed=discord.Embed(title=head,
                                url=link,
                                description=location,
                                color=0x0096FF)

            for anchor in recipients:
                await client.get_channel(anchor).send(embed=embed)
    
@client.command(name="add", description="add keyword to look for", help="add keyword to look for")
async def test(ctx):
    await ctx.send('W')


@client.event
async def on_ready():
    print("Ready")
    
client.run(os.getenv('LULW'))
with open('anchors.txt') as f:
    f.write('\n'.join(anchors))
