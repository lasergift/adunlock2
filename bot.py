import discord
from discord.ext import commands, tasks
import sqlite3
import asyncio

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="/", intents=intents)

import os
TOKEN = os.getenv("TOKEN")
GUILD_ID = 123456789012345678  # Remplace par ton ID de serveur
ROLE_NAME = "VIP"

def is_valid_key(key):
    conn = sqlite3.connect("../db/db.sqlite")
    cur = conn.cursor()
    cur.execute("SELECT used FROM keys WHERE key = ?", (key,))
    row = cur.fetchone()
    if row and row[0] == 0:
        cur.execute("UPDATE keys SET used = 1 WHERE key = ?", (key,))
        conn.commit()
        conn.close()
        return True
    conn.close()
    return False

@bot.command()
async def valider(ctx, clé: str):
    if is_valid_key(clé):
        role = discord.utils.get(ctx.guild.roles, name=ROLE_NAME)
        await ctx.author.add_roles(role)
        await ctx.send("✅ Accès accordé pour 30 minutes.")
        await asyncio.sleep(1800)
        await ctx.author.remove_roles(role)
        await ctx.send("🕒 Ton accès a expiré.")
    else:
        await ctx.send("❌ Clé invalide ou déjà utilisée.")

bot.run(TOKEN)
