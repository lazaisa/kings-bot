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

# Footer tekst da ne pišemo stalno isto
FOOTER_TEXT = "By KnEz.exe | Kings Of Reselling"

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

async def get_invites_count(member):
    total_invites = 0
    for guild in bot.guilds:
        try:
            guild_invites = await guild.invites()
            for invite in guild_invites:
                if invite.inviter and invite.inviter.id == member.id:
                    total_invites += invite.uses
        except:
            continue
    return total_invites

@bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name="📍┃dobrodoslica")
    if channel:
        embed = discord.Embed(
            title="👑 NOVI CLAN JE STIGAO!",
            description=f"Dobrodošao brate {member.mention} u **Kings Of Reselling**! 🚀\n\nSpremi se za najjači reselling na Balkanu!",
            color=0xffd700
        )
        embed.set_thumbnail(url=member.avatar.url if member.avatar else None)
        embed.set_footer(text=FOOTER_TEXT) # Dodat footer
        await channel.send(embed=embed)

@bot.command()
async def invite(ctx, member: discord.Member = None):
    target = member if member else ctx.author
    count = await get_invites_count(target)
    bot_link = "https://discord.com/oauth2/authorize?client_id=1479767434167849111&permissions=8&scope=bot"
    
    embed = discord.Embed(title="📈 INVITE STATISTIKA", color=0xffd700)
    embed.add_field(name="Korisnik", value=target.mention, inline=True)
    embed.add_field(name="Broj ljudi koje je doveo", value=f"**{count}**", inline=True)
    embed.add_field(name="Pozovi bota na svoj server", value=f"[KLIKNI OVDE]({bot_link})", inline=False)
    embed.set_footer(text=FOOTER_TEXT) # Dodat footer
    await ctx.send(embed=embed)

@bot.command()
async def invitelab(ctx):
    all_members = {}
    for guild in bot.guilds:
        try:
            guild_invites = await guild.invites()
            for inv in guild_invites:
                if inv.inviter:
                    all_members[inv.inviter] = all_members.get(inv.inviter, 0) + inv.uses
        except:
            continue
            
    sorted_invites = sorted(all_members.items(), key=lambda x: x[1], reverse=True)[:10]
    lb_text = ""
    for i, (user, count) in enumerate(sorted_invites, 1):
        lb_text += f"{i}. {user.mention} - **{count}** invajta\n"
    
    embed = discord.Embed(title="🏆 TOP 10 INVITER-A", description=lb_text if lb_text else "Još uvek nema podataka.", color=0xffd700)
    embed.set_footer(text=FOOTER_TEXT) # Dodat footer
    await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(manage_channels=True)
async def lock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
    embed = discord.Embed(title="🔒 KANAL JE ZAKLJUČAN", description="Ovde trenutno ne moze da se pise. Samo administracija može da piše! 🤫", color=0xff0000)
    embed.set_footer(text=FOOTER_TEXT) # Dodat footer
    await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(manage_channels=True)
async def unlock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
    embed = discord.Embed(title="🔓 KANAL JE OTKLJUČAN", description="Prodaja i zabava mogu da se nastave! Pišite slobodno. 🔥", color=0x00ff00)
    embed.set_footer(text=FOOTER_TEXT) # Dodat footer
    await ctx.send(embed=embed)

@bot.command()
async def giveaway(ctx, minuti: int, pobednika: int, *, nagrada: str):
    embed = discord.Embed(
        title="🎊 Kings Of Reselling GIVEAWAY 🎊",
        description=f"🎁 Nagrada: **{nagrada}**\n🏆 Broj pobednika: **{pobednika}**\n⏳ Trajanje: **{minuti} min**\n\nReagujte sa 🎉 da učestvujete!",
        color=0xffd700
    )
    embed.set_footer(text=FOOTER_TEXT) # Dodat footer
    msg = await ctx.send(embed=embed)
    await msg.add_reaction("🎉")
    await asyncio.sleep(minuti * 60)
    
    new_msg = await ctx.channel.fetch_message(msg.id)
    users = [user async for user in new_msg.reactions[0].users() if not user.bot]
    
    if len(users) < pobednika:
        await ctx.send(f"Nema dovoljno ljudi za izvlačenje (potrebno {pobednika})! ❌")
        return

    winners = random.sample(users, pobednika)
    winner_mentions = ", ".join([w.mention for w in winners])
    
    win_embed = discord.Embed(
        title="👑 IMAMO POBEDNIKE! 👑",
        description=f"Čestitamo kraljevi: {winner_mentions}\nOsvojili ste: **{nagrada}**! 🏆",
        color=0x00ff00
    )
    win_embed.set_footer(text=FOOTER_TEXT) # Dodat footer
    await ctx.send(embed=win_embed)

@bot.command()
async def help(ctx):
    embed = discord.Embed(title="📜 KRALJEVSKE KOMANDE", color=0xffd700)
    embed.add_field(name="🛡️ Moderacija", value="`&kick`, `&ban`, `&clear`, `&lock`, `&unlock`", inline=False)
    embed.add_field(name="🎉 Zabava", value="`&giveaway [min] [pobednici] [nagrada]`", inline=False)
    embed.add_field(name="📈 Statistička", value="`&invite [@korisnik]`, `&invitelab`", inline=False)
    embed.set_footer(text=FOOTER_TEXT) # Dodat footer
    await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount + 1)
    embed = discord.Embed(description=f"🧹 Obrisano **{amount}** poruka, Cepaj dalje!", color=0x3498db)
    embed.set_footer(text=FOOTER_TEXT) # Dodat footer
    await ctx.send(embed=embed, delete_after=5)

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason="Nije naveden"):
    await member.kick(reason=reason)
    await ctx.send(f"🚀 **{member.name}** je lansiran sa servera! Razlog: {reason}")

keep_alive()
bot.run(os.getenv('DISCORD_TOKEN'))
