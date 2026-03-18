"""
Training module for the French-Wolof Translator.
Handles model training and fine-tuning.
"""
from transformers import (
    AutoModelForSeq2SeqLM,
    AutoTokenizer,
    Seq2SeqTrainingArguments,
    Seq2SeqTrainer,
    DataCollatorForSeq2Seq
)
from datasets import DatasetDict
from typing import Optional
import wandb

from config import TrainingConfig, WandbConfig
from evaluator import Evaluator


class ModelTrainer:
    """Handles model training operations."""
    
    def __init__(
        self,
        model_config_checkpoint: str,
        training_config: TrainingConfig,
        wandb_config: Optional[WandbConfig] = None
    ):
        """
        Initialize the trainer.
        
        Args:
            model_config_checkpoint: Model checkpoint to use
            training_config: Training configuration
            wandb_config: Optional Weights & Biases configuration
        """
        self.model_config_checkpoint = model_config_checkpoint
        self.training_config = training_config
        self.wandb_config = wandb_config
        
        # Initialize tokenizer and model
        self.tokenizer = AutoTokenizer.from_pretrained(
            model_config_checkpoint,
            src_lang="fra_Latn"
        )
        self.tokenizer.tgt_lang = "wol_Latn"
        self.model = AutoModelForSeq2SeqLM.from_pretrained(
            model_config_checkpoint
        )
        
        # Initialize evaluator
        self.evaluator = Evaluator(self.tokenizer)
        
        # Setup wandb if enabled
        if wandb_config and wandb_config.enabled:
            if wandb_config.api_key:
                wandb.login(key=wandb_config.api_key)
            if wandb_config.project_name:
                wandb.init(project=wandb_config.project_name)
    
    def create_training_arguments(self) -> Seq2SeqTrainingArguments:
        """
        Create training arguments from configuration.
        
        Returns:
            Seq2SeqTrainingArguments object
        """
        training_args = Seq2SeqTrainingArguments(
            output_dir=self.training_config.output_dir,
            eval_strategy=self.training_config.eval_strategy,
            learning_rate=self.training_config.learning_rate,
            per_device_train_batch_size=self.training_config.per_device_train_batch_size,
            per_device_eval_batch_size=self.training_config.per_device_eval_batch_size,
            weight_decay=self.training_config.weight_decay,
            save_total_limit=self.training_config.save_total_limit,
            num_train_epochs=self.training_config.num_train_epochs,
            predict_with_generate=True,
            fp16=self.training_config.fp16,
            push_to_hub=self.training_config.push_to_hub,
            hub_model_id=self.training_config.hub_model_id,
            hub_token=self.training_config.hub_token,
        )
        return training_args
    
    def create_data_collator(self) -> DataCollatorForSeq2Seq:
        """
        Create data collator for batching.
        
        Returns:
            DataCollatorForSeq2Seq object
        """
        data_collator = DataCollatorForSeq2Seq(
            tokenizer=self.tokenizer,
            model=self.model
        )
        return data_collator
    
    def create_trainer(
        self,
        train_dataset: DatasetDict,
        eval_dataset: DatasetDict
    ) -> Seq2SeqTrainer:
        """
        Create the trainer instance.
        
        Args:
            train_dataset: Training dataset
            eval_dataset: Evaluation dataset
            
        Returns:
            Seq2SeqTrainer instance
        """
        training_args = self.create_training_arguments()
        data_collator = self.create_data_collator()
        
        trainer = Seq2SeqTrainer(
            model=self.model,
            args=training_args,
            train_dataset=train_dataset,
            eval_dataset=eval_dataset,
            processing_class=self.tokenizer,
            data_collator=data_collator,
            compute_metrics=self.evaluator.compute_metrics,
        )
        return trainer
    
    def train(
        self,
        train_dataset: DatasetDict,
        eval_dataset: DatasetDict
    ) -> dict:
        """
        Train the model.
        
        Args:
            train_dataset: Training dataset
            eval_dataset: Evaluation dataset
            
        Returns:
            Dictionary containing training metrics
        """
        trainer = self.create_trainer(train_dataset, eval_dataset)
        train_result = trainer.train()
        return train_result.metrics
    
    def evaluate(self, eval_dataset: DatasetDict) -> dict:
        """
        Evaluate the model.
        
        Args:
            eval_dataset: Evaluation dataset
            
        Returns:
            Dictionary containing evaluation metrics
        """
        trainer = self.create_trainer(eval_dataset, eval_dataset)
        metrics = trainer.evaluate()
        return metrics

