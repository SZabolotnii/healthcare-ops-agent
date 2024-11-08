# src/config/settings.py
import os
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()

class Settings:
    """Configuration settings for the Healthcare Operations Management Agent"""
    
    # OpenAI Configuration
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    MODEL_NAME = "gpt-4o-mini-2024-07-18"
    MODEL_TEMPERATURE = 0
    
    # LangGraph Configuration
    MEMORY_TYPE = os.getenv("MEMORY_TYPE", "sqlite")
    MEMORY_URI = os.getenv("MEMORY_URI", ":memory:")
    
    # Hospital Configuration
    HOSPITAL_SETTINGS = {
        "total_beds": 300,
        "departments": ["ER", "ICU", "General", "Surgery", "Pediatrics"],
        "staff_roles": ["Doctor", "Nurse", "Specialist", "Support Staff"]
    }
    
    # Application Settings
    MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))
    REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "30"))
    BATCH_SIZE = int(os.getenv("BATCH_SIZE", "10"))
    
    # Logging Configuration
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LOG_FILE = "logs/healthcare_ops_agent.log"
    
    # Quality Metrics Thresholds
    QUALITY_THRESHOLDS = {
        "min_satisfaction_score": 7.0,
        "max_wait_time_minutes": 45,
        "optimal_bed_utilization": 0.85,
        "min_staff_ratio": {
            "ICU": 0.5,  # 1 nurse per 2 patients
            "General": 0.25  # 1 nurse per 4 patients
        }
    }
    
    @classmethod
    def get_model_config(cls) -> Dict[str, Any]:
        """Get model configuration"""
        return {
            "model": cls.MODEL_NAME,
            "temperature": cls.MODEL_TEMPERATURE,
            "api_key": cls.OPENAI_API_KEY
        }
    
    @classmethod
    def validate_settings(cls) -> bool:
        """Validate required settings"""
        required_settings = [
            "OPENAI_API_KEY",
            "MODEL_NAME",
            "MEMORY_TYPE"
        ]
        
        for setting in required_settings:
            if not getattr(cls, setting):
                raise ValueError(f"Missing required setting: {setting}")
        
        return True# Configuration settings implementation
