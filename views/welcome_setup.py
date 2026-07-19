import discord
from services import settings_service


class WelcomeChannelSelect(discord.ui.ChannelSelect):
    def __init__(self):
        super().__init__(
            placeholder="Select Welcome Channel",
            channel_types=[discord.ChannelType.text],
            min_values=1,
            max_values=1,
        )

    async def callback(self, interaction: discord.Interaction):
        channel = self.values[0]

        settings_service.set_value(
            interaction.guild.id,
            "welcome_channel",
            channel.id,
        )

        await interaction.response.send_message(
            f"✅ Welcome channel set to {channel.mention}",
            ephemeral=True,
        )


class LeaveChannelSelect(discord.ui.ChannelSelect):
    def __init__(self):
        super().__init__(
            placeholder="Select Leave Channel",
            channel_types=[discord.ChannelType.text],
            min_values=1,
            max_values=1,
        )

    async def callback(self, interaction: discord.Interaction):
        channel = self.values[0]

        settings_service.set_value(
            interaction.guild.id,
            "leave_channel",
            channel.id,
        )

        await interaction.response.send_message(
            f"✅ Leave channel set to {channel.mention}",
            ephemeral=True,
        )


class WelcomeSetupView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=300)
        self.add_item(WelcomeChannelSelect())
        self.add_item(LeaveChannelSelect())
