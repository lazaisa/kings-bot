import os
import discord
from discord.ext import commands
import random
import asyncio
from KeepAlive import keep_alive

# Intenti za dozvole
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.invites = True 

bot = commands.Bot(command_prefix='&', intents=intents, help_command=None)

# Konstante
FOOTER_TEXT = "By KnEz.exe | Kings Of Reselling"
KING_COLOR = 0xffd700

# --- TICKET SISTEM ---
class TicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="🎫 Open Ticket", style=discord.ButtonStyle.success, custom_id="open_ticket")
    async def open_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild = interaction.guild
        user = interaction.user
        ticket_name = f"ticket-{user.name.lower()}"
        
        # Provera da li već postoji kanal sa tim imenom da ne pravi duplikate
        existing_channel = discord.utils.get(guild.text_channels, name=ticket_name)
        if existing_channel:
            return await interaction.response.send_message(f"Već imaš otvoren tiket ovde: {existing_channel.mention}", ephemeral=True)

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }
        
        channel = await guild.create_text_channel(ticket_name, overwrites=overwrites)
        
        embed = discord.Embed(
            title="👑 Kings Of Reselling SUPPORT",
            description=f"Dobrodošao {user.mention}!\nSačekaj trenutak, administracija će ti se javiti.\n\nDa zatvoriš ovaj tiket, kucaj `&close`",
            color=KING_COLOR
        )
        embed.set_footer(text=FOOTER_TEXT)
        await channel.send(embed=embed)
        await interaction.response.send_message(f"Tiket otvoren: {channel.mention}", ephemeral=True)

@bot.event
async def on_ready():
    bot.add_view(TicketView())
    await bot.change_presence(activity=discord.Game(name="Kings Of Reselling 👑"))
    print(f'👑 King {bot.user.name} je spreman i stabilan!')

# --- AUTOMATSKA ROLA ---
@bot.event
async def on_member_join(member):
    role = discord.utils.get(member.guild.roles, name="[ 👤 ] MEMBER")
    if role:
        try: await member.add_roles(role)
        except: pass

# --- MODERACIJA ---
@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason="///"):
    try:
        await member.kick(reason=reason)
        await ctx.send(f"🚀 **{member.name}** je lansiran! Razlog: {reason}")
    except: await ctx.send("❌ Nemam dozvolu da izbacim tog korisnika.")

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason="///"):
    try:
        await member.ban(reason=reason)
        await ctx.send(f"🔨 **{member.name}** je banovan! Razlog: {reason}")
    except: await ctx.send("❌ Nemam dozvolu da banujem tog korisnika.")

@bot.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, id: int):
    try:
        user = await bot.fetch_user(id)
        await ctx.guild.unban(user)
        await ctx.send(f"🔓 Korisnik **{user.name}** je unbanovan!")
    except: await ctx.send("❌ Ne mogu da nađem tog korisnika na ban listi.")

@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
    try:
        await ctx.channel.purge(limit=amount + 1)
        await ctx.send(f"🧹 Obrisano **{amount}** poruka.", delete_after=5)
    except discord.errors.HTTPException:
        await ctx.send("⚠️ Ne mogu da obrišem poruke starije od 14 dana ili me Discord usporava.")

@bot.command()
@commands.has_permissions(manage_channels=True)
async def lock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
    await ctx.send("🔒 Kanal je zaključan.")

@bot.command()
@commands.has_permissions(manage_channels=True)
async def unlock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
    await ctx.send("🔓 Kanal je otključan.")

# --- TICKET KOMANDE ---
@bot.command(hidden=True)
@commands.has_permissions(administrator=True)
async def ticket(ctx):
    try: await ctx.message.delete()
    except: pass
    embed = discord.Embed(
        title="🎫 KINGS SUPPORT",
        description="Ukoliko vam je potrebna pomoć ili želite nešto da kupite, otvorite tiket klikom na dugme ispod!",
        color=KING_COLOR
    )
    embed.set_footer(text=FOOTER_TEXT)
    await ctx.send(embed=embed, view=TicketView())

@bot.command()
async def close(ctx):
    if "ticket-" in ctx.channel.name or ctx.channel.name.startswith("ticket"):
        await ctx.send("Ovaj tiket će biti obrisan za par sekundi...")
        await asyncio.sleep(3)
        await ctx.channel.delete()

# --- SOCIAL & INFO ---
@bot.command()
async def invite(ctx, member: discord.Member = None):
    target = member if member else ctx.author
    try:
        invs = await ctx.guild.invites()
        count = sum(i.uses for i in invs if i.inviter and i.inviter.id == target.id)
        await ctx.send(f"📈 {target.mention} ima **{count}** invajtova.")
    except: await ctx.send("❌ Nemam dozvolu da vidim invajtove.")

@bot.command()
async def ping(ctx):
    await ctx.send(f"🏓 Pong! Latencija: **{round(bot.latency * 1000)}ms**")

@bot.command()
async def help(ctx):
    embed = discord.Embed(title="📜 KRALJEVSKE KOMANDE", color=KING_COLOR)
    embed.add_field(name="🛡️ Moderacija", value="`kick`, `ban`, `unban [ID]`, `clear`, `lock`, `unlock`", inline=False)
    embed.add_field(name="📈 Statistika", value="`invite`, `ping`", inline=False)
    embed.add_field(name="🎉 Zabava", value="`giveaway`", inline=False)
    embed.set_footer(text=FOOTER_TEXT)
    await ctx.send(embed=embed)

@bot.command()
async def giveaway(ctx, minuti: int, pobednika: int, *, nagrada: str):
    embed = discord.Embed(title="🎊 GIVEAWAY 🎊", description=f"🎁 Nagrada: **{nagrada}**\n🏆 Pobednika: **{pobednika}**", color=KING_COLOR)
    msg = await ctx.send(embed=embed)
    await msg.add_reaction("🎉")
    await asyncio.sleep(minuti * 60)
    msg = await ctx.channel.fetch_message(msg.id)
    users = [u async for u in msg.reactions[0].users() if not u.bot]
    if len(users) < pobednika: return await ctx.send("Nema dovoljno učesnika.")
    winners = random.sample(users, pobednika)
    await ctx.send(f"👑 Čestitamo {', '.join([w.mention for w in winners])}! Osvojili ste **{nagrada}**!")

keep_alive()
bot.run(os.getenv('DISCORD_TOKEN'))
