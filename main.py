import asyncio
import logging
import sys
import os
import time
from pathlib import Path

# ==============================================================
# إجبار بايثون على إضافة مجلد المشروع في أول قائمة sys.path
# واكتشاف الحزم تلقائياً لمنع أي خطأ ModuleNotFoundError نهائياً
# ==============================================================
BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

# 0. استخراج الحزمة التلقائي إذا وجد ملف deploy_server_package.zip على السيرفر
bot_candidate = BASE_DIR / "bot"
if not bot_candidate.exists():
    zip_files = list(BASE_DIR.glob("*.zip"))
    for z_file in zip_files:
        try:
            import zipfile
            print(f"📦 [Auto-Extract] وجد أرشيف '{z_file.name}' على السيرفر! جاري فك ضغط الحزمة تلقائياً...")
            with zipfile.ZipFile(z_file, "r") as z:
                z.extractall(BASE_DIR)
            print("✅ [Auto-Extract] تم فك ضغط مجلدات bot و solver وبنك البيانات بنجاح تام!")
            break
        except Exception as e_zip:
            print(f"⚠️ فشل استخراج {z_file.name}: {e_zip}")

# 1. البحث التلقائي عن حزمة bot سواء في المجلد الأساسي أو مجلدات فرعية (مثل PythonProject3 أو src أو Bot)
if not bot_candidate.exists():
    for item in os.listdir(BASE_DIR):
        item_path = BASE_DIR / item
        if item.lower() == "bot" and item_path.is_dir():
            try:
                os.symlink(item_path, bot_candidate)
            except Exception:
                pass
            if str(BASE_DIR) not in sys.path:
                sys.path.insert(0, str(BASE_DIR))
            break

    if not bot_candidate.exists():
        for root, dirs, files in os.walk(BASE_DIR):
            if "handlers.py" in files and os.path.basename(root).lower() == "bot":
                parent_dir = os.path.dirname(root)
                if parent_dir not in sys.path:
                    sys.path.insert(0, parent_dir)
                break

# 2. طباعة تشخيصية لمحتويات السيرفر في السجلات للتحقق
current_files = [f for f in os.listdir(BASE_DIR) if not f.startswith(".")]
print("\n" + "=" * 65)
print(f"🚀 [Qureo Bot Engine] بدء تشغيل البوت في المسار: {BASE_DIR}")
print(f"📂 محتويات مجلد العمل في السيرفر: {current_files}")
has_bot = (BASE_DIR / "bot").exists() or any("bot" in str(p).lower() for p in sys.path)
if not has_bot:
    print("⚠️ [تنبيه هام]: لم يتم العثور على مجلد 'bot' في السيرفر!")
else:
    print("✅ تم التحقق من وجود حزمة 'bot' بنجاح تام!")
print("=" * 65 + "\n")

# إجبار بايثون على استخدام ترميز UTF-8 في ويندوز لمنع أي أخطاء في الرموز التعبيرية واللغة العربية
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace", line_buffering=True)
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace", line_buffering=True)

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


async def start_health_server(port: int):
    """
    خادم HTTP خفيف في الخلفية (Health Check Server) للرد على فحص جاهزية المنصات السحابية
    مثل blitz.cloud و Render و Railway و Fly.io ولمنع المنصة من وضع البوت في السكون (Sleep mode)
    """
    from aiohttp import web

    async def handle_ping(request):
        return web.json_response({
            "status": "online",
            "service": "Qureo Solution Bot",
            "timestamp": int(time.time()),
            "health": "ok"
        })

    app = web.Application()
    app.router.add_get("/", handle_ping)
    app.router.add_get("/health", handle_ping)
    app.router.add_get("/ping", handle_ping)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    logger.info(f"🌐 [Web Health Check] خادم فحص الحالة السحابي يعمل على المنفذ: {port} (0.0.0.0:{port})")
    return runner


async def main():
    if not Config.TELEGRAM_BOT_TOKEN or Config.TELEGRAM_BOT_TOKEN == "YOUR_TELEGRAM_BOT_TOKEN_HERE":
        logger.error("لم يتم العثور على TELEGRAM_BOT_TOKEN! يرجى التحقق من ملف .env")
        return

    print("\n" + "=" * 65)
    print("🚀 جاري بدء تشغيل نظام بوت كيريو والحل التلقائي الفوري (Qureo Solution Bot ⚡)")
    print("=" * 65)

    # 0. تشغيل خادم فحص الصحة لمنصات الاستضافة السحابية الخارجية (مثل blitz.cloud)
    health_runner = None
    try:
        health_runner = await start_health_server(Config.PORT)
    except Exception as e_srv:
        logger.warning(f"⚠️ تعذر تشغيل خادم فحص الصحة على المنفذ {Config.PORT}: {e_srv}")

    # 1. إحصائيات بنك البيانات المحلي
    from solver.answers_db import answers_db
    py_count = len(answers_db.get_all_chapters("python_short_ar"))
    js_count = len(answers_db.get_all_chapters("javascript_ar"))
    ans_count = answers_db.get_total_count()

    print(f"✅ [1/5] تم تهيئة بنك البيانات بنجاح (SQLite):")
    print(f"       📚 فصول مسار بايثون المسجلة: {py_count} فصلاً")
    print(f"       🌐 فصول مسار جافاسكريبت المسجلة: {js_count} فصلاً")
    print(f"       🎯 بنك الإجابات المعتمدة: {ans_count} إجابة نموذجية")

    # 2. حالة الاتصال بقاعدة البيانات
    db_mode = "🔥 Firebase Cloud Firestore (سحابي متزامن)" if getattr(answers_db.firebase, "is_connected", False) else "💾 SQLite محلي فوري وآمن (data/answers.db)"
    print(f"✅ [2/5] وضع التخزين والمزامنة: {db_mode}")

    # 3. إنشاء كائن البوت والموزع
    bot = Bot(
        token=Config.TELEGRAM_BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN)
    )
    dp = Dispatcher()

    # 4. تسجيل مسارات الأوامر والأحداث
    dp.include_router(router)
    print("✅ [3/5] تم تسجيل مسارات وأوامر البوت وأزرار التحكم بنجاح")

    # 5. تنظيف التحديثات المعلقة
    await bot.delete_webhook(drop_pending_updates=True)
    print("✅ [4/5] تم تنظيف التحديثات المعلقة السابقة بنجاح")

    # تسجيل قائمة أوامر البوت الرسمية في تليجرام
    try:
        from aiogram.types import BotCommand
        await bot.set_my_commands([
            BotCommand(command="start", description="🚀 بدء واستخدام البوت واختيار الصف"),
            BotCommand(command="clear", description="🧹 مسح الشاشة بالكامل وتسجيل الخروج"),
            BotCommand(command="status", description="📊 تقرير مستواي الحالي والـ API"),
            BotCommand(command="logout", description="🔒 تسجيل الخروج ومسح بيانات الحساب"),
            BotCommand(command="stop", description="⏹️ إيقاف الحل التلقائي")
        ])
    except Exception as e_cmd:
        logger.warning(f"Could not set bot commands: {e_cmd}")

    bot_info = await bot.get_me()
    print(f"✅ [5/5] تم الاتصال بخوادم تليجرام بنجاح! اسم البوت: @{bot_info.username}")

    print("=" * 65)
    print("🎉 جميع عمليات التهيئة تمت بنجاح تام 100%! البوت يعمل الآن.")
    print(f"🤖 يوزر البوت على تليجرام: @{bot_info.username}")
    print(f"🔗 رابط الوصول المباشر: https://t.me/{bot_info.username}")
    print("=" * 65 + "\n")

    try:
        await dp.start_polling(bot)
    finally:
        logger.info("جاري إغلاق المتصفحات وإيقاف البوت...")
        if health_runner:
            try:
                await health_runner.cleanup()
            except Exception:
                pass
        await close_all_user_browsers()
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("تم إيقاف البوت.")
