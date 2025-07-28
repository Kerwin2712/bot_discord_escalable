# bot.py
import discord
from discord.ext import commands
from config import DISCORD_BOT_TOKEN, GUILD_ID
from main_mod.send_message import send_text_message
from main_mod.send_resource import send_resource_message
from main_mod.create_button import create_button_component

# Definir los intents que tu bot necesitará.
# Los intents son un conjunto de eventos de Discord a los que tu bot se suscribirá.
# Para la mayoría de los bots, necesitarás al menos los intents por defecto.
# Si tu bot necesita acceder a información de miembros (como nombres de usuario),
# necesitarás el intent 'members' y habilitarlo en el portal de desarrolladores de Discord.
intents = discord.Intents.default()
intents.message_content = True # Necesario para leer el contenido de los mensajes
intents.members = True # Necesario si quieres acceder a información de miembros (ej. para comandos de bienvenida)

# Crear una instancia del bot con un prefijo de comando y los intents definidos
# El prefijo de comando es lo que los usuarios escribirán antes de tus comandos (ej. !hola)
bot = commands.Bot(command_prefix='&', intents=intents)

# Evento que se dispara cuando el bot está listo y conectado a Discord
@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user.name} (ID: {bot.user.id})')
    print('------')

    # Si tienes un GUILD_ID configurado, puedes sincronizar los comandos de barra aquí
    # Esto es útil para que los comandos de barra se registren rápidamente en un servidor específico
    if GUILD_ID:
        try:
            guild = discord.Object(id=int(GUILD_ID))
            bot.tree.copy_global_to(guild=guild)
            await bot.tree.sync(guild=guild)
            print(f"Comandos sincronizados con el servidor ID: {GUILD_ID}")
        except Exception as e:
            print(f"Error al sincronizar comandos con el servidor ID {GUILD_ID}: {e}")
    else:
        # Si no hay GUILD_ID, sincroniza globalmente (puede tardar hasta 1 hora)
        await bot.tree.sync()
        print("Comandos sincronizados globalmente.")

# Ejemplo de un comando de texto simple
@bot.command(name='hola')
async def hola_command(ctx):
    """
    Responde con un saludo.
    Uso: !hola
    """
    await send_text_message(ctx, "¡Hola! Soy tu bot de Discord.")

# Ejemplo de un comando de barra (slash command)
@bot.tree.command(name="saludo", description="Envía un saludo personalizado.")
async def saludo_slash_command(interaction: discord.Interaction):
    """
    Envía un saludo personalizado como comando de barra.
    Uso: /saludo
    """
    await interaction.response.send_message("¡Hola desde un comando de barra!", ephemeral=True)

# Ejemplo de un comando que envía un recurso (usando la función de send_resource.py)
@bot.command(name='recurso')
async def recurso_command(ctx, url: str = "https://www.google.com", filename: str = None):
    """
    Envía un recurso (URL o archivo).
    Uso: !recurso [URL] [nombre_archivo]
    Si no se proporciona URL, usa Google.
    """
    await send_resource_message(ctx, url, filename)

# Ejemplo de un comando que crea un botón (usando la función de create_button.py)
@bot.command(name='boton')
async def boton_command(ctx):
    """
    Crea un mensaje con un botón interactivo.
    Uso: !boton
    """
    # Crear un botón con una etiqueta y un estilo
    button = create_button_component(
        custom_id="mi_primer_boton",
        label="Haz clic aquí",
        style=discord.ButtonStyle.primary # Estilo de botón primario (azul)
    )

    # Crear una vista (View) para añadir el botón
    view = discord.ui.View()
    view.add_item(button)

    # Enviar el mensaje con el botón
    await ctx.send("Aquí tienes un botón:", view=view)

# Manejador para la interacción del botón
@bot.event
async def on_interaction(interaction: discord.Interaction):
    if interaction.type == discord.InteractionType.component:
        if interaction.data['custom_id'] == 'mi_primer_boton':
            await interaction.response.send_message("¡Has hecho clic en el botón!", ephemeral=True)
    # Asegúrate de procesar otras interacciones si las tienes
    await bot.process_commands(interaction)


# Iniciar el bot con el token
def run_bot():
    if DISCORD_BOT_TOKEN:
        bot.run(DISCORD_BOT_TOKEN)
    else:
        print("Error: El token del bot de Discord no está configurado. "
              "Por favor, asegúrate de que DISCORD_BOT_TOKEN esté en tu archivo .env")

if __name__ == '__main__':
    run_bot()
