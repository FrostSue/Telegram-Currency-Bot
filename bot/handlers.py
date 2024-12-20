from pyrogram import Client, filters
from datetime import datetime
import aiohttp
import configparser
import os

config = configparser.ConfigParser()
config.read('config.ini')

CURRENCY_API_KEY = config['Currency']['API_KEY']
CURRENCY_API_URL = config['Currency']['CURRENCY_API_URL']

async def get_exchange_rate(currency: str) -> dict:
    headers = {
        "apikey": CURRENCY_API_KEY
    }
    
    async with aiohttp.ClientSession() as session:
        url = f"{CURRENCY_API_URL}?currencies={currency}&base_currency=TRY"
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                return data.get('data', {}).get(currency, {})
    return None

async def start_command(client, message):
    welcome_text = """
🌟 Döviz Kuru Botuna hoş geldiniz.

Mevcut komutlar:
/kur USD - Dolar kurunu gösterir
/kur EUR - Euro kurunu gösterir
/kur GBP - İngiliz Sterlini kurunu gösterir
/hesapla USD 100 - 100 Doları TL'ye çevirir
/tersine TRY 1000 USD - 1000 TL'yi Dolara çevirir

Örnek kullanım:
/kur USD
/hesapla EUR 50
/tersine TRY 1000 USD
"""
    await message.reply_text(welcome_text)

async def exchange_rate_command(client, message):
    try:
        command_parts = message.text.split()
        if len(command_parts) != 2:
            await message.reply_text("❌ Lütfen geçerli bir para birimi girin.\nÖrnek: /kur USD")
            return

        currency = command_parts[1].upper()
        if currency not in ["USD", "EUR", "GBP"]:
            await message.reply_text("❌ Desteklenmeyen para birimi. USD, EUR veya GBP kullanın.")
            return

        rate_data = await get_exchange_rate(currency)
        if rate_data:
            rate = 1 / rate_data.get('value', 0) 
            current_time = datetime.now().strftime("%d.%m.%Y %H:%M")
            response = f"""
💰 Döviz Kuru Bilgisi
🕒 {current_time}

1 {currency} = {rate:.4f} TRY
"""
            await message.reply_text(response)
        else:
            await message.reply_text("❌ Döviz kuru bilgisi alınamadı. Lütfen daha sonra tekrar deneyin.")

    except Exception as e:
        await message.reply_text("❌ Bir hata oluştu. Lütfen daha sonra tekrar deneyin.")
        print(f"Hata: {e}")

async def calculate_command(client, message):
    try:
        command_parts = message.text.split()
        if len(command_parts) != 3:
            await message.reply_text("❌ Lütfen geçerli bir format kullanın.\nÖrnek: /hesapla USD 100")
            return

        currency = command_parts[1].upper()
        try:
            amount = float(command_parts[2])
        except ValueError:
            await message.reply_text("❌ Lütfen geçerli bir miktar girin.")
            return

        if currency not in ["USD", "EUR", "GBP"]:
            await message.reply_text("❌ Desteklenmeyen para birimi. USD, EUR veya GBP kullanın.")
            return

        rate_data = await get_exchange_rate(currency)
        if rate_data:
            rate = 1 / rate_data.get('value', 0)
            converted_amount = amount * rate
            current_time = datetime.now().strftime("%d.%m.%Y %H:%M")
            response = f"""
💱 Döviz Çevirisi
🕒 {current_time}

{amount:.2f} {currency} = {converted_amount:.2f} TRY
Güncel Kur: 1 {currency} = {rate:.4f} TRY
"""
            await message.reply_text(response)
        else:
            await message.reply_text("❌ Döviz kuru bilgisi alınamadı. Lütfen daha sonra tekrar deneyin.")

    except Exception as e:
        await message.reply_text("❌ Bir hata oluştu. Lütfen daha sonra tekrar deneyin.")
        print(f"Hata: {e}")

async def reverse_calculate_command(client, message):
    try:
        command_parts = message.text.split()
        if len(command_parts) != 4 or command_parts[1] != "TRY":
            await message.reply_text("❌ Lütfen geçerli bir format kullanın.\nÖrnek: /tersine TRY 1000 USD")
            return

        try:
            amount = float(command_parts[2])
        except ValueError:
            await message.reply_text("❌ Lütfen geçerli bir miktar girin.")
            return

        target_currency = command_parts[3].upper()
        if target_currency not in ["USD", "EUR", "GBP"]:
            await message.reply_text("❌ Desteklenmeyen para birimi. USD, EUR veya GBP kullanın.")
            return

        rate_data = await get_exchange_rate(target_currency)
        if rate_data:
            rate = 1 / rate_data.get('value', 0)
            converted_amount = amount / rate
            current_time = datetime.now().strftime("%d.%m.%Y %H:%M")
            response = f"""
💱 Tersine Döviz Çevirisi
🕒 {current_time}

{amount:.2f} TRY = {converted_amount:.2f} {target_currency}
Güncel Kur: 1 {target_currency} = {rate:.4f} TRY
"""
            await message.reply_text(response)
        else:
            await message.reply_text("❌ Döviz kuru bilgisi alınamadı. Lütfen daha sonra tekrar deneyin.")

    except Exception as e:
        await message.reply_text("❌ Bir hata oluştu. Lütfen daha sonra tekrar deneyin.")
        print(f"Hata: {e}")

async def help_command(client, message):
    help_text = """
📚 Yardım Menüsü

Mevcut komutlar:
/start - Botu başlat
/kur [USD/EUR/GBP] - Seçilen döviz kurunun güncel değerini gösterir
/hesapla [USD/EUR/GBP] [miktar] - Girilen miktarı TL'ye çevirir
/tersine TRY [miktar] [USD/EUR/GBP] - Girilen TL miktarını seçilen dövize çevirir
/yardim - Bu yardım menüsünü gösterir

Örnek kullanım:
/kur USD - Dolar kurunu gösterir
/hesapla USD 100 - 100 Doları TL'ye çevirir
/tersine TRY 1000 USD - 1000 TL'yi Dolara çevirir
"""
    await message.reply_text(help_text)