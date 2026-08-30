#!/usr/bin/env python3

"""Prioritize everyday digital safety alerts by urgency and potential impact."""



from dataclasses import dataclass





@dataclass(frozen=True)

class Alert:
  
    source: str
  
    signal: str
  
    importance: int  # 1–5: potential damage
  
    urgency: int  # 1–5: time pressure
  




def prioritize(alerts: list[Alert]) -> list[tuple[Alert, float]]:
  
    """Return alerts ranked by a simple explainable risk score."""
  
    scored = [(alert, round(alert.importance * alert.urgency / 5, 2)) for alert in alerts]
  
    return sorted(scored, key=lambda pair: pair[1], reverse=True)
  




if __name__ == "__main__":
  
    alerts = [
      
        Alert("bank_sms", "unknown_link", 5, 5),
      
        Alert("social_media", "login_notice", 4, 3),
      
        Alert("newsletter", "routine_offer", 1, 1),
      
    ]
  
    for alert, score in prioritize(alerts):
      
        print(f"{score:.2f} | {alert.source}: {alert.signal}")
      

















