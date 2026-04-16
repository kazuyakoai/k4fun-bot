import os
import random
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

users = {}

def get_user(uid):
    if uid not in users:
        users[uid] = {"coins": 100}
    return users[uid]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎮 K4FUN Bot is online!")

async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    u = get_user(update.effective_user.id)
    await update.message.reply_text(f"💰 Coins: {u['coins']}")

async def flip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    u = get_user(uid)

    if len(context.args) < 2:
        return await update.message.reply_text("Use /flip heads 10")

    choice = context.args[0]
    bet = int(context.args[1])

    if bet > u["coins"]:
        return await update.message.reply_text("❌ Not enough coins")

    result = random.choice(["heads", "tails"])

    if choice == result:
        u["coins"] += bet
        msg = f"🪙 {result} WIN +{bet}"
    else:
        u["coins"] -= bet
        msg = f"🪙 {result} LOSE -{bet}"

    await update.message.reply_text(msg)

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("balance", balance))
    app.add_handler(CommandHandler("flip", flip))

    print("Bot running...")
    app.run_polling()

if __name__ == "__main__":
    main()
