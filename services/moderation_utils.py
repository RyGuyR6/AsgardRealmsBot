import discord


def hierarchy_check(actor: discord.Member,
                    target: discord.Member):

    if actor == target:
        return False, "You cannot moderate yourself."

    if target.guild.owner == target:
        return False, "You cannot moderate the owner."

    if actor.guild.owner == actor:
        return True, None

    if actor.top_role <= target.top_role:
        return (
            False,
            "Target has an equal or higher role."
        )

    return True, None
