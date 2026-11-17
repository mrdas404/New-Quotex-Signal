import os
import random
import logging
from datetime import datetime, timezone
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# ================== CONFIG ==================
TOKEN = "8556221504:AAEpavdgVzXbNQ5pNvJvlnRfnFdhbhADi1M"          
ADMIN_ID = None                        # optional: your Telegram user ID (for future admin features)

# Pairs you want the bot to support
PAIRS = [
    "EURUSD_otc", "GBPUSD_otc", "USDJPY_otc", "AUDUSD_otc",
    "EURGBP_otc", "USDCAD_otc", "EURJPY_otc", "GBPJPY_otc"
]

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ================== SIGNAL GENERATOR (100% free) ==================
def generate_free_signal(pair: str = None) -> str:
    """
    Completely free educational signal generator.
    Uses random + simple rules. Replace later with free public data if you want.
    """
    if pair is None:
        pair = random.choice(PAIRS)
    else:
        pair = pair.upper()

    direction = random.choice(["CALL 🟢", "PUT 🔴"])
    confidence = random.randint(58, 82)
    expiry = random.choice(["1 min", "5 min", "15 min"])
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    return (
        f"📊 **Free Quotex Signal**\n\n"
        f"Pair: `{pair}`\n"
        f"Direction: **{direction}**\n"
        f"Expiry: `{expiry}`\n"
        f"Confidence: `{confidence}%`\n"
        f"Time: `{now}`\n\n"
        f"⚠️ Educational only • High risk of loss • Always trade on demo first\n"
        f"This bot is 100% free"
    )

# ================== COMMANDS ==================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "🤖 **Free Quotex Signal Bot**\n\n"
        "Commands:\n"
        "/signal → Get a free signal\n"
        "/signal EURUSD_otc → Signal for specific pair\n"
        "/pairs → List available pairs\n"
        "/help → Show help\n\n"
        "This bot is completely free. No payments, no VIP."
    )
    await update.message.reply_text(text, parse_mode="Markdown")

async def signal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pair = None
    if context.args:
        pair = context.args[0]
    msg = generate_free_signal(pair)
    await update.message.reply_text(msg, parse_mode="Markdown")

async def pairs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "📋 Available pairs:\n\n" + "\n".join(f"• `{p}`" for p in PAIRS)
    await update.message.reply_text(text, parse_mode="Markdown")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Free educational bot.\n"
        "Just send /signal anytime.\n"
        "You can improve the signal logic later with free public data sources.",
        parse_mode="Markdown"
    )

# ================== MAIN ==================
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("signal", signal))
    app.add_handler(CommandHandler("pairs", pairs))
    app.add_handler(CommandHandler("help", help_command))

    print("✅ Free Quotex Signal Bot is running...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()