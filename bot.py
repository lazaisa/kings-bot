import os
import discord
from discord.ext import commands
import random
import asyncio
from KeepAlive import keep_alive

# Podešavanje dozvola (Intents)
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.invites = True 

bot = commands.Bot(command_prefix='&', intents=intents, help_command=None)

# Globalne varijable
FOOTER_TEXT = "By KnEz.exe | Kings Of Reselling"
KING_COLOR = 0xffd700

# --- SISTEM ZA INVITE ---
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="Kings Of Reselling 👑"))
    print(f'👑 King {bot.user.name} je spreman!')

async def get_invites_count(member):
    total = 0
    try:
        invs = await member.guild.invites()
        for i in invs:
            if i.inviter and i.inviter.id == member.id:
                total += i.uses
    except:
        pass
    return total

# --- AUTOMATSKA ROLA I DOBRODOŠLICA ---
@bot.event
async def on_member_join(member):
    # 1. Dodeljivanje role
    role = discord.utils.get(member.guild.roles, name="[ 👤 ] MEMBER")
    if role:
        try:
            await member.add_roles(role)
        except:
            print(f"Greška: Bot nema dozvolu da dodeli rolu!")

    # 2. Poruka dobrodošlice
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

# --- INVITE KOMANDE ---
@bot.command()
async def invite(ctx, member: discord.Member = None):
    target = member if member else ctx.author
    count = await get_invites_count(target)
    bot_link = f"https://discord.com/oauth2/authorize?client_id={bot.user.id}&permissions=8&scope=bot"
    
    embed = discord.Embed(title="📈 INVITE STATISTIKA", color=KING_COLOR)
    embed.add_field(name="Korisnik", value=target.mention, inline=True)
    embed.add_field(name="Broj ljudi", value=f"**{count}**", inline=True)
    embed.add_field(name="Pozovi bota", value=f"[KLIKNI OVDE]({bot_link})", inline=False)
    embed.set_footer(text=FOOTER_TEXT)
    await ctx.send(embed=embed)

@bot.command()
async def invitelab(ctx):
    all_invites = {}
    try:
        current_invites = await ctx.guild.invites()
        for inv in current_invites:
            if inv.inviter:
                all_invites[inv.inviter] = all_invites.get(inv.inviter, 0) + inv.uses
    except:
        return await ctx.send("Nemam dozvolu da vidim invajtove! ❌")

    sorted_invites = sorted(all_invites.items(), key=lambda x: x[1], reverse=True)[:10]
    lb_text = ""
    for i, (user, count) in enumerate(sorted_invites, 1):
        lb_text += f"{i}. {user.mention} - **{count}** invajta\n"
    
    embed = discord.Embed(title="🏆 TOP 10 INVITER-A", description=lb_text if lb_text else "Nema podataka.", color=KING_COLOR)
    embed.set_footer(text=FOOTER_TEXT)
    await ctx.send(embed=embed)

# --- MODERACIJA ---
@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason="Nije naveden"):
    await member.kick(reason=reason)
    embed = discord.Embed(title="🚀 IZBAČEN SA SERVERA", description=f"Korisnik {member.mention} je lansiran!\n**Razlog:** {reason}", color=0xffa500)
    embed.set_footer(text=FOOTER_TEXT)
    await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason="Nije naveden"):
    await member.ban(reason=reason)
    embed = discord.Embed(title="🔨 TRAJNO IZBACEN", description=f"Korisnik {member.mention} je izbacen!\n**Razlog:** {reason}", color=0xff0000)
    embed.set_footer(text=FOOTER_TEXT)
    await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, id: int):
    user = await bot.fetch_user(id)
    await ctx.guild.unban(user)
    embed = discord.Embed(title="🔓 POVRATAK", description=f"Korisnik **{user.name}** je pomilovan!", color=0x00ff00)
    embed.set_footer(text=FOOTER_TEXT)
    await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(manage_channels=True)
async def lock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
    embed = discord.Embed(title="🔒 KANAL ZAKLJUČAN", description="Samo administracija može da piše! 🤫", color=0xff0000)
    embed.set_footer(text=FOOTER_TEXT)
    await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(manage_channels=True)
async def unlock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
    embed = discord.Embed(title="🔓 KANAL OTKLJUČAN", description="Svi mogu ponovo da pišu! 🔥", color=0x00ff00)
    embed.set_footer(text=FOOTER_TEXT)
    await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount + 1)
    embed = discord.Embed(description=f"🧹 Obrisao sam **{amount}** poruka!", color=0x3498db)
    embed.set_footer(text=FOOTER_TEXT)
    await ctx.send(embed=embed, delete_after=5)

# --- GIVEAWAY ---
@bot.command()
async def giveaway(ctx, minuti: int, pobednika: int, *, nagrada: str):
    embed = discord.Embed(title="🎊 Kings Of Reselling GiveAway 🎊", description=f"🎁 Nagrada: **{nagrada}**\n🏆 Pobednika: **{pobednika}**\n⏳ Trajanje: **{minuti} min**", color=KING_COLOR)
    embed.set_footer(text=FOOTER_TEXT)
    msg = await ctx.send(embed=embed)
    await msg.add_reaction("🎉")
    await asyncio.sleep(minuti * 60)
    new_msg = await ctx.channel.fetch_message(msg.id)
    users = [user async for user in new_msg.reactions[0].users() if not user.bot]
    if len(users) < pobednika:
        return await ctx.send("Nema dovoljno učesnika! ❌")
    winners = random.sample(users, pobednika)
    mentions = ", ".join([w.mention for w in winners])
    win_embed = discord.Embed(title="👑 POBEDNIK!", description=f"Čestitamo: {mentions}\nNagrada: **{nagrada}**!", color=0x00ff00)
    win_embed.set_footer(text=FOOTER_TEXT)
    await ctx.send(embed=win_embed)

# --- INFO KOMANDE ---
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
async def ping(ctx):
    embed = discord.Embed(description=f"🏓 **Pong!** {round(bot.latency * 1000)}ms", color=KING_COLOR)
    embed.set_footer(text=FOOTER_TEXT)
    await ctx.send(embed=embed)

@bot.command()
async def poll(ctx, *, pitanje):
    embed = discord.Embed(title="📊 GLASANJE", description=pitanje, color=KING_COLOR)
    embed.set_footer(text=FOOTER_TEXT)
    msg = await ctx.send(embed=embed)
    await msg.add_reaction("👍")
    await msg.add_reaction("👎")

@bot.command(hidden=True)
@commands.is_owner()
async def say(ctx, *, poruka):
    await ctx.message.delete()
    embed = discord.Embed(description=poruka, color=KING_COLOR)
    embed.set_footer(text=FOOTER_TEXT)
    await ctx.send(embed=embed)

@bot.command()
async def help(ctx):
    embed = discord.Embed(title="📜 KRALJEVSKE KOMANDE", color=KING_COLOR)
    embed.add_field(name="🛡️ Admin", value="`&kick`, `&ban`, `&unban`, `&clear`, `&lock`, `&unlock`", inline=False)
    embed.add_field(name="📊 Info", value="`&userinfo`, `&serverinfo`, `&ping`", inline=False)
    embed.add_field(name="📈 Social", value="`&invite`, `&invitelab`", inline=False)
    embed.add_field(name="🎉 Fun", value="`&giveaway`, `&poll`", inline=False)
    embed.set_footer(text=FOOTER_TEXT)
    await ctx.send(embed=embed)

keep_alive()
bot.run(os.getenv('DISCORD_TOKEN'))
