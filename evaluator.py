"""
Evaluation module for the French-Wolof Translator.
Handles model evaluation using BLEU score and other metrics.
"""
import numpy as np
import evaluate
from transformers import AutoTokenizer
from typing import Dict, Tuple, Any


class Evaluator:
    """Handles model evaluation and metrics computation."""
    
    def __init__(self, tokenizer: AutoTokenizer):
        """
        Initialize the evaluator.
        
        Args:
            tokenizer: The tokenizer used for decoding predictions
        """
        self.tokenizer = tokenizer
        self.metric = evaluate.load("sacrebleu")
    
    def postprocess_text(self, preds: list, labels: list) -> Tuple[list, list]:
        """
        Postprocess predictions and labels for evaluation.
        
        Args:
            preds: List of predicted strings
            labels: List of label strings
            
        Returns:
            Tuple of (postprocessed_preds, postprocessed_labels)
        """
        preds = [pred.strip() for pred in preds]
        labels = [[label.strip()] for label in labels]
        return preds, labels
    
    def compute_metrics(self, eval_preds: Tuple) -> Dict[str, float]:
        """
        Compute evaluation metrics (BLEU score).
        
        Args:
            eval_preds: Tuple containing predictions and labels
            
        Returns:
            Dictionary containing computed metrics
        """
        preds, labels = eval_preds
        
        # Handle tuple predictions
        if isinstance(preds, tuple):
            preds = preds[0]
        
        # Decode predictions
        decoded_preds = self.tokenizer.batch_decode(
            preds,
            skip_special_tokens=True
        )
        
        # Decode labels (replacing -100 with pad_token_id)
        labels = np.where(
            labels != -100,
            labels,
            self.tokenizer.pad_token_id
        )
        decoded_labels = self.tokenizer.batch_decode(
            labels,
            skip_special_tokens=True
        )
        
        # Postprocess
        decoded_preds, decoded_labels = self.postprocess_text(
            decoded_preds,
            decoded_labels
        )
        
        # Compute BLEU score
        result = self.metric.compute(
            predictions=decoded_preds,
            references=decoded_labels
        )
        result = {"bleu": result["score"]}
        
        # Compute average generation length
        prediction_lens = [
            np.count_nonzero(pred != self.tokenizer.pad_token_id)
            for pred in preds
        ]
        result["gen_len"] = np.mean(prediction_lens)
        
        # Round results
        result = {k: round(v, 4) for k, v in result.items()}
        return result

