import asyncio
# Python 3.14+ compatibility fix
try:
    asyncio.get_event_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import UserNotParticipant

# --- CONFIGURATION ---
API_ID = 33379492                          # Apni API ID dalein
API_HASH = "324ab8ffb7c4567a5855693b22e23278"            # Apna API Hash dalein
BOT_TOKEN = "8832723339:AAGnQCO-OUQGLz7aJwYn-j7_ocY116_2mQQ"          # Apna Bot Token dalein

DB_CHANNEL = -1004476031919                # Private Database Channel ID

FORCE_SUB_CHANNEL_1 = -1004307696517       # Pehle channel ki ID
FORCE_SUB_LINK_1 = "https://t.me/epicflixtoon"

FORCE_SUB_CHANNEL_2 = -1004412685050       # Dusre channel ki ID
FORCE_SUB_LINK_2 = "https://t.me/dailylootsshoppings"

bot = Client("FileStoreBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

async def check_user_joined(client, channel_id, user_id):
    try:
        await client.get_chat_member(channel_id, user_id)
        return True
    except UserNotParticipant:
        return False
    except Exception:
        return True

@bot.on_message(filters.command("start") & filters.private)
async def start_handler(client, message):
    user_id = message.from_user.id
    
    is_joined_1 = await check_user_joined(client, FORCE_SUB_CHANNEL_1, user_id)
    is_joined_2 = await check_user_joined(client, FORCE_SUB_CHANNEL_2, user_id)

    if not (is_joined_1 and is_joined_2):
        buttons = []
        if not is_joined_1:
            buttons.append([InlineKeyboardButton("📢 Join Channel 1", url=FORCE_SUB_LINK_1)])
        if not is_joined_2:
            buttons.append([InlineKeyboardButton("📢 Join Channel 2", url=FORCE_SUB_LINK_2)])
            
        start_param = message.text.split()[1] if len(message.text.split()) > 1 else ''
        buttons.append([InlineKeyboardButton("🔄 Try Again", url=f"https://t.me/{client.me.username}?start={start_param}")])

        await message.reply_text(
            "❌ **File download karne ke liye aapko niche diye gaye dono channels join karne honge!**",
            reply_markup=InlineKeyboardMarkup(buttons)
        )
        return

    text_args = message.text.split()
    if len(text_args) > 1:
        try:
            msg_id = int(text_args[1])
            await client.copy_message(
                chat_id=user_id,
                from_chat_id=DB_CHANNEL,
                message_id=msg_id
            )
            return
        except Exception:
            await message.reply_text("⚠️ File nahi mili ya link expire ho gaya hai.")
            return

    await message.reply_text("Welcome! Mujhe koi bhi file bhejo, main uska shareable link bana dunga.")

@bot.on_message((filters.document | filters.video | filters.audio | filters.photo) & filters.private)
async def file_store_handler(client, message):
    db_msg = await message.copy(chat_id=DB_CHANNEL)
    file_link = f"https://t.me/{client.me.username}?start={db_msg.id}"
    
    await message.reply_text(
        f"✅ **File Saved!**\n\n🔗 **Aapka File Link:**\n`{file_link}`",
        disable_web_page_preview=True
    )

print("Bot chal raha hai (Dual Channel Force Sub Active)...")
bot.run()