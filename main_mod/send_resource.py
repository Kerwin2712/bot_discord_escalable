# send_resource.py
import discord
from discord.ext import commands
import aiohttp # Para hacer solicitudes HTTP asíncronas
import re # Para expresiones regulares, útil para detectar URLs de imagen

async def send_resource_message(ctx: commands.Context, url: str):
    """
    Envía un recurso, que puede ser un enlace de texto o una imagen a partir de una URL.
    Intenta detectar si la URL es una imagen y la adjunta; de lo contrario, la envía como texto.

    Args:
        ctx (commands.Context): El contexto del comando.
        url (str): La URL del recurso a enviar (enlace o imagen).
    """
    if not url:
        await ctx.send("Por favor, proporciona una URL para enviar.")
        print("Advertencia: send_resource_message llamado sin URL.")
        return

    # Patrón de expresión regular para detectar extensiones de archivo de imagen comunes
    image_pattern = re.compile(r'\.(png|jpg|jpeg|gif|webp)(\?.*)?$', re.IGNORECASE)

    if image_pattern.search(url):
        # La URL parece ser una imagen, intentar enviarla como adjunto
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    if resp.status != 200:
                        await ctx.send(f"No pude obtener la imagen de la URL: {url} (Código de estado: {resp.status})")
                        print(f"Error al obtener imagen de URL: {url} (Estado: {resp.status})")
                        return

                    data = await resp.read()
                    # Extrae el nombre del archivo de la URL o usa un nombre genérico
                    filename = url.split('/')[-1].split('?')[0]
                    if not filename or '.' not in filename: # Asegura que haya una extensión
                        filename = "image.png" # Nombre por defecto si no se puede extraer

                    discord_file = discord.File(data, filename=filename)
                    await ctx.send(f"Aquí tienes la imagen de: {url}", file=discord_file)
                    print(f"Imagen de URL '{url}' enviada en el canal '{ctx.channel.name}'")

        except aiohttp.ClientError as e:
            await ctx.send(f"Error de conexión al intentar obtener la imagen: {e}")
            print(f"Error de conexión al obtener imagen: {e}")
        except discord.Forbidden:
            await ctx.send(f"Error: No tengo permisos para adjuntar archivos en el canal '{ctx.channel.name}'.")
            print(f"Error: Permisos insuficientes para adjuntar archivos en '{ctx.channel.name}'.")
        except Exception as e:
            await ctx.send(f"Ocurrió un error inesperado al enviar la imagen: {e}")
            print(f"Error inesperado al enviar imagen: {e}")
    else:
        # La URL no parece ser una imagen, enviarla como texto
        try:
            await ctx.send(f"Aquí tienes el enlace: {url}")
            print(f"Enlace enviado: '{url}' en el canal '{ctx.channel.name}'")
        except discord.Forbidden:
            print(f"Error: No tengo permisos para enviar mensajes en el canal '{ctx.channel.name}'.")
        except discord.HTTPException as e:
            print(f"Error HTTP al enviar enlace: {e}")
        except Exception as e:
            print(f"Ocurrió un error inesperado al enviar enlace: {e}")

# La función send_image_from_url se ha integrado en send_resource_message para simplificar el módulo.
