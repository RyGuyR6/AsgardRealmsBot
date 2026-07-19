import discord

from services import settings_service
from views.welcome_setup import WelcomeSetupView


class ModLogChannelSelect(discord.ui.ChannelSelect):

    def __init__(self):
        super().__init__(
            channel_types=[discord.ChannelType.text],
            placeholder="Select the moderation log channel...",
            min_values=1,
            max_values=1,
        )

    async def callback(self, interaction: discord.Interaction):

        channel = self.values[0]

        settings_service.set_value(
            interaction.guild.id,
            "modlog_channel",
            channel.id,
        )

        await interaction.response.send_message(
            f"✅ Moderation log channel set to {channel.mention}",
            ephemeral=True,
        )


class ModLogView(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=300)
        self.add_item(ModLogChannelSelect())


class SetupPanel(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Welcome",
        emoji="👋",
        style=discord.ButtonStyle.blurple,
    )
    async def welcome(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button,
    ):
        await interaction.response.send_message(
            "Configure welcome settings below.",
            view=WelcomeSetupView(),
            ephemeral=True,
        )

    @discord.ui.button(
        label="Moderation",
        emoji="🛡️",
        style=discord.ButtonStyle.red,
    )
    async def moderation(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button,
    ):
        await interaction.response.send_message(
            "Select a moderation log channel.",
            view=ModLogView(),
            ephemeral=True,
        )

    @discord.ui.button(
        label="Tickets",
        emoji="🎫",
        style=discord.ButtonStyle.green,
    )
    async def tickets(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button,
    ):
        await interaction.response.send_message(
            "Coming soon.",
            ephemeral=True,
        )

    @discord.ui.button(
        label="Logging",
        emoji="📜",
        style=discord.ButtonStyle.gray,
    )
    async def logging(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button,
    ):
        await interaction.response.send_message(
            "Coming soon.",
            ephemeral=True,
        )
