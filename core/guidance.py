from typing import Any, Dict, List

def get_vertical_guidance(guidance: Dict[str, Any], vertical: str) -> str:
    return guidance.get("vertical_guidance", {}).get(vertical, "No guidance available.")

def get_competitor_guidance(guidance: Dict[str, Any], competitor: str) -> str:
    return guidance.get("competitor_guidance", {}).get(competitor, "No guidance available.")

def get_icps(guidance: Dict[str, Any], vertical: str) -> List[str]:
    return guidance.get("icps", {}).get(vertical, [])