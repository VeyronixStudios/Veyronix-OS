import disnake
from disnake.ext import commands
import aiohttp
import os

class Broadcaster(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.tg_token = os.getenv("TG_TOKEN")
        self.official_id = -1003855629073

    @commands.command(name="broadcast")
    async def broadcast(self, ctx, *, message: str):
        # Discord
        embed = disnake.Embed(title="🛰️ VEYRONIX STUDIOS | OFFICIAL", description=message, color=0x2b2d31)
        embed.set_thumbnail(url=self.bot.user.display_avatar.url)
        await ctx.send(embed=embed)
        # Telegram
        if self.tg_token:
            url = f"https://api.telegram.org/bot{self.tg_token}/sendMessage"
            payload = {"chat_id": self.official_id, "text": f"🛰️ *VEYRONIX STUDIOS | OFFICIAL*\n\n{message}", "parse_mode": "Markdown"}
            async with aiohttp.ClientSession() as session:
                await session.post(url, json=payload)

def setup(bot):
    bot.add_cog(Broadcaster(bot))
