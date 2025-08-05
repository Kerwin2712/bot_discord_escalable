
# cmd_bienvenida.py
# Este archivo fue generado automáticamente por create_discord_command.py

import discord
from discord.ext import commands
# Importa desde main_mod ya que send_message, send_resource, create_button están allí
from main_mod.send_message import send_text_message
from main_mod.send_resource import send_resource_message
from main_mod.create_button import create_button_component # Usado para crear los objetos Button

class BienvenidaCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="bienvenida")
    async def bienvenida_command(self, ctx: commands.Context):
        """
        Comando 'bienvenida'
        """
        print(f"Comando 'bienvenida' invocado por {ctx.author.name}")


        await send_text_message(ctx, "Bienvenido al equipo")

        # Definir una vista (View) para los botones
        class BienvenidaView(discord.ui.View):
            def __init__(self, original_ctx):
                super().__init__(timeout=180) # Los botones expiran después de 3 minutos
                self.original_ctx = original_ctx


            @discord.ui.button(label="Saludo", style=discord.ButtonStyle.primary, custom_id="bienvenida_btn_1", emoji="🎉")
            async def button_1_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
                await interaction.response.defer(ephemeral=True) # Defer the interaction to avoid "This interaction failed"


                await interaction.followup.send("Hola!", ephemeral=True)

            @discord.ui.button(label="Salir", style=discord.ButtonStyle.danger, custom_id="bienvenida_btn_2")
            async def button_2_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
                await interaction.response.defer(ephemeral=True) # Defer the interaction to avoid "This interaction failed"


                await interaction.followup.send("Adios!", ephemeral=True)

        view = BienvenidaView(ctx)
        await ctx.send("Aquí tienes los botones:", view=view)


async def setup(bot):
    await bot.add_cog(BienvenidaCommand(bot))

