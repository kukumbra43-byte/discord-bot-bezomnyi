# main.py — безопасный вариант (не содержит токена)
import discord
import asyncio
import os

# Словарь: ID участника → путь к аудиофайлу
TARGET_USERS = {
    1155033257927249950: "kontrakt_nety_doma.mp3",
    1076415883137789952: "kontrakt_nety_doma.mp3",
    1247385333210022014: "kontrakt_nety_doma.mp3"
}

TOKEN = 'MTQ0MTQ2MTgwMTYyMjcwNDE0OA.GUpjJb.-ZzRjYy0e5BqKTK6KNQUOJeuaFE2PT_tR6_zSQ'

intents = discord.Intents.default()
intents.voice_states = True
intents.message_content = True  # если нужны команды по содержимому сообщений

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Бот {client.user} готов!')

@client.event
async def on_voice_state_update(member, before, after):
    # участник только что зашёл в голосовой канал
    if before.channel is None and after.channel is not None:
        if member.id in TARGET_USERS:
            audio_file = TARGET_USERS[member.id]
            print(f"{member} зашёл в {after.channel.name} → играем {audio_file}")
            try:
                vc = await after.channel.connect()
                # Если ffmpeg не найден — будет бросено исключение
                vc.play(discord.FFmpegPCMAudio(audio_file))

                while vc.is_playing():
                    await asyncio.sleep(1)

                await vc.disconnect()
                print(f"Бот отключился после проигрывания {audio_file}")

            except Exception as e:
                print(f"Ошибка при воспроизведении для {member}: {e}")

client.run(TOKEN)
