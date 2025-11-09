# backend/db/init_supabase.py
import os, re
from pathlib import Path
from supabase import create_client
from dotenv import load_dotenv

# Always load the .env that sits in the backend/ folder
ENV_PATH = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(dotenv_path=ENV_PATH)

def _clean(v: str) -> str:
    return (v or "").strip().strip('"').strip("'")

SUPABASE_URL = _clean(os.getenv("SUPABASE_URL"))
SUPABASE_KEY = _clean(os.getenv("SUPABASE_KEY"))

# helpful validation
if not re.match(r"^https://[a-z0-9-]+\.supabase\.co$", SUPABASE_URL):
    raise RuntimeError(f"SUPABASE_URL looks invalid or missing: '{SUPABASE_URL}'")

def get_supabase_client():
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise RuntimeError("Set SUPABASE_URL and SUPABASE_KEY environment variables")
    return create_client(SUPABASE_URL, SUPABASE_KEY)
