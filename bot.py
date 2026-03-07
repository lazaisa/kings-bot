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

    @discord.ui.button(label="🎫 Open Ticket", style=discord.ButtonStyle.success, custom_id="open_ticket")
    async def open_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild = interaction.guild
        user = interaction.user
        ticket_name = f"ticket-{user.name.lower()}"
        
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
    bot.add_view(TicketView())
    await bot.change_presence(activity=discord.Game(name="Kings Of Reselling 👑"))
    print(f'👑 King {bot.user.name} je spreman!')

# --- AUTOMATSKA ROLA ---
@bot.event
async def on_member_join(member):
    role = discord.utils.get(member.guild.roles, name="[ 👤 ] MEMBER")
    if role:
        try: await member.add_roles(role)
        except: pass

# --- MODERACIJA (SA UNBAN KOMANDOM) ---
@bot.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, id: int):
    try:
        user = await bot.fetch_user(id)
        await ctx.guild.unban(user)
        embed = discord.Embed(title="🔓 POVRATAK", description=f"Korisnik **{user.name}** je pomilovan!", color=0x00ff00)
        embed.set_footer(text=FOOTER_TEXT)
        await ctx.send(embed=embed)
    except:
        await ctx.send("❌ Korisnik sa tim ID-em nije pronađen na ban listi.")

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason="zato"):
    try:
        await member.kick(reason=reason)
        await ctx.send(f"🚀 **{member.name}** je lansiran! Razlog: {reason}")
    except: pass

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason="zato"):
    try:
        await member.ban(reason=reason)
        await ctx.send(f"🔨 **{member.name}** je proteran! Razlog: {reason}")
    except: pass

@bot.command()
@commands.has_permissions(manage_channels=True)
async def lock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
    await ctx.send("🔒 Kanal zaključan.")

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

# --- OSTALO ---
@bot.command(hidden=True)
@commands.has_permissions(administrator=True)
async def ticket(ctx):
    try: await ctx.message.delete()
    except: pass
    embed = discord.Embed(title="🎫 KINGS SUPPORT", description="Kliknite na dugme ispod za pomoć!", color=KING_COLOR)
    embed.set_footer(text=FOOTER_TEXT)
    await ctx.send(embed=embed, view=TicketView())

@bot.command()
async def close(ctx):
    if "ticket-" in ctx.channel.name:
        await ctx.send("Tiket se gasi...")
        await asyncio.sleep(3)
        await ctx.channel.delete()

@bot.command()
async def invite(ctx, member: discord.Member = None):
    target = member if member else ctx.author
    try:
        invs = await ctx.guild.invites()
        count = sum(i.uses for i in invs if i.inviter and i.inviter.id == target.id)
        await ctx.send(f"📈 {target.mention} je doveo **{count}** ljudi.")
    except: await ctx.send("Greška pri čitanju invajtova.")

@bot.command()
async def ping(ctx):
    await ctx.send(f"🏓 Pong! **{round(bot.latency * 1000)}ms**")

@bot.command()
async def help(ctx):
    embed = discord.Embed(title="📜 KRALJEVSKE KOMANDE", color=KING_COLOR)
    embed.add_field(name="🛡️ Admin", value="`kick`, `ban`, `unban [ID]`, `clear`, `lock`, `unlock`")
    embed.add_field(name="📈 Social", value="`invite`, `invitelab`")
    embed.add_field(name="🎉 Fun", value="`giveaway`, `ping`")
    embed.set_footer(text=FOOTER_TEXT)
    await ctx.send(embed=embed)

keep_alive()
bot.run(os.getenv('DISCORD_TOKEN'))
