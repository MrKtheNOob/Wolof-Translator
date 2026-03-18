"""
Configuration settings for the French-Wolof Translator.
Centralizes all configuration parameters for easy modification.
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class ModelConfig:
    """Model configuration parameters."""
    checkpoint: str = "facebook/nllb-200-distilled-600M"  # Override with MODEL_CHECKPOINT env var
    source_lang: str = "fra_Latn"
    target_lang: str = "wol_Latn"
    max_length: int = 128
    max_generation_length: int = 30
    
    def __post_init__(self):
        """Override with environment variables if available."""
        try:
            from env_config import EnvConfig
            checkpoint = EnvConfig.MODEL_CHECKPOINT()
            if checkpoint:
                self.checkpoint = checkpoint
        except ImportError:
            pass  # env_config not available, use default


@dataclass
class TrainingConfig:
    """Training configuration parameters."""
    output_dir: str = "wolofToFrenchTranslator_nllb"  # Override with OUTPUT_DIR env var
    eval_strategy: str = "epoch"
    learning_rate: float = 2e-5  # Override with LEARNING_RATE env var
    per_device_train_batch_size: int = 8
    per_device_eval_batch_size: int = 8
    weight_decay: float = 0.01
    save_total_limit: int = 3
    num_train_epochs: int = 2  # Override with NUM_TRAIN_EPOCHS env var
    fp16: bool = True
    push_to_hub: bool = False
    hub_model_id: Optional[str] = None  # Auto-set from HUB_USERNAME/HUB_MODEL_NAME env vars
    hub_token: Optional[str] = None  # Override with HF_TOKEN env var
    
    def __post_init__(self):
        """Override with environment variables if available."""
        try:
            from env_config import EnvConfig
            output_dir = EnvConfig.OUTPUT_DIR()
            if output_dir:
                self.output_dir = output_dir
            learning_rate = EnvConfig.LEARNING_RATE()
            if learning_rate:
                self.learning_rate = learning_rate
            num_epochs = EnvConfig.NUM_TRAIN_EPOCHS()
            if num_epochs:
                self.num_train_epochs = num_epochs
            hf_token = EnvConfig.HF_TOKEN()
            if hf_token:
                self.hub_token = hf_token
            if not self.hub_model_id:
                self.hub_model_id = EnvConfig.get_hub_model_id()
        except ImportError:
            pass  # env_config not available, use defaults


@dataclass
class DatasetConfig:
    """Dataset configuration parameters."""
    dataset_name: str = "galsenai/french-wolof-translation"  # Override with DATASET_NAME env var
    test_size: float = 0.2
    prefix_fr_to_wo: str = ""
    prefix_wo_to_fr: str = ""
    
    def __post_init__(self):
        """Override with environment variables if available."""
        try:
            from env_config import EnvConfig
            dataset_name = EnvConfig.DATASET_NAME()
            if dataset_name:
                self.dataset_name = dataset_name
        except ImportError:
            pass  # env_config not available, use default


@dataclass
class WandbConfig:
    """Weights & Biases configuration."""
    enabled: bool = False  # Override with WANDB_ENABLED env var
    api_key: Optional[str] = None  # Override with WANDB_API_KEY env var
    project_name: Optional[str] = None  # Override with WANDB_PROJECT_NAME env var
    
    def __post_init__(self):
        """Override with environment variables if available."""
        try:
            from env_config import EnvConfig
            if EnvConfig.WANDB_ENABLED():
                self.enabled = True
            wandb_key = EnvConfig.WANDB_API_KEY()
            if wandb_key:
                self.api_key = wandb_key
            wandb_project = EnvConfig.WANDB_PROJECT_NAME()
            if wandb_project:
                self.project_name = wandb_project
        except ImportError:
            pass  # env_config not available, use defaults

