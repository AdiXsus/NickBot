import discord
from discord.ext import commands
import os
import requests
from keep_alive import keep_alive

# Inicjalizacja bota z intents
intents = discord.Intents.default()
intents.members = True  # Upewnij się, że bot ma uprawnienia do zarządzania członkami
bot = commands.Bot(command_prefix='!', intents=intents)

# Token bota
TOKEN = os.getenv('BOT_TOKEN')

# URL webhooka
WEBHOOK_URL = os.getenv('WEBHOOK_URL')

# Emotikon do dodania
EMOJI = "🍷 |"


@bot.event
async def on_ready():
    print(f'Bot zalogowany jako {bot.user}')
    # Ustawienie statusu bota
    await bot.change_presence(activity=discord.CustomActivity(
        type=discord.ActivityType.custom, name="🍷 Marlowe Vineyards Open"))

    # Wysłanie webhooka
    if WEBHOOK_URL:
        payload = {"content": f"Bot {bot.user} został uruchomiony!"}
        try:
            response = requests.post(WEBHOOK_URL, json=payload)
            response.raise_for_status()
            print(f'Webhook wysłany: {response.status_code}')
        except requests.exceptions.RequestException as e:
            print(f'Błąd podczas wysyłania webhooka: {e}')


@bot.event
async def on_member_join(member):
    # Nowa nazwa użytkownika z emotikonem
    new_nick = f"{EMOJI} {member.display_name}"

    try:
        # Zmiana nazwy użytkownika
        await member.edit(nick=new_nick)
        print(f'Zmieniono nazwę użytkownika {member.name} na {new_nick}')
    except discord.Forbidden:
        print(f'Brak uprawnień do zmiany nazwy użytkownika {member.name}')
    except discord.HTTPException as e:
        print(
            f'Wystąpił błąd podczas zmiany nazwy użytkownika {member.name}: {e}'
        )


keep_alive()

# Uruchomienie bota
bot.run(TOKEN)
