# create_button.py
import discord

def create_button_component(custom_id: str, label: str, style: discord.ButtonStyle = discord.ButtonStyle.secondary, url: str = None, emoji: str = None, disabled: bool = False):
    """
    Crea un componente de botón para Discord.

    Args:
        custom_id (str): Un ID único para el botón. Se usará para identificar la interacción.
                         Este ID es obligatorio para botones que no son de tipo URL.
        label (str): El texto que se mostrará en el botón.
        style (discord.ButtonStyle): El estilo visual del botón (primary, secondary, success, danger, link).
                                     Por defecto es secondary (gris).
        url (str, optional): Si el estilo es discord.ButtonStyle.link, esta URL será el destino del botón.
                             custom_id no es necesario para botones de enlace.
        emoji (str, optional): Un emoji para mostrar en el botón. Puede ser un emoji unicode o un ID de emoji.
        disabled (bool, optional): Si el botón debe estar deshabilitado. Por defecto es False.

    Returns:
        discord.ui.Button: El objeto de botón creado.
    """
    if style == discord.ButtonStyle.link and not url:
        raise ValueError("Los botones de estilo 'link' requieren una URL.")
    if style != discord.ButtonStyle.link and not custom_id:
        raise ValueError("Los botones que no son de estilo 'link' requieren un custom_id.")

    button = discord.ui.Button(
        label=label,
        style=style,
        custom_id=custom_id if style != discord.ButtonStyle.link else None, # custom_id solo para botones no URL
        url=url if style == discord.ButtonStyle.link else None, # URL solo para botones de enlace
        emoji=emoji,
        disabled=disabled
    )
    return button

# Ejemplo de uso (no se ejecuta directamente, es para referencia)
if __name__ == '__main__':
    # Ejemplo de cómo crear diferentes tipos de botones
    print("Ejemplos de creación de botones (esto no se ejecuta en el bot):")

    # Botón primario
    primary_btn = create_button_component(
        custom_id="primary_action",
        label="Acción Principal",
        style=discord.ButtonStyle.primary
    )
    print(f"Botón Primario: {primary_btn.label}, ID: {primary_btn.custom_id}")

    # Botón de enlace
    link_btn = create_button_component(
        custom_id=None, # No se necesita custom_id para botones de enlace
        label="Visitar Google",
        style=discord.ButtonStyle.link,
        url="https://www.google.com"
    )
    print(f"Botón de Enlace: {link_btn.label}, URL: {link_btn.url}")

    # Botón con emoji
    emoji_btn = create_button_component(
        custom_id="emoji_action",
        label="Me gusta",
        style=discord.ButtonStyle.success,
        emoji="👍"
    )
    print(f"Botón con Emoji: {emoji_btn.label}, Emoji: {emoji_btn.emoji}")
