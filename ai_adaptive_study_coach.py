#!/usr/bin/env python3

"""Explainable adaptive study coach for an AI education hackathon prototype.



The model uses learner mastery, confidence, available time, and recent error

rate to choose a next step. The examples are synthetic and are not a

psychological or educational assessment.

"""

from dataclasses import dataclass





@dataclass(frozen=True)

class LearnerState:
  
    topic: str
  
    mastery: float       # 0-1
  
    confidence: float    # 0-1
  
    error_rate: float    # 0-1
  
    minutes_left: int
  




def clamp(value: float) -> float:
  
    return max(0.0, min(1.0, value))
  




def recommend(state: LearnerState) -> tuple[str, str]:
  
    """Return an action and a human-readable reason from bounded signals."""
  
    mastery = clamp(state.mastery)
  
    confidence = clamp(state.confidence)
  
    errors = clamp(state.error_rate)
  


    if state.minutes_left < 10:
      
        return "micro_review", "Short time window: review one example and answer one check question."
      
    if errors >= 0.45 or mastery < 0.45:
      
        return "worked_example", "Frequent errors or low mastery: study a worked example before retrying."
      
    if confidence < 0.50:
      
        return "low_stakes_quiz", "Mastery is developing but confidence is low: use a short, low-pressure quiz."
      
    if mastery >= 0.80 and errors < 0.20:
      
        return "transfer_task", "Strong mastery with few errors: apply the idea to a new context."
      
    return "retrieval_practice", "Stable progress: retrieve the concept without notes and explain one step."
  




def coach(states: list[LearnerState]) -> list[tuple[str, str, str]]:
  
    """Create recommendations without storing personally identifying data."""
  
    return [(state.topic, *recommend(state)) for state in states]
  




if __name__ == "__main__":
  
    synthetic_states = [
      
        LearnerState("fractions", 0.35, 0.60, 0.55, 25),
      
        LearnerState("sorting algorithms", 0.82, 0.78, 0.12, 30),
      
        LearnerState("linear equations", 0.62, 0.35, 0.18, 40),
      
        LearnerState("reading comprehension", 0.70, 0.70, 0.20, 7),
      
    ]
  


    print("Adaptive study coach recommendations (synthetic demo)")
  
    for topic, action, reason in coach(synthetic_states):
      
        print(f"{topic:22} -> {action:18} | {reason}")
      
    print("Safety note: recommendations support learning; they do not diagnose ability or disability.")
  




































