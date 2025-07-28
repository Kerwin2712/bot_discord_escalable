# config.py
import os
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Obtener el token del bot de Discord desde las variables de entorno
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")

# Obtener el ID del servidor (guild) si está configurado
GUILD_ID = os.getenv("GUILD_ID")

# Verificar que el token del bot esté configurado
if not DISCORD_BOT_TOKEN:
    raise ValueError("No se encontró la variable de entorno DISCORD_BOT_TOKEN. "
                     "Asegúrate de que esté configurada en tu archivo .env")

# Puedes añadir más variables de entorno aquí según las necesidades de tu bot
# Por ejemplo, IDs de canales, roles, etc.
# CHANNEL_ID = os.getenv("CHANNEL_ID")

print("Configuración cargada exitosamente.")
