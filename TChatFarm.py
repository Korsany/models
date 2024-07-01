# meta developer: @korsany
import random
from datetime import timedelta
import asyncio
import time
from telethon import events

from telethon import functions
from telethon.tl.types import Message

from .. import loader, utils


@loader.tds
class FarmMonacoMod(loader.Module):
    """Модуль для автоматического фарминга ниток в боте @TChat_TChat_bot"""

    strings = {"name": "TChatFarm"}

    def __init__(self):
        self.tasks = []

    async def b_run(self, client):
        while True:
            await client.send_message('@TChat_TChat_bot', "Фарм")
            await asyncio.sleep(14460)

    @loader.unrestricted
    @loader.ratelimit
    async def farmcmd(self, message):
        """Запустить автоматический фарминг в боте"""
        if self.tasks:
            return await message.edit("Автоматический фарминг уже запущен.")
        
        await message.edit("Автоматический фарминг запущен.")
    
        while True:
            current_time = time.strftime("%H:%M", time.gmtime(time.time() + 3 * 3600))  # UTC+3 для времени в Москве
    
            if current_time[-2:] == "00":
                current_hour = int(current_time[:2])
                if current_hour % 4 == 0 or current_hour == 0:
                    await client.send_message('@TChat_TChat_bot', "Фарм")
    
                    # Ждем час, прежде чем снова проверить время
                    await asyncio.sleep(3600)
    
        client = message.client
        self.tasks = [asyncio.create_task(self.b_run(client))]

    @loader.unrestricted
    @loader.ratelimit
    async def stopcmd(self, message):
        """Остановить автоматический фарминг в боте"""
        if not self.tasks:
            return await message.edit("Автоматический фарминг не запущен.")
        for task in self.tasks:
            task.cancel()
        self.tasks = []
        await message.edit("Автоматический фарминг остановлен.")
