# GEMINI.md - French-Wolof NMT Project Context

This document provides essential context and instructions for AI agents working on the French-Wolof Neural Machine Translation (NMT) project.

## 🚀 Project Overview
This project is a modular, production-ready French-Wolof translation system built on Meta's **NLLB (No Language Left Behind)** model. It provides a complete framework for training, evaluating, and using bidirectional translation models.

- **Primary Languages:** French (fra_Latn), Wolof (wol_Latn)
- **Core Stack:** Python 3.8+, PyTorch, Hugging Face (Transformers, Datasets, Evaluate), SacreBLEU, Weights & Biases (WandB).
- **Architecture:** Modular and object-oriented, separating configuration, data processing, training, and inference.

## 📁 Key Components
- `translator.py`: Contains `FrenchWolofTranslator`, the high-level API for inference.
- `trainer.py`: Contains `ModelTrainer` for fine-tuning and evaluation.
- `data_processor.py`: Manages dataset loading, splitting, and tokenization.
- `config.py`: Centralized configuration using Python dataclasses.
- `env_config.py`: Integrates environment variables (via `python-dotenv`) into the configuration system.
- `evaluator.py`: Logic for computing BLEU scores.
- `main.py`: CLI entry point for translation demonstrations.
- `train.py`: CLI entry point for the training pipeline.

## 🛠️ Building and Running

### Setup
```bash
# Install dependencies
pip install -r requirements.txt

# (Optional) Install as editable package
pip install -e .
```

### Configuration
The project relies heavily on environment variables defined in a `.env` file.
Key variables include:
- `MODEL_CHECKPOINT`: The base or fine-tuned model (e.g., `facebook/nllb-200-distilled-600M`).
- `DATASET_NAME`: Hugging Face dataset (default: `galsenai/french-wolof-translation`).
- `HF_TOKEN`: Required for pushing models to the Hub.
- `WANDB_API_KEY`: Required for experiment tracking.

### Commands
- **Inference:** `python main.py [optional_checkpoint]`
- **Training:** `python train.py`
- **Tests:** `python -m pytest tests/` (Note: Ensure tests directory exists)

## 📏 Development Conventions

### 1. Configuration Management
Always use the classes in `config.py` (`ModelConfig`, `TrainingConfig`, etc.) to manage parameters. These classes automatically prioritize environment variables from `env_config.py`.

### 2. Modular Responsibility
Maintain the existing separation of concerns:
- Do not add training logic to `translator.py`.
- Keep preprocessing logic within `data_processor.py`.
- Add new metrics to `evaluator.py`.

### 3. Versioning
The project follows **Semantic Versioning (SemVer)**. The current version is tracked in `version.py`. Update this file when making significant changes or releases.

### 4. Code Quality
- Use **type hints** for all function signatures.
- Provide **Google-style docstrings** for classes and functions.
- Prefer **Vanilla Python** and standard library features where possible, unless a library like `transformers` is already established.

### 5. Integration
When adding features, ensure they integrate with:
- **Hugging Face Hub:** Supporting `push_to_hub`.
- **WandB:** Supporting experiment logging if enabled.

## 📊 Evaluation
The primary metric for this project is the **BLEU score**. Always validate model changes by running evaluation through the `ModelTrainer.evaluate()` method or the `evaluator.py` module.
