from typing import Any, Dict, List

def get_vertical_guidance(guidance: Dict[str, Any], vertical: str) -> str:
    return guidance.get("vertical_guidance", {}).get(vertical, "No guidance available.")

def get_competitor_guidance(guidance: Dict[str, Any], competitor: str) -> str:
    return guidance.get("competitor_guidance", {}).get(competitor, "No guidance available.")

def get_product_guidance(guidance: Dict[str, Any], product: str) -> str:
    return guidance.get("product_guidance", {}).get(product, "No guidance available.")

def get_mkting(guidance: Dict[str, Any], vertical: str) -> List[str]:
    return guidance.get("mkting", {}).get(vertical, [])

import os

def normalize_key(s: str) -> str:
    return "".join(ch.lower() for ch in (s or "") if ch.isalnum())

def load_battlecard(competitor: str, base_dir: str = "battlecards") -> str:
    key = normalize_key(competitor)
    if not key:
        path = os.path.join(base_dir, "_default.md")
        return open(path, "r", encoding="utf-8").read() if os.path.exists(path) else ""
    path = os.path.join(base_dir, f"{key}.md")
    if os.path.exists(path):
        return open(path, "r", encoding="utf-8").read()
    # fallback
    default_path = os.path.join(base_dir, "_default.md")
    return open(default_path, "r", encoding="utf-8").read() if os.path.exists(default_path) else ""