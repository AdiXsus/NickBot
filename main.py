import discord
from discord.ext import commands
import os
import requests
from keep_alive import keep_alive

# Inicjalizacja bota z intents
intents = discord.Intents(guilds=True,
                          guild_messages=True,
                          message_content=True,
                          presences=True)
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


@bot.event
async def on_message(message):
    # Automatyczne reakcje
    keywords = ["hello", "hej", "siema", "elo", "witam", "dzien dobry"]
    lowercased_content = message.content.lower()

    if any(keyword in lowercased_content for keyword in keywords):
        await message.add_reaction("👋🏽")

    if "👍" in message.content:
        await message.add_reaction("👍🏽")

    # Pozostała część kodu obsługująca inne komendy
    if lowercased_content == "!ping":
        ping = discord.utils.utcnow() - message.created_at
        reply_message = await message.reply(
            f'🏓 Pong! Opóźnienie bota wynosi {ping.total_seconds() * 1000} ms.'
        )

    # Sprawdzanie czy wiadomość została wysłana przez określonego użytkownika
    user_id_to_monitor = "373730000609869835"  # ID użytkownika, którego wiadomości będą usuwane
    if message.author.id == int(user_id_to_monitor):
        try:
            # Zapisanie treści wiadomości
            original_content = message.content

            # Usunięcie wiadomości użytkownika
            await message.delete()

            # Wysłanie wiadomości od bota z oryginalną treścią
            await message.channel.send(original_content)
        except Exception as error:
            print('Wystąpił błąd podczas usuwania wiadomości:', error)


keep_alive()

# Dodaj swój token bota tutaj
bot.run(TOKEN)
