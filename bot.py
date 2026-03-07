import os
import discord
from discord.ext import commands
import random
import asyncio
from KeepAlive import keep_alive

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.invites = True

bot = commands.Bot(command_prefix='&', intents=intents, help_command=None)

# Footer i Boja
FOOTER_TEXT = "By KnEz.exe | Kings Of Reselling"
KING_COLOR = 0xffd700 # Zlatna

invites = {}

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="Kings Of Reselling 👑"))
    for guild in bot.guilds:
        try:
            invites[guild.id] = await guild.invites()
        except:
            pass
    print(f'👑 King {bot.user.name} je spreman!')

# --- AUTOMATSKO DODELJIVANJE ROLE I DOBRODOŠLICA ---
@bot.event
async def on_member_join(member):
    # Dodeljivanje role [ 👤 ] MEMBER
    role = discord.utils.get(member.guild.roles, name="[ 👤 ] MEMBER")
    if role:
        try:
            await member.add_roles(role)
        except:
            print(f"Greška: Ne mogu da dodelim rolu {member.name}")

    # Dobrodošlica
    channel = discord.utils.get(member.guild.text_channels, name="📍┃dobrodoslica")
    if channel:
        embed = discord.Embed(
            title="👑 NOVI CLAN JE STIGAO!",
            description=f"Dobrodošao brate {member.mention} u **Kings Of Reselling**! 🚀\n\nSpremi se za najjači reselling na Balkanu!",
            color=KING_COLOR
        )
        embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
        embed.set_footer(text=FOOTER_TEXT)
        await channel.send(embed=embed)

# --- SKRIVENA KOMANDA: SAY (Samo za tebe) ---
@bot.command(hidden=True)
@commands.is_owner() # Samo vlasnik bota (ti) može ovo
async def say(ctx, *, poruka):
    await ctx.message.delete() # Briše tvoju poruku &say...
    embed = discord.Embed(description=poruka, color=KING_COLOR)
    embed.set_footer(text=FOOTER_TEXT)
    await ctx.send(embed=embed)

# --- MODERACIJA ---

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason="Nije naveden"):
    await member.kick(reason=reason)
    embed = discord.Embed(title="🚀 IZBAČEN SA DVORA", description=f"Korisnik {member.mention} je lansiran!\n\n**📝 Razlog:** {reason}", color=0xffa500)
    embed.set_footer(text=FOOTER_TEXT)
    await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason="Nije naveden"):
    await member.ban(reason=reason)
    embed = discord.Embed(title="🔨 TRAJNO PROTERAN", description=f"Korisnik {member.mention} je proteran!\n\n**📝 Razlog:** {reason}", color=0xff0000)
    embed.set_footer(text=FOOTER_TEXT)
    await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, id: int):
    user = await bot.fetch_user(id)
    await ctx.guild.unban(user)
    embed = discord.Embed(title="🔓 POVRATAK NA DVOR", description=f"Korisnik **{user.name}** je pomilovan!", color=0x00ff00)
    embed.set_footer(text=FOOTER_TEXT)
    await ctx.send(embed=embed)

# --- STATISTIKA I INFO ---

@bot.command()
async def userinfo(ctx, member: discord.Member = None):
    target = member if member else ctx.author
    embed = discord.Embed(title=f"👤 INFO: {target.name}", color=KING_COLOR)
    embed.add_field(name="ID", value=target.id, inline=True)
    embed.add_field(name="Nalog napravljen", value=target.created_at.strftime("%d.%m.%Y"), inline=True)
    embed.add_field(name="Ušao na server", value=target.joined_at.strftime("%d.%m.%Y"), inline=True)
    embed.set_thumbnail(url=target.avatar.url if target.avatar else target.default_avatar.url)
    embed.set_footer(text=FOOTER_TEXT)
    await ctx.send(embed=embed)

@bot.command()
async def serverinfo(ctx):
    embed = discord.Embed(title=f"🏰 {ctx.guild.name} STATS", color=KING_COLOR)
    embed.add_field(name="👥 Članova", value=ctx.guild.member_count, inline=True)
    embed.add_field(name="💎 Boostovi", value=ctx.guild.premium_subscription_count, inline=True)
    embed.add_field(name="👑 Vlasnik", value=ctx.guild.owner.mention, inline=True)
    embed.set_footer(text=FOOTER_TEXT)
    await ctx.send(embed=embed)

@bot.command()
async def avatar(ctx, member: discord.Member = None):
    target = member if member else ctx.author
    embed = discord.Embed(title=f"🖼️ AVATAR: {target.name}", color=KING_COLOR)
    embed.set_image(url=target.avatar.url if target.avatar else target.default_avatar.url)
    embed.set_footer(text=FOOTER_TEXT)
    await ctx.send(embed=embed)

@bot.command()
async def ping(ctx):
    embed = discord.Embed(description=f"🏓 **Pong!** Brzina bota: **{round(bot.latency * 1000)}ms**", color=KING_COLOR)
    embed.set_footer(text=FOOTER_TEXT)
    await ctx.send(embed=embed)

# --- OSTALO ---

@bot.command()
async def poll(ctx, *, pitanje):
    embed = discord.Embed(title="📊 GLASANJE", description=pitanje, color=KING_COLOR)
    embed.set_footer(text=f"Pokrenuo: {ctx.author.name} | {FOOTER_TEXT}")
    msg = await ctx.send(embed=embed)
    await msg.add_reaction("👍")
    await msg.add_reaction("👎")

@bot.command()
async def help(ctx):
    embed = discord.Embed(title="📜 KRALJEVSKE KOMANDE", color=KING_COLOR)
    embed.add_field(name="🛡️ Moderacija", value="`&kick`, `&ban`, `&unban [ID]`, `&clear`, `&lock`, `&unlock`", inline=False)
    embed.add_field(name="📊 Statistika", value="`&userinfo`, `&serverinfo`, `&avatar`, `&ping`", inline=False)
    embed.add_field(name="📈 Invites", value="`&invite`, `&invitelab`", inline=False)
    embed.add_field(name="🎉 Zabava", value="`&giveaway`, `&poll`", inline=False)
    embed.set_footer(text=FOOTER_TEXT)
    await ctx.send(embed=embed)

# --- STARE KOMANDE (LOCK, CLEAR, GIVEAWAY, INVITE) ---
# (Zadržane iz tvog koda, samo ubačen FOOTER_TEXT)

@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount + 1)
    embed = discord.Embed(description=f"🧹 Obrisao sam **{amount}** poruka, Cepaj dalje!", color=0x3498db)
    embed.set_footer(text=FOOTER_TEXT)
    await ctx.send(embed=embed, delete_after=5)

@bot.command()
@commands.has_permissions(manage_channels=True)
async def lock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
    embed = discord.Embed(title="🔒 KANAL JE ZAKLJUČAN", description="Brate, ovde trenutno ne moze da se pise.", color=0xff0000)
    embed.set_footer(text=FOOTER_TEXT)
    await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(manage_channels=True)
async def unlock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
    embed = discord.Embed(title="🔓 KANAL JE OTKLJUČAN", description="Prodaja i zabava mogu da se nastave!", color=0x00ff00)
    embed.set_footer(text=FOOTER_TEXT)
    await ctx.send(embed=embed)

# (Ovde idu get_invites_count, invite, invitelab i giveaway koje si već imao)
# Skratio sam da bi stalo, ali obavezno ubaci svoje stare funkcije za invajmove ako želiš!

keep_alive()
bot.run(os.getenv('DISCORD_TOKEN'))
