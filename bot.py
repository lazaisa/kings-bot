import os
import discord
from discord.ext import commands
import random
import asyncio
from KeepAlive import keep_alive

# Podešavanje dozvola
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.invites = True 

bot = commands.Bot(command_prefix='&', intents=intents, help_command=None)

# Globalne varijable
FOOTER_TEXT = "By KnEz.exe | Kings Of Reselling"
KING_COLOR = 0xffd700

# --- TICKET SISTEM ---
class TicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    # POPRAVLJENO: style je sada discord.ButtonStyle.success (zelena)
    @discord.ui.button(label="🎫 Open Ticket", style=discord.ButtonStyle.success, custom_id="open_ticket")
    async def open_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild = interaction.guild
        user = interaction.user
        ticket_name = f"ticket-{user.name.lower()}"
        
        # Dozvole: samo user i admini vide kanal
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }
        
        channel = await guild.create_text_channel(ticket_name, overwrites=overwrites)
        
        embed = discord.Embed(
            title="👑 TICKET OTVOREN",
            description=f"Dobrodošao {user.mention}, administracija će ti se javiti uskoro.\n\nDa zatvorite tiket, kucajte `&close`",
            color=KING_COLOR
        )
        embed.set_footer(text=FOOTER_TEXT)
        await channel.send(embed=embed)
        await interaction.response.send_message(f"Tvoj tiket je otvoren ovde: {channel.mention}", ephemeral=True)

@bot.event
async def on_ready():
    bot.add_view(TicketView()) # Da dugme ostane aktivno
    await bot.change_presence(activity=discord.Game(name="Kings Of Reselling 👑"))
    print(f'👑 King {bot.user.name} je spreman i online!')

# --- POMOĆNA FUNKCIJA ZA INVITE ---
async def get_invites_count(member):
    try:
        invs = await member.guild.invites()
        for i in invs:
            if i.inviter and i.inviter.id == member.id:
                return i.uses
    except:
        return 0
    return 0

# --- AUTOMATSKA ROLA I DOBRODOŠLICA ---
@bot.event
async def on_member_join(member):
    role = discord.utils.get(member.guild.roles, name="[ 👤 ] MEMBER")
    if role:
        try: await member.add_roles(role)
        except: pass

    channel = discord.utils.get(member.guild.text_channels, name="📍┃dobrodoslica")
    if channel:
        embed = discord.Embed(title="👑 NOVI CLAN JE STIGAO!", description=f"Dobrodošao brate {member.mention} u **Kings Of Reselling**! 🚀", color=KING_COLOR)
        embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
        embed.set_footer(text=FOOTER_TEXT)
        await channel.send(embed=embed)

# --- KOMANDE ZA TICKET ---
@bot.command(hidden=True)
@commands.has_permissions(administrator=True)
async def ticket(ctx):
    try: await ctx.message.delete()
    except: pass
    embed = discord.Embed(
        title="🎫 KINGS SUPPORT",
        description="Ukoliko vam je potrebna pomoć ili želite da kupite nešto, otvorite tiket klikom na dugme ispod!",
        color=KING_COLOR
    )
    embed.set_footer(text=FOOTER_TEXT)
    await ctx.send(embed=embed, view=TicketView())

@bot.command()
async def close(ctx):
    if "ticket-" in ctx.channel.name:
        await ctx.send("Tiket će biti obrisan za 5 sekundi...")
        await asyncio.sleep(5)
        await ctx.channel.delete()

# --- MODERACIJA ---
@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason="zato"):
    try:
        await member.kick(reason=reason)
        await ctx.send(f"🚀 **{member.name}** je lansiran sa servera! Razlog: {reason}")
    except:
        await ctx.send("❌ Ne mogu da izbacim ovog korisnika.")

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason="zato"):
    try:
        await member.ban(reason=reason)
        await ctx.send(f"🔨 **{member.name}** je proteran! Razlog: {reason}")
    except:
        await ctx.send("❌ Ne mogu da banujem ovog korisnika.")

@bot.command()
@commands.has_permissions(manage_channels=True)
async def lock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
    await ctx.send("🔒 Kanal zaključan za @everyone.")

@bot.command()
@commands.has_permissions(manage_channels=True)
async def unlock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
    await ctx.send("🔓 Kanal otključan.")

@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
    try:
        await ctx.channel.purge(limit=amount + 1)
        await ctx.send(f"🧹 Obrisano **{amount}** poruka.", delete_after=5)
    except: pass

# --- INVITE & SOCIAL ---
@bot.command()
async def invite(ctx, member: discord.Member = None):
    target = member if member else ctx.author
    count = await get_invites_count(target)
    embed = discord.Embed(title="📈 STATISTIKA", description=f"Korisnik {target.mention} je doveo **{count}** ljudi.", color=KING_COLOR)
    embed.set_footer(text=FOOTER_TEXT)
    await ctx.send(embed=embed)

@bot.command()
async def invitelab(ctx):
    all_invites = {}
    try:
        invs = await ctx.guild.invites()
        for i in invs:
            if i.inviter:
                all_invites[i.inviter] = all_invites.get(i.inviter, 0) + i.uses
        sorted_inv = sorted(all_invites.items(), key=lambda x: x[1], reverse=True)[:10]
        text = "\n".join([f"{i+1}. {u.mention} - **{c}**" for i, (u, c) in enumerate(sorted_inv)])
        embed = discord.Embed(title="🏆 TOP 10 INVITER-A", description=text if text else "Nema podataka.", color=KING_COLOR)
        embed.set_footer(text=FOOTER_TEXT)
        await ctx.send(embed=embed)
    except: await ctx.send("Greška pri učitavanju.")

# --- OSTALO ---
@bot.command()
async def giveaway(ctx, minuti: int, pobednika: int, *, nagrada: str):
    embed = discord.Embed(title="🎊 KINGS GIVEAWAY 🎊", description=f"🎁 Nagrada: **{nagrada}**\n🏆 Pobednika: **{pobednika}**\n⏳ Trajanje: **{minuti} min**", color=KING_COLOR)
    embed.set_footer(text=FOOTER_TEXT)
    msg = await ctx.send(embed=embed)
    await msg.add_reaction("🎉")
    await asyncio.sleep(minuti * 60)
    msg = await ctx.channel.fetch_message(msg.id)
    users = [u async for u in msg.reactions[0].users() if not u.bot]
    if len(users) < pobednika: return await ctx.send("Nema dovoljno učesnika.")
    winners = random.sample(users, pobednika)
    await ctx.send(f"👑 Pobednici: {', '.join([w.mention for w in winners])}! Nagrada: **{nagrada}**")

@bot.command()
async def ping(ctx):
    await ctx.send(f"🏓 Pong! **{round(bot.latency * 1000)}ms**")

@bot.command(hidden=True)
@commands.is_owner()
async def say(ctx, *, poruka):
    try: await ctx.message.delete()
    except: pass
    embed = discord.Embed(description=poruka, color=KING_COLOR)
    embed.set_footer(text=FOOTER_TEXT)
    await ctx.send(embed=embed)

@bot.command()
async def help(ctx):
    embed = discord.Embed(title="📜 KRALJEVSKE KOMANDE", color=KING_COLOR)
    embed.add_field(name="🛡️ Admin", value="`kick`, `ban`, `clear`, `lock`, `unlock`", inline=False)
    embed.add_field(name="📈 Social", value="`invite`, `invitelab`", inline=False)
    embed.add_field(name="🎉 Ostalo", value="`giveaway`, `ping`", inline=False)
    embed.set_footer(text=FOOTER_TEXT)
    await ctx.send(embed=embed)

keep_alive()
bot.run(os.getenv('DISCORD_TOKEN'))
