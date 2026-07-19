import discord
from services import settings_service


class AutoroleSelect(discord.ui.RoleSelect):

    def __init__(self):
        super().__init__(
            placeholder="Select the default member role...",
            min_values=1,
            max_values=1
        )

    async def callback(self, interaction: discord.Interaction):

        role = self.values[0]

        settings_service.set_value(
            interaction.guild.id,
            "autorole",
            role.id
        )

        await interaction.response.send_message(
            f"✅ Autorole set to {role.mention}",
            ephemeral=True
        )


class AutoroleView(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=300)
        self.add_item(AutoroleSelect())
