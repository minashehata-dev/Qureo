import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
ENV_PATH = BASE_DIR / ".env"

load_dotenv(dotenv_path=ENV_PATH)


class Config:
    TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "").strip()
    # الوضع الافتراضي في بيئات السيرفرات والحاويات هو Headless = True
    HEADLESS: bool = os.getenv("HEADLESS", "True").lower() in ("true", "1", "yes")

    DEFAULT_COURSE_URL: str = os.getenv(
        "DEFAULT_COURSE_URL", "https://me-tp.qureo.education/course/javascript_ar"
    ).strip()
    DEFAULT_JS_COURSE_URL: str = os.getenv(
        "DEFAULT_JS_COURSE_URL", "https://me-tp.qureo.education/course/javascript_ar"
    ).strip()
    LOGIN_URL: str = os.getenv(
        "LOGIN_URL", "https://me-portal.qureo.education/login"
    ).strip()
    QUREO_USERNAME: str = os.getenv("QUREO_USERNAME", "").strip()
    QUREO_PASSWORD: str = os.getenv("QUREO_PASSWORD", "").strip()

    # معرف تيليجرام الخاص بالمسؤول / الأدمن لاستقبال بيانات الطلاب وتحديثات المستويات الحية
    _admin_env = os.getenv("ADMIN_ID", "5918488755").strip()
    ADMIN_ID: int = int(_admin_env) if _admin_env.isdigit() else 5918488755

    # منفذ خادم فحص الصحة لمنصات الاستضافة السحابية مثل blitz.cloud و Railway و Render
    _port_env = os.getenv("PORT", "8080").strip()
    PORT: int = int(_port_env) if _port_env.isdigit() else 8080

    # إعدادات قاعدة بيانات فايربيس (Cloud Firestore)
    FIREBASE_CREDENTIALS_FILE: str = os.getenv("FIREBASE_CREDENTIALS_FILE", "firebase_credentials.json").strip()
    FIREBASE_CREDENTIALS_PATH: Path = (
        Path(FIREBASE_CREDENTIALS_FILE) if Path(FIREBASE_CREDENTIALS_FILE).is_absolute()
        else BASE_DIR / FIREBASE_CREDENTIALS_FILE
    )
    ENABLE_FIREBASE: bool = os.getenv("ENABLE_FIREBASE", "True").lower() in ("true", "1", "yes")

    # المجلدات التخزينية المساعدة للمشروع
    SCREENSHOTS_DIR: Path = BASE_DIR / "screenshots"
    LOGS_DIR: Path = BASE_DIR / "logs"
    DATA_DIR: Path = BASE_DIR / "data"


# التأكد من إنشاء جميع المجلدات المساعدة تلقائياً
Config.SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
Config.LOGS_DIR.mkdir(parents=True, exist_ok=True)
Config.DATA_DIR.mkdir(parents=True, exist_ok=True)
