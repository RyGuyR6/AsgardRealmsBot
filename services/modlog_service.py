from embeds import make_embed

async def send(channel, title, description):
    if channel is None:
        return

    embed = make_embed(title, description)
    await channel.send(embed=embed)
