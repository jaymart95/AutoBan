from dataclasses import dataclass
import logging
from datetime import datetime

import disnake
from disnake.embeds import Embed
from disnake.utils import get
from disnake.ext.commands import Cog
from disnake.ext.commands.slash_core import slash_command
from disnake.ext.commands import has_permissions
from lib.db import db
import json

##Change ID to your Guild ID##
guild_ids=[938542872700018688]

class AutoBan(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up('AutoBan')
            ##Change ID to your own log channel##
            self.log_channel = self.bot.get_channel(939916860294561873)

    @slash_command(name='abl', guild_ids=guild_ids)
    @has_permissions(manage_guild=True)
    async def blacklist(self, inter, memberid = None, name = None):
        if memberid is not None:
            _check = db.record("SELECT is_blacklisted FROM users WHERE UserID = ?", memberid)
            if int(1) in _check:
                await inter.send('Member ID already blacklisted!', ephemeral=True)
                return
            db.execute("UPDATE users SET is_blacklisted = ? WHERE UserID = ?", True, memberid)
            await inter.send("Member ID added!", ephemeral=True)
            return
        if name is not None:
            _check = db.record("SELECT dName FROM names")
            if name in _check:
                await inter.send('Member name already blacklisted!', ephemeral=True)
                return
            db.execute("INSERT OR IGNORE INTO names (dName) VALUES (?)", name)
            await inter.send("Member name blacklisted!", ephemeral=True)
        db.commit()


    @slash_command(name='rbl', guild_ids=guild_ids)
    @has_permissions(manage_guild=True)
    async def remove_blacklist(self, inter, memberid):
        """Remove a members id from the blacklist"""
        _check = db.record("SELECT is_blacklisted FROM users WHERE UserID = ?", memberid)
        if int(0) in _check:
            await inter.send('Member ID not blacklisted!', ephemeral=True)
            return
        db.execute("UPDATE users SET is_blacklisted = ? WHERE UserID = ?", False, memberid)
        await inter.send("Member ID removed!", ephemeral=True)



    @Cog.listener()
    async def on_member_join(self, member):
        _check = db.record("SELECT is_blacklisted FROM users WHERE UserID = ?", member)
        if int(1) in _check:
            await member.ban(reason="Blacklisted Member")
            embed = disnake.Embed(title='Member banned', description='Blacklisted member')
            embed.add_field(name='Member', value=member.mention, inline=False)
            embed.set_thumbnail(url=member.avatar.url)
            embed.set_footer(text="Member ID: {}".format(member.id))
            await self.log_channel.send(embed=embed)

            




def setup(bot):
    bot.add_cog(AutoBan(bot))
