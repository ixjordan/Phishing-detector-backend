#!/usr/bin/env python3
from pathlib import Path
import os
from huggingface_hub import HfApi, login, whoami

# Optional: silence tokenizers warning
os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")

# ---- Paths (project root = parent of this script's folder) ----
THIS_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = THIS_DIR.parent          # utils/ -> project root
LOCAL_MODEL_PATH = PROJECT_ROOT / "artifacts" / "distilbert_phishing"

if not LOCAL_MODEL_PATH.is_dir():
    raise SystemExit(f"❌ Model folder not found: {LOCAL_MODEL_PATH}")

# ---- Hugging Face repo ----
HF_USERNAME = "your-username"           # <-- change this
REPO_NAME   = "distilbert_phishing_sms" # or your preferred name
REPO_ID     = f"{HF_USERNAME}/{REPO_NAME}"

# ---- Auth (will prompt once per venv if not cached) ----
try:
    whoami()
except Exception:
    login()  # or: login(token="hf_...")

# ---- Create repo if needed & upload (skip checkpoints) ----
api = HfApi()
api.create_repo(repo_id=REPO_ID, private=True, exist_ok=True)
print(f"Repo ready: {REPO_ID}")

print(f"Uploading: {LOCAL_MODEL_PATH} -> {REPO_ID}")
api.upload_folder(
    folder_path=str(LOCAL_MODEL_PATH),
    repo_id=REPO_ID,
    repo_type="model",
    commit_message="Upload model export",
    ignore_patterns=["training/**", "**/checkpoint-*", "*.ckpt", "*.bin.tmp"]
)
print(f"✅ Upload complete: https://huggingface.co/{REPO_ID}")
