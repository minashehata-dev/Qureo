@echo off
chcp 65001 > nul
set PYTHONUTF8=1
set PYTHONIOENCODING=utf-8

echo ============================================================
echo   جاري تنظيف أي جلسات قديمة وتشغيل بوت تليجرام لمنصة كيريو
echo ============================================================
echo.

:: إغلاق أي عملية بايثون سابقة كانت معلقة في الذاكرة لضمان تحميل الكود الجديد 100%
taskkill /F /IM python.exe 2>nul

IF NOT EXIST ".venv\Scripts\python.exe" (
    echo [خطأ] البيئة الافتراضية .venv غير موجودة!
    pause
    exit /b 1
)

echo [1/2] جاري تشغيل main.py...
.\.venv\Scripts\python.exe main.py

pause
