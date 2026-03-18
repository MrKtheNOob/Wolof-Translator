"""
Main entry point for the French-Wolof Translator.
Demonstrates usage of the modular translator system.

The model checkpoint can be specified via:
1. MODEL_CHECKPOINT environment variable
2. Command line argument
3. Interactive prompt
"""
import sys
import io
from translator import FrenchWolofTranslator
from config import ModelConfig, DatasetConfig
from env_config import EnvConfig
from version import __version__

def safe_print(text):
    """Prints text with safe encoding handling."""
    try:
        print(text)
    except UnicodeEncodeError:
        print(text.encode('ascii', 'replace').decode('ascii'))

def main():
    """Main function demonstrating translator usage."""
    # Ensure UTF-8 output if possible
    if hasattr(sys.stdout, 'buffer'):
        try:
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        except Exception:
            pass

    print(f"French-Wolof Translator v{__version__}")
    print("=" * 50)
    
    # Get model checkpoint from various sources
    if len(sys.argv) > 1:
        # From command line argument
        model_checkpoint = sys.argv[1]
        print(f"Using model checkpoint from command line: {model_checkpoint}")
    else:
        # Try environment variable first
        model_checkpoint = EnvConfig.MODEL_CHECKPOINT()
        
        # If using default, prompt user
        if model_checkpoint == "":
            print("\nNo model checkpoint specified.")
            print("You can:")
            print("  1. Set MODEL_CHECKPOINT in your .env file")
            print("  2. Pass it as command line argument: python main.py <model_checkpoint>")
            print("  3. Enter it now (or press Enter to use base model)")
            try:
                user_input = input("\nModel checkpoint (or Enter for base model): ").strip()
                if user_input:
                    model_checkpoint = user_input
                else:
                    print("Using base NLLB model (may not be fine-tuned for French-Wolof)")
            except (EOFError, KeyboardInterrupt):
                print("\nUsing base NLLB model (may not be fine-tuned for French-Wolof)")
    
    print(f"\nLoading model: {model_checkpoint}")
    
    translator = FrenchWolofTranslator(
        model_checkpoint=model_checkpoint,
        model_config=ModelConfig(),
        dataset_config=DatasetConfig()
    )
    
    # Example translations
    print("\n1. French to Wolof:")
    french_text = "Bonjour"
    wolof_translation = translator.translate_french_to_wolof(french_text)
    safe_print(f"   French: {french_text}")
    safe_print(f"   Wolof:  {wolof_translation}")
    
    print("\n2. Wolof to French:")
    wolof_text = "Naka nga def?"
    french_translation = translator.translate_wolof_to_french(wolof_text)
    safe_print(f"   Wolof:  {wolof_text}")
    safe_print(f"   French: {french_translation}")
    
    print("\n3. Using generic translate method:")
    result = translator.translate("Comment allez-vous?", source_lang="fr")
    safe_print(f"   Input:  Comment allez-vous?")
    safe_print(f"   Output: {result}")


if __name__ == "__main__":
    main()

