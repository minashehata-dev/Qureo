# ==============================================================
# Dockerfile لتشغيل بوت منصة كيريو التعليمية مع متصفح Playwright
# جاهز 100% للنشر على blitz.cloud و VPS و Render و Railway
# ==============================================================

FROM python:3.11-slim

# ضبط المتغيرات البيئية لضمان عمل بايثون والمسارات والمتصفح بسلاسة
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    HEADLESS=true \
    DEBIAN_FRONTEND=noninteractive \
    PYTHONPATH=/app \
    PORT=8080

WORKDIR /app

# تثبيت الحزم الأساسية للنظام لتشغيل Chromium و Playwright
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    fonts-liberation \
    fonts-noto-color-emoji \
    fonts-noto-core \
    libnss3 \
    libatk-bridge2.0-0 \
    libdrm2 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libgbm1 \
    libasound2 \
    libpango-1.0-0 \
    libxshmfence1 \
    && rm -rf /var/lib/apt/lists/*

# تثبيت مكتبات بايثون المطلوبة أولاً للاستفادة من طبقات التخزين المؤقت (Docker Cache)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# تثبيت متصفح كروميوم مع جميع اعتمادات نظام التشغيل الخاصة بـ Playwright
RUN playwright install --with-deps chromium

# نسخ الكود المصدري للمشروع كاملاً
COPY . .

# إنشاء المجلدات التخزينية للمشروع لضمان الصلاحيات
RUN mkdir -p /app/data /app/logs /app/screenshots

# إعلان المنفذ لمنصات الاستضافة السحابية
EXPOSE 8080

# أمر التشغيل الأساسي للبوت
CMD ["python", "main.py"]
