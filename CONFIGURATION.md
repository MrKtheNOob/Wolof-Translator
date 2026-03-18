# Configuration Guide

This guide explains how to configure the French-Wolof Translator for open-source deployment.

## 🔐 Security Best Practices

**Never commit sensitive information to version control!**

- All tokens, API keys, and personal identifiers should be stored in `.env` file
- The `.env` file is already in `.gitignore` and will not be committed
- Use `.env.example` as a template (this file is safe to commit)

## 📝 Environment Variables

### Required Variables

None of the variables are strictly required, but some are needed for specific features:

#### For Basic Usage
- **MODEL_CHECKPOINT**: Model checkpoint path (default: `facebook/nllb-200-distilled-600M`)
  - Can be a HuggingFace model ID (e.g., `username/model-name`)
  - Or a local path to a trained model

#### For Training
- **DATASET_NAME**: Dataset name from HuggingFace Hub (default: `galsenai/french-wolof-translation`)

### Optional Variables

#### HuggingFace Hub Integration
- **HF_TOKEN**: Your HuggingFace authentication token
  - Get it from: https://huggingface.co/settings/tokens
  - Required only if you want to push models to HuggingFace Hub
  
- **HUB_USERNAME**: Your HuggingFace username or organization name
  - Used to create model ID: `HUB_USERNAME/HUB_MODEL_NAME`
  
- **HUB_MODEL_NAME**: Name for your model on HuggingFace Hub
  - Combined with HUB_USERNAME to create the full model ID

#### Weights & Biases (Experiment Tracking)
- **WANDB_ENABLED**: Set to `true` to enable wandb logging (default: `false`)
- **WANDB_API_KEY**: Your Weights & Biases API key
  - Get it from: https://wandb.ai/authorize
  - Required only if WANDB_ENABLED is `true`
  
- **WANDB_PROJECT_NAME**: Project name for wandb (default: `french-wolof-translator`)

#### Training Overrides
- **OUTPUT_DIR**: Output directory for trained models (default: `wolofToFrenchTranslator_nllb`)
- **NUM_TRAIN_EPOCHS**: Number of training epochs (default: `2`)
- **LEARNING_RATE**: Learning rate for training (default: `2e-5`)

## 🚀 Quick Setup

1. **Copy the example file:**
   ```bash
   cp .env.example .env
   ```

2. **Edit `.env` with your values:**
   ```bash
   # Use your favorite editor
   nano .env
   # or
   vim .env
   # or
   code .env
   ```

3. **Fill in your values:**
   ```bash
   # Minimum configuration for training
   MODEL_CHECKPOINT=facebook/nllb-200-distilled-600M
   DATASET_NAME=galsenai/french-wolof-translation
   
   # If you want to push to HuggingFace Hub
   HUB_USERNAME=your_username
   HUB_MODEL_NAME=my-translator
   HF_TOKEN=hf_your_token_here
   
   # If you want to use Weights & Biases
   WANDB_ENABLED=true
   WANDB_API_KEY=your_wandb_key_here
   ```

## 📋 Example Configurations

### Minimal Configuration (Inference Only)
```bash
# .env
MODEL_CHECKPOINT=username/pretrained-model
```

### Training Without Hub Push
```bash
# .env
MODEL_CHECKPOINT=facebook/nllb-200-distilled-600M
DATASET_NAME=galsenai/french-wolof-translation
OUTPUT_DIR=my_trained_model
NUM_TRAIN_EPOCHS=3
```

### Full Configuration (Training + Hub Push + Wandb)
```bash
# .env
MODEL_CHECKPOINT=facebook/nllb-200-distilled-600M
DATASET_NAME=galsenai/french-wolof-translation
OUTPUT_DIR=my_trained_model
NUM_TRAIN_EPOCHS=3
LEARNING_RATE=2e-5

HUB_USERNAME=my_username
HUB_MODEL_NAME=french-wolof-translator
HF_TOKEN=hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

WANDB_ENABLED=true
WANDB_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
WANDB_PROJECT_NAME=my-translation-project
```

## 🔄 How It Works

1. The `env_config.py` module loads variables from your `.env` file using `python-dotenv`
2. Configuration classes in `config.py` automatically read from `EnvConfig` in their `__post_init__` methods
3. You can still override values programmatically if needed
4. Environment variables take precedence over defaults but can be overridden by programmatic values

## ⚠️ Troubleshooting

### "Required environment variable is not set"
- Make sure you've created a `.env` file
- Check that the variable name matches exactly (case-sensitive)
- Verify the `.env` file is in the project root directory

### "Module 'env_config' not found"
- Make sure `python-dotenv` is installed: `pip install python-dotenv`
- Check that `env_config.py` is in your Python path

### Variables not being loaded
- Ensure `.env` file is in the project root (same directory as `env_config.py`)
- Check for typos in variable names
- Verify there are no spaces around the `=` sign in `.env` file
- Make sure values don't have quotes unless necessary (e.g., `HF_TOKEN=token` not `HF_TOKEN="token"`)

## 🔒 Security Reminders

- ✅ `.env` is in `.gitignore` - safe to use
- ✅ `.env.example` is safe to commit (contains no real values)
- ❌ Never commit `.env` file
- ❌ Never hardcode tokens in source code
- ❌ Never share your `.env` file

