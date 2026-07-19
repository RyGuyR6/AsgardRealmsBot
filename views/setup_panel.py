import discord

class SetupPanel(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Welcome",
        emoji="👋",
        style=discord.ButtonStyle.blurple,
        custom_id="setup:welcome"
    )
    async def welcome(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):
        await interaction.response.send_message(
            "Welcome configuration coming soon.",
            ephemeral=True
        )

    @discord.ui.button(
        label="Moderation",
        emoji="🛡️",
        style=discord.ButtonStyle.red,
        custom_id="setup:moderation"
    )
    async def moderation(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):
        await interaction.response.send_message(
            "Moderation configuration coming soon.",
            ephemeral=True
        )

    @discord.ui.button(
        label="Tickets",
        emoji="🎫",
        style=discord.ButtonStyle.green,
        custom_id="setup:tickets"
    )
    async def tickets(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):
        await interaction.response.send_message(
            "Ticket configuration coming soon.",
            ephemeral=True
        )

    @discord.ui.button(
        label="Logging",
        emoji="📜",
        style=discord.ButtonStyle.gray,
        custom_id="setup:logging"
    )
    async def logging(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):
        await interaction.response.send_message(
            "Logging configuration coming soon.",
            ephemeral=True
        )
