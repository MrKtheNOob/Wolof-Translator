# French-Wolof Translator

A modular, production-ready French-Wolof translation system built on Facebook's NLLB (No Language Left Behind) model. This project provides a complete framework for training, evaluating, and using bidirectional translation models between French and Wolof.

## 📋 Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [Usage](#usage)
- [Training](#training)
- [Configuration](#configuration)
- [Versioning](#versioning)
- [Contributing](#contributing)
- [License](#license)

> 📖 **For detailed configuration instructions, see [CONFIGURATION.md](CONFIGURATION.md)**

## ✨ Features

- **Bidirectional Translation**: Translate between French and Wolof in both directions
- **Modular Architecture**: Clean, maintainable codebase organized into logical modules
- **Easy Training**: Simple interface for fine-tuning models on custom datasets
- **Evaluation Metrics**: Built-in BLEU score evaluation for model assessment
- **HuggingFace Integration**: Seamless integration with HuggingFace Hub for model sharing
- **Flexible Configuration**: Centralized configuration system for easy customization
- **Version Control**: Semantic versioning system for tracking releases

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- CUDA-capable GPU (recommended for training, optional for inference)

### Install from Source

1. Clone the repository:
```bash
git clone git@github-second:Galsenaicommunity/Wolof-NMT.git
cd Wolof-NMT
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your settings
# At minimum, you may want to set:
# - MODEL_CHECKPOINT (if using a custom trained model)
# - HF_TOKEN (if pushing models to HuggingFace Hub)
# - WANDB_API_KEY (if using Weights & Biases)
```

4. (Optional) Install as a package:
```bash
pip install -e .
```

## 🏃 Quick Start

### Configuration

Before using the translator, configure your environment variables. Create a `.env` file from the example:

```bash
cp .env.example .env
```

Edit `.env` with your settings. The most important variables are:

- **MODEL_CHECKPOINT**: Your model checkpoint (default: `facebook/nllb-200-distilled-600M`)
- **DATASET_NAME**: Dataset name for training (default: `galsenai/french-wolof-translation`)
- **HF_TOKEN**: HuggingFace token (required only if pushing models to Hub)
- **HUB_USERNAME** and **HUB_MODEL_NAME**: For pushing trained models to HuggingFace Hub
- **WANDB_API_KEY**: Weights & Biases API key (optional, for experiment tracking)

### Using a Pre-trained Model

```python
from translator import FrenchWolofTranslator

# Initialize translator
# Model checkpoint can be set via MODEL_CHECKPOINT env var or passed directly
translator = FrenchWolofTranslator(
    model_checkpoint="your-username/your-model-name"  # Or use env var
)

# Translate French to Wolof
wolof_text = translator.translate_french_to_wolof("Bonjour")
print(wolof_text)

# Translate Wolof to French
french_text = translator.translate_wolof_to_french("Naka nga def?")
print(french_text)

# Generic translation method
result = translator.translate("Comment allez-vous?", source_lang="fr")
print(result)
```

### Running the Example

```bash
# Uses MODEL_CHECKPOINT from .env, or prompts for input
python main.py

# Or specify model checkpoint directly
python main.py "your-username/your-model-name"
```

## 📁 Project Structure

```
.
├── version.py              # Version information
├── config.py               # Configuration classes
├── env_config.py           # Environment variable loader
├── data_processor.py       # Dataset loading and preprocessing
├── trainer.py              # Model training logic
├── evaluator.py            # Evaluation metrics
├── translator.py           # Main translation interface
├── main.py                 # Example usage script
├── train.py                # Training script
├── requirements.txt        # Python dependencies
├── setup.py                # Package setup
├── .env.example            # Example environment configuration
├── .gitignore              # Git ignore rules
└── README.md               # This file
```

### Module Descriptions

- **`version.py`**: Contains version information using semantic versioning
- **`config.py`**: Centralized configuration classes for model, training, dataset, and wandb settings
- **`data_processor.py`**: Handles dataset loading, splitting, and preprocessing
- **`trainer.py`**: Manages model training, fine-tuning, and evaluation
- **`evaluator.py`**: Computes evaluation metrics (BLEU score)
- **`translator.py`**: Main translation interface for end users
- **`main.py`**: Example script demonstrating translator usage
- **`train.py`**: Complete training pipeline script

## 💻 Usage

### Basic Translation

```python
from translator import FrenchWolofTranslator

translator = FrenchWolofTranslator(
    model_checkpoint="galsenai/wolofToFrenchTranslator_nllb"
)

# Method 1: Using convenience methods
wolof = translator.translate_french_to_wolof("Bonjour")
french = translator.translate_wolof_to_french("Naka nga def?")

# Method 2: Using generic translate method
wolof = translator.translate("Bonjour", source_lang="fr")
french = translator.translate("Naka nga def?", source_lang="wo")
```

### Custom Configuration

```python
from translator import FrenchWolofTranslator
from config import ModelConfig, DatasetConfig

# Custom model configuration
model_config = ModelConfig(
    max_generation_length=50,
    max_length=256
)

# Custom dataset configuration
dataset_config = DatasetConfig(
    prefix_fr_to_wo="Translate from French to Wolof: ",
    prefix_wo_to_fr="Translate from Wolof to French: "
)

translator = FrenchWolofTranslator(
    model_checkpoint="your-model-checkpoint",
    model_config=model_config,
    dataset_config=dataset_config
)
```

### Device Selection

```python
# Use CPU
translator = FrenchWolofTranslator(
    model_checkpoint="galsenai/wolofToFrenchTranslator_nllb",
    device="cpu"
)

# Use CUDA (default if available)
translator = FrenchWolofTranslator(
    model_checkpoint="galsenai/wolofToFrenchTranslator_nllb",
    device="cuda"
)

# Auto-detect (default)
translator = FrenchWolofTranslator(
    model_checkpoint="galsenai/wolofToFrenchTranslator_nllb"
)
```

## 🎓 Training

### Training a New Model

1. **Configure Environment Variables**:

Edit your `.env` file with training settings:

```bash
# Required for training
MODEL_CHECKPOINT=facebook/nllb-200-distilled-600M
DATASET_NAME=galsenai/french-wolof-translation

# Optional: Override training parameters
OUTPUT_DIR=my_translator_model
NUM_TRAIN_EPOCHS=3
LEARNING_RATE=2e-5

# Optional: Push to HuggingFace Hub after training
HUB_USERNAME=your_username
HUB_MODEL_NAME=my-translator-model
HF_TOKEN=your_huggingface_token

# Optional: Weights & Biases tracking
WANDB_ENABLED=true
WANDB_API_KEY=your_wandb_key
WANDB_PROJECT_NAME=french-wolof-translator
```

2. **Run Training**:

```bash
python train.py
```

The script will automatically load configuration from your `.env` file.

### Training with Weights & Biases

Configure in your `.env` file:

```bash
WANDB_ENABLED=true
WANDB_API_KEY=your-wandb-api-key
WANDB_PROJECT_NAME=french-wolof-translator
```

The training script will automatically use these settings.

### Pushing Model to HuggingFace Hub

Configure in your `.env` file:

```bash
HUB_USERNAME=your_username
HUB_MODEL_NAME=your-model-name
HF_TOKEN=your_huggingface_token
```

The training script will automatically push to Hub after training if these are set.

Or manually push after training:

```python
from translator import FrenchWolofTranslator
from env_config import EnvConfig

translator = FrenchWolofTranslator(model_checkpoint="local-model-path")
translator.push_to_hub(
    hub_model_id=EnvConfig.get_hub_model_id(),
    token=EnvConfig.HF_TOKEN
)
```

## ⚙️ Configuration

### Environment Variables

The project uses environment variables for secure configuration. All sensitive information (tokens, API keys) should be stored in a `.env` file (see `.env.example`).

**Required for training:**
- `MODEL_CHECKPOINT`: Base model checkpoint (default: `facebook/nllb-200-distilled-600M`)
- `DATASET_NAME`: Dataset name from HuggingFace Hub (default: `galsenai/french-wolof-translation`)

**Optional for training:**
- `OUTPUT_DIR`: Output directory for trained models
- `NUM_TRAIN_EPOCHS`: Number of training epochs
- `LEARNING_RATE`: Learning rate for training

**For HuggingFace Hub:**
- `HF_TOKEN`: Your HuggingFace authentication token
- `HUB_USERNAME`: Your HuggingFace username/organization
- `HUB_MODEL_NAME`: Model name for Hub (creates `HUB_USERNAME/HUB_MODEL_NAME`)

**For Weights & Biases:**
- `WANDB_ENABLED`: Set to `true` to enable wandb logging
- `WANDB_API_KEY`: Your Weights & Biases API key
- `WANDB_PROJECT_NAME`: Project name for wandb

### Programmatic Configuration

You can also configure programmatically (values will override environment variables):

```python
from config import ModelConfig, TrainingConfig, DatasetConfig

model_config = ModelConfig(
    checkpoint="facebook/nllb-200-distilled-600M",
    source_lang="french",
    target_lang="wolof",
    max_length=128,              # Maximum input length
    max_generation_length=30     # Maximum output length
)

training_config = TrainingConfig(
    output_dir="output_directory",
    eval_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    weight_decay=0.01,
    save_total_limit=3,
    num_train_epochs=2,
    fp16=True,                   # Use mixed precision training
    push_to_hub=False,
    hub_model_id=None,
    hub_token=None
)

dataset_config = DatasetConfig(
    dataset_name="galsenai/french-wolof-translation",
    test_size=0.2,
    prefix_fr_to_wo="translate French to Wolof: ",
    prefix_wo_to_fr="translate Wolof to French: "
)
```

## 📊 Versioning

This project uses [Semantic Versioning](https://semver.org/) (SemVer):

- **MAJOR** version for incompatible API changes
- **MINOR** version for backwards-compatible functionality additions
- **PATCH** version for backwards-compatible bug fixes

Current version: **1.0.0**

Version information is stored in `version.py` and can be accessed programmatically:

```python
from version import __version__, __version_info__
print(__version__)  # "1.0.0"
print(__version_info__)  # (1, 0, 0)
```

## 📈 Evaluation

The model is evaluated using the BLEU (Bilingual Evaluation Understudy) score, which measures the quality of machine translation output by comparing it to reference translations.

After training, evaluation metrics are automatically computed and displayed:

```python
trainer = ModelTrainer(...)
metrics = trainer.evaluate(eval_dataset)
print(f"BLEU Score: {metrics['eval_bleu']:.2f}")
```

## 🔧 Development

### Running Tests

```bash
# Add tests as needed
python -m pytest tests/
```

### Code Structure Guidelines

- Each module has a single, well-defined responsibility
- Configuration is centralized in `config.py`
- All classes and functions are documented with docstrings
- Type hints are used throughout for better code clarity

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [Facebook AI Research](https://ai.meta.com/research/) for the NLLB (No Language Left Behind) model
- [HuggingFace](https://huggingface.co) for the Transformers library and infrastructure
- [GalsenAI](https://galsen.ai/) for the French-Wolof translation dataset

## 📧 Contact

For questions, issues, or contributions, please open an issue on the repository.

---

**Version**: 1.0.0  
**Last Updated**: 2025

# Wolof-Translator
