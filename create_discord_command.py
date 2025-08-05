# create_discord_command.py
# Este script te ayudará a crear un nuevo módulo de comando para tu bot de Discord.

import os
import re

# --- Configuración de rutas (ajusta si es necesario) ---
# Asegúrate de que esta ruta sea correcta para tu estructura de proyecto
# Es decir, la carpeta donde se encuentran send_message.py, send_resource.py, etc.
MAIN_MOD_DIR = "main_mod"
COMMAND_MOD_DIR = "bot_discord_escalable\\command_mod" # Carpeta para los módulos de comando generados

# --- Lista de Emojis Predefinidos ---
# Puedes expandir esta lista con más emojis si lo deseas
EMOJI_OPTIONS = {
    '1': '👍', # Thumbs Up
    '2': '👎', # Thumbs Down
    '3': '✅', # Check Mark Button
    '4': '❌', # Cross Mark
    '5': '💡', # Light Bulb
    '6': '🚀', # Rocket
    '7': '⭐', # Star
    '8': '🎉', # Party Popper
    '9': '❓', # Question Mark
    '10': 'ℹ️' # Information
}

# --- Funciones auxiliares ---

def sanitize_name(name):
    """Limpia el nombre para que sea un identificador Python válido."""
    name = re.sub(r'\W|^(?=\d)', '_', name) # Reemplaza caracteres no alfanuméricos con _ y asegura que no empiece con dígito
    return name.lower()

def get_valid_input(prompt, validation_regex=None):
    """Obtiene una entrada de usuario validada."""
    while True:
        user_input = input(prompt).strip()
        if user_input:
            if validation_regex and not re.match(validation_regex, user_input):
                print("Entrada inválida. Por favor, intenta de nuevo con el formato correcto.")
            else:
                return user_input
        else:
            print("La entrada no puede estar vacía. Por favor, intenta de nuevo.")

def get_yes_no_input(prompt):
    """Obtiene una respuesta de sí/no."""
    while True:
        response = input(f"{prompt} (s/n): ").strip().lower()
        if response in ['s', 'si', 'y', 'yes']:
            return True
        elif response in ['n', 'no']:
            return False
        else:
            print("Respuesta inválida. Por favor, responde 's' o 'n'.")

# --- Recopilación de información del comando ---

print("## Generador de Comandos para Bot de Discord")
print("Este script te ayudará a crear un nuevo módulo de comando para tu bot.")

command_name_raw = get_valid_input("Introduce el nombre del comando (ej. 'mi_comando', 'saludo_personalizado'): ")
command_name = sanitize_name(command_name_raw)
print(f"Nombre del comando generado: `{command_name}`")

# Mensaje
add_message = get_yes_no_input("¿Deseas que el comando envíe un mensaje de texto inicial?")
message_content = ""
if add_message:
    message_content = get_valid_input("Introduce el contenido del mensaje: ")

# Recurso (Link/Imagen)
add_resource = get_yes_no_input("¿Deseas que el comando envíe un recurso (link o imagen desde URL)?")
resource_url = ""
if add_resource:
    resource_url = get_valid_input("Introduce la URL del recurso: ", validation_regex=r"https?://[^\s]+")

# Botones
add_buttons = get_yes_no_input("¿Deseas agregar botones al mensaje inicial?")
buttons_data = []
if add_buttons:
    while True:
        try:
            num_buttons = int(get_valid_input("¿Cuántos botones deseas agregar? "))
            if num_buttons > 0:
                break
            else:
                print("Por favor, introduce un número mayor que 0.")
        except ValueError:
            print("Entrada inválida. Por favor, introduce un número.")

    for i in range(num_buttons):
        print(f"\n--- Configuración del Botón {i+1} ---")
        button_label = get_valid_input(f"Etiqueta para el botón {i+1}: ")
        button_style_options = {
            '1': 'primary (azul)',
            '2': 'secondary (gris)',
            '3': 'success (verde)',
            '4': 'danger (rojo)',
            '5': 'link (enlace URL)'
        }
        print("Estilos de botón disponibles:")
        for key, value in button_style_options.items():
            print(f"  {key}: {value}")
        
        while True:
            style_choice = get_valid_input(f"Elige el estilo para el botón {i+1} (1-5): ")
            if style_choice in button_style_options:
                button_style_str = {
                    '1': 'discord.ButtonStyle.primary',
                    '2': 'discord.ButtonStyle.secondary',
                    '3': 'discord.ButtonStyle.success',
                    '4': 'discord.ButtonStyle.danger',
                    '5': 'discord.ButtonStyle.link'
                }[style_choice]
                break
            else:
                print("Opción inválida. Por favor, elige un número del 1 al 5.")

        button_url = ""
        if style_choice == '5': # Link button
            button_url = get_valid_input(f"Introduce la URL para el botón {i+1} (obligatorio para estilo 'link'): ", validation_regex=r"https?://[^\s]+")
            button_custom_id = None # Link buttons don't use custom_id, store as Python None
        else:
            # Generate a unique custom_id for non-link buttons
            button_custom_id = f'{command_name}_btn_{i+1}' # Store as raw string, will be quoted later

        # --- Selección de Emoji ---
        add_emoji = get_yes_no_input(f"¿Deseas agregar un emoji al botón {i+1}?")
        button_emoji = None # Initialize as Python None
        if add_emoji:
            print("\n--- Selecciona un Emoji ---")
            for num, emoji_char in EMOJI_OPTIONS.items():
                print(f"  {num}: {emoji_char}")
            print(f"  {len(EMOJI_OPTIONS) + 1}: (Ingresar emoji personalizado)")

            while True:
                emoji_choice = get_valid_input(f"Elige un número de emoji o {len(EMOJI_OPTIONS) + 1} para personalizar: ")
                if emoji_choice.isdigit():
                    emoji_choice_int = int(emoji_choice)
                    if 1 <= emoji_choice_int <= len(EMOJI_OPTIONS):
                        button_emoji = EMOJI_OPTIONS[emoji_choice] # Store raw emoji string
                        break
                    elif emoji_choice_int == len(EMOJI_OPTIONS) + 1:
                        button_emoji = get_valid_input("Introduce el emoji personalizado (ej. '👍' o ID de emoji): ")
                        break
                    else:
                        print("Opción inválida. Por favor, elige un número de la lista.")
                else:
                    print("Entrada inválida. Por favor, introduce un número.")
        # --- Fin Selección de Emoji ---

        # Acción del botón
        button_action_type = ""
        button_action_content = ""
        button_action_options = {
            '1': 'Enviar mensaje',
            '2': 'Enviar recurso (link/imagen)',
            '3': 'Acción compleja (ej. crear más botones - requiere lógica avanzada)'
        }
        print("Acciones disponibles para el botón:")
        for key, value in button_action_options.items():
            print(f"  {key}: {value}")
        
        while True:
            action_choice = get_valid_input(f"Elige la acción para el botón {i+1} (1-3): ")
            if action_choice == '1':
                button_action_type = "message"
                button_action_content = get_valid_input("Contenido del mensaje a enviar al hacer clic: ")
                break
            elif action_choice == '2':
                button_action_type = "resource"
                button_action_content = get_valid_input("URL del recurso a enviar al hacer clic: ", validation_regex=r"https?://[^\s]+")
                break
            elif action_choice == '3':
                button_action_type = "complex"
                button_action_content = "Esta acción requiere lógica personalizada para generar más botones o un flujo complejo."
                print("⚠️ Nota: La acción 'crear más botones' en este script generará un mensaje indicando que se necesita lógica avanzada. Para una implementación completa, deberás añadir esa lógica manualmente en el callback del botón.")
                break
            else:
                print("Opción inválida. Por favor, elige un número del 1 al 3.")

        buttons_data.append({
            'label': button_label,
            'style': button_style_str,
            'custom_id': button_custom_id, # Can be string or None
            'url': button_url, # Can be string or None
            'emoji': button_emoji, # Can be string or None
            'action_type': button_action_type,
            'action_content': button_action_content
        })

# --- Generación del código Python ---

generated_code = f"""
# cmd_{command_name}.py
# Este archivo fue generado automáticamente por create_discord_command.py

import discord
from discord.ext import commands
# Importa desde main_mod ya que send_message, send_resource, create_button están allí
from {MAIN_MOD_DIR}.send_message import send_text_message
from {MAIN_MOD_DIR}.send_resource import send_resource_message
from {MAIN_MOD_DIR}.create_button import create_button_component # Usado para crear los objetos Button

class {command_name.replace('_', '').title()}Command(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="{command_name}")
    async def {command_name}_command(self, ctx: commands.Context):
        \"\"\"
        Comando '{command_name}'
        \"\"\"
        print(f"Comando '{command_name}' invocado por {{ctx.author.name}}")

"""

if add_message:
    generated_code += f"""
        await send_text_message(ctx, "{message_content}")
"""

if add_resource:
    generated_code += f"""
        await send_resource_message(ctx, "{resource_url}")
"""

if add_buttons:
    generated_code += f"""
        # Definir una vista (View) para los botones
        class {command_name.replace('_', '').title()}View(discord.ui.View):
            def __init__(self, original_ctx):
                super().__init__(timeout=180) # Los botones expiran después de 3 minutos
                self.original_ctx = original_ctx

"""
    for i, btn in enumerate(buttons_data):
        # Construir dinámicamente los argumentos para el decorador @discord.ui.button
        button_args = [
            f'label="{btn["label"]}"',
            f'style={btn["style"]}'
        ]
        
        # custom_id solo si no es None (es decir, no es un botón de enlace)
        if btn['custom_id'] is not None:
            button_args.append(f'custom_id="{btn["custom_id"]}"')
        
        # url solo si el estilo es 'link' y la url no es None
        if btn['style'] == 'discord.ButtonStyle.link' and btn['url'] is not None:
            button_args.append(f'url="{btn["url"]}"')
        
        # emoji solo si no es None
        if btn['emoji'] is not None:
            button_args.append(f'emoji="{btn["emoji"]}"') # Asegurarse de que el emoji se cite correctamente

        generated_code += f"""
            @discord.ui.button({', '.join(button_args)})
            async def button_{i+1}_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
                await interaction.response.defer(ephemeral=True) # Defer the interaction to avoid "This interaction failed"

"""
        if btn['action_type'] == "message":
            generated_code += f"""
                await interaction.followup.send("{btn['action_content']}", ephemeral=True)
"""
        elif btn['action_type'] == "resource":
            generated_code += f"""
                await send_resource_message(self.original_ctx, "{btn['action_content']}")
                await interaction.followup.send("Recurso enviado.", ephemeral=True)
"""
        elif btn['action_type'] == "complex":
            generated_code += f"""
                await interaction.followup.send("Esta acción ('{btn['action_content']}') requiere lógica avanzada. Implementa aquí la creación de más botones o un flujo complejo.", ephemeral=True)
"""

    generated_code += f"""
        view = {command_name.replace('_', '').title()}View(ctx)
        await ctx.send("Aquí tienes los botones:", view=view)

"""

generated_code += f"""
async def setup(bot):
    await bot.add_cog({command_name.replace('_', '').title()}Command(bot))

"""

# --- Guardar el archivo ---

output_dir = os.path.join(os.getcwd(), COMMAND_MOD_DIR)
os.makedirs(output_dir, exist_ok=True) # Asegurarse de que el directorio exista

output_filename = os.path.join(output_dir, f"cmd_{command_name}.py")

with open(output_filename, "w", encoding="utf-8") as f:
    f.write(generated_code)

print(f"---")
print(f"**¡Comando generado exitosamente!**")
print(f"El archivo `{output_filename}` ha sido creado.")
print(f"Para integrar este comando en tu bot, añade la siguiente línea en tu `bot.py` (dentro de `on_ready` o en una función de carga de extensiones):")
print(f"```python\n    await bot.load_extension(f'{COMMAND_MOD_DIR}.cmd_{command_name}')\n```")
print(f"Recuerda que para que los comandos de barra (`/`) se actualicen, el bot debe ser reiniciado o los comandos sincronizados manualmente.")
