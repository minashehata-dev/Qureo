@echo off
chcp 65001 >nul
echo ======================================================================
echo 🚀 رفع مشروع بوت كيريو بالكامل إلى GitHub بضغطة واحدة
echo ======================================================================
echo.
echo هذا السكربت يضمن رفع مجلد bot و solver وجميع الملفات دون أي نقص
echo لحل خطأ (ModuleNotFoundError: No module named 'bot') نهائياً.
echo.

set /p REPO_URL="🔗 أدخل رابط مستودع GitHub الخاص بك (مثال: https://github.com/username/repo.git): "

if "%REPO_URL%"=="" (
    echo ❌ لم يتم إدخال رابط المستودع. تم الإلغاء.
    pause
    exit /b
)

echo.
echo 📦 [1/5] تهيئة مستودع Git المحلي...
if not exist .git (
    git init
)

echo 📄 [2/5] تجهيز وإضافة جميع الملفات والمجلدات (bot, solver, data)...
git add .

echo 💾 [3/5] حفظ التغييرات (Commit)...
git commit -m "Full project structure ready for blitz.cloud"

echo 🌿 [4/5] ضبط الفرع الرئيسي (main)...
git branch -M main

echo 🌐 [5/5] الربط والرفع المباشر إلى GitHub...
git remote remove origin 2>nul
git remote add origin %REPO_URL%
git push -u origin main --force

echo.
if %errorlevel% equ 0 (
    echo ======================================================================
    echo 🎉 تم رفع المشروع بالكامل إلى GitHub بنجاح تام!
    echo الآن توجه إلى لوحة blitz.cloud واضغط على Re-deploy أو Redeploy App.
    echo ======================================================================
) else (
    echo ======================================================================
    echo ⚠️ حدث خطأ أثناء الرفع إلى GitHub.
    echo تأكد من صحة رابط المستودع وصلاحيات حسابك على GitHub.
    echo ======================================================================
)
pause
