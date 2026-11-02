import asyncio
import logging
import sys
import os

# إجبار بايثون على استخدام ترميز UTF-8 في ويندوز لمنع أي أخلااطاء في الرموز التعبيرية واللغة العربية
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from config import Config
from bot.handlers import router, close_all_user_browsers

# إعداد السجلات (Logging) مع ترميز UTF-8
file_handler = logging.FileHandler(Config.LOGS_DIR / "bot.log", encoding="utf-8", errors="replace")
stream_handler = logging.StreamHandler(sys.stdout)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[stream_handler, file_handler]
)
logger = logging.getLogger("QureoSolverBot")



async def main():
    if not Config.TELEGRAM_BOT_TOKEN or Config.TELEGRAM_BOT_TOKEN == "YOUR_TELEGRAM_BOT_TOKEN_HERE":
        logger.error("لم يتم العثور على TELEGRAM_BOT_TOKEN! يرجى التحقق من ملف .env")
        return

    logger.info("جاري تهيئة البوت وتشغيله...")

    # إنشاء كائن البوت والموزع
    bot = Bot(
        token=Config.TELEGRAM_BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN)
    )
    dp = Dispatcher()

    # تسجيل مسارات الأوامر والأحداث
    dp.include_router(router)

    # تنظيف أي تحديثات معلقة قديمة
    await bot.delete_webhook(drop_pending_updates=True)

    bot_info = await bot.get_me()
    logger.info(f"تم تشغيل البوت بنجاح! اسم البوت: @{bot_info.username}")
    from solver.answers_db import answers_db
    db_mode = "🔥 Firebase Cloud Firestore (سحابي متزامن)" if getattr(answers_db.firebase, "is_connected", False) else "💾 SQLite محلي (data/answers.db)"
    print("\n==========================================")
    print(f"البوت يعمل الان بنجاح على تليجرام!")
    print(f"يوزر البوت: @{bot_info.username}")
    print(f"قاعدة البيانات: {db_mode}")
    print("==========================================\n")

    try:
        await dp.start_polling(bot)
    finally:
        logger.info("جاري إغلاق المتصفحات وإيقاف البوت...")
        await close_all_user_browsers()
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("تم إيقاف البوت.")
