import discord
from discord.ext import commands
from discord import app_commands
import json
import os
from datetime import datetime

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=”!”, intents=intents)

# File to store warnings and infractions

INFRACTIONS_FILE = “infractions.json”
TICKET_CONFIG_FILE = “ticket_config.json”

# Channel and Role IDs

WELCOME_CHANNEL_ID = 1453713527037628430
ORDER_CHANNEL_ID = 1453714619934838958
MOD_ROLE_ID = 1453710623635411054
LOG_CHANNEL_ID = 1453716115149684879
AUTO_ROLE_1 = 1453711369139650721
AUTO_ROLE_2 = 1453711643279360053
SUPPORT_ROLE_ID = 1453710623635411054

# Load or create infractions data

def load_infractions():
if os.path.exists(INFRACTIONS_FILE):
with open(INFRACTIONS_FILE, ‘r’) as f:
return json.load(f)
return {}

def save_infractions(data):
with open(INFRACTIONS_FILE, ‘w’) as f:
json.dump(data, f, indent=4)

def load_ticket_config():
if os.path.exists(TICKET_CONFIG_FILE):
with open(TICKET_CONFIG_FILE, ‘r’) as f:
return json.load(f)
return {}

def save_ticket_config(data):
with open(TICKET_CONFIG_FILE, ‘w’) as f:
json.dump(data, f, indent=4)

infractions_data = load_infractions()

@bot.event
async def on_ready():
print(f’{bot.user} is now online!’)
try:
synced = await bot.tree.sync()
print(f”Synced {len(synced)} commands”)
except Exception as e:
print(f”Failed to sync commands: {e}”)

# WELCOME SYSTEM

@bot.event
async def on_member_join(member):
# Send welcome message in channel
channel = bot.get_channel(WELCOME_CHANNEL_ID)
if channel:
embed = discord.Embed(
title=“👋 Welcome!”,
description=f”Greetings, {member.mention}! Welcome to **Nexora Labs**!”,
color=discord.Color.blue()
)
embed.set_thumbnail(url=member.display_avatar.url)
await channel.send(embed=embed)

```
# Send DM to user
try:
    dm_embed = discord.Embed(
        title="Welcome to Nexora Labs!",
        description=f"Greetings, {member.name}!\n\nWelcome to **Nexora Labs**! The finest and Cheapest Bots ever.\n\nOrder a bot in <#{ORDER_CHANNEL_ID}> Now!",
        color=discord.Color.gold()
    )
    await member.send(embed=dm_embed)
except:
    pass  # User has DMs disabled

# Auto-assign roles
role1 = member.guild.get_role(AUTO_ROLE_1)
role2 = member.guild.get_role(AUTO_ROLE_2)
roles_to_add = [r for r in [role1, role2] if r]
if roles_to_add:
    await member.add_roles(*roles_to_add)
```

# MODERATION COMMANDS

def has_mod_role():
async def predicate(interaction: discord.Interaction):
role = interaction.guild.get_role(MOD_ROLE_ID)
return role in interaction.user.roles
return app_commands.check(predicate)

@bot.tree.command(name=“ban”, description=“Bans a member from the server”)
@app_commands.describe(member=“The member to ban”, duration=“Ban duration in days”, reason=“Reason for ban”)
@has_mod_role()
async def ban(interaction: discord.Interaction, member: discord.Member, duration: int, reason: str = “No reason provided”):
try:
# Log infraction
user_id = str(member.id)
if user_id not in infractions_data:
infractions_data[user_id] = []

```
    infractions_data[user_id].append({
        "type": "Ban",
        "reason": reason,
        "duration": f"{duration} days",
        "moderator": str(interaction.user),
        "timestamp": datetime.now().isoformat()
    })
    save_infractions(infractions_data)
    
    # Ban member
    await member.ban(reason=reason, delete_message_days=duration)
    
    # Send confirmation
    embed = discord.Embed(
        title="🔨 Member Banned",
        description=f"{member.mention} has been banned for {duration} days.",
        color=discord.Color.red()
    )
    embed.add_field(name="Reason", value=reason)
    embed.add_field(name="Moderator", value=interaction.user.mention)
    await interaction.response.send_message(embed=embed)
    
    # Log to log channel
    log_channel = bot.get_channel(LOG_CHANNEL_ID)
    if log_channel:
        await log_channel.send(embed=embed)
except Exception as e:
    await interaction.response.send_message(f"Error: {str(e)}", ephemeral=True)
```

@bot.tree.command(name=“kick”, description=“Kicks a member from the server”)
@app_commands.describe(member=“The member to kick”, reason=“Reason for kick”)
@has_mod_role()
async def kick(interaction: discord.Interaction, member: discord.Member, reason: str = “No reason provided”):
try:
# Log infraction
user_id = str(member.id)
if user_id not in infractions_data:
infractions_data[user_id] = []

```
    infractions_data[user_id].append({
        "type": "Kick",
        "reason": reason,
        "moderator": str(interaction.user),
        "timestamp": datetime.now().isoformat()
    })
    save_infractions(infractions_data)
    
    # Kick member
    await member.kick(reason=reason)
    
    # Send confirmation
    embed = discord.Embed(
        title="👢 Member Kicked",
        description=f"{member.mention} has been kicked.",
        color=discord.Color.orange()
    )
    embed.add_field(name="Reason", value=reason)
    embed.add_field(name="Moderator", value=interaction.user.mention)
    await interaction.response.send_message(embed=embed)
    
    # Log to log channel
    log_channel = bot.get_channel(LOG_CHANNEL_ID)
    if log_channel:
        await log_channel.send(embed=embed)
except Exception as e:
    await interaction.response.send_message(f"Error: {str(e)}", ephemeral=True)
```

@bot.tree.command(name=“warn”, description=“Warns a member”)
@app_commands.describe(member=“The member to warn”, reason=“Reason for warning”)
@has_mod_role()
async def warn(interaction: discord.Interaction, member: discord.Member, reason: str = “No reason provided”):
try:
# Log infraction
user_id = str(member.id)
if user_id not in infractions_data:
infractions_data[user_id] = []

```
    infractions_data[user_id].append({
        "type": "Warning",
        "reason": reason,
        "moderator": str(interaction.user),
        "timestamp": datetime.now().isoformat()
    })
    save_infractions(infractions_data)
    
    # DM user
    try:
        dm_embed = discord.Embed(
            title="⚠️ Warning",
            description=f"You have been warned in **{interaction.guild.name}**",
            color=discord.Color.yellow()
        )
        dm_embed.add_field(name="Reason", value=reason)
        dm_embed.add_field(name="Moderator", value=str(interaction.user))
        await member.send(embed=dm_embed)
    except:
        pass
    
    # Send confirmation
    embed = discord.Embed(
        title="⚠️ Member Warned",
        description=f"{member.mention} has been warned.",
        color=discord.Color.yellow()
    )
    embed.add_field(name="Reason", value=reason)
    embed.add_field(name="Moderator", value=interaction.user.mention)
    await interaction.response.send_message(embed=embed)
    
    # Log to log channel
    log_channel = bot.get_channel(LOG_CHANNEL_ID)
    if log_channel:
        await log_channel.send(embed=embed)
except Exception as e:
    await interaction.response.send_message(f"Error: {str(e)}", ephemeral=True)
```

@bot.tree.command(name=“view-history”, description=“View a member’s infraction history”)
@app_commands.describe(member=“The member to check”)
@has_mod_role()
async def view_history(interaction: discord.Interaction, member: discord.Member):
user_id = str(member.id)

```
if user_id not in infractions_data or not infractions_data[user_id]:
    await interaction.response.send_message(f"{member.mention} has no infractions.", ephemeral=True)
    return

embed = discord.Embed(
    title=f"📋 Infraction History - {member.name}",
    color=discord.Color.blue()
)
embed.set_thumbnail(url=member.display_avatar.url)

for i, infraction in enumerate(infractions_data[user_id], 1):
    duration = infraction.get('duration', 'N/A')
    field_value = f"**Type:** {infraction['type']}\n**Reason:** {infraction['reason']}\n**Moderator:** {infraction['moderator']}\n**Date:** {infraction['timestamp'][:10]}"
    if duration != 'N/A':
        field_value += f"\n**Duration:** {duration}"
    embed.add_field(name=f"Infraction #{i}", value=field_value, inline=False)

await interaction.response.send_message(embed=embed, ephemeral=True)
```

# TICKET SYSTEM

class TicketView(discord.ui.View):
def **init**(self, ticket_type):
super().**init**(timeout=None)
self.ticket_type = ticket_type

```
@discord.ui.button(label="Open Ticket", style=discord.ButtonStyle.green, emoji="🎫")
async def open_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
    guild = interaction.guild
    user = interaction.user
    
    # Create ticket channel
    category = interaction.channel.category
    ticket_channel = await guild.create_text_channel(
        name=f"ticket-{user.name}",
        category=category,
        topic=f"Ticket opened by {user.name}"
    )
    
    # Set permissions
    await ticket_channel.set_permissions(guild.default_role, read_messages=False)
    await ticket_channel.set_permissions(user, read_messages=True, send_messages=True)
    
    if self.ticket_type == "order":
        role = guild.get_role(SUPPORT_ROLE_ID)
        if role:
            await ticket_channel.set_permissions(role, read_messages=True, send_messages=True)
        
        embed = discord.Embed(
            title="🛒 Bot Order Ticket",
            description=f"{role.mention if role else ''}\n\nPlease provide the following information:",
            color=discord.Color.gold()
        )
        embed.add_field(name="Your Discord Username", value="Please provide", inline=False)
        embed.add_field(name="Type", value="What type of bot?", inline=False)
        embed.add_field(name="Explain your bot", value="Describe what you need", inline=False)
        embed.set_footer(text="Our team will assist you shortly!")
    else:  # support
        role = guild.get_role(SUPPORT_ROLE_ID)
        if role:
            await ticket_channel.set_permissions(role, read_messages=True, send_messages=True)
        
        embed = discord.Embed(
            title="🛠️ Support Ticket",
            description=f"{role.mention if role else ''}\n\nWelcome to support! Please describe your issue and our team will help you shortly.",
            color=discord.Color.blue()
        )
        embed.add_field(name="What can we help with?", value="• Bot issues\n• Rule violations\n• General support", inline=False)
    
    # Add close button
    close_view = discord.ui.View(timeout=None)
    close_button = discord.ui.Button(label="Close Ticket", style=discord.ButtonStyle.red, emoji="🔒")
    
    async def close_callback(close_interaction: discord.Interaction):
        await close_interaction.response.send_message("Closing ticket in 5 seconds...")
        await asyncio.sleep(5)
        await ticket_channel.delete()
    
    close_button.callback = close_callback
    close_view.add_item(close_button)
    
    await ticket_channel.send(content=user.mention, embed=embed, view=close_view)
    await interaction.response.send_message(f"Ticket created: {ticket_channel.mention}", ephemeral=True)
```

@bot.tree.command(name=“ticket-setup”, description=“Setup ticket system”)
@app_commands.describe(
channel=“Channel to send ticket panel”,
ticket_type=“Type of ticket (order or support)”
)
@app_commands.choices(ticket_type=[
app_commands.Choice(name=“Bot Order”, value=“order”),
app_commands.Choice(name=“Support”, value=“support”)
])
@has_mod_role()
async def ticket_setup(interaction: discord.Interaction, channel: discord.TextChannel, ticket_type: str):
if ticket_type == “order”:
embed = discord.Embed(
title=“🛒 Order a Bot”,
description=“Open a ticket now if you want the finest bots!”,
color=discord.Color.gold()
)
embed.set_footer(text=“Click the button below to open a ticket”)
else:
embed = discord.Embed(
title=“🛠️ Support”,
description=“Having trouble with your bot or somebody breaking rules? Open a ticket now!”,
color=discord.Color.blue()
)
embed.set_footer(text=“Click the button below to get help”)

```
view = TicketView(ticket_type)
await channel.send(embed=embed, view=view)
await interaction.response.send_message(f"Ticket panel setup in {channel.mention}!", ephemeral=True)
```

# Import asyncio for ticket close delay

import asyncio

# Run bot

bot.run(‘MTQ1MzczNzk2NTY1MzE5Njg1Mg.GFQVF2._tE4_3d4HY4A52N16gYC7qqegWcRq_D_vK4whg’)
