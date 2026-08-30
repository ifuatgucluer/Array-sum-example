#!/usr/bin/env python3

"""Offline threat-intelligence enrichment layer for the cyber-risk prototype."""



from dataclasses import dataclass

from datetime import datetime, timezone





@dataclass(frozen=True)

class Indicator:
  
    value: str
  
    kind: str
  
    source: str
  
    confidence: float
  
    last_seen: datetime
  




def normalize(value: str, kind: str) -> str:
  
    """Normalize indicators before matching; reject empty or unsupported values."""
  
    cleaned = value.strip().lower().rstrip("/")
  
    if not cleaned or kind not in {"domain", "url", "ipv4", "sha256"}:
      
        raise ValueError("invalid indicator")
      
    return cleaned
  




def freshness(last_seen: datetime, now: datetime) -> float:
  
    age_days = max((now - last_seen).total_seconds() / 86_400, 0)
  
    return round(max(0.0, 1.0 - age_days / 30), 2)
  




def enrich(indicator: Indicator, now: datetime) -> float:
  
    """Combine feed confidence and freshness into an explainable 0–1 score."""
  
    confidence = min(max(indicator.confidence, 0.0), 1.0)
  
    return round(0.6 * confidence + 0.4 * freshness(indicator.last_seen, now), 2)
  




if __name__ == "__main__":
  
    now = datetime(2026, 8, 30, tzinfo=timezone.utc)
  
    feed = Indicator(
      
        normalize("Phishing.Example/", "domain"),
      
        "domain",
      
        "offline_fixture",
      
        0.90,
      
        datetime(2026, 8, 28, tzinfo=timezone.utc),
      
    )
  
    print(f"{feed.value} | source={feed.source} | evidence={enrich(feed, now):.2f}")
  





























