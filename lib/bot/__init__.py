from asyncio import sleep
from datetime import datetime
from pathlib import Path
from glob import glob

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from disnake import Embed, Intents
from disnake.errors import Forbidden
from disnake.ext import commands
from disnake.ext.commands import Bot as Jay
from disnake.ext.commands import CommandNotFound, BadArgument, MissingRequiredArgument
from disnake.ext.commands.bot import when_mentioned_or
from disnake.ext.commands.errors import CommandOnCooldown, MissingPermissions
from lib.db import db
import logging

PREFIX = '!'
OWNER_ID = [485183782328991745]
cogs = [p.stem for p in Path('.').glob("./lib/cogs/*.py")]
IGNORE_EXCEPTIONS = (CommandNotFound, BadArgument)


def get_prefix(bot, message):
    return when_mentioned_or(PREFIX)(bot, message)


class Ready(object):
    def __init__(self):
        for cog in cogs:
            setattr(self, cog, False)

    def ready_up(self, cog):
        setattr(self, cog, True)
        logging.info(f'{cog} cog ready')

    def all_ready(self):
        return all([getattr(self, cog) for cog in cogs])


class Bot(Jay):
    def __init__(self):
        self.PREFIX = PREFIX
        self.cogs_ready = Ready()
        self.scheduler = AsyncIOScheduler()
        self.ready = False

        db.autosave(self.scheduler)

        super().__init__(
            command_prefix=get_prefix,
            owner_id=OWNER_ID,
            intents=Intents.all(),
        )

    def setup(self):
        for cog in cogs:
            self.load_extension(f'lib.cogs.{cog}')
            logging.info(f'{cog} cog loaded')

        logging.info('setup complete')

    def update_db(self):
        db.multiexec('INSERT OR IGNORE INTO users (UserUD) VALUES (?)',
                     ((member.id,) for member in self.guild.members if not member.bot))

        db.commit()

    def run(self, version):
        self.VERSION = version
        logging.info('Running setup...')
        self.setup()

        with open('./lib/bot/token.0', 'r', encoding='utf-8') as tf:
            self.TOKEN = tf.read()

        logging.info('running bot....')
        super().run(self.TOKEN, reconnect=True)

    async def process_commands(self, message):
        ctx = await self.get_context(message, cls=commands.Context)

        if ctx.command is not None and ctx.guild is not None:
            await self.invoke(ctx)

    async def on_connect(self):
        logging.info('bot connected')

    async def on_disconnect(self):
        db.commit()
        logging.warn('bot disconnect')

    async def on_error(self, err, *args, **kwargs):
        if err == 'on_command_error':
            await args[0].send('Something went wrong')

            await self.stdout.send('An error occured')

        raise

    async def on_command_error(self, inter, exc):
        if any([isinstance(exc, error) for error in IGNORE_EXCEPTIONS]):
            await inter.send('Error')

        elif isinstance(exc, MissingPermissions):
            await inter.send('You do not have permission to do that')

        elif isinstance(exc, MissingRequiredArgument):
            await inter.send('Missing required arguments.')

        elif isinstance(exc, CommandOnCooldown):
            await inter.send(f"That command is on cooldown. Try again in {exc.retry_after:,.2f} secs.")

        elif hasattr(exc, 'original'):
            # await inter.send('Unable to send message.')

            if isinstance(exc.original, Forbidden):
                await inter.send('I do not have permission to do that.')

            else:
                raise exc.original

    async def on_ready(self):
        if not self.ready:
            ##Change to own Guild ID##
            self.guild = self.get_guild(938542872700018688)
            self.scheduler.start()
            self.update_db()
            self.bot = bot

            while not self.cogs_ready.all_ready():
                await sleep(0.3)

            self.ready = True
            logging.info('bot ready')
            logging.info(f"Logged in as {bot.user.name}")

        else:
            logging.warn('bot reconnect')

    async def on_message(self, message):
        if not message.author.bot:
            await self.process_commands(message)


bot = Bot()
