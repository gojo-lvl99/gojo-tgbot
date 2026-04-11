import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from generator import format_message

# ─── LOAD ENV ─────────────────────────────────────────────────────────────────
load_dotenv()

BOT_TOKEN   = os.getenv("BOT_TOKEN")
ALLOWED_ID  = int(os.getenv("ALLOWED_ID"))

# ─── LOGGING ──────────────────────────────────────────────────────────────────
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# ─── AUTH CHECK ───────────────────────────────────────────────────────────────
def is_allowed(update: Update) -> bool:
    return update.effective_user.id == ALLOWED_ID

# ─── HANDLERS ─────────────────────────────────────────────────────────────────

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_allowed(update):
        await update.message.reply_text("⛔ Unauthorized.")
        return

    msg = (
        "👁️ *GOJO BOT ONLINE*\n\n"
        "Commands:\n"
        "`/config <cloud_run_url>` — generate all proxy configs\n\n"
        "Example:\n"
        "`/config https://gojo-proxy-xxxx-uc.a.run.app`"
    )
    await update.message.reply_text(msg, parse_mode="Markdown")


async def config(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_allowed(update):
        await update.message.reply_text("⛔ Unauthorized.")
        return

    if not context.args:
        await update.message.reply_text(
            "❌ Walang URL.\n\nUsage: `/config <cloud_run_url>`",
            parse_mode="Markdown",
        )
        return

    url = context.args[0].strip()

    # basic validation
    if not url.startswith("http"):
        await update.message.reply_text("❌ Invalid URL. Dapat magsimula sa https://")
        return

    await update.message.reply_text("⏳ Generating configs...")

    try:
        result = format_message(url)
        await update.message.reply_text(result, parse_mode="Markdown")
    except Exception as e:
        logger.error(f"Error generating config: {e}")
        await update.message.reply_text(f"❌ Error: {e}")


async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_allowed(update):
        return
    await update.message.reply_text("❓ Unknown command. Try /start")


# ─── MAIN ─────────────────────────────────────────────────────────────────────

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("config", config))
    app.add_handler(MessageHandler(filters.COMMAND, unknown))

    logger.info("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
