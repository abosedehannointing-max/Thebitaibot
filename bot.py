import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Bot token - set this in Render environment variables
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Store user progress
user_progress = {}

# Welcome Message
WELCOME_MSG = """🚀 *Welcome to BitAI by Affinity AI*

Most crypto traders don't lose because they lack knowledge.
They lose because manual trading is emotional, bot settings are messy, and execution comes too late.

It's time to upgrade to BitAI - built to analyze real-time market data and execute your trades automatically, 24/7.

📹 *Video:* https://drive.google.com/file/d/1STOhv9qCUe5RxnwvSF9koJoLswOLIpD_/view?usp=sharing"""

# Step Messages
STEP1_MSG = """📌 *Step 1/6: Prepare Your Binance Account*

To start using BitAI, you need a Binance account with KYC verification completed.

✅ *Already have a verified Binance account?*
You may skip this step and continue to BitAI License Activation.

📹 *Video:* https://drive.google.com/file/d/1TGACWYMSRR2x8NLkQgA3-_JgH-fUJUBg/view?usp=sharing"""

STEP2_MSG = """📌 *Step 2/6: BitAI License Activation*

To unlock BitAI's full auto AI trading, activate your BitAI License inside your BitAI app.

Once activated, you can proceed to activate & enable your Binance Futures.

📹 *Video:* https://drive.google.com/file/d/1VLidHqhUWQv6K_6Q0s3GYHVKPBgkeVxt/view?usp=sharing"""

STEP3_MSG = """📌 *Step 3/6: Activate & Enable Binance Futures*

Before BitAI can execute, you need to activate Binance Futures inside your Binance account.

Once Futures is enabled, you can continue to the next step and create your Binance API connection.

📹 *Video:* https://drive.google.com/file/d/1pSg-u3q4YvoZHB3DETFyBQFjRGczoCJj/view?usp=sharing"""

STEP4_MSG = """📌 *Step 4/6: Set Up Your API Keys*

Next, create your Binance API Keys and connect them to your BitAI account.

This allows BitAI to analyze real-time market data and execute based on your selected risk profile.

⚠️ *Make sure your API Keys are kept private and only connected inside the official BitAI platform.*

📹 *Video:* https://drive.google.com/file/d/1nUcCkcp_jv6FN6hwHxIADmxktlG6-M6k/view?usp=sharing"""

STEP5_MSG = """📌 *Step 5/6: Transfer USDT to Binance Futures*

Before BitAI can execute, make sure your USDT is transferred into your own Binance Futures Wallet.

This will be the capital used for BitAI's AI-driven execution based on your selected risk profile.

Once completed, continue to Select Risk Profile.

📹 *Video:* https://drive.google.com/file/d/1bRXrOM-I0UuoBWetbX-EcspvAniU6x4D/view?usp=sharing"""

STEP6_MSG = """📌 *Step 6/6: Select Your Risk Profile*

Choose your preferred BitAI Risk Profile based on your capital, goals, and risk appetite.

BitAI will execute according to the risk level you select.

Once done, BitAI will start to analyze real time market data and execute your trades automatically! 🎉

📹 *Video:* https://drive.google.com/file/d/1-WystTVv0Wwawhak6xBZlU0yXyTChZmP/view?usp=sharing"""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start command"""
    user_id = update.effective_user.id
    user_progress[user_id] = 0
    
    keyboard = [
        [InlineKeyboardButton("📝 Register FREE BitAI", url="https://app.bitai.com.sg/h5/#/pages/sign/sign?invite=888")],
        [InlineKeyboardButton("📱 Download BitAI", url="https://fir.bitai.app/app.html")],
        [InlineKeyboardButton("▶️ Start Setup", callback_data="next_step")],
        [InlineKeyboardButton("🆘 Contact Support", url="http://wa.me/6589691668")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(WELCOME_MSG, reply_markup=reply_markup, parse_mode='Markdown')

async def show_step1(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show Step 1"""
    keyboard = [
        [InlineKeyboardButton("🔗 Create Binance Account", url="https://accounts.binance.com/en/register?ref=1154159582")],
        [InlineKeyboardButton("📱 Download Binance App", url="https://www.binance.com/en/download")],
        [InlineKeyboardButton("✅ Done - I completed Step 1", callback_data="step1_done")],
        [InlineKeyboardButton("⏩ Skip to Step 2", callback_data="step1_skip")],
        [InlineKeyboardButton("🆘 Contact Support", url="http://wa.me/6589691668")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.callback_query:
        await update.callback_query.edit_message_text(STEP1_MSG, reply_markup=reply_markup, parse_mode='Markdown')
    else:
        await update.message.reply_text(STEP1_MSG, reply_markup=reply_markup, parse_mode='Markdown')

async def step1_done(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """User confirmed Step 1 is done"""
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    
    # Send confirmation message
    await query.edit_message_text(
        "✅ *Great! Step 1 completed!*\n\nMoving to Step 2...",
        parse_mode='Markdown'
    )
    
    # Wait 1 second then show next step
    import asyncio
    await asyncio.sleep(1)
    
    # Show Step 2
    await show_step2(update, context)

async def step1_skip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """User skipped Step 1"""
    query = update.callback_query
    await query.answer()
    
    await query.edit_message_text(
        "⏩ *Step 1 skipped*\n\nMoving to Step 2...",
        parse_mode='Markdown'
    )
    
    import asyncio
    await asyncio.sleep(1)
    
    await show_step2(update, context)

async def show_step2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show Step 2"""
    keyboard = [
        [InlineKeyboardButton("📝 Register BitAI", url="https://app.bitai.com.sg/h5/#/pages/sign/sign?invite=888")],
        [InlineKeyboardButton("📱 Download BitAI App", url="https://fir.bitai.app/app.html")],
        [InlineKeyboardButton("✅ Done - I completed Step 2", callback_data="step2_done")],
        [InlineKeyboardButton("⏩ Skip to Step 3", callback_data="step2_skip")],
        [InlineKeyboardButton("◀️ Back to Step 1", callback_data="step1_back")],
        [InlineKeyboardButton("🆘 Contact Support", url="http://wa.me/6589691668")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.callback_query:
        await update.callback_query.edit_message_text(STEP2_MSG, reply_markup=reply_markup, parse_mode='Markdown')
    else:
        await update.message.reply_text(STEP2_MSG, reply_markup=reply_markup, parse_mode='Markdown')

async def step2_done(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """User confirmed Step 2 is done"""
    query = update.callback_query
    await query.answer()
    
    await query.edit_message_text(
        "✅ *Great! Step 2 completed!*\n\nMoving to Step 3...",
        parse_mode='Markdown'
    )
    
    import asyncio
    await asyncio.sleep(1)
    
    await show_step3(update, context)

async def step2_skip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """User skipped Step 2"""
    query = update.callback_query
    await query.answer()
    
    await query.edit_message_text(
        "⏩ *Step 2 skipped*\n\nMoving to Step 3...",
        parse_mode='Markdown'
    )
    
    import asyncio
    await asyncio.sleep(1)
    
    await show_step3(update, context)

async def show_step3(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show Step 3"""
    keyboard = [
        [InlineKeyboardButton("✅ Done - I enabled Futures", callback_data="step3_done")],
        [InlineKeyboardButton("⏩ Skip to Step 4", callback_data="step3_skip")],
        [InlineKeyboardButton("◀️ Back to Step 2", callback_data="step2_back")],
        [InlineKeyboardButton("🆘 Contact Support", url="http://wa.me/6589691668")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.callback_query:
        await update.callback_query.edit_message_text(STEP3_MSG, reply_markup=reply_markup, parse_mode='Markdown')
    else:
        await update.message.reply_text(STEP3_MSG, reply_markup=reply_markup, parse_mode='Markdown')

async def step3_done(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """User confirmed Step 3 is done"""
    query = update.callback_query
    await query.answer()
    
    await query.edit_message_text(
        "✅ *Great! Step 3 completed!*\n\nMoving to Step 4...",
        parse_mode='Markdown'
    )
    
    import asyncio
    await asyncio.sleep(1)
    
    await show_step4(update, context)

async def step3_skip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """User skipped Step 3"""
    query = update.callback_query
    await query.answer()
    
    await query.edit_message_text(
        "⏩ *Step 3 skipped*\n\nMoving to Step 4...",
        parse_mode='Markdown'
    )
    
    import asyncio
    await asyncio.sleep(1)
    
    await show_step4(update, context)

async def show_step4(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show Step 4"""
    keyboard = [
        [InlineKeyboardButton("✅ Done - I set up API Keys", callback_data="step4_done")],
        [InlineKeyboardButton("⏩ Skip to Step 5", callback_data="step4_skip")],
        [InlineKeyboardButton("◀️ Back to Step 3", callback_data="step3_back")],
        [InlineKeyboardButton("🆘 Contact Support", url="http://wa.me/6589691668")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.callback_query:
        await update.callback_query.edit_message_text(STEP4_MSG, reply_markup=reply_markup, parse_mode='Markdown')
    else:
        await update.message.reply_text(STEP4_MSG, reply_markup=reply_markup, parse_mode='Markdown')

async def step4_done(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """User confirmed Step 4 is done"""
    query = update.callback_query
    await query.answer()
    
    await query.edit_message_text(
        "✅ *Great! Step 4 completed!*\n\nMoving to Step 5...",
        parse_mode='Markdown'
    )
    
    import asyncio
    await asyncio.sleep(1)
    
    await show_step5(update, context)

async def step4_skip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """User skipped Step 4"""
    query = update.callback_query
    await query.answer()
    
    await query.edit_message_text(
        "⏩ *Step 4 skipped*\n\nMoving to Step 5...",
        parse_mode='Markdown'
    )
    
    import asyncio
    await asyncio.sleep(1)
    
    await show_step5(update, context)

async def show_step5(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show Step 5"""
    keyboard = [
        [InlineKeyboardButton("✅ Done - I transferred USDT", callback_data="step5_done")],
        [InlineKeyboardButton("⏩ Skip to Step 6", callback_data="step5_skip")],
        [InlineKeyboardButton("◀️ Back to Step 4", callback_data="step4_back")],
        [InlineKeyboardButton("🆘 Contact Support", url="http://wa.me/6589691668")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.callback_query:
        await update.callback_query.edit_message_text(STEP5_MSG, reply_markup=reply_markup, parse_mode='Markdown')
    else:
        await update.message.reply_text(STEP5_MSG, reply_markup=reply_markup, parse_mode='Markdown')

async def step5_done(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """User confirmed Step 5 is done"""
    query = update.callback_query
    await query.answer()
    
    await query.edit_message_text(
        "✅ *Great! Step 5 completed!*\n\nMoving to final Step 6...",
        parse_mode='Markdown'
    )
    
    import asyncio
    await asyncio.sleep(1)
    
    await show_step6(update, context)

async def step5_skip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """User skipped Step 5"""
    query = update.callback_query
    await query.answer()
    
    await query.edit_message_text(
        "⏩ *Step 5 skipped*\n\nMoving to final Step 6...",
        parse_mode='Markdown'
    )
    
    import asyncio
    await asyncio.sleep(1)
    
    await show_step6(update, context)

async def show_step6(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show Step 6 - Final"""
    keyboard = [
        [InlineKeyboardButton("✅ Done - Setup Complete!", callback_data="step6_done")],
        [InlineKeyboardButton("◀️ Back to Step 5", callback_data="step5_back")],
        [InlineKeyboardButton("❓ FAQ", url="https://bitai.app/faq")],
        [InlineKeyboardButton("📧 Email Support", url="mailto:info@bitai.app")],
        [InlineKeyboardButton("🆘 Contact Support", url="http://wa.me/6589691668")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.callback_query:
        await update.callback_query.edit_message_text(STEP6_MSG, reply_markup=reply_markup, parse_mode='Markdown')
    else:
        await update.message.reply_text(STEP6_MSG, reply_markup=reply_markup, parse_mode='Markdown')

async def step6_done(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """User completed all steps"""
    query = update.callback_query
    await query.answer()
    
    completion_msg = """🎉 *CONGRATULATIONS! Setup Complete!* 🎉

You've successfully completed all steps!

✨ *BitAI is now ready to:*
• 📊 Analyze real-time market data
• 🤖 Execute trades automatically
• 💎 Run 24/7

*Select your Risk Profile in the BitAI App to start trading!*

Need help? Contact our support team anytime.

Thank you for choosing BitAI! 🚀"""

    keyboard = [
        [InlineKeyboardButton("🆘 Contact Support", url="http://wa.me/6589691668")],
        [InlineKeyboardButton("🏠 Restart Setup", callback_data="restart")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(completion_msg, reply_markup=reply_markup, parse_mode='Markdown')

async def restart_setup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Restart the entire setup"""
    query = update.callback_query
    await query.answer()
    
    await start(update, context)

# Back navigation handlers
async def back_to_step1(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await show_step1(update, context)

async def back_to_step2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await show_step2(update, context)

async def back_to_step3(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await show_step3(update, context)

async def back_to_step4(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await show_step4(update, context)

async def back_to_step5(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await show_step5(update, context)

def main():
    """Start the bot"""
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Command handlers
    application.add_handler(CommandHandler("start", start))
    
    # Callback handlers
    application.add_handler(CallbackQueryHandler(show_step1, pattern="^next_step$"))
    
    # Step 1 handlers
    application.add_handler(CallbackQueryHandler(step1_done, pattern="^step1_done$"))
    application.add_handler(CallbackQueryHandler(step1_skip, pattern="^step1_skip$"))
    application.add_handler(CallbackQueryHandler(back_to_step1, pattern="^step1_back$"))
    
    # Step 2 handlers
    application.add_handler(CallbackQueryHandler(step2_done, pattern="^step2_done$"))
    application.add_handler(CallbackQueryHandler(step2_skip, pattern="^step2_skip$"))
    application.add_handler(CallbackQueryHandler(back_to_step2, pattern="^step2_back$"))
    
    # Step 3 handlers
    application.add_handler(CallbackQueryHandler(step3_done, pattern="^step3_done$"))
    application.add_handler(CallbackQueryHandler(step3_skip, pattern="^step3_skip$"))
    application.add_handler(CallbackQueryHandler(back_to_step3, pattern="^step3_back$"))
    
    # Step 4 handlers
    application.add_handler(CallbackQueryHandler(step4_done, pattern="^step4_done$"))
    application.add_handler(CallbackQueryHandler(step4_skip, pattern="^step4_skip$"))
    application.add_handler(CallbackQueryHandler(back_to_step4, pattern="^step4_back$"))
    
    # Step 5 handlers
    application.add_handler(CallbackQueryHandler(step5_done, pattern="^step5_done$"))
    application.add_handler(CallbackQueryHandler(step5_skip, pattern="^step5_skip$"))
    application.add_handler(CallbackQueryHandler(back_to_step5, pattern="^step5_back$"))
    
    # Step 6 handlers
    application.add_handler(CallbackQueryHandler(step6_done, pattern="^step6_done$"))
    application.add_handler(CallbackQueryHandler(restart_setup, pattern="^restart$"))
    
    # Start bot
    print("Bot is running...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
