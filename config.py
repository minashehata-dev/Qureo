import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
ENV_PATH = BASE_DIR / ".env"

load_dotenv(dotenv_path=ENV_PATH)


class Config:
    TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "").strip()
    HEADLESS: bool = os.getenv("HEADLESS", "False").lower() in ("true", "1", "yes")
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

    # إعدادات قاعدة بيانات فايربيس (Cloud Firestore)
    FIREBASE_CREDENTIALS_FILE: str = os.getenv("FIREBASE_CREDENTIALS_FILE", "firebase_credentials.json").strip()
    FIREBASE_CREDENTIALS_PATH: Path = (
        Path(FIREBASE_CREDENTIALS_FILE) if Path(FIREBASE_CREDENTIALS_FILE).is_absolute()
        else BASE_DIR / FIREBASE_CREDENTIALS_FILE
    )
    ENABLE_FIREBASE: bool = os.getenv("ENABLE_FIREBASE", "True").lower() in ("true", "1", "yes")

    # المجلدات المساعدة
    SCREENSHOTS_DIR: Path = BASE_DIR / "screenshots"
    LOGS_DIR: Path = BASE_DIR / "logs"


# التأكد من وجود المجلدات المساعدة
Config.SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
Config.LOGS_DIR.mkdir(parents=True, exist_ok=True)
