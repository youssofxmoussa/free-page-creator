"""
🤖 بوت معاذ محمد - الإصدار الكامل مع دعم متعدد اللغات
"""
import sqlite3, requests, re, time, random, string, os, uuid, hashlib, base64, json, csv, io, threading
from datetime import datetime
from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, LabeledPrice

# ==================== CONFIG ====================
BOT_TOKEN = "8768910192:AAGEZgyXKL2fNm-Nbl6As_cGBZBGQgpkIv0"
bot = TeleBot(BOT_TOKEN, skip_pending=True)
user_data = {}  # uid -> dict
ADMIN_ID = 8349951848
IMGBB_KEY = "d59fd9bc1d8802fb6237f495926d633e"
SOMIO_KEY = "am_a124cc3b5a124912a9f325f20b8bec4d"
SCRAPEOPS_KEY = "cc11e7d6-cc98-4bb3-b6c4-4596ee827532"
SCRAPERAPI_KEY = "8204988f0d3b5afe12f5439763b54270"
CAPTCHA_API_KEY_X = "uA1h2Smz4WzEZh7aOjQMg0HK3WBGuCrY"
MAIL_URL = "https://api.mail.tm"
NANO_BASE = "https://nanobanana.org"
SUPPORT_USERNAME = "@K_I_L_W_A"
DB_PATH = "bot.db"
SAVE_DIR = "media"
os.makedirs(SAVE_DIR, exist_ok=True)

PROXIES = [
    "209.50.187.134:3129","216.26.238.198:3129","193.56.28.1:3129",
    "65.111.12.199:3129","209.50.160.95:3129","104.207.37.228:3129",
    "104.207.50.155:3129","209.50.163.225:3129","104.207.61.4:3129",
    "65.111.5.186:3129","104.207.57.175:3129","104.207.56.249:3129",
    "104.207.53.211:3129","65.111.7.93:3129","154.213.161.38:3129",
    "65.111.13.78:3129","65.111.14.166:3129","65.111.25.85:3129",
    "45.3.35.114:3129","65.111.28.197:3129","45.3.36.166:3129",
    "216.26.231.74:3129","209.50.160.228:3129","216.26.235.143:3129",
    "65.111.2.31:3129","65.111.28.6:3129","65.111.30.21:3129",
    "216.26.236.116:3129","216.26.245.179:3129","104.207.60.149:3129",
    "209.50.183.111:3129","209.50.171.85:3129","104.207.35.29:3129",
    "154.213.160.136:3129","209.50.169.28:3129","104.207.33.168:3129",
    "216.26.249.38:3129","216.26.231.204:3129","104.207.45.109:3129",
    "104.207.48.104:3129","45.3.38.70:3129","216.26.229.116:3129",
    "104.207.46.149:3129","209.50.176.141:3129","216.26.243.69:3129",
    "45.3.41.251:3129","216.26.237.241:3129","104.207.54.20:3129",
    "65.111.26.228:3129","209.50.166.141:3129","216.26.255.48:3129",
    "104.207.62.128:3129","209.50.188.95:3129","104.207.52.98:3129",
    "154.213.160.126:3129","216.26.246.222:3129","216.26.226.63:3129",
    "65.111.1.165:3129","45.3.32.235:3129","209.50.177.226:3129",
    "104.167.25.201:3129","209.50.162.190:3129","216.26.243.199:3129",
    "104.207.51.173:3129","209.50.165.28:3129","65.111.1.130:3129",
    "45.3.55.119:3129","104.207.63.173:3129","209.50.179.7:3129",
    "216.26.225.198:3129","104.207.63.103:3129","45.3.62.243:3129",
    "104.207.51.92:3129","209.50.177.101:3129","104.207.53.145:3129",
    "65.111.28.104:3129","209.50.169.243:3129","104.207.52.7:3129",
    "216.26.236.239:3129","104.207.52.20:3129","209.50.170.14:3129",
    "65.111.28.8:3129","45.3.40.253:3129","45.3.48.72:3129",
    "216.26.247.10:3129","45.3.38.158:3129","45.3.43.47:3129",
    "104.207.34.221:3129","104.207.34.20:3129","65.111.2.5:3129",
    "209.50.176.40:3129","209.50.177.227:3129","209.50.171.140:3129",
    "45.3.40.40:3129","104.207.48.169:3129","65.111.29.168:3129",
    "209.50.181.162:3129","65.111.29.46:3129","65.111.7.171:3129",
    "65.111.24.114:3129",
]
executor = None  # removed(max_workers=30)
NANO_MODELS = {"nano_pro": "nano-banana-pro", "nano_standard": "image-editor"}


import random as _random
EMOJI_POOL = ["🌟","🎯","🚀","🎸","🦋","🌊","🔥","🎨","🍕","🎭",
              "🦁","🌈","💎","🎪","🌺","🐬","🎲","🌙","⚡","🎵",
              "🍦","🎠","🦄","🌸","🎩","🐲","🎻","🌴","🎡","🦊"]

def make_emoji_captcha():
    target = _random.choice(EMOJI_POOL)
    options = [target] + _random.sample([e for e in EMOJI_POOL if e != target], 5)
    _random.shuffle(options)
    return target, options

# ==================== TRANSLATIONS ====================
AR = {
    "welcome": "⊏ ــــــ بـوت مـعـاذ مـحـمـد لـلـذکـاء الاصـطـنـاعـی ــــــ ⊐\n\nمَـرْحَـبـاً يـا صَـدِيقِـي! 🌟 هُـنـا مَـصْـنَـعُ الإِبْـدَاع..\nجَـاهِـز تـحَـوّل أَفْـكَـارَك لـحَـقِـيـقَـة؟ 🚀\n\n✦ صَـوِّر خَـيَـالَـك بِـأَدَوَاتِ التَّـوْلِـيـد 🖼️\n✦ اصْـنَـع فِـيـدْيـوَهَـاتِـك بِـضَـغْـطَـة 🎥\n✦ أَلِّـف مُـوسِـيـقَـاك الخَـاصَّـة 🎧\n✦ اسْـأَل الـذَّكَـاءَ الاصْـطِـنَـاعِـيَّ وَتَـسَـلَّ مَـعَـنَـا 💡\n\nاخْـتَـر مِـنَ الأَزْرَارِ بِـالأَسْـفَـلِ وَانْـطَـلِـق 👇\n⊏ ـــــــــــــــــــــــــــــــ ⊐",
    "btn_edit": "🎨 تعديل صورة", "btn_image": "🖼️ إنشاء صورة",
    "btn_music": "🎵 إنشاء أغنية", "btn_video": "🎬 توليد فيديو",
    "btn_chat": "🤖 CHAT AI",
    "btn_points": "🎁 تجميع نقاط", "btn_account": "👤 حسابي",
    "btn_shop": "💳 شراء نقاط", "btn_support": "🆘 الدعم",
    "btn_dev": "💻 قسم المبرمجين | شراء ملفات",
    "back": "🔙 رجوع",
    "choose_lang": "🌍 اختر لغتك | Choose your language",
    "sub_required": "⚠️ يجب الاشتراك في القناة أولاً:",
    "sub_check": "✅ اشتركت",
    "sub_not_yet": "❌ لم تشترك بعد!",
    "banned": "🚫 أنت محظور.",
    "frozen": "❄️ حسابك مجمد، تواصل مع الدعم.",
    "maintenance": "⚙️ البوت تحت الصيانة، عد لاحقاً",
    "no_pts": "❌ نقاطك غير كافية! تحتاج {n} نقطة",
    "invite_collect": "🔗 ادعو صديق",
    "buy_pts_btn": "💳 اشتري نقاط",
    "waiting": "⏳ جارٍ التنفيذ، انتظر...",
    "fail_refund": "❌ فشل العملية، أُعيدت النقاط",
    # صور
    "img_choose": "🖼️ اختر نوع التوليد:",
    "img_nano_std": "🍌 نانو بانانا عادي ({n} نقطة)",
    "img_nano_pro": "⭐ نانو بانانا برو ({n} نقطة)",
    "img_prompt": "✅ اكتب البرومبت:",
    # تعديل
    "edit_choose": "🎨 اختر نوع التعديل:",
    "edit_std": "✏️ تعديل عادي ({n} نقطة)",
    "edit_pro": "⭐ تعديل برو ({n} نقطة)",
    "edit_send_photo": "✏️ أرسل الصورة:",
    "edit_pro_send": "⭐ أرسل الصورة أو الصور:\n(أرسل نصاً مباشرةً للتعديل)",
    "photo_ok": "✅ الصورة وصلت! أرسل البرومبت:",
    "photo_added": "✅ صورة {n} أُضيفت!\nأرسل صورة أخرى أو اكتب البرومبت:",
    # فيديو
    "vid_choose": "🎬 اختر نوع الفيديو:",
    "vid_text": "📝 نص ← فيديو",
    "vid_img": "🖼️ صورة ← فيديو",
    "vid_send_desc": "📝 أرسل وصف الفيديو:",
    "vid_send_photo": "🖼️ أرسل الصورة:",
    "vid_photo_ok": "✅ الصورة وصلت! أرسل وصف الفيديو:",
    "vid_caption": "✅ الفيديو جاهز!\n📝 {p}",
    # موسيقى
    "music_choose": "🎵 اختر:",
    "music_idea_btn": "💡 من فكرة",
    "music_lyrics_btn": "📝 من كلمات",
    "music_idea_send": "💡 أرسل فكرة الأغنية:",
    "music_lyrics_send": "📝 أرسل كلمات الأغنية:",
    # chat ai
    "chat_title": "💬 *المساعد الشخصي*\n\nاكتب أي سؤال وسأرد عليك فوراً 🌟\n\n(اضغط /start للخروج من المحادثة)",
    # دعم
    "support_title": "🆘 *الدعم الفني*\n\n💬 اكتب سؤالك عن البوت وسنساعدك فوراً!\n\n(اضغط /start للخروج)",
    "contact_btn": "💬 تواصل مباشر",
    # حسابي
    "account_title": "👤 *حسابي*",
    "account_body": "🆔 ID: `{uid}`\n⭐ النقاط: {pts}\n📊 الإجمالي: {tot}\n{emoji} المستوى: {lvl}{next}\n🎁 مميزات: {perks}\n\n🔗 دعوات: {inv}\n🖼️ {ti} صورة | 🎬 {tv} فيديو\n🎵 {tm} أغنية | ✏️ {te} تعديل",
    "next_level": "\n📈 للمستوى التالي: {n} نقطة",
    "max_level": "\n🏆 أعلى مستوى!",
    "send_ref": "📤 إرسال رابط الدعوة",
    "ref_msg": "🔗 رابط دعوتك:\n\n{link}\n\n📲 شارك الرابط واحصل على {pts} نقاط لكل دعوة!",
    # تجميع نقاط
    "collect_title": "🎁 *تجميع نقاط*\n\n⭐ نقاطك الحالية: {pts}",
    "daily_btn": "🎁 الهدية اليومية (+{pts} نقاط)",
    "daily_wait": "🎁 الهدية بعد {h}:{m:02d}",
    "invite_btn": "🔗 ادعُ صديق (+{pts} نقاط/دعوة)",
    "games_btn": "🎮 الألعاب (+4 نقاط)",
    "code_btn": "🎟️ كود نقاط",
    "transfer_btn": "💸 تحويل نقاط",
    "transfer_enter_id": "💸 *تحويل نقاط*\n\nأرسل ID المستخدم الذي تريد التحويل إليه:",
    "transfer_enter_pts": "💸 تحويل إلى `{uid2}`\n\nكم نقطة تريد تحويلها؟ (رصيدك: {bal})",
    "transfer_ok": "✅ تم تحويل {pts} نقاط إلى `{uid2}`\n⭐ رصيدك الجديد: {bal}",
    "transfer_recv": "🎁 استلمت {pts} نقاط من @{sender}!\n⭐ رصيدك: {bal}",
    "transfer_no_pts": "❌ رصيدك غير كافٍ!",
    "transfer_no_user": "❌ المستخدم غير موجود!",
    "transfer_self": "❌ لا يمكنك التحويل لنفسك!",
    "transfer_min": "❌ الحد الأدنى للتحويل نقطة واحدة!",
    "daily_claimed": "❌ أخذت الهدية اليوم!",
    "daily_ok": "🎉 +{pts} نقاط ✅\n⭐ الرصيد: {bal}",
    "code_enter": "🎟️ أرسل الكود:",
    "code_ok": "✅ +{pts} نقاط!\n⭐ الرصيد: {bal}",
    "code_wrong": "❌ كود خاطئ!",
    "code_used_up": "❌ الكود استُنفد!",
    "code_expired": "❌ الكود منتهي الصلاحية!",
    "code_already": "❌ استخدمت هذا الكود من قبل!",
    "stars_payment": "⭐ شراء بالنجوم",
    "stars_buy_btn": "💫 شراء الآن بالنجوم",
    "stars_success": "✅ شكراً! تم استلام نجومك. جاري إضافة النقاط...",
    # الألعاب
    "games_title": "🎮 اختر لعبة:",
    "game_xo": "🎮 XO",
    "game_quiz": "🧠 سؤال وجواب",
    "game_word": "🔤 أكمل الكلمة",
    "no_tries": "❌ انتهت محاولاتك اليوم!\nعُد بعد {h}:{m:02d}",
    "game_xo_start": "🎮 *XO* - المحاولة {n}/3\n🏆 الفوز = {pts} نقاط\nأنت ❌ | AI ⭕",
    "game_quiz_q": "🧠 المحاولة {n}/3 | 🏆 {pts} نقاط\n\n❓ {q}",
    "game_word_q": "🔤 المحاولة {n}/3 | 🏆 {pts} نقاط\n\n{disp}\n💡 {hint}\n\nاكتب الكلمة:",
    "game_won": "🎉 فزتَ! +{pts} نقاط ✅",
    "game_draw": "🤝 تعادل!",
    "game_ai_won": "😔 الذكاء الاصطناعي فاز! حاول مجدداً 💪",
    "game_wrong_q": "❌ خطأ! الإجابة الصحيحة: {ans}",
    "game_wrong_w": "❌ خطأ! الكلمة كانت: {word}",
    "try_again": "🎮 مجدداً",
    "xo_turn": "🎮 دورك:",
    "surrender": "🏳️ استسلام",
    "gen_question": "⏳ جارٍ توليد السؤال...",
    "fail_try": "❌ فشل، جرب مجدداً",
    # متجر
    "shop_title": "💳 *شراء نقاط بنجوم تيليغرام*",
    "shop_pkg": "{e} {n} | {p} نقطة ← {s} ⭐",
    "shop_detail": "{e} *{n}*\n\n{p} نقطة ← {s} ⭐\n\n1️⃣ أرسل {s} ⭐ على {sup}\n2️⃣ ID بتاعك: `{uid}`\n3️⃣ ستتم الإضافة خلال دقائق",
    # مبرمجين
    "dev_title": "💻 *قسم المبرمجين - شراء ملفات*",
    "dev_file": "{e} {n} | {s} ⭐",
    "dev_detail": "{e} *{n}*\n{d}\n\n💰 {s} ⭐\n\n1️⃣ أرسل {s} ⭐ على {sup}\n2️⃣ اذكر اسم الملف + ID: `{uid}`",
    "buy_btn": "💬 شراء",
    # نتائج
    "img_caption": "✅\n📝 {p}",
    "music_ok": "✅\n🎵 {p}",
    "music_fail": "❌ فشل في التوليد، أُعيدت النقاط",
    "open_btn": "🖼️ افتح",
    "choose_first": "🖼️ اختر من القائمة أولاً",
    "inv_joined": "🎉 صديقك @{u} انضم!\n+{pts} نقاط ✅",
    "new_user": "👤 *مستخدم جديد!*\nID: `{uid}`\nUsername: @{u}",
    "ai_fail": "⚠️ المساعد لا يستجيب الآن، أرسل رسالتك مرة أخرى.",
}

EN = {
    "welcome": "⊏ ━━ 𝑴𝒐𝒂𝒛 𝑴𝒐𝒉𝒂𝒎𝒎𝒆𝒅 𝑨𝑰 𝑩𝒐𝒕 ━━ ⊐\n\n𝑯𝒆𝒍𝒍𝒐 𝒎𝒚 𝒇𝒓𝒊𝒆𝒏𝒅! 🌟 𝑾𝒆𝒍𝒄𝒐𝒎𝒆 𝒕𝒐 𝒕𝒉𝒆 𝒄𝒓𝒆𝒂𝒕𝒊𝒗𝒊𝒕𝒚 𝒇𝒂𝒄𝒕𝒐𝒓𝒚..\n𝑹𝒆𝒂𝒅𝒚 𝒕𝒐 𝒕𝒖𝒓𝒏 𝒚𝒐𝒖𝒓 𝒊𝒅𝒆𝒂𝒔 𝒊𝒏𝒕𝒐 𝒓𝒆𝒂𝒍𝒊𝒕𝒚? 🚀\n\n✦ 𝑽𝒊𝒔𝒖𝒂𝒍𝒊𝒛𝒆 𝒚𝒐𝒖𝒓 𝒊𝒎𝒂𝒈𝒊𝒏𝒂𝒕𝒊𝒐𝒏 𝒘𝒊𝒕𝒉 𝒈𝒆𝒏𝒆𝒓𝒂𝒕𝒊𝒐𝒏 𝒕𝒐𝒐𝒍𝒔 🖼️\n✦ 𝑪𝒓𝒆𝒂𝒕𝒆 𝒚𝒐𝒖𝒓 𝒗𝒊𝒅𝒆𝒐𝒔 𝒘𝒊𝒕𝒉 𝒂 𝒄𝒍𝒊𝒄𝒌 🎥\n✦ 𝑪𝒐𝒎𝒑𝒐𝒔𝒆 𝒚𝒐𝒖𝒓 𝒐𝒘𝒏 𝒎𝒖𝒔𝒊𝒄 🎧\n✦ 𝑨𝒔𝒌 𝑨𝑰 & 𝒉𝒂𝒗𝒆 𝒇𝒖𝒏 𝒘𝒊𝒕𝒉 𝒖𝒔 💡\n\n𝑪𝒉𝒐𝒐𝒔𝒆 𝒇𝒓𝒐𝒎 𝒕𝒉𝒆 𝒃𝒖𝒕𝒕𝒐𝒏𝒔 𝒃𝒆𝒍𝒐𝒘 𝒂𝒏𝒅 𝒍𝒆𝒕'𝒔 𝒈𝒐 👇\n⊏ ━━━━━━━━━━━━━━━━━━━━━━━ ⊐",
    "btn_edit": "🎨 Edit Image", "btn_image": "🖼️ Create Image",
    "btn_music": "🎵 Create Song", "btn_video": "🎬 Generate Video",
    "btn_chat": "🤖 CHAT AI",
    "btn_points": "🎁 Collect Points", "btn_account": "👤 My Account",
    "btn_shop": "💳 Buy Points", "btn_support": "🆘 Support",
    "btn_dev": "💻 Dev Files | Buy Scripts",
    "back": "🔙 Back",
    "choose_lang": "🌍 اختر لغتك | Choose your language",
    "sub_required": "⚠️ You must subscribe to the channel first:",
    "sub_check": "✅ I Subscribed",
    "sub_not_yet": "❌ Not subscribed yet!",
    "banned": "🚫 You are banned.",
    "frozen": "❄️ Account frozen, contact support.",
    "maintenance": "⚙️ Bot under maintenance, come back later",
    "no_pts": "❌ Not enough points! You need {n} points",
    "invite_collect": "🔗 Invite Friend",
    "buy_pts_btn": "💳 Buy Points",
    "waiting": "⏳ Processing, please wait...",
    "fail_refund": "❌ Operation failed, points refunded",
    "img_choose": "🖼️ Choose generation type:",
    "img_nano_std": "🍌 Nano Banana Standard ({n} pts)",
    "img_nano_pro": "⭐ Nano Banana Pro ({n} pts)",
    "img_prompt": "✅ Write your prompt:",
    "edit_choose": "🎨 Choose edit type:",
    "edit_std": "✏️ Standard Edit ({n} pts)",
    "edit_pro": "⭐ Pro Edit ({n} pts)",
    "edit_send_photo": "✏️ Send the photo:",
    "edit_pro_send": "⭐ Send photo(s):\n(Send text directly to edit)",
    "photo_ok": "✅ Photo received! Send your prompt:",
    "photo_added": "✅ Photo {n} added!\nSend another photo or write the prompt:",
    "vid_choose": "🎬 Choose video type:",
    "vid_text": "📝 Text → Video",
    "vid_img": "🖼️ Image → Video",
    "vid_send_desc": "📝 Send video description:",
    "vid_send_photo": "🖼️ Send the photo:",
    "vid_photo_ok": "✅ Photo received! Send video description:",
    "vid_caption": "✅ Video ready!\n📝 {p}",
    "music_choose": "🎵 Choose:",
    "music_idea_btn": "💡 From idea",
    "music_lyrics_btn": "📝 From lyrics",
    "music_idea_send": "💡 Send your song idea:",
    "music_lyrics_send": "📝 Send your song lyrics:",
    "chat_title": "💬 *Personal Assistant*\n\nAsk me anything and I will reply instantly 🌟\n\n(Press /start to exit chat)",
    "support_title": "🆘 *Support*\n\n💬 Ask your question about the bot and we will help you!\n\n(Press /start to exit)",
    "contact_btn": "💬 Direct Contact",
    "account_title": "👤 *My Account*",
    "account_body": "🆔 ID: `{uid}`\n⭐ Points: {pts}\n📊 Total: {tot}\n{emoji} Level: {lvl}{next}\n🎁 Perks: {perks}\n\n🔗 Invites: {inv}\n🖼️ {ti} images | 🎬 {tv} videos\n🎵 {tm} songs | ✏️ {te} edits",
    "next_level": "\n📈 To next level: {n} pts",
    "max_level": "\n🏆 Max level!",
    "send_ref": "📤 Send Referral Link",
    "ref_msg": "🔗 Your referral link:\n\n{link}\n\n📲 Share and earn {pts} points per invite!",
    "collect_title": "🎁 *Collect Points*\n\n⭐ Your points: {pts}",
    "daily_btn": "🎁 Daily Gift (+{pts} pts)",
    "daily_wait": "🎁 Gift after {h}:{m:02d}",
    "invite_btn": "🔗 Invite Friend (+{pts} pts/invite)",
    "games_btn": "🎮 Games (+4 pts)",
    "code_btn": "🎟️ Points Code",
    "transfer_btn": "💸 Transfer Points",
    "transfer_enter_id": "💸 *Transfer Points*\n\nSend the ID of the user you want to transfer to:",
    "transfer_enter_pts": "💸 Transfer to `{uid2}`\n\nHow many points? (Your balance: {bal})",
    "transfer_ok": "✅ Transferred {pts} points to `{uid2}`\n⭐ New balance: {bal}",
    "transfer_recv": "🎁 Received {pts} points from @{sender}!\n⭐ Your balance: {bal}",
    "transfer_no_pts": "❌ Insufficient balance!",
    "transfer_no_user": "❌ User not found!",
    "transfer_self": "❌ Can't transfer to yourself!",
    "transfer_min": "❌ Minimum transfer is 1 point!",
    "daily_claimed": "❌ Already claimed today!",
    "daily_ok": "🎉 +{pts} points ✅\n⭐ Balance: {bal}",
    "code_enter": "🎟️ Send the code:",
    "code_ok": "✅ +{pts} points!\n⭐ Balance: {bal}",
    "code_wrong": "❌ Wrong code!",
    "code_used_up": "❌ Code fully used!",
    "code_expired": "❌ Code expired!",
    "code_already": "❌ Already used this code!",
    "stars_payment": "⭐ Buy with Stars",
    "stars_buy_btn": "💫 Buy Now with Stars",
    "stars_success": "✅ Thank you! Stars received. Adding points...",
    "games_title": "🎮 Choose a game:",
    "game_xo": "🎮 XO",
    "game_quiz": "🧠 Quiz",
    "game_word": "🔤 Complete the Word",
    "no_tries": "❌ No more tries today!\nCome back after {h}:{m:02d}",
    "game_xo_start": "🎮 *XO* - Attempt {n}/3\n🏆 Win = {pts} pts\nYou ❌ | AI ⭕",
    "game_quiz_q": "🧠 Attempt {n}/3 | 🏆 {pts} pts\n\n❓ {q}",
    "game_word_q": "🔤 Attempt {n}/3 | 🏆 {pts} pts\n\n{disp}\n💡 {hint}\n\nType the word:",
    "game_won": "🎉 You won! +{pts} points ✅",
    "game_draw": "🤝 Draw!",
    "game_ai_won": "😔 AI won! Try again 💪",
    "game_wrong_q": "❌ Wrong! Correct answer: {ans}",
    "game_wrong_w": "❌ Wrong! The word was: {word}",
    "try_again": "🎮 Try Again",
    "xo_turn": "🎮 Your turn:",
    "surrender": "🏳️ Surrender",
    "gen_question": "⏳ Generating question...",
    "fail_try": "❌ Failed, try again",
    "shop_title": "💳 *Buy Points with Telegram Stars*",
    "shop_pkg": "{e} {n} | {p} pts ← {s} ⭐",
    "shop_detail": "{e} *{n}*\n\n{p} pts ← {s} ⭐\n\n1️⃣ Send {s} ⭐ to {sup}\n2️⃣ Your ID: `{uid}`\n3️⃣ Points added within minutes",
    "dev_title": "💻 *Developer Files*",
    "dev_file": "{e} {n} | {s} ⭐",
    "dev_detail": "{e} *{n}*\n{d}\n\n💰 {s} ⭐\n\n1️⃣ Send {s} ⭐ to {sup}\n2️⃣ Mention file name + ID: `{uid}`",
    "buy_btn": "💬 Buy",
    "img_caption": "✅\n📝 {p}",
    "music_ok": "✅\n🎵 {p}",
    "music_fail": "❌ Generation failed, points refunded",
    "open_btn": "🖼️ Open",
    "choose_first": "🖼️ Choose from the menu first",
    "inv_joined": "🎉 Your friend @{u} joined!\n+{pts} points ✅",
    "new_user": "👤 *New User!*\nID: `{uid}`\nUsername: @{u}",
    "ai_fail": "⚠️ Assistant not responding, please send your message again.",
}

def T(lang, key, **kw):
    d = EN if lang == "en" else AR
    txt = d.get(key, AR.get(key, key))
    try:
        result = txt.format(**kw) if kw else txt
        # لو النص فاضي ارجع fallback
        return result if result and result.strip() else (f"[{key}]" if not result else result)
    except Exception as e:
        print(f"T() format error key={key}: {e}")
        return txt if txt else f"[{key}]"

# ==================== DATABASE ====================
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db(); c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY, username TEXT, lang TEXT DEFAULT 'ar',
        points INTEGER DEFAULT 4, total_points INTEGER DEFAULT 4,
        invites INTEGER DEFAULT 0, invited_by INTEGER DEFAULT 0,
        joined_at INTEGER DEFAULT 0, last_daily INTEGER DEFAULT 0,
        last_game INTEGER DEFAULT 0, game_attempts INTEGER DEFAULT 0,
        game_reset_time INTEGER DEFAULT 0,
        xo_attempts INTEGER DEFAULT 0, xo_reset_time INTEGER DEFAULT 0,
        quiz_attempts INTEGER DEFAULT 0, quiz_reset_time INTEGER DEFAULT 0,
        word_attempts INTEGER DEFAULT 0, word_reset_time INTEGER DEFAULT 0,
        is_banned INTEGER DEFAULT 0, is_frozen INTEGER DEFAULT 0,
        total_images INTEGER DEFAULT 0, total_videos INTEGER DEFAULT 0,
        total_music INTEGER DEFAULT 0, total_edits INTEGER DEFAULT 0)""")
    # إضافة الأعمدة الجديدة لو مش موجودة (للـ DB القديم)
    existing_cols = {row[1] for row in c.execute("PRAGMA table_info(users)").fetchall()}
    for col, definition in [
        ("game_reset_time", "INTEGER DEFAULT 0"),
        ("is_frozen", "INTEGER DEFAULT 0"),
        ("xo_attempts", "INTEGER DEFAULT 0"),
        ("xo_reset_time", "INTEGER DEFAULT 0"),
        ("quiz_attempts", "INTEGER DEFAULT 0"),
        ("quiz_reset_time", "INTEGER DEFAULT 0"),
        ("word_attempts", "INTEGER DEFAULT 0"),
        ("word_reset_time", "INTEGER DEFAULT 0"),
    ]:
        if col not in existing_cols:
            c.execute(f"ALTER TABLE users ADD COLUMN {col} {definition}")
    c.execute("""CREATE TABLE IF NOT EXISTS captcha_keys (
        id INTEGER PRIMARY KEY AUTOINCREMENT, key TEXT UNIQUE,
        label TEXT DEFAULT '', is_active INTEGER DEFAULT 1,
        is_empty INTEGER DEFAULT 0, added_at INTEGER DEFAULT 0)""")
    c.execute("""CREATE TABLE IF NOT EXISTS codes (
        id INTEGER PRIMARY KEY AUTOINCREMENT, code TEXT UNIQUE,
        points INTEGER DEFAULT 0, max_uses INTEGER DEFAULT 1,
        used INTEGER DEFAULT 0, expires_at INTEGER DEFAULT 0,
        created_at INTEGER DEFAULT 0)""")
    c.execute("""CREATE TABLE IF NOT EXISTS code_uses (
        code_id INTEGER, user_id INTEGER, used_at INTEGER DEFAULT 0)""")
    c.execute("""CREATE TABLE IF NOT EXISTS channels (
        id INTEGER PRIMARY KEY AUTOINCREMENT, channel_id TEXT UNIQUE,
        channel_name TEXT, invite_link TEXT, is_active INTEGER DEFAULT 1)""")
    c.execute("""CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT)""")
    c.execute("""CREATE TABLE IF NOT EXISTS operations (
        id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER,
        op_type TEXT, created_at INTEGER DEFAULT 0)""")
    c.execute("""CREATE TABLE IF NOT EXISTS star_transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER,
        invoice_payload TEXT, stars_amount INTEGER, points_amount INTEGER,
        status TEXT, created_at INTEGER DEFAULT 0)""")

    defaults = {
        "bot_active": "1",
        "maintenance_msg": "⚙️ البوت تحت الصيانة، عد لاحقاً",
        "welcome_type": "text", "welcome_media": "",
        "waiting_text": "⏳ جارٍ التنفيذ، انتظر...",
        "points_daily": "5", "points_invite": "2",
        "points_nano_std": "1", "points_nano_pro": "2",
        "points_video": "2", "points_music": "2",
        "force_sub": "0", "notify_new_user": "1", "notify_code_used": "1",
        "ai_system_prompt": (
            "أنت مساعد ذكي في بوت معاذ محمد للذكاء الاصطناعي.\n"
            "قواعد صارمة يجب الالتزام بها دائماً:\n"
            "- تحدث بالعربية الفصحى الرسمية فقط في جميع ردودك\n"
            "- لا تستخدم العامية أو اللهجات المحلية أبداً تحت أي ظرف\n"
            "- كن موجزاً ومفيداً ودقيقاً في إجاباتك\n"
            "- إذا وجّه إليك المستخدم سؤالاً بالعامية فأجبه بالفصحى"
        ),
        "support_system": (
            "أنت مساعد الدعم الفني الرسمي لبوت معاذ محمد على تيليغرام.\n"
            "تحدث دائماً بالعربية الفصحى فقط. أسلوبك: مفيد ومختصر وودود.\n\n"
            "⚠️ قاعدة مهمة: أجب فقط على الأسئلة المتعلقة بالبوت وخدماته.\n"
            "إذا سألك أحد عن أي شيء آخر (أخبار، رياضة، ثقافة، إلخ) قل:\n"
            "'أنا مساعد مخصص لدعم بوت معاذ فقط. للمساعدة العامة استخدم قسم المحادثة.'\n\n"
            "══ بيانات البوت الكاملة ══\n\n"
            "📌 اسم البوت: بوت معاذ محمد للذكاء الاصطناعي\n"
            "🎨 الخدمات:\n"
            "• إنشاء صور: نانو بانانا عادي (1 نقطة) أو برو (2 نقطة)\n"
            "• تعديل صور: عادي (1 نقطة) أو برو (2 نقطة، يدعم صور متعددة)\n"
            "• توليد فيديو: من نص أو صورة (2 نقطة)\n"
            "• توليد موسيقى: من فكرة أو كلمات (2 نقطة)\n"
            "• محادثة AI مجانية بدون نقاط\n\n"
            "💰 كيف تكسب النقاط:\n"
            "• عند التسجيل: 4 نقاط مجاناً\n"
            "• الهدية اليومية: 5 نقاط كل 24 ساعة\n"
            "• دعوة أصدقاء: 2 نقطة لكل شخص تدعوه\n"
            "• الألعاب: حتى 4 نقاط يومياً (3 محاولات منفصلة لكل لعبة)\n"
            "• أكواد خاصة من الأدمن\n"
            "• تحويل نقاط بين المستخدمين متاح\n\n"
            "🏆 نظام المستويات (حسب النقاط الإجمالية):\n"
            "• 🌱 مبتدئ (0-19 نقطة): المميزات الأساسية فقط\n"
            "• ⭐ محترف (20-49 نقطة): الهدية اليومية +2 نقطة إضافية + أولوية الخدمة\n"
            "• 🔥 أسطوري (50+ نقطة): الهدية اليومية +5 نقطة إضافية + أولوية + شارة\n"
            "المستوى يرتفع تلقائياً كلما راكمت نقاطاً إجمالية أكثر (لا تنقص حتى لو أنفقت)\n\n"
            "🎮 الألعاب (في قسم تجميع النقاط):\n"
            "• XO ضد الذكاء الاصطناعي (3 محاولات/12 ساعة لـ XO فقط)\n"
            "• سؤال وجواب ثقافي (3 محاولات/12 ساعة للسؤال فقط)\n"
            "• أكمل الكلمة (3 محاولات/12 ساعة للكلمة فقط)\n"
            "كل لعبة لها عداد مستقل، فوزك في XO لا يؤثر على Quiz أو الكلمة\n\n"
            "💳 شراء نقاط بنجوم تيليغرام:\n"
            "• ستارتر: 30 نقطة / 15 نجمة\n"
            "• بلس: 50 نقطة / 25 نجمة\n"
            "• برو: 100 نقطة / 50 نجمة\n"
            "• ملكي: 200 نقطة / 90 نجمة\n"
            "• أسطوري: 500 نقطة / 200 نجمة\n\n"
            "كيفية الشراء: اضغط الشراء من قسم الشراء في البوت ثم تواصل لإتمام الطلب\n\n"
            "إذا لم تعرف الإجابة بالتحديد، قل: 'هذا السؤال يحتاج تدخل بشري، تواصل عبر الدعم.'"
        ),
    }
    for k, v in defaults.items():
        c.execute("INSERT OR IGNORE INTO settings VALUES (?,?)", (k, v))

    default_keys = [
        ("uA1h2Smz4WzEZh7aOjQMg0HK3WBGuCrY", "key1"),
    ]
    for k, l in default_keys:
        c.execute("INSERT OR IGNORE INTO captcha_keys (key,label,added_at) VALUES (?,?,?)", (k, l, int(time.time())))
    conn.commit()

    conn.close()
    print("✅ Database ready!")

def gs(key, default=""):
    conn = get_db()
    r = conn.execute("SELECT value FROM settings WHERE key=?", (key,)).fetchone()
    conn.close()
    return r[0] if r else default

def gs_safe(key, default="..."):
    """gs مع ضمان عدم إرجاع نص فاضي - للاستخدام مع reply_text"""
    val = gs(key, default)
    return val if val and val.strip() else default

def ss(key, value):
    conn = get_db()
    conn.execute("INSERT OR REPLACE INTO settings VALUES (?,?)", (key, str(value)))
    conn.commit(); conn.close()

def get_user(uid):
    conn = get_db()
    u = conn.execute("SELECT * FROM users WHERE id=?", (uid,)).fetchone()
    conn.close(); return u

def get_lang(uid):
    u = get_user(uid)
    return u["lang"] if u else "ar"

def create_user(uid, username, lang="ar", invited_by=0):
    conn = get_db()
    conn.execute("""INSERT OR IGNORE INTO users
        (id,username,lang,points,total_points,invited_by,joined_at)
        VALUES (?,?,?,4,4,?,?)""", (uid, username, lang, invited_by, int(time.time())))
    conn.commit(); conn.close()

def add_points(uid, pts):
    conn = get_db()
    conn.execute("UPDATE users SET points=points+?, total_points=total_points+? WHERE id=?", (pts, pts, uid))
    conn.commit(); conn.close()

def deduct_points(uid, pts):
    conn = get_db()
    conn.execute("UPDATE users SET points=MAX(0,points-?) WHERE id=?", (pts, uid))
    conn.commit(); conn.close()

def has_points(uid, needed):
    u = get_user(uid)
    return u and u["points"] >= needed

def create_star_payment_link(pkg_idx):
    """Creates a t.me/$ payment link that opens native Telegram payment modal"""
    try:
        pkg = SHOP_POINTS_PKGS[pkg_idx]
        link = bot.create_invoice_link(
            title=f"شراء {pkg['name_ar']} | Buy {pkg['name_en']}",
            description=f"{pkg['points']} نقطة | {pkg['points']} points",
            payload=f"stars_pkg_{pkg_idx}_{int(time.time())}",
            currency="XTR",
            prices=[LabeledPrice(label=f"{pkg['stars']} ⭐", amount=pkg['stars'])],
            provider_token=""
        )
        return link
    except Exception as e:
        print(f"❌ create_star_payment_link error: {e}")
        return None

SHOP_POINTS_PKGS = [
    {"emoji": "🌱", "name_ar": "ستارتر", "name_en": "Starter", "points": 30, "stars": 15},
    {"emoji": "⭐", "name_ar": "بلس", "name_en": "Plus", "points": 50, "stars": 25},
    {"emoji": "🔥", "name_ar": "برو", "name_en": "Pro", "points": 100, "stars": 50},
    {"emoji": "👑", "name_ar": "ملكي", "name_en": "Royal", "points": 200, "stars": 90},
    {"emoji": "💎", "name_ar": "أسطوري", "name_en": "Legendary", "points": 500, "stars": 200},
]

SHOP_FILES = []

LEVELS = [
    {"min": 0,    "name_ar": "مبتدئ",    "name_en": "Beginner",   "emoji": "🌱", "daily_bonus": 0},
    {"min": 50,   "name_ar": "متعلم",    "name_en": "Learner",    "emoji": "📚", "daily_bonus": 1},
    {"min": 150,  "name_ar": "محترف",    "name_en": "Pro",        "emoji": "⚡", "daily_bonus": 2},
    {"min": 400,  "name_ar": "خبير",     "name_en": "Expert",     "emoji": "🔥", "daily_bonus": 3},
    {"min": 1000, "name_ar": "أسطورة",   "name_en": "Legend",     "emoji": "👑", "daily_bonus": 5},
]

def get_level(total_pts):
    for lv in reversed(LEVELS):
        if total_pts >= lv["min"]:
            return lv
    return LEVELS[0]

def log_op(uid, op):
    conn = get_db()
    conn.execute("INSERT INTO operations (user_id,op_type,created_at) VALUES (?,?,?)", (uid, op, int(time.time())))
    col = {"image": "total_images", "video": "total_videos", "music": "total_music", "edit": "total_edits"}.get(op)
    if col:
        conn.execute(f"UPDATE users SET {col}={col}+1 WHERE id=?", (uid,))
    conn.commit(); conn.close()

# ==================== NOTIFY ADMIN ====================
def notify_admin(text):
    if not text or not str(text).strip(): return
    try:    bot.send_message(ADMIN_ID, str(text), parse_mode="HTML")
    except Exception as e:
        try:    bot.send_message(ADMIN_ID, str(text))
        except Exception as _e: print(f"⚠️ notify_admin: {_e}")


# ==================== CAPTCHA (SCTG) ====================
SCTG_KEY = "bxFW8ONYe6sm1qlr8Q87hcPpOMqBaz5d"
SCTG_URL = "https://api.sctg.xyz"

def solve_turnstile(site_key, page_url, proxy=None):
    """حل Turnstile عبر sctg.xyz"""
    try:
        # إرسال المهمة
        r = requests.post(f"{SCTG_URL}/in.php", data={
            "key": SCTG_KEY,
            "method": "turnstile",
            "sitekey": site_key,
            "pageurl": page_url,
            "json": "1",
        }, timeout=30)
        print(f"sctg submit raw: {r.text[:100]}")
        data = r.json()
        if data.get("status") != 1:
            print(f"⚠️ sctg submit error: {data}")
            return None
        task_id = data["request"]
        # انتظار النتيجة
        for _ in range(30):
            time.sleep(5)
            r2 = requests.get(f"{SCTG_URL}/res.php", params={
                "key": SCTG_KEY, "action": "get", "id": task_id, "json": "1"
            }, timeout=15)
            print(f"sctg result raw: {r2.text[:100]}")
            d2 = r2.json()
            if d2.get("status") == 1:
                return d2["request"]
            if d2.get("request") != "CAPCHA_NOT_READY":
                print(f"⚠️ sctg result error: {d2}")
                return None
        print("⚠️ sctg timeout")
        return None
    except Exception as e:
        print(f"⚠️ solve_turnstile error: {e}")
        return None


# ==================== DEEPSEEK AI ====================
SII3_KEY = "DarkAI-DeepAI-EFF939A9130A0ABAE3A7414D"
SII3_URL = "https://sii3.top/api/deepseek/api.php"

def deepseek_chat(text, history=None):
    try:
        r = requests.post(SII3_URL, data={"key": SII3_KEY, "v3": text}, timeout=60)
        if r.status_code == 200 and r.text.strip():
            try:
                data = r.json()
                return data.get("response") or data.get("text") or r.text.strip()
            except:
                return r.text.strip()
    except Exception as e:
        print(f"deepseek error: {e}")
    return None

def support_ai(text, history=None):
    return deepseek_chat(text, history)

# ==================== PROXY ====================
def get_proxy():
    p = random.choice(PROXIES)
    return {"http": f"http://{p}", "https": f"http://{p}"}

def get_scraper_proxy():
    """ScraperAPI كـ proxy عادي - بيحافظ على الكوكيز والجلسة"""
    return {
        "http":  f"http://scraperapi:{SCRAPERAPI_KEY}@proxy-server.scraperapi.com:8001",
        "https": f"http://scraperapi:{SCRAPERAPI_KEY}@proxy-server.scraperapi.com:8001",
    }

def make_scraper_session(headers=None):
    """Session جاهز مع ScraperAPI وبدون SSL verification"""
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    s = requests.Session()
    s.proxies.update(get_scraper_proxy())
    s.verify = False
    if headers:
        s.headers.update(headers)
    return s

def smart_get(session, url, **kwargs):
    proxy = get_proxy()
    try:
        r = session.get(url, proxies=proxy, timeout=15, **kwargs)
        if r.status_code == 200: return r, proxy
    except Exception as _e: print(f"⚠️ [LINE 624] {type(_e).__name__}: {_e}")
    try:
        r = requests.get("https://proxy.scrapeops.io/v1/",
            params={"api_key": SCRAPEOPS_KEY, "url": url, "bypass": "cloudflare"}, timeout=60)
        return r, None
    except Exception as _e: print(f"⚠️ [LINE 629] {type(_e).__name__}: {_e}")
    return None, None

# ==================== AI ====================
# ========== DEEPSEAK AI ==========
# ===== DeepSeek API (sii3.top) =====
SII3_KEY = "DarkAI-DeepAI-EFF939A9130A0ABAE3A7414D"
SII3_URL = "https://sii3.top/api/deepseek/api.php"

def support_ai(text, history=None):
    return deepseek_chat(text, history)

# ===== DeepSeek fallback (deepseak.org) =====
_DS_URL   = "https://deepseak.org/wp-admin/admin-ajax.php"
_DS_PAGE  = "https://deepseak.org/"
_DS_BOT   = "156"
_DS_POST  = "9"
_DS_NONCE = "0d323ae53b"  # fallback - بيتجدد تلقائياً
_DS_HDR   = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Mobile Safari/537.36",
    "origin":  "https://deepseak.org",
    "referer": "https://deepseak.org/",
}
_ds_nonce_cache = {"value": _DS_NONCE, "ts": 0}  # كاش الـ nonce

def _ds_fetch_nonce():
    """جيب الـ nonce الجديد من الصفحة"""
    global _ds_nonce_cache
    # لو الـ nonce اتجدد خلال آخر 30 دقيقة، استخدمه
    if time.time() - _ds_nonce_cache["ts"] < 1800:
        return _ds_nonce_cache["value"]
    try:
        r = requests.get(_DS_PAGE, headers=_DS_HDR, timeout=15)
        # استخرج الـ nonce من الـ HTML
        match = re.search(r'"nonce"\s*:\s*"([a-f0-9]+)"', r.text)
        if not match:
            match = re.search(r'aipkit_nonce["\s:]+([a-f0-9]{10,})', r.text)
        if not match:
            match = re.search(r'_ajax_nonce["\s:]+([a-f0-9]{10,})', r.text)
        if match:
            new_nonce = match.group(1)
            _ds_nonce_cache = {"value": new_nonce, "ts": time.time()}
            print(f"✅ DeepSeek nonce refreshed: {new_nonce}")
            return new_nonce
        else:
            print("⚠️ DeepSeek nonce not found in page, using cached")
    except Exception as e:
        print(f"⚠️ DeepSeek nonce fetch error: {e}")
    return _ds_nonce_cache["value"]

def _ds_client_id():
    ts = int(time.time() * 1000)
    r  = ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))
    return f"aipkit-client-msg-{_DS_BOT}-{ts}-{r}"

def _ds_get_key(prompt):
    nonce = _ds_fetch_nonce()
    try:
        payload = {
            "action":                (None, "aipkit_cache_sse_message"),
            "message":               (None, prompt),
            "_ajax_nonce":           (None, nonce),
            "bot_id":                (None, _DS_BOT),
            "user_client_message_id":(None, _ds_client_id()),
        }
        r = requests.post(_DS_URL, files=payload, headers=_DS_HDR, timeout=20)
        d = r.json()
        if d.get("success"):
            return d["data"]["cache_key"]
        # لو فشل بسبب الـ nonce، اعمل refresh إجباري وجرب تاني
        if "nonce" in str(d).lower():
            print("⚠️ Nonce expired, force refreshing...")
            _ds_nonce_cache["ts"] = 0  # إعادة ضبط الكاش عشان يجيب نونس جديد
            nonce = _ds_fetch_nonce()
            payload["_ajax_nonce"] = (None, nonce)
            r2 = requests.post(_DS_URL, files=payload, headers=_DS_HDR, timeout=20)
            d2 = r2.json()
            if d2.get("success"):
                return d2["data"]["cache_key"]
            print(f"⚠️ DeepSeek cache_key failed after refresh: {d2}")
        else:
            print(f"⚠️ DeepSeek cache_key failed: {d}")
    except Exception as e:
        print(f"⚠️ DeepSeek get_key error: {e}")
    return None

def _ds_stream(cache_key):
    nonce = _ds_nonce_cache["value"]  # استخدم الـ nonce الحالي
    params = {
        "action":            "aipkit_frontend_chat_stream",
        "cache_key":         cache_key,
        "bot_id":            _DS_BOT,
        "session_id":        str(uuid.uuid4()),
        "conversation_uuid": str(uuid.uuid4()),
        "post_id":           _DS_POST,
        "_ts":               int(time.time() * 1000),
        "_ajax_nonce":       nonce,
    }
    hdrs = {**_DS_HDR, "Accept": "text/event-stream"}
    result = []
    try:
        r = requests.get(_DS_URL, params=params, headers=hdrs, stream=True, timeout=60)
        for line in r.iter_lines():
            if not line: continue
            decoded = line.decode("utf-8")
            if not decoded.startswith("data:"): continue
            data_str = decoded[5:].strip()
            if not data_str: continue
            try:
                j = json.loads(data_str)
                if "delta" in j:
                    result.append(j["delta"])
                elif j.get("finished"):
                    break
            except json.JSONDecodeError:
                pass
    except Exception as e:
        print(f"⚠️ DeepSeek stream error: {e}")
    return "".join(result).strip()

# ========== SII3 DEEPSEEK FALLBACK ==========
_SII3_KEY = "DarkAI-DeepAI-EFF939A9130A0ABAE3A7414D"
_SII3_URL = "https://sii3.top/api/deepseek/api.php"

def _sii3_ask(prompt):
    """DeepSeek عبر sii3.top كـ fallback"""
    try:
        r = requests.post(_SII3_URL, data={"key": _SII3_KEY, "v3": prompt}, timeout=30)
        if r.status_code == 200:
            data = r.json()
            resp = data.get("response", "").strip()
            if resp:
                return resp
            print(f"⚠️ sii3 no response field: {str(data)[:100]}")
        else:
            print(f"⚠️ sii3 status: {r.status_code} {r.text[:100]}")
    except Exception as e:
        print(f"⚠️ sii3 error: {e}")
    return None

def ask_ai(question, system_prompt=None, history=None):
    try:
        if system_prompt is None:
            system_prompt = gs("ai_system_prompt")
        conversation = ""
        if history:
            for h in history[-8:]:
                role_txt = "المستخدم" if h["role"] == "user" else "المساعد"
                conversation += f"{role_txt}: {h['content']}\n"
        if system_prompt and system_prompt.strip():
            full_msg = f"{system_prompt}\n\n---\n{conversation}المستخدم يسأل: {question}"
        else:
            full_msg = f"{conversation}المستخدم: {question}" if conversation else question

        # 1. جرب DeepSeek مرة واحدة
        try:
            key = _ds_get_key(full_msg)
            if key:
                resp = _ds_stream(key)
                if resp:
                    return resp
        except Exception as e:
            print(f"⚠️ DeepSeek error: {e}")

        # 2. fallback: sii3.top
        print("🔄 Trying sii3.top fallback...")
        resp = _sii3_ask(full_msg)
        if resp:
            return resp

    except Exception as e:
        print(f"⚠️ ask_ai outer error: {e}")
    return None


def support_ai(question, history=None):
    # جيب إحصائيات حية وأضفها للـ system prompt
    try:
        conn = get_db()
        total_users  = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
        active_users = conn.execute("SELECT COUNT(*) FROM users WHERE joined_at > ?", (int(time.time()) - 86400*7,)).fetchone()[0]
        conn.close()
    except:
        total_users = active_users = "غير معروف"
    live_info = (
        f"\n\n══ إحصائيات البوت الحية ══\n"
        f"👥 إجمالي المستخدمين: {total_users}\n"
        f"🟢 نشطين آخر 7 أيام: {active_users}\n"
    )
    system = gs("support_system") + live_info
    return ask_ai(question, system, history)

def generate_quiz_question(difficulty="medium"):
    diff_map = {"hard": "hard specialized", "medium": "medium general", "easy": "easy general"}
    prompt = (
        f"Create a {diff_map.get(difficulty,'medium')} Arabic trivia question.\n"
        "STRICT RULES:\n"
        "- All 4 options (A,B,C,D) must be COMPLETELY DIFFERENT from each other\n"
        "- Only ONE option is correct\n"
        "- Wrong options must be plausible but clearly wrong\n"
        "- No repetition between options\n"
        "Reply ONLY in this exact format, nothing else:\n"
        "QUESTION: [السؤال هنا]\n"
        "A: [الخيار أ]\n"
        "B: [الخيار ب]\n"
        "C: [الخيار ج]\n"
        "D: [الخيار د]\n"
        "ANSWER: [A or B or C or D]"
    )
    for _ in range(5):
        response = ask_ai(prompt, "")
        if not response: continue
        try:
            q_m = re.search(r'QUESTION:\s*(.+)', response)
            a_m = re.search(r'A:\s*(.+)', response)
            b_m = re.search(r'B:\s*(.+)', response)
            c_m = re.search(r'C:\s*(.+)', response)
            d_m = re.search(r'D:\s*(.+)', response)
            ans_m = re.search(r'ANSWER:\s*([ABCD])', response)
            if not (q_m and a_m and b_m and c_m and d_m and ans_m): continue
            opts = {
                "A": a_m.group(1).strip(),
                "B": b_m.group(1).strip(),
                "C": c_m.group(1).strip(),
                "D": d_m.group(1).strip(),
            }
            # تحقق إن كل الإجابات مختلفة
            vals = list(opts.values())
            vals_lower = [v.strip().lower() for v in vals]
            if len(set(vals_lower)) < 4:
                print("quiz: duplicate options detected, retrying...")
                continue
            return {
                "question": q_m.group(1).strip(),
                "options": opts,
                "answer": ans_m.group(1).strip()
            }
        except Exception as _e:
            print(f"⚠️ [LINE 721] {type(_e).__name__}: {_e}")
            continue
    return None

def generate_word_question(difficulty="medium", used_words=None):
    if used_words is None: used_words = []
    diff_config = {
        "hard":   {"letters": "7 أحرف أو أكثر", "hide": "اخفِ 70% من الحروف"},
        "medium": {"letters": "5-6 أحرف",       "hide": "اخفِ 50% من الحروف"},
        "easy":   {"letters": "4-5 أحرف",        "hide": "اخفِ 30% من الحروف"},
    }
    cfg = diff_config.get(difficulty, diff_config["medium"])
    exclude = f"\nلا تستخدم هذه الكلمات أبداً: {', '.join(used_words)}" if used_words else ""

    prompt = f"""أنت لعبة تعليمية عربية. اختر كلمة عربية واحدة ({cfg['letters']}) وأنشئ لغزاً.
{exclude}

القواعد الصارمة:
1. اختر كلمة عربية شائعة ومفيدة
2. {cfg['hide']} واستبدلها بـ _
3. الحروف الظاهرة يجب أن تكون في مواضعها الصحيحة من الكلمة
4. التلميح قصير جداً (3-5 كلمات) ولا يحتوي على الكلمة

أجب بهذا التنسيق الحرفي فقط بدون أي نص إضافي:
WORD: [الكلمة]
DISPLAY: [الكلمة مع _]
HINT: [التلميح]

مثال:
WORD: مدرسة
DISPLAY: م_ر_ة
HINT: مكان للتعلم"""

    for attempt in range(5):
        response = ask_ai(prompt, "")
        if not response:
            continue
        try:
            word_m  = re.search(r'WORD:\s*([^\n]+)',    response)
            disp_m  = re.search(r'DISPLAY:\s*([^\n]+)', response)
            hint_m  = re.search(r'HINT:\s*([^\n]+)',    response)
            if not (word_m and disp_m and hint_m):
                print(f"⚠️ Word game parse failed attempt {attempt+1}: {response[:100]}")
                continue
            word    = word_m.group(1).strip()
            display = disp_m.group(1).strip()
            hint    = hint_m.group(1).strip()

            # تجاهل لو الكلمة مكررة
            if word in used_words:
                continue
            # تحقق إن الحروف الظاهرة في الـ display صح
            if len(word) == len(display):
                for i, (w, d) in enumerate(zip(word, display)):
                    if d != '_' and d != w:
                        print(f"⚠️ Display mismatch at pos {i}: word={w} display={d}")
                        break
                else:
                    # تأكد إن في _ على الأقل واحد
                    if '_' in display:
                        return {"word": word, "display": display, "hint": hint}
            else:
                # لو الأطوال مختلفة - ممكن AI عمل فرمتة غلط، نقبله لو منطقي
                if '_' in display and len(display) >= 3:
                    return {"word": word, "display": display, "hint": hint}
        except Exception as e:
            print(f"⚠️ generate_word_question error attempt {attempt+1}: {e}")
    return None

def _minimax(board, is_maximizing, alpha=-float('inf'), beta=float('inf'), depth=0):
    """Minimax with Alpha-Beta pruning - AI is O (2), human is X (1)"""
    wins = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]
    # Check terminal state
    for w in wins:
        if board[w[0]] == board[w[1]] == board[w[2]] != 0:
            return (10 - depth) if board[w[0]] == 2 else (depth - 10)
    if 0 not in board: return 0  # draw
    if is_maximizing:  # AI (O=2)
        best = -float('inf')
        for i in range(9):
            if board[i] == 0:
                board[i] = 2
                best = max(best, _minimax(board, False, alpha, beta, depth+1))
                board[i] = 0
                alpha = max(alpha, best)
                if beta <= alpha: break
        return best
    else:  # Human (X=1)
        best = float('inf')
        for i in range(9):
            if board[i] == 0:
                board[i] = 1
                best = min(best, _minimax(board, True, alpha, beta, depth+1))
                board[i] = 0
                beta = min(beta, best)
                if beta <= alpha: break
        return best

def ai_xo_move(board, difficulty=65):
    empties = [i for i, v in enumerate(board) if v == 0]
    if not empties: return -1
    # لو صعوبة أقل من 90 - حركة عشوائية أحياناً (10% فقط)
    if random.randint(1, 100) > 90:
        return random.choice(empties)
    # Minimax - دايماً يختار أفضل حركة
    best_score = -float('inf')
    best_move = empties[0]
    for i in empties:
        board[i] = 2
        score = _minimax(board, False, -float('inf'), float('inf'), 0)
        board[i] = 0
        if score > best_score:
            best_score = score
            best_move = i
    return best_move

def check_xo_winner(board):
    for w in [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]:
        if board[w[0]] == board[w[1]] == board[w[2]] != 0:
            return board[w[0]]
    return -1 if 0 not in board else 0

# ==================== CORE GENERATION FUNCTIONS ====================
def _rand(n=10):
    return ''.join(random.choices(string.ascii_lowercase, k=n))

# ========== IMAGE HEADERS ==========
IMAGE_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36",
    "Content-Type": "application/json",
    "origin": "https://image-editor.org",
    "referer": "https://image-editor.org/",
}

# ========== WAIT FOR TASK ==========
def wait_for_task(task_id, proxy=None, timeout=180):
    import urllib3; urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    print(f"⏳ Waiting for result of task: {task_id}...")
    start = time.time()
    while time.time() - start < timeout:
        try:
            req_kwargs = {"headers": IMAGE_HEADERS, "timeout": 30, "verify": False}
            if proxy: req_kwargs["proxies"] = proxy
            r = requests.get(f"https://image-editor.org/api/task/{task_id}", **req_kwargs)
            print(f"   [Debug API] Status {r.status_code}: {r.text[:200]}")
            try:
                json_data = r.json()
            except ValueError:
                print("❌ السيرفر لم يرجع JSON صالح.")
                time.sleep(5)
                continue
            if not json_data.get("success"):
                print(f"❌ فشل من السيرفر أثناء الانتظار: {json_data}")
                return None
            data = json_data.get("data", {})
            status = data.get("status")
            if status == "completed":
                result = data.get("result", [])
                if result:
                    print(f"✅ Done: {result[0]}")
                    return result[0]
                return None
            elif status == "failed":
                print(f"❌ Task failed!")
                return None
            print(f"   ⏳ حالة المهمة الآن: {status}...")
        except Exception as e:
            err = str(e)
            print(f"❌ خطأ: {err}")
            if proxy and ("407" in err or "Proxy" in err):
                print("⚠️ ScraperAPI مش شغّال، بجرب بدون بروكسي...")
                proxy = None
        time.sleep(5)
    print("❌ Timeout")
    return None

# ========== SESSION CACHE ==========
_session_cache = {
    "veo3_image":  {"session": None, "token": None, "ts": 0},
    "veo3_video":  {"session": None, "token": None, "ts": 0},
    "veo3_img2vid":{"session": None, "token": None, "ts": 0},
}
SESSION_TTL = 3600 * 2  # ساعتين

def _get_cached_session(key):
    return None  # Session caching disabled

def _save_session(key, session):
    pass  # disabled

def _invalidate_session(key):
    _session_cache[key] = {"session": None, "ts": 0}

# ========== GENERATE IMAGE ==========
def generate_image(prompt, image_size="1:1", max_retries=3):
    import urllib3; urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    for attempt in range(max_retries):
        print(f"\n🚀 بدء محاولة التوليد رقم {attempt + 1}/{max_retries}")
        try:
            # أول محاولة بدون بروكسي، الباقي بـ ScraperAPI
            if attempt == 0:
                proxy = None
                print("🔄 بدون بروكسي")
            else:
                proxy = get_scraper_proxy()
                print("🔄 ScraperAPI proxy")

            token = solve_turnstile("0x4AAAAAACE-XLGoQUckKKm_", "https://image-editor.org/")
            if not token:
                continue
            user_uuid = str(uuid.uuid4())
            req_kwargs = {"headers": IMAGE_HEADERS, "timeout": 30, "verify": False}
            if proxy:
                req_kwargs["proxies"] = proxy

            r = requests.post("https://image-editor.org/api/generate", json={
                "prompt": prompt, "image_size": image_size,
                "turnstileToken": token, "userUUID": user_uuid
            }, **req_kwargs)
            print(f"Generate response: {r.text[:300]}")
            try:
                data = r.json()
            except ValueError:
                print("❌ Response not JSON, skipping")
                continue
            if not data.get("success"):
                continue
            task_data = data.get("data", {})
            task_id = task_data.get("taskId")
            if task_data.get("status") == "completed" and task_data.get("result"):
                return task_data["result"][0]
            if not task_id:
                continue
            result_url = wait_for_task(task_id, proxy)
            if result_url:
                return result_url
        except Exception as e:
            print(f"❌ Image Error: {e}")
    return None

# ========== NANOBANANA IMAGE ==========
# ========== VEO3AI IMAGE LOGIN ==========
VEO3_BASE = "https://www.veo3ai.io"
MAIL_GW_URL = "https://api.mail.gw"

def veo3_image_login(max_retries=2):
    """تسجيل دخول لـ veo3ai.io للصور"""
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    for attempt in range(max_retries):
        try:
            session = make_scraper_session({
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "content-type": "application/json",
                "origin": VEO3_BASE,
                "referer": f"{VEO3_BASE}/text-to-image",
            })

            print(f"📧 إنشاء إيميل (محاولة {attempt+1})...")
            r = requests.get(f"{MAIL_GW_URL}/domains", timeout=15, verify=False)
            domains = r.json().get("hydra:member", [])
            if not domains: continue
            email = f"{_rand(10)}@{random.choice(domains)['domain']}"
            pwd = "Pass1234!"
            requests.post(f"{MAIL_GW_URL}/accounts", json={"address": email, "password": pwd}, timeout=15, verify=False)
            tok_r = requests.post(f"{MAIL_GW_URL}/token", json={"address": email, "password": pwd}, timeout=15, verify=False)
            mail_token = tok_r.json().get("token")
            if not mail_token: continue
            print(f"✅ إيميل: {email}")

            token = solve_turnstile("0x4AAAAAABwzqT6AqNwHJZWq", VEO3_BASE)
            if not token: continue

            session.post(f"{VEO3_BASE}/api/auth/signup", json={
                "name": _rand(8), "email": email, "password": pwd, "captchaToken": token
            }, timeout=20)

            # انتظر رابط التفعيل (mail.gw بدون بروكسي)
            mail_headers = {"Authorization": f"Bearer {mail_token}"}
            verify_link = None
            for _ in range(30):
                msgs = requests.get(f"{MAIL_GW_URL}/messages", headers=mail_headers, timeout=10, verify=False).json().get("hydra:member", [])
                if msgs:
                    msg = requests.get(f"{MAIL_GW_URL}/messages/{msgs[0]['id']}", headers=mail_headers, timeout=10, verify=False).json()
                    m = re.search(r"(https://rjmeqtivlxgtconwkcmm\.supabase\.co/auth/v1/verify\?[^\s\"'\\]+)", str(msg))
                    if m:
                        verify_link = m.group(1)
                        break
                time.sleep(3)

            if not verify_link:
                print("❌ لم يصل رابط التفعيل")
                continue

            session.get(verify_link, allow_redirects=True, timeout=20)
            print("✅ تم التفعيل!")

            csrf = session.get(f"{VEO3_BASE}/api/auth/csrf", timeout=30).json().get("csrfToken")
            session.post(f"{VEO3_BASE}/api/auth/email-signin", json={"email": email, "password": pwd}, timeout=30)
            session.post(f"{VEO3_BASE}/api/auth/callback/email", data={
                "email": email, "password": pwd, "redirect": "false",
                "csrfToken": csrf, "callbackUrl": VEO3_BASE
            }, headers={"x-auth-return-redirect": "1", "content-type": "application/x-www-form-urlencoded"}, timeout=30)

            sess_data = session.get(f"{VEO3_BASE}/api/auth/session", timeout=30).json()
            if not sess_data.get("user"):
                print("❌ فشل تأكيد الجلسة")
                continue

            cookie_str = "; ".join([f"{k}={v}" for k, v in session.cookies.items()])
            session.headers.update({"Cookie": cookie_str})
            print(f"✅ Logged in: {sess_data['user']['email']}")
            pass  # no session cache
            return session, cookie_str

        except Exception as e:
            print(f"❌ veo3_image_login error (attempt {attempt+1}): {e}")
    return None, None

def veo3_upload_image(cookie_str, image_bytes):
    """رفع صورة على veo3ai.io وإرجاع الـ publicUrl"""
    try:
        filename = f"{uuid.uuid4()}.jpg"
        file_size = len(image_bytes)
        headers = {"User-Agent": "Mozilla/5.0", "Cookie": cookie_str, "Content-Type": "application/json"}

        r = requests.post(f"{VEO3_BASE}/api/upload/presign", headers=headers, json={
            "filename": filename, "contentType": "image/jpeg", "fileSize": file_size
        }, timeout=20)
        data = r.json()
        if data.get("code") != 0:
            print(f"❌ Presign failed: {data}")
            return None

        up_url = data["data"].get("presignedUrl")
        pub_url = data["data"].get("publicUrl")
        if not up_url or not pub_url: return None

        put_r = requests.put(up_url, data=image_bytes, headers={"Content-Type": "image/jpeg"}, timeout=60)
        if put_r.status_code in (200, 204):
            print(f"✅ Image uploaded: {pub_url[:60]}...")
            return pub_url
        else:
            print(f"❌ PUT failed: {put_r.status_code}")
    except Exception as e:
        print(f"❌ Upload error: {e}")
    return None

def _veo3_poll_image(task_id, session_or_headers, timeout=300):
    """انتظار نتيجة مهمة صورة من veo3ai.io"""
    start = time.time()
    body = json.dumps({"id": task_id})
    hdrs = {"Content-Type": "application/json"}
    while time.time() - start < timeout:
        time.sleep(5)
        try:
            if isinstance(session_or_headers, dict):
                r = requests.post(f"{VEO3_BASE}/api/image-generation/status",
                                  data=body, headers={**session_or_headers, **hdrs}, timeout=30)
            else:
                r = session_or_headers.post(f"{VEO3_BASE}/api/image-generation/status",
                                            data=body, headers=hdrs, timeout=30)
            if not r.text.strip():
                print("⚠️ Poll empty response, retrying...")
                continue
            data = r.json()
            if data.get("code") == 0:
                st = data["data"].get("status", "")
                print(f"   ⏳ {st}...")
                if st in ("COMPLETED", "SAVED_TO_R2", "completed"):
                    return (data["data"].get("image_url") or data["data"].get("url")
                            or data["data"].get("image_url_r2"))
                elif st in ("FAILED", "failed", "ERROR"):
                    print(f"❌ Task failed: {data['data'].get('error_message')}")
                    return None
            else:
                print(f"⚠️ Poll response: {data}")
        except Exception as e:
            print(f"⚠️ Poll error: {e}")
            # استمر ولا توقف - ممكن البروكسي انقطع لحظياً
    print("❌ Timeout")
    return None

SITE       = "fluxproweb.com"
BASE_URL   = f"https://{SITE}/ar/model/nano-banana-pro-ai/"
API        = "https://api2.tap4.ai"
MAIL_API   = "https://api.mail.gw"
ACTION_REG = "424401cbe4e8b1b79045e4ac3dcf3d788c2156dd"
ACTION_VER = "efbaa6169049c8cb5fd4fd1abe810d880738ab19"
ACTION_LOG = "1c7778f900ce2db3f2c455a90e709ef29ae30db3"

HEADERS = {
    "User-Agent":         "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Mobile Safari/537.36",
    "sec-ch-ua":          '"Not(A:Brand";v="8", "Chromium";v="144", "Brave";v="144"',
    "sec-ch-ua-mobile":   "?1",
    "sec-ch-ua-platform": '"Android"',
    "sec-gpc":            "1",
    "accept-language":    "ar-EG,ar;q=0.5",
    "origin":             f"https://{SITE}",
    "referer":            BASE_URL,
}

ROUTER = "%5B%22%22%2C%7B%22children%22%3A%5B%5B%22locale%22%2C%22ar%22%2C%22d%22%5D%2C%7B%22children%22%3A%5B%22(with-footer)%22%2C%7B%22children%22%3A%5B%22(templates)%22%2C%7B%22children%22%3A%5B%22model%22%2C%7B%22children%22%3A%5B%22nano-banana-pro-ai%22%2C%7B%22children%22%3A%5B%22__PAGE__%22%2C%7B%7D%2Cnull%2Cnull%5D%7D%2Cnull%2Cnull%5D%7D%2Cnull%2Cnull%5D%7D%2Cnull%2Cnull%5D%7D%2Cnull%2Cnull%5D%7D%2Cnull%2Cnull%2Ctrue%5D%7D%2Cnull%2Cnull%5D"

def get_account():
    r       = requests.get(f"{MAIL_API}/domains", timeout=10)
    domains = [d["domain"] for d in r.json().get("hydra:member", [])]
    for domain in domains:
        try:
            username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
            email    = f"{username}@{domain}"
            password = "Pass" + ''.join(random.choices(string.digits, k=8))
            r2 = requests.post(f"{MAIL_API}/accounts", json={"address": email, "password": password}, timeout=10)
            if r2.status_code not in (200, 201): continue
            r3 = requests.post(f"{MAIL_API}/token",    json={"address": email, "password": password}, timeout=10)
            if r3.status_code != 200: continue
            mail_token = r3.json()["token"]
            if try_register(email, password):
                return email, mail_token, password
        except:
            continue
    raise Exception("فشل إنشاء حساب")

def try_register(email, password):
    nickname = ''.join(random.choices(string.ascii_letters, k=8))
    hdrs     = {**HEADERS, "Accept": "text/x-component", "Content-Type": "text/plain;charset=UTF-8",
                "next-action": ACTION_REG, "next-router-state-tree": ROUTER}
    r        = requests.post(BASE_URL, data=json.dumps([{"email": email, "userName": nickname, "password": password}]),
                             headers=hdrs, timeout=15)
    m = re.search(r'1:\{"code":(\d+)', r.text)
    return m and int(m.group(1)) == 200

def wait_otp(mail_token):
    hdrs = {"Authorization": f"Bearer {mail_token}"}
    for _ in range(30):
        time.sleep(5)
        r    = requests.get(f"{MAIL_API}/messages", headers=hdrs)
        msgs = r.json().get("hydra:member", [])
        if msgs:
            r2   = requests.get(f"{MAIL_API}/messages/{msgs[0]['id']}", headers=hdrs)
            msg  = r2.json()
            text = msg.get("text", "") or ""
            html = msg.get("html", "") or ""
            if isinstance(text, list): text = " ".join(text)
            if isinstance(html, list): html = " ".join(html)
            m = re.search(r'\b(\d{6})\b', text + html)
            if m: return m.group(1)
    raise Exception("OTP لم يصل")

def verify_otp(email, otp):
    hdrs = {**HEADERS, "Accept": "text/x-component", "Content-Type": "text/plain;charset=UTF-8",
            "next-action": ACTION_VER, "next-router-state-tree": ROUTER}
    requests.post(BASE_URL, data=json.dumps([{"email": email, "emailCode": otp}]),
                  headers=hdrs, timeout=15)

def login(email, password):
    hdrs = {**HEADERS, "Accept": "text/x-component", "Content-Type": "text/plain;charset=UTF-8",
            "next-action": ACTION_LOG, "next-router-state-tree": ROUTER}
    r = requests.post(BASE_URL, data=json.dumps([{"email": email, "password": password}]),
                      headers=hdrs, timeout=15)
    for pattern in [r'"access_token":"([^"]+)"', r'Authorization=Bearer%20([^;%]+)']:
        m = re.search(pattern, r.text + r.headers.get("set-cookie", ""))
        if m: return m.group(1)
    raise Exception("فشل تسجيل الدخول")

def flux_generate(prompt, model="nb", image_urls=None, status_cb=None):
    def s(step, txt):
        if status_cb: status_cb(step, txt)

    s(1, "🔐 إنشاء حساب...")
    email, mail_token, password = get_account()

    s(2, "📬 انتظار OTP...")
    otp   = wait_otp(mail_token)
    verify_otp(email, otp)
    token = login(email, password)

    s(3, "🎨 إرسال الطلب...")
    hdrs = {
        **HEADERS,
        "Content-Type":     "application/json",
        "authorization":    f"Bearer {token}",
        "credentials":      "include",
        "content-language": "en",
        "sec-fetch-site":   "cross-site",
        "sec-fetch-mode":   "cors",
        "sec-fetch-dest":   "empty",
        "referer":          f"https://{SITE}/",
    }

    if model == "nbp":
        # Nano Banana Pro
        payload = {
            "site":         SITE,
            "imageType":    "nano-banana-pro-image",
            "platformType": 39,
            "modelName":    "gemini-3-pro-image-preview",
            "isPublic":     1,
            "prompt":       prompt,
            "outputPrompt": prompt,
            "resolution":   "2k",
            "width": 1, "height": 1, "ratio": "1:1",
            "supportRatio": True,
            "nsfwFilter":   True,
        }
    else:
        # Nano Banana
        payload = {
            "site":         SITE,
            "platformType": 44,
            "modelName":    "gemini-25-flash-image",
            "isTranslate":  True,
            "isPublic":     1,
            "prompt":       prompt,
            "outputPrompt": prompt,
            "width": 1, "height": 1, "ratio": "1:1",
            "supportRatio": True,
            "nsfwFilter":   True,
        }

    if image_urls:
        payload["imageUrlList"] = image_urls
    if image_urls:
        payload["imageUrlList"] = image_urls

    r   = requests.post(f"{API}/image/generator4login/async", data=json.dumps(payload), headers=hdrs)
    key = r.json()["data"]["key"]

    s(4, "🖼 جاري التوليد...")
    for i in range(60):
        time.sleep(4)
        r2   = requests.get(f"{API}/image/getResult/{key}?site={SITE}", headers=hdrs)
        item = r2.json().get("data", {})
        if item.get("status") in ("success", "finish", "done", "completed"):
            vo  = item.get("imageResponseVo", {})
            url = vo.get("url") or (vo.get("images", [{}])[0].get("url"))
            if url: return url
        if status_cb and i % 3 == 0:
            s(4, f"🖼 جاري التوليد... {(i+1)*4}s")
    raise Exception("انتهت المهلة")


def generate_image(prompt, image_size="1:1", max_retries=3):
    import urllib3; urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    for attempt in range(max_retries):
        print(f"\n🚀 بدء محاولة التوليد رقم {attempt + 1}/{max_retries}")
        try:
            # أول محاولة بدون بروكسي، الباقي بـ ScraperAPI
            if attempt == 0:
                proxy = None
                print("🔄 بدون بروكسي")
            else:
                proxy = get_scraper_proxy()
                print("🔄 ScraperAPI proxy")

            token = solve_turnstile("0x4AAAAAACE-XLGoQUckKKm_", "https://image-editor.org/")
            if not token:
                continue
            user_uuid = str(uuid.uuid4())
            req_kwargs = {"headers": IMAGE_HEADERS, "timeout": 30, "verify": False}
            if proxy:
                req_kwargs["proxies"] = proxy

            r = requests.post("https://image-editor.org/api/generate", json={
                "prompt": prompt, "image_size": image_size,
                "turnstileToken": token, "userUUID": user_uuid
            }, **req_kwargs)
            print(f"Generate response: {r.text[:300]}")
            try:
                data = r.json()
            except ValueError:
                print("❌ Response not JSON, skipping")
                continue
            if not data.get("success"):
                continue
            task_data = data.get("data", {})
            task_id = task_data.get("taskId")
            if task_data.get("status") == "completed" and task_data.get("result"):
                return task_data["result"][0]
            if not task_id:
                continue
            result_url = wait_for_task(task_id, proxy)
            if result_url:
                return result_url
        except Exception as e:
            print(f"❌ Image Error: {e}")
    return None

# ========== NANOBANANA IMAGE ==========
# ========== VEO3AI IMAGE LOGIN ==========
VEO3_BASE = "https://www.veo3ai.io"
MAIL_GW_URL = "https://api.mail.gw"

def veo3_image_login(max_retries=2):
    """تسجيل دخول لـ veo3ai.io للصور"""
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    for attempt in range(max_retries):
        try:
            session = make_scraper_session({
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "content-type": "application/json",
                "origin": VEO3_BASE,
                "referer": f"{VEO3_BASE}/text-to-image",
            })

            print(f"📧 إنشاء إيميل (محاولة {attempt+1})...")
            r = requests.get(f"{MAIL_GW_URL}/domains", timeout=15, verify=False)
            domains = r.json().get("hydra:member", [])
            if not domains: continue
            email = f"{_rand(10)}@{random.choice(domains)['domain']}"
            pwd = "Pass1234!"
            requests.post(f"{MAIL_GW_URL}/accounts", json={"address": email, "password": pwd}, timeout=15, verify=False)
            tok_r = requests.post(f"{MAIL_GW_URL}/token", json={"address": email, "password": pwd}, timeout=15, verify=False)
            mail_token = tok_r.json().get("token")
            if not mail_token: continue
            print(f"✅ إيميل: {email}")

            token = solve_turnstile("0x4AAAAAABwzqT6AqNwHJZWq", VEO3_BASE)
            if not token: continue

            session.post(f"{VEO3_BASE}/api/auth/signup", json={
                "name": _rand(8), "email": email, "password": pwd, "captchaToken": token
            }, timeout=20)

            # انتظر رابط التفعيل (mail.gw بدون بروكسي)
            mail_headers = {"Authorization": f"Bearer {mail_token}"}
            verify_link = None
            for _ in range(30):
                msgs = requests.get(f"{MAIL_GW_URL}/messages", headers=mail_headers, timeout=10, verify=False).json().get("hydra:member", [])
                if msgs:
                    msg = requests.get(f"{MAIL_GW_URL}/messages/{msgs[0]['id']}", headers=mail_headers, timeout=10, verify=False).json()
                    m = re.search(r"(https://rjmeqtivlxgtconwkcmm\.supabase\.co/auth/v1/verify\?[^\s\"'\\]+)", str(msg))
                    if m:
                        verify_link = m.group(1)
                        break
                time.sleep(3)

            if not verify_link:
                print("❌ لم يصل رابط التفعيل")
                continue

            session.get(verify_link, allow_redirects=True, timeout=20)
            print("✅ تم التفعيل!")

            csrf = session.get(f"{VEO3_BASE}/api/auth/csrf", timeout=30).json().get("csrfToken")
            session.post(f"{VEO3_BASE}/api/auth/email-signin", json={"email": email, "password": pwd}, timeout=30)
            session.post(f"{VEO3_BASE}/api/auth/callback/email", data={
                "email": email, "password": pwd, "redirect": "false",
                "csrfToken": csrf, "callbackUrl": VEO3_BASE
            }, headers={"x-auth-return-redirect": "1", "content-type": "application/x-www-form-urlencoded"}, timeout=30)

            sess_data = session.get(f"{VEO3_BASE}/api/auth/session", timeout=30).json()
            if not sess_data.get("user"):
                print("❌ فشل تأكيد الجلسة")
                continue

            cookie_str = "; ".join([f"{k}={v}" for k, v in session.cookies.items()])
            session.headers.update({"Cookie": cookie_str})
            print(f"✅ Logged in: {sess_data['user']['email']}")
            pass  # no session cache
            return session, cookie_str

        except Exception as e:
            print(f"❌ veo3_image_login error (attempt {attempt+1}): {e}")
    return None, None

def veo3_upload_image(cookie_str, image_bytes):
    """رفع صورة على veo3ai.io وإرجاع الـ publicUrl"""
    try:
        filename = f"{uuid.uuid4()}.jpg"
        file_size = len(image_bytes)
        headers = {"User-Agent": "Mozilla/5.0", "Cookie": cookie_str, "Content-Type": "application/json"}

        r = requests.post(f"{VEO3_BASE}/api/upload/presign", headers=headers, json={
            "filename": filename, "contentType": "image/jpeg", "fileSize": file_size
        }, timeout=20)
        data = r.json()
        if data.get("code") != 0:
            print(f"❌ Presign failed: {data}")
            return None

        up_url = data["data"].get("presignedUrl")
        pub_url = data["data"].get("publicUrl")
        if not up_url or not pub_url: return None

        put_r = requests.put(up_url, data=image_bytes, headers={"Content-Type": "image/jpeg"}, timeout=60)
        if put_r.status_code in (200, 204):
            print(f"✅ Image uploaded: {pub_url[:60]}...")
            return pub_url
        else:
            print(f"❌ PUT failed: {put_r.status_code}")
    except Exception as e:
        print(f"❌ Upload error: {e}")
    return None

def _veo3_poll_image(task_id, session_or_headers, timeout=300):
    """انتظار نتيجة مهمة صورة من veo3ai.io"""
    start = time.time()
    body = json.dumps({"id": task_id})
    hdrs = {"Content-Type": "application/json"}
    while time.time() - start < timeout:
        time.sleep(5)
        try:
            if isinstance(session_or_headers, dict):
                r = requests.post(f"{VEO3_BASE}/api/image-generation/status",
                                  data=body, headers={**session_or_headers, **hdrs}, timeout=30)
            else:
                r = session_or_headers.post(f"{VEO3_BASE}/api/image-generation/status",
                                            data=body, headers=hdrs, timeout=30)
            if not r.text.strip():
                print("⚠️ Poll empty response, retrying...")
                continue
            data = r.json()
            if data.get("code") == 0:
                st = data["data"].get("status", "")
                print(f"   ⏳ {st}...")
                if st in ("COMPLETED", "SAVED_TO_R2", "completed"):
                    return (data["data"].get("image_url") or data["data"].get("url")
                            or data["data"].get("image_url_r2"))
                elif st in ("FAILED", "failed", "ERROR"):
                    print(f"❌ Task failed: {data['data'].get('error_message')}")
                    return None
            else:
                print(f"⚠️ Poll response: {data}")
        except Exception as e:
            print(f"⚠️ Poll error: {e}")
            # استمر ولا توقف - ممكن البروكسي انقطع لحظياً
    print("❌ Timeout")
    return None

SITE       = "fluxproweb.com"
BASE_URL   = f"https://{SITE}/ar/model/nano-banana-pro-ai/"
API        = "https://api2.tap4.ai"
MAIL_API   = "https://api.mail.gw"
ACTION_REG = "424401cbe4e8b1b79045e4ac3dcf3d788c2156dd"
ACTION_VER = "efbaa6169049c8cb5fd4fd1abe810d880738ab19"
ACTION_LOG = "1c7778f900ce2db3f2c455a90e709ef29ae30db3"
ROUTER     = "%5B%22%22%2C%7B%22children%22%3A%5B%5B%22locale%22%2C%22ar%22%2C%22d%22%5D%2C%7B%22children%22%3A%5B%22(with-footer)%22%2C%7B%22children%22%3A%5B%22(templates)%22%2C%7B%22children%22%3A%5B%22model%22%2C%7B%22children%22%3A%5B%22nano-banana-pro-ai%22%2C%7B%22children%22%3A%5B%22__PAGE__%22%2C%7B%7D%2Cnull%2Cnull%5D%7D%2Cnull%2Cnull%5D%7D%2Cnull%2Cnull%5D%7D%2Cnull%2Cnull%5D%7D%2Cnull%2Cnull%5D%7D%2Cnull%2Cnull%2Ctrue%5D%7D%2Cnull%2Cnull%5D"
HEADERS = {
    "User-Agent":         "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Mobile Safari/537.36",
    "sec-ch-ua":          '"Not(A:Brand";v="8", "Chromium";v="144", "Brave";v="144"',
    "sec-ch-ua-mobile":   "?1",
    "sec-ch-ua-platform": '"Android"',
    "sec-gpc":            "1",
    "accept-language":    "ar-EG,ar;q=0.5",
    "origin":             f"https://{SITE}",
    "referer":            BASE_URL,
}

def get_account():
    r       = requests.get(f"{MAIL_API}/domains", timeout=10)
    domains = [d["domain"] for d in r.json().get("hydra:member", [])]
    for domain in domains:
        try:
            username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
            email    = f"{username}@{domain}"
            password = "Pass" + ''.join(random.choices(string.digits, k=8))
            r2 = requests.post(f"{MAIL_API}/accounts", json={"address": email, "password": password}, timeout=10)
            if r2.status_code not in (200, 201): continue
            r3 = requests.post(f"{MAIL_API}/token",    json={"address": email, "password": password}, timeout=10)
            if r3.status_code != 200: continue
            mail_token = r3.json()["token"]
            if try_register(email, password):
                return email, mail_token, password
        except:
            continue
    raise Exception("فشل إنشاء حساب")

def try_register(email, password):
    try:
        nickname = ''.join(random.choices(string.ascii_letters, k=8))
        hdrs     = {**HEADERS, "Accept": "text/x-component", "Content-Type": "text/plain;charset=UTF-8",
                    "next-action": ACTION_REG, "next-router-state-tree": ROUTER}
        r        = requests.post(BASE_URL, data=json.dumps([{"email": email, "userName": nickname, "password": password}]),
                                 headers=hdrs, timeout=15)
        print(f"register raw: {r.text[:100]}")
        m = re.search(r'1:\{"code":(\d+)', r.text)
        return m and int(m.group(1)) == 200
    except Exception as e:
        print(f"try_register error: {e}")
        return False

def wait_otp(mail_token):
    hdrs = {"Authorization": f"Bearer {mail_token}"}
    for _ in range(30):
        time.sleep(5)
        r    = requests.get(f"{MAIL_API}/messages", headers=hdrs)
        msgs = r.json().get("hydra:member", [])
        if msgs:
            r2   = requests.get(f"{MAIL_API}/messages/{msgs[0]['id']}", headers=hdrs)
            msg  = r2.json()
            text = msg.get("text", "") or ""
            html = msg.get("html", "") or ""
            if isinstance(text, list): text = " ".join(text)
            if isinstance(html, list): html = " ".join(html)
            m = re.search(r'\b(\d{6})\b', text + html)
            if m: return m.group(1)
    raise Exception("OTP لم يصل")

def verify_otp(email, otp):
    hdrs = {**HEADERS, "Accept": "text/x-component", "Content-Type": "text/plain;charset=UTF-8",
            "next-action": ACTION_VER, "next-router-state-tree": ROUTER}
    requests.post(BASE_URL, data=json.dumps([{"email": email, "emailCode": otp}]),
                  headers=hdrs, timeout=15)

def login(email, password):
    try:
        hdrs = {**HEADERS, "Accept": "text/x-component", "Content-Type": "text/plain;charset=UTF-8",
                "next-action": ACTION_LOG, "next-router-state-tree": ROUTER}
        r = requests.post(BASE_URL, data=json.dumps([{"email": email, "password": password}]),
                          headers=hdrs, timeout=15)
        print(f"login raw: {r.text[:200]}")
        full = r.text + r.headers.get("set-cookie", "")
        for pattern in [
            r'"access_token":"([^"]+)"',
            r'"token":"([^"]+)"',
            r'Authorization=Bearer%20([^;%&]+)',
            r'Bearer ([A-Za-z0-9_\-\.]+)',
            r'access_token=([^;& ]+)',
        ]:
            m = re.search(pattern, full)
            if m:
                tok = m.group(1)
                if len(tok) > 10:
                    print(f"✅ got token: {tok[:30]}...")
                    return tok
        raise Exception(f"مفيش token في الرد: {r.text[:200]}")
    except Exception as e:
        raise Exception(f"فشل تسجيل الدخول: {e}")

def flux_generate(prompt, model="nb", image_urls=None, status_cb=None):
    def s(step, txt):
        if status_cb: status_cb(step, txt)

    s(1, "🔐 إنشاء حساب...")
    email, mail_token, password = get_account()

    s(2, "📬 انتظار OTP...")
    otp   = wait_otp(mail_token)
    verify_otp(email, otp)
    token = login(email, password)

    s(3, "🎨 إرسال الطلب...")
    hdrs = {
        **HEADERS,
        "Content-Type":     "application/json",
        "authorization":    f"Bearer {token}",
        "credentials":      "include",
        "content-language": "en",
        "sec-fetch-site":   "cross-site",
        "sec-fetch-mode":   "cors",
        "sec-fetch-dest":   "empty",
        "referer":          f"https://{SITE}/",
    }

    if model == "nbp":
        # Nano Banana Pro
        payload = {
            "site":         SITE,
            "imageType":    "nano-banana-pro-image",
            "platformType": 39,
            "modelName":    "gemini-3-pro-image-preview",
            "isPublic":     1,
            "prompt":       prompt,
            "outputPrompt": prompt,
            "resolution":   "4k",
            "width": 1, "height": 1, "ratio": "1:1",
            "supportRatio": True,
            "nsfwFilter":   True,
        }
    else:
        # Nano Banana
        payload = {
            "site":         SITE,
            "platformType": 44,
            "modelName":    "gemini-25-flash-image",
            "isTranslate":  True,
            "isPublic":     1,
            "prompt":       prompt,
            "outputPrompt": prompt,
            "width": 1, "height": 1, "ratio": "1:1",
            "supportRatio": True,
            "nsfwFilter":   True,
        }

    if image_urls:
        payload["imageUrlList"] = image_urls
    if image_urls:
        payload["imageUrlList"] = image_urls

    print(f"payload: {json.dumps(payload)}")
    r   = requests.post(f"{API}/image/generator4login/async", data=json.dumps(payload), headers=hdrs)
    print(f"gen raw: {r.text[:300]}")
    print(f"gen status: {r.status_code}")
    rj = r.json()
    if not rj.get("data"):
        raise Exception(f"generate failed: {r.text[:200]}")
    key = rj["data"]["key"]

    s(4, "🖼 جاري التوليد...")
    for i in range(60):
        time.sleep(4)
        r2   = requests.get(f"{API}/image/getResult/{key}?site={SITE}", headers=hdrs)
        item = r2.json().get("data", {})
        if item.get("status") in ("success", "finish", "done", "completed"):
            vo  = item.get("imageResponseVo", {})
            url = vo.get("url") or (vo.get("images", [{}])[0].get("url"))
            if url: return url
        if status_cb and i % 3 == 0:
            s(4, f"🖼 جاري التوليد... {(i+1)*4}s")
    raise Exception("انتهت المهلة")


def generate_image(prompt, image_size="1:1", max_retries=2):
    for attempt in range(max_retries):
        try:
            return flux_generate(prompt)
        except Exception as e:
            print(f"generate_image attempt {attempt+1} error: {e}")
    return None

def nanobanana_generate(prompt, image_bytes=None, image_size="1:1", output_format="png", mime="image/jpeg"):
    image_urls = None
    if image_bytes:
        import base64 as _b
        b64 = _b.b64encode(image_bytes).decode()
        image_urls = [f"data:{mime};base64,{b64}"]
    for attempt in range(2):
        try:
            return flux_generate(prompt, image_urls=image_urls)
        except Exception as e:
            print(f"nanobanana_generate attempt {attempt+1} error: {e}")
    return None

def nanobanana_image_to_image(image_bytes_list, prompt, model="nano-banana-pro"):
    """تعديل/دمج صور عبر veo3ai.io"""
    for attempt in range(2):
        try:
            session, cookie_str = veo3_image_login()
            if not session: continue

            # رفع كل الصور
            public_urls = []
            for img_bytes in image_bytes_list:
                url = veo3_upload_image(cookie_str, img_bytes)
                if not url: break
                public_urls.append(url)
            if len(public_urls) != len(image_bytes_list):
                print("❌ فشل رفع الصور")
                continue
            print(f"📤 Uploaded {len(public_urls)} images")

            token = solve_turnstile("0x4AAAAAABwzqT6AqNwHJZWq", VEO3_BASE)
            if not token: continue

            payload = {
                "prompt": prompt, "model": "nano-banana-pro", "mode": "image-edit",
                "image_urls": public_urls, "enable_prompt_enhancement": False,
                "output_format": "png", "aspect_ratio": "1:1", "resolution": "4K",
                "image_input": public_urls, "agent_mode": False, "captchaToken": token
            }
            r = session.post(f"{VEO3_BASE}/api/image-generation/submit",
                             data=json.dumps(payload),
                             headers={"Content-Type": "application/json"},
                             timeout=30)
            data = r.json()
            if data.get("code") != 0:
                print(f"❌ Submit failed (attempt {attempt+1}): {data}")
                continue
            task_id = data["data"]["id"]
            print(f"🎨 i2i Task: {task_id}")
            result = _veo3_poll_image(task_id, session)
            if result: return result
        except Exception as e:
            print(f"❌ nanobanana_image_to_image error (attempt {attempt+1}): {e}")
    return None


# ========== EDIT IMAGE ==========
def edit_image(image_bytes, prompt, image_size="1:1", max_retries=3):
    for attempt in range(max_retries):
        print(f"\n✏️ بدء محاولة التعديل رقم {attempt + 1}/{max_retries}")
        try:
            # المحاولة الأولى بدون بروكسي، الباقي بـ ScraperAPI
            if attempt == 0:
                proxy = None
                print("🔄 بدون بروكسي")
            else:
                proxy = get_scraper_proxy()
                print("🔄 ScraperAPI proxy")
            import urllib3; urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            image_hash = hashlib.sha256(image_bytes).hexdigest()
            user_uuid = str(uuid.uuid4())
            filename = f"{image_hash}.jpg"
            req_kwargs = {"headers": IMAGE_HEADERS, "timeout": 30, "verify": False}
            if proxy: req_kwargs["proxies"] = proxy
            r = requests.post("https://image-editor.org/api/upload/presigned", json={
                "filename": filename, "contentType": "image/jpeg"
            }, **req_kwargs)
            try:
                data = r.json()
            except ValueError:
                continue
            if not data.get("success"):
                continue
            upload_url = data["data"]["uploadUrl"]
            file_url = data["data"]["fileUrl"]
            upload_id = data["data"]["uploadId"]
            put_kwargs = {"data": image_bytes, "headers": {
                "Content-Type": "image/jpeg",
                "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36",
            }, "timeout": 60, "verify": False}
            if proxy: put_kwargs["proxies"] = proxy
            r = requests.put(upload_url, **put_kwargs)
            if r.status_code not in (200, 204):
                continue
            token = solve_turnstile("0x4AAAAAACE-XLGoQUckKKm_", "https://image-editor.org/")
            if not token:
                continue
            edit_kwargs = {"headers": {**IMAGE_HEADERS, "referer": "https://image-editor.org/editor"}, "timeout": 30, "verify": False}
            if proxy: edit_kwargs["proxies"] = proxy
            r = requests.post("https://image-editor.org/api/edit", json={
                "prompt": prompt, "image_urls": [file_url], "image_size": image_size,
                "turnstileToken": token, "uploadIds": [upload_id],
                "userUUID": user_uuid, "imageHash": image_hash
            }, **edit_kwargs)
            try:
                data = r.json()
            except ValueError:
                continue
            if not data.get("success"):
                continue
            task_data = data.get("data", {})
            task_id = task_data.get("taskId")
            if task_data.get("status") == "completed" and task_data.get("result"):
                return task_data["result"][0]
            if not task_id:
                continue
            result_url = wait_for_task(task_id, proxy)
            if result_url:
                return result_url
        except Exception as e:
            print(f"❌ Edit Error: {e}")
    return None

# ========== VIDEO ==========
def create_mail():
    r = requests.get(f"{MAIL_URL}/domains")
    domain = r.json()["hydra:member"][0]["domain"]
    email = f"{_rand(10)}@{domain}"
    pwd = "Pass1234!"
    requests.post(f"{MAIL_URL}/accounts", json={"address": email, "password": pwd})
    r = requests.post(f"{MAIL_URL}/token", json={"address": email, "password": pwd})
    mail_token = r.json().get("token")
    return email, mail_token

def get_verify_link(mail_token, timeout=90):
    headers = {"Authorization": f"Bearer {mail_token}"}
    start = time.time()
    while time.time() - start < timeout:
        r = requests.get(f"{MAIL_URL}/messages", headers=headers)
        msgs = r.json().get("hydra:member", [])
        if msgs:
            r = requests.get(f"{MAIL_URL}/messages/{msgs[0]['id']}", headers=headers)
            text = str(r.json())
            m = re.search(r"(https://rjmeqtivlxgtconwkcmm\.supabase\.co/auth/v1/verify\?[^\s\"'\\]+)", text)
            if m:
                return m.group(1)
        time.sleep(5)
    return None

def veo3_login(referer_page="text-to-video"):
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    cache_key = "veo3_img2vid" if "image" in referer_page else "veo3_video"
    
    try:
        BASE = "https://www.veo3ai.io"
        session = make_scraper_session({
            "User-Agent": "Mozilla/5.0 (Linux; Android 11; RMX2180) AppleWebKit/537.36",
            "content-type": "application/json",
            "origin": BASE,
            "referer": f"{BASE}/{referer_page}",
        })
        email, mail_token = create_mail()
        print(f"📧 Email: {email}")
        token = solve_turnstile("0x4AAAAAABwzqT6AqNwHJZWq", BASE)
        if not token:
            return None, None
        pwd = "Pass1234!"
        r = session.post(f"{BASE}/api/auth/signup", json={
            "name": _rand(8), "email": email, "password": pwd, "captchaToken": token
        })
        print(f"Signup: {r.text[:100]}")
        verify_link = get_verify_link(mail_token)
        if not verify_link:
            return None, None
        session.get(verify_link, allow_redirects=True)
        print("✅ Verified!")
        r = session.get(f"{BASE}/api/auth/csrf")
        csrf = r.json().get("csrfToken")
        session.post(f"{BASE}/api/auth/email-signin", json={"email": email, "password": pwd})
        session.post(f"{BASE}/api/auth/callback/email",
                     data={"email": email, "password": pwd, "redirect": "false",
                           "csrfToken": csrf, "callbackUrl": f"{BASE}/{referer_page}"},
                     headers={"x-auth-return-redirect": "1",
                              "content-type": "application/x-www-form-urlencoded"})
        session_token = session.cookies.get("__Secure-authjs.session-token")
        if not session_token:
            return None, None
        auth = make_scraper_session({
            "User-Agent": "Mozilla/5.0 (Linux; Android 11; RMX2180) AppleWebKit/537.36",
            "content-type": "application/json",
            "origin": BASE,
            "referer": f"{BASE}/{referer_page}",
        })
        auth.cookies.set("__Secure-authjs.session-token", session_token, domain="www.veo3ai.io")
        print("✅ Logged in!")
        return auth, None
    except Exception as e:
        print(f"❌ Login error: {e}")
    return None, None

def generate_video(prompt, duration="8", aspect_ratio="16:9", max_retries=2):
    # تأكد إن duration رقم صح
    try:
        duration = int(duration) if duration is not None else 8
    except (ValueError, TypeError):
        duration = 8
    for attempt in range(max_retries):
        print(f"\n🎬 بدء محاولة توليد الفيديو رقم {attempt + 1}/{max_retries}")
        try:
            BASE = "https://www.veo3ai.io"
            session, proxy = veo3_login("text-to-video")
            if not session:
                continue
            token = solve_turnstile("0x4AAAAAABwzqT6AqNwHJZWq", BASE)
            if not token:
                continue
            enhanced_prompt = f"""You are a creative video director.
Create a cinematic, high-quality video based on this description: {prompt}
Style: Cinematic, detailed, realistic, high quality visuals.
If the description is in Arabic, translate it perfectly and create accordingly."""
            r = session.post(f"{BASE}/api/video-generation/submit",
                             data=json.dumps({
                                 "model": "kie-veo3-text-to-video",
                                 "prompt": enhanced_prompt,
                                 "duration": duration,
                                 "aspect_ratio": aspect_ratio,
                                 "resolution": "720p",
                                 "generate_audio": True,
                                 "enable_prompt_enhancement": False,
                                 "captchaToken": token,
                                 "watermarkEnabled": True
                             }), headers={"Content-Type": "application/json"}, timeout=30)
            if not r.text.strip():
                print("❌ Submit empty response"); continue
            data = r.json()
            video_id = data.get("data", {}).get("id")
            if not video_id:
                print(f"❌ Submit failed: {r.text[:150]}")
                continue
            print(f"🎬 Video ID: {video_id}")
            start = time.time()
            while time.time() - start < 300:
                try:
                    r = session.post(f"{BASE}/api/video-generation/status",
                                     data=json.dumps({"id": video_id}),
                                     headers={"Content-Type": "application/json"}, timeout=30)
                    if not r.text.strip():
                        time.sleep(8); continue
                    status_data = r.json().get("data", {})
                except Exception as poll_e:
                    print(f"⚠️ Video poll error: {poll_e}")
                    time.sleep(8); continue
                status = status_data.get("status")
                if status in ("COMPLETED", "SAVED_TO_R2"):
                    video_url = (status_data.get("video_url") or status_data.get("video_url_r2") or
                                 status_data.get("video_url_veo3") or status_data.get("video_url_fal"))
                    if video_url:
                        print("✅ Video done!")
                        return video_url
                elif status == "FAILED":
                    print(f"❌ Failed: {status_data.get('error_message')}")
                    break
                print(f"   ⏳ {status}...")
                time.sleep(8)
        except Exception as e:
            print(f"❌ Video error: {e}")
    return None

# ========== IMAGE TO VIDEO ==========
def upload_to_imgbb(image_bytes):
    try:
        b64 = base64.b64encode(image_bytes).decode("utf-8")
        r = requests.post("https://api.imgbb.com/1/upload", data={
            "key": IMGBB_KEY, "image": b64,
        })
        data = r.json()
        if data.get("success"):
            return data["data"]["url"]
    except Exception as e:
        print(f"❌ ImgBB error: {e}")
    return None

def generate_image_to_video(image_bytes, prompt):
    try:
        BASE = "https://www.veo3ai.io"
        print("📤 Uploading image to ImgBB...")
        image_url = upload_to_imgbb(image_bytes)
        if not image_url:
            return None
        print(f"✅ Image URL: {image_url}")
        session, proxy = veo3_login("image-to-video")
        if not session:
            return None
        token = solve_turnstile("0x4AAAAAABwzqT6AqNwHJZWq", BASE)
        if not token:
            return None
        r = session.post(f"{BASE}/api/video-generation/submit",
                         data=json.dumps({
                             "model": "kie-veo3-image-to-video",
                             "prompt": prompt,
                             "duration": 8,
                             "aspect_ratio": "Auto",
                             "resolution": "720p",
                             "generate_audio": True,
                             "enable_prompt_enhancement": False,
                             "image_url": image_url,
                             "image_urls": [image_url],
                             "captchaToken": token,
                             "watermarkEnabled": True
                         }), headers={"Content-Type": "application/json"}, timeout=30)
        print(f"Submit: {r.text[:150]}")
        video_id = r.json().get("data", {}).get("id")
        if not video_id:
            return None
        print(f"🎬 Video ID: {video_id}")
        start = time.time()
        while time.time() - start < 300:
            try:
                r = session.post(f"{BASE}/api/video-generation/status",
                                 data=json.dumps({"id": video_id}),
                                 headers={"Content-Type": "application/json"}, timeout=30)
                if not r.text.strip():
                    time.sleep(8); continue
                data = r.json().get("data", {})
            except Exception as pe:
                print(f"⚠️ i2v poll error: {pe}")
                time.sleep(8); continue
            status = data.get("status")
            print(f"   ⏳ {status}...")
            if status in ("COMPLETED", "SAVED_TO_R2"):
                return (data.get("video_url") or data.get("video_url_r2") or
                        data.get("video_url_veo3") or data.get("video_url_fal"))
            elif status == "FAILED":
                print(f"❌ Failed: {data.get('error_message')}")
                return None
            time.sleep(8)
    except Exception as e:
        print(f"❌ Image to video error: {e}")
    return None

# ========== MUSIC (aimu.1010diy.com) ==========
AIMU_BASE = "https://aimu.1010diy.com"

def generate_music(user_idea):
    try:
        KILWA_API = "https://moazjk-kilwa-music.hf.space/api"
        
        # Step 1: Submit idea and get track_id
        print(f"🎵 Submitting idea: {user_idea[:50]}...")
        resp = requests.post(f"{KILWA_API}/generate_idea", 
            json={"idea": user_idea},
            timeout=30
        ).json()
        
        track_id = resp.get("track_id")
        if not track_id:
            print(f"❌ Failed to submit idea: {resp}")
            return None
        
        print(f"🎵 Track ID: {track_id}")
        
        # Step 2: Poll status until success
        for attempt in range(60):
            time.sleep(5)
            try:
                status_resp = requests.get(f"{KILWA_API}/status/{track_id}", timeout=30).json()
                
                if status_resp.get("status") == "success":
                    print(f"✅ Music generated!")
                    return {
                        "title": status_resp.get("title", "AI Song"),
                        "lyrics": "",
                        "audio_url": status_resp.get("audio_url"),
                        "image_url": status_resp.get("image_url"),
                    }
                elif status_resp.get("status") == "failed":
                    print(f"❌ Generation failed")
                    break
                else:
                    print(f"⏳ Status: {status_resp.get('status')}")
            except Exception as e:
                print(f"❌ Poll error: {e}")
        
        print("❌ Timeout waiting for music generation")
    except Exception as e:
        print(f"❌ Music error: {e}")
    return None

def generate_music_from_lyrics(lyrics):
    try:
        KILWA_API = "https://moazjk-kilwa-music.hf.space/api"
        
        # Create idea from lyrics
        idea = f"أغنية بالكلمات التالية: {lyrics[:100]}"
        
        # Step 1: Submit idea and get track_id
        print(f"🎵 Submitting lyrics-based song...")
        resp = requests.post(f"{KILWA_API}/generate_idea", 
            json={"idea": idea},
            timeout=30
        ).json()
        
        if resp.get("message") != "تم استلام الطلب بنجاح، جاري التوليد":
            print(f"❌ Failed to submit: {resp}")
            return None
        
        track_id = resp.get("track_id")
        if not track_id:
            print(f"❌ No track_id returned: {resp}")
            return None
        
        print(f"🎵 Track ID: {track_id}")
        
        # Step 2: Poll status until success
        for attempt in range(60):
            time.sleep(5)
            try:
                status_resp = requests.get(f"{KILWA_API}/status/{track_id}", timeout=30).json()
                
                if status_resp.get("status") == "success":
                    print(f"✅ Music generated!")
                    return {
                        "title": status_resp.get("title", "My Song"),
                        "lyrics": lyrics,
                        "audio_url": status_resp.get("audio_url"),
                        "image_url": status_resp.get("image_url"),
                    }
                elif status_resp.get("status") == "failed":
                    print(f"❌ Generation failed")
                    break
                else:
                    print(f"⏳ Status: {status_resp.get('status')}")
            except Exception as e:
                print(f"❌ Poll error: {e}")
        
        print("❌ Timeout waiting for music generation")
    except Exception as e:
        print(f"❌ Music from lyrics error: {e}")
    return None



# ==================== KEYBOARDS ====================
def get_main_keyboard(lang="ar"):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(T(lang,"btn_edit"), callback_data="edit_select"),
         InlineKeyboardButton(T(lang,"btn_image"), callback_data="img_select")],
        [InlineKeyboardButton(T(lang,"btn_music"), callback_data="music_select")],
        [InlineKeyboardButton(T(lang,"btn_chat"), callback_data="chat_ai")],
        [InlineKeyboardButton(T(lang,"btn_points"), callback_data="collect_points"),
         InlineKeyboardButton(T(lang,"btn_account"), callback_data="my_account")],
        [InlineKeyboardButton(T(lang,"btn_shop"), callback_data="shop_menu"),
         InlineKeyboardButton(T(lang,"btn_support"), callback_data="support_menu")],
        [InlineKeyboardButton(T(lang,"btn_dev"), callback_data="dev_menu")],
    ])

def back_kb(lang="ar", cb="back_main"):
    return InlineKeyboardMarkup([[InlineKeyboardButton(T(lang,"back"), callback_data=cb)]])

def send_image_smart(chat_id, img_url, caption=""):
    """يبعت الصورة مع retry"""
    import io as _io
    img_data = None
    try:
        r = requests.get(img_url, timeout=60, headers={"User-Agent": "Mozilla/5.0"})
        r.raise_for_status()
        img_data = r.content
        print(f"✅ Downloaded image: {len(img_data)//1024}KB")
    except Exception as e:
        print(f"⚠️ Download failed: {e}")

    for attempt in range(3):
        try:
            if img_data:
                buf = _io.BytesIO(img_data); buf.name = "image.jpg"
                bot.send_photo(chat_id, buf, caption=caption)
            else:
                bot.send_photo(chat_id, img_url, caption=caption)
            return True
        except Exception as e:
            print(f"⚠️ send_photo attempt {attempt+1}: {e}")
            # لو send_photo فشل جرب document
            try:
                if img_data:
                    buf = _io.BytesIO(img_data); buf.name = "image.jpg"
                    bot.send_document(chat_id, buf, caption=caption)
                    return True
            except: pass
            time.sleep(2)
    # آخر حل: رابط
    try:
        kb = InlineKeyboardMarkup([[InlineKeyboardButton("🖼️ فتح الصورة", url=img_url)]])
        bot.send_message(chat_id, caption or "✅ تم!", reply_markup=kb)
    except Exception as e:
        print(f"⚠️ fallback failed: {e}")
    return False

def send_music_result(chat_id, result, caption, lang):
    """يبعت الأغنية مع الصورة كـ thumbnail داخل مشغل الصوت"""
    import io as _io
    audio_url = result.get("audio_url")
    image_url = result.get("image_url")
    title = result.get("title", "AI Song")

    # تحميل ملف الصوت
    audio_data = None
    try:
        r = requests.get(audio_url, timeout=120, headers={"User-Agent": "Mozilla/5.0"})
        r.raise_for_status()
        audio_data = r.content
        print(f"✅ Downloaded audio: {len(audio_data)//1024}KB")
    except Exception as e:
        print(f"⚠️ Audio download failed: {e}")

    # تحميل الصورة للـ thumbnail
    thumb_data = None
    if image_url:
        try:
            r = requests.get(image_url, timeout=30, headers={"User-Agent": "Mozilla/5.0"})
            r.raise_for_status()
            thumb_data = r.content
            print(f"✅ Downloaded thumbnail: {len(thumb_data)//1024}KB")
        except Exception as e:
            print(f"⚠️ Thumbnail download failed: {e}")

    # إرسال الصوت مع الـ thumbnail
    if audio_data:
        audio_buf = _io.BytesIO(audio_data)
        audio_buf.name = "song.mp3"
        thumb_buf = None
        if thumb_data:
            thumb_buf = _io.BytesIO(thumb_data)
            thumb_buf.name = "cover.jpg"
        try:
            bot.send_audio(chat_id, audio_buf, title=title, caption=caption, thumbnail=thumb_buf)
            return True
        except Exception as e:
            print(f"⚠️ send_audio with thumbnail failed: {e}")
            # محاولة بدون thumbnail
            try:
                audio_buf.seek(0)
                bot.send_audio(chat_id, audio_buf, title=title, caption=caption)
                return True
            except Exception as e2:
                print(f"⚠️ send_audio failed: {e2}")

    # آخر حل: رابط
    try:
        kb = InlineKeyboardMarkup([[InlineKeyboardButton(T(lang, "open_btn"), url=audio_url)]])
        bot.send_message(chat_id, caption, reply_markup=kb)
    except Exception as e:
        print(f"⚠️ Music fallback failed: {e}")
    return False


def _xo_keyboard(board, lang="ar"):
    symbols = {0: "⬜", 1: "❌", 2: "⭕"}
    rows = [[InlineKeyboardButton(symbols[board[i*3+j]], callback_data=f"xo_{i*3+j}" if board[i*3+j] == 0 else "noop") for j in range(3)] for i in range(3)]
    rows.append([InlineKeyboardButton(T(lang,"surrender"), callback_data="back_main")])
    return InlineKeyboardMarkup(rows)

def no_points_kb(lang="ar"):
    return InlineKeyboardMarkup([[
        InlineKeyboardButton(T(lang,"invite_collect"), callback_data="collect_points"),
        InlineKeyboardButton(T(lang,"buy_pts_btn"), callback_data="shop_menu"),
    ]])

# ==================== SUBSCRIPTION CHECK ====================
def check_subscription(user_id):
    if gs("force_sub", "0") != "1": return True
    conn = get_db()
    channels = conn.execute("SELECT * FROM channels WHERE is_active=1").fetchall()
    conn.close()
    if not channels: return True
    not_joined = []
    for ch in channels:
        try:
            cid = ch["channel_id"]
            if cid.startswith("https://t.me/"): cid = "@" + cid.replace("https://t.me/","").split("/")[0]
            elif cid.startswith("t.me/"): cid = "@" + cid.replace("t.me/","").split("/")[0]
            member = bot.get_chat_member(cid, user_id)
            if member.status in ["left", "kicked"]: not_joined.append(dict(ch))
        except: not_joined.append(dict(ch))
    return not_joined if not_joined else True

def send_sub_msg_direct(chat_id, not_joined, lang="ar"):
    keyboard = []
    for ch in not_joined:
        link = ch.get("invite_link") or ch.get("channel_id", "")
        name = ch.get("channel_name", "القناة")
        if link:
            keyboard.append([InlineKeyboardButton(f"➕ {name}", url=link)])
    keyboard.append([InlineKeyboardButton(
        "✅ تحققت من الاشتراك" if lang=="ar" else "✅ Check Subscription",
        callback_data="check_sub"
    )])
    text = T(lang,"sub_required") if lang else "يرجى الاشتراك في القنوات أولاً"
    try:
        bot.send_message(chat_id, text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")
    except Exception as e:
        print(f"send_sub_msg error: {e}")


# ==================== START ====================
@bot.message_handler(commands=["start"])
def start(msg):
    uid = msg.from_user.id
    username = msg.from_user.username or msg.from_user.first_name or str(uid)
    user = get_user(uid)
    ref = msg.text.split()[1] if len(msg.text.split()) > 1 else None
    invited_by = 0
    if ref and ref.isdigit():
        invited_by = int(ref)
        if invited_by == uid: invited_by = 0

    if not user:
        # مستخدم جديد - اختار لغة
        lang_kb = InlineKeyboardMarkup([[
            InlineKeyboardButton("🇸🇦 عربي", callback_data=f"newlang_ar_{invited_by}"),
            InlineKeyboardButton("🇬🇧 English", callback_data=f"newlang_en_{invited_by}"),
        ]])
        bot.send_message(uid, "🌍 اختر لغتك | Choose your language", reply_markup=lang_kb)
        return

    lang = user["lang"]
    if gs("bot_active","1") == "0" and uid != ADMIN_ID:
        bot.send_message(uid, T(lang,"maintenance")); return

    sub = check_subscription(uid)
    if sub is not True:
        send_sub_msg_direct(uid, sub, lang); return

    kb = get_main_keyboard(lang)
    wtype = gs("welcome_type","text")
    wmedia = gs("welcome_media","")
    welcome_txt = T(lang,"welcome")
    try:
        if wtype == "photo" and wmedia:
            bot.send_photo(uid, wmedia, caption=welcome_txt, reply_markup=kb)
        elif wtype == "sticker" and wmedia:
            bot.send_sticker(uid, wmedia)
            bot.send_message(uid, welcome_txt, reply_markup=kb)
        else:
            bot.send_message(uid, welcome_txt, reply_markup=kb)
    except Exception as e:
        print(f"start error: {e}")
        bot.send_message(uid, welcome_txt, reply_markup=kb)

# ==================== ADMIN ====================
def _admin_kb(*args):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📊 إحصائيات", callback_data="admin_stats"),
         InlineKeyboardButton("📢 بث رسالة", callback_data="admin_broadcast")],
        [InlineKeyboardButton("🎫 الأكواد", callback_data="admin_codes"),
         InlineKeyboardButton("👤 بحث مستخدم", callback_data="admin_search")],
        [InlineKeyboardButton("📡 القنوات", callback_data="admin_channels"),
         InlineKeyboardButton("⚙️ الإعدادات", callback_data="admin_settings")],
        [InlineKeyboardButton("📤 تصدير", callback_data="admin_export")],
    ])

@bot.message_handler(commands=["admin"])
def admin_cmd(msg):
    if msg.from_user.id != ADMIN_ID: return
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("📊 إحصائيات", callback_data="admin_stats"),
         InlineKeyboardButton("📢 بث رسالة", callback_data="admin_broadcast")],
        [InlineKeyboardButton("🎫 الأكواد", callback_data="admin_codes"),
         InlineKeyboardButton("👤 بحث مستخدم", callback_data="admin_search")],
        [InlineKeyboardButton("📡 القنوات", callback_data="admin_channels"),
         InlineKeyboardButton("⚙️ الإعدادات", callback_data="admin_settings")],
        [InlineKeyboardButton("📤 تصدير", callback_data="admin_export")],
    ])
    bot.send_message(msg.chat.id, "🔧 لوحة التحكم", reply_markup=kb)

# ==================== BUTTON HANDLER ====================
def safe_edit(call, text, **kwargs):
    """تعديل رسالة بأمان"""
    if not text or not str(text).strip():
        text = "‌"
    try:
        bot.edit_message_text(
            text, call.message.chat.id, call.message.message_id,
            parse_mode=kwargs.get("parse_mode","HTML"),
            reply_markup=kwargs.get("reply_markup")
        )
    except Exception as e:
        err = str(e).lower()
        if "message is not modified" in err or "query is too old" in err: return
        try:
            bot.send_message(
                call.message.chat.id, text,
                parse_mode=kwargs.get("parse_mode","HTML"),
                reply_markup=kwargs.get("reply_markup")
            )
        except Exception as e2:
            print(f"safe_edit failed: {e2}")

@bot.pre_checkout_query_handler(func=lambda query: True)
def process_pre_checkout_query(pre_checkout_query):
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

@bot.message_handler(content_types=["successful_payment"])
def handle_successful_payment(msg):
    uid = msg.from_user.id
    user = get_user(uid)
    if not user:
        bot.send_message(uid, "⚠️ سجل أولاً | Register first"); return
    lang = user["lang"]
    payment = msg.successful_payment
    
    if not payment.invoice_payload or not payment.invoice_payload.startswith("stars_pkg_"):
        bot.send_message(uid, "❌ خطأ في معرّف الشراء | Payment ID error"); return
    
    try:
        parts = payment.invoice_payload.split("_")
        pkg_idx = int(parts[2])
        pkg = SHOP_POINTS_PKGS[pkg_idx]
        points = pkg["points"]
        stars = payment.total_amount
        
        if stars != pkg["stars"]:
            bot.send_message(uid, f"⚠️ عدم تطابق المبلغ | Amount mismatch: expected {pkg['stars']}, got {stars}"); return
        
        add_points(uid, points)
        conn = get_db()
        conn.execute(
            "INSERT INTO star_transactions (user_id,invoice_payload,stars_amount,points_amount,status,created_at) VALUES (?,?,?,?,?,?)",
            (uid, payment.invoice_payload, stars, points, "completed", int(time.time()))
        )
        conn.commit(); conn.close()
        
        bot.send_message(uid, 
            f"✅ {T(lang,'stars_success')}\n\n"
            f"⭐ نجوم | Stars: {stars}\n"
            f"🎁 نقاط | Points: +{points}\n"
            f"💰 الرصيد | Balance: {get_user(uid)['points']}",
            parse_mode="HTML"
        )
    except Exception as e:
        print(f"❌ successful_payment error: {e}")
        bot.send_message(uid, f"❌ خطأ: {str(e)[:100]}")

@bot.callback_query_handler(func=lambda c: True)
def button_handler(call):
    query = call
    # answer فوراً قبل أي حاجة تانية (Telegram بيدي 10 ثواني بس)
    try:
        bot.answer_callback_query(call.id, )
    except Exception:
        pass  # لو انتهت صلاحيتها مش مشكلة، نكمل
    uid = call.from_user.id
    data = call.data
    user = get_user(uid)
    lang = user["lang"] if user else "ar"

    if gs("bot_active","1") == "0" and uid != ADMIN_ID:
        try: bot.answer_callback_query(call.id, T(lang,"maintenance"), show_alert=True)
        except: pass
        return

    # ===== كابتشا إيموجي =====
    if data.startswith("captcha_"):
        chosen_emoji = data.replace("captcha_", "")
        target = user_data.get(uid, {}).get('captcha_target')
        invited_by = user_data.get(uid, {}).get('captcha_invited_by', 0)
        if not target:
            bot.answer_callback_query(call.id, "⚠️ انتهت صلاحية الكابتشا، اضغط /start", show_alert=True); return
        if chosen_emoji == target:
            # ✅ صح - امسح الكابتشا وعرض اختيار اللغة
            user_data.get(uid, {}).pop('captcha_target', None)
            user_data.get(uid, {}).pop('captcha_invited_by', None)
            bot.answer_callback_query(call.id, "✅ صح!")
            lang_kb = InlineKeyboardMarkup([[
                InlineKeyboardButton("🇸🇦 عربي", callback_data=f"newlang_ar_{invited_by}"),
                InlineKeyboardButton("🇬🇧 English", callback_data=f"newlang_en_{invited_by}"),
            ]])
            safe_edit(call, "🌍 اختر لغتك | Choose your language", reply_markup=lang_kb)
        else:
            # ❌ غلط - كابتشا جديدة
            bot.answer_callback_query(call.id, "❌ غلط! حاول تاني", show_alert=True)
            target2, options2 = make_emoji_captcha()
            user_data.setdefault(uid, {})['captcha_target'] = target2
            keyboard2 = [[InlineKeyboardButton(e, callback_data=f"captcha_{e}") for e in options2]]
            safe_edit(call, 
                f"❌ إجابة خاطئة!\n\n🤖 حاول تاني، اضغط على:\n\n{target2}",
                reply_markup=InlineKeyboardMarkup(keyboard2)
            )
        return

    # ===== اختيار لغة المستخدم الجديد =====
    if data.startswith("newlang_"):
        parts = data.split("_")
        chosen_lang = parts[1]
        try: invited_by = int(parts[2])
        except: invited_by = 0
        username = call.from_user.username or call.from_user.first_name or str(uid)

        # فحص الاشتراك
        sub = check_subscription(uid)
        if sub is not True:
            # احفظ المستخدم مؤقتاً باللغة المختارة لعرض رسالة الاشتراك
            create_user(uid, username, chosen_lang, invited_by)
            send_sub_msg_direct(uid, sub, chosen_lang)
            return

        create_user(uid, username, chosen_lang, invited_by)

        if gs("notify_new_user","1") == "1":
            threading.Thread(target=lambda: notify_admin(T("ar","new_user", uid=uid, u=username), daemon=True).start())

        if invited_by:
            pts = int(gs("points_invite","2"))
            add_points(invited_by, pts)
            try: bot.send_message(invited_by, T("ar","inv_joined", u=username, pts=pts))
            except Exception as _e: print(f"⚠️ [LINE 1840] {type(_e).__name__}: {_e}")

        wtype = gs("welcome_type","text")
        wmedia = gs("welcome_media","")
        kb = get_main_keyboard(chosen_lang)
        welcome_txt = T(chosen_lang,"welcome")
        if wtype == "photo" and wmedia:
            try:
                bot.send_photo(uid, photo=wmedia, caption=welcome_txt, reply_markup=kb)
                bot.delete_message(call.message.chat.id, call.message.message_id)
            except Exception as _e:
                print(f"⚠️ [LINE 1850] {type(_e).__name__}: {_e}")
                safe_edit(call, welcome_txt, reply_markup=kb)
        elif wtype == "sticker" and wmedia:
            try:
                bot.send_sticker(uid, sticker=wmedia)
                bot.send_message(uid, welcome_txt, reply_markup=kb)
                bot.delete_message(call.message.chat.id, call.message.message_id)
            except Exception as _e:
                print(f"⚠️ [LINE 1857] {type(_e).__name__}: {_e}")
                safe_edit(call, welcome_txt, reply_markup=kb)
        else:
            safe_edit(call, welcome_txt, reply_markup=kb)
        return

    if not user:
        bot.answer_callback_query(call.id, "⚠️ سجّل أولاً", show_alert=True); return

    if user["is_banned"] and uid != ADMIN_ID:
        bot.answer_callback_query(call.id, T(lang,"banned"), show_alert=True); return

    # ===== اشتراك =====
    if data == "check_sub":
        sub = check_subscription(uid)
        if sub is True:
            safe_edit(call, T(lang,"welcome"), reply_markup=get_main_keyboard(lang))
        else:
            bot.answer_callback_query(call.id, T(lang,"sub_not_yet"), show_alert=True)
        return

    # ===== رجوع للقائمة الرئيسية - يعرض رسالة الترحيب دائماً =====
    if data == "back_main":
        user_data.setdefault(uid, {})['mode'] = None
        safe_edit(call, T(lang,"welcome"), reply_markup=get_main_keyboard(lang))
        return

    # ===== إنشاء صورة =====
    if data == "img_select":
        std = gs("points_nano_std","1"); pro = gs("points_nano_pro","2")
        safe_edit(call, T(lang,"img_choose"), reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(T(lang,"img_nano_std",n=std), callback_data="nano_standard")],
            [InlineKeyboardButton(T(lang,"img_nano_pro",n=pro), callback_data="nano_pro")],
            [InlineKeyboardButton(T(lang,"back"), callback_data="back_main")],
        ]))

    elif data in ("nano_pro","nano_standard"):
        cost = int(gs("points_nano_pro","2") if data=="nano_pro" else gs("points_nano_std","1"))
        if not has_points(uid, cost):
            safe_edit(call, T(lang,"no_pts",n=cost), reply_markup=no_points_kb(lang)); return
        nano_model = NANO_MODELS.get(data, "nano-banana-pro")
        user_data.setdefault(uid, {})["mode"] = "nano_image"
        user_data.setdefault(uid, {})["nano_model"] = nano_model
        user_data.setdefault(uid, {})["nano_cost"] = cost
        label = T(lang,"img_nano_pro",n=cost) if data=="nano_pro" else T(lang,"img_nano_std",n=cost)
        safe_edit(call, f"{label}\n\n{T(lang,'img_prompt')}")

    # ===== تعديل صورة =====
    elif data == "edit_select":
        std = gs("points_nano_std","1"); pro = gs("points_nano_pro","2")
        safe_edit(call, T(lang,"edit_choose"), reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(T(lang,"edit_std",n=std), callback_data="edit_standard")],
            [InlineKeyboardButton(T(lang,"edit_pro",n=pro), callback_data="edit_pro")],
            [InlineKeyboardButton(T(lang,"back"), callback_data="back_main")],
        ]))

    elif data == "edit_standard":
        cost = int(gs("points_nano_std","1"))
        if not has_points(uid, cost):
            safe_edit(call, T(lang,"no_pts",n=cost), reply_markup=no_points_kb(lang)); return
        user_data.setdefault(uid, {})["mode"] = "edit_wait_photo"
        user_data.setdefault(uid, {})["edit_cost"] = cost
        user_data.setdefault(uid, {})["edit_model"] = "nano_standard"
        safe_edit(call, T(lang,"edit_send_photo"))

    elif data == "edit_pro":
        cost = int(gs("points_nano_pro","2"))
        if not has_points(uid, cost):
            safe_edit(call, T(lang,"no_pts",n=cost), reply_markup=no_points_kb(lang)); return
        user_data.setdefault(uid, {})["mode"] = "edit_wait_photo"
        user_data.setdefault(uid, {})["edit_cost"] = cost
        user_data.setdefault(uid, {})["edit_model"] = "nano_pro"
        safe_edit(call, T(lang,"edit_pro_send"))

    # ===== فيديو =====
    elif data == "video_select":
        cost = int(gs("points_video","2"))
        if not has_points(uid, cost):
            safe_edit(call, T(lang,"no_pts",n=cost), reply_markup=no_points_kb(lang)); return
        safe_edit(call, T(lang,"vid_choose"), reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(T(lang,"vid_text"), callback_data="video_text")],
            [InlineKeyboardButton(T(lang,"vid_img"), callback_data="video_img")],
            [InlineKeyboardButton(T(lang,"back"), callback_data="back_main")],
        ]))

    elif data == "video_text":
        user_data.setdefault(uid, {})["mode"] = "video"
        user_data.setdefault(uid, {})["video_type"] = "text"
        safe_edit(call, T(lang,"vid_send_desc"))

    elif data == "video_img":
        user_data.setdefault(uid, {})["mode"] = "video_wait_photo"
        safe_edit(call, T(lang,"vid_send_photo"))

    # ===== موسيقى =====
    elif data == "music_select":
        cost = int(gs("points_music","2"))
        if not has_points(uid, cost):
            safe_edit(call, T(lang,"no_pts",n=cost), reply_markup=no_points_kb(lang)); return
        safe_edit(call, T(lang,"music_choose"), reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(T(lang,"music_idea_btn"), callback_data="music_idea")],
            [InlineKeyboardButton(T(lang,"music_lyrics_btn"), callback_data="music_lyrics_btn")],
            [InlineKeyboardButton(T(lang,"back"), callback_data="back_main")],
        ]))

    elif data == "music_idea":
        user_data.setdefault(uid, {})["mode"] = "music"
        safe_edit(call, T(lang,"music_idea_send"))

    elif data == "music_lyrics_btn":
        user_data.setdefault(uid, {})["mode"] = "music_lyrics"
        safe_edit(call, T(lang,"music_lyrics_send"))

    # ===== Chat AI =====
    elif data == "chat_ai":
        user_data.setdefault(uid, {})['mode'] = "chat_ai"
        user_data.setdefault(uid, {})['chat_history'] = []
        safe_edit(call, T(lang,"chat_title"), parse_mode="Markdown")

    elif data == "confirm_end_chat":
        user_data.setdefault(uid, {})['mode'] = None
        user_data.setdefault(uid, {})['chat_history'] = []
        user_data.setdefault(uid, {})['support_history'] = []
        safe_edit(call, T(lang,"welcome"), reply_markup=get_main_keyboard(lang))

    elif data == "dismiss_end_chat":
        bot.delete_message(call.message.chat.id, call.message.message_id)

    # ===== الألعاب =====
    elif data == "games_menu":
        u = get_user(uid)
        now = time.time()
        # حساب المحاولات المتبقية لكل لعبة
        def game_info(attempts_col, reset_col):
            attempts = int(u[attempts_col]) if u[attempts_col] else 0
            reset_time = int(u[reset_col]) if u[reset_col] else 0
            if now - reset_time >= 43200:
                attempts = 0
            return attempts, reset_time
        xo_att, xo_rt = game_info("xo_attempts","xo_reset_time")
        qz_att, qz_rt = game_info("quiz_attempts","quiz_reset_time")
        wd_att, wd_rt = game_info("word_attempts","word_reset_time")

        def tries_label(att):
            left = 3 - att
            if left <= 0:
                return "❌"
            return f"✅ {left}/3"

        title = "🎮 *الألعاب*\n\nاختر لعبة وابدأ!" if lang=="ar" else "🎮 *Games*\n\nChoose a game!"
        safe_edit(call, title, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(f"🎮 XO {tries_label(xo_att)}", callback_data="game_xo")],
            [InlineKeyboardButton(f"🧠 {'سؤال وجواب' if lang=='ar' else 'Quiz'} {tries_label(qz_att)}", callback_data="game_quiz")],
            [InlineKeyboardButton(f"🔤 {'أكمل الكلمة' if lang=='ar' else 'Complete Word'} {tries_label(wd_att)}", callback_data="game_word")],
            [InlineKeyboardButton(T(lang,"back"), callback_data="back_main")],
        ]))

    elif data == "game_xo":
        u = get_user(uid)
        now = time.time()
        reset_time = int(u["xo_reset_time"]) if u["xo_reset_time"] else 0
        if now - reset_time >= 43200:
            conn = get_db(); conn.execute("UPDATE users SET xo_attempts=0, xo_reset_time=? WHERE id=?", (int(now), uid)); conn.commit(); conn.close()
            reset_time = int(now); u = get_user(uid)
        attempts = int(u["xo_attempts"]) if u["xo_attempts"] else 0
        if attempts >= 3:
            remaining = max(0, int(43200 - (now - reset_time))); h, m = remaining // 3600, (remaining % 3600) // 60
            no_txt = f"❌ لا محاولات متبقية في XO\nتجدد بعد {h} ساعة و{m} دقيقة" if lang=="ar" else f"❌ No XO attempts left\nResets in {h}h {m}m"
            safe_edit(call, no_txt, reply_markup=back_kb(lang)); return
        pts_list = [4, 3, 2]; pts = pts_list[min(attempts, 2)]
        board = [0] * 9
        user_data.setdefault(uid, {})["xo_board"] = board
        user_data.setdefault(uid, {})["xo_pts"] = pts
        conn = get_db(); conn.execute("UPDATE users SET xo_attempts=xo_attempts+1 WHERE id=?", (uid,)); conn.commit(); conn.close()
        n_txt = "Attempt" if lang=="en" else "المحاولة"
        pts_txt = "pts" if lang=="en" else "نقاط"
        you_txt = "You" if lang=="en" else "أنت"
        xo_header = f"🎮 XO - {n_txt} {attempts+1}/3 | 🏆 {pts} {pts_txt}\n{you_txt} ❌ | AI ⭕\n"
        user_data.setdefault(uid, {})['xo_header'] = xo_header
        safe_edit(call, xo_header, reply_markup=_xo_keyboard(board, lang))

    elif data.startswith("xo_"):
        pos = int(data.split("_")[1])
        board = user_data.get(uid, {}).get('xo_board', [0]*9)
        if board[pos] != 0: bot.answer_callback_query(call.id, "❌", show_alert=True); return
        board[pos] = 1
        xo_header = user_data.get(uid, {}).get('xo_header', "🎮 XO\n")
        winner = check_xo_winner(board)
        if winner == 1:
            pts = user_data.get(uid, {}).get('xo_pts', 4)
            add_points(uid, pts)
            conn = get_db(); conn.execute("UPDATE users SET xo_attempts=3, xo_reset_time=? WHERE id=?", (int(time.time()), uid)); conn.commit(); conn.close()
            win_txt = f"🎉 {'فزت!' if lang=='ar' else 'You won!'} +{pts} {'نقاط' if lang=='ar' else 'pts'}"
            safe_edit(call, xo_header + win_txt, reply_markup=back_kb(lang)); return
        if winner == -1:
            draw_txt = "🤝 " + ("تعادل!" if lang=="ar" else "Draw!")
            safe_edit(call, xo_header + draw_txt, reply_markup=back_kb(lang)); return
        ai_pos = None  # removed.get('xo_diff', 65))
        if ai_pos >= 0: board[ai_pos] = 2
        user_data.setdefault(uid, {})['xo_board'] = board
        winner = check_xo_winner(board)
        if winner == 2:
            lost_txt = "😔 " + ("الذكاء الاصطناعي فاز!" if lang=="ar" else "AI won!")
            safe_edit(call, xo_header + lost_txt, reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(T(lang,"try_again"), callback_data="games_menu"), InlineKeyboardButton(T(lang,"back"), callback_data="back_main")]
            ])); return
        if winner == -1:
            draw_txt = "🤝 " + ("تعادل!" if lang=="ar" else "Draw!")
            safe_edit(call, xo_header + draw_txt, reply_markup=back_kb(lang)); return
        safe_edit(call, xo_header, reply_markup=_xo_keyboard(board, lang))

    elif data == "game_quiz":
        u = get_user(uid)
        now = time.time()
        reset_time = int(u["quiz_reset_time"]) if u["quiz_reset_time"] else 0
        if now - reset_time >= 43200:
            conn = get_db(); conn.execute("UPDATE users SET quiz_attempts=0, quiz_reset_time=? WHERE id=?", (int(now), uid)); conn.commit(); conn.close()
            reset_time = int(now); u = get_user(uid)
        attempts = int(u["quiz_attempts"]) if u["quiz_attempts"] else 0
        if attempts >= 3:
            remaining = max(0, int(43200 - (now - reset_time))); h, m = remaining // 3600, (remaining % 3600) // 60
            no_txt = f"❌ لا محاولات متبقية في السؤال\nتجدد بعد {h} ساعة و{m} دقيقة" if lang=="ar" else f"❌ No Quiz attempts left\nResets in {h}h {m}m"
            safe_edit(call, no_txt, reply_markup=back_kb(lang)); return
        pts_map = {0:4,1:3,2:2}; pts = pts_map[min(attempts,2)]
        diff_map = {0:"hard",1:"medium",2:"easy"}; diff = diff_map[min(attempts,2)]
        safe_edit(call, T(lang,"gen_question"))
        conn = get_db(); conn.execute("UPDATE users SET quiz_attempts=quiz_attempts+1 WHERE id=?", (uid,)); conn.commit(); conn.close()
        q = None  # removed
        if not q:
            conn = get_db(); conn.execute("UPDATE users SET quiz_attempts=quiz_attempts-1 WHERE id=?", (uid,)); conn.commit(); conn.close()
            safe_edit(call, T(lang,"fail_try"), reply_markup=back_kb(lang)); return
        user_data.setdefault(uid, {})["quiz_q"] = q
        kb = [[InlineKeyboardButton(f"{k}) {v}", callback_data=f"quiz_ans_{k}")] for k,v in q["options"].items()]
        kb.append([InlineKeyboardButton(T(lang,"back"), callback_data="back_main")])
        n_txt = "Attempt" if lang=="en" else "المحاولة"
        pts_txt = "pts" if lang=="en" else "نقاط"
        q_txt = f"🧠 {n_txt} {attempts+1}/3 | 🏆 {pts} {pts_txt}\n\n❓ {q['question']}"
        safe_edit(call, q_txt, reply_markup=InlineKeyboardMarkup(kb))

    elif data.startswith("quiz_ans_"):
        ans = data.split("_")[-1]
        correct = user_data.get(uid, {}).get('quiz_answer', "")
        pts = user_data.get(uid, {}).get('quiz_pts', 2)
        if ans == correct:
            add_points(uid, pts)
            conn = get_db(); conn.execute("UPDATE users SET quiz_attempts=3, quiz_reset_time=? WHERE id=?", (int(time.time()), uid)); conn.commit(); conn.close()
            safe_edit(call, T(lang,"game_won",pts=pts), reply_markup=back_kb(lang))
        else:
            opts = user_data.get(uid, {}).get('quiz_options', {})
            wrong_txt = T(lang,"game_wrong_q",ans=f"{correct}) {opts.get(correct,'')}")
            safe_edit(call, wrong_txt, reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(T(lang,"try_again"), callback_data="games_menu"),
                 InlineKeyboardButton(T(lang,"back"), callback_data="back_main")]
            ]))

    elif data == "game_word":
        u = get_user(uid)
        now = time.time()
        reset_time = int(u["word_reset_time"]) if u["word_reset_time"] else 0
        if now - reset_time >= 43200:
            conn = get_db(); conn.execute("UPDATE users SET word_attempts=0, word_reset_time=? WHERE id=?", (int(now), uid)); conn.commit(); conn.close()
            reset_time = int(now); u = get_user(uid)
        attempts = int(u["word_attempts"]) if u["word_attempts"] else 0
        if attempts >= 3:
            remaining = max(0, int(43200 - (now - reset_time))); h, m = remaining // 3600, (remaining % 3600) // 60
            no_txt = f"❌ لا محاولات متبقية في الكلمة\nتجدد بعد {h} ساعة و{m} دقيقة" if lang=="ar" else f"❌ No Word attempts left\nResets in {h}h {m}m"
            safe_edit(call, no_txt, reply_markup=back_kb(lang)); return
        pts_map = {0:4,1:3,2:2}; pts = pts_map[min(attempts,2)]
        diff_map = {0:"hard",1:"medium",2:"easy"}; diff = diff_map[min(attempts,2)]
        safe_edit(call, T(lang,"gen_question"))
        conn = get_db(); conn.execute("UPDATE users SET word_attempts=word_attempts+1 WHERE id=?", (uid,)); conn.commit(); conn.close()
        # تمرير الكلم المستخدمة لتجنب التكرار
        used_words = user_data.get(uid, {}).get('used_words', [])
        w = None  # removed
        if not w:
            conn = get_db(); conn.execute("UPDATE users SET word_attempts=word_attempts-1 WHERE id=?", (uid,)); conn.commit(); conn.close()
            safe_edit(call, T(lang,"fail_try"), reply_markup=back_kb(lang)); return
        # احفظ الكلمة في قائمة الكلم المستخدمة
        used_words.append(w["word"])
        user_data.setdefault(uid, {})['used_words'] = used_words[-20:]  # احتفظ بآخر 20 كلمة بس
        if not w:
            conn = get_db(); conn.execute("UPDATE users SET word_attempts=word_attempts-1 WHERE id=?", (uid,)); conn.commit(); conn.close()
            safe_edit(call, T(lang,"fail_try"), reply_markup=back_kb(lang)); return
        user_data.setdefault(uid, {})["word_q"] = w
        user_data.setdefault(uid, {})["mode"] = "word_game"
        n_txt = "Attempt" if lang=="en" else "المحاولة"
        pts_txt = "pts" if lang=="en" else "نقاط"
        type_txt = "Type the word:" if lang=="en" else "اكتب الكلمة:"
        word_q = f"🔤 {n_txt} {attempts+1}/3 | 🏆 {pts} {pts_txt}\n\n{w['display']}\n💡 {w['hint']}\n\n{type_txt}"
        safe_edit(call, word_q)

    # ===== حسابي =====
    elif data == "my_account":
        u = get_user(uid)
        if not u: return
        lv = get_level(u["total_points"])
        lv_name = lv["name_en"] if lang=="en" else lv["name_ar"]
        next_lv = next((l for l in LEVELS if l["min"] > lv["min"]), None)
        next_txt = (f"\n📈 {'To next level' if lang=='en' else 'للمستوى التالي'}: {next_lv['min']-u['total_points']} {'pts' if lang=='en' else 'نقطة'}" if next_lv else f"\n🏆 {'Max level!' if lang=='en' else 'أعلى مستوى!'}")

        # معلومات المستويات
        if lang == "en":
            levels_txt = (
                "\n━━━━━━━━━━━━━━\n"
                "🏆 <b>Levels:</b>\n"
                "🌱 Beginner: 0-19 pts | Basic features\n"
                "⭐ Pro: 20-49 pts | Daily +2 | Priority\n"
                "🔥 Legendary: 50+ pts | Daily +5 | Priority | Badge"
            )
        else:
            levels_txt = (
                "\n━━━━━━━━━━━━━━\n"
                "🏆 <b>المستويات:</b>\n"
                "🌱 مبتدئ: 0-19 نقطة | المميزات الأساسية\n"
                "⭐ محترف: 20-49 نقطة | هدية +2 | أولوية\n"
                "🔥 أسطوري: 50+ نقطة | هدية +5 | أولوية | بادج"
            )

        # أعلى 3 مستخدمين
        conn = get_db()
        top3 = conn.execute("SELECT id, username, total_points FROM users WHERE is_banned=0 ORDER BY total_points DESC LIMIT 3").fetchall()
        conn.close()
        medals = ["🥇","🥈","🥉"]
        top_lines = []
        for i, tu in enumerate(top3):
            t_lv = get_level(tu["total_points"])
            t_lv_name = t_lv["name_en"] if lang=="en" else t_lv["name_ar"]
            uname = f"@{tu['username']}" if tu["username"] else f"ID:{tu['id']}"
            top_lines.append(f"{medals[i]} {uname} | {t_lv['emoji']} {t_lv_name} | {tu['total_points']}")
        top_header = "\n━━━━━━━━━━━━━━\n" + ("<b>Top Users:</b>\n" if lang=="en" else "<b>أعلى المستخدمين:</b>\n")
        top_txt = top_header + "\n".join(top_lines) if top_lines else ""

        # بيانات الحساب
        if lang == "en":
            body = (
                f"🆔 ID: <code>{uid}</code>\n"
                f"⭐ Points: {u['points']}\n"
                f"📊 Total: {u['total_points']}\n"
                f"{lv['emoji']} Level: {lv_name}{next_txt}\n\n"
                f"🔗 Invites: {u['invites']}\n"
                f"🖼️ {u['total_images']} images | 🎬 {u['total_videos']} videos\n"
                f"🎵 {u['total_music']} songs | ✏️ {u['total_edits']} edits"
            )
        else:
            body = (
                f"🆔 ID: <code>{uid}</code>\n"
                f"⭐ النقاط: {u['points']}\n"
                f"📊 الإجمالي: {u['total_points']}\n"
                f"{lv['emoji']} المستوى: {lv_name}{next_txt}\n\n"
                f"🔗 دعوات: {u['invites']}\n"
                f"🖼️ {u['total_images']} صورة | 🎬 {u['total_videos']} فيديو\n"
                f"🎵 {u['total_music']} أغنية | ✏️ {u['total_edits']} تعديل"
            )

        title = "👤 <b>My Account</b>" if lang=="en" else "👤 <b>حسابي</b>"
        full_txt = f"{title}\n\n{body}{levels_txt}{top_txt}"
        change_lang_btn = "🌍 Change Language" if lang=="en" else "🌍 تغيير اللغة"
        safe_edit(call, full_txt, parse_mode="HTML", reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(change_lang_btn, callback_data="change_language")],
            [InlineKeyboardButton(T(lang,"back"), callback_data="back_main")],
        ]))

    elif data == "change_language":
        safe_edit(call, 
            "🌍 اختر لغتك | Choose your language",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("🇸🇦 عربي", callback_data="switch_lang_ar"),
                InlineKeyboardButton("🇬🇧 English", callback_data="switch_lang_en"),
            ]]))

    elif data in ("switch_lang_ar","switch_lang_en"):
        new_lang = data.split("_")[-1]
        conn = get_db(); conn.execute("UPDATE users SET lang=? WHERE id=?", (new_lang, uid)); conn.commit(); conn.close()
        lang = new_lang
        done_txt = "✅ تم تغيير اللغة إلى العربية!" if new_lang=="ar" else "✅ Language changed to English!"
        safe_edit(call, done_txt, reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(T(new_lang,"back"), callback_data="back_main")]
        ]))

    # ===== رابط الدعوة =====
    elif data in ("send_ref_link","collect_invite"):
        me = context.bot.get_me()
        ref_link = f"https://t.me/{me.username}?start=ref_{uid}"
        bot.answer_callback_query(call.id, "✅")
        bot.send_message(uid, T(lang,"ref_msg", link=ref_link, pts=int(gs("points_invite","2"))))

    # ===== تجميع نقاط =====
    elif data == "collect_points":
        u = get_user(uid)
        daily_pts = int(gs("points_daily","5")) + get_level(u["total_points"])["daily_bonus"]
        invite_pts = int(gs("points_invite","2"))
        # صف 1: هدية يومية + ألعاب
        if time.time() - (u["last_daily"] or 0) >= 86400:
            daily_btn = InlineKeyboardButton(T(lang,"daily_btn",pts=daily_pts), callback_data="daily_gift")
        else:
            remaining = int(86400 - (time.time() - u["last_daily"])); h, m = remaining//3600, (remaining%3600)//60
            daily_btn = InlineKeyboardButton(T(lang,"daily_wait",h=h,m=m), callback_data="noop")
        # صف 2: رابط الدعوة
        # صف 3: تحويل نقاط + كود نقاط
        kb = [
            [daily_btn, InlineKeyboardButton(T(lang,"games_btn"), callback_data="games_menu")],
            [InlineKeyboardButton(T(lang,"invite_btn",pts=invite_pts), callback_data="collect_invite")],
            [InlineKeyboardButton(T(lang,"transfer_btn"), callback_data="transfer_points"),
             InlineKeyboardButton(T(lang,"code_btn"), callback_data="use_code")],
            [InlineKeyboardButton(T(lang,"back"), callback_data="back_main")],
        ]
        safe_edit(call, T(lang,"collect_title",pts=u["points"]), parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(kb))

    elif data == "daily_gift":
        u = get_user(uid)
        if time.time() - (u["last_daily"] or 0) < 86400:
            bot.answer_callback_query(call.id, T(lang,"daily_claimed"), show_alert=True); return
        daily_pts = int(gs("points_daily","5")) + get_level(u["total_points"])["daily_bonus"]
        add_points(uid, daily_pts)
        conn = get_db(); conn.execute("UPDATE users SET last_daily=? WHERE id=?", (int(time.time()), uid)); conn.commit(); conn.close()
        safe_edit(call, T(lang,"daily_ok",pts=daily_pts,bal=get_user(uid)["points"]), reply_markup=back_kb(lang))

    elif data == "transfer_points":
        user_data.setdefault(uid, {})['mode'] = "transfer_step1"
        safe_edit(call, T(lang,"transfer_enter_id"))

    elif data == "use_code":
        user_data.setdefault(uid, {})['mode'] = "use_code"
        safe_edit(call, T(lang,"code_enter"))

    elif data == "noop":
        pass

    # ===== شراء نقاط =====
    elif data == "shop_menu":
        pkg_name = "name_en" if lang=="en" else "name_ar"
        kb = [[InlineKeyboardButton(T(lang,"shop_pkg",e=p["emoji"],n=p[pkg_name],p=p["points"],s=p["stars"]),
                                    callback_data=f"buy_stars_{i}")] for i,p in enumerate(SHOP_POINTS_PKGS)]
        kb.append([InlineKeyboardButton(T(lang,"back"), callback_data="back_main")])
        safe_edit(call, T(lang,"shop_title"), parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(kb))

    elif data.startswith("buy_stars_"):
        idx = int(data.split("_")[-1]); pkg = SHOP_POINTS_PKGS[idx]
        pkg_name = pkg["name_en"] if lang=="en" else pkg["name_ar"]
        payment_link = create_star_payment_link(idx)
        if payment_link:
            kb = [[InlineKeyboardButton(f"💫 {T(lang,'stars_buy_btn')}", url=payment_link)]]
            kb.append([InlineKeyboardButton(T(lang,"back"), callback_data="shop_menu")])
            safe_edit(call, 
                f"⭐ {pkg['emoji']} {pkg_name}\n\n💰 {pkg['stars']} نجوم / Stars | 🎁 {pkg['points']} نقطة / Points\n\n👇 اضغط الزر أدناه | Click button below 👇",
                parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(kb))
        else:
            safe_edit(call, "❌ خطأ في إنشاء الفاتورة | Invoice creation failed", reply_markup=back_kb(lang))

    # ===== قسم المبرمجين =====
    elif data == "dev_menu":
        f_name = "name_en" if lang=="en" else "name_ar"
        kb = [[InlineKeyboardButton(T(lang,"dev_file",e=f["emoji"],n=f[f_name],s=f["stars"]),
                                    callback_data=f"dev_file_{i}")] for i,f in enumerate(SHOP_FILES)]
        kb.append([InlineKeyboardButton(T(lang,"back"), callback_data="back_main")])
        safe_edit(call, T(lang,"dev_title"), parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(kb))

    elif data.startswith("dev_file_"):
        idx = int(data.split("_")[-1]); f = SHOP_FILES[idx]
        f_name = f["name_en"] if lang=="en" else f["name_ar"]
        f_desc = f["desc_en"] if lang=="en" else f["desc_ar"]
        safe_edit(call, 
            T(lang,"dev_detail",e=f["emoji"],n=f_name,d=f_desc,s=f["stars"],sup=SUPPORT_USERNAME,uid=uid),
            parse_mode="Markdown", reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(T(lang,"buy_btn"), url=f"https://t.me/{SUPPORT_USERNAME.replace('@','')}")],
                [InlineKeyboardButton(T(lang,"back"), callback_data="dev_menu")],
            ]))

    elif data.startswith("coupon_"):
        code = data.replace("coupon_", "")
        u = get_user(uid)
        if u["points"] >= 999999:
            bot.answer_callback_query(call.id, "❌ أنت بالفعل لديك 999999+ نقطة", show_alert=True); return
        conn = get_db()
        check = conn.execute("SELECT * FROM code_uses WHERE user_id=? AND code_id=(SELECT id FROM codes WHERE code=?)", (uid, code)).fetchone()
        if check:
            conn.close()
            bot.answer_callback_query(call.id, "❌ استخدمت هذا الكود من قبل!", show_alert=True); return
        code_row = conn.execute("SELECT * FROM codes WHERE code=?", (code,)).fetchone()
        if not code_row:
            conn.close()
            bot.answer_callback_query(call.id, "❌ كود خاطئ!", show_alert=True); return
        if code_row["expires_at"] and time.time() > code_row["expires_at"]:
            conn.close()
            bot.answer_callback_query(call.id, "❌ الكود منتهي الصلاحية!", show_alert=True); return
        if code_row["used"] >= code_row["max_uses"]:
            conn.close()
            bot.answer_callback_query(call.id, "❌ الكود استُنفد!", show_alert=True); return
        add_points(uid, code_row["points"])
        conn.execute("INSERT INTO code_uses (code_id,user_id,used_at) VALUES (?,?,?)", (code_row["id"], uid, int(time.time())))
        conn.execute("UPDATE codes SET used=used+1 WHERE id=?", (code_row["id"],))
        conn.commit(); conn.close()
        safe_edit(call, T(lang,"code_ok",pts=code_row["points"],bal=get_user(uid)["points"]), reply_markup=back_kb(lang))

    elif data == "support_menu":
        user_data.setdefault(uid, {})['mode'] = "support_chat"
        user_data.setdefault(uid, {})['support_history'] = []
        safe_edit(call, T(lang,"support_title"), parse_mode="Markdown")
    
    if data.startswith("admin") and uid == ADMIN_ID:
        handle_admin(call, data)

# ==================== ADMIN HANDLER ====================
def handle_admin(call, data):
    uid = call.from_user.id
    if data == "admin_menu":
        safe_edit(call, "أهلاً بيك يا معاذ في لوحة التحكم الخاصة بك ❤️", reply_markup=_admin_kb())

    elif data == "admin_toggle":
        new = "0" if gs("bot_active") == "1" else "1"
        ss("bot_active", new)
        safe_edit(call, "✅ تم التبديل", reply_markup=_admin_kb())

    elif data == "admin_stats":
        conn = get_db()
        total = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
        banned = conn.execute("SELECT COUNT(*) FROM users WHERE is_banned=1").fetchone()[0]
        today = int(time.time()) - 86400
        new_today = conn.execute("SELECT COUNT(*) FROM users WHERE joined_at>?", (today,)).fetchone()[0]
        ops = conn.execute("SELECT COUNT(*) FROM operations").fetchone()[0]
        conn.close()
        safe_edit(call, 
            f"📊 *الإحصائيات*\n\n👥 المستخدمون: {total}\n🚫 محظور: {banned}\n🆕 اليوم: {new_today}\n⚙️ العمليات: {ops}",
            parse_mode="Markdown", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙", callback_data="admin_menu")]]))

    elif data == "admin_broadcast":
        user_data.setdefault(uid, {})['admin_mode'] = "broadcast"
        safe_edit(call, "📢 أرسل رسالة الإذاعة:",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("❌ إلغاء", callback_data="admin_menu")]]))

    elif data == "admin_search":
        user_data.setdefault(uid, {})['admin_mode'] = "search_user"
        safe_edit(call, "👤 أرسل ID أو يوزرنيم:",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("❌ إلغاء", callback_data="admin_menu")]]))

    elif data == "admin_codes":
        conn = get_db()
        codes = conn.execute("SELECT * FROM codes ORDER BY created_at DESC LIMIT 10").fetchall()
        conn.close()
        txt = "🎟️ *الأكواد*\n\n"
        for c in codes:
            txt += f"`{c['code']}` | {c['points']}نق | {c['used']}/{c['max_uses']}\n"
        if not codes: txt += "لا توجد أكواد"
        safe_edit(call, txt, parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙", callback_data="admin_menu")]]))

    elif data == "admin_newcode":
        user_data.setdefault(uid, {})['admin_mode'] = "new_code_step1"
        safe_edit(call, "🎟️ *كود جديد - الخطوة 1/3*\n\nأرسل اسم الكود:", parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("❌ إلغاء", callback_data="admin_menu")]]))

    elif data == "admin_channels":
        conn = get_db(); chs = conn.execute("SELECT * FROM channels").fetchall(); conn.close()
        sub = "✅ مفعّل" if gs("force_sub") == "1" else "❌ معطّل"
        kb = [[InlineKeyboardButton(f"🗑️ {c['channel_name'] or c['invite_link']}", callback_data=f"del_ch_{c['id']}")] for c in chs]
        kb.append([InlineKeyboardButton("➕ أضف قناة", callback_data="add_channel")])
        kb.append([InlineKeyboardButton(f"الاشتراك الإجباري: {sub}", callback_data="toggle_sub")])
        kb.append([InlineKeyboardButton("🔙", callback_data="admin_menu")])
        safe_edit(call, "📣 *قنوات الاشتراك*", parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(kb))

    elif data == "add_channel":
        user_data.setdefault(uid, {})['admin_mode'] = "add_channel"
        safe_edit(call, "📣 أرسل رابط القناة:\n`https://t.me/CHANNEL`", parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("❌ إلغاء", callback_data="admin_channels")]]))

    elif data == "toggle_sub":
        new = "0" if gs("force_sub") == "1" else "1"
        ss("force_sub", new)
        bot.answer_callback_query(call.id, "✅ تم التبديل")
        handle_admin(query, context, "admin_channels")

    elif data.startswith("del_ch_"):
        cid = int(data.split("_")[-1])
        conn = get_db(); conn.execute("DELETE FROM channels WHERE id=?", (cid,)); conn.commit(); conn.close()
        bot.answer_callback_query(call.id, "✅ حُذفت")
        handle_admin(query, context, "admin_channels")

    elif data == "admin_settings":
        kb = [
            [InlineKeyboardButton("🖼️ تغيير رسالة الترحيب", callback_data="set_welcome_text")],
            [InlineKeyboardButton("📷 صورة ترحيب", callback_data="set_welcome_photo"),
             InlineKeyboardButton("🎭 ستيكر ترحيب", callback_data="set_welcome_sticker")],
            [InlineKeyboardButton("❌ إزالة الوسائط", callback_data="clear_welcome_media")],
        ]
        for s in ["ai_system_prompt","support_system","points_daily","points_invite",
                  "points_nano_std","points_nano_pro","points_video","points_music","waiting_text"]:
            kb.append([InlineKeyboardButton(f"⚙️ {s}", callback_data=f"edit_setting_{s}")])
        kb.append([InlineKeyboardButton("🗑️ حذف كل البيانات", callback_data="admin_reset_db")])
        kb.append([InlineKeyboardButton("🔙", callback_data="admin_menu")])
        safe_edit(call, "⚙️ *الإعدادات*", parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(kb))

    elif data == "admin_reset_db":
        safe_edit(call, 
            "⚠️ *تحذير!*\n\nهل أنت متأكد من حذف كل بيانات المستخدمين والنقاط؟\nهذا الإجراء لا يمكن التراجع عنه!",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("✅ نعم، احذف كل شيء", callback_data="confirm_reset_db")],
                [InlineKeyboardButton("❌ إلغاء", callback_data="admin_settings")],
            ]))

    elif data == "confirm_reset_db":
        conn = get_db()
        conn.execute("DELETE FROM users")
        conn.execute("DELETE FROM operations")
        conn.execute("DELETE FROM code_uses")
        conn.commit(); conn.close()
        safe_edit(call, "✅ *تم حذف كل بيانات المستخدمين والنقاط!*\nالبوت جاهز للبداية من الصفر.", parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙", callback_data="admin_menu")]]))

    elif data == "set_welcome_text":
        user_data.setdefault(uid, {})['admin_mode'] = "set_welcome_text"
        safe_edit(call, 
            "📝 أرسل رسالة الترحيب الجديدة:\n(تظهر للمستخدمين الجدد عند أول تشغيل)\n\nاستخدم \\n للسطر الجديد",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("❌ إلغاء", callback_data="admin_settings")]]))

    elif data == "set_welcome_photo":
        user_data.setdefault(uid, {})['admin_mode'] = "set_welcome_photo"
        safe_edit(call, 
            "📷 أرسل الصورة التي ستظهر في رسالة الترحيب:",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("❌ إلغاء", callback_data="admin_settings")]]))

    elif data == "set_welcome_sticker":
        user_data.setdefault(uid, {})['admin_mode'] = "set_welcome_sticker"
        safe_edit(call, 
            "🎭 أرسل الستيكر الذي سيظهر مع رسالة الترحيب:",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("❌ إلغاء", callback_data="admin_settings")]]))

    elif data == "clear_welcome_media":
        ss("welcome_type", "text"); ss("welcome_media", "")
        bot.answer_callback_query(call.id, "✅ تم حذف الوسائط - الترحيب بالنص فقط")

    elif data.startswith("edit_setting_"):
        key = data.replace("edit_setting_","")
        user_data.setdefault(uid, {})['admin_mode'] = "edit_setting"
        user_data.setdefault(uid, {})['edit_setting_key'] = key
        current = gs(key)[:200]
        safe_edit(call, f"⚙️ *{key}*\n\nالقيمة الحالية:\n`{current}`\n\nأرسل القيمة الجديدة:",
            parse_mode="Markdown", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("❌ إلغاء", callback_data="admin_settings")]]))

    elif data == "admin_editpoints":
        user_data.setdefault(uid, {})['admin_mode'] = "search_user_pts"
        safe_edit(call, "🔧 أرسل ID المستخدم:",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("❌ إلغاء", callback_data="admin_menu")]]))

    elif data.startswith("adm_pts_"):
        parts = data.split("_"); action = parts[2]; uid2 = int(parts[3])
        user_data.setdefault(uid, {})['admin_mode'] = f"adm_{action}_pts"
        user_data.setdefault(uid, {})['adm_target'] = uid2
        safe_edit(call, f"🔧 أرسل عدد النقاط للمستخدم `{uid2}`:", parse_mode="Markdown")

    elif data.startswith("ban_"):
        uid2 = int(data.split("_")[1])
        conn = get_db(); conn.execute("UPDATE users SET is_banned=1 WHERE id=?", (uid2,)); conn.commit(); conn.close()
        bot.answer_callback_query(call.id, f"✅ تم حظر {uid2}")

    elif data.startswith("unban_"):
        uid2 = int(data.split("_")[1])
        conn = get_db(); conn.execute("UPDATE users SET is_banned=0 WHERE id=?", (uid2,)); conn.commit(); conn.close()
        bot.answer_callback_query(call.id, f"✅ تم رفع الحظر عن {uid2}")

    elif data.startswith("freeze_"):
        uid2 = int(data.split("_")[1])
        conn = get_db(); conn.execute("UPDATE users SET is_frozen=1 WHERE id=?", (uid2,)); conn.commit(); conn.close()
        bot.answer_callback_query(call.id, f"✅ تم تجميد {uid2}")

    elif data.startswith("unfreeze_"):
        uid2 = int(data.split("_")[1])
        conn = get_db(); conn.execute("UPDATE users SET is_frozen=0 WHERE id=?", (uid2,)); conn.commit(); conn.close()
        bot.answer_callback_query(call.id, f"✅ تم رفع تجميد {uid2}")

    elif data == "admin_export":
        conn = get_db()
        users = conn.execute("SELECT * FROM users").fetchall()
        conn.close()
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["id","username","lang","points","total_points","invites","joined_at","is_banned"])
        for u in users:
            writer.writerow([u["id"],u["username"],u["lang"],u["points"],u["total_points"],u["invites"],u["joined_at"],u["is_banned"]])
        bio = io.BytesIO(output.getvalue().encode())
        bio.name = "users.csv"
        bot.send_document(ADMIN_ID, document=bio)
        bot.answer_callback_query(call.id, "✅ تم التصدير")

# ==================== MESSAGE HANDLER ====================
@bot.message_handler(content_types=["text","photo","voice","audio","video","document"])
@bot.message_handler(content_types=["text","photo","voice","audio","video","document"])
def handle_message(msg):
    uid = msg.from_user.id
    if not msg: return
    uid = uid
    user = get_user(uid)
    if not user:
        bot.send_message(uid, "⚠️ اضغط /start أولاً"); return
    lang = user["lang"]
    if gs("bot_active","1") == "0" and uid != ADMIN_ID:
        bot.send_message(uid, T(lang,"maintenance")); return
    if user["is_banned"]:
        bot.send_message(uid, T(lang,"banned")); return
    if user["is_frozen"]:
        bot.send_message(uid, T(lang,"frozen")); return

    mode = user_data.get(uid, {}).get('mode')
    text = msg.text or ""

    # ===== أدمن =====
    if uid == ADMIN_ID:
        admin_mode = user_data.get(uid, {}).get('admin_mode')
        if admin_mode:
            user_data.setdefault(uid, {})['admin_mode'] = None

            if admin_mode == "broadcast":
                conn = get_db(); users_list = conn.execute("SELECT id FROM users WHERE is_banned=0").fetchall(); conn.close()
                sent = 0
                for u in users_list:
                    try:
                        bot.forward_message(u["id"], uid, msg.message_id)
                        sent += 1; time.sleep(0.05)
                    except Exception as _e: print(f"⚠️ [LINE 2574] {type(_e).__name__}: {_e}")
                bot.send_message(uid, f"✅ أُرسل لـ {sent} مستخدم")

            elif admin_mode == "search_user":
                try:
                    query_text = text.strip().lstrip("@")
                    conn = get_db()
                    u = None
                    if text.strip().lstrip("@").isdigit() and not text.strip().startswith("@"):
                        u = conn.execute("SELECT * FROM users WHERE id=?", (int(text.strip()),)).fetchone()
                    if not u:
                        u = conn.execute("SELECT * FROM users WHERE LOWER(username)=LOWER(?)", (query_text,)).fetchall()
                        u = u[0] if u else None
                    if not u:
                        # بحث بالاسم
                        u = conn.execute("SELECT * FROM users WHERE LOWER(username) LIKE LOWER(?)", (f"%{query_text}%",)).fetchall()
                        u = u[0] if u else None
                    ops_count = 0; inviter_info = ""; invited_users = []
                    if u:
                        try: ops_count = conn.execute("SELECT COUNT(*) FROM operations WHERE user_id=?", (u["id"],)).fetchone()[0]
                        except: ops_count = 0
                        if u["invited_by"]:
                            inv = conn.execute("SELECT username FROM users WHERE id=?", (u["invited_by"],)).fetchone()
                            inviter_info = f"@{inv['username']}" if inv else str(u["invited_by"])
                        invited_list = conn.execute("SELECT id, username FROM users WHERE invited_by=? LIMIT 10", (u["id"],)).fetchall()
                        invited_users = [f"@{r['username']}" for r in invited_list]
                    conn.close()
                    if not u:
                        bot.send_message(uid, "❌ مستخدم غير موجود"); return
                    lv = get_level(u["total_points"])
                    lv_name = lv["name_ar"]
                    joined   = datetime.fromtimestamp(u["joined_at"]).strftime("%Y-%m-%d %H:%M") if u["joined_at"] else "غير معروف"
                    last_daily = datetime.fromtimestamp(u["last_daily"]).strftime("%Y-%m-%d") if u["last_daily"] else "لم يستخدمها"
                    status_parts = []
                    if u["is_banned"]: status_parts.append("🚫 محظور")
                    if u["is_frozen"]: status_parts.append("❄️ مجمد")
                    if not status_parts: status_parts.append("✅ نشط")
                    status_str   = " | ".join(status_parts)
                    invited_str  = ", ".join(invited_users) if invited_users else "لا أحد"
                    if len(invited_users) == 10: invited_str += "..."
                    # escape HTML
                    def eh(s):
                        return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
                    uname = eh(u['username'] or u['id'])
                    uname_display = f"@{uname}" if u['username'] else f"ID: {u['id']}"
                    uname_link = f"<a href='tg://user?id={u['id']}'>{eh(u['username'] or u['id'])}</a>"
                    u_dict = dict(u)
                    info = (
                        f"👤 <b>معلومات المستخدم</b>\n\n"
                        f"🆔 ID: <code>{u_dict.get('id','?')}</code>\n"
                        f"📛 اليوزر: {uname_display}\n"
                        f"👤 الاسم: {uname_link}\n"
                        f"🌍 اللغة: {'عربي 🇸🇦' if u_dict.get('lang')=='ar' else 'English 🇬🇧'}\n"
                        f"📅 التسجيل: {eh(joined)}\n\n"
                        f"<b>━━ النقاط والمستوى ━━</b>\n"
                        f"⭐ حالية: <b>{u_dict.get('points',0)}</b> | إجمالي: <b>{u_dict.get('total_points',0)}</b>\n"
                        f"{lv['emoji']} المستوى: <b>{eh(lv_name)}</b>\n"
                        f"🎁 آخر هدية: {eh(last_daily)}\n\n"
                        f"<b>━━ الاستخدام ━━</b>\n"
                        f"🖼️ {u_dict.get('total_images',0)} صورة | 🎬 {u_dict.get('total_videos',0)} فيديو\n"
                        f"🎵 {u_dict.get('total_music',0)} أغنية | ✏️ {u_dict.get('total_edits',0)} تعديل\n"
                        f"📈 إجمالي عمليات: {ops_count}\n\n"
                        f"<b>━━ الدعوات ━━</b>\n"
                        f"🔗 دعا: <b>{u_dict.get('invites',0)}</b> | دعاه: {eh(inviter_info or 'لا أحد')}\n"
                        f"👥 المدعوون: {eh(invited_str)}\n\n"
                        f"<b>━━ الحالة ━━</b>\n"
                        f"{eh(status_str)}"
                    )
                    bot.send_message(uid, info, parse_mode="HTML",
                        reply_markup=InlineKeyboardMarkup([
                            [InlineKeyboardButton("➕ أضف نقاط", callback_data=f"adm_pts_add_{u['id']}"),
                             InlineKeyboardButton("➖ خصم نقاط", callback_data=f"adm_pts_sub_{u['id']}")],
                            [InlineKeyboardButton("🚫 حظر" if not u['is_banned'] else "✅ رفع حظر",
                                callback_data=f"ban_{u['id']}" if not u['is_banned'] else f"unban_{u['id']}"),
                             InlineKeyboardButton("❄️ تجميد" if not u['is_frozen'] else "🔥 رفع تجميد",
                                callback_data=f"freeze_{u['id']}" if not u['is_frozen'] else f"unfreeze_{u['id']}")],
                        ]))
                except Exception as e:
                    print(f"⚠️ search_user error: {e}")
                    bot.send_message(uid, f"❌ خطأ في البحث: {e}")

            elif admin_mode == "search_user_pts":
                try:
                    uid2 = int(text)
                    u = get_user(uid2)
                    if not u: bot.send_message(uid, "❌ مستخدم غير موجود"); return
                    user_data.setdefault(uid, {})['admin_mode'] = None
                    bot.send_message(uid, 
                        f"🔧 المستخدم: `{uid2}` | النقاط: {u['points']}", parse_mode="Markdown",
                        reply_markup=InlineKeyboardMarkup([
                            [InlineKeyboardButton("➕ أضف", callback_data=f"adm_pts_add_{uid2}"),
                             InlineKeyboardButton("➖ خصم", callback_data=f"adm_pts_sub_{uid2}")],
                        ]))
                except: bot.send_message(uid, "❌ ID غير صالح")

            elif admin_mode == "new_code_step1":
                user_data.setdefault(uid, {})['new_code_name'] = text.strip()
                user_data.setdefault(uid, {})['admin_mode'] = "new_code_step2"
                bot.send_message(uid, f"🎟️ *كود جديد - الخطوة 2/3*\n\nالكود: `{text.strip()}`\n\nأرسل الحد الأقصى للاستخدامات:", parse_mode="Markdown",
                    reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("❌ إلغاء", callback_data="admin_menu")]]))

            elif admin_mode == "new_code_step2":
                try:
                    max_uses = int(text.strip())
                    user_data.setdefault(uid, {})['new_code_max_uses'] = max_uses
                    user_data.setdefault(uid, {})['admin_mode'] = "new_code_step3"
                    bot.send_message(uid, f"🎟️ *كود جديد - الخطوة 3/3*\n\nالكود: `{user_data.get(uid, {}).get('new_code_name')}`\nاستخدامات: {max_uses}\n\nأرسل عدد النقاط:", parse_mode="Markdown",
                        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("❌ إلغاء", callback_data="admin_menu")]]))
                except: bot.send_message(uid, "❌ أدخل رقماً صحيحاً!")

            elif admin_mode == "new_code_step3":
                try:
                    pts = int(text.strip())
                    code = user_data.get(uid, {}).get('new_code_name')
                    max_uses = user_data.get(uid, {}).get('new_code_max_uses')
                    conn = get_db()
                    conn.execute("INSERT INTO codes (code,points,max_uses,created_at) VALUES (?,?,?,?)", (code, pts, max_uses, int(time.time())))
                    conn.commit(); conn.close()
                    bot.send_message(uid, f"✅ *تم إنشاء الكود!*\n\n🎟️ الكود: `{code}`\n💰 النقاط: {pts}\n🔢 الاستخدامات: {max_uses}", parse_mode="Markdown")
                except Exception as e:
                    bot.send_message(uid, f"❌ خطأ: {e}")

            elif admin_mode == "add_channel":
                link = text.strip()
                if not (link.startswith("https://t.me/") or link.startswith("http://t.me/")):
                    bot.send_message(uid, "❌ أدخل رابطاً صحيحاً!\nمثال: `https://t.me/CHANNEL`", parse_mode="Markdown"); return
                ch_username = link.replace("https://t.me/","").replace("http://t.me/","").split("/")[0]
                ch_id = f"@{ch_username}"
                conn = get_db()
                try:
                    conn.execute("INSERT INTO channels (channel_id,channel_name,invite_link) VALUES (?,?,?)", (ch_id, ch_username, link))
                    conn.commit()
                    bot.send_message(uid, f"✅ أُضيفت: `{link}`", parse_mode="Markdown")
                except: bot.send_message(uid, "❌ القناة موجودة!")
                finally: conn.close()

            elif admin_mode == "set_welcome_text":
                ss("welcome_ar", text.replace("\\n", "\n"))
                bot.send_message(uid, "✅ تم تغيير رسالة الترحيب العربية!\n\nأرسل /admin للعودة")

            elif admin_mode == "set_welcome_photo":
                if msg.photo:
                    file_id = msg.photo[-1].file_id
                    ss("welcome_type", "photo"); ss("welcome_media", file_id)
                    bot.send_message(uid, "✅ تم حفظ صورة الترحيب!")
                else:
                    user_data.setdefault(uid, {})['admin_mode'] = "set_welcome_photo"
                    bot.send_message(uid, "❌ أرسل صورة!")

            elif admin_mode == "set_welcome_sticker":
                if msg.sticker:
                    file_id = msg.sticker.file_id
                    ss("welcome_type", "sticker"); ss("welcome_media", file_id)
                    bot.send_message(uid, "✅ تم حفظ ستيكر الترحيب!")
                else:
                    user_data.setdefault(uid, {})['admin_mode'] = "set_welcome_sticker"
                    bot.send_message(uid, "❌ أرسل ستيكر!")

            elif admin_mode == "edit_setting":
                key = user_data.get(uid, {}).get('edit_setting_key', "")
                ss(key, text)
                bot.send_message(uid, f"✅ `{key}` تم التحديث", parse_mode="Markdown")

            elif admin_mode == "adm_add_pts":
                uid2 = user_data.get(uid, {}).get('adm_target')
                try:
                    add_points(uid2, int(text))
                    bot.send_message(uid, f"✅ أُضيف {text} لـ {uid2}")
                except: bot.send_message(uid, "❌")

            elif admin_mode == "adm_sub_pts":
                uid2 = user_data.get(uid, {}).get('adm_target')
                try:
                    deduct_points(uid2, int(text))
                    bot.send_message(uid, f"✅ خُصم {text} من {uid2}")
                except: bot.send_message(uid, "❌")

            return

    # ===== أوضاع المستخدم =====
    if mode == "transfer_step1":
        try:
            uid2 = int(text.strip())
            if uid2 == uid:
                bot.send_message(uid, T(lang,"transfer_self")); return
            target = get_user(uid2)
            if not target:
                bot.send_message(uid, T(lang,"transfer_no_user")); return
            user_data.setdefault(uid, {})["transfer_to"] = uid2
            bot.send_message(uid, T(lang,"transfer_enter_pts",uid2=uid2,bal=user["points"]),
                parse_mode="Markdown")
        except Exception as _e:
            print(f"⚠️ [LINE 2767] {type(_e).__name__}: {_e}")
            bot.send_message(uid, T(lang,"transfer_no_user"))

    elif mode == "transfer_step2":
        user_data.setdefault(uid, {})['mode'] = None
        try:
            pts = int(text.strip())
            if pts < 1:
                bot.send_message(uid, T(lang,"transfer_min")); return
            uid2 = user_data.get(uid, {}).get('transfer_target')
            if not has_points(uid, pts):
                bot.send_message(uid, T(lang,"transfer_no_pts")); return
            deduct_points(uid, pts)
            add_points(uid2, pts)
            sender_name = msg.from_user.username or str(uid)
            try:
                bot.send_message(uid2, T(get_lang(uid2),"transfer_recv",
                    pts=pts, sender=sender_name, bal=get_user(uid2)["points"]))
            except Exception as _e: print(f"⚠️ [LINE 2785] {type(_e).__name__}: {_e}")
            bot.send_message(uid, T(lang,"transfer_ok",
                pts=pts, uid2=uid2, bal=get_user(uid)["points"]), parse_mode="Markdown",
                reply_markup=back_kb(lang))
        except Exception as _e:
            print(f"⚠️ [LINE 2789] {type(_e).__name__}: {_e}")
            bot.send_message(uid, T(lang,"transfer_min"))

    elif mode == "use_code":
        user_data.setdefault(uid, {})['mode'] = None
        conn = get_db()
        row = conn.execute("SELECT * FROM codes WHERE code=?", (text.strip(),)).fetchone()
        if not row: bot.send_message(uid, T(lang,"code_wrong")); conn.close(); return
        if row["used"] >= row["max_uses"]: bot.send_message(uid, T(lang,"code_used_up")); conn.close(); return
        if row["expires_at"] and row["expires_at"] < int(time.time()): bot.send_message(uid, T(lang,"code_expired")); conn.close(); return
        used = conn.execute("SELECT 1 FROM code_uses WHERE code_id=? AND user_id=?", (row["id"], uid)).fetchone()
        if used: bot.send_message(uid, T(lang,"code_already")); conn.close(); return
        conn.execute("UPDATE codes SET used=used+1 WHERE id=?", (row["id"],))
        conn.execute("INSERT INTO code_uses VALUES (?,?,?)", (row["id"], uid, int(time.time())))
        conn.commit(); conn.close()
        add_points(uid, row["points"])
        bot.send_message(uid, T(lang,"code_ok",pts=row["points"],bal=get_user(uid)["points"]))

    elif mode == "word_game":
        user_data.setdefault(uid, {})['mode'] = None
        correct = user_data.get(uid, {}).get('word_answer', "").strip().lower()
        pts = user_data.get(uid, {}).get('word_pts', 2)
        if text.strip().lower() == correct:
            add_points(uid, pts)
            conn = get_db(); conn.execute("UPDATE users SET word_attempts=3, word_reset_time=? WHERE id=?", (int(time.time()), uid)); conn.commit(); conn.close()
            bot.send_message(uid, T(lang,"game_won",pts=pts), reply_markup=back_kb(lang))
        else:
            wrong_txt = T(lang,"game_wrong_w",word=user_data.get(uid, {}).get('word_answer', ""))
            bot.send_message(uid, wrong_txt, reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(T(lang,"try_again"), callback_data="games_menu"),
                 InlineKeyboardButton(T(lang,"back"), callback_data="back_main")]
            ]))
    elif mode == "chat_ai":
        if not text.strip():
            return
        history = user_data.get(uid, {}).get('chat_history', [])
        wtext = gs_safe("waiting_text","⏳ جارٍ التنفيذ، انتظر...")
        msg = bot.send_message(uid, wtext)
        try:
            answer = deepseek_chat(text, history)
        except Exception as e:
            print(f"chat_ai executor error: {e}")
            answer = None
        try:
            bot.delete_message(uid, msg.message_id)
        except Exception as _e: print(f"⚠️ [LINE 2835] {type(_e).__name__}: {_e}")
        # تأكد إن الـ answer مش فاضي
        if answer and str(answer).strip():
            history.append({"role": "user", "content": text})
            history.append({"role": "assistant", "content": answer})
            user_data.setdefault(uid, {})['chat_history'] = history[-16:]
            bot.send_message(uid, str(answer).strip())
        else:
            bot.send_message(uid, T(lang,"ai_fail"))

    elif mode == "support_chat":
        if not text.strip():
            return
        history = user_data.get(uid, {}).get('support_history', [])
        wtext = gs_safe("waiting_text","⏳ جارٍ التنفيذ، انتظر...")
        msg = bot.send_message(uid, wtext)
        try:
            answer = support_ai(text, history)
        except Exception as e:
            print(f"support_chat executor error: {e}")
            answer = None
        try:
            bot.delete_message(uid, msg.message_id)
        except Exception as _e: print(f"⚠️ [LINE 2859] {type(_e).__name__}: {_e}")
        if answer and str(answer).strip():
            history.append({"role": "user", "content": text})
            history.append({"role": "assistant", "content": answer})
            user_data.setdefault(uid, {})['support_history'] = history[-12:]
            bot.send_message(uid, str(answer).strip())
        else:
            bot.send_message(uid, T(lang,"ai_fail"))
    elif mode == "nano_image":
        prompt = text
        nano_model = user_data.get(uid, {}).get('nano_model', "nano-banana-pro")
        cost = user_data.get(uid, {}).get('nano_cost', 1)
        if not has_points(uid, cost):
            bot.send_message(uid, T(lang,"no_pts",n=cost), reply_markup=no_points_kb(lang)); return
        deduct_points(uid, cost)
        wtext = gs_safe("waiting_text","⏳ جارٍ التنفيذ، انتظر...")
        msg = bot.send_message(uid, wtext)
        wait_msg = bot.send_message(uid, gs_safe("waiting_text","⏳ جارٍ التنفيذ، انتظر..."))
        def do_nano():
            try:
                img_url = generate_image(prompt) if nano_model == "image-editor" else nanobanana_generate(prompt)
                if not img_url:
                    add_points(uid, cost)
                    try: bot.edit_message_text(T(lang,"fail_refund"), uid, wait_msg.message_id)
                    except: pass
                    return
                log_op(uid,"image")
                try: bot.delete_message(uid, wait_msg.message_id)
                except: pass
                send_image_smart(uid, img_url, T(lang,"img_caption",p=prompt[:200]))
            except Exception as e:
                print(f"do_nano error: {e}")
                add_points(uid, cost)
                try: bot.edit_message_text(f"❌ خطأ: {str(e)[:200]}", uid, wait_msg.message_id)
                except: pass
        threading.Thread(target=do_nano, daemon=True).start()

    elif mode == "edit_wait_photo":
        if msg.photo:
            photo = bot.get_file(msg.photo[-1].file_id)
            img_bytes = requests.get(f'https://api.telegram.org/file/bot{BOT_TOKEN}/{photo.file_path}').content
            user_data.setdefault(uid, {})["edit_photo_bytes"] = img_bytes
            user_data.setdefault(uid, {})["mode"] = "edit_prompt"
            bot.send_message(uid, T(lang,"photo_ok"))
        elif msg.sticker:
            bot.send_message(uid, T(lang,"edit_send_photo"))
        else:
            bot.send_message(uid, T(lang,"edit_send_photo"))

    elif mode == "edit_prompt":
        prompt = text
        img_bytes = user_data.get(uid, {}).get('edit_photo_bytes')
        cost = user_data.get(uid, {}).get('edit_cost', 1)
        if not img_bytes:
            bot.send_message(uid, T(lang,"choose_first")); return
        if not has_points(uid, cost):
            bot.send_message(uid, T(lang,"no_pts",n=cost), reply_markup=no_points_kb(lang)); return
        deduct_points(uid, cost)
        wtext = gs_safe("waiting_text","⏳ جارٍ التنفيذ، انتظر...")
        wait_msg = bot.send_message(uid, wtext)
        def do_edit():
                try:
                    img_url = nanobanana_generate(prompt, image_bytes=img_bytes)
                    if not img_url:
                        add_points(uid, cost)
                        try: bot.edit_message_text(T(lang,"fail_refund"), uid, wait_msg.message_id)
                        except: pass
                        return
                    log_op(uid,"edit" if "edit" in "do_edit" else "image")
                    try: bot.delete_message(uid, wait_msg.message_id)
                    except: pass
                    send_image_smart(uid, img_url, T(lang,"img_caption",p=prompt[:200]))
                except Exception as e:
                    print(f"do_edit error: {e}")
                    add_points(uid, cost)
                    try: bot.edit_message_text(f"❌ خطأ: {str(e)[:200]}", uid, wait_msg.message_id)
                    except: pass
        threading.Thread(target=do_edit, daemon=True).start()

    elif mode == "nano_edit_photos":
        if msg.sticker:
            bot.send_message(uid, T(lang,"edit_pro_send")); return
        if msg.photo:
            photo = bot.get_file(msg.photo[-1].file_id)
            img_bytes = requests.get(f'https://api.telegram.org/file/bot{BOT_TOKEN}/{photo.file_path}').content
            imgs = user_data.get(uid, {}).get('nano_edit_images', [])
            imgs.append(bytes(img_bytes))
            user_data.setdefault(uid, {})['nano_edit_images'] = imgs
            bot.send_message(uid, T(lang,"photo_added",n=len(imgs)))
        elif msg.text:
            prompt = msg.text
            imgs = user_data.get(uid, {}).get('nano_edit_images', [])
            if not imgs:
                bot.send_message(uid, T(lang,"edit_pro_send")); return
            cost = user_data.get(uid, {}).get('edit_cost', 2)
            if not has_points(uid, cost):
                bot.send_message(uid, T(lang,"no_pts",n=cost), reply_markup=no_points_kb(lang)); return
            deduct_points(uid, cost)
            wtext = gs_safe("waiting_text","⏳ جارٍ التنفيذ، انتظر...")
            wait_msg = bot.send_message(uid, wtext)
            def do_nano_edit():
                    try:
                        img_url = nanobanana_generate(prompt, image_bytes=img_bytes)
                        if not img_url:
                            add_points(uid, cost)
                            try: bot.edit_message_text(T(lang,"fail_refund"), uid, wait_msg.message_id)
                            except: pass
                            return
                        log_op(uid,"edit" if "edit" in "do_nano_edit" else "image")
                        try: bot.delete_message(uid, wait_msg.message_id)
                        except: pass
                        send_image_smart(uid, img_url, T(lang,"img_caption",p=prompt[:200]))
                    except Exception as e:
                        print(f"do_nano_edit error: {e}")
                        add_points(uid, cost)
                        try: bot.edit_message_text(f"❌ خطأ: {str(e)[:200]}", uid, wait_msg.message_id)
                        except: pass
            threading.Thread(target=do_nano_edit, daemon=True).start()


    elif mode == "img2video_wait_photo":
        if msg.photo:
            photo = bot.get_file(msg.photo[-1].file_id)
            img_bytes = requests.get(f'https://api.telegram.org/file/bot{BOT_TOKEN}/{photo.file_path}').content
            user_data.setdefault(uid, {})["vid_photo_bytes"] = img_bytes
            user_data.setdefault(uid, {})["mode"] = "img2video_prompt"
            bot.send_message(uid, T(lang,"vid_photo_ok"))

    elif mode == "img2video_prompt":
        prompt = text
        img_bytes = user_data.get(uid, {}).get('img2video_bytes')
        cost = user_data.get(uid, {}).get('video_cost', 2)
        if not has_points(uid, cost):
            bot.send_message(uid, T(lang,"no_pts",n=cost), reply_markup=no_points_kb(lang)); return
        deduct_points(uid, cost)
        wtext = gs_safe("waiting_text","⏳ جارٍ التنفيذ، انتظر...")
        wait_msg = bot.send_message(uid, wtext)
        def do_img2video():
            try:
                result = image_to_video(img_bytes, prompt)
            except Exception as e:
                result = None
                print(f"do_img2video error: {e}")
            if not result:
                add_points(uid, cost)
                bot.edit_message_text(T(lang,"fail_refund"), uid, msg.message_id); return
            log_op(uid,"video")
            bot.delete_message(uid, msg.message_id)
            if isinstance(result, str):
                vid_url = result
            elif isinstance(result, dict):
                vid_url = result.get("url") or result.get("videoUrl") or result.get("video_url") or ""
            else:
                vid_url = ""
            if not vid_url:
                add_points(uid, cost)
                bot.send_message(uid, T(lang,"fail_refund")); return
            try: msg.reply_video(video=vid_url, caption=T(lang,"vid_caption",p=prompt[:200]))
            except: bot.send_message(uid, T(lang,"vid_caption",p=prompt[:100]), reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(T(lang,"open_btn"), url=vid_url)]]))
        threading.Thread(target=do_img2video, daemon=True).start()

    elif mode == "music":
        prompt = text
        cost = user_data.get(uid, {}).get('music_cost', 2)
        if not has_points(uid, cost):
            bot.send_message(uid, T(lang,"no_pts",n=cost), reply_markup=no_points_kb(lang)); return
        deduct_points(uid, cost)
        wtext = gs_safe("waiting_text","⏳ جارٍ التنفيذ، انتظر...")
        msg = bot.send_message(uid, wtext)
        def do_music():
            result = generate_music(prompt)
            if not result:
                add_points(uid, cost)
                bot.edit_message_text(T(lang,"music_fail"), chat_id=uid, message_id=msg.message_id); return
            log_op(uid,"music")
            bot.delete_message(uid, msg.message_id)
            caption = T(lang,"music_ok",p=result["title"])
            send_music_result(uid, result, caption, lang)
        threading.Thread(target=do_music, daemon=True).start()

    elif mode == "music_lyrics":
        lyrics = text
        cost = user_data.get(uid, {}).get('music_cost', 2)
        if not has_points(uid, cost):
            bot.send_message(uid, T(lang,"no_pts",n=cost), reply_markup=no_points_kb(lang)); return
        deduct_points(uid, cost)
        wtext = gs_safe("waiting_text","⏳ جارٍ التنفيذ، انتظر...")
        msg = bot.send_message(uid, wtext)
        def do_music_lyrics():
            result = generate_music_from_lyrics(lyrics)
            if not result:
                add_points(uid, cost)
                bot.edit_message_text(T(lang,"music_fail"), chat_id=uid, message_id=msg.message_id); return
            log_op(uid,"music")
            bot.delete_message(uid, msg.message_id)
            caption = T(lang,"music_ok",p=result["title"])
            send_music_result(uid, result, caption, lang)
        threading.Thread(target=do_music_lyrics, daemon=True).start()

    else:
        bot.send_message(uid, T(lang,"choose_first"), reply_markup=get_main_keyboard(lang))

# ==================== MAIN ====================
def main():
    init_db()
    print("🤖 البوت شغّال!")
    bot.infinity_polling(timeout=20, long_polling_timeout=20)

if __name__ == "__main__":
    main()
