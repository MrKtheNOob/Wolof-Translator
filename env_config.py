"""
Environment configuration loader.
Loads configuration from environment variables for secure, open-source deployment.
"""
import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()


def get_env_var(key: str, default: Optional[str] = None, required: bool = False) -> Optional[str]:
    """
    Get environment variable with optional default and required flag.
    
    Args:
        key: Environment variable name
        default: Default value if not found
        required: If True, raises error when variable is missing
        
    Returns:
        Environment variable value or default
        
    Raises:
        ValueError: If required variable is missing
    """
    value = os.getenv(key, default)
    if required and value is None:
        raise ValueError(
            f"Required environment variable '{key}' is not set. "
            f"Please set it in your .env file or environment."
        )
    return value


class EnvConfig:
    """Configuration loaded from environment variables."""
    
    @classmethod
    def _get(cls, key: str, default: Optional[str] = None) -> Optional[str]:
        """Helper method to get env var (evaluated at access time)."""
        return get_env_var(key, default)
    
    # HuggingFace
    @classmethod
    def HF_TOKEN(cls) -> Optional[str]:
        return cls._get("HF_TOKEN")
    
    @classmethod
    def HUB_USERNAME(cls) -> Optional[str]:
        return cls._get("HUB_USERNAME")
    
    @classmethod
    def HUB_MODEL_NAME(cls) -> str:
        return cls._get("HUB_MODEL_NAME", "wolofToFrenchTranslator_nllb") or "wolofToFrenchTranslator_nllb"
    
    # Model
    @classmethod
    def MODEL_CHECKPOINT(cls) -> str:
        return cls._get("MODEL_CHECKPOINT", "facebook/nllb-200-distilled-600M") or "facebook/nllb-200-distilled-600M"
    
    # Dataset
    @classmethod
    def DATASET_NAME(cls) -> str:
        return cls._get("DATASET_NAME", "galsenai/french-wolof-translation") or "galsenai/french-wolof-translation"
    
    # Weights & Biases
    @classmethod
    def WANDB_API_KEY(cls) -> Optional[str]:
        return cls._get("WANDB_API_KEY")
    
    @classmethod
    def WANDB_PROJECT_NAME(cls) -> str:
        return cls._get("WANDB_PROJECT_NAME", "french-wolof-translator") or "french-wolof-translator"
    
    @classmethod
    def WANDB_ENABLED(cls) -> bool:
        val = cls._get("WANDB_ENABLED", "false")
        return val.lower() == "true" if val else False
    
    # Training (optional overrides)
    @classmethod
    def OUTPUT_DIR(cls) -> Optional[str]:
        return cls._get("OUTPUT_DIR")
    
    @classmethod
    def NUM_TRAIN_EPOCHS(cls) -> Optional[int]:
        val = cls._get("NUM_TRAIN_EPOCHS")
        return int(val) if val else None
    
    @classmethod
    def LEARNING_RATE(cls) -> Optional[float]:
        val = cls._get("LEARNING_RATE")
        return float(val) if val else None
    
    @classmethod
    def get_hub_model_id(cls) -> Optional[str]:
        """
        Get full HuggingFace Hub model ID.
        
        Returns:
            Model ID in format "username/model-name" or None if not configured
        """
        username = cls.HUB_USERNAME()
        model_name = cls.HUB_MODEL_NAME()
        if username and model_name:
            return f"{username}/{model_name}"
        return None

