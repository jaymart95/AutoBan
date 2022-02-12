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
guild_ids=[GUILD ID]
configData = open("./config.json", "r", encoding="utf-8")

class AutoBan(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up('AutoBan')
            ##Change ID to your own log channel##
            self.log_channel = self.bot.get_channel(CHANNEL ID)

    @slash_command(name='abl', guild_ids=guild_ids)
    @has_permissions(manage_guild=True)
    async def blacklist(self, inter, memberid):
        """Add a members id to the blacklist"""
        with open("./data/blacklist.json", "r+", encoding="utf-8") as f:
            data = json.load(f)
            if memberid in data:
                await inter.send("Member ID already added!", ephemeral=True)
                return
            data.append(memberid)
            f.seek(0)
            json.dump(data, f)
            f.truncate()
            await inter.send("Member ID added!", ephemeral=True)

    @slash_command(name='rbl', guild_ids=guild_ids)
    @has_permissions(manage_guild=True)
    async def remove_blacklist(self, inter, memberid):
        """Remove a members id from the blacklist"""
        with open("./data/blacklist.json", "r+", encoding="utf-8") as f:
            data = json.load(f)
            if memberid not in data:
                await inter.send("Member ID not found!", ephemeral=True)
                return
            data.remove(memberid)
            f.seek(0)
            json.dump(data, f)
            f.truncate()
            await inter.send("Member ID removed!", ephemeral=True)

    #Currently working on a fix.
    @slash_command(guild_ids=guild_ids)
    @has_permissions(manage_guild=True)
    async def unban(self, inter, memberid: int):
        """Unban a member by their ID"""
        member = disnake.Object(memberid)
        #user = await self.bot.fetch_user(member)
        await inter.guild.unban(member)
        await inter.send("Member unbanned!", ephemeral=True)



    @Cog.listener()
    async def on_member_join(self, member):
        with open("./data/blacklist.json", "r") as json_file:
            json_dict = json.load(json_file)
            if [member.id == i for i in json_dict]:
                await member.ban(reason="Blacklisted Member")
                embed = disnake.Embed(title='Member banned', description='Blacklisted member')
                embed.add_field(name='Member', value=member.mention, inline=False)
                embed.set_thumbnail(url=member.avatar.url)
                embed.set_footer(text="Member ID: {}".format(member.id))
                await configData["LOG_CHANNEL"].send(embed=embed)

            




def setup(bot):
    bot.add_cog(AutoBan(bot))
