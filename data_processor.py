"""
Data processing module for the French-Wolof Translator.
Handles dataset loading, preprocessing, and tokenization.
"""
from datasets import load_dataset, DatasetDict
from transformers import AutoTokenizer
from typing import Dict, Any
from config import DatasetConfig, ModelConfig


class DataProcessor:
    """Handles all data processing operations."""
    
    def __init__(
        self,
        tokenizer: AutoTokenizer,
        dataset_config: DatasetConfig,
        model_config: ModelConfig
    ):
        """
        Initialize the data processor.
        
        Args:
            tokenizer: The tokenizer to use for preprocessing
            dataset_config: Dataset configuration
            model_config: Model configuration
        """
        self.tokenizer = tokenizer
        self.dataset_config = dataset_config
        self.model_config = model_config
    
    def load_dataset(self) -> DatasetDict:
        """
        Load the dataset from HuggingFace.
        
        Returns:
            DatasetDict containing the loaded dataset
        """
        dataset_dict = load_dataset(self.dataset_config.dataset_name)
        return dataset_dict
    
    def split_dataset(self, dataset_dict: DatasetDict) -> DatasetDict:
        """
        Split the dataset into train and test sets.
        
        Args:
            dataset_dict: The dataset dictionary
            
        Returns:
            DatasetDict with train and test splits
        """
        dataset_dict = dataset_dict["train"].train_test_split(
            test_size=self.dataset_config.test_size
        )
        return dataset_dict
    
    def preprocess_function(self, examples: Dict[str, Any]) -> Dict[str, Any]:
        """
        Preprocess examples for training.
        
        Args:
            examples: Dictionary containing source and target language examples
            
        Returns:
            Preprocessed examples with tokenized inputs and labels
        """
        # NLLB uses specific language tags
        self.tokenizer.src_lang = "fra_Latn"
        
        # Dataset column names (keeping 'french' and 'wolof' for data access)
        inputs = [self.dataset_config.prefix_fr_to_wo + text for text in examples["french"]]
        targets = [text for text in examples["wolof"]]
        
        model_inputs = self.tokenizer(
            inputs,
            max_length=self.model_config.max_length,
            truncation=True
        )
        
        # Tokenize targets with the target language tag
        with self.tokenizer.as_target_tokenizer():
            labels = self.tokenizer(
                targets,
                max_length=self.model_config.max_length,
                truncation=True
            )
            
        model_inputs["labels"] = labels["input_ids"]
        return model_inputs
    
    def preprocess_dataset(self, dataset_dict: DatasetDict) -> DatasetDict:
        """
        Preprocess the entire dataset.
        
        Args:
            dataset_dict: The dataset dictionary to preprocess
            
        Returns:
            Preprocessed dataset dictionary
        """
        dataset_dict = dataset_dict.map(self.preprocess_function)
        return dataset_dict
    
    def prepare_dataset(self) -> DatasetDict:
        """
        Complete dataset preparation pipeline.
        
        Returns:
            Fully prepared dataset dictionary
        """
        dataset_dict = self.load_dataset()
        dataset_dict = self.split_dataset(dataset_dict)
        dataset_dict = self.preprocess_dataset(dataset_dict)
        return dataset_dict

