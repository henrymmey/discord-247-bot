import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv(".env.two")

TOKEN = os.getenv("DISCORD_TOKEN")
ALLOWED_ROLE_ID = int(os.getenv("ALLOWED_ROLE_ID", "0"))

if not TOKEN:
    raise RuntimeError("DISCORD_TOKEN fehlt in der .env.two-Datei.")

if not ALLOWED_ROLE_ID:
    raise RuntimeError("ALLOWED_ROLE_ID fehlt in der .env.two-Datei.")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


def has_allowed_role(ctx):
    return any(role.id == ALLOWED_ROLE_ID for role in ctx.author.roles)


@bot.event
async def on_ready():
    print(f"Bot ist online als {bot.user}")


@bot.command(name="join2")
async def join(ctx):
    if not has_allowed_role(ctx):
        await ctx.send("❌ Du hast keine Berechtigung für diesen Befehl.")
        return

    if not ctx.author.voice:
        await ctx.send("❌ Du musst zuerst in einem Voice-Channel sein.")
        return

    channel = ctx.author.voice.channel

    if ctx.voice_client:
        await ctx.voice_client.move_to(channel)
    else:
        await channel.connect()

    await ctx.send(f"✅ Bin jetzt in **{channel.name}**.")


@bot.command(name="leave2")
async def leave(ctx):
    if not has_allowed_role(ctx):
        await ctx.send("❌ Du hast keine Berechtigung für diesen Befehl.")
        return

    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("✅ Bin aus dem Voice-Channel gegangen.")
    else:
        await ctx.send("❌ Ich bin gerade in keinem Voice-Channel.")


bot.run(TOKEN)
