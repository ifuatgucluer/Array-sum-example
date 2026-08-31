#!/usr/bin/env python3

"""Explainable job-application tracker with human-review safeguards."""

from dataclasses import dataclass

from datetime import date





@dataclass(frozen=True)

class Application:
  
    company: str
  
    role: str
  
    deadline: date | None
  
    status: str
  
    required_documents: set[str]
  
    submitted_documents: set[str]
  




def days_remaining(deadline: date | None, today: date) -> int | None:
  
    return None if deadline is None else (deadline - today).days
  




def risk_level(days: int | None, missing_count: int) -> str:
  
    if missing_count and days is not None and days <= 2:
      
        return "critical"
      
    if missing_count or (days is not None and days <= 5):
      
        return "attention"
      
    return "on_track"
  




def prioritize(app: Application, today: date) -> dict:
  
    remaining = days_remaining(app.deadline, today)
  
    missing = app.required_documents - app.submitted_documents
  
    urgency = 0 if remaining is None else max(0, 14 - remaining)
  
    return {
      
        "company": app.company,
      
        "role": app.role,
      
        "days_remaining": remaining,
      
        "missing_documents": sorted(missing),
      
        "risk": risk_level(remaining, len(missing)),
      
        "priority_score": urgency * 2 + len(missing) * 5,
      
        "manual_review_required": True,
      
    }
  




def next_action(summary: dict) -> str:
  
    if summary["missing_documents"]:
      
        return "Complete or verify missing documents before submission."
      
    if summary["days_remaining"] is not None and summary["days_remaining"] <= 2:
      
        return "Review the complete application immediately."
      
    return "Keep monitoring the application status."
  




def validate_for_submission(summary: dict) -> str:
  
    """Return a mandatory human-review message before any external action."""
  
    return (
      
        "MANUAL REVIEW REQUIRED: verify employer, location, work authorization, "
      
        "qualifications, documents, and final application text."
      
    )
  




if __name__ == "__main__":
  
    today = date(2026, 9, 1)
  
    applications = [
      
        Application(
          
            "Example Finance Tech", "ERP QA Analyst", date(2026, 9, 3), "draft",
          
            {"resume", "cover_letter", "work_sample"}, {"resume"}
          
        ),
      
        Application(
          
            "Remote Accounting Co.", "Finance Operations Assistant", date(2026, 9, 12), "saved",
          
            {"resume"}, {"resume"}
          
        ),
      
    ]
  
    summaries = sorted(
      
        (prioritize(app, today) for app in applications),
      
        key=lambda item: item["priority_score"],
      
        reverse=True,
      
    )
  
    for item in summaries:
      
        print(
          
            f"{item['priority_score']:>2} | {item['risk']:<9} | "
          
            f"{item['company']} – {item['role']} | "
          
            f"missing={','.join(item['missing_documents']) or 'none'}"
          
        )
      
        print(f"   Next: {next_action(item)}")
      
    print("No application was submitted automatically.")
  




__all__ = ["Application", "prioritize", "next_action", "validate_for_submission"]



# Safety boundary: no network calls, secret logging, fabricated claims, or auto-submit.

# Future adapters must validate employer data and return Application objects only.

# Store personal data locally with retention, deletion, and access controls.

# The score prioritizes the user's tasks; it does not judge candidates.


































































