import disnake
from disnake.ext import commands, tasks
import aiohttp
import sqlite3
import os

class Linker(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.tg_token = os.getenv("TG_TOKEN")
        self.db_path = "gate.db"
        self.last_update_id = -1
        self.init_db()
        self.sync_loop.start()

    def init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS topic_map (tg_topic_id INTEGER PRIMARY KEY, ds_channel_id INTEGER)')
        conn.commit()
        conn.close()

    @tasks.loop(seconds=2)
    async def sync_loop(self):
        if not self.tg_token: return
        async with aiohttp.ClientSession() as session:
            url = f"https://api.telegram.org/bot{self.tg_token}/getUpdates"
            params = {"offset": self.last_update_id + 1, "timeout": 5}
            try:
                async with session.get(url, params=params) as response:
                    if response.status != 200: return
                    data = await response.json()
                    for update in data.get("result", []):
                        self.last_update_id = update["update_id"]
                        msg = update.get("message") or update.get("channel_post")
                        if not msg: continue
                        
                        t_id = msg.get("message_thread_id", 0)
                        text = msg.get("text") or msg.get("caption") or "[Медіа]"
                        
                        conn = sqlite3.connect(self.db_path)
                        cursor = conn.cursor()
                        cursor.execute("SELECT ds_channel_id FROM topic_map WHERE tg_topic_id = ?", (t_id,))
                        row = cursor.fetchone()
                        conn.close()
                        if row:
                            channel = self.bot.get_channel(int(row[0]))
                            if channel: await channel.send(f"💬 **Telegram:** {text}")
            except: pass

    @commands.command(name="link_topic")
    async def link_topic(self, ctx, tg_id: int):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("INSERT OR REPLACE INTO topic_map (tg_topic_id, ds_channel_id) VALUES (?, ?)", (tg_id, ctx.channel.id))
        conn.commit()
        conn.close()
        await ctx.send(f"🔗 Зв'язок встановлено: TG {tg_id} -> <#{ctx.channel.id}>")

def setup(bot):
    bot.add_cog(Linker(bot))
