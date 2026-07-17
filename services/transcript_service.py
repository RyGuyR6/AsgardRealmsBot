import discord
import html
import os
from datetime import datetime

TRANSCRIPT_FOLDER = "transcripts"

os.makedirs(TRANSCRIPT_FOLDER, exist_ok=True)


async def create_transcript(channel: discord.TextChannel):
    """
    Creates an HTML transcript of a ticket channel.

    Returns:
        (filepath, filename)
    """

    filename = f"{channel.name}.html"
    filepath = os.path.join(TRANSCRIPT_FOLDER, filename)

    messages = []

    async for message in channel.history(limit=None, oldest_first=True):
        messages.append(message)

    with open(filepath, "w", encoding="utf-8") as f:

        f.write("""
<!DOCTYPE html>
<html>
<head>

<meta charset="utf-8">

<title>Odin Ticket Transcript</title>

<style>

body{
background:#2b2d31;
color:white;
font-family:Arial;
padding:20px;
}

.message{
margin-bottom:18px;
padding:12px;
background:#1e1f22;
border-radius:8px;
}

.author{
font-weight:bold;
color:#57F287;
font-size:16px;
}

.time{
font-size:12px;
color:gray;
margin-bottom:8px;
}

.content{
white-space:pre-wrap;
}

img.avatar{
width:40px;
height:40px;
border-radius:50%;
vertical-align:middle;
margin-right:10px;
}

.attachments{
margin-top:10px;
}

</style>

</head>

<body>

<h1>Odin Ticket Transcript</h1>

<hr>
""")

        for message in messages:

            avatar = message.author.display_avatar.url

            timestamp = message.created_at.strftime(
                "%Y-%m-%d %H:%M:%S UTC"
            )

            content = html.escape(message.content)

            f.write(f"""
<div class="message">

<div class="author">
<img class="avatar" src="{avatar}">
{html.escape(str(message.author))}
</div>

<div class="time">
{timestamp}
</div>

<div class="content">
{content}
</div>
""")

            if message.attachments:

                f.write('<div class="attachments">')

                for attachment in message.attachments:

                    f.write(
                        f'<p><a href="{attachment.url}">{attachment.filename}</a></p>'
                    )

                f.write("</div>")

            if message.embeds:

                f.write("<p><em>Embed Sent</em></p>")

            f.write("</div>")

        f.write("""

</body>
</html>

""")

    return filepath, filename