import logging
from supabase import create_client, Client
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# --- المفاتيح التي طلبتها (للتجربة) ---
TELEGRAM_TOKEN = "8375173644:AAGwwZhYTKjsz1bcH-goSq5v9MhxQ0M9hAw"
SUPABASE_URL = "https://psmyicemromnyknquccy.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBzbXlpY2Vtcm9tbnlrbnF1Y2N5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjI3MTE5MzEsImV4cCI6MjA3ODI4NzkzMX0.Pj48UwW0TBmiyUN-GGO4RDTKvMo0_hR5zqJT_bWVAcI"
# (ملاحظة: أنت أرسلت المفتاح السري (secret) وليس مفتاح anon. الكود سيستخدمه.)

# إعداد الـ logging لمعرفة الأخطاء
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- إعداد الاتصال بـ Supabase ---
try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    logger.info("تم الاتصال بـ Supabase بنجاح!")
except Exception as e:
    logger.error(f"فشل الاتصال بـ Supabase: {e}")
    # لا نوقف البرنامج، قد يكون التوكن خاطئاً ولكنه سيستمر بالمحاولة

# --- أوامر البوت ---

# دالة لأمر /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """يرسل رسالة ترحيب عند إرسال أمر /start."""
    user = update.effective_user
    await update.message.reply_html(
        f"أهلاً بك يا {user.mention_html()}! أنا بوت تجريبي جاهز للعمل.",
    )

# دالة للرد على الرسائل النصية
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """يكرر الرسالة النصية التي يرسلها المستخدم."""
    logger.info(f"المستخدم {update.effective_user.id} أرسل: {update.message.text}")
    await update.message.reply_text(f"لقد أرسلت: {update.message.text}")

# دالة للتعامل مع الأخطاء
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    """يسجل الأخطاء التي تحدث."""
    logger.error(f"حدث خطأ: {context.error}")

# --- الدالة الرئيسية لتشغيل البوت ---
def main():
    """الدالة الرئيسية لتشغيل البوت."""
    
    # إنشاء التطبيق وربطه بالتوكن
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # إضافة الأوامر (Handlers)
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # إضافة معالج الأخطاء
    application.add_error_handler(error_handler)

    # تشغيل البوت (وضع الاستماع)
    logger.info("البوت قيد التشغيل...")
    application.run_polling()

if __name__ == "__main__":
    main()
