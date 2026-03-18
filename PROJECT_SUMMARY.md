# Project Summary: Wolof-NMT Engineering & Deployment

This document summarizes the technical transformations, bug fixes, and deployment steps taken to turn the base NMT research code into a functional, production-ready translation application.

## 🛠 1. Technical Diagnostics & Bug Fixes

### The "Strange Characters" & Accuracy Issue
**Problem:** Initial runs produced gibberish or incorrect scripts.
**Root Cause:** 
1. **Missing Language Tags:** NLLB models require specific tokens (`fra_Latn`, `wol_Latn`) to set the source and target languages.
2. **Tokenizer Mismatch:** The code was using generic text prefixes (e.g., "translate French to Wolof:") which NLLB ignored.
3. **Encoding:** Standard Python `print` in some terminal environments failed to render Wolof-specific UTF-8 characters (ë, ñ).

**Solution:**
- Updated `translator.py` to inject `forced_bos_token_id` using `tokenizer.convert_tokens_to_ids(tgt_lang)`.
- Updated `config.py` to use NLLB-standard language tags.
- Implemented `safe_print` and UTF-8 buffer overrides in `main.py`.

## 🏗 2. Resource Optimization (EC2 Hardware)
**Constraint:** EC2 t3.medium (4GB RAM, 30GB Disk).
- **Model Swap:** Replaced the heavy 3.3B and 3B models (which would crash the instance) with `facebook/nllb-200-distilled-600M` (~2.4GB).
- **Memory Strategy:** Configured the API to load the model **once** on startup as a singleton to stay within the 4GB RAM limit.

## 🚀 3. Application Architecture

### Backend (FastAPI)
- **File:** `server.py`
- **Features:** 
  - Asynchronous `/translate` endpoint.
  - Startup event handler for model loading.
  - Pydantic models for request/response validation.
  - Static file serving for the frontend.

### Frontend (Google Translate Clone)
- **Directory:** `/static`
- **Structure:** Separated into `index.html`, `style.css`, and `script.js`.
- **Design:** Clean, CSS-based (non-Tailwind) UI mimicking Google Translate.
- **Credits:** Includes a shout-out to the **GalsenAI Community** in the footer.

## 📋 4. Deployment & DevOps Ready
- **Systemd Service:** Created `wolof-nmt.service` to ensure the app runs in the background and restarts on boot.
- **Environment Management:** Centralized configuration via `.env` file for easy swapping of model checkpoints.

## ⏭ 5. Future Engineering Steps
If you move into the DevOps phase, consider:
1. **Reverse Proxy:** Setting up **Nginx** on port 80/443 to forward traffic to FastAPI (port 8000).
2. **SSL:** Using **Certbot (Let's Encrypt)** for HTTPS.
3. **Monitoring:** Using `htop` or `nmon` to monitor the RAM usage when multiple users hit the API.
4. **Fine-Tuning:** Running `python train.py` to move from the "Distilled" base knowledge to specialized French-Wolof expertise.

---
**Shout out to GalsenAI for the foundational dataset and research.**
**Project Version:** 1.0.0
**Status:** Deployed & Functional
