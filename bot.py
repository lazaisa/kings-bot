import discord
from discord.ext import commands
import random
import asyncio
from KeepAlive import keep_alive

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='&', intents=intents, help_command=None)

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="Kings Of Reselling 👑"))
    print(f'👑 King {bot.user.name} je spreman!')

# --- AUTOMATSKA DOBRODOŠLICA ---
@bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name="welcome") # Promeni ime u kanal koji imas
    if channel:
        embed = discord.Embed(
            title="👑 NOVI KRALJ JE STIGAO!",
            description=f"Dobrodošao brate {member.mention} u **Kings Of Reselling**! 🚀\n\nSpremi se za najjači reselling na Balkanu!",
            color=0xffd700
        )
        embed.set_thumbnail(url=member.avatar.url if member.avatar else None)
        embed.set_footer(text="Kreator bota: KnEz.exe")
        await channel.send(embed=embed)

# --- LOCK / UNLOCK ---
@bot.command()
@commands.has_permissions(manage_channels=True)
async def lock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
    embed = discord.Embed(title="🔒 KANAL JE ZAKLJUČAN", description="Brate, ovde je trenutno tišina. Samo administracija može da piše! 🤫", color=0xff0000)
    await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(manage_channels=True)
async def unlock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
    embed = discord.Embed(title="🔓 KANAL JE OTKLJUČAN", description="Vatru pali, prodaja može da se nastavi! Pišite slobodno. 🔥", color=0x00ff00)
    await ctx.send(embed=embed)

# --- GIVEAWAY (Sa brojem pobednika) ---
@bot.command()
async def giveaway(ctx, minuti: int, pobednika: int, *, nagrada: str):
    embed = discord.Embed(
        title="🎊 KINGS GIVEAWAY 🎊",
        description=f"🎁 Nagrada: **{nagrada}**\n🏆 Broj pobednika: **{pobednika}**\n⏳ Trajanje: **{minuti} min**\n\nReagujte sa 🎉 da učestvujete!",
        color=0xffd700
    )
    msg = await ctx.send(embed=embed)
    await msg.add_reaction("🎉")
    await asyncio.sleep(minuti * 60)
    
    new_msg = await ctx.channel.fetch_message(msg.id)
    users = [user for user in await new_msg.reactions[0].users().flatten() if not user.bot]
    
    if len(users) < pobednika:
        await ctx.send("Nema dovoljno ljudi za izvlačenje! ❌")
        return

    winners = random.sample(users, pobednika)
    winner_mentions = ", ".join([w.mention for w in winners])
    
    win_embed = discord.Embed(
        title="👑 IMAMO POBEDNIKE! 👑",
        description=f"Čestitamo kraljevi: {winner_mentions}\nOsvojili ste: **{nagrada}**! 🏆",
        color=0x00ff00
    )
    await ctx.send(embed=win_embed)

# --- HELP KOMANDA (Visual Update) ---
@bot.command()
async def help(ctx):
    embed = discord.Embed(title="📜 KRALJEVSKE KOMANDE", color=0xffd700)
    embed.add_field(name="🛡️ Moderacija", value="`&kick`, `&ban`, `&clear`, `&lock`, `&unlock`", inline=False)
    embed.add_field(name="🎉 Zabava", value="`&giveaway [min] [pobednici] [nagrada]`", inline=False)
    embed.add_field(name="📈 Ostalo", value="`&invite`, `&help`", inline=False)
    embed.set_footer(text="By KnEz.exe | Kings Of Reselling")
    await ctx.send(embed=embed)

# --- MODERACIJA OSTALO ---
@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason="Nije naveden"):
    await member.kick(reason=reason)
    await ctx.send(f"🚀 **{member.name}** je lansiran sa servera! Razlog: {reason}")

@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount + 1)
    embed = discord.Embed(description=f"🧹 Obrisao sam **{amount}** poruka, brate. Čisto ko suza!", color=0x3498db)
    await ctx.send(embed=embed, delete_after=5)

keep_alive()
bot.run('OVDE_ZALEPITE_VAS_TOKEN')
