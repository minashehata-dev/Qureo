# ==============================================================
# Dockerfile لتشغيل بوت منصة كيريو التعليمية مع متصفح Playwright
# يدعم بيئة Headless Chromium بالكامل على مدار 24/7
# ==============================================================

FROM python:3.11-slim

# ضبط المتغيرات البيئية لضمان عمل بايثون والمتصفح بسلاسة
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    HEADLESS=true \
    DEBIAN_FRONTEND=noninteractive

WORKDIR /app

# تثبيت الحزم الأساسية للنظام
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

# تثبيت مكتبات بايثون المطلوبة
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# تثبيت متصفح كروميوم مع جميع اعتمادات النظام الخاصة بـ Playwright
RUN playwright install --with-deps chromium

# نسخ الكود المصدري للمشروع
COPY . .

# إنشاء المجلدات التخزينية للمشروع
RUN mkdir -p /app/data /app/logs /app/screenshots

# أمر التشغيل الأساسي للبوت
CMD ["python", "main.py"]
