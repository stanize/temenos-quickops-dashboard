import json
import re
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

import requests

@dataclass
class OfsResult:
    ok: bool
    status_code: Optional[str]
    ofs_response: str
    transact_date: Optional[str]
    error: Optional[str] = None


def _extract_status_code(ofs_response: str) -> Optional[str]:
    """
    Expected format includes slash-separated parts, and status code is the 3rd segment.
    Example (conceptual): "....../....../1,...."
    """
    try:
        parts = ofs_response.split("/")
        if len(parts) < 3:
            return None
        third = parts[2]
        return third.split(",")[0].strip()
    except Exception:
        return None


def _extract_first_date_iso(ofs_response: str) -> Optional[str]:
    """
    Finds first date like '04 JUN 2025' in the ofsResponse and returns ISO '2025-06-04'
    """
    m = re.search(r"\b(\d{2})\s+([A-Z]{3})\s+(\d{4})\b", ofs_response)
    if not m:
        return None

    dd, mon, yyyy = m.group(1), m.group(2), m.group(3)

    # Python %b expects title case (Jun), so convert
    mon_title = mon.capitalize()

    try:
        dt = datetime.strptime(f"{dd} {mon_title} {yyyy}", "%d %b %Y")
        return dt.strftime("%Y-%m-%d")
    except Exception:
        return None


def enquiry_dates_list(
    *,
    endpoint: str,
    basic_auth_b64: str,
    user: str,
    password: str,
    enquiry_name: str = "DATES.LIST",
    timeout_seconds: int = 10,
) -> OfsResult:
    """
    Performs login validation by calling:
      ENQUIRY.SELECT,,<USER>/<PASS>,DATES.LIST

    Success condition:
      status_code == "1"
    """
    ofs_request = f"ENQUIRY.SELECT,,{user}/{password},{enquiry_name} "

    headers = {
        "Authorization": f"Basic {basic_auth_b64}",
        "content-type": "application/json",
        "cache-control": "no-cache",
    }

    payload = {"ofsRequest": ofs_request}

    try:
        resp = requests.post(endpoint, headers=headers, json=payload, timeout=timeout_seconds)
        resp.raise_for_status()

        data = resp.json()
        ofs_response = str(data.get("ofsResponse", "")).strip()

        status_code = _extract_status_code(ofs_response)
        transact_date = _extract_first_date_iso(ofs_response)

        ok = (status_code == "1")
        return OfsResult(
            ok=ok,
            status_code=status_code,
            ofs_response=ofs_response,
            transact_date=transact_date if ok else None,
            error=None if ok else "OFS processed but status_code != 1",
        )

    except requests.RequestException as e:
        return OfsResult(
            ok=False,
            status_code=None,
            ofs_response="",
            transact_date=None,
            error=f"HTTP error: {e}",
        )
    except json.JSONDecodeError:
        return OfsResult(
            ok=False,
            status_code=None,
            ofs_response=resp.text if "resp" in locals() else "",
            transact_date=None,
            error="Response was not valid JSON",
        )
    except Exception as e:
        return OfsResult(
            ok=False,
            status_code=None,
            ofs_response="",
            transact_date=None,
            error=f"Unexpected error: {e}",
        )

