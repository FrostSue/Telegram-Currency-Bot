from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler
from pyrogram.types import BotCommand
import configparser

from .handlers import (
    start_command,
    exchange_rate_command,
    help_command,
    calculate_command,
    reverse_calculate_command,
)

class CurrencyBot:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        
        self.api_id = config['Telegram']['API_ID']
        self.api_hash = config['Telegram']['API_HASH']
        self.bot_token = config['Telegram']['BOT_TOKEN']
        
        self.app = Client(
            "currency_bot",
            api_id=self.api_id,
            api_hash=self.api_hash,
            bot_token=self.bot_token
        )
        
        self._setup_handlers()

    def _setup_handlers(self):
        """Bot komutlarını ayarla"""
        self.app.add_handler(MessageHandler(start_command, filters.command("start")))
        self.app.add_handler(MessageHandler(exchange_rate_command, filters.command("kur")))
        self.app.add_handler(MessageHandler(calculate_command, filters.command("hesapla")))
        self.app.add_handler(MessageHandler(reverse_calculate_command, filters.command("tersine")))
        self.app.add_handler(MessageHandler(help_command, filters.command("yardim")))

    async def set_bot_commands(self):
        """Bot komutlarını menüye ekle"""
        commands = [
            BotCommand("start", "Botu başlat"),
            BotCommand("kur", "Güncel döviz kurunu gösterir"),
            BotCommand("hesapla", "Döviz miktarını TL'ye çevirir"),
            BotCommand("tersine", "TL'yi seçilen dövize çevirir"),
            BotCommand("yardim", "Yardım menüsünü gösterir")
        ]
        await self.app.set_bot_commands(commands)
        print("Bot komutları menüye eklendi...")

    def run(self):
        """Botu çalıştır"""
        print("Bot başlatılıyor...")
        self.app.run()
        self.app.loop.run_until_complete(self.set_bot_commands())