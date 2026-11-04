@echo off
chcp 65001 >nul
echo ==============================================================
echo 📦 تجهيز وضغط حزمة المشروع الجاهزة للرفع على السيرفر الخارجي
echo ==============================================================
if exist .venv\Scripts\python.exe (
    .venv\Scripts\python.exe package_project.py
) else (
    python package_project.py
)
pause
