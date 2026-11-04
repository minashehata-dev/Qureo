import os
import sys
import zipfile

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

OUTPUT_ZIP = "deploy_server_package.zip"

ITEMS_TO_INCLUDE = [
    "bot",
    "solver",
    "data",
    "logs",
    "screenshots",
    "Dockerfile",
    "docker-compose.yml",
    "Procfile",
    "main.py",
    "config.py",
    "requirements.txt",
    ".env.example",
    ".dockerignore",
    ".gitignore",
    "solve_level_cli.py",
    "README.md",
    "DEPLOYMENT.md"
]

print("\n" + "=" * 60)
print("📦 جاري تجهيز وضغط حزمة السيرفر الإنتاجية النظيفة...")
print("=" * 60)

count = 0
with zipfile.ZipFile(OUTPUT_ZIP, "w", zipfile.ZIP_DEFLATED) as z:
    for item in ITEMS_TO_INCLUDE:
        if not os.path.exists(item):
            continue
        if os.path.isdir(item):
            for root, dirs, files in os.walk(item):
                # استبعاد مجلدات الكاش المؤقتة
                if "__pycache__" in root or ".idea" in root or ".venv" in root:
                    continue
                for f in files:
                    if f.endswith((".pyc", ".pyo", ".log", ".tmp")):
                        continue
                    file_path = os.path.join(root, f)
                    arcname = os.path.relpath(file_path, ".")
                    z.write(file_path, arcname)
                    count += 1
        elif os.path.isfile(item):
            z.write(item, item)
            count += 1

size_mb = os.path.getsize(OUTPUT_ZIP) / (1024 * 1024)
print(f"✅ تم إنشاء الحزمة بنجاح تام!")
print(f"📁 اسم الملف: {OUTPUT_ZIP}")
print(f"📊 عدد الملفات المضمنة: {count} ملفاً")
print(f"💾 الحجم الإجمالي: {size_mb:.2f} ميجابايت")
print("=" * 60)
print("🚀 الحزمة جاهزة للرفع المباشر على blitz.cloud أو استخراجها في VPS / GitHub!\n")
