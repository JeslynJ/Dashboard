import re
from typing import List, Tuple

CYBERBULLY = [r"\bidiot\b", r"\bstupid\b", r"\bkill yourself\b", r"\bhate\b"]
HATE_SPEECH = [r"\bracist\b", r"\bterrorist\b", r"\bgo back\b"]
MISINFO = [r"\bfake news\b", r"\bhoax\b", r"\bmisleading\b"]
MENTAL_HEALTH = [r"\bdepress\b", r"\bsuicid\b", r"\blonely\b", r"\bself harm\b"]
SCAM_PHISH = [r"\bverify your account\b", r"\bfree\b", r"\bprize\b", r"\bwin\b", r"\botp\b", r"\bpassword\b", r"\blogin\b"]
HACKING = [r"\bhack(?:ed|ing)?\b", r"\bbreach\b", r"\bexploit\b"]
PRIVACY = [r"\bprivacy\b", r"\bexpose(?:d)?\b", r"\bdoxx?\b"]

SUSPICIOUS_DOMAINS = ["bit.ly", "tinyurl.com", "t.co"]

CATEGORY_ORDER = [
    ("Scam/Phishing", SCAM_PHISH, "high"),
    ("Hacking/Exploit", HACKING, "high"),
    ("Hate Speech", HATE_SPEECH, "medium"),
    ("Cyberbullying", CYBERBULLY, "medium"),
    ("Misinformation", MISINFO, "medium"),
    ("Privacy Risk", PRIVACY, "medium"),
    ("Mental Health Risk", MENTAL_HEALTH, "medium"),
]

def _match_any(text: str, patterns: List[str]) -> bool:
    for p in patterns:
        if re.search(p, text, flags=re.IGNORECASE):
            return True
    return False

def classify(text: str, domains: List[str]) -> Tuple[str, str]:
    # domain heuristic
    if any(d in SUSPICIOUS_DOMAINS for d in (domains or [])):
        return "Scam/Phishing", "high"
    for name, patterns, risk in CATEGORY_ORDER:
        if _match_any(text or "", patterns):
            return name, risk
    return "Neutral", "low"
