import disnake
from disnake.ext import commands

class Helper(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.remove_command("help")

    @commands.command(name="help")
    async def help_command(self, ctx):
        embed = disnake.Embed(title="🖥️ VEYRONIX OS | ГІД", color=0x2b2d31)
        embed.add_field(name="📢 Broadcast", value="`!broadcast [текст]`", inline=False)
        embed.add_field(name="🔗 Linker", value="`!link_topic [ID]`", inline=False)
        embed.add_field(name="🛠️ System", value="`!status`, `!clear [n]`, `!verify [@user]`", inline=False)
        embed.set_footer(text="Veyronix Studios | Authorized Only")
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Helper(bot))
