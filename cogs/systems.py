import disnake
from disnake.ext import commands
import time

class Systems(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.start_time = time.time()

    @commands.command(name="status")
    async def status(self, ctx):
        ping = round(self.bot.latency * 1000)
        uptime = round(time.time() - self.start_time)
        await ctx.send(f"👁️ **Watcher**: Ping `{ping}ms` | Uptime `{uptime}s`")

    @commands.command(name="clear")
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int):
        await ctx.channel.purge(limit=amount + 1)
        await ctx.send(f"🧹 Видалено `{amount}`", delete_after=3)

    @commands.command(name="verify")
    async def verify(self, ctx, member: disnake.Member):
        role = disnake.utils.get(ctx.guild.roles, name="Verified")
        if role:
            await member.add_roles(role)
            await ctx.send(f"✅ {member.display_name} верифікований.")

def setup(bot):
    bot.add_cog(Systems(bot))
