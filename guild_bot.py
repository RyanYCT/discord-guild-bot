import logging
import os
import sys

import discord
from discord.ext import commands

import config

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

class GuildBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="/", intents=intents)

    async def on_ready(self):
        """
        Load all cog files, and sync commands at launch.
        """
        logger.info("Python %s", sys.version)
        logger.info("discord.py %s", discord.__version__)
        logger.info("Logged in as %s (%s)", self.user.name, self.user.id)

        # Load listed cog files
        number_of_cogs = len(config.cog_list)
        count = 0
        for file in config.cog_list:
            count += 1
            file = file[:-3]
            try:
                await self.load_extension(f"cogs.{file}")
            except commands.ExtensionNotFound as enf:
                logger.exception("Failed to load %s: %s", file, enf)
            else:
                logger.info("Loaded %s [%d/%d]", file, count, number_of_cogs)

        # # Load all cog files
        # cogs_dir = os.listdir(config.cogs_dir)
        # number_of_cogs = len(cogs_dir) - 1
        # count = 0
        # for file in cogs_dir:
        #     if not file.startswith("__") and file.endswith(".py"):
        #         count += 1
        #         file = file[:-3]
        #         try:
        #             await self.load_extension(f"cogs.{file}")
        #         except commands.ExtensionNotFound as enf:
        #             logger.exception("Failed to load %s: %s", file, enf)
        #         else:
        #             logger.info("Loaded %s [%d/%d]", file, count, number_of_cogs)

        # Sync commands
        try:
            await self.tree.sync()
        except Exception as e:
            logger.exception("Failed to sync commands: %s", e)
        else:
            logger.info("Synced commands")
            logger.info("Bot is ready")
