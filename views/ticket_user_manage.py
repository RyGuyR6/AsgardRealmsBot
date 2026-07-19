import discord


class AddUserModal(discord.ui.Modal, title="Add User"):

    user_id = discord.ui.TextInput(
        label="User ID",
        placeholder="Enter Discord User ID",
        required=True,
    )

    async def on_submit(self, interaction: discord.Interaction):

        try:
            member = await interaction.guild.fetch_member(
                int(self.user_id.value)
            )
        except Exception:
            await interaction.response.send_message(
                "❌ User not found.",
                ephemeral=True,
            )
            return

        await interaction.channel.set_permissions(
            member,
            view_channel=True,
            send_messages=True,
            read_message_history=True,
        )

        await interaction.response.send_message(
            f"✅ Added {member.mention} to the ticket."
        )


class RemoveUserModal(discord.ui.Modal, title="Remove User"):

    user_id = discord.ui.TextInput(
        label="User ID",
        placeholder="Enter Discord User ID",
        required=True,
    )

    async def on_submit(self, interaction: discord.Interaction):

        try:
            member = await interaction.guild.fetch_member(
                int(self.user_id.value)
            )
        except Exception:
            await interaction.response.send_message(
                "❌ User not found.",
                ephemeral=True,
            )
            return

        await interaction.channel.set_permissions(
            member,
            overwrite=None,
        )

        await interaction.response.send_message(
            f"🗑 Removed {member.mention} from the ticket."
        )
