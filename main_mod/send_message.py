# send_message.py
import discord
from discord.ext import commands

async def send_text_message(ctx: commands.Context, message_content: str):
    """
    Envía un mensaje de texto simple al canal donde se invocó el comando.

    Args:
        ctx (commands.Context): El contexto del comando, que contiene información
                                sobre el mensaje que invocó el comando.
        message_content (str): El contenido del mensaje de texto a enviar.
    """
    try:
        await ctx.send(message_content)
        print(f"Mensaje de texto enviado: '{message_content}' en el canal '{ctx.channel.name}'")
    except discord.Forbidden:
        print(f"Error: No tengo permisos para enviar mensajes en el canal '{ctx.channel.name}'.")
    except discord.HTTPException as e:
        print(f"Error HTTP al enviar mensaje de texto: {e}")
    except Exception as e:
        print(f"Ocurrió un error inesperado al enviar mensaje de texto: {e}")

# Puedes añadir funciones para enviar mensajes embebidos (embeds) aquí
async def send_embed_message(ctx: commands.Context, title: str, description: str, color: discord.Color = discord.Color.blue()):
    """
    Envía un mensaje embebido (embed) al canal.

    Args:
        ctx (commands.Context): El contexto del comando.
        title (str): El título del embed.
        description (str): La descripción del embed.
        color (discord.Color): El color de la barra lateral del embed.
    """
    embed = discord.Embed(
        title=title,
        description=description,
        color=color
    )
    try:
        await ctx.send(embed=embed)
        print(f"Mensaje embebido enviado: '{title}' en el canal '{ctx.channel.name}'")
    except discord.Forbidden:
        print(f"Error: No tengo permisos para enviar embeds en el canal '{ctx.channel.name}'.")
    except discord.HTTPException as e:
        print(f"Error HTTP al enviar embed: {e}")
    except Exception as e:
        print(f"Ocurrió un error inesperado al enviar embed: {e}")
