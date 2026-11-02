"""
أداة مزامنة ونقل بنك البيانات من SQLite إلى Cloud Firestore (Firebase)
-------------------------------------------------------------
تقوم هذه الأداة بفحص الاتصال بفايربيس ونقل كافة الإجابات المحفوظة وحسابات الطلاب
وفصول المسارات إلى السحابة فور وضع ملف الاعتماد firebase_credentials.json
"""

import sys
from pathlib import Path

# ضبط ترميز UTF-8 في ويندوز
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from config import Config
from solver.answers_db import answers_db


def main():
    print("=" * 60)
    print("🚀 أداة مزامنة قاعدة البيانات مع Firebase Cloud Firestore")
    print("=" * 60)

    # 1. التحقق من وجود ملف الاعتماد
    cred_path = Config.FIREBASE_CREDENTIALS_PATH
    if not cred_path.exists():
        print(f"\n❌ لم يتم العثور على ملف مفاتيح الاعتماد: {cred_path.name}")
        print("📁 المسار المتوقع للملف هو:")
        print(f"   {cred_path}")
        print("\n💡 خطوات الحل:")
        print("1. افتح Firebase Console: https://console.firebase.google.com/")
        print("2. ادخل على إعدادات المشروع (Project Settings) ⚙️ -> Service accounts.")
        print("3. اضغط على Generate new private key وحمل ملف الـ JSON.")
        print(f"4. قم بتسميته '{cred_path.name}' وضعه في مجلد المشروع الرئيسي.")
        print("5. أعد تشغيل هذا السكربت مجدداً: python migrate_to_firebase.py\n")
        return

    # 2. التحقق من حالة الاتصال بفايربيس
    if not answers_db.firebase or not answers_db.firebase.is_connected:
        print("\n❌ فشل الاتصال بقاعدة بيانات فايربيس Firestore.")
        print("يرجى التأكد من تفعيل 'Cloud Firestore' داخل مشروعك في Firebase Console.")
        return

    print("\n✅ تم الاتصال بـ Cloud Firestore بنجاح!")
    print("\n📊 إحصائيات البيانات المحلية الحالية في SQLite:")
    total_answers = answers_db.get_total_count()
    fin_count = answers_db.get_financial_questions_count()
    print(f"   - إجمالي الإجابات البرمجية المحفوظة: {total_answers}")
    print(f"   - إجمالي أسئلة الثقافة المالية: {fin_count}")

    print("\n⏳ جاري بدء عملية الرفع والمزامنة إلى السحابة (Cloud Firestore)...")
    stats = answers_db.sync_all_to_firebase()

    print("\n" + "=" * 60)
    print("🎉 اكتملت المزامنة بنجاح تام!")
    print("=" * 60)
    print(f"👤 حسابات الطلاب المرفوعة: {stats['users']}")
    print(f"📚 الفصول والمسارات المرفوعة: {stats['chapters']}")
    print(f"💡 الإجابات البرمجية المرفوعة: {stats['answers']}")
    print(f"💼 أسئلة الثقافة المالية المرفوعة: {stats['finance']}")
    print("=" * 60)
    print("✅ الآن البوت متصل بالكامل بفايربيس ويحفظ كل شيء سحابياً ومحلياً بالتوازي!")


if __name__ == "__main__":
    main()
