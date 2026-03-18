"""
Training script for the French-Wolof Translator.
Use this script to train or fine-tune the translation model.

Configuration is loaded from environment variables (see .env.example).
Create a .env file with your settings before running.
"""
from transformers import AutoTokenizer
from data_processor import DataProcessor
from trainer import ModelTrainer
from config import (
    ModelConfig,
    TrainingConfig,
    DatasetConfig,
    WandbConfig
)
from env_config import EnvConfig
from version import __version__


def main():
    """Main training function."""
    print(f"French-Wolof Translator Training v{__version__}")
    print("=" * 50)
    
    # Configuration (automatically loads from environment variables)
    model_config = ModelConfig()
    training_config = TrainingConfig(
        push_to_hub=EnvConfig.get_hub_model_id() is not None
    )
    dataset_config = DatasetConfig()
    
    # Weights & Biases configuration (from environment variables)
    wandb_config = WandbConfig()
    
    # Display configuration
    print("\nConfiguration:")
    print(f"  Model checkpoint: {model_config.checkpoint}")
    print(f"  Dataset: {dataset_config.dataset_name}")
    print(f"  Output directory: {training_config.output_dir}")
    print(f"  Push to hub: {training_config.push_to_hub}")
    if training_config.push_to_hub:
        print(f"  Hub model ID: {training_config.hub_model_id}")
    print(f"  Wandb enabled: {wandb_config.enabled}")
    
    if training_config.push_to_hub and not training_config.hub_token:
        print("\n⚠️  WARNING: push_to_hub is enabled but HF_TOKEN is not set!")
        print("   Set HF_TOKEN in your .env file to push models to HuggingFace Hub.")
        try:
            response = input("   Continue without pushing to hub? (y/n): ")
            if response.lower() != 'y':
                print("   Exiting. Please configure your .env file.")
                return
        except (EOFError, KeyboardInterrupt):
            print("\n   Exiting. Please configure your .env file.")
            return
        training_config.push_to_hub = False
    
    # Initialize tokenizer
    tokenizer = AutoTokenizer.from_pretrained(
        model_config.checkpoint,
        src_lang="fra_Latn"
    )
    
    # Process dataset
    print("\nLoading and preprocessing dataset...")
    data_processor = DataProcessor(
        tokenizer=tokenizer,
        dataset_config=dataset_config,
        model_config=model_config
    )
    dataset_dict = data_processor.prepare_dataset()
    print(f"Dataset prepared: {len(dataset_dict['train'])} train samples, "
          f"{len(dataset_dict['test'])} test samples")
    
    # Initialize trainer
    print("\nInitializing trainer...")
    trainer = ModelTrainer(
        model_config_checkpoint=model_config.checkpoint,
        training_config=training_config,
        wandb_config=wandb_config if wandb_config.enabled else None
    )
    
    # Train model
    print("\nStarting training...")
    train_metrics = trainer.train(
        train_dataset=dataset_dict["train"],
        eval_dataset=dataset_dict["test"]
    )
    print(f"\nTraining completed!")
    print(f"Training metrics: {train_metrics}")
    
    # Evaluate model
    print("\nEvaluating model...")
    eval_metrics = trainer.evaluate(dataset_dict["test"])
    print(f"Evaluation metrics: {eval_metrics}")
    
    if "eval_bleu" in eval_metrics:
        print(f"\nFinal BLEU Score: {eval_metrics['eval_bleu']:.2f}")
    elif "bleu" in eval_metrics:
        print(f"\nFinal BLEU Score: {eval_metrics['bleu']:.2f}")


if __name__ == "__main__":
    main()

