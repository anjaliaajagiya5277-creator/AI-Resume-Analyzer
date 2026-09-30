import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "resume_screening_secret")

    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    MODEL_NAME="gemini-2.5-flash"

    UPLOAD_FOLDER = "uploads"

    MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10 MB

    ALLOWED_RESUME_EXTENSIONS = {"pdf"}

    ALLOWED_JD_EXTENSIONS = {"pdf", "docx", "txt"}