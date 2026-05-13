import logging
import asyncio
from datetime import datetime, timedelta
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Bot token - set this in Render environment variables
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Store user data (in production, use database - for simplicity, using dict)
user_data = {}
user_reminders = {}

# Messages
WELCOME_MSG = """🚀 *Welcome to BitAI by Affinity AI*

Most crypto traders don't lose because they lack knowledge.
They lose because manual trading is emotional, bot settings are messy, and execution comes too late.

It's time to upgrade to BitAI - built to analyze real-time market data and execute your trades automatically, 24/7.

📹 *Video:* https://drive.google.com/file/d/1STOhv9qCUe5RxnwvSF9koJoLswOLIpD_/view?usp=sharing"""

MSG_1 = """📌 *Step 1/6: Prepare Your Binance Account*

To start using BitAI, you need a Binance account with KYC verification completed.

✅ *Already have a verified Binance account?*
You may skip this video and continue to BitAI License Activation.

📹 *Video:* https://drive.google.com/file/d/1TGACWYMSRR2x8NLkQgA3-_JgH-fUJUBg/view?usp=sharing"""

MSG_2 = """📌 *Step 2/6: BitAI License Activation*

To unlock BitAI's full auto AI trading, activate your BitAI License inside your BitAI app.

Once activated, you can proceed to activate & enable your Binance Futures.

📹 *Video:* https://drive.google.com/file/d/1VLidHqhUWQv6K_6Q0s3GYHVKPBgkeVxt/view?usp=sharing"""

MSG_3 = """📌 *Step 3/6: Activate & Enable Binance Futures*

Before BitAI can execute, you need to activate Binance Futures inside your Binance account.

Once Futures is enabled, you can continue to the next step and create your Binance API connection.

📹 *Video:* https://drive.google.com/file/d/1pSg-u3q4YvoZHB3DETFyBQFjRGczoCJj/view?usp=sharing"""

MSG_4 = """📌 *Step 4/6: Set Up Your API Keys*

Next, create your Binance API Keys and connect them to your BitAI account.

This allows BitAI to analyze real-time market data and execute based on your selected risk profile.

⚠️ *Make sure your API Keys are kept private and only connected inside the official BitAI platform.*

📹 *Video:* https://drive.google.com/file/d/1nUcCkcp_jv6FN6hwHxIADmxktlG6-M6k/view?usp=sharing"""

MSG_5 = """📌 *Step 5/6: Transfer USDT to Binance Futures*

Before BitAI can execute, make sure your USDT is transferred into your own Binance Futures Wallet.

This will be the capital used for BitAI's AI-driven execution based on your selected risk profile.

Once completed, continue to Select Risk Profile.

📹 *Video:* https://drive.google.com/file/d/1bRXrOM-I0UuoBWetbX-EcspvAniU6x4D/view?usp=sharing"""

MSG_6 = """📌 *Step 6/6: Select Your Risk Profile*

Choose your preferred BitAI Risk Profile based on your capital, goals, and risk appetite.

BitAI will execute according to the risk level you select.

Once done, BitAI will start to analyze real time market data and execute your trades automatically! 🎉

📹 *Video:* https://drive.google.com/file/d/1-WystTVv0Wwawhak6xBZlU0yXyTChZmP/view?usp=sharing"""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_data[user_id] = {"step": 0, "tasks": {}}
    await show_welcome(update, context)

async def show_welcome(update, context):
    keyboard = [
        [InlineKeyboardButton("📝 Register my FREE BitAI account", url="https://app.bitai.com.sg/h5/#/pages/sign/sign?invite=888")],
        [InlineKeyboardButton("📱 Download BitAI (iOS & Android)", url="https://fir.bitai.app/app.html")],
        [InlineKeyboardButton("📹 Watch BitAI Setup Video", callback_data="next_step_binance")],
        [InlineKeyboardButton("🆘 Contact Support", url="http://wa.me/6589691668")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.callback_query:
        await update.callback_query.edit_message_text(WELCOME_MSG, reply_markup=reply_markup, parse_mode='Markdown')
    else:
        await update.message.reply_text(WELCOME_MSG, reply_markup=reply_markup, parse_mode='Markdown')

async def show_step1(update, context):
    user_id = update.effective_user.id
    if user_data.get(user_id, {}).get("tasks", {}).get("step1") == "done":
        await show_step2(update, context)
        return
    
    keyboard = [
        [InlineKeyboardButton("🔗 Create a FREE Binance account", url="https://accounts.binance.com/en/register?ref=1154159582")],
        [InlineKeyboardButton("📱 Download Binance", url="https://www.binance.com/en/download")],
        [InlineKeyboardButton("✅ I have created my Binance account", callback_data="confirm_step1")],
        [InlineKeyboardButton("⏩ Skip to License Activation", callback_data="skip_step1")],
        [InlineKeyboardButton("🆘 Contact Support", url="http://wa.me/6589691668")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.callback_query:
        await update.callback_query.edit_message_text(MSG_1, reply_markup=reply_markup, parse_mode='Markdown')
    else:
        await update.message.reply_text(MSG_1, reply_markup=reply_markup, parse_mode='Markdown')
    
    # Schedule 6-hour reminder
    schedule_reminder(user_id, "step1", context)

async def show_step2(update, context):
    user_id = update.effective_user.id
    if user_data.get(user_id, {}).get("tasks", {}).get("step2") == "done":
        await show_step3(update, context)
        return
    
    keyboard = [
        [InlineKeyboardButton("⏩ Skip to Activate Futures", callback_data="skip_step2")],
        [InlineKeyboardButton("📝 Register FREE BitAI", url="https://app.bitai.com.sg/h5/#/pages/sign/sign?invite=888")],
        [InlineKeyboardButton("📱 Download BitAI", url="https://fir.bitai.app/app.html")],
        [InlineKeyboardButton("✅ I have activated my license", callback_data="confirm_step2")],
        [InlineKeyboardButton("🆘 Contact Support", url="http://wa.me/6589691668")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.callback_query:
        await update.callback_query.edit_message_text(MSG_2, reply_markup=reply_markup, parse_mode='Markdown')
    else:
        await update.message.reply_text(MSG_2, reply_markup=reply_markup, parse_mode='Markdown')
    
    schedule_reminder(user_id, "step2", context)

async def show_step3(update, context):
    user_id = update.effective_user.id
    if user_data.get(user_id, {}).get("tasks", {}).get("step3") == "done":
        await show_step4(update, context)
        return
    
    keyboard = [
        [InlineKeyboardButton("⏩ Skip to Setting API Keys", callback_data="skip_step3")],
        [InlineKeyboardButton("◀️ Back to License Activation", callback_data="back_step2")],
        [InlineKeyboardButton("✅ I have enabled Futures", callback_data="confirm_step3")],
        [InlineKeyboardButton("🆘 Contact Support", url="http://wa.me/6589691668")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.callback_query:
        await update.callback_query.edit_message_text(MSG_3, reply_markup=reply_markup, parse_mode='Markdown')
    else:
        await update.message.reply_text(MSG_3, reply_markup=reply_markup, parse_mode='Markdown')
    
    schedule_reminder(user_id, "step3", context)

async def show_step4(update, context):
    user_id = update.effective_user.id
    if user_data.get(user_id, {}).get("tasks", {}).get("step4") == "done":
        await show_step5(update, context)
        return
    
    keyboard = [
        [InlineKeyboardButton("⏩ Skip to Transferring USDT", callback_data="skip_step4")],
        [InlineKeyboardButton("◀️ Back to Enable Futures", callback_data="back_step3")],
        [InlineKeyboardButton("✅ I have connected API Keys", callback_data="confirm_step4")],
        [InlineKeyboardButton("🆘 Contact Support", url="http://wa.me/6589691668")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.callback_query:
        await update.callback_query.edit_message_text(MSG_4, reply_markup=reply_markup, parse_mode='Markdown')
    else:
        await update.message.reply_text(MSG_4, reply_markup=reply_markup, parse_mode='Markdown')
    
    schedule_reminder(user_id, "step4", context)

async def show_step5(update, context):
    user_id = update.effective_user.id
    if user_data.get(user_id, {}).get("tasks", {}).get("step5") == "done":
        await show_step6(update, context)
        return
    
    keyboard = [
        [InlineKeyboardButton("⏩ Skip to Select Risk Profile", callback_data="skip_step5")],
        [InlineKeyboardButton("◀️ Back to API Setup", callback_data="back_step4")],
        [InlineKeyboardButton("✅ I have transferred USDT", callback_data="confirm_step5")],
        [InlineKeyboardButton("🆘 Contact Support", url="http://wa.me/6589691668")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.callback_query:
        await update.callback_query.edit_message_text(MSG_5, reply_markup=reply_markup, parse_mode='Markdown')
    else:
        await update.message.reply_text(MSG_5, reply_markup=reply_markup, parse_mode='Markdown')
    
    schedule_reminder(user_id, "step5", context)

async def show_step6(update, context):
    keyboard = [
        [InlineKeyboardButton("◀️ Back to Transfer USDT", callback_data="back_step5")],
        [InlineKeyboardButton("❓ Frequently Answered Questions", url="https://bitai.app/faq")],
        [InlineKeyboardButton("📧 Email support: info@bitai.app", url="mailto:info@bitai.app")],
        [InlineKeyboardButton("🆘 Contact Support", url="http://wa.me/6589691668")],
        [InlineKeyboardButton("🚪 Exit Conversation", callback_data="exit")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    complete_msg = """🎉 *Congratulations! Setup Complete!* 🎉

BitAI will now:
- 📊 Analyze real-time market data
- 🤖 Execute trades automatically
- 💎 Run 24/7

*Select your Risk Profile in the BitAI App to start!*

Need help? Contact support anytime."""
    
    if update.callback_query:
        await update.callback_query.edit_message_text(complete_msg, reply_markup=reply_markup, parse_mode='Markdown')
    else:
        await update.message.reply_text(complete_msg, reply_markup=reply_markup, parse_mode='Markdown')

async def confirm_step(update: Update, context: ContextTypes.DEFAULT_TYPE, step: int):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    
    if user_id not in user_data:
        user_data[user_id] = {"step": 0, "tasks": {}}
    
    user_data[user_id]["tasks"][f"step{step}"] = "done"
    
    # Clear reminder
    if user_id in user_reminders and f"step{step}" in user_reminders[user_id]:
        del user_reminders[user_id][f"step{step}"]
    
    # Go to next step
    if step == 1:
        await show_step2(update, context)
    elif step == 2:
        await show_step3(update, context)
    elif step == 3:
        await show_step4(update, context)
    elif step == 4:
        await show_step5(update, context)
    elif step == 5:
        await show_step6(update, context)

async def skip_step(update: Update, context: ContextTypes.DEFAULT_TYPE, step: int):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    
    if user_id not in user_data:
        user_data[user_id] = {"step": 0, "tasks": {}}
    
    user_data[user_id]["tasks"][f"step{step}"] = "skipped"
    
    # Go to next step
    if step == 1:
        await show_step2(update, context)
    elif step == 2:
        await show_step3(update, context)
    elif step == 3:
        await show_step4(update, context)
    elif step == 4:
        await show_step5(update, context)
    elif step == 5:
        await show_step6(update, context)

async def back_step(update: Update, context: ContextTypes.DEFAULT_TYPE, step: int):
    query = update.callback_query
    await query.answer()
    
    if step == 2:
        await show_step1(update, context)
    elif step == 3:
        await show_step2(update, context)
    elif step == 4:
        await show_step3(update, context)
    elif step == 5:
        await show_step4(update, context)

async def exit_conversation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        "Thank you for using BitAI! 🤖\n\n"
        "Send /start anytime to continue setup.\n\n"
        "Happy trading! 🚀"
    )

def schedule_reminder(user_id: int, step: str, context: ContextTypes.DEFAULT_TYPE):
    """Schedule 6-hour reminder for incomplete task"""
    if user_id not in user_reminders:
        user_reminders[user_id] = {}
    
    if step not in user_reminders[user_id]:
        user_reminders[user_id][step] = True
        # Schedule reminder after 6 hours
        context.job_queue.run_once(
            send_reminder, 
            when=timedelta(seconds=6*3600),
            data={"user_id": user_id, "step": step}
        )

async def send_reminder(context: ContextTypes.DEFAULT_TYPE):
    """Send reminder to user"""
    job_data = context.job.data
    user_id = job_data["user_id"]
    step = job_data["step"]
    
    # Check if task is still incomplete
    if user_id in user_data and user_data[user_id].get("tasks", {}).get(step) not in ["done", "skipped"]:
        reminder_msgs = {
            "step1": "⏰ *Reminder:* Have you created your Binance account? Complete Step 1 to continue with BitAI setup.",
            "step2": "⏰ *Reminder:* Have you activated your BitAI license? Complete Step 2 to unlock AI trading.",
            "step3": "⏰ *Reminder:* Have you enabled Binance Futures? Complete Step 3 to proceed.",
            "step4": "⏰ *Reminder:* Have you connected your API keys? Complete Step 4 for BitAI to start trading.",
            "step5": "⏰ *Reminder:* Have you transferred USDT to Futures Wallet? Complete Step 5 to fund your trading."
        }
        
        keyboard = [[InlineKeyboardButton("📋 Continue Setup", callback_data="resume")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        try:
            await context.bot.send_message(
                chat_id=user_id,
                text=reminder_msgs.get(step, f"⏰ Reminder: Please complete {step} to continue BitAI setup."),
                reply_markup=reply_markup,
                parse_mode='Markdown'
            )
            # Schedule another reminder in 6 hours
            context.job_queue.run_once(
                send_reminder,
                when=timedelta(seconds=6*3600),
                data={"user_id": user_id, "step": step}
            )
        except Exception as e:
            logger.error(f"Failed to send reminder to {user_id}: {e}")

async def resume_setup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Resume setup from current step"""
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    
    if user_id not in user_data:
        await show_welcome(update, context)
        return
    
    tasks = user_data[user_id].get("tasks", {})
    
    if tasks.get("step1") not in ["done", "skipped"]:
        await show_step1(update, context)
    elif tasks.get("step2") not in ["done", "skipped"]:
        await show_step2(update, context)
    elif tasks.get("step3") not in ["done", "skipped"]:
        await show_step3(update, context)
    elif tasks.get("step4") not in ["done", "skipped"]:
        await show_step4(update, context)
    elif tasks.get("step5") not in ["done", "skipped"]:
        await show_step5(update, context)
    else:
        await show_step6(update, context)

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    
    # Command handlers
    app.add_handler(CommandHandler("start", start))
    
    # Callback handlers
    app.add_handler(CallbackQueryHandler(show_step1, pattern="^next_step_binance$"))
    app.add_handler(CallbackQueryHandler(lambda u,c: confirm_step(u,c,1), pattern="^confirm_step1$"))
    app.add_handler(CallbackQueryHandler(lambda u,c: skip_step(u,c,1), pattern="^skip_step1$"))
    app.add_handler(CallbackQueryHandler(lambda u,c: confirm_step(u,c,2), pattern="^confirm_step2$"))
    app.add_handler(CallbackQueryHandler(lambda u,c: skip_step(u,c,2), pattern="^skip_step2$"))
    app.add_handler(CallbackQueryHandler(lambda u,c: confirm_step(u,c,3), pattern="^confirm_step3$"))
    app.add_handler(CallbackQueryHandler(lambda u,c: skip_step(u,c,3), pattern="^skip_step3$"))
    app.add_handler(CallbackQueryHandler(lambda u,c: confirm_step(u,c,4), pattern="^confirm_step4$"))
    app.add_handler(CallbackQueryHandler(lambda u,c: skip_step(u,c,4), pattern="^skip_step4$"))
    app.add_handler(CallbackQueryHandler(lambda u,c: confirm_step(u,c,5), pattern="^confirm_step5$"))
    app.add_handler(CallbackQueryHandler(lambda u,c: skip_step(u,c,5), pattern="^skip_step5$"))
    app.add_handler(CallbackQueryHandler(lambda u,c: back_step(u,c,2), pattern="^back_step2$"))
    app.add_handler(CallbackQueryHandler(lambda u,c: back_step(u,c,3), pattern="^back_step3$"))
    app.add_handler(CallbackQueryHandler(lambda u,c: back_step(u,c,4), pattern="^back_step4$"))
    app.add_handler(CallbackQueryHandler(lambda u,c: back_step(u,c,5), pattern="^back_step5$"))
    app.add_handler(CallbackQueryHandler(resume_setup, pattern="^resume$"))
    app.add_handler(CallbackQueryHandler(exit_conversation, pattern="^exit$"))
    
    # Start bot
    print("Bot is running...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
