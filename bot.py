import os
import discord
from discord.ext import commands
import random
import asyncio
from KeepAlive import keep_alive
import datetime

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
        ticket_name = f"ticket-{user.name.lower()}".replace(" ", "-")
        
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
    print(f'👑 King {bot.user.name} je online i sve komande su spremne!')

# --- POMOĆNA FUNKCIJA ZA INVITE ---
async def get_invites_count(member):
    try:
        invs = await member.guild.invites()
        count = 0
        for i in invs:
            if i.inviter and i.inviter.id == member.id:
                count += i.uses
        return count
    except:
        return 0


# -- NAZAD/NAPRED --

class InvitePaginator(discord.ui.View):
    def __init__(self, pages, timeout=60):
        super().__init__(timeout=timeout)
        self.pages = pages
        self.current_page = 0

    async def update_view(self, interaction: discord.Interaction):
        await interaction.response.edit_message(embed=self.pages[self.current_page], view=self)

    @discord.ui.button(label="⬅️ Back", style=discord.ButtonStyle.gray)
    async def previous(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current_page > 0:
            self.current_page -= 1
            await self.update_view(interaction)

    @discord.ui.button(label="Next ➡️", style=discord.ButtonStyle.gray)
    async def next(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current_page < len(self.pages) - 1:
            self.current_page += 1
            await self.update_view(interaction)

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
        await ctx.send("Tiket će biti obrisan za 3 sekunde...")
        await asyncio.sleep(3)
        await ctx.channel.delete()


# --- ANTI-LINK SA AUTOMATSKIM TIMEOUT-OM (15 MIN) ---
    if "discord.gg/" in msg_content and author_name not in allowed_users:
        try:
            await message.delete()
            
            # Timeout na 15 minuta
            trajanje = datetime.timedelta(minutes=15)
            await message.author.timeout(trajanje, reason="Slanje Discord linkova (reklamiranje)")
            
            embed = discord.Embed(title="🚫 REKLAMIRANJE ZABRANJENO", color=0xff0000)
            embed.description = (
                f"━━━━━━━━━━━━━━━━━━\n"
                f"👑 Na **Kings Of Reselling** je zabranjeno reklamiranje!\n"
                f"👤 **Clan:** {message.author.mention}\n"
                f"⚠️ **Kazna:** Poruka obrisana + **TIMEOUT 15 MIN**.\n"
                f"━━━━━━━━━━━━━━━━━━"
            )
            embed.set_footer(text=FOOTER_TEXT)
            
            await message.channel.send(embed=embed)
            return # Odmah prekidamo da ne bi proveravao ostale filtere
        except Exception as e:
            print(f"Greska kod antilinka: {e}")

    # --- FILTER ZA PRODAJU (TVOJ POSTOJEĆI KOD) ---
    if ("prodaja" in msg_content or "prodajem" in msg_content) and author_name not in allowed_users:
        try:
            await message.delete()
            prodaja_channel_id = 1479762526819586070 
            embed = discord.Embed(
                description=f"{message.author.mention} Pogrešan kanal!!! Koristi kanal namenjen za prodaju <#{prodaja_channel_id}>",
                color=KING_COLOR
            )
            embed.set_footer(text=FOOTER_TEXT)
            await message.channel.send(embed=embed)
            return
        except Exception as e:
            print(f"Greska kod filtera prodaje: {e}")}")

# --- BRISANJE PORUKE PRODAJEM ---
# --- FILTER ZA PRODAJU (PROVERAVA SVA SLOVA) ---
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    # Dozvoljeni korisnici koji mogu da pisu ove reci
    allowed_users = ["knez.exe", "nemanjaa79"]
    author_name = message.author.name.lower()
    
    # Ovde pretvaramo celu poruku u mala slova za proveru
    # To znaci da ce hvatati i "PRODAJA" i "pRoDaJeM" i "Prodajem"
    msg_content = message.content.lower()

    if ("prodaja" in msg_content or "prodajem" in msg_content) and author_name not in allowed_users:
        try:
            await message.delete()
            
            # ID tvog kanala #🏷️┃prodajem
            prodaja_channel_id = 1479762526819586070 
            
            embed = discord.Embed(
                description=f"{message.author.mention} Pogresan kanal!!! Koristi kanal koji je namenjen za prodaju <#{prodaja_channel_id}>",
                color=KING_COLOR
            )
            embed.set_footer(text=FOOTER_TEXT)
            
            # Poruka ostaje u kanalu da svi vide pravilo
            await message.channel.send(embed=embed)
        except Exception as e:
            print(f"Greska kod filtera: {e}")

    # OVO JE OBAVEZNO da bi ostale komande radile
    await bot.process_commands(message)

# =========================================================
#          KINGS ULTRA AUDIT LOG SISTEM (FINAL)
# =========================================================

LOG_CHANNEL_ID = 1479757402336268429

# 1. LOG: Izmena poruke
@bot.event
async def on_message_edit(before, after):
    if before.author.bot or before.content == after.content: return
    log_ch = bot.get_channel(LOG_CHANNEL_ID)
    if not log_ch: return
    embed = discord.Embed(title="📝 LOG: IZMENA PORUKE", color=discord.Color.blue())
    embed.description = f"━━━━━━━━━━━━━━━━━━\n👤 **Autor:** {before.author.mention}\n📍 **Kanal:** {before.channel.mention}\n❌ **Stara:** \"{before.content}\"\n✅ **Nova:** \"{after.content}\"\n━━━━━━━━━━━━━━━━━━"
    await log_ch.send(embed=embed)

# 2. LOG: Brisanje poruke
@bot.event
async def on_message_delete(message):
    if message.author.bot: return
    log_ch = bot.get_channel(LOG_CHANNEL_ID)
    if not log_ch: return
    embed = discord.Embed(title="🗑️ LOG: PORUKA OBRISANA", color=discord.Color.red())
    embed.description = f"━━━━━━━━━━━━━━━━━━\n👤 **Autor:** {message.author.mention}\n📍 **Kanal:** {message.channel.mention}\n💬 **Sadržaj:** \"{message.content}\"\n━━━━━━━━━━━━━━━━━━"
    await log_ch.send(embed=embed)

# 3. LOG: Role Update & Timeout
@bot.event
async def on_member_update(before, after):
    log_ch = bot.get_channel(LOG_CHANNEL_ID)
    if not log_ch: return
    if before.roles != after.roles:
        added = [role.mention for role in after.roles if role not in before.roles]
        removed = [role.mention for role in before.roles if role not in after.roles]
        async for entry in after.guild.audit_logs(action=discord.AuditLogAction.member_role_update, limit=1):
            executor = entry.user
            break
        else: executor = "Nepoznato"
        embed = discord.Embed(title="🛡️ ADMIN AKCIJA: ROLE UPDATE", color=discord.Color.orange())
        desc = f"━━━━━━━━━━━━━━━━━━\n👤 **Meta:** {after.mention}\n🛠️ **Izvršio:** {executor}\n"
        if added: desc += f"➕ **Dodata rola:** {', '.join(added)}\n"
        if removed: desc += f"➖ **Skinuta rola:** {', '.join(removed)}\n"
        desc += "━━━━━━━━━━━━━━━━━━"
        embed.description = desc
        await log_ch.send(embed=embed)
    if before.timed_out_until != after.timed_out_until:
        if after.timed_out_until:
            async for entry in after.guild.audit_logs(action=discord.AuditLogAction.member_update, limit=1):
                executor = entry.user
                break
            else: executor = "Nepoznato"
            embed = discord.Embed(title="⏳ KAZNA: TIMEOUT", color=discord.Color.gold())
            embed.description = f"━━━━━━━━━━━━━━━━━━\n👤 **Kome:** {after.mention}\n🛠️ **Izvršio:** {executor}\n🕒 **Traje do:** {after.timed_out_until.strftime('%d.%m.%Y %H:%M')}\n━━━━━━━━━━━━━━━━━━"
            await log_ch.send(embed=embed)

# 4. LOG: Kick, Ban, Unban
@bot.event
async def on_member_remove(member):
    log_ch = bot.get_channel(LOG_CHANNEL_ID)
    if not log_ch: return
    async for entry in member.guild.audit_logs(limit=1):
        if entry.action == discord.AuditLogAction.kick and entry.target.id == member.id:
            embed = discord.Embed(title="🚀 SISTEM: KICK", color=discord.Color.red())
            embed.description = f"━━━━━━━━━━━━━━━━━━\n👤 **Izbačen:** {member.name}\n🛠️ **Izvršio:** {entry.user}\n📝 **Razlog:** {entry.reason if entry.reason else '///'}\n━━━━━━━━━━━━━━━━━━"
            await log_ch.send(embed=embed)
            break

@bot.event
async def on_member_ban(guild, user):
    log_ch = bot.get_channel(LOG_CHANNEL_ID)
    if not log_ch: return
    async for entry in guild.audit_logs(action=discord.AuditLogAction.ban, limit=1):
        embed = discord.Embed(title="🔨 SISTEM: BAN", color=discord.Color.dark_red())
        embed.description = f"━━━━━━━━━━━━━━━━━━\n👤 **Banovan:** {user.name}\n🛠️ **Izvršio:** {entry.user}\n📝 **Razlog:** {entry.reason if entry.reason else '///'}\n━━━━━━━━━━━━━━━━━━"
        await log_ch.send(embed=embed)

@bot.event
async def on_member_unban(guild, user):
    log_ch = bot.get_channel(LOG_CHANNEL_ID)
    if not log_ch: return
    async for entry in guild.audit_logs(action=discord.AuditLogAction.unban, limit=1):
        embed = discord.Embed(title="🔓 SISTEM: UNBAN", color=discord.Color.green())
        embed.description = f"━━━━━━━━━━━━━━━━━━\n👤 **Pomilovan:** {user.name}\n🛠️ **Izvršio:** {entry.user}\n━━━━━━━━━━━━━━━━━━"
        await log_ch.send(embed=embed)

# 5. LOG: Kanali & Kategorije
@bot.event
async def on_guild_channel_create(channel):
    log_ch = bot.get_channel(LOG_CHANNEL_ID)
    async for entry in channel.guild.audit_logs(action=discord.AuditLogAction.channel_create, limit=1):
        embed = discord.Embed(title="⚙️ SISTEM: KANAL NAPRAVLJEN", color=discord.Color.green())
        embed.description = f"━━━━━━━━━━━━━━━━━━\n📂 **Kanal:** {channel.mention}\n🛠️ **Izvršio:** {entry.user}\n📁 **Kategorija:** {channel.category.name if channel.category else 'Nema'}\n━━━━━━━━━━━━━━━━━━"
        await log_ch.send(embed=embed)

@bot.event
async def on_guild_channel_delete(channel):
    log_ch = bot.get_channel(LOG_CHANNEL_ID)
    async for entry in channel.guild.audit_logs(action=discord.AuditLogAction.channel_delete, limit=1):
        embed = discord.Embed(title="⚙️ SISTEM: KANAL OBRISAN", color=discord.Color.dark_gray())
        embed.description = f"━━━━━━━━━━━━━━━━━━\n🗑️ **Kanal:** `#{channel.name}`\n🛠️ **Izvršio:** {entry.user}\n━━━━━━━━━━━━━━━━━━"
        await log_ch.send(embed=embed)

# 6. LOG: IZMENA PERMISIJA (Stavka 10 - Kanali & Role)
@bot.event
async def on_guild_role_update(before, after):
    if before.permissions != after.permissions:
        log_ch = bot.get_channel(LOG_CHANNEL_ID)
        async for entry in after.guild.audit_logs(action=discord.AuditLogAction.role_update, limit=1):
            executor = entry.user
            break
        else: executor = "Nepoznato"
        embed = discord.Embed(title="🔑 SISTEM: IZMENA PERMISIJA ROLE", color=discord.Color.blurple())
        embed.description = f"━━━━━━━━━━━━━━━━━━\n🛡️ **Rola:** {after.name}\n🛠️ **Izvršio:** {executor}\n⚠️ **Akcija:** Promenjene globalne dozvole role.\n━━━━━━━━━━━━━━━━━━"
        await log_ch.send(embed=embed)

@bot.event
async def on_guild_channel_update(before, after):
    # Provera za permisije kanala (Stavka 10)
    if before.overwrites != after.overwrites:
        log_ch = bot.get_channel(LOG_CHANNEL_ID)
        async for entry in after.guild.audit_logs(action=discord.AuditLogAction.channel_overwrite_update, limit=1):
            executor = entry.user
            break
        else: executor = "Nepoznato"
        embed = discord.Embed(title="🔒 SISTEM: KANAL PERMISIJE", color=discord.Color.dark_magenta())
        embed.description = f"━━━━━━━━━━━━━━━━━━\n📍 **Kanal:** {after.mention}\n🛠️ **Izvršio:** {executor}\n📝 **Info:** Izmenjene dozvole za uloge/članove u kanalu.\n━━━━━━━━━━━━━━━━━━"
        await log_ch.send(embed=embed)

# 7. LOG: Invite & Role Create/Delete
@bot.event
async def on_invite_create(invite):
    log_ch = bot.get_channel(LOG_CHANNEL_ID)
    embed = discord.Embed(title="🔗 SISTEM: INVITE NAPRAVLJEN", color=discord.Color.purple())
    embed.description = f"━━━━━━━━━━━━━━━━━━\n🛠️ **Napravio:** {invite.inviter}\n🆔 **Kod:** `{invite.code}`\n📍 **Kanal:** {invite.channel.mention}\n━━━━━━━━━━━━━━━━━━"
    await log_ch.send(embed=embed)

@bot.event
async def on_guild_role_create(role):
    log_ch = bot.get_channel(LOG_CHANNEL_ID)
    async for entry in role.guild.audit_logs(action=discord.AuditLogAction.role_create, limit=1):
        await log_ch.send(f"🛡️ **SISTEM:** Rola **{role.name}** napravljena (Izvršio: {entry.user})")

@bot.event
async def on_guild_role_delete(role):
    log_ch = bot.get_channel(LOG_CHANNEL_ID)
    async for entry in role.guild.audit_logs(action=discord.AuditLogAction.role_delete, limit=1):
        await log_ch.send(f"🛡️ **SISTEM:** Rola **{role.name}** obrisana (Izvršio: {entry.user})")

# --- MODERACIJA ---
@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason="///"):
    try:
        await member.kick(reason=reason)
        await ctx.send(f"🚀 **{member.name}** je lansiran! Razlog: {reason}")
    except: pass

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason="///"):
    try:
        await member.ban(reason=reason)
        await ctx.send(f"🔨 **{member.name}** je proteran! Razlog: {reason}")
    except: pass

@bot.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, id: int):
    try:
        user = await bot.fetch_user(id)
        await ctx.guild.unban(user)
        await ctx.send(f"🔓 Korisnik **{user.name}** je pomilovan!")
    except: await ctx.send("❌ ID nije na ban listi.")

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

# --- INVITE & SOCIAL (OPCIJA 3) ---
@bot.command()
async def invite(ctx, member: discord.Member = None):
    target = member if member else ctx.author
    
    try:
        invs = await ctx.guild.invites()
        joined = 0
        # Računamo koliko je ljudi ušlo preko svih njegovih aktivnih linkova
        for i in invs:
            if i.inviter and i.inviter.id == target.id:
                joined += i.uses
        
        # Simulacija za Left i Total (bez baze podataka ovo su najbolje procene)
        # Napomena: Za 100% tačan 'Left' bot bi morao da prati ulaze/izlaze u realnom vremenu
        left = 0 
        total = joined - left

        embed = discord.Embed(title="📈 STATISTIKA", color=KING_COLOR)
        embed.description = (
            f"👤 **Član:** {target.mention}\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"📥 **Joined:** {joined}\n"
            f"📤 **Left:** {left}\n"
            f"🏆 **Total:** {total}\n"
            f"━━━━━━━━━━━━━━━━━━"
        )
        embed.set_footer(text=FOOTER_TEXT)
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ Greška pri čitanju invite-ova: {e}")

@bot.command()
async def invitelab(ctx):
    all_invites = {}
    try:
        invs = await ctx.guild.invites()
        for i in invs:
            if i.inviter:
                all_invites[i.inviter] = all_invites.get(i.inviter, 0) + i.uses
        
        sorted_inv = sorted(all_invites.items(), key=lambda x: x[1], reverse=True)[:20]
        
        if not sorted_inv:
            return await ctx.send("Nema podataka o invite-ovima.")

        pages = []
        for i in range(0, len(sorted_inv), 10):
            chunk = sorted_inv[i:i + 10]
            embed = discord.Embed(title="🏆 TOP 20 INVITER-A", color=KING_COLOR)
            
            description = "━━━━━━━━━━━━━━━━━━\n"
            for index, (user, joined) in enumerate(chunk):
                left = 0 
                total = joined - left
                description += f"**{i + index + 1}. {user.name}**\n📥 Joined: `{joined}` | 📤 Left: `{left}` | 🏆 Total: `{total}`\n\n"
            
            description += "━━━━━━━━━━━━━━━━━━"
            embed.description = description
            embed.set_footer(text=f"Stranica {len(pages) + 1} | {FOOTER_TEXT}")
            pages.append(embed)

        view = InvitePaginator(pages)
        await ctx.send(embed=pages[0], view=view)
        
    except Exception as e:
        await ctx.send(f"Greška: {e}")

# --- INFO & SERVERINFO ---
@bot.command()
async def info(ctx, member: discord.Member = None):
    target = member if member else ctx.author
    
    # Dobijanje najveće uloge (ignorišemo @everyone)
    top_role = target.top_role.mention if len(target.roles) > 1 else "Nema rol"
    
    embed = discord.Embed(title="👑 KINGS CLAN | PROFIL", color=KING_COLOR)
    embed.description = (
        f"━━━━━━━━━━━━━━━━━━\n"
        f"👤 **Clan:** {target.mention}\n"
        f"🆔 **ID:** `{target.id}`\n"
        f"📅 **Na serveru od:** {target.joined_at.strftime('%d.%m.%Y.')}\n"
        f"🛡️ **Najveci Rol:** {top_role}\n"
        f"━━━━━━━━━━━━━━━━━━"
    )
    embed.set_footer(text=FOOTER_TEXT)
    await ctx.send(embed=embed)

@bot.command()
async def serverinfo(ctx):
    guild = ctx.guild
    # Brojanje članova (bez botova)
    member_count = len([m for m in guild.members if not m.bot])
    
    embed = discord.Embed(title="🌍 INFORMACIJE O SERVERU", color=KING_COLOR)
    embed.description = (
        f"━━━━━━━━━━━━━━━━━━\n"
        f"👑 **Owner:** {guild.owner.mention}\n"
        f"👥 **Ukupno clanova:** {member_count}\n"
        f"✨ **Nivo servera:** Level {guild.premium_tier}\n"
        f"📅 **Datum kreiranja:** {guild.created_at.strftime('%d.%m.%Y.')}\n"
        f"━━━━━━━━━━━━━━━━━━"
    )
    embed.set_footer(text=FOOTER_TEXT)
    await ctx.send(embed=embed)


# --- OSTALO ---
@bot.command()
async def giveaway(ctx, minuti: int, pobednika: int, *, nagrada: str):
    embed = discord.Embed(title="🎊 GIVEAWAY 🎊", description=f"🎁 Nagrada: **{nagrada}**\n🏆 Pobednika: **{pobednika}**\n⏳ Trajanje: **{minuti} min**", color=KING_COLOR)
    embed.set_footer(text=FOOTER_TEXT)
    msg = await ctx.send(embed=embed)
    await msg.add_reaction("🎉")
    await asyncio.sleep(minuti * 60)
    try:
        msg = await ctx.channel.fetch_message(msg.id)
        users = [u async for u in msg.reactions[0].users() if not u.bot]
        winners = random.sample(users, min(len(users), pobednika))
        await ctx.send(f"👑 Pobednici: {', '.join([w.mention for w in winners])}! Nagrada: **{nagrada}**")
    except: pass

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
    embed.description = "━━━━━━━━━━━━━━━━━━"
    
    # 🛡️ ADMIN
    embed.add_field(name="🛡️ Admin", value="`kick`, `ban`, `unban`, `clear`, `lock`, `unlock`", inline=False)
    
    # 📈 SOCIAL (Dodate info i serverinfo ovde)
    embed.add_field(name="📈 Social", value="`invite`, `invitelab`, `info`, `serverinfo`", inline=False)
    
    # 🎉 OSTALO
    embed.add_field(name="🎉 Ostalo", value="`giveaway`, `ping`, `ticket`", inline=False)
    
    embed.set_footer(text=FOOTER_TEXT)
    await ctx.send(embed=embed)

keep_alive()
bot.run(os.getenv('DISCORD_TOKEN'))
