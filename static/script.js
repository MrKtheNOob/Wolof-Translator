document.addEventListener('DOMContentLoaded', () => {
    const sourceText = document.getElementById('source-text');
    const targetText = document.getElementById('target-text');
    const translateBtn = document.getElementById('translate-btn');
    const swapBtn = document.getElementById('swap-btn');
    const loader = document.getElementById('loader');
    const sourceLabel = document.getElementById('source-label');
    const targetLabel = document.getElementById('target-label');

    let currentSourceLang = 'fr';

    // Clear target if source is empty
    sourceText.addEventListener('input', () => {
        if (sourceText.value.length === 0) {
            targetText.textContent = '';
        }
    });

    // Swap languages
    swapBtn.addEventListener('click', () => {
        currentSourceLang = currentSourceLang === 'fr' ? 'wo' : 'fr';
        
        // Update Labels
        if (currentSourceLang === 'fr') {
            sourceLabel.textContent = 'French';
            targetLabel.textContent = 'Wolof';
        } else {
            sourceLabel.textContent = 'Wolof';
            targetLabel.textContent = 'French';
        }

        // Swap Content
        const temp = sourceText.value;
        sourceText.value = targetText.textContent;
        targetText.textContent = temp;
    });

    // Translation function
    async function performTranslation() {
        const text = sourceText.value.trim();
        if (!text) return;

        loader.style.display = 'block';
        
        try {
            const response = await fetch('/translate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    text: text,
                    source_lang: currentSourceLang
                })
            });

            if (!response.ok) throw new Error('Translation failed');

            const data = await response.json();
            targetText.textContent = data.translated_text;
        } catch (error) {
            targetText.textContent = 'Error: ' + error.message;
        } finally {
            loader.style.display = 'none';
        }
    }

    // Event listeners
    translateBtn.addEventListener('click', performTranslation);
    
    sourceText.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            performTranslation();
        }
    });
});
