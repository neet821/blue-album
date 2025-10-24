"""
Environment-adaptive configuration
Auto-detects Windows/Linux and adjusts paths/settings accordingly
"""
import os
import sys
import platform
from pathlib import Path
from typing import Literal

# Detect operating system
IS_WINDOWS = platform.system() == "Windows"
IS_LINUX = platform.system() == "Linux"

# Auto-detect project root (works on both Windows and Linux)
if getattr(sys, 'frozen', False):
    # Running as compiled executable
    PROJECT_ROOT = Path(sys.executable).parent
else:
    # Running as script
    PROJECT_ROOT = Path(__file__).parent.parent.resolve()

# Environment type detection
def get_environment() -> Literal["development", "production", "docker"]:
    """Auto-detect environment type"""
    if os.getenv("DOCKER_ENV") == "true":
        return "docker"
    elif IS_WINDOWS or os.path.exists(PROJECT_ROOT / "Laragon"):
        return "development"
    else:
        return "production"

ENV = get_environment()

# Platform-specific settings
class PlatformConfig:
    """Platform-specific configuration"""
    
    # Project paths (cross-platform)
    PROJECT_ROOT = PROJECT_ROOT
    BACKEND_DIR = PROJECT_ROOT / "backend"
    FRONTEND_DIR = PROJECT_ROOT / "frontend"
    UPLOAD_DIR = PROJECT_ROOT / "uploads"
    LOGS_DIR = PROJECT_ROOT / "logs"
    
    # Database configuration (environment-based)
    if ENV == "docker":
        DB_HOST = os.getenv("DB_HOST", "mysql")
        DB_PORT = int(os.getenv("DB_PORT", "3306"))
    elif ENV == "development":
        DB_HOST = os.getenv("DB_HOST", "localhost")
        DB_PORT = int(os.getenv("DB_PORT", "3306"))
    else:  # production
        DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
        DB_PORT = int(os.getenv("DB_PORT", "3306"))
    
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    DB_NAME = os.getenv("DB_NAME", "blue_album")
    
    # Server configuration
    if ENV == "docker":
        HOST = "0.0.0.0"  # Docker needs to listen on all interfaces
        PORT = 8000
    elif ENV == "development":
        HOST = "127.0.0.1"  # Local development
        PORT = 8000
    else:  # production
        HOST = "0.0.0.0"  # Production needs external access
        PORT = int(os.getenv("PORT", "8000"))
    
    # CORS origins (environment-based)
    if ENV == "development":
        CORS_ORIGINS = [
            "http://localhost:5173",
            "http://localhost:8080",
            "http://127.0.0.1:5173",
            "http://127.0.0.1:8080",
        ]
    else:
        CORS_ORIGINS = os.getenv(
            "CORS_ORIGINS",
            "http://localhost:5173"
        ).split(",")
    
    # JWT configuration
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    ALGORITHM = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    # File upload settings
    MAX_UPLOAD_SIZE = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".mp4", ".webm"}
    
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO" if ENV == "production" else "DEBUG")
    
    @classmethod
    def ensure_directories(cls):
        """Create necessary directories if they don't exist"""
        for dir_path in [cls.UPLOAD_DIR, cls.LOGS_DIR]:
            dir_path.mkdir(parents=True, exist_ok=True)
    
    @classmethod
    def get_database_url(cls) -> str:
        """Get database connection URL"""
        return (
            f"mysql+pymysql://{cls.DB_USER}:{cls.DB_PASSWORD}"
            f"@{cls.DB_HOST}:{cls.DB_PORT}/{cls.DB_NAME}"
        )
    
    @classmethod
    def print_config(cls):
        """Print current configuration (for debugging)"""
        print("=" * 60)
        print(f"🖥️  Environment: {ENV}")
        print(f"🔧 Platform: {platform.system()} {platform.release()}")
        print(f"📁 Project Root: {cls.PROJECT_ROOT}")
        print(f"🗄️  Database: {cls.DB_HOST}:{cls.DB_PORT}/{cls.DB_NAME}")
        print(f"🌐 Server: {cls.HOST}:{cls.PORT}")
        print(f"🔐 CORS Origins: {cls.CORS_ORIGINS}")
        print(f"📝 Log Level: {cls.LOG_LEVEL}")
        print("=" * 60)

# Create directories on import
PlatformConfig.ensure_directories()

# Export for easy import
config = PlatformConfig

if __name__ == "__main__":
    # Test configuration detection
    config.print_config()
