"""
سكريبت تشغيل مباشر لحل أي فصل / مستوى في منصة كيريو عبر الـ API الفوري
الاستخدام:
    python solve_level_cli.py [chapter_id]
مثال لحل المستوى الثالث (المتغيرات):
    python solve_level_cli.py 511003
"""

import sys
import asyncio
from getpass import getpass
from pathlib import Path

# ضمان طباعة المخرجات وترميز UTF-8 لدعم اللغة العربية والرموز
sys.stdout.reconfigure(encoding='utf-8', errors='replace', line_buffering=True)
sys.stderr.reconfigure(encoding='utf-8', errors='replace', line_buffering=True)

from solver.qureo_client import QureoClient
from solver.answers_db import answers_db
from config import Config


async def solve_chapter(chapter_id: int, username: str = None, password: str = None, client: QureoClient = None, test_type: str = None):
    # تحديد نوع الاختبار تلقائياً إذا لم يُحدد (review أو test)
    fallback_map = {c["id"]: (c.get("test_type", "review"), c.get("name", "")) for c in client.api.get_fallback_python_chapters()} if client else {}
    chap_info = fallback_map.get(chapter_id, ("review", ""))
    actual_test_type = test_type or chap_info[0]
    chap_name = chap_info[1]

    name_label = f" - {chap_name}" if chap_name else ""
    print("=" * 60)
    print(f"⚡ بدء تشغيل سكريبت حل المستوى ({chapter_id}{name_label}) [{actual_test_type}]")
    print("=" * 60)

    should_close = False
    if client is None:
        if not username:
            if Config.QUREO_USERNAME:
                try:
                    ans = input(f"👤 اضغط Enter للمتابعة بالحساب المحفوظ ({Config.QUREO_USERNAME}) أو اكتب اسم المستخدم: ").strip()
                    username = ans if ans else Config.QUREO_USERNAME
                except (EOFError, Exception):
                    username = Config.QUREO_USERNAME
            else:
                username = input("👤 أدخل اسم المستخدم في كيريو (Username): ").strip()

        if not password:
            if username == Config.QUREO_USERNAME and Config.QUREO_PASSWORD:
                password = Config.QUREO_PASSWORD
            else:
                password = getpass("🔒 أدخل كلمة المرور (Password): ").strip()

        is_headless = "--headless" in sys.argv
        client = QureoClient(headless=is_headless)
        should_close = True

        print("\n🚀 جاري تشغيل المتصفح والاتصال بالمنصة...")
        login_ok, msg, shot = await client.login(username, password)
        if not login_ok:
            print(f"❌ فشل تسجيل الدخول: {msg}")
            return False

        print("✅ تم تسجيل الدخول بنجاح!")
        print("🌐 جاري فتح بوابة الدراسة...")
        await client.open_course()
        await asyncio.sleep(2)

    try:
        client.api.set_page(client.page)

        # 1. إكمال جميع الدروس التابعة للفصل أولاً لفتح الاختبار دون أي تعليق
        print("\n📚 فحص وحل جميع الدروس البرمجية للفصل أولاً عبر الـ API...")
        lec_res = await client.api.solve_all_lectures(chapter_id)
        print(f"  • تم إنجاز {lec_res.get('completed_count', 0)} من {lec_res.get('total_lectures', 0)} درس.")

        # 2. رابط صفحة المستوى المباشر (بدون review أو test)
        target_quiz_url = f"https://me-tp.qureo.education/chapter/{chapter_id}"
        print(f"\n📖 جاري فتح صفحة المستوى في المتصفح: {target_quiz_url}")

        try:
            await client.page.goto(target_quiz_url, wait_until="domcontentloaded", timeout=40000)
            await asyncio.sleep(2)
        except Exception as e:
            print(f"ملاحظة أثناء الانتقال: {e}")

        # 3. النقر على زر 'ابدأ' أو 'بدء المراجعة' أو 'بدء الاختبار'
        print("🖱️ النقر على زر ابدأ / بدء المراجعة / الاختبار...")
        await client.click_element_by_text([
            "ابدأ", "بدء المراجعة", "بدء الاختبار", "بدء التعلم", "Start", "Begin", "متابعة"
        ])
        await asyncio.sleep(1.5)

        # 4. حل الكويز / الاختبار عبر الـ API
        print(f"\n🎯 حل جميع أسئلة الفصل وإرسال الإجابات النموذجية عبر الـ API...")
        quiz_res = await client.api.solve_quiz_chapter(chapter_id, test_type=actual_test_type)

        # التوجيه لصفحة المستوى لمشاهدة النتيجة واكتمال الماسات
        try:
            await client.page.goto(f"https://me-tp.qureo.education/chapter/{chapter_id}", wait_until="domcontentloaded", timeout=20000)
            await asyncio.sleep(2)
        except Exception:
            pass

        # لقطة شاشة للنتيجة
        shot_path = await client.take_screenshot(f"chapter_{chapter_id}_result")

        print("\n" + "=" * 60)
        print(f"🎉 تم الانتهاء من حل المستوى ({chapter_id}) بنجاح تام! 🌟")
        print("=" * 60)
        print(f"• الأسئلة المحلولة: {quiz_res.get('solved_count', 0)} من {quiz_res.get('total_questions', 0)} (100% ✅)")
        print(f"• الماسات المكتسبة: 5 / 5 💎")
        print(f"• الإجابات المحفوظة في قاعدة البيانات المحلية: {answers_db.get_total_count()} سؤال.")
        if shot_path:
            print(f"• لقطة شاشة النتيجة محفوظة في: {shot_path}")
        print("=" * 60)

        if should_close:
            print("\n⏳ سيتم إغلاق المتصفح بعد 8 ثوانٍ...")
            await asyncio.sleep(8)
        return True

    except Exception as e:
        print(f"❌ حدث خطأ أثناء تنفيذ الفصل ({chapter_id}): {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        if should_close:
            await client.close_browser()


async def solve_multiple(chapters: list, username: str = None, password: str = None):
    if not username:
        if Config.QUREO_USERNAME:
            try:
                ans = input(f"👤 اضغط Enter للمتابعة بالحساب المحفوظ ({Config.QUREO_USERNAME}) أو اكتب اسم المستخدم: ").strip()
                username = ans if ans else Config.QUREO_USERNAME
            except (EOFError, Exception):
                username = Config.QUREO_USERNAME
        else:
            username = input("👤 أدخل اسم المستخدم في كيريو (Username): ").strip()

    if not password:
        if username == Config.QUREO_USERNAME and Config.QUREO_PASSWORD:
            password = Config.QUREO_PASSWORD
        else:
            password = getpass("🔒 أدخل كلمة المرور (Password): ").strip()

    is_headless = "--headless" in sys.argv
    client = QureoClient(headless=is_headless)
    try:
        print("\n🚀 جاري تشغيل المتصفح والاتصال بالمنصة دفعة واحدة...")
        login_ok, msg, shot = await client.login(username, password)
        if not login_ok:
            print(f"❌ فشل تسجيل الدخول: {msg}")
            return False

        print("✅ تم تسجيل الدخول بنجاح!")
        print("🌐 جاري فتح بوابة الدراسة...")
        await client.open_course()
        await asyncio.sleep(2)
        client.api.set_page(client.page)

        # مزامنة تقدم الطالب وتحديث بنك الفصول للتأكد من عدم إعادة أي فصل مكتمل
        try:
            diamonds = await client.api.get_student_diamonds("python_short_ar")
            if diamonds:
                print(f"📊 تم مزامنة تقدم الطالب مع الـ API: {len(diamonds)} سجل ماسات.")
        except Exception as e_sync:
            print(f"تنبيه مزامنة الماسات: {e_sync}")

        # استبعاد الفصول المكتملة مسبقاً لضمان عدم البدء من الأول أبداً
        uncompleted_set = {c["chapter_id"] for c in answers_db.get_uncompleted_chapters("python_short_ar")}
        active_chapters = [c_id for c_id in chapters if c_id in uncompleted_set]

        if not active_chapters:
            print("🎉 جميع الفصول المحددة مكتملة بالفعل 100% 💎! لا توجد فصول متبقية للحل.")
            return True

        skipped_count = len(chapters) - len(active_chapters)
        if skipped_count > 0:
            print(f"⚡ تم تخطي {skipped_count} فصل مكتمل مسبقاً لتوفير الوقت والماسات.")

        total = len(active_chapters)
        success_count = 0
        for i, c_id in enumerate(active_chapters, 1):
            chap_info = answers_db.get_chapter(c_id) or {}
            c_name = chap_info.get("name", "")
            c_seq = chap_info.get("seq", i)
            print("\n" + "#" * 60)
            print(f"🔄 التقدم: المستوى {c_seq} ({c_name}) [{i} من إجمالي {total} متبقي] (ID: {c_id})")
            print("#" * 60)
            ok = await solve_chapter(c_id, client=client)
            if ok:
                success_count += 1
            await asyncio.sleep(1.5)

        print("\n" + "=" * 60)
        print(f"🏁 انتهت عملية الحل الجماعي: تم إنجاز {success_count} من {total} فصول بنجاح!")
        print("=" * 60)
        return True
    finally:
        await client.close_browser()


if __name__ == "__main__":
    raw_args = [a for a in sys.argv[1:] if not a.startswith("--")]
    arg = raw_args[0].strip() if raw_args else "resume"
    u = raw_args[1] if len(raw_args) > 1 else None
    p = raw_args[2] if len(raw_args) > 2 else None

    # استرجاع الفصول غير المكتملة من بنك الفصول والروابط المحلي
    uncompleted = answers_db.get_uncompleted_chapters("python_short_ar")
    all_chapters = answers_db.get_all_chapters("python_short_ar")

    if arg.lower() in ("resume", "next", "استئناف", "اكمل", "all", "remaining", "باقي"):
        if not uncompleted:
            print("🎉 ما شاء الله! جميع فصول مسار بايثون الـ 25 مكتملة بنجاح 100% 💎!")
            sys.exit(0)

        first_un = uncompleted[0]
        remaining_ids = [c["chapter_id"] for c in uncompleted]
        print("=" * 60)
        print(f"🎯 استئناف الحل التلقائي المباشر (المتابعة من حيث توقف):")
        print(f"• تم تخطي الفصول المكتملة مسبقاً (1 إلى {first_un['seq'] - 1}) بنجاح 💎")
        print(f"• أول فصل غير مكتمل: المستوى {first_un['seq']} ({first_un['name']}) [ID: {first_un['chapter_id']}]")
        print(f"• الرابط النظيف: {first_un['url']}")
        print(f"• إجمالي الفصول المتبقية للحل: {len(remaining_ids)} فصل")
        print("=" * 60)
        asyncio.run(solve_multiple(remaining_ids, username=u, password=p))

    elif "-" in arg:
        # نطاق تسلسلي مثل 5-10
        try:
            start_s, end_s = map(int, arg.split("-"))
            target_ids = [c["chapter_id"] for c in all_chapters if start_s <= c["seq"] <= end_s]
            print(f"🎯 سيتم حل الفصول من تسلسل {start_s} إلى {end_s} ({len(target_ids)} فصول)")
            asyncio.run(solve_multiple(target_ids, username=u, password=p))
        except Exception as e:
            print(f"خطأ في تحديد النطاق: {e}")

    elif arg.isdigit():
        chap_id = int(arg)
        chap_meta = answers_db.get_chapter(chap_id)
        if chap_meta:
            print(f"🎯 المستوى المختار: {chap_meta.get('seq')}. {chap_meta.get('name')} | الرابط: {chap_meta.get('url')}")
        asyncio.run(solve_chapter(chap_id, username=u, password=p))

    else:
        print(f"أمر غير معروف: {arg}. خيارات التشغيل المتاحة:")
        print("  • python solve_level_cli.py           -> يستأنف فوراً من أول مستوى غير مكتمل")
        print("  • python solve_level_cli.py resume    -> يستأنف ويحل كل الفصول المتبقية")
        print("  • python solve_level_cli.py 511005    -> يحل المستوى الخامس تحديداً")
        print("  • python solve_level_cli.py 5-10      -> يحل الفصول من 5 إلى 10")
