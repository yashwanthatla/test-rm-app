import sys
import os
from pathlib import Path

current_dir = Path(__file__).resolve().parent
parent_dir = current_dir.parent
sys.path.append(str(parent_dir))

from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()


class Settings:
    OPENAI_MODEL = "gpt-4o-mini"
    TEMPERATURE = 0
    VECTOR_STORE_PATH = "vectorstore"
    
    @classmethod
    def get_model_kwargs(cls) -> Dict[str, Any]:
        return {
            "temperature": cls.TEMPERATURE,
            "model": cls.OPENAI_MODEL
        }

