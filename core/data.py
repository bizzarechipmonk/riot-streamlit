import pandas as pd
import json
from typing import Optional, Dict, Any
from core.models import DealContext


def load_opps(path: str = "opportunities.csv") -> pd.DataFrame:
    df = pd.read_csv(path, dtype=str).fillna("")
    df.columns = [c.strip() for c in df.columns]
    # Normalize Id column if needed
    if "Id" not in df.columns and "opp_id" in df.columns:
        df = df.rename(columns={"opp_id": "Id"})
    if "Id" in df.columns:
        df["Id"] = df["Id"].astype(str).str.strip()
    return df

def _pick_account_series(df: pd.DataFrame) -> pd.Series:
    for col in ["AccountName", "Account", "Account Name", "Account_Name", "Account.Name", "Name"]:
        if col in df.columns:
            return df[col].astype(str).fillna("").str.strip()
    return pd.Series([""] * len(df), index=df.index)

def _parse_amount_to_float(raw: str) -> Optional[float]:
    """Parse values like '$74,333' or '74333' to float. Returns None if not parseable."""
    if raw is None:
        return None
    s = str(raw).strip()
    if not s:
        return None
    try:
        cleaned = s.replace("$", "").replace(",", "").strip()
        return float(cleaned)
    except Exception:
        return None

def load_guidance(path: str = "guidance.json") -> Dict[str, Any]:
    with open(path, "r") as f:
        return json.load(f)

def find_opp(df: pd.DataFrame, opp_id: str) -> Optional[pd.Series]:
    opp_id = (opp_id or "").strip()
    if not opp_id:
        return None
    if "Id" not in df.columns:
        raise KeyError("opportunities.csv is missing an 'Id' column.")
    match = df[df["Id"] == str(opp_id)]
    if match.empty:
        return None
    return match.iloc[0]

def _pick_value(row: pd.Series, candidates: list[str], default: str = "—") -> str:
    for col in candidates:
        if col in row.index:
            val = str(row.get(col, "")).strip()
            if val != "":
                return val
    return default

def get_opp_context(opp_row):
    def pick(row, candidates):
        for col in candidates:
            if col in row.index:
                val = str(row.get(col, "")).strip()
                if val:
                    return val
        return ""

    account = pick(opp_row, ["AccountName", "Account", "Account Name", "Account_Name", "Account.Name", "Name"])
    amount_raw = pick(opp_row, ["Amount", "OpportunityAmount", "OppAmount", "ACV", "ARR"])
    stage = pick(opp_row, ["StageName", "Stage", "Stage Name", "SalesStage"])
    vertical = pick(opp_row, ["Vertical", "IndustryVertical", "Vert"])
    competitor = pick(opp_row, ["Competitor", "PrimaryCompetitor", "Primary Competitor"])
    owner = pick(opp_row, ["Owner", "OwnerName"])
    close_date = pick(opp_row, ["CloseDate", "Close Date"])
    region = pick(opp_row, ["Region", "Territory"])

    # Convert amount to float safely
    amount = None
    if amount_raw:
        try:
            cleaned = (
                amount_raw
                .replace("$", "")
                .replace(",", "")
                .strip()
            )
            amount = float(cleaned)
        except Exception:
            amount = None

    return DealContext(
        opp_id=str(opp_row.get("Id", "")).strip(),
        account=account or "—",
        amount=amount,
        stage=stage,
        vertical=vertical,
        competitor=competitor or None,
        owner=owner or None,
        close_date=close_date or None,
        region=region or None,
    )

def find_similar_opps_by_amount_and_vertical(
    df: pd.DataFrame,
    opp_id: str,
    vertical: str,
    amount: Optional[float],
    n: int = 10,
    pct_band: float = 0.25,   # +/- 25% by default
    min_floor: float = 10000, # at least +/- $10k band for small deals
) -> pd.DataFrame:
    """
    Find opportunities in the same vertical with similar amounts.
    Returns a dataframe with Id, Account, Vertical.
    """
    if "Id" not in df.columns:
        return df.head(0)

    # Base filter: exclude self + match vertical if possible
    filt = (df["Id"].astype(str).str.strip() != str(opp_id).strip())
    if vertical and "Vertical" in df.columns:
        filt &= (df["Vertical"].astype(str).str.strip() == str(vertical).strip())

    candidates = df.loc[filt].copy()

    # Add Account display column
    candidates["_AccountDisplay"] = _pick_account_series(candidates)

    # If amount is missing, just return same-vertical candidates
    if amount is None:
        out_cols = [c for c in ["Id", "_AccountDisplay", "Vertical"] if c in candidates.columns]
        out = candidates[out_cols].head(n).rename(columns={"_AccountDisplay": "Account"})
        return out

    # Determine which amount column exists
    amount_col = None
    for col in ["Amount", "OpportunityAmount", "OppAmount", "ACV", "ARR"]:
        if col in candidates.columns:
            amount_col = col
            break

    if amount_col is None:
        out_cols = [c for c in ["Id", "_AccountDisplay", "Vertical"] if c in candidates.columns]
        out = candidates[out_cols].head(n).rename(columns={"_AccountDisplay": "Account"})
        return out

    # Parse amounts to float and filter by similarity band
    candidates["_AmountFloat"] = candidates[amount_col].apply(_parse_amount_to_float)
    candidates = candidates.dropna(subset=["_AmountFloat"])

    band = max(amount * pct_band, min_floor)
    low, high = amount - band, amount + band

    candidates = candidates[(candidates["_AmountFloat"] >= low) & (candidates["_AmountFloat"] <= high)]

    # Sort by closeness to target amount
    candidates["_AmountDiff"] = (candidates["_AmountFloat"] - amount).abs()
    candidates = candidates.sort_values("_AmountDiff", ascending=True)

    out = candidates[[c for c in ["Id", "_AccountDisplay", "Vertical"] if c in candidates.columns]].head(n)
    out = out.rename(columns={"_AccountDisplay": "Account"})
    return out